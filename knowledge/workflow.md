# Workflow: new scan video, start to finish

0. **Read** `knowledge/lessons.md`, `knowledge/style-guide.md`, `training/examples/INDEX.md`
   (top two examples) and any `training/references/*.md` the user points at.
1. **Brief** — what car, which deliverable (reel default), which IRL story beats, which scan states.
   If the user gave reference videos, `ive analyze` them and write `training/references/<name>.md`.
2. **Gather** — list Dropbox dump folder and the engineering Drive car folder (`knowledge/sources.md`).
   Download footage + scans to `/home/user/media/<project>/`.
3. **Watch** — `ive probe` every clip (HDR? rotation? fps?), `ive sheet` each clip and look at it.
   Write a one-line description per clip in `projects/<project>/clips.md`.
4. **Music + beats** — `ive beats <track>`; lay the beat grid in `project.yaml: beats`.
5. **Story** — IRL setup (2–3 shots) → **1:1 cut** to scan → scan beats (Temerario-style moves,
   exploded part) → IRL payoff → logo card. Log each choice: `ive log <project> "<decision>" --why "<reason>"`.
6. **Scan prep** — `knowledge/scan-pipeline.md`.
7. **Match cut** — `knowledge/match-cut.md`. Save `points.json`, `cam.json`, `check.jpg` in `projects/<project>/match/`.
8. **Render** scan shots (framing check at 30 % first, then finals at 15 fps in the background).
9. **HUD** — write `overlay.json` (frames = seconds × fps), `ive hud overlay.json hud.mov`.
10. **Assemble** — `ive assemble projects/<project>/project.yaml`. Watch the output: contact sheet
    plus frames ±2 around every cut.
11. **Self-review** against `training/rubric.md`; fix anything that scores < 3.
12. **Deliver** — upload/hand over; ask for feedback; record it with `ive feedback` (`--rule` for
    anything that should apply to every future video).
13. **Archive** — `ive archive projects/<project>`; commit + push.
