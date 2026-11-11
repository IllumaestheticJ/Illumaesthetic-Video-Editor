# NFS-style car lot reel - source media

Media is never committed. Sources: `/home/user/media/nfs-carlot/`. Work dir: `/home/user/media/work/nfs-carlot/`.

## Game capture (Dropbox `/5. Claude Training/Good Reels (Epsilon)/`, renamed 2026-11-11 at the user's request)
| File | What | Used |
|---|---|---|
| `NFSU2 car lot - 1440p.mp4` (207 MB, 110 s) | phone screen recording of a PC no-commentary longplay; 1206x2622 rotated, ~59 fps VFR; game picture 2144x1206 at x 239 | picture and sound |
| `NFSU2 car lot - clean audio.mp4` (91 MB, 67 s) | second playthrough, 4:3, darker, ~38 fps; menu song also playing (track banner on screen) | not used |

Local: `/home/user/media/nfs-carlot/capture/`. Working copies: `a60.mp4` (60 fps, cropped, all-intra), `a.wav`.

Timecodes in the 1440p capture (frames of `a60.mp4`, 60 fps):
| Frames | Seconds | What |
|---|---|---|
| 0–600 | 0–10 | driving to the lot (YouTube player controls on screen for the first second) |
| 600–905 | 10–15.1 | rolling up to the car-lot marker |
| 905–1011 | 15.1–16.85 | "Would you like to enter the Shop?" prompt; Enter Shop lit from f1010 |
| 1012–1113 | 16.87–18.55 | cutscene, overhead: the 350Z turns in |
| 1114–1291 | 18.57–21.52 | cutscene, front: the 350Z drives past the camera; black at f1292 |
| 1297–3780 | 21.6–63 | comic-book movie (not used) |
| 3790–3815 | 63.2–63.6 | loading screen |
| 3818–3831 | 63.6–63.85 | menu up, turntable EMPTY at rest. **f3825 = clean plate** |
| 3832–3861 | 63.87–64.35 | first car slides in (half-speed version of the scroll) |
| 3861–5208 | 64.35–86.8 | car select: 15 scrolls, 14–15 frames each (list in `track.json`), holds 0.3–3.3 s |
| 5210– | 86.9– | "Do you want this stock 240SX?", save prompts, loading, drive-out |

Purchase (a60 frames): 5205-5212 cursor to Continue; 5213-5218 prompt fades in; 5218-5263 "Do you want this
stock 240SX?" (No is the default, cursor reaches Yes about 5250); 5264 bare scene, no UI (used to measure the
prompt's transparency); 5266- Save/Load. Real-time capture B: scrolls 50.03, 52.03, 53.30; prompt 54.10; Yes 55.30;
silent from 58.2.
Used in v5: intro f952-1291; menu f3829-3919, 4041-4112, 4631-4682, 4732-4791, 4947-4984, 5089-5103 + 5204-5212;
prompt f5213-5218 + 5234-5263.

Cursor in capture A (top-left of a 46x70 box): f3829-3919 at (1046,1032); f4041-4079 on the right arrow (1730,242),
then to the left arrow; f4631-4791 right arrow (1724,221); f4947-5103 left arrow (405,231); f5204-5224 on Continue
(1611,1087); f5224-5233 up to the No button; f5248-5254 across to Yes (700,731); click about f5263.
Used in v7 prompt: f5213-5218, 5224-5233, 5238, 5240, 5243, 5247-5263.

Capture B audio: voice message 35.1-44.6 s (mono, no music), menu music from 44.8 s.
Used in v8: menu f3829-3919, 4041-4112, 4631-4682, 4732-4785, 4947-4999, 5089-5103 + 5204-5212; audio B 34.83-45.49, then 53.22 on.

Capture B menu song: first hit 44.84 s, bar 1.1765 s (two-bar phrase 2.353 s).
Used in v9: menu f3829-3919, 4041-4112, 4631-4682, 4732-4785, 4947-4984, 5089-5103 + 5204-5212; audio B 34.83-44.92, then 53.16 on.

Used in v1: intro f952–1291; menu f3818–4040, 4041–4126, 4631–4731, 4732–4871, 5089–5208.
Earlier dead ends (YouTube download, playing nfsu2.xyz here): `knowledge/game-menu-reel.md`.

## Cars (Drive `Epsilon-final-GLBs-2026-10-15.zip`, file id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7)
See `cars.yaml`. Menu renders: `/home/user/media/work/nfs-carlot/cars/*.png`. Line-up check: `/home/user/media/work/nfs-carlot/lineup2/lineup_sheet.jpg` (sent to the user).
The first line-up (`lineup/`) used the older repo GLBs and had no EP3.

| Slot | Car | Model | Kit fitted |
|---|---|---|---|
| 1 | Toyota Corolla Hatchback E210 (Zenki) | `eps-toyota-corolla-hatch-e210-v18.glb` | lip, skirts, spats, WRC wing |
| 2 | Honda Civic Si sedan FE (11th gen) | `eps-honda-civic-sedan-fe-v10.glb` | lip, skirts, rear lip, sport wing on the Si duckbill |
| 3 | Acura Integra DE4 | `eps-acura-integra-de-v29.glb` | lip, skirts, spats, trunk lip, wing; flares hidden |
| 4 | Honda Civic Si EP3 | `eps-honda-civic-ep3-v17.glb` | lip, skirts, rear lip, rear wing |
| 5 | Mazda MX-5 NC | `eps-mazda-mx5-nc-v19.glb` | bumper, lip, canards, brake ducts, fender cuts, tyre spats, skirts, spats, GT wing |
