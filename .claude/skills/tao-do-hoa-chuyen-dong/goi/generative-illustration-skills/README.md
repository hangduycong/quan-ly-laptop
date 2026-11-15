# Generative Illustration Skills

> Generative-illustration / 动态平面 skills for AI coding agents — **AI generates the illustration parts, code structures and animates them** into expressive, concept-driven pieces (motion poems, visual metaphors, ambient brand art).

![Generative Illustration Skills — animated showcase](./showcase.gif)

Not the same as [motion-design-skills](https://github.com/iart-ai/motion-design-skills) (timing/easing/AE/Remotion craft for visuals you already have). This pack is about *making the visuals generatively* — an AI draws the independent parts, and code gives them structure, life, and meaning.

## Install

```bash
npx skills add iart-ai/generative-illustration-skills
```

Or add it as a Claude Code plugin marketplace:

```bash
/plugin marketplace add iart-ai/generative-illustration-skills
```

## Requirements

**One API key.** AI generation (assets + music) uses an **OpenRouter** key — set `OPENROUTER_API_KEY`; it covers all three models this skill uses:

- vectors → `recraft/recraft-v4.1-vector`
- textures → `google/gemini-2.5-flash-image`
- music → `google/lyria-3-clip-preview`

Rendering itself needs no key. Optional: `REPLICATE_API_KEY` (cheaper Recraft), Google `GEMINI_KEY` (Lyria direct), or bring your own assets/music. (Render toolchain — Node + Playwright + ffmpeg — is documented in `references/render-harness.md`.)

## What's included

| Skill | What it does |
|---|---|
| [generative-illustration](./skills/generative-illustration) | Generate isolated illustration assets with AI, composite them as sprites, and animate them frame-accurately into poetic, concept-driven motion. Covers asset prompting, background-stripping, a deterministic seek-harness render, and the craft (causality, restraint, rhythm). |

## The one idea

Don't try to animate one big AI illustration (you get a PowerPoint, or an uncanny wobble). **Generate many small independent elements and let code animate each as a whole unit** — the structure lives *between* assets, not inside one image.

---

The full agent runs at **[iart.ai](https://iart.ai)**.
