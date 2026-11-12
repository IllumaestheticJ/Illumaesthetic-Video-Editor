# Nissan Frontier Pro-4X scan reel v3 - self-review (training/rubric.md). v2: review_v2.md, v1: review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v3.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.37 s, 1151 frames.
User notes on v2 and what changed:
- "Logo too small" -> 700 px wide (v2 380).
- "Front bumper removed scan shows bumper parts leftover on the truck" -> truck's bumper skin removed by diff against the
  bumper-off state (composite.py --remove-diff), detached scan debris dropped (attached.py). S3/S4/S5/S6 now show only the state scan.
- "Hood needs to open normally to show underside" -> hinge fitted to the propped-open hood fragments in two state scans
  (33.5 / 35.5 deg, 7.2 / 5.1 mm median); hood opens, stays open through structure + flares, closes in the reassembly.
- "Flare section has a lot of artifacts; need to show backside" -> flares re-cut to the four arch bands; right-side flares pull
  out onto black under the truck and turn 180 deg.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole truck orbit from frame 1 (v2 render) |
| 2 | Beat sync | 5 | cuts vs decoded audio onsets: -15.1/+9.9/+7.8/-5.1/+0.4/-10.0/-14.6 ms |
| 3 | 1:1 match | n/a | scan-only |
| 4 | Scan quality | 4 | no leftovers/debris in the bumper-off shots, clean flares; hood underside and flare backs are the reverse of the outer skin (not scanned); no wheels |
| 5 | Story | 5 | front -> side -> rear, one section per shot, hero bumper-removed beat |
| 6 | Grade | 4 | luma clean in every render |
| 7 | Text | 4 | one label per section, all in clear black except none over the subject |
| 8 | Ending | 5 | parts home on accents, fade, larger logo |
| 9 | Technical | 5 | exact frames, no dup frames |

Known gaps: S7 crops the nose slightly at the right edge; parked bumper partly clipped at the lower edge in S5/S6.
