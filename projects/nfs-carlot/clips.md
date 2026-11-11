# NFS-style car lot reel - source media

Media is never committed. Work dir: `/home/user/media/work/nfs-carlot/`.

## Game capture - chosen, NOT YET DOWNLOADED (blocker, 2026-11-11)
Nothing in Dropbox or Drive. User cleared use of the game's assets and approved `www.youtube.com` plus two
video hosts for the environment.

Chosen source: **"Need for Speed Underground 2 Full Gameplay Walkthrough [PC Longplay Playthrough] No Commentary"**
(GameWalk Tutor, `youtube.com/watch?v=tt4LXox7vb4`, 11 h 12 m, PC, no commentary; 1080p60 H.264 = format 299,
audio = 140; 1440p60 is VP9 only). Only the first ~12 minutes are needed (intro drive, car lot, car select).

Other candidates looked up (metadata only): `3AUpXdmoSaY` PS2/PCSX2 1080p60 12:21; `xIymlHq_KSI` 4K60 but a
remaster mod (not the original look); `0OklyrtDEPw` PC longplay 720p60; `46pRaTOoR9w` 1:22 intro FMV only.

What happened: `yt-dlp` reads metadata and formats fine. The partial download (`--download-sections "*0-720"`)
fails because ffmpeg cannot open the stream through the session proxy, and the two fixes (ranged `curl`, or
`yt-dlp --proxy $HTTPS_PROXY`) were refused by the session's safety check. Not retried. Waiting on the user:
either the first 12 minutes of that video dropped in Dropbox, or permission for the download command.

## Cars (Epsilon-Site GLBs)
See `cars.yaml`. Line-up check render: `/home/user/media/work/nfs-carlot/lineup/lineup_sheet.jpg` (sent to the user).

| Slot | Car | Model | State |
|---|---|---|---|
| 1 | Toyota Corolla Hatchback E210 (Zenki) | `eps-toyota-corolla-hatch-e210-v3.glb` | lip, skirts, spats, WRC wing - looks right |
| 2 | Honda Civic Si sedan FE (11th gen) | `eps-honda-civic-sedan-fe-v4.glb` | lip, skirts, rear lip, sport wing on the Si duckbill - looks right |
| 3 | Acura Integra DE4 | `eps-acura-integra-de-v8.glb` | lip, skirts, spats, trunk lip, wing; flares hidden - looks right |
| 4 | Mazda MX-5 NC | `eps-mazda-mx5-nc-v2.glb` | Epsilon bumper, canards, spats - looks right |
| ? | Honda Civic Si EP3 | none | only a bare 30k-tri scan in the wing configurator; no kit model. Waiting on the user |
