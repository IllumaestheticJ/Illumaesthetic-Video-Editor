# bf-miata-mr2-night-meet: draft v1 notes (2026-11-17)

User feedback on v0.1: "base video is good, but start with stock cars and then slowly modify them - make sure the sections
are actually trimmed/cropped correctly". Output: `/home/user/media/work/out/bf-miata-mr2-night-meet_v1.mp4` (28.0 s,
1080x1920/30, still preview quality: 540x960 renders at 15 fps, frames doubled).

## What changed
- **Both cars start stock** and the sale parts install one zone at a time (`tools/shot.py` ZONES; `tools/make_specs.py`).
  - MR2: stock in the lot -> 1:1 cut to the stock scan -> skirt/fender combo (scan) -> eyelids -> hood vents -> rear spats,
    then duckbill (CGI). The MR2 keeps its stock front bumper throughout (the Epsilon bumper is "No deal").
  - NC: stock in the lot -> 1:1 cut to the stock scan -> front bumper + lip + canards (scan) -> fender cuts (scan) ->
    side skirts, then rear spats (CGI).
  - Then both fully kitted scans, the sale card and the wordmark.
- **Scan sections re-cut** (`tools/cutparts.py`): a zone is the footprint of the lookbook stock piece (normal distance +
  tight lateral limit), not a 3D radius, so the edge follows the panel outline. Wheels are masked by cylinder.
- **NC front bumper from the removed-state scan** (`tools/nc_bumper_state.py`): "Front Bumper Off (Hood Closed)"
  (Drive 1LGmOpWaPGVPgkBQeO-CQVBrkv7Qb9vTA) sits in the full-car frame (1.8 mm median). Bumper = full-car nose triangles
  the state does not confirm (> 10 mm); the state's own crash-bar geometry shows once the bumper is off.
- **NC fender** (`tools/nc_fender_zone.py`): the lookbook NC body already has the fender-cut opening and no stock nose,
  so the stock fender panel and stock bumper in the CGI lot are our own scan pieces, painted.
- **Fit refined model -> scan** (`tools/refine_fit.py`): MR2 6.1 mm median, NC 2.5 mm (v0: about 15 / 9 mm).
- Check renders of every zone (tinted / removed / part seated): `tools/check_zones.py`.

## Checks
- Cuts land on the planned frames (58, 131, 180, 231, 307, 355, 433, 501, 581, 650, 763); times are attacks measured in
  the source track. Not re-measured in the final mix.
- Loudness -14.1 LUFS, true peak -1.8 dBFS.
- Contact sheet: `/home/user/media/bf-miata-mr2-night-meet/work/contact_v1.jpg`.

## Still rough
- Preview resolution and doubled frames; simple lot.
- The eyelid install is small on screen and hard to read.
- NC skirt in shot 9 flies in from the camera side and the car is tight in frame; MR2 rear shot crops the car's left edge.
- Wheels still change across each 1:1 cut (scan cars and lookbook models run different wheels).
- NC side-skirt and rear-spat zones on the scan are footprint cuts with patchy edges; they are only seen fully kitted
  (shot 10), where the parts cover them.
- Labels appear only on scan shots, so eyelids, hood vents, spats and duckbill are named only on the card.

## v1.1: safe zones (owner rule, knowledge/safe-zones.md)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.1.mp4`. Same picture and audio as v1; only text and logo moved.
- Sale card: title block moved down (was y 230, in the top/feed-crop zone), rows tightened to end at y ~1390 (were to
  ~1500, in the bottom zone), prices right-aligned at x 900 (were at 970, under the right rail).
- "FENDER CUTS" label moved from y 1380-1510 (bottom zone) to the top-left label position (y 300-440).
- Wordmark and URL centred on x 484 (the safe band's centre).
- `scripts/safezone_check.py` sheets looked at before and after: no text or logo touches red or amber in v1.1.
- Not fixed: some shots' cars extend under the right rail or outside the 4:5 feed crop (close-ups; NC fender wheel).

## v1.2: URL (owner rule, MASCOT_AND_PRICES.md 22e387c)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.2.mp4`. The end card URL now reads WWW.EPSILON.PLUS (was epsilon.plus). Nothing else changed.
Safe-zone sheet looked at: all text and the logo are clear of red and amber. -14.1 LUFS, TP -1.8 dBFS, 28.0 s.

## v1.3: per-part price labels, cars apart in the last scene (user feedback on v1.2)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.3.mp4` (28.0 s, -14.1 LUFS, TP -1.8 dBFS).
- User: "for each clip of the parts, show the text so people know what part and the pricing/saving". Every part clip,
  lot shots included (the user asked for it), now shows: part name, car · 20% OFF, was (struck) -> now, SAVE $.
  Prices from `bf_liquidation_pricing.csv` (`tools/post.py` PRICE / LABELS). Two-part shots show one label per part in
  turn (MR2 spats then duckbill; NC bumper + lip then canards; NC skirts then spats).
- Lot close-ups and the NC fender shot put the label on a soft dark plate, because the car fills the frame there.
- User: "in the last scene the cars are clipping into eachother". They were 2.2 m apart centre to centre with opposite
  yaw, so the bodies overlapped. Now staggered front/back (NC front-left, MR2 back-right, 4.4 m apart in depth) and
  framed inside the safe area.
- Safe-zone sheet looked at: all text and the logo clear of red and amber; both cars in the last scene inside the safe
  area. Close-up shots' cars still run under the right rail.

## v1.4: opening title, labels held, two labels above/below the car (user feedback on v1.3)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.4.mp4` (28.0 s, -14.1 LUFS, TP -1.8 dBFS).
- "The beginning needs a title to show the deal/platforms": shot 1 (and the first ~0.5 s of shot 2) carries
  BLACK FRIDAY / 20% OFF / MR2 SPYDER · NC MIATA / EPSILON+ FIBERGLASS AERO on a soft plate (`tools/post.py` title()).
- "Some of the text cuts away too fast": every part label enters earlier (15-30 % into its shot) and stays to the cut.
- "If there is two text you can put one above and another below": two-part shots put the first label above the car
  (y ~300) and the second below it (y ~1130-1400). Both stay to the end of the shot. Plates on every lot/close shot.
- Safe-zone sheet (every 0.5 s) looked at: all text and the logo clear of red and amber.

## v1.5: NC fender fit, longer text (user feedback on v1.4)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.5.mp4` (42.5 s, -14.0 LUFS, TP -1.8 dBFS).
- "The nc fender cuts don't line up well": the scan hole was bigger than the part (the old zone also took scan skin the
  lookbook body lacks), leaving dark slits at the door edge and under the crease. A local re-fit (`tools/nc_fender_fit.py`)
  moved the part only 2 mm, so the fix is the zone: it is now the part's own side outline rasterised at 2 mm, closed and
  filled (`tools/nc_fender_outline.py`), on the outer skin only. Check render: hole = part outline, part flush.
- "Make sure the text is a bit longer so slow readers can digest info": shots re-timed to more hits (title 3, single-part
  4, two-part 6, card 6; specs/timeline.json `units`), labels enter at 10-20 % of the shot and stay to the cut. On screen:
  single-part labels 2.6-3.0 s, two-part labels 3.8-4.6 s (first) and 2.6-3.1 s (second), opening title ~3 s, card 4.9 s.
  Two-part installs finish by ~60 % of the shot so the second label has time.
- Bug fixed: text was drawn straight onto opaque frames, so fades were ignored (labels popped on; the URL stayed while the
  wordmark faded). Text now goes on a transparent layer (`post.py` Layer).
- Length is now 42.5 s (was 28 s) because of the longer holds.

## Fonts (owner rule, knowledge/fonts.md), wired into tools/post.py for v1.6
Headlines, offers, prices, part names: Akira if `assets/fonts/akira/` has the file, else Unbounded 800/900 stand-in (Akira
not supplied yet). Small lines and the price table: Unbounded 500. URL under the wordmark: Unbounded 400. Preview stills only;
no new export yet (waiting on the length decision).

## v1.6: spats/duckbill over stock, NC spat bumper cut, TC wings + MR2 diffuser, house fonts (user feedback on v1.5)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.6.mp4` (50.7 s, -14.0 LUFS, TP -1.8 dBFS).
- "The duckbill and spats don't have a section removed, they go over stock": MR2 spats and duckbill land on the stock
  body; nothing comes off (`tools/shot.py` ZONES).
- "The NC should also have the rear spats (rear bumper needs to be cut)": the NC rear-bumper cut is the Epsilon spat's
  own outline (footprint -80/+30 mm, 3 mm lateral), so the hole matches the part.
- "...and the TC wing included": NC TC wing = engineering Drive 'NC swan short mount assm.stp' (1mrtynCDvxFzutOrOV0R7i7iEHg-r8agt;
  47.5" element, endplates, one upright mirrored), meshed per solid with OCP and placed per its drawing
  ('NC swan short mount.pdf': uprights 981 mm apart, base plates at the lid's rear edge) on our scan (`tools/nc_tcwing.py`).
  New CGI shot s09b. The lookbook NC only has a GT wing; the configurator page (epsilon.plus) is blocked from this session.
- "Same with the MR2 - include the rear diffuser (black) and the TC wing": lookbook `part_diffuser` (black) and
  `part_tc_wing_kit` (carbon) in new CGI shot s05b; both also on the final two-car scan shot.
- Diffuser and TC wings are NOT on the BF sheet: labels show the regular store price ("COMPLETE THE KIT", $750 / $1,100),
  no discount. They are not on the 20 % card.
- Fonts per knowledge/fonts.md (Unbounded stand-in for Akira). Length now 50.7 s.

## v1.7: Akira (owner licence confirmed 2026-11-18)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.7.mp4` (50.7 s, -14.0 LUFS, TP -1.8 dBFS). Composite-only change from v1.6.
- AkiraExpanded-SuperBold.otf (Drive 1nrF80enolDd9HAu5807kv5XIx0cUSDya, SHA-256 checked, gitignored, never committed) now
  sets headlines, offers, prices and part names. Unbounded 400 beside the logo, 500 for small text.
- Akira is ASCII-only: "TC WING - SWAN MOUNT" and "MR2 SPYDER + NC MIATA" replace the middle-dot versions; every Akira
  string checked against the font cmap (no missing glyphs). Akira is wider: long lines auto-shrink to the safe band (post.py fit()).
- Safe-zone sheet looked at: all text and the logo clear of red and amber.

## v1.8: spats visible and seated, 66.5" TC wings, MR2 front bumper (user feedback on v1.7)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v1.8.mp4` (50.7 s, -14.0 LUFS, TP -1.8 dBFS; safe-zone sheet looked at, all text clear). Lookbook seams measured: spats 0.1-0.7 mm, duckbill/skirts <=0.1 mm, diffuser seated on the spats.
- "The rear spats also clip through the body": v1.6 left the stock MR2 corner in place under the spats (I misread "they go
  over stock" as an instruction). Now the stock corner and duckbill pieces come off before the parts land: the lookbook stock
  pieces are hidden in CGI, and the scan uses the footprint cut. Check stills: the part seats with no clipping.
- "The rear spats dont show up in the screen": the NC spat is only a 0.1 m lip under the bumper. Side and high angles
  showed stock and kit identically (check stills). s05 and s09 now land the spats on a low (z ~0.2 m) close-up of the rear
  corner. s05 then pulls back for the duckbill.
- "The TC wing needs to be the bigger 67 inch one": both wings use the 1700 mm element (Drive 'BMS-S420C-1700mm.stp'; the
  store variant is "66.5""). `tools/wing67.py` moves the endplates out to +/-0.85 m and stretches the element; uprights
  and bases stay unchanged.
  - Labels: 'TC WING 66.5"' $1,100.
  - NC: Shopify TCW-NC-665-SM, $1,100.
  - MR2: the MR2 listing only has the 47.5" swan variant ($1,100). The 66.5" MR2 price needs owner confirmation.
- "MR2 spyder doesn't show the front bumper": the Epsilon bumper installs in s02 after the skirts. On the scan, the
  stock bumper is cut by the lookbook stock-bumper footprint. The sheet lists it as "No deal - out of stock", so the label
  shows the $900 regular price ("COMPLETE THE KIT") and it is not on the 20% card.

## v1.9 (dropped)
- A 67.9 s re-time with 3.2 s+ label holds was approved and started rendering. The owner then revised the text rule
  (prices 2.2 s, 1-3 words 1.8 s + 0.3 s per word; "a bit too slow" before), and the user chose to keep v1.8. Reverted.
- **On the next change:** retime only the labels below 2.2 s in v1.8:
  - s02 MR2 bumper 1.24 s
  - s07 canards 1.69 s
  - s05b MR2 wing 1.88 s
  - s09 NC spats 1.92 s
  - s05 duckbill 2.04 s
  - s08 fender 2.14 s
- The v1.8 shot renders were deleted when v1.9 started. The v1.8 mp4 is intact. A v1.9-style fixed 10-frame label fade
  (instead of 20% of the shot) alone lifts most of these.

## v2.0: trimmed MR2 bumper cut, uncut MR2 rear, MR2 47.5" wing, NC tall stands, in-frame swaps (user feedback on v1.8)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v2.0.mp4` (55.6 s, -14.0 LUFS, TP -1.8 dBFS; safe-zone sheet looked at, all text clear).
- "The front bumper swap removes too much material on the MR2 Spyder": the stock-footprint cut also took a strip above the
  Epsilon bumper, leaving a black gap. `tools/mr2_bumper_cover.py` keeps on the car every cut triangle the part does not
  cover (front/side silhouette test). Check render: the part sits flush under the hood.
- "The rear bumper should not be getting cut on the MR2 - same with duckbill": nothing slides off. The stock patch under
  each part is hidden only on the frame the part seats, so it cannot poke through (`shot.py` OVER).
- "The TC wing is too wide on the MR2": back to the lookbook 47.5" wing; label "TC WING" $1,100 (store TCW-MR2-475-SM).
- "Use the taller wing stands for the NC": Drive 'NC swan tall mount assm.stp' (1rhb9tnkC7M8k-BDyJE3pH7WcxKoX10Nl). It carries
  the real 1700 mm element and endplates, so `wing67.py` is no longer used.
- "Focus on the bumper on the Spyder and the side skirt on the NC when it gets removed/readded - currently off-frame":
  s02 moves to the nose and holds while the bumper lifts off and the new one slides in; s09 holds a low side view on the
  skirt until it lands, then drops to the spat corner.
- Labels retimed to the owner minimums (prices 2.2 s): every price is readable 2.4 s or more. Cuts sit on hi-hat attacks.
- All 12 shots re-rendered (the v1.8 renders were gone). Per-shot frames are on the shared drive (frames_sXX).

## v2.1: MR2 bumper swap from the bumper-removed scan (user feedback on v2.0)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v2.1.mp4` (55.6 s, -14.0 LUFS, TP -1.8 dBFS; safe-zone sheet looked at).
- "MR2 Spyder needs the front bumper scan to transition to the 'bumper removed scan' for a clean cut - still looks odd":
  the bumper zone now comes from the engineering scan 'Front Bumper Data/hood closed no bumper.stl'
  (1Id9y9SVLsgm4Ta4EJRfC4smGDkmshsQU), the same way the NC bumper does (`tools/mr2_bumper_state.py`).
  - Registration: Open3D FPFH + RANSAC, then point-to-plane ICP onto the full-car scan; 2.6 mm RMSE on the shared surfaces.
    A hand-rolled ICP grid search did not converge (only ~40 % of that scan overlaps the full car).
  - Zone = full-car nose triangles the bumper-off scan does not confirm, gated to within 60 mm of the lookbook stock bumper.
  - With the bumper off, the scan's real crash bar, radiators and supports show. `mr2_bumper_cover.py` is no longer used.
- Only s02 and s10 were re-rendered. Timing, labels and all other shots are v2.0.

## v2.2: all game-model shots, spat clipping fix, flipped s05 cards (user feedback on v2.1)
`/home/user/media/work/out/bf-miata-mr2-night-meet_v2.2.mp4` (55.6 s, -14.0 LUFS, TP -1.8 dBFS; safe-zone sheet looked at).
- "Can this be done entirely on game models? ... cutting back and forth between game/scan feels unnecessary": every shot
  is now the lookbook model in the night lot (s02, s07, s08, s10 were scan-look). No silver scan shots and no CGI -> scan cut.
  Scan data only supplies what the lookbook lacks:
  - the NC stock nose and fender that come off (scan pieces, painted);
  - what sits behind both bumpers (`dec/*_under_bumper.stl` from the bumper-off scans, dark metal);
  - the NC TC wing placement.
- "There's still too much cut out / bumper gap - line it up cleaner": the Epsilon bumper now seats on the lookbook body it
  was designed on; test frames show no gap on either car.
- "The rear spats still clip through the bumper": frames showed blotches where the stock surface coincides with the
  spat, and a notch at the arch when the stock corner was hidden. Now the stock corner stays, and its vertices within
  12 mm of the part tuck 10 mm inward once the part seats (`shot.py` inset_under). Same for the duckbill. The small step
  left at the arch is the part's own shape.
- "Flip the rear spat and duckbill title cards": in s05 the duckbill card is above the car and the spats card below.
- s10 is a low front view of both kitted cars in the lot. Re-rendered: s02, s05, s05b, s07, s08, s10.

## v2.3 (58.9 s)
- New shot s04b (4 units, after the hood vents): the MR2 hardtop lands on the open car, high front 3/4 view. The hardtop stays on in s05, s05b and s10.
- Hardtop label: "HARDTOP / MR2 SPYDER · PREORDER OPEN", no price. The store lists only a $50 non-refundable preorder deposit (Shopify, 2026-11-20), which would read as the price.
- MR2 rear spats moved 8 mm outward and 8 mm rearward; the bumper surface under them is inset 10 mm once they seat (body and stock). Checked on full-size s05 frames: no bumper showing through.
- Re-rendered s04b, s05, s05b, s06, s08, s10. Audio -14.0 LUFS, TP -1.8 dBFS. Safe-zone sheet looked at: all text inside.
