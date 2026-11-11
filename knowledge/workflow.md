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
14. **Close out** — when the user says the video is done, rename the Dropbox dump folder to
    `<name> (completed)` (Dropbox MCP `move`) and update the path in `projects/<project>/clips.md`.

## Notes added from the Lola scan-process reel (2026-11)
- **HUD counters land 0.1 % low.** ScanHUD's `Counter` eases with `Easing.out(Easing.exp)`, which
  ends at 1-2^-10, so `value: 21696194` settles on 21,675,006 — an invented number. Until the
  component is fixed, put `value = true / (1 - 2**-10)` (rounded so the final display is exact)
  and keep the real count in `true_value`; check the last counter frame of the HUD render.
- **Ray-Ban Meta glasses footage** (SDR bt709, 3:4 portrait, mixed sizes): solve the focal free;
  on a 1080-wide 9:16 crop it came out fx ≈ 1094 px (HFOV ≈ 67°), not the iPhone 28 mm value.
- **Hard 1:1 solves:** if the silhouette refine stalls, mirror the other side's raycast landmarks
  (x→−x) for a PnP start, then re-pick landmarks on a near render (Lola cut B: 5.2 px RMSE).
- **End the IRL clip on the solved frame** (move the in-point) instead of correcting drift with
  phaseCorrelate when the action allows it.

## Director pass (added 2026-11-11, Ferrari 296 - reviewer asked for "a director agent that guides the shots and
## minimizes redundant frames")
- Before rendering a new version, and after every assembly: `python -m ive director projects/<p>/project.yaml`
  (dead frames, repeated views, subject coverage/cropping, seconds per `section:`, missing `focus:`), then hand the
  report + feedback to the **director** agent (`.claude/agents/director.md`), which writes `projects/<p>/director.md`:
  one focus per shot, sections held instead of cut away, a cut list and a hold list, reuse-vs-render budget.
- Tag every timeline clip with `section:` and `focus:`; the editor implements the director's plan.
## Scene direction (added 2026-11-11, user rule)
- Shot order comes from the car's scan features, not a fixed template. Before planning shots (and for every
  v1 -> v2 revision), run the **scene-director** agent (`.claude/agents/scene-director.md`; in a session started
  before it existed, spawn a general-purpose agent told to follow that file). It writes `projects/<p>/direction.md`
  (feature inventory → ordered scenes → music map) and reviews the contact sheets after rendering.
- Every long Cycles render: scan the per-frame mean luma of the PNGs before assembly. Persistent data can drop the
  studio lights mid-animation with no log error (WRX VA, Cappuccino). Render with persistent data off
  (`use_persistent_data = False`; subaru-wrx-va `tools/shots.py --no-persist`).
- Verify cut timing against the decoded audio (broadband onset, 1 ms RMS half-rise), not only the beat grid.
