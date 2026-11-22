import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { preparePerson } from '../skills/talking-head/scripts/prepare-person.mjs';
import { probe, readJSON } from '../skills/talking-head/scripts/core.mjs';

test('self-recorded video prepares reusable identity assets entirely locally', { timeout: 60_000 }, async t => {
  const root = await mkdtemp(resolve(tmpdir(), 'talking-head-person-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const video = resolve(root, 'my recording.mov');
  execFileSync('ffmpeg', ['-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=160x240:r=10:d=3', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', video]);
  const original = await readFile(video);

  await t.test('CLI works without provider keys and produces three default candidates', async () => {
    const env = { ...process.env };
    for (const key of ['FAL_KEY', 'FAL_API_KEY', 'ELEVENLABS_API_KEY']) delete env[key];
    const out = resolve(root, 'default');
    const result = JSON.parse(execFileSync(process.execPath, [resolve('skills/talking-head/scripts/talking-head.mjs'), 'prepare-person', '--video', video, '--out', out], { env, encoding: 'utf8' }));
    assert.equal(result.images.length, 3);
    assert.deepEqual(result, await readJSON(resolve(out, 'person.json')));
    assert.ok(Math.abs(result.audio_duration - 3) < 0.1);
    for (const file of [...result.images, result.contact_sheet]) {
      const bytes = await readFile(resolve(out, file));
      assert.equal(bytes.readUInt16BE(0), 0xffd8, 'actual JPEG output');
      assert.ok(bytes.length > 1000);
    }
  });

  await t.test('selected timestamps and speech interval preserve portrait geometry and audible audio', async () => {
    const out = resolve(root, 'selected');
    const result = await preparePerson({ video, out, frameTimes: [0.2, 0.7, 1.2, 2.2], audioStart: 0.5, audioDuration: 1.5 });
    assert.deepEqual(result.frames.map(f => f.time), [0.2, 0.7, 1.2, 2.2]);
    assert.ok(Math.abs(result.audio_duration - 1.5) < 0.1);
    const info = file => JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_streams', '-of', 'json', resolve(out, file)], { encoding: 'utf8' })).streams[0];
    assert.equal(info('portrait-01.jpg').width, 160);
    assert.equal(info('portrait-01.jpg').height, 240);
    assert.equal(info('frames.jpg').width, 960);
    assert.equal(info('frames.jpg').height, 960);
    const audio = info('voice.wav');
    assert.equal(audio.channels, 1); assert.equal(audio.sample_rate, '44100');
    const pcm = execFileSync('ffmpeg', ['-v', 'error', '-i', resolve(out, 'voice.wav'), '-f', 's16le', 'pipe:1']);
    let power = 0; for (let i = 0; i + 1 < pcm.length; i += 2) power += pcm.readInt16LE(i) ** 2;
    assert.ok(power / (pcm.length / 2) > 10000);
    assert.equal(probe(resolve(out, 'voice.wav')).audio, true);
    await assert.rejects(preparePerson({ video, out }), /already exists/);
    assert.deepEqual(await readJSON(resolve(out, 'person.json')), result);
  });

  await t.test('invalid selections fail before creating output', async () => {
    const out = resolve(root, 'invalid');
    for (const options of [{ frameTimes: [] }, { frameTimes: [NaN] }, { frameTimes: [3] }, { audioStart: -1 }, { audioDuration: 4 }]) {
      await assert.rejects(preparePerson({ video, out, ...options }), /must/);
      await assert.rejects(access(out), { code: 'ENOENT' });
    }
    const cli = spawnSync(process.execPath, [resolve('skills/talking-head/scripts/talking-head.mjs'), 'prepare-person', '--video', video, '--out', out, '--frame-times', '0.2,,1'], { encoding: 'utf8' });
    assert.equal(cli.status, 1); assert.match(cli.stderr, /frame-times/);
    await assert.rejects(access(out), { code: 'ENOENT' });
  });

  await t.test('missing audio or video directs the user to the other input path', async () => {
    const silent = resolve(root, 'silent.mp4');
    execFileSync('ffmpeg', ['-v', 'error', '-i', video, '-an', '-c:v', 'copy', silent]);
    await assert.rejects(preparePerson({ video: silent, out: resolve(root, 'no-audio') }), /no audio track/);
    await assert.rejects(preparePerson({ video: resolve(root, 'default/voice.wav'), out: resolve(root, 'no-video') }), /no video track/);
  });
  assert.deepEqual(await readFile(video), original, 'source recording remains byte-for-byte unchanged');
});
