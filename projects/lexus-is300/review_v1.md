# Lexus IS300 (first gen) Temerario-style scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/is300/out/lexus_is300_v1.mp4` — 1080x1920, 30 fps, 37.37 s (1121 frames), scan only, no text.
Shots: front 3/4 turntable → rear 3/4 orbit → wheel ECU → headlight/grille slide (on the drop) → front bumper lifts off
→ trunk lid opens → rise to top-down → exploded view (front/rear bumper, right skirt, trunk lid) locks on the last hit → logo on the tail.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Camera orbits from frame 0, but the first transformation (bumper off) is at 13.1 s; first 5 s is a slow turntable by design (Temerario reference). |
| 2 | Beat sync | 5 | Measured on the delivered file: cuts at frames 158/275/315/393/510/628/706/941 = planned; kick onsets within ±15 ms of every cut. Beat-48 logo cut is after the last hit (no kick there, by design). |
| 3 | 1:1 match | n/a | No IRL footage in this brief. Part registrations checked red-over-silver (rmse 2.4–3.2 mm). |
| 4 | Scan quality | 3 | 2022 Artec scan: glass is open (holes in windscreen/side glass), wiper/cowl scraps, rough tyre edges in the wheel ECU. Front-bumper part derived (car − bumper-removed state) has a slightly ragged lower edge. Licence plate is readable in the scan (left as captured — ask before publishing). |
| 5 | Story | 4 | Whole car → details → panels open → top-down → parts separate and reassemble → logo. Explode is 4 panels (only those with part/state scans). |
| 6 | Grade | 4 | No IRL. House satin silver at −0.5 EV (car median luma ~205 vs Temerario ~200). |
| 7 | Text | 5 | None. |
| 8 | Ending | 5 | Explode locks on the last hit (30.05 s), holds 2 beats, logo on beat 48 over the music tail, fades out with it. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC; no black or duplicate frames at cuts. |

## Notes for the next agent
- v1 assembly had every cut 2 frames early: first clip `dur` must be (first cut frame − 1)/30, check with frame diffs.
- Top-down ends nose-down and the explode starts nose-up from behind: a deliberate hard flip on beat 36.
- The OEM trunk scan only registers against a rear-deck crop of the car (whole-car ICP was inconsistent).
