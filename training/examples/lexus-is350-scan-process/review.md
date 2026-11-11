# Lexus IS350 scan-process reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/is350/out/is350_scan_process_v1.mp4` — 1080x1920, 30 fps, 27.57 s, H.264 yuv420p + AAC, faststart.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | camera walks out of the shop onto the powdered car; the 1:1 transformation hits at 3.0 s on the drop (the track's real drop - a 2 s hook would cut on a quiet build) |
| 2 | Beat sync | 5 | 6 cuts measured from frame diffs vs kicks in the delivered audio: 0, +1, -16 (kick sub-peak), 0, +1, 0 ms |
| 3 | 1:1 match | 5 | front: FX30554 f264, PnP + silhouette refine, onion aligns grille/emblem/plate/lamps/mirrors/roof. Rear: FX30542 f1135, 11 points incl. plate screws, onion aligns plate/exhausts/fins. Crop cameras verified numerically (<0.5 px) |
| 4 | Scan quality | 4 | levelled + cleaned (no ground flap), silver on black; 4 mm full car; silver is bright in the front orbit; x-ray shows scan interior layers (busy for ~1 s) |
| 5 | Story | 4 | real walk-out -> scan -> powder + scanner + rear scanning -> scan -> reflector out/inside+outside -> x-ray reassembly -> listing. **No panel/bumper removal exists in the footage**, so the removal beat is the reflector popping out in the scan (only part-state scan of this car) |
| 6 | Grade | 4 | all FX3A S-Log3 clips through one LUT (S-Log3/S-Gamut3.Cine -> 709, Hable); spray insert is bright (backlit concrete) |
| 7 | Text | 5 | only on scan shots, <=2 items: 24,999,992 (full-car STL header), 408,984 (reflector STL header), INSIDE + OUTSIDE verified on the rendered spin. Counter bug fixed (see editlog) |
| 8 | Ending | 5 | x-ray ends on the listing 360-viewer pose in listing grey, dissolves into the IS350 listing; zoom-out lands on a downbeat; title, logo, URL below it last; music fades with the end |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart; match frames are the clips' last frames; no black/dup frames at cuts |

## Known issues / ideas for v2
- If the team has footage of the reflector (or bumper) actually coming off, a real removal -> part-state 1:1 cut would replace the scan-only pop-out.
- Front orbit silver reads hot; a lower key light for close full-car shots.
- The reflector is small (~200 px); a slow push toward it during the spin would help on phones.

## v2 (user feedback)
- End card now shows the listing with the **2026+ front bumper** dataset selected and the title "SCAN DATA + 2026 BUMPER NOW AVAILABLE";
  dissolve match unchanged (viewer pixel-identical). The 2026 bumper scans are a different car, so they are not in the 1:1 story.

## v3 (all-reels v2 brief, scene-director + director plans)
Output: `/home/user/media/work/is350/out/is350_scan_process_v3.mp4` — 1080x1920, 30 fps, 27.57 s.

| # | Criterion | Score | Change vs v1 |
|---|---|---|---|
| 1 | Hook | 4 | unchanged opener; 1:1 on the 3.0 s drop |
| 2 | Beat sync | 5 | music delayed 25 ms so cuts sit on broadband kick attacks; cut frames 90/210/240/285/390/570 all on the 0.5 s grid |
| 3 | 1:1 match | 5 | both match crops widened (window 1063 px, blurred fill) so the whole car reads; scan camera re-derived (sensor 35.6*win/1920); onions re-checked |
| 4 | Scan quality | 5 | front shot is a push to grille/headlights instead of a repeated orbit; reflector framed close, never leaves frame |
| 5 | Story | 4 | still no real removal in the footage (reflector pop-out in scan) |
| 6 | Grade | 4 | unchanged |
| 7 | Text | 5 | labels re-timed and moved onto black under the part; numbers from STL headers |
| 8 | Ending | 5 | x-ray path from the reflector close-up to the listing pose, 0.5 s dissolve kept (director proposed a hard cut; overridden per brief) |
| 9 | Technical | 5 | persistent data off on moving-part renders; no luma dropouts; no black/dup frames at cuts |

Director flags left on purpose: the two 'same view' pairs are the continuity cut and the listing dissolve; the 1.2 s end hold carries the logo + URL.
