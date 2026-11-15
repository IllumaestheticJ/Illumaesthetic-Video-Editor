# GR Corolla - short-form Temerario restart (v6)

User on v5: "wtf did you do to the door. I said the front bumper was missing a chunk from it" and "completely start
this over, using the short form temerario skill, and graphify". Answers to the up-front questions: plan from the
graphify graph (logo-only ending), 'Going Up North' from its beginning, content = front bumper + under parts, rear
bumper/diffuser/crash, hatch open. (v4 plan kept as direction_v4.md.)

## Rules pulled from the graph (graphify-out/ + knowledge/feedback/, `graphify query` on this repo)
| Source note | Applied as |
|---|---|
| WRX VB: "remove the front bumper first, then pull the grille and other parts off" | b1 = bumper alone, everything behind it seated |
| GR86: "as the bumper is removed, parts of the old bumper are still visible on the car" | every car face cut as bumper skin moves WITH the bumper (bumperfill.py) |
| GR Corolla v5 (this user): "the front bumper was missing a chunk" | fbumper6 = bumper scan + the car's own skin where the scan is torn |
| GR Corolla v4: "front end scan missing a huge chunk" | fbase5 keeps headlights + fender tops (frontcut.py, bumperline.py) |
| GR86: "the hood needs to hinge open THEN come off"; "trunk ... done the same way - we have a trunk open scan" | h1 hatch hinges 75 deg on its top edge (measured: 47.6 deg down closed -> 27.4 deg up in the open-state scan), h2 lifts off; cargo area = 'trunk open' state scan |
| GR Corolla v3: "parts off the bumper shouldn't come off until the bumper is off" | diffuser leaves with the rear bumper |
| GR Corolla v3: bay data must stay under the parts | Engine Bay Stripped in fbase5 |
| GR86: "the video needs to move faster"; skill: short form 15-30 s | 10 one-bar shots, ~26 s with the logo |
| GR86: "logo at the end is too small" | 720 px logo card |
| Revuelto: "parts going off the screen" / clipping | parts exit cleanly (checked per frame), no part passes through another |
| Revuelto: wheels cut flat; plate only flattened on the IS300 | car4w (round wheels, plate kept) |
| Skill: music from its beginning, -14 LUFS, true peak < -1 dBFS | start 0.485; gain set after a loudness measurement |
| User v5: the door-off 'roof' scans should not have been added | not used |

## Shots (one bar each, cuts on the kick downbeats)
| # | Shot | Frames | Render |
|---|---|---|---|
| 1 | Whole car push | 0-70 | renders5 a1 |
| 2 | Front bumper off (whole) | 70-140 | renders7 b1 |
| 3 | Bumper beams | 140-210 | renders6 b2 |
| 4 | Ducts | 210-280 | renders6 b3 |
| 5 | Intercooler | 280-350 | renders6 b4 |
| 6 | Hatch hinges open | 350-420 | renders7 h1 |
| 7 | Hatch lifts off (same camera) | 420-490 | renders7 h2 |
| 8 | Rear bumper + diffuser | 490-560 | renders7 c1 (hatch off) |
| 9 | Crash beam removed (same camera swap) | 560-630 | renders7 c2 (hatch off) |
| 10 | Clean car | 630-700 | renders5 d1 |
| - | Dip -> logo | 700-790 | |
