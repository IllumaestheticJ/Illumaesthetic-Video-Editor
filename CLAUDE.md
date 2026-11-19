# Illumaesthetic Video Editor — agent instructions

You edit Illumaesthetic videos: real shop footage (Dropbox) combined with 3D scan data
(engineering Google Drive) rendered in Blender, with the signature **1:1 perspective cut** from
the real car to its scan. Every project you finish teaches the next agent.

## Before touching footage (mandatory)
1. Read `knowledge/lessons.md` (standing rules from reviewer feedback — they override everything).
2. Read `knowledge/style-guide.md` and `knowledge/workflow.md`.
3. Read `training/examples/INDEX.md` and the newest two examples' `project.yaml`, `editlog.jsonl`, `feedback.jsonl`.
4. If the request involves a match cut: `knowledge/match-cut.md`. Scan data: `knowledge/scan-pipeline.md`.
5. Game-menu reels (a game's car-select screen with Epsilon kit cars from the site GLBs):
   `knowledge/game-menu-reel.md` and the `game-menu-reel` skill.
6. Game mod-shop reels (a game's customisation shop, parts bought through its menus, e.g. GTA 6):
   `knowledge/game-modshop-reel.md` and the `game-modshop-reel` skill.

## Map of this repo (Graphify)
`graphify-out/GRAPH_REPORT.md` is a generated map of the code, the knowledge documents, the project notes and the
match-check images (`graph.json`, `graph.html`). It holds two layers: the structure read from the files (functions,
calls, markdown headings) and the concepts read out of the documents (rules, procedures, versions, why-decisions).
Use it to find where something lives (`graphify explain "<name>"`, `graphify path "A" "B"`, `graphify query "<question>"`).
After adding or changing tools, knowledge or project notes: `pip install graphifyy && graphify update . && python tools/graphify_labels.py && graphify cluster-only . --no-label`
(no model needed: it refreshes the structure layer, keeps the concept layer, and `tools/graphify_labels.py` keeps the
hand-written community names). That refresh does not re-read changed documents. After a project that changed knowledge
or review notes, redo the concept layer the way Graphify's own skill describes (`python -c "import graphify,os;print(os.path.dirname(graphify.__file__)+'/skill.md')"`,
its `--update` flow: subagents read the changed documents), name any new communities, run `python tools/graphify_labels.py --save`, and commit the result.

## Tools
`python -m ive <cmd>` — fetch-drive, fetch-url, probe, sheet, frame, analyze, beats, decimate, crop,
prep, render, kit, kit-render, lookat, solve, check, hud, assemble, feedback, log, archive. `--help` on each.
- `render` / `kit-render` pass their arguments to Blender: put `--` first (`python -m ive kit-render -- --glb …`).
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
- Put text over IRL footage.
- Use a dissolve for the IRL→scan transformation (it is always a hard 1:1 cut on a beat).
- Re-normalise a scan after a camera solve without `--like`.
