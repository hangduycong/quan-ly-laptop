# Talking Head Skills

**Make a video with your face, your voice and your words.** Give your agent your own photos and a voice recording, or a video of yourself speaking. It uses your appearance and voice to make AI talking-head shots from a new script, with narration and editable motion graphics.

Bring your own **fal** and **ElevenLabs** API keys. ElevenLabs clones the voice and speaks the script; MiniMax H3 uses the photos and speech to generate the on-camera performance. The rest of the film can be drawn as motion graphics and rendered locally.

[![A generated presenter introduces one idea, followed by animated steps](showcase.gif)](examples/one-idea/film.mp4)

[Watch the 11-second example with sound](examples/one-idea/film.mp4). One 5-second H3 request, then locally rendered motion graphics. The reference portrait is an AI-generated presenter and the voice is ElevenLabs' premade Sarah voice. H3 cost: **$0.30**, excluding speech and transcription. [Inputs, editable artwork and validation notes](examples/one-idea/README.md).

Early release: this sample verifies the real TTS → H3 → transcription → render path. Voice-clone creation and recovery are covered by mocked-provider tests; a fresh personal voice clone was not created for the sample. Review likeness and lip sync on your own material before publishing it.

## Install

```bash
npx skills add iart-ai/talking-head-skills
```

Or use it as a Claude Code plugin:

```text
/plugin marketplace add iart-ai/talking-head-skills
/plugin install talking-head-skills
```

Then ask your agent:

> Use portrait.jpg and my voice recording to make a short introduction. Open with me speaking, explain the steps with motion graphics, then bring me back for the close. Use fal H3 and ElevenLabs; keep it under 20 seconds of generated on-camera footage.

Or start with a video you record yourself:

> Here's me.mov, a video of me talking to camera. Extract clear photos and my voice, then make an AI version of me delivering this new script. Add motion graphics to explain the steps.

Already have a cloned voice? Give the agent its ElevenLabs voice ID. No need to clone it again. Use your own likeness and voice or material you have permission to use.

## What you need

| Requirement | Purpose |
|---|---|
| `FAL_KEY` with credits | MiniMax H3 reference-to-video |
| `ELEVENLABS_API_KEY` and access to voice cloning | Create your voice, synthesize speech and transcribe generated shots |
| 1–9 photos of the same person | First photo sets the look and room; others help identity |
| A clean voice recording, or an existing voice ID | The speaker's voice |
| A script or a topic | What the film says |
| Node.js 22+, pnpm, FFmpeg/ffprobe | Local scripts and video rendering |

`FAL_API_KEY` is also accepted as an alias for `FAL_KEY`.

The skill installs `@fal-ai/client` and `@napi-rs/canvas` in its own directory. No iArt account, database, Vercel deployment or GPU is needed. fal and ElevenLabs bill your accounts; the MIT license covers this repository's code, not free model inference.

**A single self-recorded video can supply both the photos and voice recording.** Record yourself with your phone or webcam, ideally 30–60 seconds with one speaker, a clearly visible face and clean speech. Save the file and give it to your agent. Camera capture itself uses your usual camera app; this package provides local extraction and the generation workflow.

## How it works

1. **Clone once.** Create a voice in ElevenLabs, or reuse an existing voice ID.
2. **Plan the film.** Decide which lines need a face and which need a diagram, comparison or other motion graphic.
3. **Speak, then film.** Generate each line with ElevenLabs. Give H3 the photos and the on-camera line's audio. Actual speech length sets the video duration.
4. **Check the words.** Transcribe H3's returned video and flag differences from the script.
5. **Draw and render.** Edit the Canvas artwork, composite it over speaking shots, render full-frame motion scenes, and export an MP4.

H3 creates its own audio using the supplied take as a reference. It does not guarantee exact audio reproduction or frame-perfect lip sync. The compositor keeps that generated sound on speaking shots, and uses ElevenLabs audio on motion scenes. Review voice likeness, delivery and joins before sharing.

## Run it yourself

```bash
git clone https://github.com/iart-ai/talking-head-skills.git
cd talking-head-skills
pnpm run setup
cp .env.example .env
# Set your two keys in .env. Keep it private.
```

Put your photos and recording in the ignored `inputs/` folder. Commands that call providers use Node's built-in `.env` support.

If starting from a self-recorded video, first extract its identity assets locally:

```bash
node skills/talking-head/scripts/talking-head.mjs prepare-person \
  --video inputs/me.mov --out inputs/person
```

Inspect `inputs/person/frames.jpg` and the full-size portraits; choose a sharp face with open eyes. Listen to `inputs/person/voice.wav` for clean speech. The script samples frames and extracts audio; it does not automatically judge face quality or voice-clone suitability. It needs no API keys and leaves the recording unchanged. See [video input options](skills/talking-head/references/workflow.md#self-recorded-video) for selecting timestamps, audio intervals and SDR input.

Then clone the voice (for video input, use `inputs/person/voice.wav` as the sample):

```bash
node --env-file=.env skills/talking-head/scripts/talking-head.mjs clone-voice \
  --name 'My voice' --sample inputs/voice.wav --out voice.json --consent
```

Copy `examples/quick-intro/plan.json` to `plan.json`. Set `voice_id` from the result and change the image path to your photo, such as `inputs/portrait.jpg`, or a selected video frame, such as `inputs/person/portrait-02.jpg`. Customize the script and headings. If ElevenLabs requests verification, complete it before continuing.

```bash
# Local validation only: no uploads or paid API calls.
node --env-file=.env skills/talking-head/scripts/talking-head.mjs generate \
  --plan plan.json --out runs/intro --dry-run

# Paid provider calls. The cap is H3 output seconds, not a dollar budget.
node --env-file=.env skills/talking-head/scripts/talking-head.mjs generate \
  --plan plan.json --out runs/intro --max-video-seconds 30

# Edit runs/intro/visuals.mjs to fit the story; then render locally.
node skills/talking-head/scripts/talking-head.mjs render --manifest runs/intro/film.json
```

The starter artwork includes a transparent lower third and an animated explainer layout. Your agent can replace it with custom Canvas graphics. Changing artwork and re-rendering does not call a model.

## Outputs

| File | Contents |
|---|---|
| `film.mp4` | Finished film with graphics and sound |
| `visuals.mjs` | Editable, deterministic Canvas artwork |
| `film.json` | Scene order, source files, durations and measured word timings |
| `speech.vtt` | Timed speech sidecar; captions are not burned in |
| `verification.json` | Script/transcript differences to review |
| `review/` | Early, middle and late composited frames of every scene |
| `render-report.json` | Output dimensions, duration, audio and outstanding transcript flags |

Source media, provider responses and request IDs stay in the run directory. Treat it as private. Photos/reference speech are uploaded to fal; voice samples and text are sent to ElevenLabs. The included `.gitignore` excludes `inputs/`, `runs/`, `.env` and `voice.json`.

## Resume without buying the same take again

Repeat the **same generate command with the same output folder**. Completed audio and video are reused, and queued H3 requests are polled by their saved ID. A changed script or image requires a new folder. A lost submission response stops for recovery instead of silently submitting again.

See [the workflow reference](skills/talking-head/references/workflow.md) for request recovery, time limits and supported inputs. The current implementation uses **fal H3 + direct ElevenLabs**. OpenRouter is not yet an implemented alternative.

## Development

```bash
pnpm run setup
pnpm test
```

Tests exercise interrupted paid requests, request recovery, input changes, duration limits, transcript differences, clone reuse and actual FFmpeg composition with synthetic fixtures. They make no paid API calls. The example plan is a starting point, not evidence of model output quality.

## More motion skills

Have an existing recording and want graphics added to it? Use [b-roll-skills](https://github.com/iart-ai/b-roll-skills). This pack generates the speaking footage itself.

Collection: [Motion Skills](https://github.com/iart-ai/motion-skills).

Built by [iart.ai](https://www.iart.ai/?utm_source=github&utm_medium=readme&utm_campaign=talking-head-skills&utm_content=footer).

## License

MIT. Provider services, model licenses and uploaded assets retain their own terms.
