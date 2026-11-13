# Huracan Evo scan reel v7 - self-review (training/rubric.md)  (older: review_v6 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v7.mp4` - 1080x1920, 30 fps, AAC, 29.97 s.
Changes from the user's notes on v6: the full coupe rear-end disassembly, the exhaust and the wheel wells (2023 coupe scan set),
a 720 px logo (was 380), and a narration conclusion ("Named after a fighting bull, and built like one. This is the Huracan EVO."
landing on the logo).

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Reference engine start-up and lights-up reveal; speech from 3.0 s. |
| 2 | Beat sync | 5 | Hard cuts vs kicks on the delivered file: +22 -11 -11 -12 -12 -12 ms. The drop is at 10.28 s and the logo is on the music stop at 27.08 s. |
| 4 | Scan quality | 3 | New parts are registered (regcheck 2.3-7.6 mm median). The exhaust (scanned standalone) was fitted by ICP at 4.7 mm median. Jack stands were cut from the rear-end and wheel-well scans. The derived bumper has ragged edges where the full car and the no-bumper scan meet, and the rear-end scan ends at mid-car (framing keeps the cut edge small). |
| 5 | Story | 4 | Coupe select -> wheel -> side -> drop -> Spyder front bumper -> coupe rear bumper off (hold) -> grille/beam/decklid off -> exhaust out -> rear wheel well (no liner) -> reassembly to the whole coupe -> logo. One Spyder shot remains at the front of the teardown. |
| 7 | Text | 4 | Labels: REAR END, NO BUMPER / 9,500,000 TRIANGLES and EVO EXHAUST / 17,309,868 TRIANGLES (STL header counts, size-checked), both on black. |
| 8 | Ending | 5 | Reassembly -> whole-coupe pull-back -> fade -> 720 px logo while the narration says "This is the Huracan EVO." |
| 9 | Technical | 4 | Every new frame is lit (luma scan). Speech is -13.1 LUFS, engine -10 LUFS, peaks <= -0.4 dBFS. |
Unchanged rows (3, 6) as in v5.

## Not verified
- I can't listen here, so the conclusion line's delivery is unheard.

## What the next agent should know
- Standalone part scans (e.g. 'EVO exhaust', scanned upright on a stand) are NOT in the car frame. Fit them to a state scan that shows the part installed: PCA axes x sign-flip search + trimmed ICP, then keep the clear winner (here 4.7 mm vs 17 mm for the next orientation).
- State scans taken with the car on jack stands carry the stands. Cut low triangles outside the tyre contact zones before prep.
- `shots.py` has several `__main__` blocks. Write a single section's JSONs with `runpy.run_path(..., run_name='v7')` so older sections don't overwrite rendered shots' JSONs.
