# Porsche Macan (Electric) - self-review, v3

Output: `/home/user/media/work/macan/out/porsche_macan_v3.mp4` (1080x1920, 30 fps, 33.57 s, h264 yuv420p + AAC).
User v3 ask: "Hide/Blur/remove the rear plate, show the interior and exploded views". An explicit per-reel request,
so it overrides the IS300-only plate default.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Unchanged from v2: the whole car arcs from frame 1 and fades up with the quiet intro. |
| 2 | Beat sync | 5 | `tools/cutcheck.py` on the decoded v3 mp4: all 8 cuts land -4.6 to +15.6 ms from their onsets (max under half a frame). |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 4 | Rear plate flattened (`tools/deplate.py`) on the car and the rear bumper scan. The plate travels with the bumper when it comes off (build.py), so nothing floats behind it. Seats and bench are registered from their own scans in the same levelled frame (cabin fills the door openings; doors-closed vs doors-open interior 1.4 mm). The car's own seat skin within 25 mm is cut, and only new cabin geometry is added (`tools/build_int.py`). |
| 5 | Story | 5 | Front -> side -> rear, now with the interior: on the side shot the left doors come off and park up, then the driver seat and the rear bench slide out to camera, one after its own door. The reel ends on a full exploded view with every panel, door, bumper, seat and bench out, which locks home on the kick before the logo. |
| 6 | Grade | n/a | No IRL footage. |
| 7 | Text | 4 | 5 factual labels, no numbers: FRONT BUMPER REMOVED, CRASH BEAM, INTERIOR, REAR BUMPER REMOVED, MOUNTING POINTS. INTERIOR first sat over the seat base at y 0.70; moved to 0.80 after checking frames 735-760. |
| 8 | Ending | 4 | X3 exploded -> lock on 30.54 -> fade -> logo over the pad tail. User: logo too small at 320 px; rebuilt at 720 px (the size lessons.md already set). |
| 9 | Technical | 5 | Per-frame luma on S1v3/R1v3/X3 finals: no dropouts. Frames +-1 at every cut inspected: no black or duplicate frames. |

## Director pass
Same two repeat flags as v2 (F1/R1v3, F2/S1v3, IoU 0.70-0.77), kept for the same reason: different sections and parts.
F1's 0.8 s hold is the landing before the drop.

## What I'd do differently
- Grep lessons.md for every element before following a plan's size: the plan said ~320 px logo, the lesson says 720 px.
- Check label positions against the parts' paths before the HUD render: the seats come out low in frame, into the
  label band used by the bumper shots.
- regcheck.py against a 3M-point shell without `distance_upper_bound` ran 19+ min; always bound the query.

---

# Porsche Macan (Electric) - self-review, v2

Output: `/home/user/media/work/macan/out/porsche_macan_v2.mp4` (1080x1920, 30 fps, 33.57 s, h264 yuv420p + AAC).
Brief: Temerario-style scan reel, plus the user's V2 rules (relayed by the parent session) and the V2 addendum
(cropping, one sequence per section, bumper-removed hero beats with factual labels, no faked openings).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | The whole car arcs from frame 1 (linear 18 deg sweep after the director flagged an easeout opener as 2.4 s static). It fades up over 1.2 s with the track's quiet intro, so the first ~0.5 s is dark. |
| 2 | Beat sync | 5 | `tools/cutcheck.py` on the decoded mp4 (1 ms RMS, local half-rise): the 8 music cuts land -4.6 to +15.6 ms from their onsets (4.10, 8.17, 9.70, 16.30 drop, 20.37, 24.43, 25.47, 28.50). The logo enters at 30.53 out of black on the first missing kick (the groove stops), so it has no onset by design. |
| 3 | 1:1 match | n/a | Scan-only reel, no IRL footage. |
| 4 | Scan quality | 4 | Silver on black, ground removed. The rear plate is kept as scanned: the user rule says flatten only on the IS300, so the earlier deplate was reverted and R1 re-rendered. Every part is registered to the car (1.2-4.4 mm median) and checked in colour-over-grey renders. The warped front bumper scan (4.4 mm) and the rear speckle up close are visible on R1's push-in. |
| 5 | Story | 4 | One pass front -> side -> rear: whole car, face, wheel, hood opens on its fitted hinge into the bay, front bumper off (inside shown, then crash beam), left fender + doors with cards to camera, light bar, hatch open + rear bumper off (crash beam + mounts), then reassembly and a small logo. Every open/removed state comes from a registered state scan. |
| 6 | Grade | n/a | No IRL footage. |
| 7 | Text | 4 | 4 labels, only over the two bumper-removed hero shots (addendum C overrides "no text" and the rubric's 2-item limit): FRONT BUMPER REMOVED, CRASH BEAM, REAR BUMPER REMOVED, MOUNTING POINTS. They name what the state scans show; no numbers. They sit at y 0.70 on black, below the scan, legible at phone size. |
| 8 | Ending | 4 | Parts lock home on 29.51, fade to black, then a small (360 px) logo over the pad tail; the music fades out 0.8 s at the end. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC. Per-frame luma check on every render: no dropouts (persistent data off when parts animate). No black or duplicate frames at the cuts (frames +-1 inspected). |

## Director pass (`ive director`)
- Every clip is tagged `section:` / `focus:`.
- Repeats flagged and kept: F1/R1 and F2/S1 (silhouette IoU 0.70-0.76). F1 is the front with the hood open and R1 the rear with the hatch open; F2 is the front end and S1 the left side. Different sections and parts, not a reused shot.
- F1 has a 0.8 s hold on the open bay: it is the push-in landing before the drop.

## What I'd do differently
- Check every shot's first/last frames for parked parts before queueing finals. In a portrait frame at 28-30 mm, a part 2.6 m up is still in shot. S1 and R1 each cost a re-render (~27 min).
- Use a linear (or ease-in-out) arc for the opener from the start; easeout reads as a still once the director measures it.
- s3_wheel and s4_lightbar are v1 renders reused in their v2 slots; they fit the section order but are the most "v1" moments.
