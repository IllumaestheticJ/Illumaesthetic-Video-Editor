# Honda Civic FE1 - Epsilon kit reel v5 - director's plan (complete reshoot)

Written 2026-11-12 by the director agent. Nothing rendered, no other file edited. Inputs read: lessons.md, style-guide,
references README, feedback.jsonl, project.yaml (v4), editlog, direction.md "## v4 (Epsilon)", review.md, `ive director`
on v4 (report kept out of the project), my own 3-frames-per-shot sheets of civic_fe1_epsilon_v4.mp4, Ron's 7 renders at
full size, checks/fit5.png + fit5c.png (new kit placement).

User on v4: "all the parts are placed on incorrectly/inaccurately, and the cutting/organizaiton is a mess - please have a
separate agent plan out the shots and then reshoot everything". Standing: no Illumaesthetic logo, paced faster, Epsilon
video (open up, then install front lip, side skirts, rear apron, new wheels, rear wing; end on one of Ron's renders),
doors/trunk only open on hinges, never reuse a shot.

## 1. Why v4 reads as a mess (frames I looked at; f = frame of the delivered 833-frame file)
1. **14 shots / 13 cuts in 27.8 s and the camera teleports on every cut.** Order of viewpoints: front-left wide (f1-37) ->
   front-right close (f38-99) -> straight rear (f100-236) -> high front-right (f237-298) -> front-left macro (f299-335) ->
   low front (f336-391) -> left wheel macro (f392-434) -> left wide (f435-497) -> front-left looking back (f498-571) ->
   rear-left low (f572-633) -> rear-right high (f634-695) -> front-right low (f696-). Side, height and scale all change at once;
   no two neighbouring shots share a screen direction.
2. **Subject size pumps between ~10 % and ~60 % of the frame.** Measured silhouette area at each shot's mid frame: N1 9 %,
   N2 20, N3 28, N3b 63, N4 19, s4 58, I1 18, s3 47, I2 14, I3 16, I4 15, I5 29, W 11, R 13. Macro / tiny / macro / tiny.
3. **Stock cutaways interrupt the build.** s4_lamp (f299-335) and s3_wheel (f392-434) are stock macros from an older render
   set dropped between installs. They are the only dense frames in the back half, so the eye reads them as the subject and the
   installs (small, far) as filler; and they re-show the front and the wheel as separate shots (rule B).
4. **The opening section is four shots for two actions** (N2 doors, N3 lid, N3b interior, N4 close = 8.7 s). N3 -> N3b is the
   same camera cut into itself (`ive director`: IoU 1.0, corr 1.0), and the first kit part does not arrive until 11.2 s.
5. **Opened on the right, built on the left.** Doors open toward a front-right camera (f38-99) as flat slabs that hide the
   openings (plus the scan hole in the right rear door); then the installs live on the car's left (f435-633), the wing is shot
   from the right (f634-695), the hero from the front-right. The viewer never learns where they are standing.
6. **Parts never accumulate in one view.** Each install is its own 2 s shot from a new place: lip (front), wheels (wide left),
   skirt (looking back), apron (rear-left), wing (rear-right). The part appears, seats, cut. Nothing is held on, moved in on or
   turned (rule 1), and no frame before the last 1.2 s shows two fitted parts as the subject.
7. **Cropping (rule A).** 12 of 14 mid frames touch a frame edge, 7 of them by accident: N4 nose out of frame right while the car
   closes (f238-297); I1 right mirror/fender cut at f390; I2 nose cut left; I3 half the frame black, car cut left (f499-570);
   I4 cut left; I5 cut right; W_kit nose on the right edge. The wides sit in the upper-middle third (y 30-60 %) with 40 %
   dead black below.
8. **The hand-over is small and dead.** W_kit (1.2 s) + R_ron (3.3 s) = 4.5 s where the car is 19-21 % of frame height and
   nothing moves (`ive director`: 1.2 s + 2.7 s dead). The right-rear-door scan hole sits in the middle of the match frame.

Rejected guess: "installs must not be on a closed car". The closing itself is not what reads badly; a separate closing
shot from a fourth viewpoint is. v5 keeps closed-car installs (reasons in 2c) but closes inside the opening shot.

## 2. Decisions (one each)
**a. Three clips, two cuts.** S1 open-up (one held top view) -> L, ONE continuous 15.9 s take that laps the car while the
five parts go on in travel order -> Ron's render. v4 had 13 cuts.

**b. The camera lives on the car's LEFT** (lap: front -> left side -> rear -> rear-left 3/4). Reasons, all visible in
checks/fit5.png: the left flank is clean; the right flank has the scan hole in the rear door and the right-rear scanned
wheel is a tyre ring; both scanned left wheels are complete, so the wheel swap shows a real wheel leaving. The right side
is seen only in S1 from above (doors), where the door hole is foreshortened and the wheel is under the arch.

**c. Open-up first, in one shot, and the car is shut again before the first part.** S1 is a rolled near-top view (car
vertical in the 9:16 frame): doors swing out on the drop, the trunk lid stands up, 1.24 s to read the real open-state data
(sills/jambs, trunk interior from above), everything shuts, cut on the slam. Car CLOSED for every install because:
(1) the wing seats on the lid's top face - on a lid standing at 94 deg it has nowhere to land; (2) in 9:16 a front or rear
detail frame is ~4 m tall at the car, so open right doors and the raised lid poke into the lip/skirt/apron frames as clipped
slabs (and any rearward view of the doors shows their unscanned inner faces); (3) the lap ends in a 1:1 cut to a closed
render; (4) car_nowheels and every kit part are built on the closed car. Why a top view for the opening: it is the only
camera that sees both doors EDGE-ON (no outer slab, no inner face), looks INTO the openings and the trunk, and fills the
tall frame with the whole car.

**d. Install order = the user's list, unchanged:** front lip, side skirts, rear apron, new wheels, rear wing. It is also the
travel order of the lap (front, side, rear low, rear 3/4 wide, rear high), so nothing has to be reordered.

**e. Hand-over: hard 1:1 cut on the B7a downbeat (33.161) to Ron's render 7 (rear-left 3/4, low).** Why 7 instead of 1:
the last part (wing) goes on at the rear-left, so the take can settle straight into the render camera instead of running
190 deg back to the front-right past the damaged right flank; render 7 shows four of the five parts (wing, apron, skirt, gold
wheels) and the wing large; its car bbox is 1180x459 px (2.6:1) against render 1's 1402x504 (2.8:1), so at the same 87 % width the car is ~8 % taller
in the 9:16 window. Needs a new solve (match_render.py, same method as render 1). See section 7 for the fallback.

**f. Length 24.93 s (748 frames), audio in at 12.026 as v4, picture and music fade over 0.5 s from the B8a hit (36.471).**
v4 was 27.77 s; the user said "paced too slowly", and with no closing shot, no cutaways and no W_kit hold the story is done
one bar earlier. New scan footage 21.14 s.

## 3. Shot table
Scan frame: front +Y, car's left -X, floor z~0, nose y 2.41, tail y -2.25, wheel centres y 1.43 / -1.31, half-width 0.95,
roof z 1.6. `az` as in shots_v4.cam(): 0 = in front, +90 = car's left, 180 = behind. Lens = focal on the 20.25 mm-wide
portrait sensor used so far (frame width at distance d = d * 20.25 / focal). Video frame = round((track - 12.026) * 30).
All camera numbers are starting values: tune them on the 30 % preview until the first/mid/last sheet passes section 6.

| section | id | track in-out / video in-out (frames) | focus | camera | part actions (shot-local s -> hit) | why it earns its seconds |
|---|---|---|---|---|---|---|
| TOP | **S1_open** | 12.026-17.216 / 0.00-5.19 (f0-155, 156 fr) | whole car opening: right doors, trunk lid | Near-top view leaning to the car's right, ROLLED so the nose points up the frame. Direction target->camera = (0.343, -0.152, 0.927): elevation 68 deg, bearing 24 deg behind the pure right side (= edge-on to both open doors, 68/64 deg). f35. K0 t0: target (0.45, 0.05, 0.6), d 7.3, roll +8 deg off. K1 t1.27 (drop): d 6.4, roll 0, ease out - car = ~72 % of frame height, nose and tail >= 120 px inside, room on frame-right for the doors. K2 t3.33: d 6.3 (lin creep). K3 t4.57: target (0.55, -0.55, 0.5), d 5.7 - drifts toward the trunk and the sills (tail may sit ~60 px from the bottom, nose stays in). K4 t5.19: target (0.2, 0.9, 0.5), d 5.7, ease in - starts moving toward the nose, cut mid-move | Base = doors_base + trunk_base composite as v3 N4. Front-right door 0 -> 68 deg from t1.27 (DROP 13.295), open ON B1b 13.916. Rear-right door 0 -> 64 deg t1.89 -> open ON B1c 14.542. Lid opens on its fitted hinge t2.52 -> open ON B1d 15.358. Hold open t3.33-4.57. All three shut t4.57 (B2a 16.600) -> t5.16, rear door 2 frames ahead, fully shut on the last frame; cut ON B2b 17.216 | The only wide of the stock car, the hook (first motion on the drop at 1.27 s) and the whole open-up in one held view. Replaces N1+N2+N3+N3b+N4 (9.9 s) with 5.2 s; only real open-state data is looked at |
| FRONT | **L_build** leg 1 | 17.216-19.27 / 5.19-7.25 (f156-217) | front lip | Low front, slightly left. K0 t0: az +10, d 4.3, h 0.50, target (0, 2.25, 0.45), f35. K1 t0.635: az +12, d 3.8, h 0.45, target (0, 2.25, 0.42), ease out - bumper width ~83 % of frame width, lip on the lower-middle third, roof in. K2 t1.459: d 3.65 (lin creep). K3 t2.05: loc (-1.9, 3.3, 0.30), target (-0.75, 2.25, 0.22) - the lip's left end and its wrap round the corner fill the width (frame ~0.9 m wide) | Lip pops into black at (0, +0.50, -0.12) at t0, already moving on the cut frame; SEATED t0.635 ON B2c 17.851 (ease out). Hold t0.635-1.459 (to B2d 18.675). Then the camera, not the part, moves: low slide in on the lip's left end | First part, 0.6 s after the cut. Whole lip seating, then moved in on (its end cap = new information), per "hold, move in, show it off" |
| LEFT SIDE | L_build leg 2 | 19.27-22.2 / 7.25-10.2 (f217-305) | left side skirt | K4 t2.707: loc (-2.1, 3.0, 0.32), target (-0.98, 0.0, 0.30), f35, ease inout - grazing view back along the sill: front-left wheel large at frame-left, sill running into depth, clear black on the right half for the skirt. K5 t3.943: loc (-2.1, 2.7, 0.34), target (-0.98, -0.3, 0.30) (lin glide 0.3 m rearward). K6 t5.0: loc (-2.3, -2.6, 0.45), target (-0.8, -1.6, 0.40) - travels low along the whole skirt to its rear end and the rear-left corner | skirt_L pops into black 0.40 m outboard (-X), 0.06 low at t2.09 (out of the leg-1 frame; verify), SEATED t2.707 ON B3a 19.923 (downbeat). skirt_R mirrored, unseen. Glide hold t2.707-3.943 (to B3c 21.159) | The skirt only reads from a low grazing view; the travel to the rear runs along its full length, so the move that connects front to rear IS the show-off. Front wheel still stock here = the "before" for the wheels, without a cutaway |
| REAR | L_build leg 3 | 22.2-25.10 / 10.2-13.07 (f305-392) | rear apron | K7 t6.011: az 168 (12 deg left of straight behind), d 3.7, h 0.45, target (0, -2.15, 0.45), f35, ease out - rear bumper ~83 % of frame width, apron + exhaust cut-outs in the lower-middle third, lid edge and roof in. K8 t6.632: d 3.5 (lin creep) | rear_apron pops into black at (0, -0.50, -0.12) at t5.39, SEATED t6.011 ON B4a 23.227 (downbeat). Hold t6.011-6.632 (to B4b 23.848) | Third part in the third section; the camera lands and the part seats on the same downbeat |
| WHEELS (inside the rear run) | L_build leg 4 | 25.10-28.61 / 13.07-16.59 (f392-498) | wheel swap, then the rear-left gold wheel | K9 t7.884: rise and pull back to the rear-left 3/4 wide: az 140, elevation 35 deg, d 9.6, target (-0.25, -0.1, 0.6) -> loc ~(-5.3, -6.1, 6.1), f35, ease inout - whole car ~80 % of frame width, ~45 % of height, 0.8 m free on frame-left for the wheels. K10 t9.305: d 9.2 (lin). K11 t9.955: same line, d 9.0. K12 t10.567: loc (-2.0, -2.4, 0.70), target (-0.93, -1.31, 0.36) - fast push to the rear-left wheel, wheel + brake ~75 % of frame width, skirt tail and apron corner at the edges. K13 t11.396: 5 deg arc toward the tail, same distance (lin) | scanwheel_FL/FR/RL/RR release ON B4d 25.100 (t7.884), pull 0.9 m straight outboard in 0.5 s (ease in), then parked hidden. New rim/tyre/brake x4 pop in 0.9 m outboard at t8.69, SEATED t9.305 ON B5a 26.521 (downbeat). Hold t9.305-9.955 (to B5b). Push-in lands ON B5c 27.783; close hold to B5d 28.612 | The only place the whole car is the subject mid-build: lip, skirt and apron are all on and visible while the wheels change. Then the wheel gets its detail (gold rim + brake, never shown close in v4) |
| REAR (wing) | L_build leg 5 | 28.61-31.09 / 16.59-19.06 (f498-572) | rear wing | K14 t12.631: az 155, d 3.4, h 2.2, target (0, -1.95, 1.15), f35, ease inout - lid + wing fill the width, rear glass above, tail lamps at the bottom third, free black over the lid for the drop. K15 t13.238: d 3.3 (lin). K16 t13.872: loc (-1.9, -2.9, 1.35), target (-0.6, -2.0, 1.12) - left upright / endplate where it meets the lid | wing pops into black 0.65 m above its seat (0, -0.10, +0.65) at t12.0, drops, SEATED t12.631 ON B6a 29.847 (downbeat, ease out, no spin). Hold to B6b 30.454; slide to the upright lands ON B6c 31.088 | Last part, largest part: seated wide enough to read the whole wing, then moved in on where it meets the car |
| WHOLE (hero) | L_build leg 6 | 31.09-33.161 / 19.06-21.13 (f572-633) | finished car, rear-left 3/4 | K17 t15.55: pull back and down to the camera solved against Ron's render 7 (loc/target/focal/roll + shift from the solve, converted to the 9:16 window below), ease out, on pose by t15.55. Last 12 frames: 2D push 1.000 -> 1.007 so the cut happens inside a moving push | none - all five parts home | First and only frame of the complete car; it exists to become the render. 0.4 s on pose, not a 1.2 s still |
| RENDER | **R_ron7** | 33.161-36.971 / 21.13-24.93 (f634-747, 114 fr) | Ron's render 7 (white car, kit, gold wheels) | 7FinalSedanFL.jpg scaled so the car (bbox x 430-1610, y 713-1172 of 1920) is ~940 px wide in the 1080 frame (87 %, as v4 did for render 1), car centred, black above/below (check rows 0 and 1919 are pure black, as was done for render 1). Push continues at the same rate, 1.007 -> ~1.07 | **Hard 1:1 cut ON B7a 33.161.** Epsilon+ wordmark (white, ~300 px, centred, in the black under the car - measure luma < 10 under its box) in ON B7d 35.241 with a 4-frame fade. Picture + music fade 36.471 (B8a hit) -> 36.971 | The pay-off the user asked for. 2.08 s of render alone, then the wordmark; no Illumaesthetic logo |

Section list (rule B): TOP (S1) | FRONT (L 17.22-19.27) | LEFT SIDE (19.27-22.2) | REAR, continuous from 22.2 to the end:
apron low, wheels from the rear-left 3/4 wide, wing high, hero. No section is returned to. `ive director` will flag
L's last frames ~ R_ron7 (intended 1:1) and may flag leg 4's swap as a same-camera repeat (lesson: state swap = one beat);
log both.

Assembly: three clips, 156 + 478 + 114 = 748 frames; first clip one frame short / hold as in v4 so cuts land on f156 and
f634 exactly; verify both against the decoded audio (<= 1/2 frame).

## 4. Rules for the take (editor)
- One spec `L_build` with all keys; render it in frame ranges per leg (same keys = seamless joins), so a rejected leg is
  re-rendered alone.
- Grammar of every leg: camera LANDS (ease out) while the part seats, both ON the hit -> HOLD on a slow linear creep ->
  TRAVEL past the part just fitted to the next section. Parts appear only in clear black, never over the silver body
  (lesson), 0.62 s before their seat; park hidden parts at z -30 and jump them in between two frames as v4 did.
- Every fitted part stays on for the rest of the take. Base = car_nowheels + scanwheel_* until t7.884, then rim/tyre/brake_*.
  Parts from prep/kit2 only (front_lip, skirt_L/R, rear_apron, wing). Kit white, rims gold, car satin silver, black.
- The new wheels sit 47 mm higher and 30 mm further out than the scanned ones (Ron's fitment): expected, do not "fix".
- Re-timing for the replacement song: seats are at t0.635 / 2.707 / 6.011 / 9.305 (off 7.884) / 12.631, each followed by a
  creep hold (0.6-1.2 s). Creeps are <= 2 %/s, so up to 0.4 s can be cut out of any hold ON a hit without a visible pop;
  travel legs take `speed` 0.85-1.15. Beyond that, re-key the times and re-render the leg. Never retime inside a part window.
- Persistent data off; per-frame luma scan; no labels (parts are CAD placed on the scan, nothing to label factually).

## 5. Cut list (everything from v4 is gone; nothing is reused)
| v4 | fate | why |
|---|---|---|
| N1_open (front-left wide, car 9 % of frame) | cut | tiny, upper third; the stock whole car is now S1's first 1.27 s |
| N2_doors (front-right close) | replaced by S1 | doors as flat slabs hiding the openings, car cut both sides, door hole centre frame |
| N3_trunk, N3b_interior | replaced by S1 | same camera twice (IoU 1.0); interior dive is off-story for a kit reel; interior is still seen, from above |
| N4_close (separate closing shot) | merged into S1 | fourth viewpoint for one action; nose out of frame |
| s4_lamp, s3_wheel (stock macros, v1 renders) | cut | cutaways between installs, sections shown twice, old render set |
| I1_lip, I2_wheels, I3_skirt, I4_apron, I5_wing | re-shot as legs of L_build | wrong part placement (old lookbook fit), five unrelated viewpoints, clipped, small, order changed from the user's list |
| W_kit (1.2 s still at render-1 camera) | cut | dead hold, nose on the frame edge, door hole in the match frame |
| R_ron (render 1, 3.3 s) | replaced by render 7, 3.3 s + fade | see 2e |
| 2.8 s of running time | cut | "paced too slowly" |

## 6. Framing gate (rule A) - before any final frame
30 % preview at 7.5 fps of S1 and every leg; contact sheet of FIRST / MIDDLE / LAST frame of S1 and of each of the six
legs (21 frames) plus the five seat frames. Pass = (a) wides (S1 all, leg 4 wide, leg 6): whole car inside the frame with
>= 60 px margin, open door tips and lid included; (b) details: the named part spans >= 70 % of frame width at the seat or
close frame; (c) nothing but the far end of the car touches an edge in a detail; (d) no door inner face in S1 (doors must
be slivers - adjust the bearing, not the doors); (e) each part's pop-in frame is in black and inside the frame.

## 7. Hold list (> 0.75 s)
| where | length | reason |
|---|---|---|
| S1 open state, 15.358-16.600 | 1.24 s | read the real Door Open / Trunk Open data; camera drifts in on it. Trimmable |
| leg 1 lip seated, 17.851-18.675 | 0.82 s | whole lip on the car before the camera leaves. Trimmable |
| leg 2 skirt glide, 19.923-21.159 | 1.24 s | long low-contrast part, glide reads its length. Trimmable to 0.6 |
| leg 4 wheel close-up, 27.783-28.612 | 0.83 s | the only close look at the new wheel and brake |
| render before the wordmark, 33.161-35.241 | 2.08 s | the hero; slow push, no text yet |
| wordmark, 35.241-36.971 | 1.73 s incl. fade | "small and brief" |
Not holds: wheel-less car 25.60-25.90 (0.3 s between the sets, wheels moving either side of it).

## 8. Render budget
- 15 fps base: S1 78 + L_build 240 = 318 frames (+3 tail frames per clip).
- True 30 fps in-betweens (no minterpolate on anything fast - Civic lesson): S1 13.295-15.358 and 16.600-17.216 (40 frames);
  L_build everywhere except the creep holds 17.851-18.675, 19.923-21.159, 23.227-23.848, 26.521-27.171, 27.783-28.612,
  29.847-30.454 (4.8 s stay 15 fps, blended) = ~168 frames. Total ~530 frames, ~3 h at ~20 s/frame, one job at a time.
- Stills: none. Render 7 is used as delivered. Reused from earlier versions: nothing.
- New work besides renders: camera solve for render 7; `shift_x/shift_y` (and the existing `roll`) on camera keys in shot.py
  for the solved 9:16 window - if shift is not added, centre the window on the render's principal point and accept the car
  off-centre.

## 9. Not decided here - defaults
1. **Render 7 solve quality.** Gate: wheels within ~15 px and roof/lid/wing within ~40 px at 1920, judged on the overlay.
   Default if it fails: solve render 6 (rear, slightly right; same timeline, K17 swings 45 deg across the tail instead).
   If both fail: render 1 with the existing solve, hand-over moved to B8a 36.471 - add 31.088-33.161 pull-back to the
   rear-left wide and 33.161-36.471 travel round the nose to the render-1 camera, end at 39.80 (27.77 s). Worst option:
   3.3 s of travel that shows nothing new and passes the right-door hole.
2. **"Once the parts are opened up"** read as sequence (open, then install), car shut during installs (2c). If the user
   wants parts going on while it is open, only the lip and wheels can be done honestly.
3. **Ending length.** Default 24.93 s with a fade on the running track. If the replacement song has a natural ending,
   let the render run to it but keep the wordmark <= 1.7 s.
4. **Trunk interior** gets no close shot of its own (seen from above in S1 only). Default: leave it out; it is scan content,
   not kit content.
5. **Wheel-off look.** The cut-out scanned wheels are ragged (fit5c.png). Default: they are in frame only 0.5 s, from 9 m.
   If the preview shows shards, shorten the pull to 0.35 s.
