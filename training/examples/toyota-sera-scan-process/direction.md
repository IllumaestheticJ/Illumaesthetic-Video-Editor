# Toyota Sera scan-process reel - v3 direction (scene director + director stage 2)

Date 2026-11-11. Sources read: clips.md, project.yaml, project_v1.yaml, editlog.jsonl, feedback.jsonl, review.md,
director_report.md, tools/shots.sh, knowledge/lessons.md. Renders looked at (contact sheets of every
`renders/final/*` folder + full-size frames s5_front #9, s3_rear #30) and the three IRL clips (irl/*.mp4 at 4 fps).
Coordinates: scan frame, metres, z up, car forward f = (0.258, 0.966), car right r = (0.966, -0.258).
"car (a fwd, b right)" means xy = a*f + b*r; the scan-frame xy is written next to it.

Newest user feedback (A-D, 2026-11-11) applied throughout: subject-framed crops with margins, one continuous
sequence per car section, bumper-removed data is the hero beat with short factual labels, no state without its scan.

## 1. Feature inventory

| region | scans (registered, same Artec frame) | what is actually visible | IRL | richness |
|---|---|---|---|---|
| **Front** | full car (14,999,999); front bumper part (1,800,000, inside verified: ribs, tabs, plate recess); 'Hood open' (5,000,000: bumper off + hood up); 'front bumper removed' (1,999,999, hood closed); 'Hood Open, Bumper in' (1,500,000) | behind the bumper (s5 frame 9, 'Hood open'): radiator fan + shroud, radiator/condenser core, upper core-support bar, a full-width **lower beam across the nose (crash beam)** with its end brackets, headlight mounts, engine | 4342 front 3/4 (1:1 open); 4351 crew lifting the front bumper off (1:1 into 'Hood open') | **richest**: 1 part + 3 states + 2 IRL beats with 1:1 |
| Side | 'Door Open' (10,500,000, both butterfly doors up, partial) | butterfly doors + glass canopy = the Sera's signature; doors physically opened (4305-4311 "doors up") | none | 1 state, signature feature |
| **Rear** | rear bumper part (4,999,998, inside verified); 'Rear Bumper Removed' (1,500,000; captured hatch open + tail lights out, = '... No Tail Lights' byte-identical); 'rear bumper removed 2'; 'spoiler removed' (1,000,000, **no spoiler part scan**) | behind the bumper (s3 frame 30, compB): rear tail panel, a full-width **lower rear beam (crash beam)**, bumper **mounting points/brackets** along the panel edge, latch area; tail-light openings are ragged scan holes (weak) | 4359 crew pulling the rear bumper corner loose (never fully off -> hard cut, no 1:1) | 1 part + 2 states + IRL pull |
| Top / engine bay | 'Hood open' bay | engine visible inside the front sequence; deep-bay holes | 4346 hood opening (not used) | covered by the front sequence only |
| Wheels | full car | tyres + wheels present in full car | - | no own scene (no wheel-off state) |

Weak data: deep engine-bay holes (Hood open), door scan partial, rear tail-light holes, rear wheel ghost at the listing
dissolve (known), plates (check at final res). Not used: 'spoiler removed' (no part scan to animate; showing a spoiler
leaving would be invented), 'front bumper removed' (hood closed - footage at the cut has the hood up), 'Hood Open, Bumper in'.

## 2. Scene order (travel front -> right side -> rear, one continuous sequence per section)

Opener is fixed by the scan-process structure (IRL 4342 front 3/4 -> 1:1 full car). The front is the richest region
and the travel starts there, so the whole front story (lift-off, 1:1 bay, bumper show-off, crash beam) is told
in one block; the doors (signature) bridge to the rear; the rear bumper block ends at the rear, where the x-ray
reassembly starts and orbits to the listing hero (rear-right 3/4: car fwd -3.0, right 5.2). v2 ping-ponged
front -> rear -> front; v3 does not.

| # | scene | section | scans used | feature shown | why here | beats |
|---|---|---|---|---|---|---|
| 1 | IRL open (4342) | front | - | real car, front 3/4 | hook; 1:1 on phrase 1 | 3 |
| 2 | 1:1 full car | front | full | nose/hood = the real car | the transformation, on the 1.8 s phrase change | 3 |
| 3 | IRL front lift (4351) | front | - | crew lifting stock bumper off | real removal of a part we have scanned in both states | 4 |
| 4 | 1:1 bay | front | compA (Hood open) | bay exactly as in the footage | 1:1 into the matching state | 2 |
| 5 | front bumper removed (NEW) | front | compA + fbump | bumper inner face, then crash beam + radiator/fan behind it | hero beat C for the richest region, same section continues | 7 |
| 6 | butterfly doors (NEW) | side | door-open base + both door panels on fitted hinges | the signature doors swinging up | the travel from front to rear; lands on phrase 2 (11.4 s) | 4 |
| 7 | IRL rear pull (4359) | rear | - | crew pulling the bumper corner | real removal at the rear | 3 |
| 8 | rear bumper removed (NEW) | rear | compB (Rear Bumper Removed) + rbump | bumper inner face, then rear crash beam + mounting points | hero beat C at the rear | 7 |
| 9 | x-ray reassembly (RE-RENDER) | whole car | xbase + fbump + rbump | both bumpers seat home, orbit to listing hero | closing rung; rear bumper seats ON phrase 3 (21.0 s) | 7 (incl. dissolve) |
| 10 | listing WebZoom | end card | - | page, title, logo, URL | strong final cut into the listing (dissolve) | 6 (incl. dissolve) |

## 3. Music map (100 BPM, beat 0.6 s, kick on every beat; phrase changes 1.8 / 11.4 / 21.0)
`beats: [0.0, 1.8, 3.6, 6.0, 7.2, 11.4, 13.8, 15.6, 19.8, 23.4, 27.0]` (23.4 = dissolve start, 24.0 dissolve end).
- 1.8 phrase change: 1:1 IRL -> full car.  - 6.0 kick: 1:1 IRL -> Hood open bay.
- 11.4 phrase change: front sequence ends, doors begin swinging (section change on the strongest mid accent).
- 21.0 phrase change: rear bumper seats home in the x-ray (last part home = the reel's "complete" moment).
- Length stays 27.0 s.

## 4. Shot plan (per-shot focus table)

Silver = satin silver on black, `--res-pct 75 --samples 12 --fps 15`, persistent data OFF, render dur*15 + 3 frames
(lessons: minterpolate tail). APS-C sensor 23.3 mm as in shots.sh. Every scan shot is checked first/middle/last frame
for clipping (feedback A).

| id | start-end | section / focus | camera | part action (times are reel seconds) | earns its seconds | render |
|---|---|---|---|---|---|---|
| irl_open | 0.0-1.8 | front / the real car | 4342 crop zoom 1.0 (v2) | - | hook | reuse `irl/open.mp4` (dur 1.7667) |
| scan_open | 1.8-3.6 | front / nose = scan of that car | 1:1 cam_open, push 0.10 | - | the transformation | reuse `s1_open`, src_fps 18.4 (35/1.9) so the push fills 1.8 s without a tail freeze. Framing is fixed by the 1:1 (nose fills the frame = detail shot of the front; exception to A by construction) |
| irl_front_lift | 3.6-6.0 | front / bumper coming off | v2 crop | - | real removal | reuse `irl/front.mp4` (2.4 s, ends on solved frame 250) |
| scan_front_match | 6.0-7.2 | front / bay behind the bumper, 1:1 | cam_front, push 0.04 | - | the 1:1 | reuse `s5_front` as-is |
| **scan_front_off** | 7.2-11.4 | front / **front bumper inner face -> crash beam** | start car (4.6 fwd, 1.9 right) = (3.02, 3.95, 1.50) -> target car (1.75, 0.15) = (0.60, 1.65, 0.55), focal 32 (whole nose + bumper fill the width with ~10 % margin, hood-up top in frame). 7.2-9.0 slow push 10 %; 9.0-10.2 move in and down to car (2.7, 1.2) = (1.86, 2.30, 0.75), target car (1.35, 0.2) = (0.54, 1.25, 0.42) - low raking 3/4 along the crash beam, its right-hand bracket and the radiator/fan behind it filling the frame; 10.2-11.4 hold that pose, 2 % drift | fbump starts at its lifted position (8th field start offset (0.06, 0.24, 0.05) = 0.25 m ahead, as the crew had it). 7.2-7.8 drifts forward; 7.8-9.0 translates to (0.57, 0.99, -0.20) (1.1 m forward, 0.3 m toward camera, down) **into the black below the nose** and flips 150 deg about the car-width axis, top edge toward the lens, so the scanned inside faces the camera at 9.0; 9.0-9.6 inner face held; 9.6-10.2 continues to (1.38, 1.29, -0.45) and leaves frame bottom-right as the camera moves in. Never crosses the body. | the bumper's inner face + what was behind it = the front's richest data | NEW, scene compA, 66 frames |
| **scan_doors** | 11.4-13.8 | side / both butterfly doors | right side, door section filling the width: cam car (0.3, 3.4) = (3.36, -0.59, 1.40) -> car (-0.3, 3.4) = (3.21, -1.17, 1.40) (0.6 m dolly toward the rear = the travel), target (0.03, 0.10, 1.00) -> (-0.05, -0.19, 1.00), focal 24 (3.3 m wide: front arch to rear arch, sills to fully-open door tips in frame, ~8 % margin) | both doors swing up on hinges fitted to 'Door Open' 11.4 -> 13.2 (ease out, fully open on the 13.2 kick); 13.2-13.8 open, camera still dollying | the Sera's signature; one beat of held open doors so the open state reads | NEW, 39 frames |
| irl_rear_pull | 13.8-15.6 | rear / crew pulling the bumper corner | v2 crop | - | real removal | reuse `irl/rear.mp4` (hard cut out: no 1:1 possible) |
| **scan_rear_off** | 15.6-19.8 | rear / **rear bumper inner face -> rear crash beam + mounting points** | start car (-5.0, 2.0) = (0.64, -5.35, 1.35), target car (-1.6, 0.1) = (-0.32, -1.57, 0.60), focal 32 (whole tail incl. the open hatch and both rear corners in frame, ~10 % margin). 15.6-17.4 slow push 8 %; 18.0-18.6 move in and down to car (-3.1, 1.2) = (0.36, -3.30, 0.85), target car (-1.45, 0.2) = (-0.18, -1.45, 0.50): the crash beam and the bumper mounting points along the tail panel fill the frame, tail-light holes kept above the top edge; 18.6-19.8 hold, 2 % drift | rbump starts home. 15.6-16.2 pops back 0.15 m (-0.04, -0.14, 0.0) = continuity with the IRL pull; 16.2-17.4 translates to (0.08, -1.06, -0.25) (rearward, toward camera, down into black below the tail) and flips 150 deg about the car-width axis, inside to the lens at 17.4; 17.4-18.0 inner face held; 18.0-18.6 continues to (0.46, -1.78, -0.50) and leaves frame bottom-right as the camera moves in | inner face + exposed rear structure = the rear's data | NEW, scene compB (v2's Rear Bumper Removed composite), 66 frames |
| **scan_xray** | 19.8-24.0 (dissolve 23.4-24.0) | whole car / reassembly | start `match/cam_xray_start.json` (rear-right, continues from scene 8), orbit to `match/cam_listing.json` about (0, 0, 0.7), ease in-out, lands exactly at 23.4; morph to clay 22.8-23.4 (same clay 0.05 + listing bg as v2) | translate only, both start moving at frame 0: fbump home at 20.4, rbump home at 21.0 (phrase change). Explode windows r0.0:0.143 and r0.0:0.286 of the 4.2 s move | whole-car payoff + lands the listing angle | RE-RENDER (x-ray ~3 s/frame): 4.2 s move + 0.6 s static listing pose for the dissolve = 72+3 frames |
| website | 23.4-27.0 | end card | WebZoom from 1.35x on the hero | re-time: zoom out 23.4-25.2, title 24.3, logo 24.9, URL fully in by 25.5, readable hold 1.5 s, music fade 26.2-27.0 | ends the reel without dead frames | re-render WebZoom at 3.6 s (cheap); fallback: v1 webzoom first 3.6 s at 1.5x speed |

### Labels (static ScanHUD labels only, over scan, never on IRL; numbers only from STL headers)
| time | label | where |
|---|---|---|
| 7.2-8.4 | FRONT BUMPER REMOVED | top black area |
| 8.4-9.6 | FRONT BUMPER / INSIDE + OUTSIDE / 1,800,000 TRIANGLES | next to the flipped bumper |
| 9.6-11.4 | CRASH BEAM | on the beam |
| 10.2-11.4 | RADIATOR + FAN | above, on the fan |
| 11.6-13.8 | BUTTERFLY DOORS | top black |
| 16.2-17.4 | REAR BUMPER REMOVED | top black |
| 17.4-18.0 | REAR BUMPER / INSIDE + OUTSIDE / 4,999,998 TRIANGLES | next to bumper |
| 18.6-19.8 | CRASH BEAM; MOUNTING POINTS | on beam / on bracket row |
| 21.0-22.8 | FULL CAR SCAN / 14,999,999 TRIANGLES | x-ray, black area |
Confirm at final res that the front/rear lower beams read as beams (name what is visible; if not, use "BUMPER MOUNTS").
HUD overlay must be re-rendered for the new times (hud_sera_v1.mov timings no longer apply).

## 5. Section coverage (feedback B: one continuous sequence per section)
front 0.0-11.4 (irl_open, scan_open, irl_front_lift, scan_front_match, scan_front_off) | side 11.4-13.8 (scan_doors) |
rear 13.8-19.8 (irl_rear_pull, scan_rear_off) | whole car 19.8-24.0 (scan_xray) | end card 23.4-27.0.
Engine bay appears only inside the front sequence. No section returns later.

## 6. Cut list (removed from v2)
- `s3_rear` (rear explode, 6.0-9.0 in v2): too wide (car ~1/3 of frame width), Z-spin about vertical (lessons: tip about the width axis), cut away before showing what was behind the bumper; also placed before the front = ping-pong.
- `s6_frontx` (front explode wide, 12.6-15.6): too wide, bumper rose ABOVE the car across the open hood (not clear background), Z-spin, never moved in on the bay.
- `s7_xray` as rendered: last 0.6 s frozen + 5.4 s slot; parts landed off the phrase; replaced by the re-timed re-render.
- Website 2.3 s of dead frames (director report) and 3.0 s of total length: card goes 6.6 -> 3.6 s.
- v2 order rear-before-front (front -> rear -> front -> whole) - replaced by front -> side -> rear -> whole.

## 7. Hold list (> 0.75 s with little part motion)
- scan_front_match 6.0-7.2 (1.2 s): the 1:1 must read as the same car/state; tiny push.
- scan_front_off 10.2-11.4 (1.2 s): readable hold on crash beam + radiator/fan with labels (feedback C), 2 % drift.
- scan_doors 13.2-13.8 (0.6): open doors read; below threshold.
- scan_rear_off 18.6-19.8 (1.2 s): readable hold on rear crash beam + mounting points with labels (C).
- scan_xray 23.4-24.0 (0.6 static): needed for the position-locked dissolve to the listing.
- website 25.5-27.0 (1.5 s): URL must be readable.

## 8. Reuse vs render, budget
Reused unchanged: irl/open.mp4, irl/front.mp4, irl/rear.mp4, s5_front; s1_open retimed (src_fps 18.4).
New silver: scan_front_off 66 + scan_doors 39 + scan_rear_off 66 = **171 frames** (~22 s/frame = ~63 min, serial).
X-ray re-render 75 frames (~4 min). WebZoom + HUD re-render (Remotion, cheap). Preview every new shot at 20 % first
and check first/middle/last frames for clipping and the bumper path (must stay over black, never across the body).

## 9. Open questions / blockers for the editor
1. **Doors need hinges in THIS project's frame.** The sibling reel's door panels/hinges (/home/user/media/toyota-sera/clean)
   are not on disk. Refit with projects/toyota-sera/tools/hinge_fit.py on work/sera/door_3mm.stl vs full (keep `--like`
   on any re-prep), and confirm registration red-over-silver (feedback D). If the fit is > 3 mm median or the
   right-hand door's capture is ragged in the preview, drop the door motion and render the same camera on the
   closed full car (canopy/side profile still new) in the same 11.4-13.8 slot, and change the label from
   "BUTTERFLY DOORS" to "GLASS CANOPY".
2. IRL 4359 looks like the car's rear-LEFT corner; the scan rear shot is rear-right (to continue the right-side travel
   and reach the listing). It is a hard cut, not 1:1, so this is accepted; flip to rear-left only if the reviewer objects.
3. Front 1:1 is now on a kick (6.0), not a phrase change; the phrase changes carry the open 1:1, the front->side
   section change and the reassembly. Shifting the music would break the 1.8 s open cut.
4. Plates: check the front/rear close-ups at final res (bumper parts carry the plate recess; plates aren't in the part scans).
