# Self-review rubric (score 1–5, fix anything < 3 before delivering)

| # | Criterion | 5 looks like |
|---|---|---|
| 1 | Hook | something moves or transforms within the first 1.5 s |
| 2 | Beat sync | every cut within ±1 frame of a beat (`project.yaml: beats`) |
| 3 | 1:1 match | car silhouette overlaps within a few px at the cut (check overlay), cut on a beat |
| 4 | Scan quality | no ground scraps, floating debris, holes in hero areas; silver-on-black look |
| 5 | Story | viewer understands: real car → scanned → parts → (product) |
| 6 | Grade | no washed-out HLG clips, consistent warmth across IRL shots |
| 7 | Text | true data only, ≤2 items, never over IRL, legible on a phone |
| 8 | Ending | logo card on the last downbeat, audio fades with it |
| 9 | Technical | 1080×1920, 30 fps, yuv420p, AAC, faststart, no black/dup frames at cuts |

Record the scores in `projects/<name>/review.md` before delivery; reviewers' scores go in
`feedback.jsonl`. The gap between the two is what the next agent should learn from.
