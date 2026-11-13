# Nissan 400Z scan reel — v6 self-review (2026-11-14)

Output `/home/user/media/work/out/nissan_400z_scan_v6.mp4`: 1080x1920, 30 fps, 48.67 s, -14.4 LUFS, true peak -3.4 dBTP.

## User feedback on v5 -> v6
- **"Front bumper on the Kaido House bumper is cut funny ... it still uses part of the original bumper (check photos)"**:
  the Bomex front is a U-shaped surround around the stock nose and grille. v5 removed the whole stock bumper first, so the
  surround looked cut open. v6 kit bases keep the stock bumper + grilles; the surround lands over them (matches the photos).
- **"Bomex mirrors"**: Ron's folder Mirror/V1 Shell + Glass Backing (v5 had only read the V2 folder = internals). Installed
  on the bare mounts after the canards.
- **"Deep dish BBS LMs"**: no scan/CAD of the wheels on the Drive (searched). Procedural stand-in (tools/make_bbs.py:
  polished stepped lip, 20 cross-laced spokes, rivets, low-profile tyre) placed 20 mm inside the kit arch lips; hard 1:1
  swap for the stock wheels on the 34.656 kick (no hub scan exists to show wheels-off). Label: BBS LM WHEELS / DEEP DISH -
  STAND-IN MODEL.
- Re-rendered KIT_FRONT, KIT_SIDE, REAR, LIVERY, HERO; teardown shots unchanged from v5.

## Checks
Luma clean on all five; nothing touches the frame edge; cuts unchanged from v5 (all within half a frame of the kick);
12 labels, one at a time, all fully typed before they leave.

## Scores (1-5)
Hook 3 · Beat sync 5 · Scan quality 4 · Story 5 · Text 5 · Ending 4 · Technical 5.

## For the next agent
- Look at photos of the built car before deciding what a kit part replaces: add-on surrounds go OVER stock panels.
- List every version folder of a CAD part (V1/V2) before calling it missing.
- A part with no scan/CAD that the user asks for: procedural stand-in, hard swap, say STAND-IN on screen and in the delivery.

---

# Nissan 400Z scan reel — v5 self-review (2026-11-13)

Output `/home/user/media/work/out/nissan_400z_scan_v5.mp4`: 1080x1920, 30 fps, 48.67 s. Music: user's album audio from 19:50,
-14.4 LUFS, true peak -3.4 dBTP.

## User requests -> v5
- **"A bunch of parts that were removed didn't show up, including the grille"**: added the real part/state scans v2-v4 had
  skipped (400Z Scans folder; all already in the car frame, p50 1.3-2.9 mm): Upper Grille, Lower Grille (bumper alone,
  exploded forward), Air Ducting (lifts off the structure), Front end crash foam removed (1:1 state swap on the 21.49 kick),
  Side Mirrors (real part scans incl. mount base + harness, no glass). Every removed part has a beat and a label.
- **"Include the Bomex bodykit from Ron's folder"**: Ron's Folder / Nissan 400Z Bomex/Kaido House / STL via the service
  account. 64 print sections merged into 16 parts, rigid trimmed ICP to the scan (p20 2.2 mm, p35 3.9 mm, 0.9 deg).
  Installed in order after the teardown: front fenders -> slats -> bumper -> stock grilles back in -> canards; rear fenders
  -> skirts -> slats -> gas cap; stock wing off -> ducktail -> diffuser. Kit mirror files skipped (glass backing/skeleton only).
- **"And the livery files"**: 400z-full.psd layers (flame/alligator, BOMEX + slogan, rear claw, sponsor row) projected on
  both sides (passenger text pre-mirrored), BOMEX block on the hood, dark glass. Matched to the build photos the user sent:
  satin grey paint, KAIDO*HOUSE windscreen banner, stock grille inside the Bomex bumper.

## Checks
- Luma: no dark frames in any v5 render. Edge margins: first-pass finals clipped in STRUCT/KIT_SIDE/REAR/LIVERY/HERO;
  all re-framed and re-rendered, final sheets show every parked part fully in frame.
- Cuts (broadband half-rise): 420 -3.6, 504 +3.5, 701 +3.6, 785 -14.7, 870 +12.5, 984 +10.7, 1096 -13.5, 1209 +11.0,
  1376 -0.8 ms; 219 and 1321 within -16 ms of the measured kick (cutcheck window picks a louder non-kick hit).
- Labels: 11, one at a time, text from file/folder names, all in black space (SIDE MIRRORS moved to the top band).

## Scores (1-5)
Hook 3 (quiet 14 s intro = the chosen music) · Beat sync 5 · Scan quality 4 (raw capture noise in the bay/structure) ·
Story 5 (stock teardown -> kit build -> livery) · Text 5 · Ending 4 · Technical 5.

## Known weaknesses / for the next agent
- Windscreen banner font is a stand-in (Inter Display Black); no vector of the real KAIDO*HOUSE decal was supplied. The
  "KW automotive" strip and hood-side small sponsors in the photos have no files and are not shown.
- Wheels are the scanned stock wheels (photos show polished deep-dish wheels; no scan of them).
- Kit fenders sit over the stock fenders (no fender-removed scan), so the stock fender never comes off on screen.

---

# Nissan 400Z scan reel — v4 self-review (2026-11-13)

Output `/home/user/media/work/out/nissan_400z_scan_v4.mp4`: 1080x1920, 30 fps, 1320 f (44.00 s).

## User feedback on v3 → v4 changes
- **"Music too large"** (read as too loud): v3 measured −10.5 LUFS, +0.4 dBTP (clipping). Music gain 0.63 (−4 dB) →
  v4 measures **−14.4 LUFS, −3.5 dBTP**.
- **"Nothing should come off the bumper until the bumper itself comes off"** (recorded as a rule): v3 pulled the grille out
  first. Now grille + bumper shell share one key set — seated until the 14.971 kick, out together, up out of frame by
  16.846. In s8b the grille stacks inside the bumper (same offset/delay), so it also goes home with it.
- N1a re-rendered at native 30 fps: under minterpolate the fast bumper exit tore (f491-503). Checked frame by frame: clean.

## Cut timing
420 −3.6 · 534 +5.1 · 701 +3.6 · 785 −14.7 · 870 +12.5 · 1010 −5.3 ms; 219 −11 ms vs the 7.311 intro kick. All within ±½ frame.
(cutcheck lists f488-501: the bumper unit's motion inside N1a, not cuts.)

## Scores (1–5)
Hook 3 (quiet 14 s intro is the track) · Beat sync 5 · Scan quality 4 · Story 5 (parts now come off in a physical order) ·
Text 5 · Ending 4 · Technical 5 (level −14.4 LUFS; no interpolation tearing on fast parts).

## For the next agent
- Child parts travel with their parent panel; separate them only after the parent is off (lessons.md rule).
- Any shot where a part leaves the frame fast: render at native 30 fps, not 15 fps + minterpolate.
- Measure the mix (loudnorm summary) before delivery; aim near −14 LUFS, true peak below −1 dBTP.

---

# Nissan 400Z scan reel — v3 self-review (2026-11-12)

Output `/home/user/media/work/out/nissan_400z_scan_v3.mp4`: 1080x1920, 30 fps, h264 yuv420p, AAC, 1320 f (44.00 s).

## User feedback on v2 → v3 changes
- **"Logo needs to be bigger"**: card logo 340 → 640 px wide, fades in on the 41.172 kick, ends on the 44.03 phrase.
- **"Side mirror coming off took a part of the window with it"**: the parts.py diff had flagged door-glass triangles
  (|x| 765–783 mm; glass scans differently between sessions) as mirror. Fitted the glass plane, dropped everything within
  8 mm / inboard from both mirror parts, rebuilt comp_explode with the trimmed parts, re-rendered N2 and s8b. Checked: the
  mirror lifts off alone, the window stays on the door.
- **New music (album audio from 19:50)**: 128 BPM, 14 s quiet intro, drop 14.031. Intro = N0 (7.27 s) + H (6.7 s), both
  re-rendered with longer moves; bumper-off hero on the drop; cuts on measured half-rise onsets.
- Also: N2 re-rendered at native 30 fps (minterpolate left ghost trails on the fast mirror); s8b re-render cleared its old
  dark f101-112 tail.

## Cut timing (cutcheck, broadband half-rise)
219 −11 ms vs the 7.311 intro kick (cutcheck's ±120 ms window picks a stronger non-kick hit at 7.194) · 420 −3.6 · 534 +10.8 ·
701 +3.6 · 785 −14.7 · 870 +12.5 · 1010 −5.2 — all within ±½ frame.

## Scores (1–5)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 3 | Quiet 14 s intro (user's music choice); car orbits under the fade from frame 1, but the first big moment is at 14 s |
| 2 | Beat sync | 5 | 7/7 hard cuts within ±½ frame |
| 3 | 1:1 match | N/A | scan only |
| 4 | Scan quality | 4 | mirror/glass fixed; bay and radiator capture noise is real; N2 wheel spokes have scan holes |
| 5 | Story | 4 | unchanged section order, hero on the drop |
| 6 | Grade | N/A | |
| 7 | Text | 5 | two factual labels over scan only |
| 8 | Ending | 4 | reassembly locks near the 37.43 kick, fade, bigger logo on 41.17, ends on the phrase at 44.03 |
| 9 | Technical | 5 | spec correct, no dark/dup frames at cuts, no interpolation ghosting on N2 |

## For the next agent
- parts.py diffs pick up glass/trim that scanned differently between sessions; fit and strip the glass plane before using a
  door-mounted part, and look at the part alone from the side before rendering.
- Fast small parts ghost under minterpolate: render those shots at native 30 fps.
- s5_tail -> N3 still joins two close badge framings (see v2 notes).

---

# Nissan 400Z scan reel — v2 self-review

Output: `/home/user/media/work/out/nissan_400z_scan_v2.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p, AAC, 1151 frames (38.37 s).
Scope: scan-only Temerario-style reel. There is no IRL footage, so criteria 3 and 6 are N/A.

## What changed from v1
These changes follow the v2 brief and addendum A–D relayed from the user.

- **Order, from scan features (direction.md and director.md):**
  1. Whole car.
  2. Engine bay, from the real Hood Open scan.
  3. Front bumper removed: grille out, then shell out. This is the hero section.
  4. Structure, from the 2 mm "Bumper and hood removed" scan, with two labels.
  5. Right mirror off.
  6. Tail detail.
  7. Wing off.
  8. Reassembly.
  9. Fade to black, then a small logo.

  Travel runs front → side → rear with no ping-pong, one sequence per section, and no reused shots.
- **Removed or opened states:** each one is shown only from its own registered scan. There is no animated hood opening and no trunk shot, because there is no trunk scan.
- **Labels:** exact wording, over scan shots only.
  - FRONT BUMPER REMOVED / SCAN: BUMPER AND HOOD REMOVED
  - CRASH BEAM / BEHIND THE FRONT BUMPER, shown over the visible beam
- **Renders:** persistent data was off for every new shot.
- **Luma dropout check:** every new shot is clean. The s8b reused render has a dark tail at frames 101–112; it is unused and faded to black (logged).
- **Cut timing:** measured against the decoded audio with the broadband 1 ms RMS half-rise (`tools/cutcheck.py`).

  | Cut frame | Offset (ms) |
  |---|---|
  | 112 | +12.3 |
  | 222 | −11.1 |
  | 333 | −5.1 |
  | 499 | −9.5 |
  | 579 | −15.9 |
  | 665 | −13.7 |
  | 801 | +1.6 |

  All are within ±½ frame (16.7 ms). The first assembly had five cuts at 17–28 ms, all one frame off; I retimed N0, H and N3.
- **Framing (first, middle and last frame of every shot):**
  - N3: the wing left the top of the frame for about 2 s, so the lift was reduced. Its left tip was then clipped at the end of the shot, so the end camera was widened from f35 to f27.
  - N0: the whole car stays in frame from the first frame.

## Scores (1–5)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | The car is orbiting under a 1.2 s fade-in; motion is visible by about 0.6 s. A fade-in, not a hard open. |
| 2 | Beat sync | 5 | 7/7 hard cuts within ±½ frame of the measured onset. |
| 3 | 1:1 match | N/A | No IRL footage in this reel. |
| 4 | Scan quality | 4 | Silver on black. Scan noise in the bay and on the radiator is real capture, not cleaned. The N2 wheel spokes show scan holes. |
| 5 | Story | 4 | Whole car → bay → bumper off → structure → mirror → rear → wing → reassembly. Bumper-removed data is the hero section and is labelled. |
| 6 | Grade | N/A | Scan only. Uniform ×0.955 gain. |
| 7 | Text | 5 | Two labels, factual, no numbers, over scan only. Legible at phone size; the full sub was checked at f493. |
| 8 | Ending | 4 | s8b reassembly fades out from 31.5 s, then a 0.8 s black lead, then a small 340 px logo, with the music fading 1.2 s. |
| 9 | Technical | 4 | Spec is correct. The reel is 1151 frames, not 1152: the first clip comes out one frame short, which is a known assembler behaviour. No black or duplicate frames at cuts. |

## Known weaknesses for the next agent
- **Rear jump cut:** s5_tail (a reused v1 push-in) ends on almost the same badge framing that N3 starts on. I started N3 six source frames in so the wing is already lifting on the cut. It still reads as a continuation more than a new shot. Next time, render the tail and wing as one continuous move.
- **Engine bay into bumper hero:** H ends wider and closer than N1a starts. The cut steps back a little; it is acceptable but not a clean progression.
- **Frame-diff cut detection:** cutcheck flags the fast part exits in N1a (frames 280–331) as cuts. Read the cut list against the timeline, not blindly.
