# Mazda Miata NC scan reel - sources

Scan only (no IRL footage, no text). Engineering Drive folder `Mazda Miata NC` (117x9LQvHdB1J88dcs8H8bagCL9DTstfK),
listed recursively with the service account. Media in `/home/user/media/mazda-miata-nc/` (not in git).

| File (Drive id) | Used as | Notes |
|---|---|---|
| NC Miata Full Car.stl (1KnzXa391W0DCdSqmQe3i2IZEjGv17CLe, 2026-10-23, 15.0M tris) | base car | PRHT hardtop, aftermarket wheels; no ground scanned. Decimated 4 mm (full-car shots) and 3 mm (close-ups) |
| NC Miata Bumper only.stl (1LAwZsiIJwyL_-aGAqISgfvIO92hZRjek, 2026-07-30) | exploded bumper | inside + outside surfaces; z-fights with the car bumper at identity |
| NC Miata Front Bumper Off (Hood Closed).stl (1LGmOpWaPGVPgkBQeO-CQVBrkv7Qb9vTA) | crash structure fill | identity in the car frame (ICP p50 1.6 mm before, ICP makes it worse) |
| NC Miata Front Bumper Off (Hood Open).stl (1LEcwaAX2bw1A2R7UVCijIH1goBo3o1xu) | engine-bay fill | same frame as hood-closed; does NOT contain the propped hood (no hinge fit possible) |
| NC Miata Hood and Bumper Removed.stl (14pdKFLPBAi85irxIP_SEdkENY-faE_YR) | engine-bay fill | car on stands, wheels drooped and jack stands: fills limited to the hood/bumper footprint, z > 0.23 m |
| NC miata Trunk Closed.stl (1SBIgwTCnzHs0_vu8asYwUYqsJXtGmI0p, 2023-09-30) | registration of the 2023 set | own frame -> FPFH+RANSAC+ICP onto the car (projects/a90-supra/tools/globalreg.py): same pose 4/4, rmse 4.4 mm |
| NC miata Trunk Open.stl (1SBOVXhoxskECittHLRLLp7LYDbD3srVK, 2023-09-30) | trunk interior + lid hinge | in trunk-closed's frame (p50 2.4 mm at identity) |

Not used: `NC Miata NC3 Body.stl` (no states), `Bumper Scan (epsilon)/Bumper Scan.stl` (separate product scan),
`Trunk Closed.stl` (2023-10, duplicate state), `nc fender scoop/*` and `Headlight Project/*` (product/CAD work).

Frame: tools/level.py (XY-PCA yaw so nose = -Y, tilt from the four tyre contact points) applied to every scan, then
`ive crop` and `ive prep --like prep/car4.json`. Prepped extents 3.99 x 1.86 (2.0 with mirrors) x 1.18 m.
Registration checks: `/home/user/media/work/miata/reg/sheet*.jpg` (colour part over silver car).

Panels: hood = raw-scan seam outline (tools/seammap.py -> polycut.py); trunk lid = tools/extract.py (absent in Trunk Open);
lid hinge tools/hinge.py (74.3 deg, median 1.0 mm). Composites (tools/fill.py): comp_hood, comp_trunk, comp_explode.

Music: `/home/user/media/work/music/mazda-miata-nc_track.mp3`, generated for this reel by the parent session (not in git).
Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com/cdn/shop/files/ (the homepage is behind a bot check;
the CDN path works) -> `remotion/public/illumaesthetic_logo.png` (gitignored).
