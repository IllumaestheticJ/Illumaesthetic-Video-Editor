# Graph Report - Illumaesthetic-Video-Editor  (2026-11-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1187 nodes · 1938 edges · 87 communities (58 shown, 29 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bc8b536c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- blender: kit_render.py
- remotion: package.json + ScanHUD.tsx
- gta6-customs: compose3.py + compose.py
- gta6-customs: assemble3.py + assemble.py
- blender: scan_render.py
- 240sx-scan: project_v1.yaml
- example 240sx-scan: project_v1.yaml
- 240sx-scan: project.yaml
- 240sx-scan: project_v2.yaml
- 240sx-scan: project_v3.yaml
- example 240sx-scan: project.yaml
- example 240sx-scan: project_v2.yaml
- example 240sx-scan: project_v3.yaml
- gta6-customs: cars.yaml
- example gta6-customs: cars.yaml
- gta6-customs: ui.py + check.py
- gta6-customs: ui4.py + ui.py
- _template: project.yaml
- fg2-race-car: project.yaml
- example fg2-race-car: project.yaml
- nfs-carlot: composite.py
- gta6-customs: review.md
- example gta6-customs: review.md
- gta6-customs: compose4.py + ui4.py
- ive: assemble.py + hud.py
- ive: media.py
- nfs-carlot: cars.yaml
- example nfs-carlot: cars.yaml
- ive: solve.py + camera.py
- gta6-customs: compose3.py + assemble4.py
- knowledge: game-menu-reel.md
- gta6-customs: compose.py
- gta6-customs: cursor.py + camfit.py
- remotion: tsconfig.json
- knowledge: game-modshop-reel.md
- nfs-carlot: review.md
- example nfs-carlot: review.md
- CLAUDE.md: CLAUDE.md + README.md
- ive: kit.py + analyze.py
- ive: training.py + cli.py
- ive: mesh.py
- ive: fetch.py
- knowledge: match-cut.md
- knowledge: scan-pipeline.md
- gta6-customs: vps.py + refine.py
- tools: game_driver.js
- knowledge: style-guide.md
- fg2-race-car: clips.md
- remotion: README.md
- example fg2-race-car: clips.md
- example README.md: README.md
- knowledge: lessons.md
- gta6-customs: clips.md
- nfs-carlot: clips.md
- example gta6-customs: clips.md
- example nfs-carlot: clips.md
- knowledge: sources.md
- 240sx-scan: review.md
- 240sx-scan: review_v2.md
- 240sx-scan: review_v3.md
- fg2-race-car: review.md
- example 240sx-scan: review.md
- example 240sx-scan: review_v2.md
- example 240sx-scan: review_v3.md
- example fg2-race-car: review.md
- skills: SKILL.md
- skills: SKILL.md
- skills: SKILL.md
- knowledge: workflow.md
- 240sx-scan: clips.md
- 240sx-scan: review_v4.md
- fg2-race-car: render_angle.sh
- gta6-customs: fetch_fonts.sh
- nfs-carlot: fetch_fonts.sh
- scripts: setup.sh
- example 240sx-scan: clips.md
- example 240sx-scan: review_v4.md
- example INDEX.md: INDEX.md
- training: rubric.md
- gta6-customs: assemble4.py
- nfs-carlot: camfit.py + kenburns.py
- nfs-carlot: assemble.py

## God Nodes (most connected - your core abstractions)
1. `box()` - 27 edges
2. `main()` - 25 edges
3. `build()` - 24 edges
4. `car_tag()` - 23 edges
5. `retitle()` - 22 edges
6. `draw()` - 21 edges
7. `main()` - 21 edges
8. `gta6-customs: self-review` - 20 edges
9. `gta6-customs: self-review` - 20 edges
10. `main()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `8. Sound (`assemble4.py`)` --references--> `radio_bed()`  [INFERRED]
  knowledge/game-modshop-reel.md → projects/gta6-customs/tools/assemble4.py
- `5. Menus (`ui.py`, `ui4.py`, `toast.py`)` --references--> `Menu`  [INFERRED]
  knowledge/game-modshop-reel.md → projects/gta6-customs/tools/ui.py
- `5. Menus (`ui.py`, `ui4.py`, `toast.py`)` --references--> `set_tab()`  [INFERRED]
  knowledge/game-modshop-reel.md → projects/gta6-customs/tools/ui4.py
- `main()` --calls--> `drive_download()`  [EXTRACTED]
  ive/cli.py → ive/fetch.py
- `main()` --calls--> `url_download()`  [EXTRACTED]
  ive/cli.py → ive/fetch.py

## Import Cycles
- None detected.

## Communities (87 total, 29 thin omitted)

### Community 0 - "blender: kit_render.py"
Cohesion: 0.08
Nodes (26): area(), argv(), bbox(), bsdf(), build_ground(), build_rig(), cam_from_json(), cam_orbit() (+18 more)

### Community 1 - "remotion: package.json + ScanHUD.tsx"
Cohesion: 0.05
Nodes (52): eslint, prettier, react, react-dom, remotion, @remotion/cli, @remotion/eslint-config-flat, @types/react (+44 more)

### Community 2 - "gta6-customs: compose3.py + compose.py"
Cohesion: 0.13
Nodes (15): main(), frame(), over(), plate(), static(), with_car(), main(), over() (+7 more)

### Community 3 - "gta6-customs: assemble3.py + assemble.py"
Cohesion: 0.23
Nodes (8): audio(), card(), main(), read(), audio(), card(), main(), read()

### Community 4 - "blender: scan_render.py"
Cohesion: 0.14
Nodes (27): add_light(), animate_camera(), argv(), bbox(), ease(), emission(), fresnel_mix(), main() (+19 more)

### Community 5 - "240sx-scan: project_v1.yaml"
Cohesion: 0.06
Nodes (31): beats, format, music, fade_out, path, start, output, crf (+23 more)

### Community 6 - "example 240sx-scan: project_v1.yaml"
Cohesion: 0.06
Nodes (31): beats, format, music, fade_out, path, start, output, crf (+23 more)

### Community 7 - "240sx-scan: project.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 8 - "240sx-scan: project_v2.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 9 - "240sx-scan: project_v3.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 10 - "example 240sx-scan: project.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 11 - "example 240sx-scan: project_v2.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 12 - "example 240sx-scan: project_v3.yaml"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 13 - "gta6-customs: cars.yaml"
Cohesion: 0.07
Nodes (28): car, finish, glb, id, paint, part_paint, catalogue, front_lip (+20 more)

### Community 14 - "example gta6-customs: cars.yaml"
Cohesion: 0.07
Nodes (28): car, finish, glb, id, paint, part_paint, catalogue, front_lip (+20 more)

### Community 15 - "gta6-customs: ui.py + check.py"
Cohesion: 0.13
Nodes (11): check(), _edges(), verdict(), sil(), main(), build(), diamond(), main() (+3 more)

### Community 16 - "gta6-customs: ui4.py + ui.py"
Cohesion: 0.10
Nodes (40): 5. Menus (`ui.py`, `ui4.py`, `toast.py`), build(), applied(), panel_from_A(), part(), respray(), rims(), susp() (+32 more)

### Community 17 - "_template: project.yaml"
Cohesion: 0.08
Nodes (25): beats, format, music, fade_out, path, start, output, crf (+17 more)

### Community 18 - "fg2-race-car: project.yaml"
Cohesion: 0.08
Nodes (24): beats, format, music, fade_out, path, start, output, crf (+16 more)

### Community 19 - "example fg2-race-car: project.yaml"
Cohesion: 0.08
Nodes (24): beats, format, music, fade_out, path, start, output, crf (+16 more)

### Community 20 - "nfs-carlot: composite.py"
Cohesion: 0.13
Nodes (11): build_zone(), font(), integra_plate(), main(), paint(), prompt(), t_map(), rest_offset() (+3 more)

### Community 21 - "gta6-customs: review.md"
Cohesion: 0.10
Nodes (20): gta6-customs: self-review, v10 (2026-11-19) - after the user's review of v9, v11 (2026-11-19) - after the user's review of v10, v12 (2026-11-19) - after the user's review of v11, v13 (2026-11-19) - after the user's review of v12, v14 (2026-11-19) - after the user's review of v13, v15 (2026-11-19) - after the user's review of v14, v16 (2026-11-19) - after the user's review of v15 (+12 more)

### Community 22 - "example gta6-customs: review.md"
Cohesion: 0.10
Nodes (20): gta6-customs: self-review, v10 (2026-11-19) - after the user's review of v9, v11 (2026-11-19) - after the user's review of v10, v12 (2026-11-19) - after the user's review of v11, v13 (2026-11-19) - after the user's review of v12, v14 (2026-11-19) - after the user's review of v13, v15 (2026-11-19) - after the user's review of v14, v16 (2026-11-19) - after the user's review of v15 (+12 more)

### Community 23 - "gta6-customs: compose4.py + ui4.py"
Cohesion: 0.15
Nodes (16): main(), dewatermark(), frame(), over(), plate(), static(), with_car(), pp() (+8 more)

### Community 24 - "ive: assemble.py + hud.py"
Cohesion: 0.20
Nodes (7): assemble(), _clip_inputs(), _needs_tonemap(), _render_clip(), _xfade_expr(), _browser(), render_hud()

### Community 25 - "ive: media.py"
Cohesion: 0.18
Nodes (9): blender(), blender_cmd(), contact_sheet(), grab_frame(), grab_frame_sdr(), probe(), run(), scenes() (+1 more)

### Community 26 - "nfs-carlot: cars.yaml"
Cohesion: 0.11
Nodes (17): bought, cars, finish, fitted, glb, hide, id, kit (+9 more)

### Community 27 - "example nfs-carlot: cars.yaml"
Cohesion: 0.11
Nodes (17): bought, cars, finish, fitted, glb, hide, id, kit (+9 more)

### Community 28 - "ive: solve.py + camera.py"
Cohesion: 0.15
Nodes (11): lookat(), save(), grade(), _intrinsics(), _matrix_to_euler_xyz(), overlay(), _pnp(), run() (+3 more)

### Community 29 - "gta6-customs: compose3.py + assemble4.py"
Cohesion: 0.28
Nodes (7): palm(), pp(), timeline(), add(), buy(), m(), simple()

### Community 30 - "knowledge: game-menu-reel.md"
Cohesion: 0.13
Nodes (14): 10. Layout, assemble, review (`projects/nfs-carlot/tools/assemble.py`), 1. Inputs to collect before anything else, 2. Cars: kit state from the site, never by hand, 3. Line-up check (do this while waiting for anything else), 4. Break down the capture, 5. Track the slide (`projects/nfs-carlot/tools/track.py`), 6. Match the menu camera and light, 7. Swap the cars (`projects/nfs-carlot/tools/composite.py`) (+6 more)

### Community 31 - "gta6-customs: compose.py"
Cohesion: 0.40
Nodes (3): timeline(), car_at(), m1()

### Community 32 - "gta6-customs: cursor.py + camfit.py"
Cohesion: 0.16
Nodes (4): fit(), main(), frame(), sprite()

### Community 33 - "remotion: tsconfig.json"
Cohesion: 0.14
Nodes (13): compilerOptions, esModuleInterop, forceConsistentCasingInFileNames, jsx, lib, module, moduleResolution, noEmit (+5 more)

### Community 34 - "knowledge: game-modshop-reel.md"
Cohesion: 0.15
Nodes (12): 0. Ask first (each of these cost a review round), 10. Check before every send (all at delivery size, not on contact sheets), 1. Capture breakdown (`clips.md`), 2. Cameras (`vps.py`, `camfit.py`, `mancam.py`), 3. Plates (`plate.py`), 4. Car renders (`ive kit-render`), 6. Timeline (`compose4.py`), 7. Whips (+4 more)

### Community 35 - "nfs-carlot: review.md"
Cohesion: 0.15
Nodes (12): NFS car lot reel v1 - self-review (2026-11-11), v10 (2026-11-11) - after the user's review of v9, v11 (2026-11-11) - after the user's review of v10, v12 (2026-11-11) - after the user's review of v11, v2 (2026-11-11) - after the user's review of v1, v3 (2026-11-11) - after the user's review of v2, v4 (2026-11-11) - after the user's review of v3, v5 (2026-11-11) - after the user's review of v4 (+4 more)

### Community 36 - "example nfs-carlot: review.md"
Cohesion: 0.15
Nodes (12): NFS car lot reel v1 - self-review (2026-11-11), v10 (2026-11-11) - after the user's review of v9, v11 (2026-11-11) - after the user's review of v10, v12 (2026-11-11) - after the user's review of v11, v2 (2026-11-11) - after the user's review of v1, v3 (2026-11-11) - after the user's review of v2, v4 (2026-11-11) - after the user's review of v3, v5 (2026-11-11) - after the user's review of v4 (+4 more)

### Community 37 - "CLAUDE.md: CLAUDE.md + README.md"
Cohesion: 0.15
Nodes (11): After delivering, Before touching footage (mandatory), Illumaesthetic Video Editor — agent instructions, Map of this repo (Graphify), Never, Tools, While editing, How the agent "training" works (+3 more)

### Community 38 - "ive: kit.py + analyze.py"
Cohesion: 0.29
Nodes (5): analyze(), _hist(), glb_nodes(), kit(), manifest()

### Community 39 - "ive: training.py + cli.py"
Cohesion: 0.23
Nodes (8): beats(), main(), _p(), add_feedback(), _append(), archive(), log_decision(), _now()

### Community 40 - "ive: mesh.py"
Cohesion: 0.31
Nodes (4): bbox(), cluster_decimate(), crop_to_footprint(), stl_info()

### Community 41 - "ive: fetch.py"
Cohesion: 0.36
Nodes (4): drive_download(), drive_meta(), _drive_session(), url_download()

### Community 42 - "knowledge: match-cut.md"
Cohesion: 0.22
Nodes (8): 1:1 perspective cut: IRL frame → scan data, 1. Pick the cut frame (most important decision), 2. Get the frame, 3. Reference render + landmarks, 4. Solve, 5. Verify, 6. Render the scan shot, Never change the scan's normalisation after solving

### Community 43 - "knowledge: scan-pipeline.md"
Cohesion: 0.22
Nodes (8): Exploded views, Ground-removal rules that survived (and one that didn't), Looks, Render budget, Scan data → Blender: what actually works on the work box, Steps, Vertical framing, Where scans live

### Community 44 - "gta6-customs: vps.py + refine.py"
Cohesion: 0.20
Nodes (12): cost(), sil(), unpack(), angle_to_vp(), line_h(), main(), ransac_vp(), refine() (+4 more)

### Community 45 - "tools: game_driver.js"
Cohesion: 0.22
Nodes (4): { chromium }, http, log, [W, H]

### Community 46 - "knowledge: style-guide.md"
Cohesion: 0.25
Nodes (7): Formats, Grade, Illumaesthetic house style — scan videos, Pacing (measured), Scan look (Temerario reference), Text / HUD (Remotion `ScanHUD`), The 1:1 perspective cut (signature transition)

### Community 47 - "fg2-race-car: clips.md"
Cohesion: 0.29
Nodes (6): CGI (Ecky), FG2 #806 race car — source media, Finished photos (epsilon.plus product pages, Shopify CDN), Logo, Music, Scan (engineering Drive `Honda Civic FG2/Scan Data`)

### Community 48 - "remotion: README.md"
Cohesion: 0.29
Nodes (6): Commands, Docs, Help, Issues, License, Remotion video

### Community 49 - "example fg2-race-car: clips.md"
Cohesion: 0.29
Nodes (6): CGI (Ecky), FG2 #806 race car — source media, Finished photos (epsilon.plus product pages, Shopify CDN), Logo, Music, Scan (engineering Drive `Honda Civic FG2/Scan Data`)

### Community 50 - "example README.md: README.md"
Cohesion: 0.29
Nodes (6): `edited_oct31_1330_46` — 240SX scanning, IRL-only reel (approved, Oct 31 2026), `FG2 Lip CGI-Real.mp4` — Ecky's CGI→real cut (FG2 #806), `reel_0144_48` — Corolla "Good Reel" (Epsilon), `reel_0149_10` — Civic "Good Reel" (Epsilon), Reference edits, `v_jul22_1047_58` — Lamborghini Temerario scan reel (website reference)

### Community 51 - "knowledge: lessons.md"
Cohesion: 0.40
Nodes (4): From the 240SX scan reel (2026-11-10, built by an agent), From the FG2 #806 photo/CGI/scan reel (2026-11-11, built by an agent), From the GTA 6 mod-shop reel (2026-11-19, built by an agent, 19 review rounds), Lessons (standing rules)

### Community 52 - "gta6-customs: clips.md"
Cohesion: 0.50
Nodes (3): Frames used in v3, GTA 6 mod-shop capture, Second capture (user, 2026-11-19: "include the audio and sounds")

### Community 53 - "nfs-carlot: clips.md"
Cohesion: 0.50
Nodes (3): Cars (Drive `Epsilon-final-GLBs-2026-10-15.zip`, file id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7), Game capture (Dropbox `/5. Claude Training/Good Reels (Epsilon)/`, renamed 2026-11-11 at the user's request), NFS-style car lot reel - source media

### Community 54 - "example gta6-customs: clips.md"
Cohesion: 0.50
Nodes (3): Frames used in v3, GTA 6 mod-shop capture, Second capture (user, 2026-11-19: "include the audio and sounds")

### Community 55 - "example nfs-carlot: clips.md"
Cohesion: 0.50
Nodes (3): Cars (Drive `Epsilon-final-GLBs-2026-10-15.zip`, file id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7), Game capture (Dropbox `/5. Claude Training/Good Reels (Epsilon)/`, renamed 2026-11-11 at the user's request), NFS-style car lot reel - source media

### Community 84 - "gta6-customs: assemble4.py"
Cohesion: 0.21
Nodes (8): audio(), closing(), main(), purchase_sfx(), radio_bed(), read(), vice_card(), voice_line()

### Community 86 - "nfs-carlot: assemble.py"
Cohesion: 0.33
Nodes (5): audio(), card(), load(), main(), rms_db()

## Knowledge Gaps
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `timeline()` connect `gta6-customs: compose3.py + assemble4.py` to `gta6-customs: compose3.py + compose.py`, `gta6-customs: vps.py + refine.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Should `blender: kit_render.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0841813135985199 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `gta6-customs: compose4.py + ui4.py` to `gta6-customs: compose3.py + compose.py`, `ive: kit.py + analyze.py`, `gta6-customs: vps.py + refine.py`, `gta6-customs: ui.py + check.py`, `gta6-customs: ui4.py + ui.py`, `nfs-carlot: camfit.py + kenburns.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Should `remotion: package.json + ScanHUD.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05143191116306254 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `gta6-customs: compose3.py + compose.py` to `ive: kit.py + analyze.py`, `gta6-customs: vps.py + refine.py`, `gta6-customs: ui.py + check.py`, `nfs-carlot: camfit.py + kenburns.py`, `gta6-customs: compose.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Should `gta6-customs: compose3.py + compose.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12688172043010754 - nodes in this community are weakly interconnected._
- **Should `blender: scan_render.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1408199643493761 - nodes in this community are weakly interconnected._