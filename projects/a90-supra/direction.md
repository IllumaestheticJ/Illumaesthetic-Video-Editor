# A90 Supra v2 - scene direction (scene-director stage)

Scan-only Temerario-style reel, 9:16, 120 BPM. Stage 2 (shot-level focus, cut list, hold list, render budget) is in
`plan_v2_sections.md`. Scenes are ordered by what this car's scans contain, travelling once around the car:
**whole -> front -> front corner -> right side -> rear -> rear corner -> line-up -> reassembly -> logo** (no ping-pong).

## 1. Feature inventory (what the data holds)
All files prepped in the car frame (`--like car.json`) under `/home/user/media/work/a90/blend/`. Registration column =
how it was verified (red/green/blue-over-silver overlays: `/home/user/media/work/a90/plan/regcheck/sheet_reg1.jpg`,
`sheet_interior.jpg`; overlap = % of the part's surface within 8 mm of the car or of the scan it duplicates).

| Region | File(s) | What it shows | Kind | Registration | Richness |
|---|---|---|---|---|---|
| whole car | car.blend (4 mm, 3.3 M tris) + L_corner_{FR,FL,RR,RL} | complete exterior; car was scanned without corners, wheels/brakes/coilovers come from bench scans placed on engineering hardpoints (match/corners.json) | base | defines the frame | high |
| **front bumper** | n_fbump_norad (Outside+Inside union minus radar module), fbump | bumper skin AND its scanned inner face (ribs, tabs - verified v1, regcheck/inside_cmp.jpg) | part | v1 overlay, p50 2-6 mm | **high** |
| radar module | n_radar_mod = Supra Radar Cover + Supra Radar Mounting Grille | lower-right intake: radar cover + its mounting grille | part (2 scans) | 97 % / 84 % within 8 mm of the bumper scan; red/green over silver sits in the right lower intake (C_radar) | medium |
| **behind front bumper** | ufb (Under Front Bumper), in base_v2 | crash beam, radiators/ducts, mounts | removed state | v1 overlay | **high (hero)** |
| front-right fender section | fender (lower-rear piece of the RH front fender) + ufender (Under Fender), liners | fender panel; washer bottle / inner structure behind it | part + state | v1 overlay, p50 2.1 mm | medium |
| front corners | p_FR_wheel/rotor/caliper/coilover (full), L_corner_FL | 255/35R19 wheel+tyre, rotor, caliper, coilover (right scans; left = mirrored right) | parts | placed on hardpoints (corners.json), not scan-registered - see editlog | high |
| **right side** | n_dtrim (Supra Door Trim), n_uskirt (Upper Skirt), n_lskirt (Lower Skirt) | rear-of-door side trim, upper + lower side skirt | parts (NEW) | blue/green/red patches z-fight on the car (A_side); 69 / 70 / 98 % within 8 mm of car | medium-high |
| under the side panels | n_udtrim (Under Door Trim), n_uskirt_under (Chassis Under Upper Skirt), spliced in base_v2 | sill/rocker structure and door structure the trims cover | removed states (NEW) | overlays B_under; median 4.8 / 12.7 mm (they are mostly NEW surface, as expected) | medium |
| **rear bumper** | rbump (Outside+Inside union) | bumper skin + scanned inner face (verified v1) | part | v1 overlay | **high** |
| **behind rear bumper** | n_urb = Supra Under Rear Bumper (27 M -> 3 mm, 1.7 M), 843 k tris spliced into base_v2 where >7 mm from the car | rear crash beam, exhaust tips/silencer, mounts - fills v1's hollow tail | removed state (NEW) | red-over-silver D_urb: coincident at rear corners/exhaust; 47 % within 8 mm of base_explode | **high (hero)** |
| rear corners | p_RR_wheel/rotor/caliper/spring/damper (full), L_corner_RL | wheel, rotor, caliper, coil spring, damper | parts | hardpoints (corners.json) | high |
| interior | n_interior (Interior_(2.4m)), n_interior6 (6 mm), n_console (Center Console) | seats, dash, steering wheel, door cards, trunk floor; console | static fill | cut-view render (E2/E3): seats under the roof, between the sills, console on the centreline - sits in the cabin; 3 % within 8 mm (the car shell has no cabin, so no overlap is expected) | medium |
| trunk | r24_lid / r24_rear / r24_open1-2 (2024, global reg rmse 4.4 mm) | closed lid; "cover open" files are small interior fragments | NOT an open state | - | **excluded** (no open-trunk scan; brief rule D) |
| hood, doors, roof | none | - | - | - | **no data: never opened** |
| BMW reverse light | own frame | - | - | not registered | excluded |
| weak data | car shell has no cabin (hollow through the glassless windows), arches nearly empty without corners, composite seams where panels were carved; licence plate - see plan_v2_sections.md "Plate" | | | | |

Signature features from the scans: double-bubble roof + ducktail, big lower intakes with the radar module, side intake
trim behind the door, wide rear haunches, 19" wheels on the bench-scanned corners.

Richest regions: **front (bumper + inside, radar module, crash structure, fender, corner)** and **rear (bumper + inside,
under-rear-bumper structure, corner)**. These get the 6 s hero scenes on the two biggest musical moments (first
separation 7.0 s, rear release 21.0 s).

## 2. Scene order
| # | Scene (shot id) | Reel s | Scans used | Feature shown (section covered) | Why here (inventory) | Beats | Camera |
|---|---|---|---|---|---|---|---|
| 1 | v01_whole | 0-4 | car + 4 corners + interior | WHOLE car with wheels/suspension | opener = complete car, motion from frame 1 (slow track), fades up like the Temerario | 8 | right side profile, 6.6 m, 35 mm, slight arc |
| 2 | v02_face | 4-6 | same | FRONT face (intakes, radar lower intake, headlights) | travel starts at the richest end; sets up the bumper | 4 | low front 3/4 push-in |
| 3 | v03_fbump | 6-12 | base_v2, bumper, radar module | FRONT BUMPER off + inside; radar module; crash beam/radiators behind | richest region, hero data (ufb) on the first big hit | 12 | front 3/4: pull up/out for the tipped bumper, then push IN to the crash structure |
| 4 | v04_fcorner | 12-16 | fender, FR parts, FL corner | FRONT CORNER: fender section, wheel, caliper, rotor, coilover (+FL corner) | adjacent to the front; wheels/suspension are the user's ask (feedback 10.0 s) | 8 | high 3/4 on the RF corner, push in on the hub |
| 5 | v05_side | 16-20 | door trim, skirts, base_v2 | RIGHT SIDE: door trim, upper + lower skirt off, structure under them | travel front -> side; new 2026 side scans | 8 | high side, 40 deg down, tracks rearward |
| 6 | v06_rbump | 20-26 | rbump, base_v2 (urb) | REAR BUMPER off + inside; structure behind it | second hero region on the second-biggest hit | 12 | rear 3/4: up/out for the tipped bumper, then push IN to the crash beam / exhaust |
| 7 | v07_rcorner | 26-30 | RR parts, RL corner | REAR CORNER: wheel, caliper, rotor, spring, damper (+RL corner) | adjacent to the rear | 8 | high 3/4 on the RR corner, push in on the hub |
| 8 | v08_lineup | 30-34 | everything | FULL EXPLODED LINE-UP (only time all sections are seen together) | Temerario 28-32 s payoff | 8 | high front 3/4, 6.6 m, slow drift |
| 9 | v09a/b | 34-38 | everything -> car.blend | REASSEMBLY, lock on 36.0, clean car, fade to black 37-38 | Temerario 32-36 s | 8 | rear 3/4 high, car small |
| 10 | logo | 38-41.5 | logo png | small ILLUMAESTHETIC logo on black | house ending | 7 | - |

Each section appears in ONE continuous scene only. Interior is a static fill (never exploded: lifting it out would
leave an empty shell - the car scan has no cabin - and there is no roof/door-off scan to reveal it honestly).

## 3. Music map (120 BPM, beat 0.5 s, bar 2 s; cues_v2.json)
| Bar line / beat | Event |
|---|---|
| 0.0 | fade up on drone (no kick) |
| 4.0 | cut v02; kick on one; riser 4.0 -> 7.0 |
| 6.0 | cut v03 |
| **7.0** | riser resolves: IMPACT, front bumper releases |
| 9.0 / 9.6 | radar module out / bumper parked (inside up) |
| 12.0, 12.5, 13.0, 13.5, 14.0, 14.5 | cut v04; fender, wheel(+FL), caliper, rotor, coilover - one tick per part |
| 16.0, 16.5, 17.5, 18.5 | cut v05; door trim, upper skirt, lower skirt |
| 20.0, **21.0** | cut v06; IMPACT rear bumper releases |
| 26.0, 26.5, 27.0, 27.5, 28.0, 28.5 | cut v07; wheel(+RL), caliper, rotor, spring, damper |
| 30.0 | cut v08 line-up (drums thin to kick-on-one) |
| 34.0 | cut v09; drums out; swell |
| **36.0** | BIG: reassembly lock + hard swap to clean car |
| 37.0-38.0 | fade to black |
| 38.0 | logo chord |

## 4. Diff against v1 (project.yaml timeline)
| v1 | v2 | Why |
|---|---|---|
| s01 front 3/4 turntable 5 s | replaced by v01 side profile (whole car with wheels) + v02 front push 2 s | v1 had no wheels; turntables that show nothing new are banned (lessons: mazda-miata-nc) |
| s02 low rear 3/4 orbit | **dropped** | rear is shown once, in its own section (v06/v07); no ping-pong |
| s03 front arch (empty arch) | **dropped** - corner shown with real suspension in v04 | feedback 10.0 s (complete suspension); director report: s03 ~ s06 repeated view (IoU 0.71) |
| s04 headlight, s05 tail light | **dropped** | not sections that come apart; keeps the reel on the disassembly the user asked for |
| s06 side glide | replaced by v05 (side panels come off) | same subject now earns its time |
| s07 top-down rise | **dropped** | director report: 1.2 s dead; nothing new |
| s08 explode 7.5 s (all at once) | v03-v09: progressive, section by section, 30 s | user + Temerario: progressive, camera stays on each section |
| logo hard cut, large | fade to black + small logo fade-in | Temerario ending |
No v1 render can be reused (new corners, new base, new cameras).

## 5. Open questions for the editor / user
- Corners are bench scans on engineering hardpoints, left side mirrored from the right: OK to show the FL/RL corners
  pulling out (they are mirrored copies)? Plan keeps them as single units, never in close-up.
- The Door Trim scan is the curved side-intake trim behind the door (renders as that shape); label it "SIDE TRIM"?
  (Drive name is "Door Trim".) Plan uses "DOOR TRIM" to match the file name.
- Interior is in the cabin as a static fill. Confirm it should stay unexploded.
