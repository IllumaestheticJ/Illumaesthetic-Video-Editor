# Illumaesthetic Video Editor

An agent-operated pipeline for Illumaesthetic videos: shop footage (Dropbox) + 3D scan data
(engineering Google Drive) rendered in Blender, cut together with the signature **1:1 perspective
cut** from the real car to its scan. It also carries the knowledge base and feedback loop that
train future editing agents.

```
Dropbox footage ──┐                         ┌─ knowledge/ (style, procedures, lessons)
                  ├─ ive probe/sheet/analyze │
Drive scans ──────┤                         ├─ training/  (references, rubric, examples)
                  ├─ ive decimate/crop/prep  │
                  ├─ ive solve/check  (1:1)  │  agents read these first ─┐
                  ├─ ive render (Blender)    │                           │
                  ├─ ive hud (Remotion)      │  feedback --rule ─────────┤
                  └─ ive assemble (ffmpeg) ──┴─> video ──> review ───────┘
```

## Quick start
```bash
scripts/setup.sh                       # deps, Blender 5.3, Remotion
python -m ive --help
```
Agents: start at [`CLAUDE.md`](CLAUDE.md) (or the `scan-video-edit` skill).

## Layout
| Path | What |
|---|---|
| `ive/` | Python CLI: fetch, probe, analyze, beats, mesh decimate/crop, camera solve, QA check, HUD, assemble, training loop |
| `blender/` | `scan_prep.py` (import/normalise scans), `scan_render.py` (looks, camera moves, exploded parts, raycast), `kit_render.py` (Epsilon-Site showroom GLBs with their kit fitted) |
| `remotion/` | `ScanHUD` composition — transparent data overlays driven by JSON |
| `knowledge/` | house style, match-cut + scan-pipeline procedures, sources, lessons (standing rules) |
| `training/` | reference-edit breakdowns, review rubric, archived worked examples |
| `projects/` | one folder per video: `project.yaml`, `overlay.json`, `match/` solves, edit log, feedback |

## How the agent "training" works
No fine-tuning. Each video leaves structured artifacts: decisions with reasons (`editlog.jsonl`),
timecoded reviewer notes (`feedback.jsonl`), camera solves, QA overlays, and rubric scores.
Notes marked `--rule` become standing rules in `knowledge/lessons.md`. Finished projects are
archived to `training/examples/`. Every agent must read lessons, style guide and the latest
examples before editing, so each review makes the next edit better.
