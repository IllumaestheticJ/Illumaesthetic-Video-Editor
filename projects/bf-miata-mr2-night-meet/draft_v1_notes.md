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
