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
