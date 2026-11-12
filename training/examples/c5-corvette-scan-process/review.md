# C5 Corvette scan-process reel v4 - agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_scan_process_v4.mp4` - 1080x1920, 30 fps, 31.83 s; cuts at frames 65/294/360/425/458/621, -6..+13 ms from the decoded kicks, H.264 yuv420p + AAC.
v3 = user notes on v2 (front bumper glides toward the camera showing its mounting side; add the rear-bumper-removed data) +
the all-reels brief and its addendum (one sequence per section, travel without ping-pong, bumper-removed hero beats with labels,
wider 1:1 crops, shorter ending, persistent data off + luma check). Plan: direction.md.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real stock rear pass, 1:1 cut to the scan on the kick drop at 2.17 s |
| 2 | Beat sync | 5 | 6 hard cuts on kick peaks measured in the decoded audio (after nudging 3 cuts 1 frame earlier); dissolve into the listing |
| 3 | 1:1 match | 4 | cut A RMSE 5 px (taillights/lettering/silhouette on); cut B now on a wider 1158x2058 window (camera rescaled, not re-solved), edges on the wheel/arch/door; aftermarket wheel + raised hood still differ from the scan |
| 4 | Scan quality | 3 | silver on black, no dark frames (all folders luma-checked); ragged borders remain on the exposed structure of both state scans |
| 5 | Story | 4 | rear: real -> scan -> rear bumper mounting side -> push-in on rear-bumper-removed structure; front: crew pulls fender + bumper -> 1:1 -> fender inside, bumper mounting side -> push-in on the stripped nose; x-ray reassembly of all three parts -> listing. Each section appears once. No scanner footage exists |
| 6 | Grade | 4 | SDR DJI footage, consistent late-afternoon warmth |
| 7 | Text | 4 | scan shots only, one label at a time; numbers from STL headers (8,255,611 full car; 8,028,053 rear-bumper-removed); "MOUNTING POINTS" / "INSIDE + OUTSIDE" verified from the scans; static labels (ScanHUD counter easing bug avoided) |
| 8 | Ending | 4 | x-ray ends on the listing hero angle (IoU 0.91), morphs to its grey, dissolves; end card 5.7 s (was 7.1) |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC; no black/duplicate frames at cuts; renders persistent-data off |

## Known issues
- The opening real clip is native portrait (full frame) - its crop cannot be widened further.
- Rear bumper part is the car's rear skin + the separately scanned inside surface (no single loose-bumper scan exists).
- Hood stays closed in the scans (the hood-open supplement does not register), while it is up in the stripped-front footage.

## v4 (user: use the uploaded NASCAR 2005 Chase theme; include more scans, e.g. under the hood)
- Music: 'Thunder' from track 48.03 s; 1:1 cut on the section change (2.0 s), end card on the final hit (38 s); 39.8 s total.
  8 hard cuts on accented even beats, -4..+15 ms from the kick peaks in the decoded audio.
- New sections: TARGA ROOF (registered targa top lifts, turns its scanned underside to camera, then the 2026 roof-open cockpit)
  and UNDERBODY (Project 8 C5 Underside, x-ray). Order: rear -> top -> front (IRL + 1:1) -> underbody -> reassembly -> listing.
- Under the hood: not possible with this car's data (Engine Bay Z06 = a different car; hood-open supplement does not register;
  'front bumper and hood removed' covers only the radiator support). Asked the user for a registered engine-bay scan.
- Scores unchanged except Story 4 -> 4 (more data shown, still no scanner footage) and Beat sync 5.
- Risk: underbody (x-ray) and reassembly (x-ray) sit back to back - different subjects, similar look.
