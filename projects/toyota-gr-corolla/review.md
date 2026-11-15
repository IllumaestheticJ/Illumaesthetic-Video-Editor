# Self-review - Toyota GR Corolla short-form Temerario restart (`toyota_gr_corolla_v6.mp4`, 25.8 s, 1080x1920)

User on v5: "wtf did you do to the door. I said the front bumper was missing a chunk from it" / "completely start this
over, using the short form temerario skill, and graphify". Plan from the graphify feedback graph: direction.md.
v5 review kept as review_v5.md.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Song starts on its first hit with the whole car pushing in; the bumper starts moving 3 frames into shot 2 (2.4 s). |
| 2 | Beat sync | 5 | Cuts from frame diffs 70/140/210/280/350/(420 same camera)/490/560/630 + dip 685; a 40-200 Hz hit within 0.6 fr of every cut on the decoded mp4. |
| 3 | 1:1 match | n/a | No IRL. Same-camera continuations h1->h2 and c1->c2 (state swap) checked at frames 419/421, 559/561. |
| 4 | Scan quality | 4 | Front bumper part whole (car skin fills the torn corners of its scan), nothing of it left on the car, headlights kept, bay scan behind the parts. Hatch shell cut from the closed car (no open-lid part scan), cargo area from the trunk-open state scan. |
| 5 | Story | 5 | Whole -> front bumper first -> beams -> ducts -> intercooler -> hatch hinges open -> hatch off -> rear bumper with its diffuser -> crash beam -> clean car -> logo. No door shots. |
| 6 | Grade | 5 | One silver look; per-shot luma min 25-44 on the new renders, max jump 3.8. |
| 7 | Text | 5 | Seven labels from scan file names in clear black; bumper labels name the part while it comes off, "REMOVED" only on states. |
| 8 | Ending | 5 | Clean car, dip on the 10th downbeat where the drums thin, 720 px logo, music fades with it. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart, 774 frames; -16.5 LUFS integrated, true peak -1.6 dBFS (gain 0.88, skill ceiling -1 dBFS). |

Director flags kept on purpose: a1~d1 (bookends), h1~h2 and c1~c2 (same-camera continuations).
