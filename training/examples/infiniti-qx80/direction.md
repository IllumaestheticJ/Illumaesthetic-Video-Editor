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
