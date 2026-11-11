# Self-review — Porsche 911 GT3 (992) scan reel, v2

Output: `/home/user/media/work/gt3/out/porsche_gt3_992_v2.mp4` (33.0 s, 1080x1920, 30 fps; not in git).
Order (direction.md): FRONT whole car -> lid opens over frunk scan | FR brake | side skirt off |
REAR wing detail -> wing/bumper/diffuser/lip off on the drop -> exhaust behind the bumper -> parts lock home |
top-down -> fade -> small logo.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | Frame 1 is the whole car with the camera already moving. The lid starts on the 4.15 accent. |
| 2 | Beat sync | 5 | Cuts were measured on the decoded audio of the delivered mp4 (1 ms RMS half-rise): +16.3, -16.3, +10.9, +13.3, -12, -11, -9, -13.8 ms. All are within ±½ frame. The 299→298 move is in the editlog. |
| 3 | 1:1 match | n/a | Scan-only reel. The n5→s6 cut is a same-camera invisible cut: the frames match on the contact sheet. |
| 4 | Scan quality | 4 | Silver on black. The bumper-off composite is fragmented above the exhaust, so n4 stays tight and low on the tailpipes, silencers and pipes. The FR wheel-arch scan edge is ragged at the top of s3, kept small by the tighter framing. |
| 5 | Story | 4 | One continuous sequence per section, travelling front→side→rear, with the bumper-removed data as the hero beat on the drop. It has no IRL leg because the brief asked for scan only. |
| 6 | Grade | n/a | No IRL footage. |
| 7 | Text | 4 | Six one-at-a-time labels: the user's brief (addendum C) asked for short factual labels, which overrides the rubric's limit of 2. The labels are names only, with no numbers. Every label window was checked so the labels stay off the silhouette (FRUNK and EXHAUST were moved) and inside the 80 px margins. |
| 8 | Ending | 5 | The top-down fades to black from 29.94 s, then a small 300 px logo lands on the 30.9 hit. The audio fades over the last 0.4 s. |
| 9 | Technical | 5 | h264 yuv420p, 1080x1920, 30/1, AAC, faststart. No dark frames: luma scan of all 8 shot folders. Frames ±1 around every cut were checked, with no black or duplicate frames. |

## Checks run
- Luma-dropout scan of every render folder: clean. Persistent data was off.
- Contact sheets of the first, middle and last frame of every shot (`chk/final2/fml_a.jpg`, `fml_b.jpg`), plus frames around each cut (`chk/v2cuts/sheet.jpg`) and each label window (`labelwin.jpg`, `labels2.jpg`).
- `ive director` on v2 flagged two "repeats", both accepted with reasons in the editlog:
  - n5/s6 is one continuous camera.
  - n1 (lid and frunk from above) vs n2 (low grazing sill) share only a front-right direction.

## Known weak spots / for the next agent
- The side skirt only reads at a low grazing angle. Side-on, it is lost against the door.
- `ive assemble` ends one frame short of the planned 990 frames (989), because the last clip gets no cut hold. That frame falls on the logo, so it doesn't matter here.
- The relayed brief had no front-bumper-removed scan or engine-lid-open scan, so neither is shown (rule D).
