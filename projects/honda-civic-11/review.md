# Honda Civic FE1 — Epsilon kit reel v4 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/civic/out/civic_fe1_epsilon_v4.mp4` — 1080×1920, 30 fps, h264/AAC, 833 frames = 27.77 s.
v4 answers the user's v3 notes: logo too long, whole video too slow, make it an Epsilon video (install lip, skirts, apron,
wheels, wing through the scan data), end on one of Ron's renders. Plan: `direction.md` "## v4 (Epsilon)" (scene-director).
Earlier reviews: `review_v3.md`.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | audio starts 1.27 s before the drop; whole car moving from frame 1, doors open ON the drop |
| 2 | Beat sync | 5 | 13 hard cuts measured on the decoded audio: −2, +1, +8, +3, −3, −1, −7, +5, +14, +5, −2, −15, −12 ms (all ≤ ½ frame). Each install seats on the next hit of its bar |
| 3 | 1:1 match | 3 | scan + kit → Ron's render 1 (hard cut on 36.471). Camera solved by silhouette + both wheel centres (IoU 0.80, wheels within 12 px of 1920). Looked at the overlay: wheels, doors, roofline coincide; nose and wing differ up to ~40 px because Ron's car is lowered and the scanned car sits ~3° nose-down |
| 4 | Scan quality | 4 | as v3; new wheels replace the scanned ones, so the incomplete right-rear wheel is gone after the swap. The cut-out scanned wheels carry some hub/liner fragments (visible for ~0.6 s as they leave) |
| 5 | Story | 4 | whole car → doors open → trunk opens → interior → close → stock nose → lip → stock wheel → wheel swap → skirts → apron → wing → full kit → Ron's render. One focus per shot, no shot reused (N3b is a later window of the trunk render used as a cut-in). Install order differs from the user's list (wheels second) to keep side and rear continuous |
| 6 | Grade | 4 | house silver on black; kit white and rims gold as in Ron's render; the cut to the render changes body colour silver → white |
| 7 | Text | 5 | only the Epsilon+ wordmark (Drive `EPSILON+ Logos`), 300 px, last 1.5 s, on the render's black; no numbers |
| 8 | Ending | 4 | render holds 3.3 s with a slow push shared with the scan still before it; wordmark arrives at +1.85 s; no Illumaesthetic logo |
| 9 | Technical | 4 | per-frame luma scan of the delivered file: no dropouts (largest non-cut step 3.1 at f452 = wheels entering frame); part motion uses rendered 30 fps in-betweens; holds are 50/50 blends of 15 fps frames (slow pushes only). Music is still the v1–v3 track: the user's replacement song could not be downloaded |

## Open items
- **Music**: user asked for youtube AECgTogQV-0 via a "yt audio downloader skill" — not present in any session/branch, YouTube blocked. Waiting for the audio file; every install seats within ≤1.26 s then holds, so the shots re-time by trimming.
- **Kit source**: parts are the Epsilon lookbook model (eps-honda-civic-sedan-fe-facelift-v9) fitted to the scan (body ICP, scale 1.0099, median 9.9 mm) — not scans of physical parts. Lip/apron revision vs Ron's render not confirmed.
- **Doors/trunk closed during installs** (wing sits on the closed lid; open doors would show unscanned inner faces) — the user's "once the parts are opened up" could also mean installing while open.
- Right-side wheels swap unseen during I2 (popped, hidden by the body).
