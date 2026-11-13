# Huracan Evo scan reel v8 - self-review (training/rubric.md)  (older: review_v7 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v8.mp4` - 1080x1920, 30 fps, AAC, 29.97 s.
Changes from the user's notes on v7: narration re-flowed (the ending felt patched on), rear bumper rebuilt (it came off as one giant
piece with too much attached), triangle counts removed from the labels.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 2 | Beat sync | 5 | Hard cuts vs kicks on the delivered file: +22 -11 -11 -12 -12 -12 ms. |
| 4 | Scan quality | 4 | The rear bumper is now the skin inside the scanned 'Rear Bumper B side' envelope plus that scan as its inner face (1.44M tris). The wheels stay on the car as a static object. The skin's outline is still cut from the full-car scan, so its edge is slightly ragged. |
| 5 | Story | 4 | Same order as v7. |
| 7 | Text | 5 | Two title-only labels on black: REAR END, NO BUMPER and EVO EXHAUST. No numbers. |
| 8 | Ending | 5 | The speech ends at 26.6 s on its concluding sentence, the music stops at 27.08 s, and the 720 px logo follows. |
| 9 | Technical | 4 | Re-rendered frames all lit. Speech -13.0 LUFS, peaks <= -0.4 dBFS. |
Rows 1, 3, 6 unchanged from v7.

## Narration (one take, untrimmed, no tempo/pitch change)
"Lamborghini Huracan EVO. Its naturally aspirated V10 makes six hundred thirty-one horsepower. Four-wheel drive and rear-wheel
steering are run by LDVI, a brain that predicts your next move. It makes more than five times the downforce of the original
Huracan, reaches sixty-two in two-point-nine seconds, and runs on to two hundred and two miles per hour. It was named after a
fighting bull, and the EVO has more than earned it."

## Not verified
- I can't listen here, so the take's delivery is unheard.

## What the next agent should know
- "Feels patched on" came from three things: clipped fragment sentences added after a spec list, pause-trimming, and the voice running past the music stop. Write the conclusion as the speech's last sentence, generate one take that fits untrimmed, and end it before the music stops.
- Don't derive a removable panel as "everything the panel-off state scan lacks": state scans are often shot wheels-off and on stands, so wheels and underbody come along. Bound the panel by its own part scan (here the B-side scan's envelope).
- No triangle counts in labels (reviewer rule).
