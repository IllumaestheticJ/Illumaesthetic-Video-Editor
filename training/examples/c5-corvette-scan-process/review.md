# C5 Corvette scan-process reel v5 - agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_scan_process_v5.mp4` - 1080x1920, 30 fps, 47.77 s, H.264 yuv420p + AAC.
v5 = user on v4: "use the Z06 engine bay scan anyway, there are a ton more scans not shown. get rid of the redundant scan of
the roof (after roof goes away). again, no one cares about triangle count". Plan: direction.md (v5 table).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real C5 rear pass, 1:1 cut to the scan on the kick at 2.0 s |
| 2 | Beat sync | 5 | 14 hard cuts measured on the decoded output: -4..+16 ms from the kick peaks; listing dissolve ends on beat 168, URL on the final hit (46.0 s) |
| 3 | 1:1 match | 4 | cut A RMSE 5 px, cut B on the wider window (unchanged from v4); new same-camera state cut door panel on -> removed (shared scan frame, handle cup and sill line up) |
| 4 | Scan quality | 4 | all new folders luma-checked (no dark frames); interior + doorsill scans rejected as fragmentary; ragged top edge on both door scans and the engine-bay perimeter remain |
| 5 | Story | 4 | rear -> roof (cut as it leaves) -> crew strips the front -> 1:1 -> front structure -> Z06 engine bay -> parts front to rear (head lamp, turn signal, door panel on/removed, fuel door) -> underbody -> reassembly -> listing. Engine bay is a separate Z06 scan, shown on its own and labelled Z06 |
| 6 | Grade | 4 | SDR DJI footage, consistent warmth |
| 7 | Text | 5 | no triangle counts anywhere; labels name what is on screen (from file names / visible geometry); scan shots only, one label at a time |
| 8 | Ending | 4 | unchanged v4 ending (x-ray -> listing grey -> same-angle listing), still on the track's final hit |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC; no black/duplicate frames at cuts; persistent data off |

## Known issues
- Engine bay is from a Z06 (different car), as the user asked; it is not composited onto this C5.
- Montage holds are 1 s on head lamp / turn signal / fuel door - fast by design; door reveal holds 3 s.
- Hood stays closed in the full-car scans (hood-open supplement does not register).
