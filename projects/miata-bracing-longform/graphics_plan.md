# CGI and graphics plan (after agent review + scan tests, 2026-11-12)

| # | Priority | Where (v3 cut) | What | Needs | Status / risk |
|---|---|---|---|---|---|
| 1 | must | 4:12 | "How to read the heat maps" card with the reports' real colour ramp | none | done (cards/legend.png); animate in Remotion later |
| 2 | must | tables at 4:07, 6:08, 7:29, 8:45; chart 9:38 | Animated table (rows add one at a time) and bar chart (bars grow, 1.695 stays as reference) | Remotion | fixed labels, not ScanHUD counters (they stop 0.1 % short) |
| 3 | must | width cards 3:09, 3:49, 5:51, 7:08, 8:27 | Engine-bay scan in house silver, top-down, dimension line drawing tower to tower; state scan cross-fades on the same camera, label changes | 5 engine-bay STLs (shared frame, tested) | print the report's numbers only; endpoints depend on owner question 1 |
| 4 | must | heat cards 4:42-5:19, 6:14-6:55, 7:36-8:18, 9:03-9:38 | Deviation heat map baked onto the real scan, ONE +-15 mm scale for all four states, same three cameras (both sides, top), slow push | 5 exterior STLs | gate PASSED: exported alignment reproduces the unbraced report pattern (tools/heat.py --asis). Mask floor, wheels, glass; label doors/top/trunk as panels |
| 5 | should | before the chart (9:38) | 2x2 split screen of the four states, same camera and scale | renders from #4 | makes the strut-only result obvious; narration already owns it |
| 6 | should | 5:05 | Exaggerated deflection: control scan displaced by the unbraced deviation x20, labelled "movement exaggerated 20x" | field from #4 | hinged panels frozen; label must be large |
| 7 | should | 3:04 | House 1:1 hard cut from the static front shot to the control scan | control exterior, camera solve | source shot has a burned-in title; needs a clean export |
| 8 | nice | 0:14-0:23 | Intro flex graphics on the real NB scan instead of schematic boxes | control exterior + bay | scene 3 (fixed roof vs open top) stays 2D |
| 9 | skip | - | Strut-tower close-up heat maps | - | no braced/unbraced difference visible |

Render budget (Cycles CPU, one job at a time): #3 five stills + cross-fades; #4 twelve short shots, emission shading, low samples.
