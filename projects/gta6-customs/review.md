# gta6-customs: self-review

## v1 (2026-11-19)
Output: `/home/user/media/work/out/gta6-customs_v1.mp4`, 1080x1920, 30 fps, 13.7 s.

What was checked by looking: placement overlay of the Civic on the game car in the menu and rear views; clean
plates for both views; every re-lettered block against the capture's original at 1:1; all 16 whip frames; a
sheet of every 12th frame of the composite; a strip of the 9:16 reel. Sound: tick positions against the cuts.

Holds up:
- Civic stands on the game car's spot with the room's perspective in both views (wheels on wheels in the menu view).
- Menu lettering matches the game's faces, sizes and colours; prices and part names are the catalogue's.
- Whips keep the capture's 8-frame timing and blur.

Weak, known:
- The car is a clean render in a photoreal game: no driver, dark opaque glass, no dirt, simpler reflections
  (a painted HDR panorama of the room, not the room). It reads as CG next to the garage, most in the menu view.
- The picture is a third of the 9:16 frame's height.
- "Not enough cash" and the $99 wallet are the capture's own and now sit under an Epsilon part and price.
- Stat bars and numbers are the game's for its car. The +0.1 handling gain shown with the wing is the game's
  number for its "Custom Wing"; it is still on screen. The kit screen uses the panel without gains.
- Camera positions rest on assumed El Camino dimensions for the game's car; the Civic is 0.45 m further back
  in the rear view than in the menu view so that tails line up (not visible, but not one solve).
- Whip frames: faint streaks of the game car remain under the blur.
- No Front Lip / Side Skirts / Rear Lip screens: the capture has no camera move for them.
- Parts are black on every state; no colour-matched option shown.

## v2 (2026-11-19) - after the user's review of v1
User: "side skirt, front bumper, rear lip, and rear wing need to actually be combined with a confirmation sound
effect", then a second capture: "include the audio and sounds".

Output: `/home/user/media/work/out/gta6-customs_v2.mp4`, 14.6 s.
- Stock car, then four purchases that stay on: Front Lip and Side Skirts on the list screen, select Rear Lip,
  whip to the rear view, Rear Lip and Sport Wing there, whip back with all four rows marked and the kit on.
- Each purchase is the second capture's own: its sound (1.65 s), part and "Applied" 0.1 s in, "Purchased" pop-up
  0.3 s in. Wallet pays the catalogue prices: $1,420 > $1,135 > $735 > $450 > $0. "Not enough cash" is gone.
- The list is now built per state (highlight bar measured from the capture, yellow marker on fitted rows).
- Checked: 18 frames across every install and both whips; all ten menu states on their own; the highlight bar
  against the game's at 1.6x; sound level per frame at each event (purchase 10 dB over room tone, on its frame).
- Not checked by ear. Still open from v1: render look, small picture in 9:16, no driver. New: the list fits two
  parts directly, which the game does on a part's own screen; the part is called Front Lip (catalogue), the
  user said front bumper; room tone sits at -33 dB after the gain, on the loud side.

## v3 (2026-11-19) - after the user's review of v2
User: car comes in stock; front lip, side skirts, rear lip (camera to the sample's exhaust angle), rear wing, all paint
matched; then a colour change that paints everything; then suspension (handling goes up) and wheels (custom);
after checkout the NPC says "need anything else or is that everything?".

Output: `/home/user/media/work/out/gta6-customs_v3.mp4`, 24.5 s. Tools: `ui3.py`, `compose3.py`, `assemble3.py`.
- Seven purchases, each with the game's purchase sound, "Applied" and the "Purchased" pop-up: Front Lip, Side
  Skirts (list screen), Rear Lip (second capture's Exhaust camera, moved 0.6 m closer so the Civic covers the
  game's car), Sport Wing (rear view), Respray grey > Boost Blue (body and parts), Lowered Suspension Kit (car
  drops 45 mm; the game's +0.3 asphalt handling), Custom 6-spoke rims (site's TE37-style wheel, bronze).
- Wallet $2,730 > $0: Epsilon parts at catalogue prices, respray free and suspension/rims at the game's prices.
- Exit: the capture's UI-free shop frame, wallet $0, the line as a subtitle. No voice (see edit log).
- Checked by looking: every menu state at 1:1; overlays of the three new cameras; 21 frames across the timeline;
  the exhaust view after a leftover taillight was found (capture's camera creeps in: frame range cut to 0.5 s,
  mask widened); the suspension view after its background fill came out as a grey blob (now filled from above).
- Known weak points: all six camera moves are synthetic blur whips (the capture has real ones for two); the
  second capture's views carry the uploader's watermark and overcast light next to the first capture's sun;
  stats panel on the suspension screen keeps the preview arrows after purchase; background behind the car in
  the suspension and wheel close-ups is invented; rear lip's lower section is black plastic in the model, so it
  does not read as fully paint matched; sound not checked by ear.

## v4 (2026-11-19) - after the user's review of v3
User: "fix the audio, add dynamic money/pricing so its accurate - brand the kit as epsilon"; "the repeating 'need anything
else' is annoying - should only do it at the end"; camera should snap to the front and sides for front lip and side
skirts; vary the voice lines if the sample allows, never repeat one; pan round the stationary car at the end if
possible; improve the mesh of the 6-spoke wheels.

Output: `/home/user/media/work/out/gta6-customs_v4.mp4`, 26.5 s. Tools: `ui4.py`, `compose4.py`, `assemble4.py`.
- Audio: the v2/v3 "purchase sound" had the mechanic's line in it (right-panned, from 0.25 s in). Purchase sound is now
  the ticks and the chime up to the voice, then only the chime's highs; the line plays once at the exit. Measured: speech
  band after each purchase is at room-tone level (-54 dB), the line is 30 dB above it. Not checked by ear.
- No extra lines: three more right-panned phrases follow in the capture (3:36.1, 3:36.9, 3:38.2) but nothing is
  subtitled and I cannot hear what they say, so they are not used. Asked the user.
- Cameras: front (front lip) and side (side skirts) from the second capture, moved in so the Civic covers the game's car.
- Pricing: painted variants (485 / 800 / 485 / 850), wallet 3,930 counting down to 0; EPSILON+ badge and names.
- Wheel: rebuilt from the TE37 scan at 160k triangles (rim) with the scanned tyre; old one was 8k and faceted.
- Ending: 3.4 s orbit (150 degrees) round the stationary car on black with the wordmark. Not in the shop: no 3D shop.
- Still weak: background behind the car in the side and suspension views is invented and soft; synthetic whips;
  uploader's watermark on second-capture views; sunny/overcast mix; the orbit car is small in the 9:16 frame.
- Process note: the first v4 audio build used left-minus-right for the chime, which is where a right-panned voice
  lives. Caught by measuring the result before sending. Measure the channels before choosing a separation.

## v5 (2026-11-19) - after the user's review of v4
User: "Fix the brake caliper underneath the 6 spoke wheels, and fix the environment blur so it's not as prominent on the
side skirt camera change".

Output: `/home/user/media/work/out/gta6-customs_v5.mp4`, 26.5 s.
- Brakes: the Civic's own drilled disc and caliper are kept behind the swapped wheels (wheel close-up, exit shot, orbit).
- Side-skirt view: new camera, Civic covers 98 % of the game's car (was 67 %); remaining 3 % of the frame continued from
  the wall and floor without blur. Whips into and out of the view re-rendered from the new camera.
- Checked: wheel close-up before/after; the side view at full size; frames through both whips; reel strip with the orbit.
- Left: a few-pixel fragment of mirrored sign text at the right frame edge behind the tail in the side view; the front
  view still has soft fill beside the mirrors (same cause, not asked about); whips are still blur by nature.

## v6 (2026-11-19) - after the user's review of v5
User: "If you can't render a 360 without bugging out, then skip it. I wanted the environment. Use the longer reference
video to build out more of the GTA6 garage environment if needed."

Output: `/home/user/media/work/out/gta6-customs_v6.mp4`, 25.6 s. Orbit removed; ends in the shop, then the wordmark.
- Environment build tested and not used: SfM on the longer capture connects 9 of 20 views (546 points), none facing the
  front of the shop. See the edit log. `assemble4.py` only uses an orbit render with ORBIT=1.
- Lesson: I shipped a studio orbit on black when the user asked for a pan round the car "if possible". The context was
  the garage; when a request cannot be met as meant, say so and offer options rather than substitute a different shot.

## v7 (2026-11-19) - after the user's review of v6
User: "Remove the 'epsilon' from the primary menu - so it just says 'front lip' etc."

Output: `/home/user/media/work/out/gta6-customs_v7.mp4`, 25.6 s. List rows renamed; nothing else changed.
First splice dropped the 8 whip frames after the list (partial render stopped at the whip); caught by the frame count
(685 instead of 693) and a look at frame 42, redone before sending.

## v8 (2026-11-19) - after the user's review of v7
User: "Are you able to point the camera down lower for the side skirt shot? The skirts don't fit in the frame"

Output: `/home/user/media/work/out/gta6-customs_v8.mp4`, 25.6 s.
- Side-skirt shot re-sited (see edit log): whole skirt in frame, before/after reads. Only frames 114-197 and 439-530 were
  re-rendered (START/END in compose4.py) and spliced in; alignment checked against v7 at ten frames.
- Fixed on the way: price block hidden behind the front wheel (now a layer on top), wallet box visible during whips
  (figure only now), streaky fill right of the tail in both low views (doorway mirrored in instead).
- Weak: the patch behind the tail is mirrored trees/grass, plausible but invented; the skirt and suspension shots share
  an angle; the wallet icon is missing for the 8 frames of each whip.

## v9 (2026-11-19) - after the user's review of v8
User: "It should say 'rear wing' instead of 'sport wing'. The menu title names should stay true to GTA6. Also, the menu
skips the navigation to the paint section entirely."

Output: `/home/user/media/work/out/gta6-customs_v9.mp4`, 29.3 s (803 menu frames + card).
- Rear Wing on the list, its screen and its item line. Suspension screen title restored to PRO BUILDS / WHEEL KITS.
- Tab navigation before paint, suspension and wheels, with the game's lists and a tab tick, row tick and select each time.
- Checked: all navigation states at full size (lists, tab bar in four positions), 20 frames across the new timeline,
  frame count after the splice (803). Sound events printed from the timeline, not listened to.
- Open: whether "titles true to GTA 6" also meant the part screens (the game's own would be Front Bumper, Rear Bumper,
  Spoiler; it has no skirt category for this car) - asked. One tab press from Pro Builds to Wheels where the game needs
  several; Wheels list on the menu camera. Deselected Bodywork tab is redrawn (close, not pixel-identical).

## v10 (2026-11-19) - after the user's review of v9
User: "Wheels kits is not suspension..."

Output: `/home/user/media/work/out/gta6-customs_v10.mp4`, 29.3 s. Suspension on the Performance tab (see edit log).
Lesson: "true to the game" does not outrank making sense to the viewer. The game's own filing (lowered kit under Wheel
Kits) was a detail of this build that a viewer reads as wrong. When a game label would mislead, say so and propose the
sensible home instead of restoring it silently.

## v11 (2026-11-19) - after the user's review of v10
User: uploaded a clip of GTA 6's Honey FM: "put this radio station as in game audio overlay ... background noise like
the real game".

Output: `/home/user/media/work/out/gta6-customs_v11.mp4`, 29.3 s. Radio bed added (see edit log); picture unchanged.
- Measured: bed -32.6 dB between events, purchases -24.7 dB, line -23.8 dB; starts with a 0.5 s fade, gone 0.4 s before
  the card. Not checked by ear: level, the muffling, and whether the clip's creator is audible are for the user to judge.

## v12 (2026-11-19) - after the user's review of v11
User: "The menu navigation for all the aero bits is also incorrect. It's skipping steps", then "remove the watermark on the
bottom right".

Output: `/home/user/media/work/out/gta6-customs_v12.mp4`, 28.7 s (786 menu frames + card).
- Aero parts: list > select > part > buy > back > list (row marked) > down > select, four times. Holds tightened so the menu
  (26.2 s) still fits under the 26.8 s radio bed.
- Watermark covered on all second-capture frames; clean BACK hint restored.
- Fixed on the way: during whips back to the list the whole list rectangle was held sharp over the blurred car; now only the
  rows and the tab bar are.
- Checked: 20 frames across the four part loops; bottom-right corners of five views at full size; a whip frame.
- Weak: the patched corner is faintly lighter than the floor around it at full size; part screens are now 2.0 s each, tight
  for reading the price; fourteen camera whips in 26 s is busy.

## v13 (2026-11-19) - after the user's review of v12
User: "Finish off with the epsilon logo at the end redone in gta6 colors"

Output: `/home/user/media/work/out/gta6-customs_v13.mp4`, 28.7 s. End card only; picture and sound before it unchanged.
Card: `/home/user/media/work/gta6-customs/end_card.png`. Colours sampled from the game's logo in the capture (edit log).
