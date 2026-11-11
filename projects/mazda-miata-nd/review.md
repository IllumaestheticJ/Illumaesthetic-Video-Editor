# Mazda Miata ND scan reel - self-review (v3, delivered)

File: `/home/user/media/work/miata/out/miata_nd_v3.mp4` - 1080x1920, 30 fps, 29.5 s (885 frames), h264 yuv420p + AAC, faststart.
v3 = the user's v2 brief + addendum (relayed by the parent session). Scene order from the scene-director agent
(`direction.md`, `director.md`). v1 review: `review_v1.md` (file miata_nd_v2.mp4 was v1 with an s7 fix).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, front 3/4, moving from frame 1 (car 10-91 % of the width); first cut on the first kick at 2.07 s |
| 2 | Beat sync | 4 | Cuts on even kicks, measured against the decoded audio's broadband onset: -11..+13 ms on clear onsets (one -23 ms); later cuts sit in a dense section where the onset rise is only x1.5-2 (measurement noise -36..-62 ms). Parts lock on the last hit (frame 807) |
| 3 | 1:1 match | n/a | Scan-only reel |
| 4 | Scan quality | 4 | Plate flattened; jack stands dropped; hood/trunk panels are single skin (cameras keep away from their undersides); mirror cap shows small dark patches; hood speckle visible in the engine-bay shot |
| 5 | Story | 4 | Front (lamp -> bumper off + crash beam -> hood to captured open pose -> wheel) -> side (mirror mount, skirt) -> rear (bumper off + exhaust/structure -> trunk to captured pose) -> progressive explode (front angle, rear angle) -> reassembly on the last hit -> fade -> small logo. Each section once; no repeated view |
| 6 | Grade | 5 | House silver; no lighting dropouts (per-frame mean luma scanned for every render folder) |
| 7 | Text | 4 | 4 factual labels, bumper-removed sections only, 80 px inside the edges, above the car. 'ENGINE BAY' dropped: no clear area off the car. 'REAR CRASH BAR' not used: not clearly readable behind the exhaust |
| 8 | Ending | 5 | Reassembly locks on the last hit, fades to black, 300 px logo over the decay |
| 9 | Technical | 5 | Exact frame counts (concat assembler), no frozen frames at cuts (only eased-start frames and a planned 0.27 s pause on the bumper's inner face) |

## Changed from v1 (why)
- Opener re-framed to the whole car (v1 cropped). s1/s2 duplicate turntables, s7 top-down rotation and the all-at-once s8 explode cut.
- Bumper-off sections are the hero beats: the part turns its scanned inner face to the lens in clear black, then the camera pushes in on what's behind it.
- Hood and trunk open only to their registered captured poses ('Bumper Off Hood Open', 'Rear End Trunk Open Bumper Removed'). No door.
- Explode is progressive over two tight angles, then reassembly. Parts translate; only the bumpers (scanned inside) and the right mirror (scanned mount plate) turn.
- Cut grid moved 31.8 ms earlier onto the broadband kick onset.

## Open for the reviewer
- The bumpers exit through the bottom of frame while the camera pushes in (moving, not parked) - say if you'd rather they leave sideways.
- Right side only for the mirror/skirt (the skirt state scan exists for the right side only).
