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
