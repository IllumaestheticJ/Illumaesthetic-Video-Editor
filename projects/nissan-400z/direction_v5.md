# Nissan 400Z: scene direction v5 (scene director, 2026-11-13)

User on v4: *"there are a bunch of parts that were removed that didn't show up here, including the grille. Can you also
include the bomex bodykit from ron's folder, and the livery files"*. Standing user rules for this reel still apply:
- nothing comes off the bumper until the bumper itself is off;
- the mirror must not take the window;
- music not too loud (keep gain 0.63, about -14 LUFS);
- logo big (720 px);
- no dissolves for state changes;
- labels must be factual and come from the file names.

Sources I read: lessons.md (all of it), direction.md (v2), review.md, feedback.jsonl, editlog, project.yaml (v4), clips.md,
the Revuelto v4 direction and shots_v4.py, the part/kit prep json bboxes in `/home/user/media/work/z400/blend/`, and the
livery PSD and mockups (`livery/render/*.png`).
Sheets I looked at: first, middle and last frames of N0, H, N1a, N3, N2 and N1b (scratchpad `fml_*.jpg`), plus `livery_sheet.jpg` and `psd_full.jpg`.
Frame: front is -Y, rear is +Y, and **+X is the driver (left) side**. Kit `*_driver` parts sit at +X. **k_gas_cap_x sits at -X, on the passenger rear quarter.**
The livery PSD is drawn on the driver side.
N0, H and N1a all use passenger-front 3/4 cameras (x < 0).

## 1. Inventory delta (v4 -> v5)

| region | new data | what it adds | richness |
|---|---|---|---|
| Front structure | Air_Ducting_2mm (part), Front_end_crash_foam_removed_2mm (state) | 2 teardown steps behind the bumper: ducting off, then foam off | **richest teardown** (4 states, 5 parts) |
| Front bumper | bumper_shell_v5, Upper_Grille_2mm, Lower_Grille_2mm (real part scans) | the grille beat the user asked for, nested in the bumper | 3 parts |
| Side (doors) | mirror_r_scan / mirror_l_scan (real part scans incl. mount base and harness) | both mirrors, real geometry | 2 parts + state |
| Rear | p_wing + Rear Wing Removed (unchanged) | stock duck-tail off, deck mounts | 1 part |
| Bomex x Kaido House kit | 16 CAD parts (~4 mm registration) | the build: front, passenger side, rear | **richest overall** |
| Livery | PSD side view on both sides, grey paint | finish of the build | side only: no hood, window or wheel artwork in the files (see Q6) |

## 2. Structure: two chapters, one loop around the car each
Chapter 1 is the stock teardown and stays on the front: front -> structure -> bumper alone -> mirrors.
Chapter 2 is the Bomex build. It travels round the car in one direction: head-on -> passenger side -> tail -> driver side (livery) -> driver-front hero.
The kit lands on the 29.03 phrase, straight after the 27.6-29.0 break.

Why the draft order changed:
- **The stock wing moves from chapter 1 into the chapter-2 rear shot** (stock duck-tail off, then the Bomex ducktail on, in one camera).
  - The draft did not fit 8 bars. Bumper unit, structure (3 states + 3 labels), bumper alone and mirrors with a hold already fill 8 bars, and the draft still needed the wing on top of that.
  - The rear now appears in **one** continuous sequence. In the draft it appeared twice: wing off, then the kit rear later.
  - Physically, the ducktail replaces that wing.
- **The structure comes before the bumper alone.** N1a already ends pushed in on the structure, so the structure shot continues that move (rule C, and the Revuelto v4 order: front, then frontin, then fb alone). Showing the bumper alone first would give structure -> bumper -> structure.
- **Mirrors: one front-high shot with both mirrors.** The passenger side belongs to the kit/gas-cap beat in chapter 2, and the driver side to the livery. That way each side appears once.
- **The chapter-2 base is reset:** hood, mirrors, ducting and foam are back, the stock bumper and wing are not yet fitted with kit parts. This is a hard cut on the phrase after the break, carried by the BOMEX x KAIDOHOUSE label.
  - It is the one deliberate state jump in the reel.
  - The kit needs the car closed (hood on, as in the mockups), and no scan shows the stock parts going back on.

## 3. Cut table
- Grid: bar b = 14.031 + 1.875 b. Big kick k = 14.031 + 0.9375 k. Frame = round(t x 30).
- **Cut on the measured onsets, not the grid.** v4 measured onsets: 14.004, 17.795, 23.363, 26.181, 28.987, 33.672, 37.429, 40.289, 41.172, 44.049.
- Measure the new cut points: 16.84, 32.78, 36.53 and 45.91.

| # | shot | bars | t (s) | frames | section | reuse/new |
|---|---|---|---|---|---|---|
| 1 | N0_open | intro | 0-7.311 | 0-219 | whole car, passenger-front 3/4 | REUSE as v4 |
| 2 | H_hoodopen | intro | 7.311-14.031 | 219-421 | engine bay | REUSE as v4 |
| 3 | N1a_bumper_off | 0-1.5 | 14.031-16.843 | 421-505 | front: bumper+grille unit off ON the drop | REUSE, `trim_start` ~27 f (0.9 s) so the unit moves on the drop frame (it moved 0.967 s after the v4 cut) |
| 4 | STRUCT | 1.5-5 | 16.843-23.406 | 505-702 | front structure: ducting off, swap to foam removed on the 21.531 phrase | NEW, 30 fps |
| 5 | BUMPER | 5-6.5 | 23.406-26.218 | 702-787 | front bumper alone: upper and lower grille out | NEW, 30 fps |
| 6 | MIRRORS | 6.5-8 | 26.218-29.031 | 787-871 | both mirrors off, hold on the mounts through the break | NEW, 30 fps |
| 7 | KIT_FRONT | 8-10 | 29.031-32.781 | 871-983 | kit front installs (phrase) | NEW, 30 fps |
| 8 | KIT_SIDE | 10-12 | 32.781-36.531 | 983-1096 | passenger side: rear fender, skirt, slats, gas cap | NEW, 30 fps |
| 9 | REAR | 12-14 | 36.531-40.281 | 1096-1208 | stock wing off (phrase), ducktail and diffuser on | NEW, 30 fps |
| 10 | LIVERY | 14-16 | 40.281-44.031 | 1208-1321 | driver side, livery sweep, hold through the 42.2-44.0 break | NEW (camera-only: 15 fps + interp OK) |
| 11 | HERO | 16-17 | 44.031-45.906 | 1321-1377 | whole kitted, liveried car, driver-front 3/4 | NEW (15 fps OK) |
| 12 | logo | 17-18 | 45.906-47.781 | 1377-1433 | 720 px card on the kick, rides the 1.2 s music fade | re-make card (v3 is 640 px) |

Total **47.78 s** (1433 f). Dropped, so nothing shows twice:
- **N1b_structure**: replaced by STRUCT. Same section, now with the new states.
- **s5_tail**: the rear is shown once, in REAR.
- **N2_mirror**: old diff mirror, one side only. Replaced by MIRRORS with the real scans.
- **N3_wing**: a stock-quarter car. Shown after the kit side it would undo the rear fenders, and its move is now part of REAR.
- **s8b_explode**: a stock reassembly would put the stock bumper back. The kit build is the reassembly now.

## 4. Shots: camera, part motion, labels
Labels: one at a time, `shadow: true`, title of 18 characters or fewer, sub never empty, in clear black away from moving parts.
Subs of about 30 characters need 50 frames or more. No numbers.

**H (reuse).** Add the label ENGINE BAY / HOOD REMOVED at 9.0-12.5 s. The hood is absent in H, which is backed by the "Bumper and hood removed" scan.
This is the hood's only beat. No hood motion: the captured open hood is ragged (v2 Q2).

**N1a (reuse).** The bumper shell and grilles leave as one unit (user rule). No label while the unit is moving.
Risk: the unit exits through the top of the frame. If the user flags "parts leave the screen", re-render it parked below the nose (Miata v3).

**STRUCT** (k = 16.843 + 0.9375 n)
- Camera: cut on the structure, slightly wider and more frontal than N1a's tight end pose.
  - Start: passenger-front about 25 deg, about 2.6 m, target the beam centre (about -0.05, -1.85, 0.45).
  - Slide to about 8 deg off head-on and push to about 2.2 m.
  - Both headlamp backs stay in frame, with about 30 % black above for the parked ducting.
- Base: bhr2 (2 mm), with the hood off as captured. Ducting (Air_Ducting_2mm) at home.
  - From the first ducting key on, switch to `bhr2_noduct`: bhr2 minus tris within 6 mm of the ducting. Fill its holes only from the foam-removed state, inside the ducting bbox.
- Moves:
  - k2 (18.718, f562): the ducting slides forward (-Y) 0.25 m out of the openings (via key), then rises to park about 0.5 m above the structure, fully in frame by k3 (19.656).
  - k5 (21.531 phrase, f646): **hard 1:1 swap** (same camera, no dissolve) to Front_end_crash_foam_removed_2mm as captured. Keep its full width and carve the car around it (Revuelto v5). The ducting stays parked.
- Labels (low band):

  | time | label |
  |---|---|
  | 16.9-18.6 | FRONT BUMPER / REMOVED |
  | 19.0-20.9 | AIR DUCTING / REMOVED |
  | 21.6-23.3 | CRASH FOAM / REMOVED |

**BUMPER**
- Bumper alone on black. The car is hidden and used only as the light reference.
- Pieces: bumper_shell_v5, Upper_Grille_2mm and Lower_Grille_2mm, all at home on the cut.
- The grilles leave along their mounting axis (Y): **out the back if their flanges sit behind the openings, forward if in front.** Read this off a section render first.
  - Upper grille: 24.343 (f730). Via 0.12 m along Y, then +0.30 m Z.
  - Lower grille: 24.812 (f744). Via 0.12 m along Y, then -0.25 m Z.
- Camera: about 30 deg off the exit axis on the side they leave toward, el 15-20 deg, 3.8-4.1 m (Revuelto: 2 m bumper in portrait).
  - All three pieces stay in frame with 20 px or more of margin, and the shell never hides a grille.
  - No spin. Turn about 15 deg only if bumper_shell_v5's inner face is really scanned.
- Label: GRILLES / UPPER · LOWER, 24.5-26.1.

**MIRRORS**
- Camera: front-high, looking back over the open bay at the A-pillars. el about 30 deg, az 0 -> -12, slow 5 % push.
  - Both mirror housings in frame with about 12 % side margins.
  - Keep the nose below the frame. If it shows, it must be the foam-removed state with no ducting.
- Base: comp_explode with the Side Mirrors Removed fill, and p_wing at home (the wing is still on in chapter 1).
- Move at k1 (27.156, f815): mirror_r_scan and mirror_l_scan leave outboard along the door normal (±X 0.15 m via, clear of the skin and glass), then rise 0.35 m. Both are parked in frame by 27.6.
  - Base and harness go with the mirror. **No glass moves.** Check against the v3 fix.
- Hold on the exposed door mounts through the break.
- Label: SIDE MIRRORS / REMOVED, 27.6-28.95.

**KIT_FRONT** (k = 29.031 + 0.9375 n)
- Camera: head-on, el about 12 deg, about 5.6 m, target (0, -1.5, 0.55). Eases to passenger-front 3/4 (az about -30, about 5.0 m) by the end.
  - It never matches N0's framing.
  - Kit front plus staged parts at 85-90 % of the width.
- Base:
  - car.blend, hood and mirrors on.
  - Remove the stock bumper and grille skin: the car tris the bumper-off state lacks, inside the bumper zone (gr86 v4).
  - Fill only that opening from bhr2.
  - Carve stock fender skin wherever it pokes through a seated kit fender (Frontier v6/v7). There is **no fender-removed scan, so the stock fender never comes off.**
- All parts are staged in frame on the first frame, in black, **stacked above or outboard**, never in front of the lens:

  | part | staged at |
  |---|---|
  | front fenders | ±X +0.15, Z +0.45 |
  | fender slats | Z +0.85 |
  | kit bumper | -Y 0.7 |
  | canards | -Y 0.5, ±X +0.25 |

- Install order (child parts after the parent):

  | kick | time | frame | move |
  |---|---|---|---|
  | k1 | 29.968 | f899 | fenders seat (via 0.08 m outboard) |
  | k1.5 | 30.437 | f913 | slats into the fender vents along X |
  | k2 | 30.906 | f927 | bumper slides home along +Y (via 0.15 m ahead of home, tucks under the fender fronts) |
  | k3 | 31.843 | f955 | canards onto the bumper corners |

- Labels:

  | time | label |
  |---|---|
  | 29.1-30.8 | BOMEX x KAIDOHOUSE / BODY KIT (PSD title spelling; Ron's folder "Bomex/Kaido House") |
  | 31.0-32.7 | FRONT BUMPER / CANARDS · FENDERS · SLATS |

**KIT_SIDE** (passenger side, -X; k = 32.781 + 0.9375 n)
- Camera: low (el 6-8 deg; skirts only read grazing). Tracks from passenger side-front (az about -70) to the rear quarter (az about -125).
  - Skirt, rear fender and gas cap fill the frame. No part touches an edge.
- Staging, outboard -X:

  | part | staged at |
  |---|---|
  | rear fender | 0.45 m, Z +0.25 |
  | skirt | 0.45 m, low |
  | rear slats | 0.75 m, Z +0.35 |
  | gas cap | 0.35 m |

  The +X twins run the same keys mirrored, hidden behind the body.
- Order:

  | kick | time | frame | move |
  |---|---|---|---|
  | k1 | 33.718 | f1012 | rear fenders seat along X |
  | k1.5 | 34.187 | f1026 | side skirts in along X (bridge the two fenders) |
  | k2 | 34.656 | f1040 | rear fender slats |
  | k3 | 35.593 | f1068 | gas cap X onto the fuel door. Its bbox sits on the kit rear fender, so it goes on after the fender. |

- Label: SIDE SKIRTS / REAR FENDERS · SLATS · GAS CAP, 34.7-36.4.

**REAR** (k = 36.531 + 0.9375 n)
- Camera: rear 3/4, passenger side -> centre (az -150 -> 180), el 18-22 deg. The whole rear half plus parked parts in frame.
- Base: the kitted car. p_wing at home over the Rear Wing Removed fill, compared at about 1.5 mm against the car minus the wing (Mazda 3 thin-part lesson).
- Moves:

  | kick | time | frame | move |
  |---|---|---|---|
  | k0 | 36.531 phrase | f1096 | the stock wing lifts straight up (0.15 m via), then parks top of frame (Z +0.6, Y +0.2), fully in frame, out of the ducktail's lane |
  | k2 | 38.406 | f1152 | the ducktail comes from behind and above: via 0.08 m above home, then down onto the deck |
  | k2.5 | 38.875 | f1166 | the diffuser slides forward (-Y) from behind, low, under the rear bumper |

- Labels:

  | time | label |
  |---|---|
  | 36.6-37.9 | REAR WING / REMOVED (over the exposed deck mounts) |
  | 38.5-40.2 | DUCKTAIL / DIFFUSER |

**LIVERY** (driver side, +X)
- Camera: continues round the tail. From driver rear 3/4 (az about +140), track forward along the side to about +75, el 8-10 deg.
  - The door-to-rear-fender graphic (BOMEX block, flame/claw, sponsor row) fills the width.
- Reveal: the grey paint plus the PSD projection (`livery_tex.py`, `mat_livery`) is revealed by a **hard-edged keyed wipe** along Y, following the camera. No cross-fade.
  - Starts on k0 (40.281). Complete by 42.156 (f1265).
  - The camera then drifts slowly across the slogan and sponsor row through the break, so they can be read.
- Paint scope: the kit parts get the same grey. Glass is dark (by height and normal). The scanned wheels are masked dark: **no stand-in BBS wheels.**
- No label: the livery text is the subject.

**HERO**
- Hard cut on 44.031. Driver-front 3/4, low (az about +35, el about 6 deg), with a 3-4 % push.
- The whole kitted car in frame with at least 6 % margins, both canards and the ducktail tip included.
- Load the clean car plus kit only, with no state-scan fills, so there are no frayed seams (c5 lesson).

## 5. Before assembly
- **Paths:** run pathcheck on every kit, ducting, mirror and grille path. No part may pass through the body or another part away from home.
- **Kit clipping:** count stock points inside each seated kit part.
- **Edge-touch:** test every frame of shots 3-11. Edge margins must be at least 20 px, parked parts included.
- **Labels:** check 4 frames per label window.
- **Luma:** scan each shot frame by frame. Persistent data stays off for any shot with keys.
- **Cuts:** measure on the decoded kick band.
- **Loudness:** about -14 LUFS, true peak below -1 dBTP.

`ive director` will flag the following. Log them as intended, each with its reason:
- N1a/STRUCT: a continuous push.
- The STRUCT swap: a same-camera state swap.
- N0 vs HERO: mirrored whole-car silhouettes, different state.
- KIT_FRONT vs N1a: same end of the car, but a build chapter, a different camera and different geometry.

Make a first/mid/last sheet of every new shot at preview resolution before any final render.

## 6. Open questions (do not guess)
1. **Data not in /blend yet:** Front_end_crash_foam_removed_2mm, bumper_shell_v5, mirror_r_scan and mirror_l_scan have no .blend in `/home/user/media/work/z400/blend/`. The foam STL is not in `nissan-400z/parts/` either. Prep them `--like car.json` and regcheck them (red over silver).
2. **Ducting vs foam state:** is the ducting inside bhr2 (does it z-fight there)? Is it **absent** from the foam-removed scan? If the foam-removed scan still has the ducting, the order flips: swap to foam removed first, then lift the ducting off it.
3. **Grille exit side:** front or back of the bumper? Take it from a section render (see BUMPER).
4. **Kit fenders:** full replacement panels or over-fenders? This decides how much stock skin must be carved, and confirms the stock fender is never shown coming off.
5. **Kit mirrors:** Ron's folder has Mirror V2 CAD (merged in `kit/merged`), but it is not in the prepped list and the mockups show stock mirrors. So the plan keeps stock mirrors. Confirm.
6. **Livery coverage:** the mockups show hood sponsors, a KAIDO★HOUSE windscreen banner, rear-window decals and gold wheels. The only artwork we have is the side PSD, and `livery/render/*.png` are mockup renders, not decal files. Plan: plain grey hood and windows, scanned wheels. Ask the user for the hood and window artwork if they want it.
7. The chapter-2 reset (hood, mirrors, ducting and foam back for the kit) is the one state jump. If the user rejects it, the alternative is a fast stock reassembly before 29.03. That costs about 1 bar and pushes the logo to bar 18 (about 49.7 s).
