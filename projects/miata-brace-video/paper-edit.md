# Miata brace video — notes on MiataScan_RoughCut_1.mp4 (7:05, UHD, 23.976)

Source: Dropbox `/3. Epsilon Motorsports/1. Video Dumps/NA MIATA GRIMACE/MiataScan_RoughCut_1.mp4`.
Scan reports: same folder, `Chassis Scan Video/*.pdf`. All numbers below are read from the
tables/dimensions already on screen in the cut (engine-bay width between the strut towers).

## Reviewer notes received
- 0:20 — wants a 2D "chassis flex" graphic as a corner overlay on the track footage, showing flex over bumps and under cornering (delivered: `ChassisFlexOverlay`, cornering at 0:13–0:18, bumps at 0:18–0:23). The earlier full-frame `ChassisFlex` card was not what was wanted.
- 0:49 — caption reads "kind of races", should be "fender braces".
- 0:51 — caption reads "Thank you. Good one.", should be "Good-win" (Goodwin Racing).
- 3:00 onward — no voiceover yet; wants each scan followed directly by its own data, for suspense.

## What is in the cut from 3:00 now
| # | Timecode | Content |
|---|---|---|
| A | 3:04–3:30 | "Scanning the Stock Miata": ground scan, jack up one corner, tape measure, jacked scan (all one block) |
| B | 3:30–4:07 | "Stock Miata" data: bay width control vs jacked, table, "how to read the heatmaps", exterior heatmaps |
| C | 4:08–4:29 | Install strut tower brace, jack, scan |
| D | 4:30–4:55 | "Strut Brace Only" data + table row |
| E | 4:56–5:20 | Install fender brace |
| F | 5:20–5:29 | Scan fender + strut brace |
| G | 5:30–6:02 | "Fender Brace + Strut Brace" data + table row, strut-tower close-up heatmap |
| H | 6:03–6:18 | Remove strut brace, final scan |
| I | 6:19–6:57 | "Fender Brace Only" data + final table |

Measured engine-bay width (mm) and change vs. control:
| Configuration | Width | vs control |
|---|---|---|
| Control (stock, on the ground) | 960.948 | — |
| Stock, one corner jacked | 962.643 | +1.695 |
| Strut tower brace, jacked | 961.679 | +0.731 |
| Fender + strut brace, jacked | 961.384 | +0.436 |
| Fender brace only, jacked | 961.185 | +0.237 |

## Proposed order (scan -> its own data, one configuration at a time)
The braces are already in scan -> data order. The part that is lumped together is the stock car:
block A shows both stock scans before any data. Split it:

1. **Control** — A (3:04–~3:12, ground scan only) -> B bay-width image, left half only + table with
   the single control row (960.948 mm). Move "how to read the heatmaps" (3:44–3:50) here, before
   the first heatmap appears.
2. **Stock, jacked** — A (~3:12–3:30: jack, tape measure, scan) -> B right half + table row 2
   (+1.695 mm) -> exterior heatmaps (3:50–4:07). This is the "how bad is it" reveal.
3. **Strut tower brace** — C -> D (+0.731 mm).
4. **Fender + strut** — E, F -> G (+0.436 mm).
5. **Fender brace only** — H -> I (+0.237 mm), end on the full table.

Recommendation: keep the braces in the order they were shot (strut -> both -> fender only) rather
than fender first. It matches what the footage shows on the car, and the numbers fall in that
order, so the smallest figure lands last. Note the result the VO has to address: fender brace
alone (+0.237) measured tighter than fender + strut together (+0.436).

For suspense, hold each table row back until after that configuration's scan footage, and cut the
on-screen list at 2:40–2:55 ("Scan 1 / Scan 2 / Scan 3") to match the five steps above.

## Voiceover draft for 3:00 onward (numbers from the table; edit freely)
1. Control: "First, the baseline. Stock car, all four wheels on the ground. Strut tower to strut
   tower, the engine bay measures 960.9 millimetres. Every number after this is compared to that."
2. Stock, jacked: "Now we load it. One corner on the jack, same height every time, and scan again.
   With no bracing the bay opens up by 1.7 millimetres. On the heatmap, green is where the body
   hasn't moved; the further it goes to red or blue, the more it has."
3. Strut tower brace: "Strut tower brace on, same corner, same height. The bay now moves 0.73
   millimetres — less than half of stock."
4. Fender + strut: "Add the fender braces and scan again: 0.44 millimetres."
5. Fender brace only: "Last one. Strut brace off, fender braces only: 0.24 millimetres. That is the
   smallest movement of the day — and it's with fewer parts on the car."
