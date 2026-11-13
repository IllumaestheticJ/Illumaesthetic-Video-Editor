# Honda Civic FE1 — Epsilon kit reel v5 (complete reshoot) — agent self-review (training/rubric.md)

Output: `/home/user/media/work/civic/out/civic_fe1_epsilon_v5.mp4` — 1080×1920, 30 fps, h264/AAC, 748 frames = 24.93 s.
v5 answers the user's v4 note: "all the parts are placed on incorrectly/inaccurately, and the cutting/organizaiton is a mess -
please have a separate agent plan out the shots and then reshoot everything". Plan: `director_v5.md` (director agent).
Earlier reviews: `review_v4.md`, `review_v3.md`.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole car from above, moving from frame 1; doors open ON the drop at 1.27 s |
| 2 | Beat sync | 4 | cut 1 measured +10 ms on the decoded audio; cut 2 (the 1:1 hand-over) sits on frame 634 = 33.161 by construction (the frame-diff detector does not see it because the two pictures match). Part seats are keyed to the hits (lip 17.851, skirts 19.923, apron 23.227, wheels 26.521, wing 29.847) but not measured individually |
| 3 | 1:1 match | 4 | scan + kit → Ron's render 7. Camera = Ron's own Camera.006 moved into the scan frame, refined on silhouette + rim centres (IoU 0.87, rims 10 px / 0 px of 1920). Looked at the 50/50 overlay and at the last take frame beside the render: roof, wing, wheels, apron, lamps coincide. Body goes silver → white on the cut |
| 4 | Scan quality | 4 | kit parts are Ron's production STLs / render-scene wing and wheels, placed by a 1.4 mm registration of his scan copy onto ours (v4's lookbook fit had the apron and wing 7–8 cm too far back). The low rear view of the apron shows scanned underbody; the cut-out scanned wheels are ragged for the 0.5 s they are in frame |
| 5 | Story | 4 | three clips, two cuts: open-up → one continuous take (lip, skirts, apron, wheels, wing in the user's order, each part stays on) → Ron's render. No cutaways, no section revisited |
| 6 | Grade | 4 | house silver on black, kit white, rims gold; S1 rendered at −0.9 stops (top view blew out at 0) |
| 7 | Text | 5 | Epsilon+ wordmark only, 300 px, last 1.7 s incl. fade, on pure black (luma 0 under it) |
| 8 | Ending | 4 | render holds 2.1 s alone, then wordmark, picture and music fade over 0.5 s; no Illumaesthetic logo |
| 9 | Technical | 4 | luma scan: no dropouts (steps are camera travel); true 30 fps in-betweens everywhere except creep holds. The pull-back to the render pose starts abruptly (luma step 15 at take frame 417). Container restarted mid-render; the remaining 143 in-betweens were re-rendered, nothing lost |

## Open items
- **Music**: still the old track; the user's YouTube song could not be downloaded (no skill, YouTube blocked). Seats are followed by trimmable holds.
- **Wheels** sit where Ron placed them (47 mm up, 30 mm out vs the scanned wheels = his lowered, flush fitment).
- **Car closed during installs** (wing seats on the closed lid; ending is a closed car).
- Trunk interior is not shown (from above the open lid covers it).
