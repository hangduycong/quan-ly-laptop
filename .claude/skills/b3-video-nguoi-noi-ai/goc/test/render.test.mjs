import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, copyFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { generate, cloneVoice } from '../skills/talking-head/scripts/pipeline.mjs';
import { renderFilm } from '../skills/talking-head/scripts/render.mjs';
import { probe, readJSON } from '../skills/talking-head/scripts/core.mjs';

test('synthetic media runs through generation, transcription and real ffmpeg composition', { timeout: 120_000 }, async t => {
  const root = await mkdtemp(resolve(tmpdir(), 'talking-head-media-'));
  if (!process.env.KEEP_TEST_MEDIA) t.after(() => rm(root, { recursive: true, force: true }));
  else console.log(`Offline media fixture (not an H3 sample): ${root}`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1.5', '-c:a', 'libmp3lame', resolve(root, 'voice.mp3')]);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=0x344959:s=640x360:r=30:d=5', '-f', 'lavfi', '-i', 'sine=frequency=220:duration=5', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', resolve(root, 'clip.mp4')]);
  const { createCanvas } = await import('../skills/talking-head/node_modules/@napi-rs/canvas/index.js');
  const canvas = createCanvas(64, 64); canvas.getContext('2d').fillRect(0, 0, 64, 64);
  await writeFile(resolve(root, 'face.png'), canvas.toBuffer('image/png'));
  const plan = { language: 'English', voice_id: 'testvoice', images: ['face.png'], aspect_ratio: '16:9', resolution: '768P', scenes: [
    { id: 'intro', kind: 'talking', text: 'A synthetic test clip.', heading: 'Offline rendering test' },
    { id: 'steps', kind: 'motion', text: 'Write, speak and explain.', heading: 'Make the message visible', points: ['Write your message', 'Choose the on-camera lines', 'Explain with motion'] },
  ] };
  await writeFile(resolve(root, 'plan.json'), JSON.stringify(plan));
  const audio = await readFile(resolve(root, 'voice.mp3')), video = await readFile(resolve(root, 'clip.mp4'));
  const api = {
    async tts(_voice, text) { return { audio_base64: audio.toString('base64'), alignment: { characters: Array.from(text), character_start_times_seconds: Array.from(text, (_, i) => i * 1.2 / text.length), character_end_times_seconds: Array.from(text, (_, i) => (i + 1) * 1.2 / text.length) } }; },
    async upload() { return 'https://example.com/fixture'; }, async submit() { return { request_id: 'fixture-id' }; },
    async status() { return { status: 'COMPLETED' }; }, async result() { return { video: { url: 'https://example.com/fixture' } }; },
    async download() { return video; }, async transcribe() { return { text: plan.scenes[0].text, words: [{ type: 'word', text: 'A synthetic test clip.', start: 0.2, end: 2.4 }] }; },
  };
  const out = resolve(root, 'run');
  await generate({ planFile: resolve(root, 'plan.json'), out }, api);
  assert.ok(probe(resolve(out, 'intro.reference.mp3')).duration >= 2, 'short reference speech is padded locally');
  const result = await renderFilm({ manifestFile: resolve(out, 'film.json') });
  assert.equal(probe(result.file).audio, true); assert.ok(result.duration > 6.5 && result.duration < 6.8);
  assert.ok((await readFile(resolve(out, 'review/intro-middle.jpg'))).length > 1000);
  const report = await readJSON(resolve(out, 'render-report.json')); assert.deepEqual(report.transcriptReview, []);
  // Audio is actually present, not merely a silent audio stream.
  const pcm = execFileSync('ffmpeg', ['-v', 'error', '-i', result.file, '-t', '1', '-f', 's16le', '-ac', '1', '-ar', '8000', 'pipe:1']);
  let power = 0; for (let i = 0; i + 1 < pcm.length; i += 2) power += pcm.readInt16LE(i) ** 2;
  assert.ok(power / (pcm.length / 2) > 10000);
  // A saved clone is reusable, and provider verification is not lost.
  let clones = 0;
  const options = { name: 'Test voice', sample: resolve(root, 'voice.mp3'), out: resolve(root, 'voice.json'), consent: true };
  const cloneApi = { async clone() { clones++; return { voice_id: 'createdvoice', requires_verification: true }; } };
  assert.equal((await cloneVoice(options, cloneApi)).requires_verification, true);
  assert.equal((await cloneVoice(options, cloneApi)).voice_id, 'createdvoice'); assert.equal(clones, 1);
});
