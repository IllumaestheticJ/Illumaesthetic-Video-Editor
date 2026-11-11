# Direction - Honda Civic EK scan-process reel, v4

Scene director, 2026-11-11. Format: 240SX-style (IRL -> 1:1 cut on the drop -> scan scenes -> website listing).
Inputs read: CLAUDE.md, knowledge/lessons.md, style-guide.md, project.yaml (v3), editlog, feedback, clips.md,
director_report.md, contact sheets of every existing render (first/middle/last + strides) and of every candidate IRL clip.

Standing rules applied: A (cropping: wide = whole car, nothing clipped), B (each section once, one continuous run),
C (no bumper-removed data -> no bumper section), D (no openings: no hood/hatch/door open, nothing comes off),
reviewer rules "nothing comes off the EK", "never reuse a shot", "rotations are wasted", "last scenes held too long",
"no text over IRL", "HUD only exact numbers".

## 1. Feature inventory

One scan file only: `EK Civic EK Full Car Scan.stl` (24,997,508 triangles, STL header). No part scans, no state scans.
Listing says "Dataset: Exterior Only".

| region | what the scan shows (from the renders) | states | parts | quality / weak data | richness |
|---|---|---|---|---|---|
| front | grille + H badge, headlights, bumper, plate (8GEX521, legible) | none | none | good; **wiper/cowl ragged** (visible in final_s2 f1, top views) | medium (best surface detail, opener) |
| left side (+X) | doors, mirror, multi-spoke wheels (spokes captured) | none | none | good | low-medium |
| right side (-X) | same as left, fender marker lamp, molding | none | none | good | low-medium |
| rear (+Y) | hatch glass, roof spoiler, taillights, rear bumper, plate frame | none | none | glass/lamp lenses not checked close - see Q3 | medium (spoiler + hatch shape = EK signature) |
| top | roof, hatch glass, hood | none | none | cowl ragged; fine from high/moving | low |
| wheels | 5-double-spoke rims, tyres | none | none | captured well in s2 | low (no wheel-off scan) |
| engine bay / interior / underside | not scanned | - | - | - | **none - no scene** |

Signature features (from the scan, not memory): the 3-door hatch profile (short tail, roof spoiler, near-vertical hatch)
and the EK front (grille + headlight shape). Reveal ladder for this car = exterior wide -> detail -> top / hero pass -> listing.
States and explode rungs are **left out** (no data, rule D + reviewer rule).

## 2. What I saw in the existing material

- `final_s1` (cam_A, front-left 3/4 eye level): car fully framed f1-f32; **from ~f33 the rear touches the right frame
  edge (x = 809/810) and the nose sits 18 px from the left edge by f51** -> rule A says use f1-f32 only.
- `v2/final_s2` (cam_B): f1 is a tight right-fender close-up with the **ragged cowl/wiper filling the top-left**; f35
  is a small front-right 3/4; f68-f101 right side -> rear-right. Tight cut + weak data + ping-pong vs S1 (left) -> drop.
- `v3/final_s3`: starts front-left (third front-left view of the reel), car only ~10 % of the frame, ends on the listing
  hero -> its start is redundant with S1; its end is what we need.
- `v_2003_40` (0.2-1.8 s): **wide LEFT side** (nose to frame right), whole car side incl. rear, operator's hand + scanner in
  the foreground. Nose bumper is cut by the right edge, rear goes out left after ~2.0 s. Not a clean 1:1 candidate
  (foreground scanner, nose cut), but the best wide "scanner in action" beat and it is on the side we travel along.
- `v_1958_06` (0-1.6 s): **wide rear, slightly right of centre (shallow rear-right 3/4, ~15-20 deg)**, whole car in frame,
  crew member at the left edge beside (not over) the car around 1.0-1.5 s; at 2.5-6 s he walks in front of the car.
  8.5-14.5 s: close powder spraying on the hatch glass / spoiler / taillight. -> **this is the wider 1:1 candidate for cut B.**
- `v_2003_29`: right door -> right fender close-up. Off the travel (right side) and tight -> drop.
- `v_1955_14`: front, low, crew spraying - second front IRL shot, ping-pong -> unused.

## 3. Scene list (v4, in order)

Beat grid: t = 3.200 + 0.46875 k. Video starts at t = 0 (k = -6.83).

| # | scene | source | feature / section | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | irl_powder_front | v_1957_24 1.8686-5.0353 (as v3) | front (IRL) | powder starts at the front; ends on match A | start - k0 (3.2 s) | unchanged; ends on f150 = 5.002 s |
| CUT A | 1:1 hard cut ON THE DROP | | | | k0 | cam_A |
| 2 | scan_front | `final_s1` **f1-f32 only** | front -> front-left (scan) | front = best surface detail, opener; the drop | k0-k5 (2.344 s) | reuse; src_fps = 32/2.344 = 13.65, interpolate. Stops before the rear hits the frame edge. HUD label here |
| 3 | irl_scanner_left | v_2003_40 in 0.20 out 1.61 | left side (IRL) | S1's orbit already turns toward the left side; IRL continues the travel down the left flank with the scanner in hand | k5-k8 (1.406 s) | wide side; no text. Do not go past ~1.9 s (rear leaves frame) |
| 4 | irl_powder_hatch | v_1958_06 ~10.0-12.34 | rear detail (IRL): powder on hatch glass / spoiler / taillight | travel reaches the rear; rear detail next to the rear wide | k8-k13 (2.344 s) | pick the 2.34 s window with the spray gun on the glass; editor checks no plate-number legibility issue |
| 5 | irl_rear_wide | v_1958_06 in 0.0 -> match B2 (~1.0-1.4 s) | rear wide (IRL) | whole car in frame -> **wide cut B** (brief: widen the 1:1) | k13-k16 (1.406 s; if match < 1.40 s, start this at k14 and give #4 one more beat) | ends on the solved match frame; move `in`, never `out` |
| CUT B | 1:1 hard cut | | | | k16 | **new cam_B2** (solve, see diff) |
| 6 | scan_rear | **new render S2'** | rear: hatch, spoiler, taillights -> top | rear = EK signature (hatch + spoiler); one continuous rear run | k16-k28 (5.625 s) | 1:1 from cam_B2, eased push-in + crane up over the hatch to a high rear view (see diff) |
| 7 | software_align | sr_align_v2.mp4 (as v3) | process | sits in the music break | k28-k32 (1.875 s) | unchanged |
| 8 | scan_sweep_hero | **new render S3'** | top -> hero (listing angle) | ladder rung "top / hero pass"; ends on the listing hero (240SX lesson) | k32-k42 (4.688 s) + 0.5 s dissolve tail | from high/top over the car, descend to cam_end; sweep raw -> solid; morph to listing grey done by k41 |
| DISS | dissolve 0.5 s | | | same angle -> one object | k42 | |
| 9 | website | WebZoom **re-timed to 4.69 s** | listing, logo, URL | end card, shortened (v3 had 2.7 s dead) | k42-k52 (4.688 s) | zoom out 0-1.5 s, title ~1.0 s, small logo ~2.0 s, URL fades in ~2.6 s, holds ~1.5 s; no static tail |

Total: 27.575 s (v3: 31.8 s). Sections in order: front (IRL) -> front (scan) -> left side (IRL) -> rear (IRL detail -> wide)
-> rear (scan) -> process -> top/hero -> listing. Each section appears in one run; no front -> rear -> front cut except the final
hero landing (see Q1).

HUD (re-render `hud_ek_v4.mov`, Remotion, cheap): one static label `24,997,508 / TRIANGLES CAPTURED` on scene 2 only,
enter ~k1, leave by k4.5 (before the cut). Nothing over IRL (scenes 1, 3, 4, 5). Optional on scene 6 or 8: `EXTERIOR SCAN`
(backed by the listing's "Dataset: Exterior Only") - max one item, editor's call. No other numbers.

## 4. Music map ("THE DEATH", 128 BPM, beat 0.46875 s)

| k | video t (s) | music | event |
|---|---|---|---|
| -6.83 | 0.000 | build -> silence -> snare fill | IRL front powder (riser over the settled pull-back) |
| 0 | 3.200 | **DROP** | 1:1 cut A -> scan_front |
| 5 | 5.544 | kick | IRL scanner, left side |
| 8 | 6.950 | bar 3 downbeat | IRL hatch powder |
| 13 | 9.294 | kick | IRL rear wide |
| 16 | 10.700 | bar 5 downbeat | **1:1 cut B** -> scan_rear |
| 28 | 16.325 | 2-bar break starts | software alignment |
| 32 | 18.200 | **phrase re-entry** | scan sweep -> hero (biggest scan moment after the drop) |
| 42 | 22.888 | kick | dissolve into the listing |
| 52 | 27.575 | bar 14 downbeat | end (0.4 s audio fade into it) |

Every cut on a k-grid beat; whole-frame durs per lessons (first clip one frame short; check with tools/cutcheck.py).
The track's own drop-out at k60 is no longer used - see Q2.

## 5. Diff vs v3

| v3 clip | v4 | change | reuse / re-render |
|---|---|---|---|
| irl_powder_front (k-7-k0) | scene 1 | unchanged | reuse |
| scan_hero `final_s1` (k0-k7, all 51 f) | scene 2 | **trimmed** to f1-f32, k0-k5 (rear hits the frame edge from f33 - rule A) | reuse, retime only |
| irl_scanner v_2003_40 0.60-1.60 (k7-k9) | scene 3 | **moved** to k5-k8, in 0.20-1.61 (wider: whole left flank) | reuse source |
| irl_scanner_pass v_2003_29 (k9-k16) | - | **dropped**: right side (ping-pong after a left-side orbit) and ends on a tight fender close-up | - |
| - | scene 4 irl_powder_hatch | **added** (v_1958_06 ~10.0-12.34) - rear detail next to rear wide | new IRL cut, no render |
| - | scene 5 irl_rear_wide | **added** (v_1958_06 0 -> ~1.4) - the wide frame for cut B | new camera solve cam_B2 |
| scan_orbit `v2/final_s2` (k16-k28) | scene 6 scan_rear | **dropped and replaced**: s2 opened on the ragged cowl, showed the right side (ping-pong) and a 3rd orbit | **re-render S2'** (~12-15 min) |
| software_align (k28-k32) | scene 7 | unchanged | reuse |
| scan_sweep `v3/final_s3` (k32-k44) | scene 8 | **replaced**: s3 opened on front-left (same as S1, rule B) with the car at ~10 % of frame | **re-render S3'** (~12-15 min); reuse cam_end, sweep shader, morph values (clay 0.06 / bg 0.015) |
| dissolve k44 | k42 | moved | - |
| website 7.5 s (k44-k60) | scene 9 4.69 s (k42-k52) | **trimmed 2.8 s** (kills the 2.7 s dead hold) | re-render WebZoom props (Remotion, minutes) |
| hud_ek_v3 | hud_ek_v4 | retimed to scene 2 | re-render (Remotion) |

Orbit count: v3 had three orbiting scan shots (s1, s2, s3). v4 has one short eased arc (s1 trimmed to 2.3 s), one push/crane
(S2') and one descent to the hero (S3') - no two moves on the same section.

### Re-render notes (scan frame: front -Y, rear +Y, car's left +X, right -X, Z up, ground 0, centre ~(0,0,0.6), L 4.2 m, W 1.87 m)

**cam_B2 (solve first, before S2').** v_1958_06 at the chosen match frame (look at 1.0-1.5 s; pick the frame where the crew
member is clear of the car's left rear corner and the camera is steadiest; measure drift with phaseCorrelate if needed).
Expected pose (sanity check for the solver, not a target): camera behind and slightly to the car's RIGHT, about
(-1.3, +6.0, 1.4) looking at ~(0, +0.8, 0.7), i.e. ~15-20 deg off the rear axis, eye/phone height. Landmarks spread in
depth: both taillight outer corners, spoiler tips, hatch emblem, plate-frame corners, both rear wheel contact points,
right mirror tip / roof front corner (for depth -> focal is observable; iPhone wide, expect ~18-24 mm on the 20.25 mm
portrait sensor like cam_A, not 28 mm). Silhouette refine with the crew member masked. Verify with an onion render.
No `--like` change: use the same yaw-aligned prepped scan as cam_A/cam_B/cam_end.

**S2' scan_rear (k16-k28, 5.625 s, ~85 frames @ 15 fps, render ~6 s).**
- f1 = cam_B2 exactly (1:1). Silver look, <= 4 mm decimation (<= 2 mm if the push gets close to the spoiler).
- 0-0.6 s: continue the IRL handheld drift direction, barely moving (cut must read as 1:1).
- 0.6-3.0 s: eased push-in ~12 % toward the hatch centre (target ~(0, +1.9, 1.0)) - spoiler, hatch glass, taillights fill
  the upper/middle frame; the rear bumper may crop at the bottom here (it is the detail beat), roof spoiler must not clip.
- 3.0-5.6 s: crane up and slightly over: end ~(-0.4, +4.2, 4.2) looking at (0, +0.2, 0.5), up vector toward the nose
  (-Y) so the car's length runs up the 9:16 frame and the whole car is back in frame (rule A: wide = whole car, ~80 px
  margins). Stays on the right/centre - do NOT swing to either flank (sides are done).
- Before rendering frames 1-85, check a 25 % preview of the push-in frame for taillight / hatch-glass holes (lesson:
  lenses are often scan holes); if blotchy, aim the push at the spoiler + hatch emblem instead.

**S3' scan_sweep_hero (k32-k42 + 0.5 s dissolve, ~5.2 s, ~78 frames @ 15 fps).**
- Start high above the car, near top-down over the rear half: ~(0, +2.0, 6.5) looking at (0, 0, 0.6), up = -Y (nose up
  in frame) - picks up where S2' ended, different from every other shot. Raw dark look.
- Scan-line sweep front -> rear (-Y -> +Y) turning the raw scan into the solid model, same shader as v3 S3; with the car
  top-down the line crosses the whole frame - finish the sweep by ~2.8 s.
- Camera: eased descent and arc to the car's LEFT front (+X, -Y) landing exactly on the stored `cam_end` (listing hero,
  front-left 3/4 elevated) at ~3.9 s; then hold still. Keep the top view high and moving while the cowl is in frame
  (ragged data).
- Morph to listing grey (clay 0.06 / bg 0.015 linear, car median ~136 / bg 26 sRGB) from ~3.4 s to 4.4 s - fully done
  before the dissolve at k42 (4.69 s), last 0.5 s static for the dissolve.
- Car size: v3 S3 ended at ~10 % cover because cam_end is defined in the WebZoom frame (startScale 1080/1424). Keep that
  end pose (the dissolve depends on it), but frame the top view so the car fills ~70 % of the frame height at the start.

**WebZoom v4:** same listing capture and focus, compress to 4.69 s + 0.5 s overlap; logo small; URL last; no static tail.

## 6. Open questions (do not guess)

1. **Hero landing vs rule B.** The listing hero is front-left 3/4 elevated, the same section as S1 (front-left eye level).
   I kept it because the 240SX/FG2 lessons require ending on the listing angle and S3' only *lands* there (~1.3 s incl. the
   still). If the reviewer still reads it as a repeat, the alternative is a re-solve of cut A on an earlier, wider
   v_1957_24 frame - but the match A frame is fixed by where the pull-back settles. Editor: flag it to the user, don't decide.
2. **Ending at k52 instead of the track's own drop-out at k60.** 27.6 s with a 0.4 s fade on a bar line. If the fade sounds
   abrupt, fall back to k56 (website 6.56 s, still 0.9 s shorter than v3 and no dead hold if WebZoom adds a slow push).
3. **Rear scan quality.** I only saw the rear at small scale (s2 f101). Taillight lenses / hatch glass may be holes; preview
   before committing S2' to the push-in target.
4. **v_1958_06 match frame.** 1.0-1.5 s looks clean at contact-sheet scale; confirm the crew member is not over the car at the
   exact frame and that the car's right flank is not clipped by the right frame edge. If 0-1.6 s is unusable, fall back to
   v3's cut B (reuse `v2/final_s2` f1-f34 trimmed) and tell the user the wider frame was not available.
5. **Plate legibility.** The scan front shows plate 8GEX521 legibly (S1); the IRL rear has a dealer plate frame. v1-v3 showed
   it without feedback - keep, unless the user wants it deplated.
6. **v_2003_40 foreground scanner.** The operator's hand + scanner crosses the lower left; no text goes there anyway. If the
   reviewer wants a cleaner wide side, there is no other wide left-side IRL clip.
