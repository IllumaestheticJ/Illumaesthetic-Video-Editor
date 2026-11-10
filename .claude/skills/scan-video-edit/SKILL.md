---
name: scan-video-edit
description: Edit an Illumaesthetic video from Dropbox shop footage and engineering-drive 3D scan data - Blender scan renders in the house silver look, a 1:1 perspective cut from the real car to its scan, beat-synced assembly, Remotion HUD, and recording feedback so future edits improve. Use for any request to edit/cut a reel or video that involves scanning, scan data, STL/OBJ car scans, Blender renders of a scan, or "IRL to scan" transitions.
---

# Scan video edit

Follow `CLAUDE.md` at the repo root first (mandatory reading list), then:

1. **Inputs** — find the footage folder (Dropbox `/2. Illumaesthetic Videos/1. Video dumps/<car>`) and
   the scan folder (engineering Drive, per-car, one STL per state). Ask the user only if neither
   search finds them. Download per `knowledge/sources.md`.
2. **Understand** — `ive probe` + `ive sheet` every clip; `ive analyze` every reference/approved edit;
   `ive beats` the music. Write `projects/<p>/clips.md`.
3. **Plan** — beat-gridded timeline in `projects/<p>/project.yaml` (copy `projects/_template`).
   Log the story decisions.
4. **Scan** — decimate → crop → prep (`knowledge/scan-pipeline.md`).
5. **Match cut** — `knowledge/match-cut.md`: frame → reference render → landmarks → raycast → solve → check.
6. **Shots** — check framing at 30 % res, then queue finals in the background (15 fps + interpolate).
7. **HUD** — `projects/<p>/overlay.json` → `ive hud`.
8. **Assemble + review** — `ive assemble`; inspect frames around every cut; score with `training/rubric.md`.
9. **Deliver + learn** — share the file, collect feedback with `ive feedback` (`--rule` for general
   rules), `ive archive`, commit, push.

Worked example to imitate: `projects/240sx-scan/` (and `training/examples/240sx-scan/` once archived).
