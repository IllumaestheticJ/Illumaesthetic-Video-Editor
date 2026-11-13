# Toyota Sera scan-process reel v3 - self review (training/rubric.md)
Output: /home/user/media/work/out/sera_scan_process_v3.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 26.97 s.
Plan: direction.md (scene director). v1/v2 reviews: review_v1.md, review_v2.md.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Real car 1.77 s, 1:1 cut to the scan on the 1.8 s phrase change. |
| 2 | Beat sync | 5 | Cuts measured on the DECODED audio of the delivered file: 1.800 3.600 6.000 7.200 9.600 11.400 13.800 15.600 18.000 19.800 - all within +/-7 ms of kick peaks (< 1/2 frame). |
| 3 | 1:1 match | 3 | Opening: wider crop (zoom 1.0), aligns within a few px. Front lift: wider, hand-placed camera on a blurred frame, ~20 px. Rear: hard cut (bumper never fully off on camera). |
| 4 | Scan quality | 4 | No lighting dropouts (per-frame luma checked on every render). Rear close-up shows the tail-light holes of the Rear Bumper Removed capture (real scan holes, kept short). |
| 5 | Story | 4 | One sequence per section: front (real car, 1:1, real bumper lift, 1:1 bay, bumper inside+outside, what's behind it) -> side (butterfly doors from the Door Open scan) -> rear (real pull, bumper inside+outside, behind it) -> x-ray reassembly -> listing. Still no handheld-scanner footage (none exists). |
| 6 | Grade | 4 | S-Log3 LUT; daylight vs shop warmth differ (real). |
| 7 | Text | 5 | Static labels only over scans; numbers = STL header counts (14,999,999 / 1,800,000 / 4,999,998 / 10,500,000); "removed"/"behind the bumper" labels name what is visible. |
| 8 | Ending | 4 | X-ray lands on the listing hero angle (clay, listing grey) and dissolves; end card 3.6 s, no dead frames; rear-wheel ghost in the dissolve remains. |
| 9 | Technical | 5 | Spec met; director report: no dead frames, every shot tagged with section + focus; only flagged repeat is the intended x-ray -> listing dissolve. |

## v3 changes (all-reels brief + addendum)
- Order front -> side -> rear, no ping-pong; v2's rear-first block and the wide spinning explodes (s3_rear, s6_frontx) cut.
- Bumper-removed hero beats: each bumper drops below the car into black and turns to show its scanned inside, then a
  close 3/4 on the exposed structure from the bumper-removed state, with labels.
- New side beat: butterfly doors from the 'Door Open' capture as captured (no faked opening), composited on the full car.
- Frames: first/middle/last of every shot checked; parts stacked vertically so nothing leaves the 9:16 frame.
- End card trimmed 6.6 -> 3.6 s; x-ray re-timed (front bumper home 20.4, rear on the 21.0 phrase change).

## Gap to learn from
v1/v2 laid scan shots out by template (rear, front, x-ray) and framed explodes wide; the feature-driven order and
stacked part paths fixed both without new footage.
