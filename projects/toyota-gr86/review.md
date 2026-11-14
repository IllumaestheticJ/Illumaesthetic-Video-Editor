# Toyota GR86 / Subaru BRZ (gen 2) - v7 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v7.mp4` (not in git). Same music, cuts and length as v5/v6 (1195 frames / 39.833 s).

v6 user notes:
1. "The BRZ and GR86 bumper are clipping into each other. Have them come off and then split apart."
   - In v4-v6 each moving bumper was ONE mesh: the BRZ full car's own bumper skin plus the GR86 Bomex bumper scan's inner face. They are two different bumpers.
   - Now (tools/split_v7.py, tools/shots_v7.py, shot.py `show` windows): the bumper pulls straight out as one piece. At 0.40 s it swaps to two parts, the BRZ skin and the GR86 scan. The BRZ skin lifts straight up out of frame; the GR86 scan tips and drops, and the rear lights ride it.
   - Labels: FRONT BUMPERS / REAR BUMPERS, sub BRZ + GR86, after the split.
   - The explode gives each bumper its own offset. In the reassembly the GR86 scan lands, then the BRZ skin, then the combined part swaps back in, so nothing clips at rest.
2. "There are still bits of the rear trunk left behind."
   - Coloured by source scan, the badge panel standing in the opening was Rear Bumper Removed fill: that capture had the lid CLOSED, so its lid skin refilled the opening. States captured with the lid closed may no longer fill within 12 mm of the lid (tools/build_v7.py).
   - The right gutter/wing strips the open captures lack are dropped (tools/lid_v7.py drop mask).
   - Uncaptured trunk-zone base tris: 39162 (v6) -> 15364. The rest is the rear-glass base in front of the shut line, hidden from the scanner by the raised lid.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 4 | Scan quality | 5 | No double bumper. No trunk leftovers in the opening. Luma is clean on all 12 re-renders. Edge margins: x2/x3 >= 42 px, h1 >= 16 px. |
| 5 | Story | 5 | The bumpers now read as two scans of two cars' bumpers: off together, then apart. |
| other | - | as v6 | |

## Remaining weak spots for the next agent
- x1 parts drop in through the frame top in frames 5-9, which is motion rather than a parked pose.
- The rear-glass base band stays (the scan hides it under the open lid).
- The exploded views are wide: a car plus two bumper pairs in 9:16.

---
# Toyota GR86 / Subaru BRZ (gen 2) - v6 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v6.mp4` (not in git). Same timeline, music, cuts and labels as v5
(1195 frames / 39.833 s, h264 yuv420p + AAC). Only the trunk changed.

v5 user note: "Rear trunk area is not cut correctly based on real trunk opening".

v5 problem: lid_v4 was a smoothed top/rear silhouette, not the scan's opening. Once the lid was off, the base showed:
- a saw-tooth deck edge at the glass,
- a ragged strip over the lamp tops,
- a stray panel in the cargo, from the bumper-off capture filling the lid zone.

v6 fix:
- lid_v6 (tools/lid_v6.py) is exactly the car4 triangles that the Trunk Open captures lack (> 8 mm).
  - The label is smoothed on the surface (20 mm majority).
  - The right half is mirrored from the clean left half, because the right C-pillar coverage hole had read as lid.
  - In top and rear projections it now matches the Trunk Open opening: a rear-face trapezoid plus wings over the lamps.
- Base comp_explode6 (tools/build_v6.py): Trunk Open, the bumper-on capture, fills the opening as captured, minus its bumper skin. The bumper-off capture is limited to the rear bumper zone.
- The 9 shots that show the lid or the opening were re-rendered (tools/respec_v6.py).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 4 | Scan quality | 5 | The trunk opening is the Trunk Open capture itself, and the lid edge is the opening edge, with no saw-tooth, strips or stray panel. Luma is clean on all 9 re-renders. |
| other | - | as v5 | Unchanged: hook 4, beat sync 4, story 5, text 4, ending 4, technical 5. |

## Remaining weak spots for the next agent
- The Trunk Open capture is sparse in the cargo floor (33k new tris). The cargo reads but is not dense.
- The rest is as in v5: small exploded views, a thin side marker, and the e4 bumper fragment.

---
# Toyota GR86 / Subaru BRZ (gen 2) - v5 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v5.mp4` (not in git). 1080x1920, 30 fps, 1195 frames / 39.833 s,
h264 yuv420p + AAC. Scan-only, so criteria 3 and 6 don't apply.

v4 user feedback addressed:
1. "Use this music instead": the user-supplied Gran Turismo 2 "East City" theme (not in git).
   - `ive beats` said 61.5 BPM (half time). The spectral-flux grid over the section is 122.05 BPM, bar 1.9664 s.
   - The excerpt starts two bars before the drop (song 79.402 s), and the cut is one shot per bar.
   - The drop (83.34 s) lands on the hood hinge. The hats enter on the side markers. The loudest bar is the rear crash beam. The section's decay sits under the logo.
2. "Make sure all parts are highlighted": every part and cut panel now gets its own bar with its own label.
   - New: the front SIDE MARKERS. Their part scan was fetched in v3 but never shown. It is placed by ICP at 3.5 mm, and the bumper keeps the "Side Markers Removed" recess.
   - New labels: HOOD, FRONT BUMPER, TRUNK LID and REAR BUMPER. These moved unlabelled in v4.
   - After the last single part, a three-angle exploded view puts every part out at once (offsets with 0.2 m+ clearance, checked by projection), then a one-bar reassembly lands on the clean car.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car with motion from frame 0, then a cut at 1.97 s. The first part move (hood hinge) is on the drop at 3.93 s. |
| 2 | Beat sync | 4 | 19 cuts measured on decoded audio: 18 within +-16 ms, and f943 at +20 ms on a doubled hit. Seven cuts were moved one frame onto their measured onsets. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | Every new render was luma-checked; the steps are only parts entering the frame. No bumper skin is left (v4 geometry). The left mirror is a broken capture, so it stays home in the explode. |
| 5 | Story | 5 | Front: hood hinge/off, side markers, front bumper, structure. Side: mirror. Rear: lid hinge/off, rear bumper, beam, reverse light, plate lamp. Then all parts at once (3 angles), reassembly, clean car, logo. One part per bar. |
| 7 | Text | 4 | 12 short factual labels, one per part/state bar. Coverage under each label box is <= 7 % (10 of 12 at 0 %). No numbers. |
| 8 | Ending | 4 | Reassembly ends on h2's camera, the clean car swaps in on the bar, then a fade and the 860 px logo over the music's decay. |
| 9 | Technical | 5 | Spec above, one Blender at a time. x2 is re-centred in the assembler (losslessly shifted, padded with the render's own black). |

## Remaining weak spots for the next agent
- x1/x2 exploded views keep the set small (a car + 1.6 m of parts in 9:16), and x2 needed a vertical re-centre. A lower, closer orbit per group would read better.
- The side marker is a thin part. It reads on the push-in, but a turn would show more if its back was scanned (unchecked).
- e4: a fragment of the parked rear bumper shows at the frame bottom (from v4).

---
# Toyota GR86 / Subaru BRZ (gen 2) - v4 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v4.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC. Scan-only, so criteria 3 and 6 don't apply.

v3 user feedback addressed:
1. "Move faster". There is now a cut on every kick: 16 clips of 2.45 s, where v3 had 8 clips of up to 9.8 s. Each shot has one action, part moves take 0.4-1.0 s, and part-move shots render at native 30 fps.
2. "Parts of the old bumper still visible".
   - Each bumper now carries every car4 triangle that its bumper-removed state lacks (tools/build_v4.py).
   - Hood Open and Trunk Open were captured with the bumpers on, so they may no longer fill the bumper zones. In v3 they put bumper skin back on the car.
   - Projections and renders show bare front and rear structure.
3. "Hood needs to hinge open THEN come off". The hood swings -50 deg about its rear corners, then lifts off on the next kick. Neither open-state scan captured the propped panel, so there was nothing to fit a hinge to. The angle matches the 250 mm strip of open hood in Hood Open.
4. "Rear trunk cut correctly / done the same".
   - lid_v4 is cut on the shut lines: top and rear silhouettes voted by the opening Trunk Open leaves, one smoothed symmetric interval per row, and the front edge at the glass shut arc (tools/lid_v4.py).
   - It hinges +65 deg, then lifts off to show the cargo area.
   - There is no "lid removed" scan, so the lid coming off rests on the user's request.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car with motion from frame 0 (v2 opener at 2x), then a cut at 2.48 s. The first part move is the hood hinge at 4.93 s; it was 7.4 s in v3. |
| 2 | Beat sync | 5 | 15 cuts on decoded audio, half-rise after the dip, offsets -16..+14 ms (target +-16.7). |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | No bumper skin is left on the base. Every render was luma-checked; the steps are only parts entering or leaving frame. The lid/hood undersides are not scanned, so the hinge cameras stay on the outer-face side. The rear wheel scan is patchy, so e1 keeps it to a corner. |
| 5 | Story | 4 | front (hinge, hood off, bumper off, structure) -> side (mirror) -> rear (lid hinge, lid off/cargo, rear bumper off, beam, reverse light, plate lamp) -> reassembly with the hood shutting on the 34.32 return -> clean car -> logo. No section repeats. |
| 7 | Text | 4 | 7 short factual labels, one per state/part beat, no numbers. Each sits where scan coverage under the label box is <= 4 % over its whole window. |
| 8 | Ending | 4 | Parts home rear -> front, hood shuts on the kick, then a clean complete car (car4) from high on the right fades into the 860 px logo. ive director calls the h2 rise + fade "dead"; it is the only hold in the reel. |
| 9 | Technical | 5 | Spec above, one Blender at a time, persistent data off. In-shot frame-diff spikes are fast part moves, checked frame by frame with no pops. |

## Remaining weak spots for the next agent
- e4_rear_beam: a fragment of the parked rear bumper shows at the frame bottom (camera-only push).
- e1_lid_hinge: the hinge reads, but the quarter panel fills the left third; a higher pass over the deck would be cleaner.
- h2_hero is a slow camera; a slightly faster rise would keep the pace to the logo.

---
# Toyota GR86 / Subaru BRZ (gen 2) - v3 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v3.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC. Scan-only, so criteria 3 and 6 don't apply.

v2 user feedback addressed:
1. The logo is bigger: an 860 px wide card, up from the small v2 logo.
2. The hood-open composite no longer cuts away the windshield. tools/hood_trim.py trims the hood at the measured cowl gap.
3. The trunk-open scan is used. The lid is masked against both open-lid states (tools/lid_mask.py), and e_rear shows TRUNK OPEN cargo.
4. The rear lights are exploded out of the rear bumper. The reverse light and licence-plate light scans are ICP-registered (tools/register_part.py), and f_lights lifts each out of the tipped bumper with a label.
5. The side-mirror-removed scan is used: d_mirror flies the right mirror off to show the scanned mount.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Same opener as v2: the whole car with motion from frame 0. The first part move is the hood at 7.4 s. |
| 2 | Beat sync | 5 | The cut frames are identical to v2 (f148, 221, 442, 515, 809, 956) and the audio is the same. v2 measured +2 to -13 ms on decoded audio. The v3 cutcheck lists the same 6 cuts. Its onset at 515 (-74 ms) locks to a later transient, the known checker issue; by the first half-rise after the dip it is -7 ms. f1103 is fade-to-logo by design, so it has no spike. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | Every shot passed the luma check. The c_front f58-64 slope is the bumper tipping away onto black, not a lighting dropout (checked on a sheet). The windshield is intact. The tail lamps survive in comp_explode3 (drop-islands 150, not 1500). The plate is kept as scanned (the IS300-only rule). The plate lamp is small and sits at the frame edge in f_lights. |
| 5 | Story | 4 | Front to side to rear on the car's right, each section once. Front: hood, then front bumper. Side: mirror. Rear: lid and cargo, then rear bumper and crash beam, then the lights. Then reassembly, a fade, and the logo. The ive director flags b_headlight vs d_mirror as the same view (silhouette iou 0.78), but they are different subjects (headlight close-up vs door mount), so it is a false positive. |
| 7 | Text | 4 | 6 factual labels, one at a time, on scan shots only, with no numbers. Coverage under each label box was measured at <= 14% scan pixels. The f_lights labels moved to y 0.33 because at y 0.08 they sat on the crash beam. |
| 8 | Ending | 5 | All parts fly home rear to front, the hood lands on the 34.32 return, then a 1.95 s fade and a full-width logo from the 36.766 kick. |
| 9 | Technical | 5 | Spec above, one Blender at a time, persistent data off. |

## Remaining weak spots for the next agent
- The plate lamp is a small part. It reads only as a silver block top-right in f_lights, and a closer push would sell it better.
- The rear bumper pokes the bottom-right of the e_rear end frame.
- There is a small notch at the right quarter edge of the lid.

---
# Toyota GR86 / Subaru BRZ (gen 2) - v2 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v2.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC, moov first. Scan-only reel (no IRL footage), so criteria 3 and 6 don't apply.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car fully in frame from frame 0, ~20 deg arc + push from the first frame. The v1 0.8 m dolly read as static (ive director: 4.8 s dead), so it was replaced. It is a camera move, not a transformation; the first part move is the hood at 7.4 s. |
| 2 | Beat sync | 5 | Measured on the delivered file's decoded audio (broadband 1 ms RMS, half-rise of the kick): offsets +2, -13, -7, +10, -6, +14 ms (cuts f148, 221, 515, 736, 956, 1103). Target is +-16.7 ms. The accents.py grid sits ~30 ms after the kicks, so every cut moved 1 frame earlier than the grid. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | The scanned licence plate is kept as scanned. The user rule in lessons.md allows plate flattening only on the IS300. tools/deplate.py was run, then reverted; g_rear and s_stack were re-rendered from the original scans. No light dropouts: every shot luma-checked (tools/lumacheck.py), no steps > 4. The comp_explode cowl area still shows the scan's dark gaps in the bay at the d_front push-in. Those are real data, not fixed. |
| 5 | Story | 4 | Order is driven by the scan features (direction.md): whole car -> front detail -> front section (hood off, bay, FRONT BUMPER REMOVED structure) -> rear section (REAR BUMPER REMOVED, crash beam push-in) -> top stack -> reassembly -> logo. Each section plays once; no repeated orbits or reused shots; no trunk shot (closed-trunk scan only). |
| 6 | Grade | n/a | No IRL. |
| 7 | Text | 4 | 3 factual labels on scan shots only, each on black above the car: FRONT BUMPER REMOVED / HOOD REMOVED · STATE SCAN, REAR BUMPER REMOVED / STATE SCAN, REAR CRASH BEAM. No numbers. The rubric allows <= 2 items, but the user's v2 brief asked for the bumper-removed data to be labelled, so there are 3 (one at a time). |
| 8 | Ending | 4 | Parts land home at 34.35 s, then a 2 s fade to black starting 0.45 s later (ive director had flagged a 2.4 s dead hold), then a small logo from the 36.766 kick to the end of the audio. |
| 9 | Technical | 5 | Spec above. Frame-diff spikes at every cut (29-78 vs median 0.9), none at the fade->logo, which is a fade by design. No duplicate frames at cuts. |

## Remaining weak spots for the next agent
- The opener's first part transform only comes at 7.4 s. A part move inside 1.5 s would score a 5 hook.
- The ive director still flags f_reassemble's fade as "dead frames": the detector counts a fade as stillness.
- s3_wheel (b_headlight) is a 2.4 s v1 shot reused from 2.4 s; it is the only v1 render left apart from the s7 tail.
