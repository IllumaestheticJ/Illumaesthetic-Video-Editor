# Nissan Frontier Pro-4X scan reel v2 - self-review (training/rubric.md). v1: review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v2.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC 320k, 38.37 s,
1151 frames, cut-only assembly with exact frame counts (no duplicated frame at cuts).
Changes vs v1: user note "highlight and label each unique scan section" + all-reels v2 brief/addendum A-D. Order from the
scene-director/director agents (direction.md, director.md): whole truck -> GRILLE -> FRONT BUMPER (off on the drop, turns to
show its scanned inside) -> FRONT BUMPER REMOVED (hero push-in) -> HOOD (lifts off; no hood-open scan, so no hinge) ->
FRONT STRUCTURE -> FENDER FLARES -> parts home one per beat -> FULL TRUCK -> fade -> small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole truck in frame, orbit moving from frame 1; first part action is the drop at 9.66 |
| 2 | Beat sync | 5 | Cuts vs broadband onsets of the delivered audio (cutcheck.py): -15.1/+9.9/+7.8/-5.1/+0.4/-10.0/-14.6 ms (all < 1/2 frame); parts land on measured onsets |
| 3 | 1:1 match | n/a | scan-only brief |
| 4 | Scan quality | 4 | Each section shown once, its own shot; bumper re-cut so it no longer carries a duplicate grille; no wheels (lift) and hood underside is the outer shell only |
| 5 | Story | 5 | Travels front -> side -> rear; every removal backed by a registered state scan; bumper-removed state is the hero beat with label |
| 6 | Grade | 4 | Silver -0.5 EV; per-frame luma clean in every render (lumacheck.py), persistent data off where parts move |
| 7 | Text | 4 | One label at a time, names + section index only, dark plate for legibility; S6 label sits over the cab (plate keeps it readable) |
| 8 | Ending | 5 | Parts home on the crash/accents, FULL TRUCK, 0.6 s fade, small logo riding the track's tail |
| 9 | Technical | 5 | Spec correct, no dup frames, first/mid/last sheets of every shot checked |

Known gaps: parked bumper partly clipped at the lower-right edge in S5; S7 crops the bed (section shot on the arches).
Labels claim only section names; FRONT BUMPER REMOVED sub = STATE SCAN. "CRASH BEAM" etc. not used (not provable from the render).
