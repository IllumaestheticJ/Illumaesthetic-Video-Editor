# C5 Corvette scan reel v4: agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_corvette_v4.mp4`: 1080x1920, 30 fps, yuv420p, AAC, 32.80 s (984 frames).
v4 = v3 with these reviewer notes (2026-11-12) applied:
- **Removed the left doorsill and trunk-open sections** ("looks bad"). The gas cap stays.
- **Logo 650 px wide** instead of 300 px ("too small").

Every later section moves up 6 kicks, so the cuts are now at 4.100, 9.300, 14.767, 18.033, 22.400 and 25.667 s, with the logo at 28.933 s.
All are within one frame of the measured kicks. The gas-cap swap lands at 15.867 s and the clean-car swap at 27.833 s, each as a hard one-frame step.
Scores as below, except Story (5 → 4): six sections now and no side door content. Scan quality goes 4 → 5, because the two weakest scans are gone.

---

# C5 Corvette scan reel v3: agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_corvette_v3.mp4`: 1080x1920, 30 fps, yuv420p, AAC, 39.37 s (1181 frames).
Scan only. Nine title-only labels, all over black. Music: the parent session's generated track only.
The v2 review (`c5_corvette_v2.mp4`) is in git history. The v3 plan is in `direction.md` ("# v3 direction"), and every decision is in `editlog.jsonl`.

## What changed from v2
Reviewer feedback: "a lot of artifacts ... we also have gas cap and doorsill scans, as well as a trunk scan ... delete/hide the
artifacts from the full car scan when it cuts in".
- **Artifacts.** v2 used one composite that carried every removed state at once. The state scans' duplicate hood, cowl and glass sat
  more than 7 mm off the car and showed as shards. v3 builds a separate base per section (`tools/composite2.py`). Each base uses
  only that section's own state scan, keeps a state triangle only if it is more than 15 mm from both the car and the parts, and
  drops connected islands under 4000 triangles.
- **Clean car.** The full car is now `car3`: `tools/carclean.py` removes ground scraps and tyre fringe. This is the car that cuts
  in at the open and the end.
- **New scans.** Left doorsill, gas cap and trunk open are shown as in-shot swaps from the closed car to the captured state
  (`tools/swapstate.py` replaces just that region), each on a strong kick. There are no door, fuel-door or hatch part scans, so
  nothing is animated off; the state simply appears. The right doorsill failed registration (5.6 mm) and is not used.
- **Order.** One lap with no line cross: whole → front bumper → hood → +X sill → gas cap → trunk → rear bumper → -X fender → whole → logo.
- **Swaps.** Each in-shot swap is a hard one-frame step. The minterpolate blend frame at each swap is replaced (freezeframes).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole clean car moving from frame 1 (0.4 s fade-up); bumper starts off at 1.2 s |
| 2 | Beat sync | 5 | cuts at 4.100, 9.300, 14.767, 18.033, 21.300, 24.600, 28.967, 32.233 s; in-shot swaps at 15.867 (sill), 19.133 (gas), 22.400 (trunk), 34.400 (clean car). All within one frame of the measured 40-150 Hz kick rise; most within ½ frame |
| 3 | 1:1 match | n/a | scan-only by brief |
| 4 | Scan quality | 4 | per-section bases: no floating shards from duplicate skins. Remaining: the trunk tub has a ragged no-data edge where the glass opening meets the sparse scan, and the gas-door seam shows a thin trim line at macro distance |
| 5 | Story | 5 | nine sections, one focus each, every state from a registered scan, no section repeats; the user's three new scans each get a held, labelled beat |
| 6 | Grade | 5 | one look throughout. Per-frame luma has no dropouts; the large steps are the intended swaps and parts turning edge-on |
| 7 | Text | 5 | nine labels worded from file / state names, over black, no numbers |
| 8 | Ending | 5 | clean car, fade, small logo on the biggest hit |
| 9 | Technical | 5 | 1080x1920 30 fps yuv420p AAC. First/mid/last frames and the frames around every swap checked. The hood leaving the top of frame is deliberate (it rises off) |

## Checks run
- `projects/porsche-macan/tools/cutcheck.py` (broadband), plus a 40-150 Hz envelope printed at frame steps around each cut.
- Swap frames were found by frame differencing the output; each blend frame was then inspected visually.
- `ive director` flags fb vs home as the same view (IoU 0.73). This is the known silhouette false positive: one is a front macro of the opened car, the other the whole clean car.

## Known issues / v4 ideas
- Trunk: the scan is sparse below y 1.6 m, so the tub edge is ragged. A tighter low camera or a fill from the trunk-closed underside would help.
- The right doorsill could be added after a manual seed for registration (current FPFH result 5.6 mm).
- 1:1 IRL → scan version from the C5 Dropbox dump.
