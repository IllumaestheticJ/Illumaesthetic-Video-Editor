# Self-review v1 - Epsilon+ Wing Configurator reel (training/rubric.md)

Deliverable: `/home/user/media/epsilon-wing-configurator/work/ewc_v1.mp4` - 1080x1920, 30 fps, yuv420p, H.264 + AAC 256k,
faststart, 1767 frames = 58.90 s, -13.1 LUFS integrated. Screen capture of the live configurator (no scans/IRL in this reel).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | GR86 3D scan + wing orbiting from frame 0; music drop at 2.57 s under the opening line. Not a transformation hook (no IRL in a UI reel). |
| 2 | Beat sync | 4 | Cuts placed on measured kick attacks of the track (40-120 Hz half-rise): 12/14 within +-14 ms of the music stem. 18.00 s and 48.70 s sit in drum fills (no clean kick) - nearest strong hit, ~10-40 ms. |
| 3 | 1:1 match | n/a | No IRL->scan transformation in a product-UI reel. |
| 4 | Scan quality | 4 | The car models are Epsilon's own configurator assets (GR86, NA Miata, FL5, C8 are labelled 3D Scan). Shown as the app renders them; scan fringes under the GR86 rear are visible in the outro. |
| 5 | Story | 4 | Narration-led walk through the app: cars -> wing -> setup/mounts/bases/AoA -> views -> fine-tune -> price/save/quote -> more options -> conclusion -> wordmark. One focus per shot (director pass). |
| 6 | Grade | 5 | Native app colours, captured losslessly frame-by-frame (fake clock). |
| 7 | Text | 4 | No added text: every word/number on screen is the app's own UI (prices, dims, labels). Narration numbers (72 cars, 45 scans) counted from the live Model list. Stage labels in the stacked desktop panes are small (rear view ~1.6x). |
| 8 | Ending | 5 | Epsilon+ wordmark (Drive EPSILON+ Logos, 720 px of 1080) on the cut at 55.57 s; track's last hit 58.45 s rings under it, audio fades with the card. |
| 9 | Technical | 5 | Exact-frame concat (no dup/dropped frames at cuts, verified by frame diffs); no static run > 0.3 s outside the logo hold after a 5 % push-in on UI holds. |

Known weaknesses / for the reviewer:
- 58.9 s is long for a reel; the brief asked for every feature + the fixed opening line. Narration is at natural pace (no atempo, per the approved processing); shortening the script is the lever if a shorter cut is wanted.
- Narration word timings were aligned from the pause map (28 phrases = 28 script clauses), not ASR (Hugging Face blocked).
- Some page chrome is cropped at pane edges (toolbar half-visible at the top of stacked panes).
- `ive director` "dead frames" flags refer to the raw clips; the delivered file's holds carry the push-in.
