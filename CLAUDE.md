# Illumaesthetic Video Editor — agent instructions

You edit Illumaesthetic videos: real shop footage (Dropbox) combined with 3D scan data
(engineering Google Drive) rendered in Blender, with the signature **1:1 perspective cut** from
the real car to its scan. Every project you finish teaches the next agent.

## Before touching footage (mandatory)
1. Read `knowledge/lessons.md` (standing rules from reviewer feedback — they override everything).
2. Read `knowledge/style-guide.md` and `knowledge/workflow.md`.
3. Read `training/examples/INDEX.md` and the newest two examples' `project.yaml`, `editlog.jsonl`, `feedback.jsonl`.
4. If the request involves a match cut: `knowledge/match-cut.md`. Scan data: `knowledge/scan-pipeline.md`.

## Tools
`python -m ive <cmd>` — fetch-drive, fetch-url, probe, sheet, frame, analyze, beats, decimate, crop,
prep, render, lookat, solve, check, hud, assemble, feedback, log, archive. `--help` on each.
- Blender 5.3 at `/usr/local/bin/blender` (setup: `scripts/setup.sh`). Cycles CPU only.
- Remotion HUD project in `remotion/` (composition `ScanHUD`, driven by JSON props).
- Media is never committed. Work in `/home/user/media/<project>/` and `/home/user/media/work/`.

## While editing
- Log every editorial decision with its reason: `python -m ive log projects/<p> "<what>" --why "<why>"`.
  A decision without a why is useless to the next agent.
- Look at your own output (contact sheets, frames around each cut, check overlays). Never
  report a match as good from the numeric score alone.
- Heavy jobs (Blender renders) run in the background, one at a time.

## After delivering
- Self-score with `training/rubric.md` into `projects/<p>/review.md`.
- Record every piece of user feedback: `python -m ive feedback projects/<p> "<note>" --at <sec> --category <c>`;
  add `--rule` when the user says it applies generally ("always", "never", "from now on").
- `python -m ive archive projects/<p>`, then commit and push.

## Never
- Invent numbers in on-screen text (scanner accuracy, specs). Use data from the files.
- Put text over IRL footage. Use dissolves for the IRL→scan transformation.
- Re-normalise a scan after a camera solve without `--like`.
