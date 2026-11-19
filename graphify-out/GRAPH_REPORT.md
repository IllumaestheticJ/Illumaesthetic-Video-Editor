# Graph Report - Illumaesthetic-Video-Editor  (2026-11-19)

## Corpus Check
- 396 files · ~95,225 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .jsonl 16, (none) 3, .hdr 1)

## Summary
- 1612 nodes · 2956 edges · 89 communities (81 shown, 8 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 272 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- NFS Car-Lot Reel Notes
- Vanishing Points & Tracking Tools
- GTA Menu Lettering (ui)
- FG2 Race Car Reel Notes
- Blender Scan Render
- GTA Compositors & Clean Plates
- Scan Prep & Mesh Decimation
- 240SX Timeline v1
- 240SX Timeline v1 (archive)
- GTA Car States & Catalogue
- 240SX Timeline (first cut)
- 240SX Timeline v2
- 240SX Timeline v3
- 240SX Timeline (first cut, archive)
- 240SX Timeline v2 (archive)
- 240SX Timeline v3 (archive)
- GTA Car States (archive)
- Scan-Edit Workflow & Rubric
- NFS Car-Lot Compositor
- Game-Menu Reel: Capture & Driver
- Project Template
- Kit Render (Showroom GLBs)
- Mod-Shop Skill & Lessons
- Reel Assembly & Audio (older)
- FG2 Timeline
- Remotion Dev Dependencies
- FG2 Timeline (archive)
- GTA Final Assembly: Sound & End Card
- Game-Menu Reel Procedure
- NFS Car List & Site GLBs
- Drive & URL Fetching
- GTA Self-Review (archive)
- Camera Solve & Look-At
- Timeline Assembly & HUD
- ive CLI Commands
- Media Probe & Frame Tools
- NFS Car List (archive)
- GTA Capture Notes
- Reference Edits & Sources
- Scan Prep in Blender
- Mod-Shop Reel Procedure
- Agent Rules & Graphify Upkeep
- GTA Menu Builder (Menu class)
- House Scan Look
- 240SX Solve Points Overlay
- GTA Review v6-v11: Orbit, Tabs
- GTA Compositor v1
- Remotion TypeScript Config
- 240SX Review v1
- 240SX Review v3
- GTA Review v3-v5: Purchases, Voice
- NFS Self-Review (archive)
- Feedback & Training Loop
- Match Cut: Pinned Scan Transform
- GTA Review v1-v2: Prices, Lettering
- GTA Review v12-v19: End Card
- 240SX Review v2
- FG2 Match Check E (fail)
- GTA Timeline Builder (compose4)
- Remotion Root & WebZoom
- Repo Layout & Setup
- ScanHUD Composition
- 240SX Review v4 (final)
- FG2 Match Check D (soft)
- On-Screen Text Rules
- NFS Prologue GPS Autopilot
- 240SX Scan Sources & Story
- FG2 Match Check P1 (fail)
- FG2 Match Check P2 (soft)
- GTA Review v7-v8: Part Cameras
- GTA Timeline Builder (compose3)
- Remotion Dependencies
- Match Cut: Landmarks & Raycast
- 240SX Footage Notes
- 240SX Match Check B (fail)
- GTA Review v16: Pop-up & Whips
- Remotion README
- Whip Cameras
- Lessons: 240SX & FG2
- Remotion npm Scripts
- 240SX Review v1 (archive link)
- GTA Review v15: Stats & Respray
- GTA Capture Notes (archive)
- FG2 Render Angle Script
- GTA Font Fetch Script

## God Nodes (most connected - your core abstractions)
1. `box()` - 27 edges
2. `main()` - 25 edges
3. `build()` - 24 edges
4. `car_tag()` - 23 edges
5. `retitle()` - 22 edges
6. `main()` - 21 edges
7. `draw()` - 21 edges
8. `NFS car lot reel v1 - self-review (2026-11-11)` - 21 edges
9. `gta6-customs: self-review` - 20 edges
10. `gta6-customs: self-review` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Remotion (video framework; npm run dev, npx remotion render)` --conceptually_related_to--> `render_hud()`  [INFERRED]
  remotion/README.md → ive/hud.py
- `8. Sound (`assemble4.py`)` --references--> `radio_bed()`  [INFERRED]
  knowledge/game-modshop-reel.md → projects/gta6-customs/tools/assemble4.py
- `6. Match the menu camera and light` --references--> `lookat()`  [EXTRACTED]
  knowledge/game-menu-reel.md → ive/camera.py
- `Look at your own output; never report a match from the numeric score alone` --conceptually_related_to--> `check()`  [INFERRED]
  CLAUDE.md → ive/check.py
- `5. Verify` --references--> `check()`  [EXTRACTED]
  knowledge/match-cut.md → ive/check.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **1:1 match-cut flow: frame, reference render, landmarks, raycast, solve, check** — ive_camera_lookat, knowledge_match_cut_landmarks, knowledge_match_cut_raycast, knowledge_match_cut_points_json, ive_solve, knowledge_match_cut_cam_json, ive_check_check [EXTRACTED 1.00]
- **Feedback loop that trains the next agent: decisions, feedback, rules, rubric, archived examples** — readme_agent_training_loop, ive_training_log_decision, ive_training_add_feedback, ive_training_archive, claude_feedback_rule_promotion, knowledge_lessons, training_rubric, training_examples_index [EXTRACTED 1.00]
- **Audio set by measurement: never cut inside music or speech, never repeat a voice line** — knowledge_lessons_never_join_inside_music, knowledge_game_menu_reel_joins_in_silence, knowledge_game_menu_reel_voice_line_detection, knowledge_game_modshop_reel_purchase_sound_voice_check, knowledge_game_modshop_reel_spoken_line_once, knowledge_game_modshop_reel_cannot_hear, knowledge_game_modshop_reel_radio_bed [INFERRED 0.85]
- **240SX scan reel version progression v1 -> v4 (FINAL)** — projects_240sx_scan_review_240sx_scan_reel_v1_agent_self_review_training_rubric_md, projects_240sx_scan_review_v2_240sx_scan_reel_v2_agent_self_review_training_rubric_md, projects_240sx_scan_review_v3_240sx_scan_reel_v3_agent_self_review_training_rubric_md, projects_240sx_scan_review_v4_240sx_scan_reel_v4_final_agent_self_review [INFERRED 0.95]
- **GTA 6 mod-shop reel end card iterations (v13, v17, v18, v19) and the lesson to ask for the exact reference early** — projects_gta6_customs_review_v13_2026_11_19_after_the_user_s_review_of_v12, projects_gta6_customs_review_v17_2026_11_19_after_the_user_s_review_of_v16, projects_gta6_customs_review_v18_2026_11_19_after_the_user_s_review_of_v17, projects_gta6_customs_review_v19_2026_11_19_after_the_user_s_review_of_v18, projects_gta6_customs_review_end_card, projects_gta6_customs_review_lesson_ask_early_for_the_exact_reference [EXTRACTED 1.00]
- **NFS car lot reel audio join: cut-off voice message, looping music, stumble, and the rule not to cut inside music (v8-v11)** — projects_nfs_carlot_review_v8_2026_11_11_after_the_user_s_review_of_v7, projects_nfs_carlot_review_v9_2026_11_11_after_the_user_s_review_of_v8, projects_nfs_carlot_review_v10_2026_11_11_after_the_user_s_review_of_v9, projects_nfs_carlot_review_v11_2026_11_11_after_the_user_s_review_of_v10, projects_nfs_carlot_review_seven_bar_join_crossfade, projects_nfs_carlot_review_no_join_inside_the_song, projects_nfs_carlot_review_rule_do_not_time_a_cut_inside_music [EXTRACTED 1.00]
- **Silhouette match check: scan overlay, footage frame, contours, error readout and verdict** — projects_240sx_scan_match_check_b_scan_overlay, projects_240sx_scan_match_check_b_footage_frame, projects_240sx_scan_match_check_b_cyan_silhouette, projects_240sx_scan_match_check_b_yellow_edges, projects_240sx_scan_match_check_b_silhouette_metric, projects_240sx_scan_match_check_b_fail_verdict [INFERRED 0.85]
- **Solve B correspondence set: named car points marked on the footage frame** — projects_240sx_scan_match_solve_b_points_roof_r, projects_240sx_scan_match_solve_b_points_mirror_r, projects_240sx_scan_match_solve_b_points_spoiler_l, projects_240sx_scan_match_solve_b_points_spoiler_r, projects_240sx_scan_match_solve_b_points_seam_l_top, projects_240sx_scan_match_solve_b_points_seam_r_top, projects_240sx_scan_match_solve_b_points_emblem, projects_240sx_scan_match_solve_b_points_pa_truncated [EXTRACTED 1.00]
- **Match-check composite: footage frame + scan silhouette overlay + edge overlay + silhouette error readout** — projects_fg2_race_car_match_check_d_race_car_806, projects_fg2_race_car_match_check_d_scan_silhouette_overlay, projects_fg2_race_car_match_check_d_footage_edge_overlay, projects_fg2_race_car_match_check_d_silhouette_error_metric [INFERRED 0.85]
- **Camera-match check readout: scan silhouette + footage edges + error metric + verdict** — projects_fg2_race_car_match_check_e_cyan_scan_silhouette, projects_fg2_race_car_match_check_e_yellow_edge_points, projects_fg2_race_car_match_check_e_silhouette_error_metric, projects_fg2_race_car_match_check_e_fail_verdict [INFERRED 0.85]
- **P1 silhouette match check: scan overlay + footage edges + error readout + verdict** — projects_fg2_race_car_match_check_p1_scan_overlay, projects_fg2_race_car_match_check_p1_footage_edge_lines, projects_fg2_race_car_match_check_p1_silhouette_error_metric, projects_fg2_race_car_match_check_p1_fail_verdict [INFERRED 0.85]
- **Match check readout: overlay layers plus silhouette error and SOFT verdict** — projects_fg2_race_car_match_check_p2_contour_overlay, projects_fg2_race_car_match_check_p2_red_tint_layer, projects_fg2_race_car_match_check_p2_silhouette_error_readout, projects_fg2_race_car_match_check_p2_soft_verdict [INFERRED 0.85]

## Communities (89 total, 8 thin omitted)

### Community 0 - "NFS Car-Lot Reel Notes"
Cohesion: 0.05
Nodes (63): Intro cutscene: the 350Z turns in and drives past the camera (f1012-1291), Working copies: a60.mp4 (60 fps, cropped, all-intra) and a.wav, Slot 3: Acura Integra DE4 (lip, skirts, spats, trunk lip, wing; flares hidden), Capture A: NFSU2 car lot - 1440p.mp4 (phone screen recording of a PC longplay; picture and sound), Capture B menu song: first hit 44.84 s, bar 1.1765 s; phrase downbeats rising from silence 44.84 / 47.19 / 51.90 s, not a steady loop, Capture B: NFSU2 car lot - clean audio.mp4 (second, real-time playthrough; 4:3, darker, menu song playing), Capture B around the purchase: Continue click 54.10-54.18, silence to -60 dB, song downbeat 54.25, Capture B voice message 35.1-44.6 s (mono, no music); menu music from 44.8 s (+55 more)

### Community 1 - "Vanishing Points & Tracking Tools"
Cohesion: 0.07
Nodes (23): check(), _edges(), verdict(), Painted HDR panorama of the room as light (rig key world_image), Focal length and pitch from the room's vanishing points (GTA 6 f = 1757 px on 2560), Camera position and scale from where the game's car meets the floor, sil(), cost() (+15 more)

### Community 2 - "GTA Menu Lettering (ui)"
Cohesion: 0.11
Nodes (39): Colour picker: the game's Recommended tab with factory colours as swatches, build(), applied(), panel_from_A(), part(), respray(), rims(), susp() (+31 more)

### Community 3 - "FG2 Race Car Reel Notes"
Cohesion: 0.06
Nodes (44): Black unpainted lip photos (one solved, all dropped per user feedback), CGI (Ecky), Civic FG2 Bodykit for turn10.blend: bumper + skirts, no wing (not used), Civic FG2 Full Car (HQ).stl - 47.75 M tris, different coordinate frame (not used), Civic FG2 Full Car (LQ).stl - 4,866,098 tris, mm (used), Ecky (CGI artist), FG2 #806 race car — source media, FG2 Lip CGI-Real.mp4: Ecky's CGI->real reference (CGI on dark ground cut to the same pose IRL) (+36 more)

### Community 4 - "Blender Scan Render"
Cohesion: 0.09
Nodes (31): add_light(), animate_camera(), argv(), bbox(), ease(), emission(), fresnel_mix(), main() (+23 more)

### Community 5 - "GTA Compositors & Clean Plates"
Cohesion: 0.11
Nodes (20): Capture creator's watermark: the user decides whether it stays, Purchase timing follows the capture; parts are bought and stay on, main(), frame(), over(), plate(), static(), with_car() (+12 more)

### Community 6 - "Scan Prep & Mesh Decimation"
Cohesion: 0.08
Nodes (17): bbox(), cluster_decimate(), crop_to_footprint(), stl_info(), Render quality that is enough at 1080-wide delivery, 1. Pick the cut frame (most important decision), Composite states with numpy (drop regions from the full car, add the part scan), Exploded views (+9 more)

### Community 7 - "240SX Timeline v1"
Cohesion: 0.06
Nodes (31): beats, format, music, fade_out, path, start, output, crf (+23 more)

### Community 8 - "240SX Timeline v1 (archive)"
Cohesion: 0.06
Nodes (31): beats, format, music, fade_out, path, start, output, crf (+23 more)

### Community 9 - "GTA Car States & Catalogue"
Cohesion: 0.07
Nodes (29): Car states are hide-lists on one GLB (cars.yaml), parts paint-matched, car, finish, glb, id, paint, part_paint, catalogue (+21 more)

### Community 10 - "240SX Timeline (first cut)"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 11 - "240SX Timeline v2"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 12 - "240SX Timeline v3"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 13 - "240SX Timeline (first cut, archive)"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 14 - "240SX Timeline v2 (archive)"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 15 - "240SX Timeline v3 (archive)"
Cohesion: 0.07
Nodes (29): beats, format, music, fade_out, path, start, output, crf (+21 more)

### Community 16 - "GTA Car States (archive)"
Cohesion: 0.07
Nodes (28): car, finish, glb, id, paint, part_paint, catalogue, front_lip (+20 more)

### Community 17 - "Scan-Edit Workflow & Rubric"
Cohesion: 0.15
Nodes (13): Scan video edit, analyze(), _hist(), archive(), Optional cut variants: flash and scanline (max once per video), End on the ILLUMAESTHETIC logo card on the final downbeat, The 1:1 perspective cut (signature transition), Beat grid in project.yaml (beats) (+5 more)

### Community 18 - "NFS Car-Lot Compositor"
Cohesion: 0.09
Nodes (14): Drawn wordmarks: study the game's plates and compare options under real plates, Name plates are per-car artwork: lift real plates from the capture, Purchase prompt compositing (prompt = T * scene + c per region), build_zone(), integra_plate(), main(), paint(), prompt() (+6 more)

### Community 19 - "Game-Menu Reel: Capture & Driver"
Cohesion: 0.07
Nodes (20): 10. Layout, assemble, review (`projects/nfs-carlot/tools/assemble.py`), 1. Inputs to collect before anything else, 2. Cars: kit state from the site, never by hand, 3. Line-up check (do this while waiting for anything else), 4. Break down the capture, 5. Track the slide (`projects/nfs-carlot/tools/track.py`), 6. Match the menu camera and light, 7. Swap the cars (`projects/nfs-carlot/tools/composite.py`) (+12 more)

### Community 20 - "Project Template"
Cohesion: 0.08
Nodes (25): beats, format, music, fade_out, path, start, output, crf (+17 more)

### Community 21 - "Kit Render (Showroom GLBs)"
Cohesion: 0.16
Nodes (20): area(), argv(), bbox(), bsdf(), build_ground(), build_rig(), cam_from_json(), cam_orbit() (+12 more)

### Community 22 - "Mod-Shop Skill & Lessons"
Cohesion: 0.14
Nodes (6): Game mod-shop reel, GTA 6 mod shop (photoreal game, several held cameras), Partial re-render with START / END / OUTNAME, then splice and verify, Radio / user music as one unbroken band-limited bed (radio_bed), From the GTA 6 mod-shop reel (2026-11-19, built by an agent, 19 review rounds), gta6-customs (worked project: game mod-shop reel, GTA 6, archived 2026-11-19)

### Community 23 - "Reel Assembly & Audio (older)"
Cohesion: 0.13
Nodes (14): 9:16 layout: the menu's 4:3 box at full width on a blurred, darkened copy, audio(), card(), main(), read(), audio(), card(), main() (+6 more)

### Community 24 - "FG2 Timeline"
Cohesion: 0.08
Nodes (24): beats, format, music, fade_out, path, start, output, crf (+16 more)

### Community 25 - "Remotion Dev Dependencies"
Cohesion: 0.10
Nodes (23): eslint, prettier, @remotion/eslint-config-flat, @types/react, @types/web, typescript, allowScripts, esbuild (+15 more)

### Community 26 - "FG2 Timeline (archive)"
Cohesion: 0.08
Nodes (24): beats, format, music, fade_out, path, start, output, crf (+16 more)

### Community 27 - "GTA Final Assembly: Sound & End Card"
Cohesion: 0.13
Nodes (12): Sound bed: looped room tone plus capture ticks for every menu action, audio(), closing(), main(), purchase_sfx(), radio_bed(), read(), vice_card() (+4 more)

### Community 28 - "Game-Menu Reel Procedure"
Cohesion: 0.11
Nodes (11): Game-menu reel, Constant-rate all-intra working copy indexed by frame number, projects/nfs-carlot/cam_carlot.json (fitted NFSU2 car-lot menu camera), Clean plate (menu drawn, turntable empty), Ending on the EPSILON+ wordmark (white on black), music fading under it, Game capture (must be collected first), Line-up sheet for kit and colour sign-off, projects/nfs-carlot/rig_showroom.json (light rig matching the game) (+3 more)

### Community 29 - "NFS Car List & Site GLBs"
Cohesion: 0.09
Nodes (19): Epsilon-final-GLBs-2026-10-15.zip (newest kit GLB exports on Drive), Epsilon-Site showroom GLBs (one shared frame, part_* nodes, role-named materials), bought, cars, finish, fitted, glb, hide (+11 more)

### Community 30 - "Drive & URL Fetching"
Cohesion: 0.14
Nodes (10): drive_download(), drive_meta(), _drive_session(), url_download(), Gotchas, google-auth, numpy, opencv-python-headless (+2 more)

### Community 31 - "GTA Self-Review (archive)"
Cohesion: 0.10
Nodes (20): gta6-customs: self-review, v10 (2026-11-19) - after the user's review of v9, v11 (2026-11-19) - after the user's review of v10, v12 (2026-11-19) - after the user's review of v11, v13 (2026-11-19) - after the user's review of v12, v14 (2026-11-19) - after the user's review of v13, v15 (2026-11-19) - after the user's review of v14, v16 (2026-11-19) - after the user's review of v15 (+12 more)

### Community 32 - "Camera Solve & Look-At"
Cohesion: 0.19
Nodes (9): lookat(), grade(), _intrinsics(), _matrix_to_euler_xyz(), _pnp(), solve(), cost(), solve_robust() (+1 more)

### Community 33 - "Timeline Assembly & HUD"
Cohesion: 0.20
Nodes (6): assemble(), _clip_inputs(), _needs_tonemap(), _render_clip(), _xfade_expr(), _browser()

### Community 34 - "ive CLI Commands"
Cohesion: 0.21
Nodes (9): beats(), save(), main(), _p(), render_hud(), glb_nodes(), kit(), manifest() (+1 more)

### Community 35 - "Media Probe & Frame Tools"
Cohesion: 0.18
Nodes (9): blender(), blender_cmd(), contact_sheet(), grab_frame(), grab_frame_sdr(), probe(), run(), scenes() (+1 more)

### Community 36 - "NFS Car List (archive)"
Cohesion: 0.11
Nodes (17): bought, cars, finish, fitted, glb, hide, id, kit (+9 more)

### Community 37 - "GTA Capture Notes"
Cohesion: 0.17
Nodes (16): Capture breakdown: held views, menu lists, screen titles, purchases, sound events, Bodywork menu, front 3/4 camera (view M), frames 0-276, cam_E: exhaust camera, set by hand closer than the capture's, cam_S (suspension) and cam_W (wheels) cameras, made with tools/mancam.py, Capture cameras: f = 1757 px on 2560 in every view; horizon row 394 (menu, kits), 75 (rear view), Exhaust view 17946-17976: capture camera creeps, only this half second matches reference frame 17960, Frames used in v3, Full Kits screen 1/4 (same camera as the menu), frames 1500-1890 (+8 more)

### Community 38 - "Reference Edits & Sources"
Cohesion: 0.17
Nodes (12): Dropbox /5. Claude Training/ (Good Reels (Epsilon), training references), Dropbox /2. Illumaesthetic Videos/1. Video dumps/<project> (raw footage and approved edits), Engineering Google Drive (per-car folder, one STL per car state), Where media lives and how agents get it, Pacing (measured), `edited_oct31_1330_46` — 240SX scanning, IRL-only reel (approved, Oct 31 2026), `FG2 Lip CGI-Real.mp4` — Ecky's CGI→real cut (FG2 #806), FG2 Race Lip.blend (CGI look: glossy red paint, black lip/wing, black sky) (+4 more)

### Community 39 - "Scan Prep in Blender"
Cohesion: 0.20
Nodes (5): argv(), import_any(), main(), parse(), world_bbox()

### Community 40 - "Mod-Shop Reel Procedure"
Cohesion: 0.13
Nodes (12): 0. Ask first (each of these cost a review round), 10. Check before every send (all at delivery size, not on contact sheets), 1. Capture breakdown (`clips.md`), 2. Cameras (`vps.py`, `camfit.py`, `mancam.py`), 3. Plates (`plate.py`), 4. Car renders (`ive kit-render`), 6. Timeline (`compose4.py`), 7. Whips (+4 more)

### Community 41 - "Agent Rules & Graphify Upkeep"
Cohesion: 0.14
Nodes (6): After delivering, Before touching footage (mandatory), Graphify repo map update procedure (graphify update, graphify_labels.py, cluster-only), Illumaesthetic Video Editor — agent instructions, Map of this repo (Graphify), While editing

### Community 42 - "GTA Menu Builder (Menu class)"
Cohesion: 0.19
Nodes (9): 5. Menus (`ui.py`, `ui4.py`, `toast.py`), Menu fonts by measurement against the capture (Lexend, Oswald 600), Build menu lists per state (ui.Menu, highlight bar, bought markers, tab highlight), set_tab(), build(), diamond(), main(), Menu (+1 more)

### Community 43 - "House Scan Look"
Cohesion: 0.15
Nodes (11): [format] TikTok format = 1080x1920 full-bleed, hero part above the bottom 20 % caption zone, Render looks: silver (house), clay, scan, wire, points, xray, color, sweep, illumaesthetic.com is not reachable; the Temerario reel is in the 240SX dump, Exploded views are the money shot, Formats, Grade, Illumaesthetic house style — scan videos, Default deliverable: Reel / Short / TikTok 1080x1920 (9:16), 30 fps, 15-30 s (+3 more)

### Community 44 - "240SX Solve Points Overlay"
Cohesion: 0.18
Nodes (12): Solve B point overlay (240sx-scan match QA image), Point emblem (centre of tail panel), Solved focal length f=28.4 mm (solve B), Footage frame: rear view of dark red coupe at dusk, Point mirror_R (right side mirror), Point with label cut off at right frame edge ('pa...'), Reprojection RMSE 3.01 px (solve B), Point roof_R (right rear roof corner) (+4 more)

### Community 45 - "GTA Review v6-v11: Orbit, Tabs"
Cohesion: 0.22
Nodes (12): projects/gta6-customs/editlog.jsonl (edit log), Aero parts loop: list > select > part > buy > back > list (row marked) > down > select, four times, Honey FM radio bed: -32.6 dB between events, 0.5 s fade in, gone 0.4 s before the card, 'Rear Wing' instead of 'Sport Wing'; suspension screen title restored to PRO BUILDS / WHEEL KITS, Environment build tested and not used: SfM on the longer capture connects 9 of 20 views (546 points), none facing the shop front, Ending: 3.4 s orbit (150 degrees) round the stationary car on black with the wordmark (v4; removed in v6), Suspension moved to the Performance tab (the game files the lowered kit under Wheel Kits), Tab navigation before paint, suspension and wheels (the game's lists; tab tick, row tick and select each time) (+4 more)

### Community 46 - "GTA Compositor v1"
Cohesion: 0.19
Nodes (8): main(), over(), plate(), static(), with_car(), timeline(), car_at(), m1()

### Community 47 - "Remotion TypeScript Config"
Cohesion: 0.14
Nodes (13): compilerOptions, esModuleInterop, forceConsistentCasingInFileNames, jsx, lib, module, moduleResolution, noEmit (+5 more)

### Community 48 - "240SX Review v1"
Cohesion: 0.21
Nodes (12): S13 Front Bumper Only scan (7,497,192 tris), v_jul22_1047_58: Temerario scan reel (style reference), 240SX scan reel v1 — agent self-review (training/rubric.md), 4 mm decimation softer than Temerario (idea: render hero close-ups at 2 mm), All 8 cuts on the 95.7 BPM grid (after fixing 1-frame-per-cut drift), Issue: side + hero shots frame the car small (~45 % width); tighter framing or a slow push reads better on phones, Problem: small ground scrap still attached to the bumper part scan, Known issues / v2 ideas (+4 more)

### Community 49 - "240SX Review v3"
Cohesion: 0.17
Nodes (11): Issue: flipped rear crash beam sits close to the body; drop it 10 cm lower, 240SX scan reel v3 — agent self-review (training/rubric.md), Issue: front shot keeps the car small because it has to match the wide IRL frame, Known issues / ideas, Issue: listing dissolve is only near-1:1 (tail offset a few %); a camera solve against the listing image would make it exact, Parts spin left/right without collisions (brief edge-on beam during spin), Ending: reassembly orbit lands on the listing render's angle -> dissolve -> zoom out on the hit, Music track extended 8 beats; cuts on measured onsets, splice keeps the grid (+3 more)

### Community 50 - "GTA Review v3-v5: Purchases, Voice"
Cohesion: 0.26
Nodes (11): Brakes: the Civic's own drilled disc and caliper are kept behind the swapped wheels, Custom 6-spoke rims (site's TE37-style wheel, bronze), Exit: the capture's UI-free shop frame, wallet $0, the line as a subtitle (one frozen frame from v15), NPC line 'need anything else or is that everything?' (subtitle only in v3; plays once at the exit from v4), Sound checked by measurement (levels, events from the timeline), not checked by ear, Seven purchases: Front Lip, Side Skirts, Rear Lip, Sport Wing, Respray, Lowered Suspension Kit, Custom 6-spoke rims, v3 (2026-11-19) - after the user's review of v2, v4 (2026-11-19) - after the user's review of v3 (+3 more)

### Community 51 - "NFS Self-Review (archive)"
Cohesion: 0.15
Nodes (12): NFS car lot reel v1 - self-review (2026-11-11), v10 (2026-11-11) - after the user's review of v9, v11 (2026-11-11) - after the user's review of v10, v12 (2026-11-11) - after the user's review of v11, v2 (2026-11-11) - after the user's review of v1, v3 (2026-11-11) - after the user's review of v2, v4 (2026-11-11) - after the user's review of v3, v5 (2026-11-11) - after the user's review of v4 (+4 more)

### Community 52 - "Feedback & Training Loop"
Cohesion: 0.27
Nodes (6): Feedback recording and promotion to a standing rule (ive feedback --rule), add_feedback(), _append(), log_decision(), _now(), Agent training loop (no fine-tuning: artifacts, rules, archived examples)

### Community 53 - "Match Cut: Pinned Scan Transform"
Cohesion: 0.20
Nodes (6): overlay(), 1:1 perspective cut: IRL frame → scan data, 2. Get the frame, 4. Solve, 5. Verify, Never change the scan's normalisation after solving

### Community 54 - "GTA Review v1-v2: Prices, Lettering"
Cohesion: 0.23
Nodes (12): Spoiler screen, rear camera (view A); Custom Wing 3/3 $790 'Not enough cash', Camera positions rest on assumed El Camino dimensions for the game's car (not one solve), Car tag re-lettered: '22 Civic -> '22 Blista (Dinka Blista); the model still wears Honda badges, Weak: clean render reads as CG in a photoreal game (no driver, dark opaque glass, no dirt, painted HDR panorama), Holds up: Civic stands on the game car's spot with the room's perspective in both views (wheels on wheels), Pricing and branding: painted variants (485 / 800 / 485 / 850), EPSILON+ badge and names (removed from list rows in v7), Problem: 'Not enough cash' and the $99 wallet are the capture's own, under an Epsilon part and price, Menus re-lettered: the game's faces, sizes and colours; prices and part names are the catalogue's (+4 more)

### Community 55 - "GTA Review v12-v19: End Card"
Cohesion: 0.29
Nodes (11): End card (end_card.png): Epsilon logo in GTA 6 colours sampled from the game's logo, gta6-customs: self-review, End card redrawn: palm-tree background, white logo, Vice City hue + (three palm passes; gradient and white + in v18), Second-capture views carry the uploader's watermark and overcast light (watermark covered in v12), End card background = the user's supplied image (endcard/bg_user.webp), wordmark white on top, v12 (2026-11-19) - after the user's review of v11, v13 (2026-11-19) - after the user's review of v12, v14 (2026-11-19) - after the user's review of v13 (+3 more)

### Community 56 - "240SX Review v2"
Cohesion: 0.20
Nodes (7): 240SX scan reel v2 — agent self-review (training/rubric.md), v2 hook (score 5): 1:1 IRL->scan cut at 1.82 s, rear teardown starts immediately, 3 mm full car; rear splice clean after limiting zone to z<0.82, Text: inside+outside only where verified; 4,527 mm removed; CTA on the web page, Rear 1:1 cut on the drop (3.07 s); every cut on a strong accent (alternate beats), holds 1.3-5.8 s, 240SX scan reel v2 — agent self-review (training/rubric.md), Known issues / v3 ideas

### Community 57 - "FG2 Match Check E (fail)"
Cohesion: 0.29
Nodes (11): check_E.jpg: camera-match check overlay, shot E (FAIL), Cyan scan silhouette contour drawn over the car, Verdict FAIL: re-solve camera (add points spread across the frame and depth), Outdoor lot: asphalt, chain-link fence with barbed wire, building behind, ILLUMAESTHETIC plate on the rear of the car, Large black rear wing with EPSILON+ endplate, Red Honda Civic coupe race car #806, rear three-quarter view, Silhouette error: median 8.9px, p90 41.7px (@1920 long side) (+3 more)

### Community 58 - "GTA Timeline Builder (compose4)"
Cohesion: 0.25
Nodes (8): pp(), timeline(), add(), back_to(), buy(), nav(), simple(), whip()

### Community 59 - "Remotion Root & WebZoom"
Cohesion: 0.29
Nodes (8): remotion, RemotionRoot(), calculateScanHudMetadata(), scanHudDefaults, calculateWebZoomMetadata(), WebZoom(), webZoomDefaults, WebZoomProps

### Community 60 - "Repo Layout & Setup"
Cohesion: 0.20
Nodes (9): Blender 5.3 at /usr/local/bin/blender, Cycles CPU only, Media is never committed (work in /home/user/media/<project> and /home/user/media/work), Tools, Work box: 4 CPU cores, 15 GB RAM, no GPU (EEVEE aborts), How the agent "training" works, Illumaesthetic Video Editor, Layout, Quick start (+1 more)

### Community 61 - "ScanHUD Composition"
Cohesion: 0.38
Nodes (9): Typefaces: Inter Display titles, JetBrains Mono data, off-white #e8ecf2, Brackets(), Counter(), HudItem, Label(), ScanHUD(), ScanHUDProps, Title() (+1 more)

### Community 62 - "240SX Review v4 (final)"
Cohesion: 0.22
Nodes (8): v_1838_02: handheld scanner on rear quarter, drifts to clean rear 3/4 (match frame 3.800 s), Rear 3/4 1:1 match: v_1838_02 @ 3.800 s, solve RMSE 3.0 px, overlay confirms silhouette + seams, 1:1 match reuses v1's solved camera (first scan frame identical to v1 match), Front 1:1 match: 8 px RMSE (lamp heights differ scan vs shoot), overlay aligned on bumper/width, 240SX scan reel v4 (FINAL) — agent self-review, cam_B: rear solved camera (3 px), cam_D2: front camera on the 6.2 s frame (height locked 0.75 m); car + crew-held bumper both match, 240SX scan reel v4 (FINAL) — agent self-review

### Community 63 - "FG2 Match Check D (soft)"
Cohesion: 0.31
Nodes (9): check_D.jpg - camera-match check overlay (3D scan over real footage frame, shot D), Car features in frame: large rear wing, front splitter, gold mesh wheels, number 806 on hood and door, Flash/scanline transition (used to hide a soft match), Yellow edge-line overlay tracing the footage (fence mesh, asphalt texture, trees, car decals and wheels), Visible outline offsets: cyan scan outline sits off the car at the front bumper/splitter and at the rear quarter, tight along roof and door line, Real footage frame: red coupe race car #806, front three-quarter view from driver side, parked on asphalt in front of a chain-link fence, 3D scan overlay: cyan silhouette outline and tint laid over the car body, wheels, front splitter and rear wing, Silhouette error readout: median 4.3px, p90 33.6px (@1920 long side) (+1 more)

### Community 65 - "NFS Prologue GPS Autopilot"
Cohesion: 0.28
Nodes (4): How to read the NFSU2 GPS arrow (tip low = ahead, tip high = behind), get(), hold(), screens()

### Community 66 - "240SX Scan Sources & Story"
Cohesion: 0.25
Nodes (7): 240SX scanning — clip notes, S13 Full Car scan (24,991,097 tris), Engineering Drive scans: Nissan S13 (Hatchback), Artec, mm, shared frame across states, S13 part-state scans (bumper mounting, headlights up, rear bumper, doorsill, side mirror removed), Story: rear skin + beam off & flipped, real front bumper pull, front off & flipped, scanner, hero, logo, X-ray reassembly: base = bumper-removed scan on trimmed full car; translate-only, 240SX scanning — clip notes

### Community 67 - "FG2 Match Check P1 (fail)"
Cohesion: 0.36
Nodes (8): check_P1.jpg - camera-match check overlay for shot P1 (3D scan overlaid on a real footage frame, verdict FAIL), Yellow edge lines traced over the footage frame (car details, decals, wheels, building, asphalt cracks), Livery decals readable on the car: EPSILON, Innspeed, HAWK, number 19 door plate, 806 on the bonnet, Honda coupe race car in the footage frame: front three-quarter view, number 19, gold multi-spoke wheels, rear wing, front splitter, Rear wing and its upright sit outside the cyan scan silhouette (visible in footage, not enclosed by the outline), Scan render overlay: semi-transparent red tint over the car body with a cyan silhouette outline, Footage location: asphalt lot in front of a corrugated-metal shop building with a roll-up door, daylight, Silhouette error readout: median 6.5px, p90 59.1px (@1920 long side)

### Community 68 - "FG2 Match Check P2 (soft)"
Cohesion: 0.33
Nodes (8): check_P2.jpg - match check overlay, shot P2 (FG2 race car), Cyan and yellow contour overlay on the car, Flash/scanline transition (used to hide a soft match), Race livery: EPSILON+, jinnspeed, ILLUMAESTHETIC, HAWK, 806 on hood, Subject: Honda coupe race car, number 19, big rear wing, gold multi-spoke wheels, Semi-transparent red-tinted car-shaped layer, Location: outside a corrugated-metal shop building with roll-up door and SwatCustoms.com sign, Silhouette error readout: median 3.6px, p90 20.6px (@1920 long side)

### Community 69 - "GTA Review v7-v8: Part Cameras"
Cohesion: 0.31
Nodes (8): Weak: background behind the car in close-up views is invented and soft (fills, mirrored patches), Partial re-render (START/END in compose4.py) of frames 114-197 and 439-530, spliced in; alignment checked against v7, Per-part cameras from the second capture (front for front lip, side for side skirts), moved in so the Civic covers the game's car, Purchase shots: cameras moved so the Civic covers the game's car (0-5 % uncovered); smeared/mirrored background gone, Side-skirt view: new camera covers 98 % of the game's car (was 67 %); re-sited lower in v8 so the whole skirt is in frame, Problem: first splice dropped the 8 whip frames after the list (685 frames instead of 693); caught by the frame count, v7 (2026-11-19) - after the user's review of v6, v8 (2026-11-19) - after the user's review of v7

### Community 70 - "GTA Timeline Builder (compose3)"
Cohesion: 0.28
Nodes (7): palm(), pp(), timeline(), add(), buy(), m(), simple()

### Community 71 - "Remotion Dependencies"
Cohesion: 0.22
Nodes (8): react, react-dom, @remotion/cli, dependencies, react@19.3.1, react-dom@19.3.1, remotion@4.0.542, @remotion/cli@4.0.542

### Community 72 - "Match Cut: Landmarks & Raycast"
Cohesion: 0.25
Nodes (5): 3. Reference render + landmarks, 8-10 landmarks visible in both the frame and the reference render, points.json (2D to 3D landmark pairs), --raycast: reference-render pixels to 3D scan points, iPhone portrait video: sensor_width_mm 20.25, 1x lens about 28 mm

### Community 73 - "240SX Footage Notes"
Cohesion: 0.32
Nodes (8): v_1945_57 / v_1946_23 / v_1949_07: crew unbolting the front bumper, Dropbox video dump: 240SX scanning (iPhone 16 Pro, HEVC HLG, portrait, 30 fps), edited_oct31_1330_46: approved IRL reel (music + logo card source), p_may11: BMW E34 scan screenshots with wing CAD (scan-look reference, terracotta), v_1838_14: scanner screen in hand, powdered flank, v_1954_41: front bumper comes off toward camera (3.7-6.2 s), v_2122_00: wide night, crew walking past the powdered car, v1 hook (score 3): opens on IRL crew walk-around, no transformation until 8.1 s

### Community 74 - "240SX Match Check B (fail)"
Cohesion: 0.36
Nodes (7): check_B.jpg - camera-match check overlay (silver car scan over a dusk footage frame, verdict FAIL), Cyan contour tracing the outer silhouette of the scan render, Verdict: FAIL - re-solve camera (add points spread across the frame and depth), Darkened footage frame: vertical 9:16 dusk exterior, building with lit doorways, parked pickup, red vehicle at right edge, tree, kerb in foreground, Scan render overlay: light silver car body seen from the rear (rear glass with wiper, spoiler, tail-light panel, plate recess), Silhouette error readout: median 6.1px, p90 62.0px (@1920 long side), Yellow edge lines drawn over the whole frame (building, tree, kerb, car body lines, speckle on the ground at left)

### Community 75 - "GTA Review v16: Pop-up & Whips"
Cohesion: 0.32
Nodes (7): Camera whips between views (8 distinct frames each), The only purchase in the capture (213.6 s, frame 12817): sound 213.84-215.3 s, 'Applied', 'Purchased' pop-up, Purchase event from the second capture: its sound (1.65 s), part and 'Applied' 0.1 s in, 'Purchased' pop-up 0.3 s in, 'Purchased' pop-up redrawn with tools/toast.py (the capture cut-out had a blob mask with the capture's floor inside the letters), Problem: list rectangle held sharp over blurred whip frames (screen tear at 17 s); from v16 nothing sharp is held except lettering, Weak: camera moves are synthetic blur whips (the capture has real ones for two), v16 (2026-11-19) - after the user's review of v15

### Community 76 - "Remotion README"
Cohesion: 0.25
Nodes (7): Commands, Docs, Help, Issues, License, Remotion (video framework; npm run dev, npx remotion render), Remotion video

### Community 77 - "Whip Cameras"
Cohesion: 0.38
Nodes (4): Synthetic whips for every view change (orbit cameras under a long horizontal blur), compose(), decompose(), main()

### Community 78 - "Lessons: 240SX & FG2"
Cohesion: 0.33
Nodes (4): From the 240SX scan reel (2026-11-10, built by an agent), From the FG2 #806 photo/CGI/scan reel (2026-11-11, built by an agent), Lessons (standing rules), fg2-race-car (worked project: FG2 #806 photo/CGI/scan reel, archived 2026-11-11)

### Community 79 - "Remotion npm Scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, upgrade

### Community 81 - "GTA Review v15: Stats & Respray"
Cohesion: 0.50
Nodes (4): Stat bars and numbers are the game's, for its own car (+0.1 handling shown with the wing), Lowered Suspension Kit (car drops 45 mm; the game's +0.3 asphalt handling), Respray: Recommended tab, eleven OEM swatches, cursor runs through all with a colour preview, Boost Blue bought, v15 (2026-11-19) - after the user's review of v14

### Community 82 - "GTA Capture Notes (archive)"
Cohesion: 0.50
Nodes (3): Frames used in v3, GTA 6 mod-shop capture, Second capture (user, 2026-11-19: "include the audio and sounds")

## Ambiguous Edges - Review These
- `Look at your own output; never report a match from the numeric score alone` → `[technical] Verify alignment numerically (silhouette bounds, phaseCorrelate)`  [AMBIGUOUS]
  knowledge/lessons.md · relation: conceptually_related_to
- `[technical] Splice part-state scans into the full car over the smallest zone that changed` → `[scan-look] Part-state composites: use the state scan as captured over the trimmed full-car scan`  [AMBIGUOUS]
  knowledge/lessons.md · relation: conceptually_related_to
- `Solve B point overlay (240sx-scan match QA image)` → `Point with label cut off at right frame edge ('pa...')`  [AMBIGUOUS]
  projects/240sx-scan/match/solve_B_points.jpg · relation: references
- `Verdict FAIL: re-solve camera (add points spread across the frame and depth)` → `Cyan contour at trunk-lid height does not coincide with the raised wing in the footage`  [AMBIGUOUS]
  projects/fg2-race-car/match/check_E.jpg · relation: rationale_for
- `Silhouette error readout: median 6.5px, p90 59.1px (@1920 long side)` → `Rear wing and its upright sit outside the cyan scan silhouette (visible in footage, not enclosed by the outline)`  [AMBIGUOUS]
  projects/fg2-race-car/match/check_P1.jpg · relation: conceptually_related_to
- `Semi-transparent red-tinted car-shaped layer` → `Subject: Honda coupe race car, number 19, big rear wing, gold multi-spoke wheels`  [AMBIGUOUS]
  projects/fg2-race-car/match/check_P2.jpg · relation: conceptually_related_to

## Knowledge Gaps
- **55 isolated node(s):** `NFS Underground 2 car lot (car-select menu)`, `How to read the NFSU2 GPS arrow (tip low = ahead, tip high = behind)`, `Steer the front wheels toward the camera (kit-render --steer 25)`, `9:16 layout: the menu's 4:3 box at full width on a blurred, darkened copy`, `GTA 6 mod shop (photoreal game, several held cameras)` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 681 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `240sx-scan (worked project: 240SX scan reel, archived 2026-11-11)` connect `Scan-Edit Workflow & Rubric` to `Reference Edits & Sources`, `240SX Timeline (first cut, archive)`, `Lessons: 240SX & FG2`, `Scan Prep & Mesh Decimation`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **What connects `NFS Underground 2 car lot (car-select menu)`, `How to read the NFSU2 GPS arrow (tip low = ahead, tip high = behind)`, `Steer the front wheels toward the camera (kit-render --steer 25)` to the rest of the system?**
  _55 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NFS Car-Lot Reel Notes` be split into smaller, more focused modules?**
  _Cohesion score 0.05413469735720375 - nodes in this community are weakly interconnected._
- **Why does `ScanHUD()` connect `ScanHUD Composition` to `On-Screen Text Rules`, `Remotion Root & WebZoom`, `Repo Layout & Setup`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Should `Vanishing Points & Tracking Tools` be split into smaller, more focused modules?**
  _Cohesion score 0.06610169491525424 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Look at your own output; never report a match from the numeric score alone` and `[technical] Verify alignment numerically (silhouette bounds, phaseCorrelate)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `[technical] Splice part-state scans into the full car over the smallest zone that changed` and `[scan-look] Part-state composites: use the state scan as captured over the trimmed full-car scan`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._