# Game mod-shop reel (photoreal game, moving camera)

A real game's customisation shop with the client's car in place of the game's, the menus re-lettered for the
client's parts, and the parts bought one after another with the game's own sounds. Worked project:
`projects/gta6-customs/` (GTA 6, Civic sedan, 19 review rounds on 2026-11-19; `review.md` has every round).
Tools live in `projects/gta6-customs/tools/`; copy them into a new project and change the constants.

Everything here was learned from reviewer feedback. Where a line says "user:", that is what was said.

## 0. Ask first (each of these cost a review round)
- The **story**, screen by screen: which items are bought, in what order, from which camera, and how it ends.
- What the **parts are called** on screen (user said "Rear Wing"; the catalogue says "Sport Wing").
- Whether a reference picture is **the** picture or a look to follow (three rounds of drawn palms, then
  "use exactly this").
- Which **voice lines** to use and what they say: I cannot hear. Ask for timestamps.
- Whether the capture's **creator watermark** stays (it is their credit; the user decides).
- Whether an **orbit / 360** is wanted. Inside the game's scene it is not possible from menu captures (§9).

## 1. Capture breakdown (`clips.md`)
- Tile the whole capture at 0.5 fps, then the menu part at 3 fps. Frame differences find camera moves and cuts
  (a 60 fps upload often doubles every frame: compare over a 2-frame window).
- List every **held view** and what it shows, every **menu list** (tab names and rows, read off the frames), every
  **screen title**, and the **one or two purchases** if there are any. A capture that never buys anything has no
  purchase sound or "Purchased" pop-up: ask for one that does.
- Audio: level per second in the speech band and the side channel; one-frame menu ticks show in the high band.
  Before reusing any clip longer than a tick, check it for a voice (§7).
- A second capture may be overcast where the first is sunny, and carry a watermark. Note both.

## 2. Cameras (`vps.py`, `camfit.py`, `mancam.py`)
- Focal length and pitch from the **room's vanishing points** (LSD segments, RANSAC, focal from each orthogonal
  pair). The game keeps one field of view: GTA 6 f = 1757 px on 2560. The horizon row gives the pitch.
- Position and scale from where the game's car meets the floor: wheel contact points (picked on a gridded zoom),
  or from behind the ends of its bumper, with the dimensions of the real car it copies. The tyre radius that
  falls out is the check.
- Then **move the camera until our car covers the game's** (user: "fix the environment blur"). The capture frame
  is a flat plate, so the camera is free. Render a 20 % silhouette per candidate, count uncovered pixels of the
  game car's mask, and also project the part's bounding box to make sure the part is in frame and clear of the
  menu blocks (user: "the skirts don't fit in the frame"). Aim for under 5 % uncovered.
- Check that a "held" view really is held (phase correlation over the range): a creeping camera left the game
  car's tail light outside the mask.

## 3. Plates (`plate.py`)
- Game-car mask: frames where the same camera shows it in different paint, or a hand polygon, dilated 20 px.
- Fill only what our car leaves uncovered, with real texture and **no blur**: wall continued downward, floor
  mirrored from the open floor, sampling only outside the game car. Tried and rejected: Telea and FSR (smear),
  shift-map (smeared the car's colour), blurred column fill (read as a smudge).
- The uploader's watermark, if the user wants it gone: cover the corner with mirrored floor from beside it and
  put a clean button hint back from the other capture.

## 4. Car renders (`ive kit-render`)
- States are hide-lists on one GLB (`cars.yaml`). Parts **paint-matched** unless told otherwise.
- Light: a painted HDR panorama of the room in the car's frame (`make_env.py`, rig key `world_image`), exposure
  per view (rear view -1.3 EV, exhaust view -0.8).
- `--wheels <glb>` swaps wheels and keeps the car's own disc and caliper (the wheel files carry a placeholder
  block; user: "fix the brake caliper"). `--wheel-color`, `--drop <m>` for suspension.
- Showroom wheel GLBs are game-budget meshes. For a close-up rebuild from the scan:
  `RIM_TRIS=160000 TYRE=scan TYRE_TRIS=160000 blender -b -P Epsilon-Site/showroom/models/tools/te37_wheel.py -- <stl> <out.glb>`.
- Quality that is enough at 1080-wide delivery: stills 60 % of 2560x1440 at 32-40 samples; whip frames 25-33 %
  at 6-12 samples; colour previews 45 % at 16. One Blender at a time.

## 5. Menus (`ui.py`, `ui4.py`, `toast.py`)
- Fonts by measurement against the capture (GTA 6: Lexend for rows and status, Oswald 600 at 94 % width for
  condensed capitals). Size from the original's capital height, same left edge and baseline.
- **Build lists per state** (`ui.Menu`): clean list background, rows, the highlight bar (its transparency measured
  from the same row with and without it), the game's marker on bought rows, counter. Tab bar highlight with
  `ui4.set_tab`.
- **Option screens** all get the same furniture: title, price row, item name, counter, status line ("Applied" lifted
  as glyphs), stats panel, car tag, wallet. Check each screen against the others (user: "the front bumper is also
  missing the stats bar").
- Blocks that sit over the car go on as an **alpha layer** after the car; opaque panels are pasted after the car;
  list and title before it.
- **Names.** The game's own screens keep the game's titles. The client's items follow the client's wording. A game
  label that would mislead a viewer is moved, not kept (GTA 6 files its lowered suspension under "Wheel Kits";
  user: "Wheel Kits is not suspension"): put the item on the tab where it belongs and say so.
- **Numbers.** Client parts at the catalogue price of the variant shown (painted parts cost the painted price).
  Screens for things the client does not sell keep the game's prices and stat changes. The wallet is drawn per
  frame and counts down at each purchase; start it at the total. Client parts get a badge in the game's badge style.
- **Colour picker.** The game's "Recommended" tab with the car's factory colours as swatches, six visible with the
  scroll bar and counter; run the cursor through all of them with the car previewing each. Force swatch alpha.
- **Pop-ups are drawn, not cut out** (`toast.py`): a cut-out's mask keeps the capture's background inside the
  letters (user: "still isn't masked correctly").

## 6. Timeline (`compose4.py`)
- Every screen is entered and left the way the game does it (user: "it's skipping steps", "skips the navigation to
  the paint section entirely"): list > select > camera to the screen > buy > back > camera to the list with the row
  marked > cursor or tab > select. Plan this from the first cut; it is most of the running time.
- A purchase follows the capture's own: sound, the part and "Applied" 0.1 s later, pop-up 0.3 s later.
- Parts are bought and stay on. Previewing is not buying (user: they "need to actually be combined").
- **Never ping-pong a stretch of capture**: anything moving in the plate runs backwards (user: "the car in the
  background is going back and forth"). Forward frames, or freeze one frame.
- Partial re-render: `START` / `END` / `OUTNAME` (and `WRITE_JSON=1` when the timeline changed), then splice with
  ffmpeg and check the frame count and a few frames against the previous composite.

## 7. Whips
- Synthetic for every view change: the two held frames slide and cross-fade under a long horizontal blur, our car
  rendered from orbit cameras between the two views (`whipcams.py`) with the same blur.
- **Only lettering may stay sharp** (user: "screen tear"). Blur frames with the list removed; hold
  `|frame - blank frame|` for the list and a tight title box for option screens. Never hold a rectangle that
  reaches into the car or the scenery. Look at one frame of every whip at delivery size.

## 8. Sound (`assemble4.py`)
- Bed: room tone from a stretch between two ticks, looped with equal-power crossfades, about -43 dB.
- Ticks from the capture for row, tab, select, back, colour step; lay one wherever the edit does something.
- **Purchase sound: look before you reuse it.** The GTA 6 clip had the mechanic's line starting 0.25 s in and it
  played on every purchase (user: "the repeating 'need anything else' is annoying"). A game voice is positional
  (louder in one channel) and has no highs; UI chimes are centred and bright. Compare 300-3000 Hz against 5-12 kHz
  and left against right in 50 ms steps. Use the chime up to the voice, then only its highs; verify the speech
  band is back at room tone after each purchase in the output.
- A spoken line plays **once**, where the story puts it, with a subtitle. Never the same line twice.
- **Radio / music from the user** (`radio_bed`): one unbroken piece under the whole shop section, starting where the
  music starts, band-limited (180 Hz - 4.2 kHz), narrowed, short room tail, 8 dB under the purchase sound, dipped
  under the spoken line, faded on its own ending. Keep the shop section shorter than the clip. Say that it is a
  commercial song or someone else's recording when it is.
- One fixed gain. I cannot hear: report levels as measured and say so.

## 9. Ending
- The exit shot in the shop without UI, the line, then the client's end card.
- **End card**: ask whether the user has the exact background. If they send one, use it as sent (scaled, not
  redrawn) with the wordmark in white. Drawn substitutes took three rounds and were then replaced.
- **No orbit on black** (user: "I wanted the environment"). An orbit inside the game's shop cannot be built from
  menu captures: SfM on a 6.5 minute capture joined 9 of 20 views with a few hundred points. Offer a walk-round on
  the game's own cameras instead.

## 10. Check before every send (all at delivery size, not on contact sheets)
1. One frame per purchase: part visible and in frame, background beside the car, pop-up, wallet figure.
2. One frame per whip: nothing sharp but lettering.
3. Every screen's title, price, names and panel against the others and against the capture.
4. Frame count and audio event list printed from the timeline; speech band after each purchase.
5. The named thing in the feedback first. "The purchased sections come out poorly" was the pop-up's mask; I fixed
   backgrounds for a round before zooming in on the pop-up.

## 11. A second car in the same shop (`projects/gta6-integra/`, Integra DE4, 2026-11-20)
Reusing a finished reel for another car is mostly a data change, but these needed work:
- **Check inputs first, all of them.** Site repo (GLB, catalogue, wordmark, wheel generator), Dropbox (captures, radio,
  end-card background). If the site repo cannot be attached: car GLBs are also in the Drive bundle named in `cars.yaml`;
  catalogue list prices are the store's compare-at prices (Shopify connector; the plain price may be a sale price);
  the wheel can be rebuilt from the Drive scan with `tools/wheel_build.py`. The wordmark has no second source: no end card.
- **Cameras carry over only if the cars match in size** (Civic sedan and Integra: within 5 cm). Overlay every view anyway.
- **Each part still needs a view that shows it.** `tools/sil.py` projects the car's triangles (dumped once with
  `tools/dump_mesh.py`) without Blender; a random search over camera position, heading and pitch that scores uncovered
  game-car area, the part's box in frame and clear of the menu, and car size finds a camera in minutes. Constrain the
  car to stay in frame or the search covers the game's car by moving absurdly close.
- **A part can hide under the menu.** The Civic's exhaust camera put the Integra's rear spats under the option block.
- **Glass.** Renders leave glass semi-transparent; through it the plate showed the game's car. Fill enclosed
  non-opaque regions of the render with a dark neutral before compositing.
- **The painted panorama mirrors as flat blocks** in glass seen from a new direction. Soften it and desaturate the
  offending block for that view (`rig_shop_soft.json`).
- **The fill must never sample the menu** (mirrored lettering beside the car) and its last-resort inpaint pulls in the
  game car's colour from under our car: block UI rectangles; use `short=True` only where a hole touches the frame edge.
- **A title that sits on the game's car** gets wiped by the plate: lay its lettering on again after the car.
- **Respray contrast.** Check the first and last colour side by side in the shop light before rendering everything:
  white to a mid grey was nearly invisible; the entrance colour was changed after 20 stills.
- **Length.** Nine purchases with full navigation take 28 s at the shortest readable holds; the radio clip that fitted
  seven is too short. Ask for a longer clip rather than cutting or looping it.

## What the user must be told
Whose footage and music it is; which numbers are the game's; what was invented (background patches, navigation
shortcuts, a row added to a game list); that sound was set by measurement; anything that reads "true to the game"
but is not.

## Second car in the same shop (MR2 Spyder, `projects/gta6-mr2-spyder/`, 2026-11-20)
The Civic reel rebuilt for another kit in one pass. Start from that project's `tools/` (they take the part list from one table,
`ui4.PARTS`, and the render states from `renders.py`); what changed and why:
- **Budget the length first.** Each part costs about 2.9 s with full navigation (whip, 1.8 s screen, whip, list beat). Eight parts plus
  respray, suspension and wheels is 37 s. A music clip shorter than that cannot cover the section unbroken: tell the user before building.
- **A smaller car needs wider masks, not just closer cameras.** `tools/camsearch.py` moves the camera until our car covers the game's,
  with a cost for zooming further than needed (without it the search fills the frame). `tools/silh.py` projects the GLB without Blender
  (geometry from `export_geo.py`), so a search is seconds. What our car still leaves uncovered was 1-9 % of the frame here.
- **Masks from paint differences miss what does not change** (chrome bumper, wheels, anything under the menu list). Look at every plate
  (`$W/v3/plate4_*.jpg`) and one frame per purchase before the full composite, not after.
- Plate fills: never sample UI panels (block them); when the mirror point lands on something blocked, take the pixel just outside
  (`fill_nearest(..., extend=True)`); a wet floor carries the game car's colour around it, so desaturate the fill there.
- **Title and option block as layers over the car** on every part screen (a wide tail reaches the title corner; the car's shadow dims
  a pasted block). The game's badge sits above the block rectangle the Civic reel pasted: check the badge is there.
- `FRAMES=72,416,...` in `compose4.py` composites only those frames (about 3 minutes instead of 19): use it after every fix.
- Held ranges per camera are in `clips.md`; play them forward and then hold the last frame (`fw`), never back and forth.
- Return whips can play the outward renders backwards unless the car changed visibly in between (roof, wheels, colour).
- **Wheel rebuild**: the generator simplifies the whole scan to its third argument first (default 30,000), so pass a target:
  `RIM_TRIS=160000 TYRE=scan TYRE_TRIS=160000 blender -b -P .../te37_wheel.py -- <stl> <out.glb> 400000`. Needs `fast_simplification`
  in Blender's own Python.
- A price that is only a deposit is shown as such (second badge beside the client's); a part the model lacks is left out and declared.
- Lore names: the maker's GTA counterpart is usually official; the model often has none. Say which half is official.
