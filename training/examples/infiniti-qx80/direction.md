# Infiniti QX80 - scene direction v2 (scene-director, 2026-11-11)

Inputs read: CLAUDE.md, knowledge/lessons.md (all), style-guide.md, clips.md, project.yaml, editlog.jsonl, review.md,
tools/shots.py, the parent's v2 brief (user notes for all reels), `python -m ive director` report (director_report.md).
No feedback.jsonl exists for this project yet; the v2 notes are the sibling-reel notes the user applied to every reel.
Contact sheets I looked at: /tmp/claude-0/qx/director/sheet_*.jpg, s7_frames.jpg, check/parts.jpg.

## 1. Feature inventory (from the scans, not the model name)

| Region | Signature features (seen in renders) | States (registered) | Parts (registered, clean) | Weak data | Richness |
|---|---|---|---|---|---|
| Front | huge vertical-fin grille + badge (fins resolve at 4 mm, s3), slim lamps, RF bumper corner + ducts | **Hood open** (Hood Underside, hinge fit 37.2 deg, real under-hood capture) | hood panel, **Fender Inner** (clean RF fender), **Side Vents** (both fender vents), **Front Bumper Duct** (RF corner + left duct, 7.2 mm - weakest fit) | under-hood has dark gaps; no scan under fender / bumper corner / vents (holes if pulled far) | **5 (1 state + 4 parts + grille)** - richest |
| Side | 22" multi-spoke RF wheel (resolves, s4), fender vent | door-open = fragments, unusable | (vents counted in front) | skirt/door fragments | 1 |
| Rear | tail-lamp bar, roof spoiler, two exhaust trims | none | **Wing Only** (roof spoiler), **Exhaust cover** (2 trims) | no scan under spoiler/trims; plate - check before close-ups | 2 |
| Top | roof | none | spoiler (rear) | roof clips bright in top-down (s6), nothing else up there | 0 |
| Interior / engine | - | under-hood only via hood state | - | no engine/interior scans of this car (GT-R swap CAD is not this reel) | - |

Not usable: Right Fender No Vent (partial corner), Right Side Skirt Door Open (fragments), mirror / calipers / T-spec
bumper / NACA ducts / badge (bench frames, not registered), Rear Bumper Inner (1 % overlap).

## 2. Look at v1 (what the renders actually show)
- s1_front34: front-right turntable, **rear cut off the left edge the whole shot** (brief item 4: opening must show the whole car) -> drop.
- s2_rear34: rear-left orbit, **front cut off**, IoU 0.76 with s1 (director report: same view twice) -> drop.
- s3_grille: grille fins + badge sliding close-up, sharp, lots of detail -> keep (face at a new scale = new information).
- s4_wheel: RF wheel push-in, the RF fender vent is in frame -> keep (sets up the vents coming off).
- s5_hood: high front-right, hood opens on the hinge, under-hood capture read -> keep unchanged.
- s6_top: rotating rise to top-down; roof clips white, shows no feature -> drop (wasted rotation, weak data).
- s7_explode: all six parts fly up at once in one wide 8.4-8.8 m orbit, car ~60 % width, parts tiny, **black holes**
  where fender/bumper corner left (frames 60-130), 2.1 s dead hold after lock -> drop (brief items 2, 6, 7).

## 3. Scene order v2

Travel: front (whole -> face -> RF corner -> hood state -> front parts) -> rear (rear parts) -> wide reassembly from the
unseen front-left -> logo. No ping-pong: v1's front -> rear -> front -> wheel -> front is gone.

| # | scene | scans used | feature shown (focus) | why here (inventory) | music in -> out (beats) | camera note |
|---|---|---|---|---|---|---|
| 1 | **N0_open** (NEW) | car4 | whole car, front-right 3/4 | opens on the front = richest region + grille signature; whole car (item 4) | 0.66 -> 5.962 (8, intro to phrase) | slow 18 deg orbit + dolly, whole car in frame from frame 1 |
| 2 | s3_grille (reuse) | car4 | grille fins + badge | signature feature, best-resolved detail | 5.962 -> 8.562 (4) | as rendered, slowed |
| 3 | s4_wheel (reuse) | car4 | RF wheel + fender vent | side detail next to the front; plants the vent that comes off in 5 | 8.562 -> 11.162 (4) | as rendered |
| 4 | s5_hood (reuse) | base_hood + hood | hood opens -> under-hood capture | the one real state; opens 11.812 -> 13.762 (lands on the low hit) | 11.162 -> 16.362 (8) | as rendered |
| 5 | **N1_front** (NEW) | x_base_explode + hood, bumper duct, vents (split L/R), fender | RF corner parts come off one by one, hood lifts off on the lift | richest region gets the biggest moment (21.56 lift) and the steps leading in (18.95, 20.90) | 16.362 -> 24.162 (12) | close on RF corner, then pull back to the front stack |
| 6 | **N2_rear** (NEW) | same + wing, exhaust cover | spoiler lifts, exhaust trims slide out | the rear's two parts; short because the rear is a 2-part region | 24.162 -> 28.062 (6) | rear-left 3/4, push in |
| 7 | **N3_reassemble** (NEW) | all parts -> clean car4 on lock | everything flies home rear -> front, hood shuts on the 32.00 step, clean car | reassembly from a new angle (front-left, never shown); clean car hides joint seams (c5 lesson) | 28.062 -> 34.562 (10), lock 31.962 | high front-left, descending; fade last 2 beats |
| 8 | logo (small) | logo card | - | ending | 34.562 -> 39.5 (end 38.84 video) | logo_card --width 360 (v1: 720 = too big, item 7) |

## 4. Music map (music t; video t = music t - 0.66)
Grid 0.112 + k*0.650; phrases from 0.762 every 8 beats (5.962, 11.162, 16.362, 21.562, 26.762, 31.962).
- 0.66 N0 starts with the music (first sound 0.685). 5.962 phrase -> grille. 8.562 -> wheel. 11.162 phrase (build steps up) -> hood.
- 13.762 low hit = hood fully open. 16.362 phrase -> N1. 17.012 bumper corner out; 18.962 step (18.95) vents out;
  20.912 step (20.90) fender out; **21.562 lift (-18 -> -10 dB): hood lifts off + camera pulls back**.
- 24.162 -> rear (N2): 24.812 spoiler up, 25.462 exhaust trims out.
- 28.062 -> N3 wide; fly-home 28.712 -> **31.962 lock (step 32.00)** = hood shuts, swap to clean car.
- 33.262 start fade to black (2 beats); **34.562 step (34.60) logo**; music fades 37.8 -> silent 39.5.

## 5. Diff vs v1
| v1 | v2 | why |
|---|---|---|
| s1_front34 0.66-5.96 | **dropped**, replaced by N0 (same slot) | crops the rear; brief: whole car from frame 1 |
| s2_rear34 5.96-9.21 | **dropped** | front cropped, IoU 0.76 with s1, and it caused the front->rear->front ping-pong; rear is now shown by N2 with its parts |
| s3_grille 9.21-11.16 | moved to 5.96-8.56, 4 beats (was 3) | face detail right after the face-forward opener |
| s4_wheel 11.16-13.76 | moved to 8.56-11.16 | side detail between face and hood; vent payoff in N1 |
| s5_hood 13.76-18.96 | moved to 11.16-16.36, same length/timing inside | hood open now ends on the 13.762 hit |
| s6_top 18.96-21.56 | **dropped** | rotation with nothing new; roof clips |
| s7_explode 21.56-34.56 | **dropped**, replaced by N1/N2/N3 | one wide all-at-once orbit, holes, small parts, dead hold (items 2/6/7) |
| logo 720 px | logo 360 px after a 2-beat fade | item 7 small logo |

Reused as-is (only position/speed changes): s3_grille, s4_wheel, s5_hood. New: N0, N1, N2, N3 (~364 frames). Details
and exact specs in director.md.

## 6. Open questions for the editor (check, don't guess)
1. **Part backsides**: render Fender Inner, Front Bumper Duct, Wing Only, Exhaust cover from their inner side (silver, alone).
   Only if the inner face is real scanned surface (not see-through shell) use the optional tilt in N1/N2; else translate only.
2. **Holes**: after N1/N2 --check, look at the last frame of each part move for black voids where the part was. If a void
   reads as the subject, shorten that part's offset (half it) - don't add geometry.
3. Front Bumper Duct sits at 7.2 mm median: check its seat in N3 at the lock; the clean-car swap on 31.962 hides it after.
4. Rear plate in N2 at ~3.9 m: check it is not legible; deplate (infiniti-g35 tools/deplate.py) if it is.
5. Side Vents is one mesh with both vents: split by x sign (x>0 = right, x<0 = left) so each can move outward.

## v3 addendum (parent session, user feedback: cropping / redundancy / bumper-removed / openings) - 2026-11-11
Section coverage - each section appears in ONE continuous run:
| shot | section | subject |
|---|---|---|
| N0_open | whole (front-right side) | whole car, fully in frame (9.8 -> 9.2 m orbit) |
| s3_grille | front | grille fins + badge |
| s4_wheel | front / RF wheel | RF wheel + fender vent |
| s5_hood | front / engine bay | hood opens (registered open-state scan) -> under-hood capture |
| N1_front | front / RF corner | bumper corner, vents, fender, hood lift - one per hit |
| N2_rear | rear | roof spoiler, exhaust trims |
| N3_reassemble | whole (front-left, unseen side) | parts home, hood shuts, clean car, fade |
- Bumper-removed hero beat (C): not applicable - no bumper/front-end-removed state scan exists for this car. No labels.
- Openings (D): hood only (real scan). No trunk, no doors.
- Cropping (A): first/mid/last of every re-rendered shot checked at 30 % (media check/v4f.jpg); s3/s4 are detail shots that
  fill the frame by design.

## v4 - how it was made (scene-director, 2026-11-13)

User: "redo this with the new knowledge you have from doing the frontier and sentra videos ... include articles of the QX80
online, Ecky's project files and folder ... WhatsApp export". The reel changes from a scan showcase to a build story
(Sentra SEMA v3 / Frontier v8 pattern). Inputs: lessons.md (all, incl. 2026-11-13 entries), style-guide, workflow, Sentra
clips/project/editlog/feedback (branch claude/upbeat-goldberg-gy0s84), Frontier feedback/editlog, WhatsApp `_chat.txt`,
wa_sheet_0..4, every photo named below opened whole-frame (grids in the scratchpad), press/*_headline.png, check/kit_fit_1.jpg.

### User taste carried over (Sentra / Frontier feedback, binding)
- Hook: real article screenshots, **cropped headlines stacking** one per hit (not full-page flashes, not text cards).
- **Section labels** on every section ("CONCEPTS" over the iterations; print / fabrication labelled too).
- Concepts -> **3D panels going on the scan -> paint in colour** (Sentra "livery being applied in colour").
- **Static photos: whole photo, no zoom/pan** (blurred fill of itself behind, label in the band ABOVE the photo, never on it).
- Finished car only in the hook and after fabrication (Sentra: SEMA shots before the scan "felt out of place").
- End: Illumaesthetic logo ~720 px + "Customize everything". **No triangle counts on screen** (lessons 2026-11-13, twice).
- "How we modified this car", not "what we scanned" (Frontier v8): scan showcase shots only where they serve the build.

### 1. Inventory (what the data really holds for this story)
| Source | What it shows (looked at) | Use |
|---|---|---|
| WA 13/16/45/46/47/48 (Apr 30-May 1 2025) | stock grey QX80 in the shop, glass taped (blue X), scan spray on grille/lamps = scan prep. 46 = cleanest (front-left 3/4, doors shut, 2048x1536). 13/47 doors open; 16/45/48 rear with clutter | **46** |
| WA 62, 67 | 62 a different black QX80 (reference), 67 a G-sedan studio shot | reject (wrong car) |
| car4 scan + renders/final/N0_open | whole stock car, front-right orbit, whole car in frame (v3 check) | reuse |
| WA concept renders 109-870 (May 14-Aug 14) | grey studio renders bronze wheels (May) -> dark-floor grey (May 30-Jul 23) -> first purple 594/595 (Jul 24) -> 610-612 (Jul 28, viewer UI dots top-right) -> purple finals 845/869-872 (Aug 14). Tan/blue viewport pairs = design-on-scan screenshots | flipbook (front-left 3/4 renders only, one angle so it reads as evolution) |
| k_*.blend (16 kit groups on the scan, Ecky's own scan matrix, 1.6 mm) | front bumper, lower grille, front lip, brake ducts, NACA (hood), 4 flares, 2 skirts, 2 vents (motoiq logo), diffuser, exhaust, wing | panels-on scene |
| WA 1129 (Aug 28) | trans adapter plate (green) seated on the purple engine scan, flywheel visible, no annotations | **ENGINEERED** |
| WA 1295 / 1314 / 1317 / 1319 | plate CAD (1295 clean), 1314/1317/1319 have red marker circles/arrows | reject (annotations) except 1295 as fallback |
| WA 1388 (Sep 8, 2160x3840) | 3D-printed exhaust shroud with tips, on the bench | **3D PRINTED** |
| WA 1356 | printed brake duct + hose in a gloved hand ("It fit so no need to reprint") | fallback for 1388 |
| WA 1402 (Sep 8, 3840x5120) | wing test-fitted on the grey car (rear 3/4), clear | **TEST FIT** |
| WA 1423 / 1424 (Sep 8) | grey car on the lift, wheels off, rear kit on (1423); front with lip on (1424) | **TEST FIT** |
| WA 1541-1544 | printed vent badge mock-ups lying on store receipts / invoices | **reject** (clutter + private paperwork) |
| WA 1629 (=1626 hi-res, Oct 10) | installed motoiq vent on the wrapped fender, clean | finale detail |
| WA 1683-1694 (Oct 17) | finished wrapped car in the shop; pairs 1683=1689, 1684=1690, 1686=1692, 1687=1693, 1688=1694 (use the 4032/5120 copies). 1690 rear (wing + tips) best; 1692 cluttered by lift post | **1690** |
| WA 1699-1702 (Oct 24) | studio warehouse shoot; 1699=1701 (rear-left 3/4), 1700=1702 (front-left 3/4). 4032x3024 copies | **1701** hook, **1702** reveal |
| press/carscoops_teaser (Oct 21), carscoops (Oct 27), motorillustrated (Oct 27) | real headline screenshots | hook |
| Ecky Drive `Render/` (19) + `Presentation Render/` (14 png) | not downloaded, not looked at | open question 1 |

Not earning a place in v4: **s5_hood** (hood open on the stock engine bay - true data, but the build story is the kit + VR38
swap; showing the stock bay invites "is that the GT-R engine?" - it is not), **s3_grille, s4_wheel** (stock-car showcase
details, same section as N0, no build information), N1/N2/N3 (explode of stock part scans - "what we scanned").

### 2. Scene list (video t = music t - 0.66; beat k at video 0.102 + 0.65k; phrases every 8 beats)
| # | video t (music t) | beats | sources (exact) | label (band above photo / on scan) | why / camera |
|---|---|---|---|---|---|
| A | 0 - 5.302 (0.66 - 5.962) | 8 | photo **1701** whole, top of frame on its own blurred fill; headlines stack below, one per 2 beats: **carscoops_teaser** @1.402, **motorillustrated** @2.702, **carscoops** @4.002 (chronological: Oct 21, Oct 27, Oct 27). Crop each to outlet masthead + headline only (no hero image, no byline) | none (the headlines are the text) | Sentra opening rule. Rear 3/4 shows wing + exhaust = the build's signature. Headlines never overlap the photo |
| B1 | 5.302 - 6.602 (5.962 - 7.262) | 2 | photo **46** whole, static | **STOCK QX80** / sub `before` | the starting point; first stock image right after the finished one |
| B2 | 6.602 - 10.502 (7.262 - 11.162) | 6 | **N0_open** reuse as rendered (front-right orbit) | **3D SCAN** / sub `the stock car, scanned in-house` (no triangle count) | hard cut on the beat. Optional upgrade: solve 46's camera and start N0 from it (front-left) for a 1:1 photo->scan cut - new render, only if time allows |
| C | 10.502 - 15.702 (11.162 - 16.362) | 8 | flipbook, 16 frames x half beat (alternate 10/9 frames), whole renders on black fill, in this order: **109, 135, 166, 216, 241, 249, 257, 326, 360, 375, 395, 520, 543, 584, 595, 870** | **CONCEPTS** / sub `design iterations, May - Aug 2025` (dates from the WA timestamps) | grey bronze-wheel -> dark-floor grey -> purple; all one front-left 3/4 angle so the car stays put and the kit morphs. 612 left out (viewer UI dots in the corner), 845 = same as 870 |
| D | 15.702 - 20.902 (16.362 - 21.562) | 8 | NEW render: car4 silver + k_* groups landing one step per beat, satin white/grey kit on silver (kit_fit colours too busy) | **DESIGNED ON THE SCAN** / sub `body kit by Ecky` (or `front · flares · skirts · rear`) | camera front-right 3/4 -> right side -> rear-right 3/4 (continues N0's side; whole car in frame, ~9.5 m at 32 mm per lesson). Order below |
| E | 20.902 - 26.102 (21.562 - 26.762) | 8 | NEW render, **same camera move continued** (no cut at 21.562 if D+E is one shot; else hard cut on the lift): kitted car, wing lands ON the lift (21.562), then colour-shift wrap wipes rear -> front, camera rear-right 3/4 -> rear -> rear-left 3/4 | **MIDNIGHT PURPLE** / sub `colour-shift wrap` | the biggest musical moment (the lift) = the colour reveal, the user's "paint in colour" beat. Match the hue shift (purple -> blue -> bronze-red with angle) to 1701/1702/1629 - check a side-by-side before finals (Sentra livery was rejected as "applied wrong") |
| F1 | 26.102 - 27.402 (26.762 - 28.062) | 2 | photo **1129** | **ENGINEERED** / sub `trans adapter plate, on our engine scans` | engineering section; one image only (no flipbook of annotated screenshots) |
| F2 | 27.402 - 28.702 (28.062 - 29.362) | 2 | photo **1388** | **3D PRINTED** / sub `exhaust shroud` | print labelled (Sentra note) |
| F3 | 28.702 - 30.002 (29.362 - 30.662) | 2 | photo **1402** | **TEST FIT** / sub `wing` | |
| F4 | 30.002 - 30.652 (30.662 - 31.312) | 1 | photo **1423** | TEST FIT (label stays, sub `rear kit`) | |
| F5 | 30.652 - 31.302 (31.312 - 31.962) | 1 | photo **1424** | TEST FIT (sub `front lip`) | quickens into the accent |
| G1 | 31.302 - 33.902 (31.962 - 34.562) | 4 | photo **1702** | **FINISHED** / sub `QX80 R-Spec · SEMA 2025` | strongest accent = the reveal, front 3/4 studio (hook was the rear 3/4 of the same shoot, different photo) |
| G2 | 33.902 - 35.202 (34.562 - 35.862) | 2 | photo **1629** | (FINISHED stays) | travel front -> side: the printed motoiq vent installed |
| G3 | 35.202 - 36.502 (35.862 - 37.162) | 2 | photo **1690** | (FINISHED stays) | travel -> rear: wing + exhaust on the real car |
| H | 36.502 - 38.84 (37.162 - 39.5) | ~3.5 | logo card ~720 px + **Customize everything** | - | track fades from 37.162 |

All photos: static, whole frame, blurred-fill background, no Ken Burns. Labels only in the band / on scan renders.
Portrait photos (1388, 1402) fill the width; the band sits above them.

### 3. Kit landing order in D (one step per beat; travel front -> side -> rear, no ping-pong; bumper-nested parts after the bumper)
| beat | video t | group(s) | camera sees |
|---|---|---|---|
| 0 | 15.702 | k_front_bumper + k_lower_grille (grille sits in the bumper; arrives as one assembly) | front-right 3/4 |
| 1 | 16.352 | k_front_lip + k_brake_ducts (both mount on the bumper -> after it) | front |
| 2 | 17.002 | k_naca (hood duct) | front / hood |
| 3 | 17.652 | k_flare_fr + k_flare_fl | front arches |
| 4 | 18.302 | k_vent_r + k_vent_l (motoiq vents on the front fenders) | right side |
| 5 | 18.952 | k_skirt_r + k_skirt_l | right side |
| 6 | 19.602 | k_flare_rr + k_flare_rl | rear arches |
| 7 | 20.252 | k_diffuser + k_exhaust | rear-right 3/4 |
| 8 | 20.902 (= E start, the lift) | k_wing | rear 3/4, then the wrap wipe |
Each part arrives along its mounting direction (out past the silhouette, then in), no path through the body (clipcheck /
pathcheck lessons). The kit front bumper sits over the stock bumper: check for stock skin poking through the kit (Frontier
"new part over old" lesson) - cut the stock bumper under the kit bumper's own silhouette if it does.

### 4. Reuse vs render
Reuse: N0_open (as-is). New renders: D+E (one continuous ~10.4 s move, or two shots cut on 21.562). Optional: N0 from photo
46's solved camera for a 1:1 cut. Everything else is stills + press + logo card (build like Sentra tools/build.py, exact frames).

### 5. Flags - things that could read as made-up
1. **Triangle count** in the draft's 3D SCAN label: removed (user rule 2026-11-13).
2. **"VR38" / "GT-R engine" on the 1129 still**: the chat is contradictory about which scan the purple engine is ("Purple
   engine is QX80" vs "If this lines up, that purple engine is the GTR engine", Aug 28). Label says only "trans adapter
   plate, on our engine scans". Don't write 1,000 hp anywhere ourselves - it appears only inside the press screenshots.
3. **"MIDNIGHT PURPLE"**: supported by the chat colour options (Midnight Purple listed), Ron "Midnight purple 3?!" and
   Adam "It's wrapped" (Oct 17), and The Drive's URL. If the editor wants zero risk: `COLOUR-SHIFT WRAP` alone.
4. **"body kit by Ecky"**: Ecky's name on screen is a credit - confirm the user wants designer names shown (Sentra credited
   the client, not staff). Neutral alternative given.
5. The 3D wrap is an approximation of a colour-shift film; it must match the photos or be cut (Sentra livery lesson).
6. "16 kit parts" or any part count: don't. The 16 groups are our grouping; the print folder has many more files.

### 6. Open questions for the editor
1. Ecky's `Render/` and `Presentation Render/` PNGs were not looked at. If they are full-res versions of the purple finals
   (870 etc.) at the same angle, swap them into the flipbook's last 2-3 frames; don't add new angles.
2. Is the user OK with a D+E continuous move of ~120 + 90 deg in 10 s? If it reads fast at preview, drop the rear-left leg of E.
3. The brake adapters (Illumaesthetic-designed) have no clean photo in the export (CAD screenshots only, annotated) - left out;
   ask whether to add a label-only beat.
