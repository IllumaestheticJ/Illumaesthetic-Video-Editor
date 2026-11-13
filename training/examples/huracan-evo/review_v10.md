# Huracan Evo scan reel v10 - self-review (training/rubric.md)  (older: review_v9 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v10.mp4` - 1080x1920, 30 fps, AAC, 39.6 s.
Changes from the user's notes on v9: slower pacing in a longer cut (may exceed 30 s), the missing chunk in the full-car rear
filled, and a label on every teardown step.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 2 | Beat sync | 5 | 10 scan cuts on the kick grid of the delivered file: +22 (drop), then -11..-13 ms. The track's own kick peaks jitter by -31..+24 ms around that grid. Logo on the last kick, 36.68 s. |
| 3 | 1:1 match | 4 | Coupe -> Spyder stealth cut unchanged from v9 (IoU 0.89). |
| 4 | Scan quality | 4 | The plate hole is gone: the plate region is the real scan surface, Laplacian-smoothed blank (nothing legible in a close-up render), on the full car and on the bumper part. Spyder wheels are still dark. |
| 5 | Story | 4 | Same order as v9. Each teardown step now runs 2.4-3.0 s at 1.0-1.6x (v9: 1.2-1.8 s at 1.3-2.7x). |
| 7 | Text | 4 | Seven title-only labels, each on black for its shot (occupancy-checked): FRONT BUMPER, HOOD + COWLS, FENDER + SIDE SKIRT, REAR BUMPER, DECKLID + GRILLE, EVO EXHAUST, REAR WHEEL WELL. Positions vary (five top-left, two lower-left) because of where black is available. |
| 8 | Ending | 5 | The speech ends at 34.6 s on its conclusion, the music's last kick is at 36.68 s with the 720 px logo, and the tail runs to 39.6 s. |
| 9 | Technical | 4 | Re-rendered frames all lit. Speech -13.8 LUFS, peak -1.0 dBFS. |

## Narration (one take, untrimmed, speech_rate 12, no tempo/pitch change)
"Lamborghini Huracan EVO. Its five-point-two-liter V10 fires at uneven intervals, fifty-four and ninety degrees apart, which
gives it that jagged, howling note. Titanium intake valves, port and direct injection, six hundred thirty-one horsepower at eight
thousand RPM. LDVI reads the car and steers all four wheels before you ask. Its successor went to a twin-turbo hybrid V8, which
makes this one of the last great naturally aspirated Lamborghinis."

## Not verified
- I can't listen here, so the take is unheard. The middle sentence is a list of fragments ("Titanium intake valves, port and direct injection, ..."), which may read as clipped.

## What the next agent should know
- Don't delete licence-plate triangles: it leaves a hole the reviewer sees as "a missing chunk". Smooth the region instead (Laplacian, boundary fixed) and check a close-up render for legibility.
- Label placement: union the shot's frames into an occupancy map and pick the emptiest of a few candidate boxes per label.
- A longer cut from the same track: keep the drop where it is and repeat groove bars after it (`tools/music_v10.py`).
