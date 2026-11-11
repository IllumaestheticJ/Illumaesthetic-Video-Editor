# Toyota Sera scan-process reel v2 - self review (training/rubric.md)
Output: /home/user/media/work/out/sera_scan_process_v2.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, faststart, 26.97 s (809 frames).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Real car for 1.77 s, 1:1 cut to the scan on the first 16-beat phrase change (1.80 s). |
| 2 | Beat sync | 5 | Cuts measured from frame diffs: 1.800 4.200 6.000 9.000 11.400 12.600 15.600 (+dissolve end 21.0); nearest detected kicks within +/-5 ms. Holds 3/4/3/5/4/2/5/8 beats. |
| 3 | 1:1 match | 3 | Opening: 7-landmark solve (6.9 px RMSE at 4K) + onion, aligns within a few px. Front lift-off: frame is pan-blurred and half covered by a crew member - hand-placed camera, ~20 px at 1080 wide in the onion (match/check_front.jpg). The rear removal could not be 1:1 (bumper never fully off on camera) - hard cut instead. |
| 4 | Scan quality | 4 | Ground cleaned, silver on black, 3 mm full car / 2 mm parts. Hood-open state has a few holes deep in the engine bay; composite seams hidden behind the bumper zone. |
| 5 | Story | 3 | Real car -> scan -> crew pulling rear bumper -> rear bumper explodes (inside+outside) -> crew lifts front bumper -> 1:1 -> front bumper explodes -> x-ray reassembly -> listing. **Missing: no handheld-scanner footage exists in the Sera dump**, so the "scanning" beat is not shown. |
| 6 | Grade | 4 | FX30 S-Log3 graded with a generated S-Log3/SGamut3.Cine -> 709 LUT; daylight (4342) vs shop (4351/4359) differ in warmth - real. |
| 7 | Text | 5 | Only on scan shots; header triangle counts (14,999,999 / 4,999,998 / 1,800,000); INSIDE + OUTSIDE verified by rendering both bumpers from behind. Counter replaced by a label (ScanHUD counter bug, see lessons). |
| 8 | Ending | 4 | X-ray lands on the listing hero angle, morphs to the listing's grey and dissolves into the page; WebZoom: title, logo, URL below the logo last; music fades at the end. Rear wheel ghosts ~60-90 px during the dissolve (hero render's camera not exactly recoverable). |
| 9 | Technical | 5 | Spec met; no black/dup frames at cuts (strips in qa). |

Open items for the reviewer: scanner footage location? Is the front 1:1 acceptable given the blurred source frame?

## v2 (user: "Much better, but the irl to cgi crops from the video are awfully close")
- Both 1:1 IRL crops widened to the full sensor height (zoom 1.0 - the widest full-bleed 9:16 window of the 4K frame):
  opening now shows the whole front of the car (was a 1.3x crop of its right half), front lift 1.2x -> 1.0x.
  The front lift cannot go wider (camera ~2 m from the car). Scan shots s1/s5 re-rendered from the re-derived crop cameras;
  onions in match/check_v2.jpg; cuts re-measured 1.8 / 11.4 s exact.
- Gap to learn from: v1 picked crops to maximise the solve's landmark area, not the viewer's read of the car.
