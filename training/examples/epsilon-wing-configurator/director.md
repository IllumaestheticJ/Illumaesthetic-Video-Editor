# Director pass: epsilon-wing-configurator (on shotplan v1)

Narration phrase times and the 0.07 + 0.5k kick grid are locked. Only one dry-run sheet exists (`hero_a_sheet.jpg`), so I
judged the other 15 shots from `tools/capture.js` (crop rects, actions). Every shot needs a first/mid/last sheet before assembly.
Scale on a phone: portrait stage = 720 css -> 1080 px (1.5x). Stacked/panel crops = 284 css -> 800 px (~2.8x), so 13 px UI
text comes out at ~37 px and reads fine. Stage labels (SIDE/REAR, MM/IN, OVERHANG/HEIGHT dims) at 1.5x come out at ~15 px
and do NOT read. **Global fix:** capture portrait-stage shots at 540x960 css @2x (that viewport is already verified in
features.md) = 2.0x, and use the TRUNK zoom in Side/Rear views.

hero_a sheet: the car fills only ~40 % of the width with dead grey around it. The view toolbar (top-left) and the IN/handles/undo
cluster (bottom-left) are cut off by the left crop edge. In the last frame the orbit pushes the nose off the right edge.

| # | shot | in-out | verdict | focus | changes / reason |
|---|---|---|---|---|---|
| 1 | hero_a | 0.00-4.07 | KEEP, re-frame | GR86 + recommended wing | Start with the car at 85-90 % of the width. Hide the stage chrome or include all of it (no half buttons). Use a 20 deg rear-3/4 orbit plus a 10 % push-in, so the nose stays in frame on the last frame (it is clipped now). |
| 2 | hero_b | 4.07-8.57 | REPLACE | the app itself (phone layout) | Same car, closer, orbiting the other way is the same subject and move as hero_a, and the outro repeats it again. Replace it with the portrait (phone) layout: the stage holds hero_a's end view (no orbit), the CONFIGURE bottom sheet slides up on 4.57, the "Est. $" header lands at about 5.5, and the sheet scrolls past steps 1-4 to end on "1 Vehicle" at 8.57. New info: what the tool is ("customization") and its 4 steps. Text read check at 2x. |
| 3 | cars | 8.57-14.07 | KEEP | Make/Model + 3D swap | 4 cars in 5.5 s, each a new subject. The Model select must show the "(3D Scan)" label in frame on "forty-five ... 3D scans" (~11.5-14). |
| 4 | wing | 14.07-18.07 | KEEP, fix the end | wing element | "Custom TC width" holds for 1 tick: hold the made-to-order width field for >= 0.5 s (from 17.57) so the "custom width" option reads. |
| 5 | mounts | 18.07-24.07 | KEEP, trim the actions | setup cards + Mount | Fender appears 3 times (rec -> Bottom -> Fender -> Swan -> Fender), so states repeat. New plan: open on the cards with the RECOMMENDED tag visible and Bottom mount selected, then click Swan neck on "swan neck" and the Fender mount card on "fender mount". That is 3 states, each new, each landing on its word. |
| 6 | bases | 24.07-26.07 | KEEP | base style | CNC -> sheet metal on GR86. The 3D close stays low on the trunk/base, so it does not overlap any other 3D shot. |
| 7 | aoa | 26.07-29.07 | KEEP, change the top view | AoA hole | Top = Side view now, then 3D (turn3d), then Side again: the side view is split in two. Use the 3D view for the top instead: a close side-on 3/4 of the wing, so the tilt reads as the holes step 0 -> 15. turn3d then continues from that exact camera (one continuous 3D run). |
| 8 | turn3d | 29.07-30.57 | KEEP, re-angle | the drag/zoom gesture | Today it is the GR86 at rear 3/4, orbiting = hero. Start from aoa's end camera. The cursor drags the car round to the front 3/4 (an angle no other shot uses), with the wheel zoom ending on the base. |
| 9 | side | 30.57-35.57 | KEEP, re-scale | side-view handles | The only Side-view sequence now. Use the TRUNK zoom at 2x so OVERHANG/HEIGHT read. Drag lands about 31.6, tilt about 34.0. Once the wing moves, the "New ... upright" / +$200 note may appear: keep it if in frame (it's data, not a label). |
| 10 | rear | 35.57-38.57 | KEEP, re-scale | endplate width drag | 2x / TRUNK zoom. This shot starts the single Rear-view sequence. |
| 11+12 | sliders+units | 38.57-43.07 | MERGE (one held 4.5 s shot) | number controls -> units | sliders (side view on top) and units (portrait side view) both reuse the side view: that makes 3 non-continuous side-view shots and a 1.5 s unit shot whose MM/IN labels are unreadable at 1.5x. One stacked shot instead: Rear view on top (UPRIGHT SPACING C-C dimension + MM/IN toggle inside the top crop), Upright spacing + height controls below. Slider drag 38.6-39.6, lock tick ~40.1 ("locks"), click MM on the 41.57 kick ("inches or millimetres"); the C-C dimension and the panel values switch together. Drop the 41.57 cut. |
| 13 | price | 43.07-48.57 | KEEP | Price & quote | 3 actions, each new. Carry the custom-upright state from shots 9-12 if the capture allows it (the +$200 line = "updates live"); never click SEND. |
| 14 | more | 48.57-52.57 | KEEP | More options | Blueprint ~49.6, own photos ~51.1 on their words. |
| 15 | outro | 52.57-55.57 | KEEP, change the view | the finished build | GR86 wide rear-3/4 orbit = hero_a again. Show the configured car (custom uprights/width from 9-12) front-3/4 high, opposite side to hero_a, 10 % push-in, no orbit, wing centred on the last frame. |
| 16 | logo | 55.57-58.57 | KEEP, trim | Epsilon+ wordmark | 3.9 s logo = "held too long" (lessons). Cut on 55.57, end on 58.57 (last hit 58.45 + decay). White wordmark ~720 px of 1080. |

## Hold list (> 0.75 s with no new motion)
- hero_b 4.07-4.57: stage still while the sheet starts to rise (0.5 s, under the limit). Every other hold is under 0.75 s or sits on a narrated word.
- mounts: each state holds ~1.5-2 s. The reason: the 3D upright change has to read, and it is timed to the narration words.
- bases 25.1-26.07: sheet-metal base held ~1 s so the 3D base change reads.
- sliders+units 41.6-43.07: values after the MM click, held ~1.4 s so the changed numbers read.
- price: "Saved. Link copied." and the locked "Unlock and edit" state, each ~1 s, so the confirmation text reads.
- logo 55.57-58.57: fade in, hold, out on the decay.

## Concrete changes (editor)
1. Recapture hero_a with the new framing (no clipped chrome, car 85-90 % of the width, nose in frame on the last frame).
2. Write a new `hero_b` capture: phone layout, bottom sheet opens and scrolls the 4 steps.
3. mounts: start on Bottom mount, then Swan neck, then Fender card (drop the 2 extra Fender clicks).
4. wing: hold the custom width field >= 15 frames before the cut.
5. aoa top = 3D close on the wing. turn3d starts from that camera and ends at front 3/4 + zoom.
6. Portrait-stage shots (side, rear, turn3d, hero, outro): viewport 540x960 @2x; Side/Rear in TRUNK zoom.
7. Merge sliders + units into one Rear-view stacked shot, 38.57-43.07; delete the `units` capture and the 41.57 cut.
8. outro: configured GR86, front 3/4, push-in, no orbit.
9. Logo 55.57-58.57 (end the video at 58.57), wordmark ~720 px.
10. Before assembly, make a first/mid/last contact sheet for all 15 shots (no clipped UI, focus text legible at 1080 wide)
    and log each change with `ive log --why`.
