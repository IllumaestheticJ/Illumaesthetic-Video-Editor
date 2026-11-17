# BF 9 days-left-countdown: draft v0 notes (2026-11-17)

This is a quick first draft made because the owner asked, through the parent session, for a quick short first draft of every BF video. It is preview quality and **not approved for posting**.

Output: `/home/user/media/work/out/bf-days-left-countdown_v0.mp4` (media is not in git).

## Assumptions (my defaults for the open questions in shotlist.md)
| Q | Default used in v0 |
|---|---|
| Q1 Sale end date | **Unknown.** v0 renders a single sample day, **"3 DAYS LEFT"**. **The 3 is a placeholder number**, not computed from a real end date. |
| Q2 Which days | Only the 3-day sample. |
| Q3 End date on screen | No date anywhere. |
| Q4 Offer line | None. The end card says "BLACK FRIDAY" with no price or percent. |
| Q5 Numeral style | A: a silver numeral built by the cyan scan sweep (Blender geometry from `--text`). |
| Q6 Del's gesture | Tape-roll tap (no watch; the locked sheet has none). In v0 it's only a small dip on the hits. |
| Q7 Music | **Changed:** "BREAKING NEWS" - DJ DF KIT (TikTok CML 7622371201206765569), from 0 s. DJ EV's "BLACK FRIDAY" is quiet until about 27 s, so it has no usable hit in a 9 s reel that starts at the song's beginning. Source file: CML preview download, full length 72.8 s. |
| Q8 Car in shot 1 | Integra DE GLB (`eps-acura-integra-de-v29.glb` from the website zip, Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7). Kit: lip, skirts, spats, Sport Wing, trunk lip; flares hidden. Rendered silver as one still with a 5 % push. The BF 2/3 plates don't exist yet. |

## Placeholders (not final)
- **Del & Eps:** cut-outs of the front views from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`. On screen they are labelled "placeholder art (model sheet), not final".
  - They are static: there is no scan-raise or eye change, and no real tape tap.
  - No Higgsfield credits were spent. That needs your OK in this chat.
- The plate is the website CGI model in the silver look, not the car's real scan.

## Timing (measured on the decoded audio, 30 fps)
| Frame | Time | Event |
|---|---|---|
| 0 | 0.00 | Shot 1: Integra + Del. Tape dips at 0.34 s and 1.23 s (low hits) |
| 59 | 1.967 | Cut on the 1.96 s hit. Shot 2: black, Eps, scan sweep starts |
| 139 | 4.633 | Drop (RMS rise 4.62 s): numeral completes in silver, key-light flare |
| 154 | 5.133 | "DAYS LEFT" slams in (5.13 s hit) |
| 180 | 6.000 | Del slides in (6.01 s hit) |
| 208 | 6.933 | Cut on the 6.92 s hit: wordmark card (720 px), BLACK FRIDAY, EPSILON.PLUS |
| 282 | 9.400 | End (picture fades over the last 14 frames, audio fades from 8.8 s) |

## Render cost measured
- Numeral 1080x1920, Cycles CPU, 16 samples: about 6.5 s/frame, 149 frames, about 16 min per number.
- Plate still: one frame at 64 samples.
- Compositing and encoding: about 1-2 min.
