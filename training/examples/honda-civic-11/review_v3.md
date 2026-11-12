# Honda Civic FE1 Si scan reel v3 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/civic/out/civic_fe1_scan_v3.mp4` — 1080×1920, 30 fps, yuv420p, AAC, 1194 frames = 39.80 s
(audio ends 39.72 s at −30 dB). Scan-only, no text. v3 answers the user's v2 note: "You hallucinated the doors coming off... they should just open. Same with rear trunk." v1 was never delivered: it was superseded by the user's v2 notes
(relayed by the parent and WRX VA sessions) before assembly. Plan: `direction.md` (scene-director) + `director.md`.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | the whole car is in frame and moving from frame 1 (slow push + rise), but nothing transforms until the k31 drop at 13.3 s; the track's quiet 10 s intro sets that pace |
| 2 | Beat sync | 5 | 5 hard cuts measured on the DECODED audio (1 ms RMS broadband half-rise): −3, +7, +5, +16, +5 ms (all ≤ ½ frame). The generated track drifts 8–76 ms behind a constant 143.56 BPM grid, so the cuts sit on the measured onsets, not the grid. k88 → logo is a baked fade (k86–k88), not a cut |
| 3 | 1:1 match | n/a | scan-only brief, no IRL footage |
| 4 | Scan quality | 4 | holes in the hood and rear glass filled; floor scraps, the prop sheet and the 849-tri scrap under the right sill removed. The licence plate is kept as scanned (user rule: flatten only on the IS300). Remaining: right-rear wheel is a tyre ring only (visible small in N4); Door Open has no data above ~0.85 m, so the cabin reads dark through the window openings; slight seam patches on the right doors |
| 5 | Story | 4 | whole car → front (wheel, lamp) → right side (doors swing open on the drop, on hinges, to the angle measured in the Door Open scan: front 68°, rear 64°; real sill/jambs/cabin) → rear (trunk opens on its fitted hinge and stays on the car, camera moves into the real trunk interior) → doors and lid close, shut on the k80 big kick. Nothing detaches → fade → small logo. Each section appears once. No hood, bumper or engine scenes, because no such state scans exist |
| 6 | Grade | 4 | consistent house silver on black (AgX); the fade goes to the logo card's black (7,7,9) so the last cut is invisible |
| 7 | Text | 5 | none (scan-only brief); nothing invented |
| 8 | Ending | 4 | doors and trunk close → fade k86–k88 → small logo (31 % of width) to the end of the audio, music fades 0.8 s. The clean car holds ~2.5 s after the lock |
| 9 | Technical | 5 | specs above; per-frame luma scan of every render folder (no dropouts; v1 s7 had one and was dropped); persistent data off for every shot with moving parts; N2, the N3 lid motion and dive, and the N4 closing use real 30 fps in-betweens (minterpolate smeared them); no black frames; one assembler hold frame per cut, plus one extra frozen frame at the end of N3 |

## v1 → v2 changes (all logged in editlog.jsonl)
- Order from the scan features (scene-director); dropped the v1 turntable opener (it clipped the nose), the rear-left orbit, the rotating top-down and the wide all-at-once explode (redundant views, too wide).
- First cut moved from k17 (no hit, +2.9 dB) to k24 (+16.6 dB); every cut is on a measured onset.
- New: N1 (whole car), N2 (doors lift up into the black above the car; they translate only, because their inner faces have no scan data), N3 (trunk opens, lid lifts off), N4 (reassembly + fade). s3/s4 reused (s3 reversed).
- Sill scrap removed (tools/boxdrop.py). A plate flatten was tried, then reverted: user rule, only the IS300 gets one (N3 f1-140 and N4 re-rendered).
- Logo card 860 → 330 px.

## v2 → v3 changes
- User: the doors and trunk lid coming off were hallucinated. Now the doors swing on vertical hinges fitted to the open-door strips in the Door Open scan (tools/shots_v3.py, doors/hinges.json) and the lid only opens on its hinge.
- Ending: rear door, front door and lid close and are shut on k80, seen from the front-right so the open doors show their scanned outer skin (their inner faces have no data).
- The closing smeared under minterpolate, so that stretch got rendered in-betweens too.

## Known issues / ideas
- The doors are cut from the full-car shell (no inner panels exist in the data), so cameras stay on their outer-skin side; the hinge axes are fitted (vertical, at the door's front edge), not scanned hinges. In N2's last second the front door is close to edge-on.
- The intro could carry a slow detail (e.g. grille) instead of 10 s of the wide, if the reviewer finds it long.
- The front-left wheel close-up (s3) is a 2 mm crop; its end shows a little fender seam.
