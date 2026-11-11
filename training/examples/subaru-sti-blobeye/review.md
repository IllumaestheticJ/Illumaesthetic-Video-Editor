# Self-review — Subaru Impreza STI GD "blobeye" scan reel (v3 edit, file `subaru_sti_blobeye_v4.mp4`)

Deliverable: `/home/user/media/work/sti/out/subaru_sti_blobeye_v4.mp4`. 1080×1920, 30 fps, 39.23 s, scan only.

User on v2: "Same issue - a bunch of improperly cut and hallucinated scans." v2 carved the hood, bumper, wing and skirt out of
the full-car scan (ragged edges), flew them off the car (no scan shows that) and filled the openings with patchworks of state
scans. v3 shows ONE scan file per shot, exactly as captured. A "removal" is a hard cut on a kick, mid camera move, from the
full-car scan to the registered scan of that state, rendered alone.

Order: whole-car rear 3/4 orbit → push in on the wing → wing end plate / tail light → wheel → headlight to scoop → push over
the hood → **cut to the engine-bay scan** → low push on the bumper → **cut to "bumper removed" scan (label)** → **cut to "all
removed" scan (label)** → whole car front 3/4, fade → small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, moving from frame 1. The first state swap comes late (13.2 s). |
| 2 | Beat sync | 5 | All 11 cuts measured on the decoded audio of the delivered file: 12–15 ms before a kick attack (half a frame is 16.7 ms). |
| 3 | 1:1 match | n/a | No IRL footage. The three state swaps share the camera across the cut (last key of x_a = first key of x_b). |
| 4 | Scan quality | 3 | Nothing carved or composited. The state scans are partial captures with their own holes and frayed capture edges (engine-bay top edge, grille and cowl gaps in the full car, the sparse "all removed" scan). These are the data, not edits. |
| 5 | Story | 3 | Honest but simpler: tour of the car, then what is under the hood and bumper. No exploded view or reassembly (no separated-part scans exist). |
| 6 | Grade | 5 | One look, AgX −0.5 EV. Every new shot passed the luma dropout check (min/neighbour ≥ 0.85). |
| 7 | Text | 5 | Two labels, only on the bumper-off state scans, on black below the subject, no numbers. |
| 8 | Ending | 4 | 0.77 s fade on the closing turntable, 280 px logo through the final hit. |
| 9 | Technical | 4 | yuv420p, AAC, faststart. Repeated frames only at cuts (1–2 frame holds). |

## Director report
- `B_b ~ B_c` (IoU 0.91, same section): intended. Same camera, two different scans (bumper off → bumper and hood off).
- `light ~ H_a` (IoU 0.75): both show hood and scoop. The light shot ends on the scoop and H_a starts wide on it. A real overlap; kept because H_a is the lead-in the engine-bay swap needs.
- One more cross-section silhouette match (front vs rear), a false positive as in v2.

## Not shown, and why
- `Rear Wing data` (rear captured with the wing off): rendered and dropped. Its capture edge is a ragged staircase across the rear window with a hole in the tail light at every framing.
- `Sideskirt removed`: a thin strip that cannot fill a vertical frame.
- `hood removed`: scattered islands.
- Exploded view / reassembly from the original brief: would need carved panels, which is what the user rejected.

## Known weaknesses
- `B_c` ("all removed") is sparse and fills only the upper-middle of the frame for 4.8 s.
- The engine-bay first frame shows black corners where the capture ends.
- The engine-bay scan comes from another session (a lip/splitter is present).
