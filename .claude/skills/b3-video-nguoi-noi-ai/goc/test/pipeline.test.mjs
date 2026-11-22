import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { generate, recover, cloneVoice, withLock } from '../skills/talking-head/scripts/pipeline.mjs';
import { shotDuration, speechComparison, readJSON } from '../skills/talking-head/scripts/core.mjs';

const base = {
  voice_id: 'testvoice', language: 'English', aspect_ratio: '16:9', resolution: '768P', images: ['face.jpg'],
  scenes: [{ id: 'hello', kind: 'talking', text: 'Hello from the test studio.', heading: 'Test studio' }],
};
async function setup(t, customize = () => {}) {
  const root = await mkdtemp(resolve(tmpdir(), 'talking-head-test-')); t.after(() => rm(root, { recursive: true, force: true }));
  await writeFile(resolve(root, 'face.jpg'), 'test-image');
  const plan = structuredClone(base); customize(plan); const planFile = resolve(root, 'plan.json');
  await writeFile(planFile, JSON.stringify(plan));
  const calls = { tts: 0, upload: 0, submit: 0, status: 0, result: 0, download: 0, transcribe: 0 };
  const api = {
    async tts(_voice, text) { calls.tts++; return { audio_base64: Buffer.alloc(200, 1).toString('base64'), alignment: { characters: Array.from(text), character_start_times_seconds: Array.from(text, (_, i) => i * 0.1), character_end_times_seconds: Array.from(text, (_, i) => (i + 1) * 0.1) } }; },
    async upload() { calls.upload++; return 'https://example.com/asset'; },
    async submit() { calls.submit++; return { request_id: 'request-123' }; },
    async status() { calls.status++; return { status: 'COMPLETED' }; },
    async result() { calls.result++; return { video: { url: 'https://example.com/video.mp4' }, billable_units: '6' }; },
    async download() { calls.download++; return Buffer.alloc(200); },
    async transcribe() { calls.transcribe++; return { text: base.scenes[0].text, words: [{ type: 'word', text: base.scenes[0].text, start: 0.1, end: 2.8 }] }; },
  };
  const options = { planFile, out: resolve(root, 'run') };
  const runtime = { probe: path => ({ duration: path.endsWith('.mp4') ? 5 : 3, audio: true, video: path.endsWith('.mp4') }), log() {}, sleep: async () => {} };
  return { root, plan, calls, api, options, runtime, run: () => generate(options, api, runtime) };
}

test('completed runs resume without repeating any provider operation', async t => {
  const f = await setup(t); const film = await f.run(); const calls = { ...f.calls };
  assert.equal(film.scenes[0].words[0].start, 0.1); assert.equal(film.duration, 5);
  assert.equal(film.scenes[0].comparison.status, 'match');
  await f.run(); assert.deepEqual(f.calls, calls);
});
test('a lost submission is not repeated and can adopt the existing request', async t => {
  const f = await setup(t); f.api.submit = async () => { f.calls.submit++; throw new Error('network lost'); };
  await assert.rejects(f.run(), /network lost/);
  await assert.rejects(f.run(), /Check the provider dashboard/);
  assert.equal(f.calls.submit, 1);
  await recover({ out: f.options.out, scene: 'hello', requestId: 'recovered-123' });
  await f.run(); assert.equal(f.calls.submit, 1); assert.equal(f.calls.tts, 1);
});
test('a TTS timeout does not buy a duplicate on resume', async t => {
  const f = await setup(t); const original = f.api.tts;
  f.api.tts = async () => { f.calls.tts++; throw new Error('TTS timed out'); };
  await assert.rejects(f.run(), /TTS timed out/); await assert.rejects(f.run(), /retry-tts/);
  assert.equal(f.calls.tts, 1); assert.equal(f.calls.submit, 0);
  f.api.tts = original; f.options.retryTts = 'hello'; await f.run(); assert.equal(f.calls.tts, 2);
});
test('download errors resume the paid request instead of submitting again', async t => {
  const f = await setup(t); const original = f.api.download;
  f.api.download = async () => { throw new Error('download lost'); };
  await assert.rejects(f.run(), /download lost/);
  f.api.download = original; await f.run(); assert.equal(f.calls.submit, 1); assert.equal(f.calls.result, 1);
});
test('queue waiting limit retains the request', async t => {
  const f = await setup(t); f.options.waitSeconds = 0;
  f.api.status = async () => ({ status: 'IN_PROGRESS' });
  await assert.rejects(f.run(), /Waiting limit/);
  f.api.status = async () => ({ status: 'COMPLETED' }); await f.run(); assert.equal(f.calls.submit, 1);
});
test('a completed provider error is not resubmitted', async t => {
  const f = await setup(t); f.api.result = async () => { throw new Error('H3 result: HTTP 422'); };
  await assert.rejects(f.run(), /422/); await assert.rejects(f.run(), /422/); assert.equal(f.calls.submit, 1);
});
test('changed photos or script cannot reuse an incompatible paid run', async t => {
  const f = await setup(t); await f.run(); await writeFile(resolve(f.root, 'face.jpg'), 'different-image');
  await assert.rejects(f.run(), /contents changed/); assert.equal(f.calls.submit, 1);
});
test('actual speech exceeding the provider limit stops before H3 is purchased', async t => {
  const f = await setup(t); f.runtime.probe = () => ({ duration: 14.8, audio: true });
  await assert.rejects(f.run(), /split a long one/); assert.equal(f.calls.submit, 0);
});
test('the H3 seconds cap stops before any H3 submission and speech is retained', async t => {
  const f = await setup(t, p => p.scenes.push({ ...p.scenes[0], id: 'again' })); f.options.maxVideoSeconds = 5;
  await assert.rejects(f.run(), /exceeding/); assert.equal(f.calls.submit, 0);
  f.options.maxVideoSeconds = 10; await f.run(); assert.equal(f.calls.tts, 2);
});
test('dry-run never calls a provider and does not create a run', async t => {
  const f = await setup(t); f.options.dryRun = true; const result = await f.run();
  assert.equal(result.paidRequests, 0); assert.equal(Object.values(f.calls).reduce((a, b) => a + b, 0), 0);
  await assert.rejects(readFile(resolve(f.options.out, 'state.json')), { code: 'ENOENT' });
});
test('transcript mismatches are surfaced without automatic paid retries', async t => {
  const f = await setup(t); f.api.transcribe = async () => ({ text: 'Something else entirely.', words: [{ type: 'word', text: 'Something', start: 0.1, end: 1 }] });
  const film = await f.run(); assert.equal(film.scenes[0].comparison.status, 'review'); assert.equal(f.calls.submit, 1);
  assert.equal((await readJSON(resolve(f.options.out, 'verification.json'))).scenes[0].status, 'review');
});
test('locking excludes a second writer', async t => {
  const f = await setup(t); const lock = resolve(f.root, 'lock');
  await withLock(lock, async () => { await assert.rejects(withLock(lock, async () => {}), /Another run owns/); });
  await withLock(lock, async () => {});
});
test('voice cloning refuses an unauthorized operation before touching the provider', async () => {
  await assert.rejects(cloneVoice({ name: 'x', sample: 'missing.wav', out: 'unused.json' }, { clone() { throw new Error('must not run'); } }), /consent/);
});
test('duration does not truncate long speech, and text comparison handles CJK', () => {
  assert.equal(shotDuration(3), 5); assert.equal(shotDuration(12.7), 15);
  assert.throws(() => shotDuration(13), /split/);
  assert.equal(speechComparison('你好，世界！', '你好世界').status, 'match');
  assert.equal(speechComparison('Hello.', 'Hello. Buy now.').status, 'review');
});
