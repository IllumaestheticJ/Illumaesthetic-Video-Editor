# Lamborghini Revuelto scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/lamborghini_revuelto_v2.mp4` — 1080x1920, 30 fps, 34.60 s (1038 frames), h264 yuv420p + AAC.
v1: review_v1.md / project_v1.yaml. v2 applies the all-reels rules A-D that landed in lessons.md while v1 rendered, with the
scene order from the scene-director agent (direction.md).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Whole car (front-left 3/4) pushing in from frame 0 under the track's quiet intro; first transformation at 7 s (bumper off). The music has no hit before ~7 s to land an earlier event on. |
| 2 | Beat sync | 5 | Measured on the delivered file's decoded audio: cuts within -59..+17 ms of onsets (the -59 ms one is in the quiet intro), logo cut 30.400 vs taiko attack 30.398, parts land 27.967 vs climax attack 27.931 (+1 frame). Exact-frame concat: no duplicated or frozen frame at any cut. |
| 3 | 1:1 match | n/a | Scan-only format. |
| 4 | Scan quality | 4 | Registered parts (1.5-2.6 mm), plate flattened, mirror crop and lid pinholes fixed. The state-scan structure is real but ragged at its edges; sparse white specks under the open lid (scan noise); dark intake trims weren't captured. |
| 5 | Story | 5 | One continuous sequence per section, travelling front -> left side -> rear (rule B): opener, front opens, move-in on the front structure, side panels, rear (richest: wing, tail lights, rear bumper) with move-in on phrase C, everything slams home on the climax, logo. Only openings with scan data (rule D): mirror never moves, the lid only swings on its fitted hinge. |
| 6 | Grade | 4 | AgX -0.5 EV silver on black, consistent. |
| 7 | Text | 4 | Four labels, max one on screen, only over the two bumper-removed holds, in clear black below the subject; counts from the STL headers, components named after looking at the renders. The original brief said "no text"; the newer all-reels rule C asks for these (flag for the user). |
| 8 | Ending | 5 | Small 320 px logo on the loudest taiko hit, rides the decay; audio fades to -56 dB at 34.6 s. |
| 9 | Technical | 5 | Spec met; per-frame luma scan of every render: no lighting dropouts. |

## Known weaknesses
- v2_side holds still for 0.33 s (frames 488-497) between the fender and the skirts; the parked front bumper peeks in
  at the top-left of that shot's first frames.
- s6 (reused from v1) is stretched 3.5 % (src_fps 14.59) to fill its slot.
- s6 -> v2_frontin is a continuous move with no visible cut at 10.47 s (same pose, by design).
