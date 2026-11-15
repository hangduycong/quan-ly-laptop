import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { providers } from '../skills/talking-head/scripts/providers.mjs';

test('provider adapters use real SDK storage and correct API bodies without live requests', async t => {
  const root = await mkdtemp(resolve(tmpdir(), 'talking-head-contract-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const sample = resolve(root, 'voice.mp3'); await writeFile(sample, Buffer.alloc(200));
  const original = globalThis.fetch;
  const oldFal = process.env.FAL_KEY, oldEleven = process.env.ELEVENLABS_API_KEY;
  process.env.FAL_KEY = 'test-fal-key'; process.env.ELEVENLABS_API_KEY = 'test-eleven-key';
  t.after(() => { globalThis.fetch = original; if (oldFal === undefined) delete process.env.FAL_KEY; else process.env.FAL_KEY = oldFal; if (oldEleven === undefined) delete process.env.ELEVENLABS_API_KEY; else process.env.ELEVENLABS_API_KEY = oldEleven; });
  const calls = [];
  globalThis.fetch = async (url, options = {}) => {
    url = String(url); calls.push({ url, options });
    if (url.includes('/storage/upload/initiate')) return Response.json({ upload_url: 'https://storage.example.com/put', file_url: 'https://storage.example.com/file.mp3' });
    if (url === 'https://storage.example.com/put') return new Response('');
    if (url.endsWith('/voices/add')) { assert.equal(options.body.get('name'), 'Example'); assert.ok(options.body.get('files') instanceof Blob); return Response.json({ voice_id: 'new-voice', requires_verification: false }); }
    if (url.includes('/with-timestamps')) { assert.equal(JSON.parse(options.body).model_id, 'eleven_multilingual_v2'); return Response.json({ audio_base64: 'fixture' }); }
    if (url.endsWith('/speech-to-text')) { assert.equal(options.body.get('model_id'), 'scribe_v2'); assert.equal(options.body.get('timestamps_granularity'), 'word'); return Response.json({ text: 'Hello' }); }
    if (url.endsWith('/reference-to-video')) { const body = JSON.parse(options.body); assert.equal(body.resolution, '768P'); assert.equal(body.prompt_expansion_mode, 'disabled'); assert.equal(body.reference_audio_urls.length, 1); return Response.json({ request_id: 'test-123' }); }
    if (url.endsWith('/status')) return Response.json({ status: 'COMPLETED' });
    if (url.endsWith('/requests/test-123')) return Response.json({ video: { url: 'https://storage.example.com/video.mp4' } }, { headers: { 'x-fal-billable-units': '6' } });
    throw new Error(`Unexpected request: ${url}`);
  };
  const api = providers();
  assert.equal(await api.upload(sample), 'https://storage.example.com/file.mp3');
  await api.clone('Example', sample); await api.tts('voice-id', 'Hello'); await api.transcribe(sample);
  await api.submit({ resolution: '768P', prompt_expansion_mode: 'disabled', reference_audio_urls: ['https://storage.example.com/file.mp3'] });
  await api.status('test-123'); const result = await api.result('test-123'); assert.equal(result.billable_units, '6');
  assert.ok(calls.some(c => c.url === 'https://queue.fal.run/minimax/h3/requests/test-123/status'));
  const upload = calls.find(c => c.url === 'https://storage.example.com/put');
  assert.ok(!new Headers(upload.options.headers).has('Authorization'), 'fal API key must not be sent to the upload host');
});
