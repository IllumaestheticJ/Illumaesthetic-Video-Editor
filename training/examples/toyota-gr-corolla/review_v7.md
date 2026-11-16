# Self-review - Toyota GR Corolla v7 (`toyota_gr_corolla_v7.mp4`, 28.1 s, 1080x1920)

User on v6: front bumper from the other full car scan (the one in use misses a huge chunk) - not the facelift one;
rear trunk not cut out correctly; the hood opening is missing. v6 review kept as review_v6.md.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car with the complete stock bumper from the first hit; bumper moves at 2.4 s. |
| 2 | Beat sync | 5 | Cuts 70/140/210/280/350/420/(490 same camera)/560/630/700 + dip 755; nearest 40-200 Hz hit within 0.54 fr of every cut. |
| 3 | 1:1 match | n/a | No IRL; same-camera continuations h1->h2, c1->c2. |
| 4 | Scan quality | 4 | Bumper from FARO (stock, complete grille/fogs/corners; registered 0.3 deg/22 mm, 86 % within 3 mm), our headlights kept. Hatch cut on its traced shut line - taillights split on the real seam, clean opening. Hood cut from the closed car (no hood part scan); engine bay scan under it. |
| 5 | Story | 5 | Whole -> front bumper -> beams -> ducts -> intercooler -> hood open then off -> hatch open -> hatch off -> rear bumper + diffuser -> crash beam -> clean car -> logo. Removed panels stay off. |
| 6 | Grade | 5 | One silver look; luma min 22-44 on new renders, max jump 4.1. |
| 7 | Text | 5 | Seven labels from scan names, clear black, checked at three frames each. |
| 8 | Ending | 5 | Clean car, dip on downbeat 11, 720 px logo. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart, 844 frames; -16.5 LUFS, true peak -1.6 dBFS. |

Not used: Complete Car_1/2 (facelift bumper - user). Risk: the hood shell is the closed car's skin (its underside is the
back of the skin; the 'Core Hood Underside' scan is in another frame).
