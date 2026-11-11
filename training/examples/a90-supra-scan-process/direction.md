# A90 Supra scan-process reel - v2 direction (scene order + shot plan)

Scene director + director (stage 2) in one file. Supersedes the v1 timeline in `project.yaml`.
Inputs: CLAUDE.md, knowledge/lessons.md (all), style-guide.md, clips.md, project.yaml, editlog.jsonl,
feedback.jsonl, review.md, shots/*.json, `director_report.md` (v1, approximate), contact sheets of
`/home/user/media/work/a90sp/renders/{s1_rear,s2_front,s3_xray}` (looked at, 8 frames each).

Rules applied (newest win): v2 user brief; reviewer "cuts into nothing" + "scan under the front bumper, not blank";
coordinator feedback 2026-11-11 A-D (deliberate 9:16 crops, one sequence per section, front-bumper data is the
hero beat with factual labels, no state without its registered scan). Lessons: honda-civic-11 / honda-s2000 (no
implied data), porsche-gt3rs (translate into clear background, spin only to show a scanned backside), mazda-miata-nc
(focus one section, no wasted rotations), c5-corvette ("focus on removed areas and useful data"), FG2 (never reuse a
shot), honda-s2000 (don't hold the end), counter-easing lessons (static labels only).

Frame: one Artec frame, metres, +X nose, -Y = car's RIGHT side, Z up, ground z = 0. Car bbox x -2.19..2.19,
y -1.015..1.015, z 0..1.266 (car.json). Azimuth below = atan2(y, x) of the camera around the car centre
(0 = dead front, -90 = right side, +/-180 = dead rear).

## 1. Feature inventory

| region | scans (tris = STL header) | state / part | what it shows | quality / limits | richness |
|---|---|---|---|---|---|
| whole car | Chassis_(8.4m) 8,400,496 | base | full body, closed; on stands, underside scanned | no wheels anywhere (empty arches); keep cameras >= 1.2 m high, no low profiles | base |
| **front** | Front Bumper Outside 1,989,952 + Inside 1,991,743 | **part** (registered; bbox x 1.386..2.198) | bumper skin + scanned inner face (ribs, tabs - verified on the v1 s2 render turned 180 deg) | good, 2 mm | **5** (2 parts + 1 state) |
| front | Under Front Bumper 3,995,589 | **state under the front bumper** (registers; bbox x 0.614..2.178, z 0.05..0.85) | radiator support, crash beam, headlight units/mounts, cooling, ducts | good; already spliced in base_explode2 | (counted above) |
| front-right corner | Supra Fender 999,568 | **part** (bbox x 0.479..1.079, y -0.931..-0.821, z 0.10..0.71) | lower-rear section of the RIGHT front fender, outside skin only | 0.6 m panel; no inner face scanned -> translate only, never spin | **3** (1 part + 1 state + liners) |
| front-right corner | Supra Under Fender 1,992,817 (+ Washer Bottle 1,999,843, overlaps) | **state under that fender** (bbox x -0.01..1.15, y -0.97..-0.41, z 0.11..1.04) | inner fender structure behind the front wheel, washer bottle area | good; washer scan not in base (overlap) | |
| arches | Liners Trimmed Fused 1,115,356 | in base | all four arch liners | fills arches; no wheels | 1 |
| rear | Rear Bumper Outside 2,992,547 + Inside 2,992,597 | part scans exist, **but NO registered state under the rear bumper** | ducktail, diffuser, twin exhausts, tail lamps, plate recess (blank in the s1 sheet) | rear bumper must stay ON (rule D). Inside+outside claim is true as a static label | 2 (signature styling, no state) |
| rear (rejected) | 2024 'Supra Rear', 2021 no-bumper/all-removed/tail-light fragments, Rear End Cut, Front Corner | - | bumper-on skin / don't register (FPFH 5-8 %) / not in car frame | unusable for any state | - |
| trunk / hood / doors / interior | none | no open state | - | no trunk, hood or door shots | 0 |

IRL footage (clips.md): rear/rear-3/4 only (Jul 13 chase), Jul 7 shop clips with the rear bumper already off.
No scanning, crew, removal or front-facing footage -> the 1:1 opener is the rear.

Region ranking: **front (bumper + under-bumper) > front-right corner (fender) > rear (styling only) > rest**.
So: rear opens (forced by footage), the front bumper is the hero (most screen time, biggest move-in), the fender
corner rides the 15.68 s energy lift, the x-ray reassembly is the whole-car beat that lands on the listing.

## 2. Scene order (travel: rear -> right side -> front -> front-right corner -> right side -> rear-right listing)

| # | scene | scans used | feature shown | why here (inventory) | start-end s (frames @30) | beats | camera note (scan frame) |
|---|---|---|---|---|---|---|---|
| 0 | irl_open | v_0713_1944_44 36.067-39.200 | real Supra pulls up behind (whole car, ~35 % -> 67 % width) | only real 1:1 candidate is the rear approach | 0-3.182 (0-95) | 5 (pickup) | real footage, full frame, no punch-in |
| 1 | s1_rear (match) | base (bumper ON) | rear: ducktail, diffuser, exhausts, tail lamps | rear is the IRL side; styling only, no removal (rule D) | 3.182-6.932 (95-208) | 6 | starts on cam_B; push in to a low rear-right 3/4 detail |
| 2 | irl_pan | v_0713_1940_51 ~10.0-11.25 | real rear 3/4 rolling past the wheel | carries the travel from rear to side; real bronze wheels (scan has none) | 6.932-8.182 (208-245) | 2 | full frame, no crop |
| 3 | s2_front (HERO) | base_explode2 + fbump + fender (in place) | front bumper off, its inside, then the Under Front Bumper structure | richest region: 2 parts + registered state | 8.182-14.432 (245-433) | 10 | front-right 3/4 medium -> push in onto crash beam / radiator support |
| 4 | s3_fender | same objects, fender animated | right-front fender section off, Under Fender structure | 1 part + registered state, adjacent to the front | 14.432-16.932 (433-508) | 4 | right side, close on the fender; part moves on the 15.682 lift |
| 5 | s4_xray | base_explode2 + fbump + fender + rbump (rbump never moves) | x-ray: parts go home, whole car, ends on listing hero | whole-car beat; ends the travel at rear-right = listing angle | 16.932-23.432 (508-703) | 10 (+dissolve) | same-pose look switch, pull back, monotonic arc az -73 -> -122.5 to cam_listing |
| 6 | website | webzoom_a90.mp4 | listing, zoom-out, title, logo, URL | product end | 22.932-28.182 (688-845) | 8.4 | dissolve 0.5 s in; zoom lands 25.682 |

Music map (96 BPM, kicks 0.682 + 0.625k, bars 0.682 + 2.5n): 1:1 cut on bar 3.182; s1 -> IRL on kick 6.932;
IRL -> scan on bar 8.182; bumper lands on kick 9.432, inside faces lens by bar 10.682; s2 -> s3 on kick 14.432;
fender off ON the 15.682 energy lift; x-ray switch on kick 16.932; front bumper home on bar 18.182; listing pose
22.182, dissolve centred on bar 23.182; zoom-out lands on the 25.682 lift; last frame on bar 28.182.
`beats:` for project.yaml = [3.182, 6.932, 8.182, 9.432, 10.682, 14.432, 15.682, 16.932, 18.182, 23.182, 25.682, 28.182].

### Section coverage (rule B: each section in one continuous sequence)

| section | shots (contiguous) | seconds |
|---|---|---|
| rear | irl_open -> s1_rear -> irl_pan (pan exits toward the side) | 0-8.18 |
| front | s2_front | 8.18-14.43 |
| front-right corner / side | s3_fender | 14.43-16.93 |
| whole car (reassembly + listing hero) | s4_xray -> website | 16.93-28.18 |
No section returns. The x-ray end pose is rear-right 3/4 but WIDE, whole car, high (7.4 m, z 2.7) and in x-ray/grey:
it is the product hero, not a rear-detail repeat; s1 ends LOW and CLOSE so the two never share a view (check IoU < 0.6).

## 3. Per-shot plan (focus, camera, part action, holds)

### 0. irl_open - focus: the real car approaching
- `in 36.0667, out 39.2000, dur 3.1333` (94 frames, first clip one frame short - lesson). Match frame 39.200 s,
  car ~67 % of the width (was 40.4 s / ~95 %, "awfully close"). Car fully in frame for the whole clip (rule A).
- No text. Full 9:16 frame of the portrait 4K, scaled only.

### 1. s1_rear - focus: rear styling (ducktail, diffuser, exhausts, tail lamps)  RE-RENDER (new)
- t 0-0.4 s (3.182-3.582): exact cam_B (`match/cam_B.json`: pos -5.366,-0.409,1.009; 28 mm on 20.25 mm sensor), static,
  to sell the 1:1. Verify with an onion of output frames 94/95 before rendering the rest (cam_B carries a "bad" quality
  string in the file even at RMSE 5.8 px - the onion decides; emblem/exhausts/plate recess/mirror must sit within a few px).
- 3.582-6.932: one ease-in-out move, push in + swing right: end pos ~(-3.55, -1.95, 0.85), look (-1.75, -0.35, 0.55),
  28 mm. The rear-right corner (ducktail tip, right lamp, diffuser, right exhaust) fills the frame; the car is cropped
  deliberately at the B-pillar, with ~80 px of black under the diffuser - no accidental clip of the ducktail at the top.
  Swing direction must match the side irl_pan rolls past (open question 1).
- Rear bumper stays ON, nothing moves (no state under it).
- No wasted rotation: ~35 deg of orbit, every degree reveals the corner the IRL pan continues from.

### 2. irl_pan - focus: real rear 3/4 / wheel
- v_0713_1940_51, 2 beats (1.25 s) from ~10.0 s, full frame, no punch-in (rule A: wider real crops). No text.

### 3. s2_front - focus: front bumper, then what is behind it  (HERO)  RE-RENDER (camera new, part keys reused)
Cut in from IRL: first frame must be full (no "cut into nothing"): front section fills >= 60 % of the width.
- Opening frame: front-right 3/4, look (1.6, -0.15, 0.5), pos ~(5.10, -3.10, 1.30) (az ~ -40, 4.6 m), 28 mm. Nose to
  A-pillar in frame with ~8 % margins; the car is cut at the door on purpose, nothing else clipped (v1 s2 frame 1 clipped
  the rear haphazardly at the left edge and pulled back to a wide high view - both fail A/C, so the v1 render is not reused).
- 8.182-8.582 hold (static).
- 8.582-9.432 bumper (fbump = Outside+Inside, one object) translates loc (1.05, 0, -0.55): forward and down, out of the
  body into clear black below the nose. Lands on kick 9.432. (Same keys as v1 s2, proven clear of the body.)
- 9.432-10.682 bumper turns 180 deg about Z in place - justified: its inside IS scanned (ribs/tabs). Camera eases in
  ~10 % toward the bumper so its inner face reads.
- 10.682-11.307 hold on the inner face (1 beat).
- 11.307-13.182 camera pushes in over the bumper onto the exposed Under Front Bumper: end pos ~(3.30, -1.20, 0.95),
  look (1.75, -0.10, 0.45), ~35 mm. Crash beam + radiator support + right headlight mount fill the frame. If the turned
  bumper enters the lower frame here, drop it a further 0.3 m during the push (never across the structure).
- 13.182-14.432 hold with a slow lateral drift (~0.3 m toward -Y) along the beam to the right headlight mount and the
  right arch (Under Fender / liner edge visible) - leads the eye into s3. Detail must read: 2 mm scans, check at full res.
- Fender stays in place in this shot. Rear bumper untouched.

### 4. s3_fender - focus: right-front fender section and the structure under it  RE-RENDER (new)
- Front bumper stays at its s2 end pose (continuity; out of frame here).
- Opening frame (14.432): right side, close: look (0.78, -0.88, 0.45), pos ~(0.95, -3.05, 0.80) (az ~ -73), 35 mm.
  The fender section (x 0.48-1.08, z 0.10-0.71) + the empty front arch fill the frame; full frame, no black where the subject is.
- 14.432-15.057 hold (1 beat, fender in place).
- 15.057-15.682 fender translates loc (0, -0.55, -0.45): straight out of the body and down, into the black below the
  sill line, so it silhouettes clear of the car. Lands ON the 15.682 energy lift. No spin (outside skin only).
- 15.682-16.932 camera pushes in ~25 % onto the exposed Under Fender structure (z 0.4-0.9, washer-bottle area), fender
  piece still visible lower frame. End pose = s4 start pose.

### 5. s4_xray - focus: the whole car reassembled, ending on the listing hero  RE-RENDER (new)
- Starts on s3's last camera and part poses, `look: xray` (same-pose look switch on kick 16.932 - full frame, continuous).
  Start moving immediately (v1 report flagged the s2~s3 same view: no hold here).
- 16.932-17.557 fender slides home (translate only), lands on the kick.
- 16.932-18.182 camera pulls straight back and up to wide right-front 3/4 (az -73, ~6.8 m, z 2.4, ~45 mm), whole car in
  frame with margins; 17.557-18.182 front bumper un-turns and slides home (reverses its reveal), lands on bar 18.182.
- 18.182-22.182 monotonic arc az -73 -> -122.5 down the right side to `match/cam_listing.json` exactly (pos -3.977,
  -6.234, 2.725; 55.71 mm on a 36 mm sensor). No reversal of direction. Rear bumper never moves (rbump in place).
  Whole car fully in frame throughout (rule A).
- 22.0-22.93 morph to listing grey (clay 0.073, bg 0.0098 as tuned in v1), hold the listing pose 22.182-22.932 (morph is the reason).
- Render through 23.432 (dissolve tail).

### 6. website - focus: the listing, then logo/URL
- dissolve 0.5 s 22.932-23.432 (x-ray grey on the listing angle -> listing, IoU 0.955). WebZoom zoom-out lands 25.682,
  title -> logo -> URL in by ~26.4, hold ~1.8 s, last frame 28.182 (845 frames total). v1 held 7.43 s with 3.7 s dead;
  now 5.25 s. Music: fade 0.6 s ending 28.182 (track would run to 29.75 - open question 6).

## 4. HUD (ScanHUD, scan shots only, static `label`s - no `counter`; max two on screen, enter on a beat, out before the cut, top ~10 % of frame, off the subject)

| shot | frames @30 | title | sub | source |
|---|---|---|---|---|
| s1 | 102-150 | CHASSIS SCAN | 8,400,496 TRIANGLES | Chassis_(8.4m).stl header |
| s1 | 152-204 | REAR BUMPER | INSIDE + OUTSIDE SCANNED · 5,985,144 TRIANGLES | 2,992,547 + 2,992,597; inside verified on v1 renders. Static claim, bumper stays on |
| s2 | 258-300 | FRONT BUMPER REMOVED | - | Under Front Bumper state registers (real removal state) |
| s2 | 300-336 | INSIDE + OUTSIDE SCANNED | 3,981,695 TRIANGLES | 1,989,952 + 1,991,743 |
| s2 | 345-392 | UNDER FRONT BUMPER | 3,995,589 TRIANGLES | STL header |
| s2 | 396-430 | CRASH BEAM | RADIATOR SUPPORT · HEADLIGHT MOUNTS | names only if each is visible in the final close frames (else drop that word) |
| s3 | 455-505 | FENDER REMOVED | UNDER FENDER · 1,992,817 TRIANGLES | Under Fender header; fender section 999,568 not shown as text (keep to 2 lines) |
| s4 | 550-640 | 9 SCANS · ONE FRAME | 26,470,665 TRIANGLES | sum of the 9 headers used (8,400,496 + 1,989,952 + 1,991,743 + 3,995,589 + 999,568 + 1,992,817 + 1,115,356 + 2,992,547 + 2,992,597); out before the morph |
"What the scan is used for" labels: none placed - no file states the use (open question 3). No text on IRL or the listing.

## 5. Diff vs v1 (delivered a90_scan_process_v4.mp4)

| v1 shot | v2 | why |
|---|---|---|
| irl_open 37.28-40.42 (match 40.4) | moved to 36.07-39.20 (match 39.2, cam_B) | match frame was "awfully close" (car filled the frame) |
| s1_rear (rear bumper off) | **re-rendered, no removal** | no registered scan under the rear bumper (rule D); v1 showed the chassis' ragged underside |
| irl_shop (bumper-off shop clip) | **dropped** | shows a removal the scan cannot show; returns to the rear after travel (ping-pong); open question 2 |
| irl_pan | kept, moved to 6.93-8.18, uncropped | bridges rear -> side |
| s2_front | **re-rendered** (bumper keys reused) | v1 pulled back/up away from the data and clipped the car at the left edge; C wants a move-in on the Under Front Bumper |
| - | **s3_fender added** | registered part + state (Under Fender) never shown in v1 |
| s3_xray (moves the rear bumper) | **re-rendered as s4** | rear bumper may not move; starts from the fender pose |
| website 7.43 s | 5.25 s | ending held too long (3.7 s dead) |
Reused unchanged: no scan render (all three v1 renders violate A, C or D). Reused assets: base_explode2/fbump/fender/rbump
blends, cam_B, cam_listing, x-ray morph settings, webzoom_a90.mp4 (re-time to 5.25 s), the music.

## 6. Render budget (15 fps, +3 tail frames per shot; one Blender at a time, persistent data off, per-frame luma scan after each)
| shot | s | frames | look | est. |
|---|---|---|---|---|
| s1_rear | 3.75 | 60 | silver | ~14 min |
| s2_front | 6.25 | 97 | silver | ~23 min |
| s3_fender | 2.5 | 41 | silver | ~10 min |
| s4_xray | 6.5 | 101 | x-ray -> clay | ~5 min |
Total ~52 min. Preview each at 25 % / 4 spp first; check frames +/-2 around every cut for full frames.

## 7. Cut list / hold list
- Cut: v1 s1 bumper removal; v1 shop insert; v1 s2 pull-back; v1 x-ray rear-bumper return; 2.2 s of the website hold; any
  orbit that does not reveal a new section.
- Holds > 0.75 s: s2 13.182-14.432 (1.25 s, with drift) - time to read crash beam/mounts; website end ~1.8 s - URL read.
  All other holds are 0.4-0.75 s (match hold, bumper inner face, fender in place, listing morph).

## 8. Open questions (editor: don't guess)
1. Which side does v_0713_1940_51 10.0-11.25 roll past (car's right or left)? If left, end s1 rear-LEFT (mirror y) and
   keep the travel rear -> left pan -> cut to front-right is acceptable only if the pan exits at the front; otherwise pick
   a pan segment on the right side.
2. irl_shop dropped: OK with the user? (real bumper-off car next to a bumper-on scan.)
3. "Label what the scan is used for": what is this scan used for (e.g. the heart tail-light design)? Need the user's
   wording or a source file; nothing placed until then.
4. Washer Bottle scan (1,999,843, overlaps Under Fender): add to the s3 base only if it fills a visible gap; label
   "WASHER BOTTLE" only if it is legible.
5. cam_B: file says RMSE 5.8 px but quality "bad" - confirm with an onion before rendering s1; if it fails, re-solve
   at 39.2 s with points spread in depth (mirror tips) rather than move the match frame closer.
6. End at 28.182 with a 0.6 s fade, or ride the track to its hard end 29.75 (adds 1.5 s of URL hold - against "don't hold
   the ending too long")? Default: 28.182.
