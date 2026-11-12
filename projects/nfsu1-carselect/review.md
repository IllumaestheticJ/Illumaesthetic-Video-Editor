# NFSU1 car-select reel v1 - self-review (2026-11-11)

Output: `/home/user/media/work/out/nfsu1-carselect_v1.mp4`, 1080x1920, 30 fps, 21.8 s, H.264 + AAC. Four cars
(GR Corolla Castrol, NA Miata #58, Del Sol Shaftwerks, FR-S green); the Elise is waiting for a model.
The scan-video rubric only partly applies (no scan, no 1:1 cut, no logo card); scored where it does.

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 5 | first frame: the Castrol Corolla driving at the lens with its lights on, under SELECT CAR |
| 2 | Cut timing | 4 | every drive-in is on the game's own hard cut and every drive-away on the game's "next" in one unbroken stretch of the capture's audio; not checked by ear |
| 3 | Car match | 4 | kit cars land on the game Miata's wheels at the hold; the track is loose for ~8 frames in the close sweep (silhouette says little there) |
| 5 | Story | 4 | reads as the game's car select with our cars; ends on the last car driving off |
| 7 | Text | 3 | Toyota/Mazda/Honda plates and logos are the game's, Scion emblem and GR COROLLA badge are real artwork; "del Sol" and "Scion FR-S" are plain type; stat bars and STYLE points are the game's own |
| 9 | Technical | 4 | 1080x1920/30/yuv420p/AAC/faststart; contact sheet and approach frames of all four cars checked, wheels straight |

Known weak points (told to the user):
- Every car passes the same stretch of garage (one tracked cycle reused).
- Music: the capture's own; "Get Low" not supplied and not confirmed in the capture.
- The game frame fills the middle 44 % of the screen.
- The "Reputation" label fades when a bright car passes under it (it is animated and not in the menu map).
- Headlight flare is the game Miata's, so it sits at Miata lamp height on the taller Corolla.
- FR-S is dark (deep green in a dim garage).
- Capture speed could not be checked against a second source.

## v2 (after user notes)
- Fixed: entry shake (camera path rebuilt with zero roll and smoothed height/distance; full re-render), wheels straight (steer 0 everywhere), player name "Mohammad" -> "Epsilon".
- Not done: "Get Low" over the reel — no audio file available here; v2 still carries the capture audio. Elise still missing (no model reachable).
- Still rough: same garage stretch per car, FR-S reads dark, "Reputation" label fades under bright cars, typeset del Sol / FR-S plates.
- Lesson: when recovering a game camera from silhouettes, constrain it (no roll, smooth height) before rendering — an unconstrained per-frame fit looks like the car shaking.

## v3
- Added EPSILON+ end card (2 s). Get Low still missing: no audio file reachable; `assemble.py video <frames> <out> <music> [start_s]` is ready for it.

## v4
- Get Low on (user's file), from 0:00, no game audio. Car screen path steadied (steady.py). Logo card kept.
- Lesson: after constraining the camera, also check the car's on-screen velocity frame by frame; the game car's suspension rock and small-size fit noise survive smoothing of the camera and read as shake on a rigid kit car.
- Not verified by ear: music start point / level; scale (distance) wobble not measured.

## v5
- Game sounds restored under Get Low (ducked in holds). Rule: keep the game car/menu sounds when adding a song.
