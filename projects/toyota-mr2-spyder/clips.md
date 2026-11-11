# Toyota MR2 Spyder scan reel (Temerario style) - sources

Scan only: no IRL footage, no text. Brief: Temerario-style reel (see training/references/README.md `v_jul22_1047_58`).

## Scans (engineering Drive `Toyota MR2 Spyder` 1Apk8IymqNIM5osub5qZzzQxO7airXf8G)
Listed recursively with the service account. Downloaded to `/home/user/media/toyota-mr2-spyder/scans/`, decimated
(vertex clustering) to `dec/*_3mm.stl`, levelled with the full car's transform (`tools/level.py`, `level.json`) -> `dec/*_L.stl`.

| file (Drive id) | size | date | what it is | used? |
|---|---|---|---|---|
| MR2 Spyder Scan Data/Full Car.stl (1Ex6611DaBiKuLZi9ZypOaqcwZdstSqbb) | 977 MB, 19,540,297 tris | 2023-03-22 | full car, **hardtop on**, wheels captured, no ground plane | base car |
| MR2 Spyder Scan Data/Full Car Top Down.stl (1F1JS1meWgjj3xeYpM8Su-FV6bZC07H1X) | 750 MB | 2023-03-22 | full car, **roof down**, interior visible | see registration below |
| Hardtop Mounting/Hardtop Mounting Full Car.stl (17NMhkW5...) | 927 MB | 2024-12-25 | roof-down full car (same size as "Copy of Full Car Top Down") | frame for the 2024 rear states |
| Hardtop Mounting/MR2 Spyder Rear Interior Trim Removed.stl (17UZP0D9...) | 250 MB | 2024-12-26 | rear cabin with trim off (partial) | see below |
| Hardtop Mounting/MR2 Spyder Trunk Open Cover On.stl (17TvP2vi...) | 250 MB | 2024-12-26 | rear end, trunk lid open (partial) | see below |
| MR2 Spyder Rear End trunk open.stl (1Qun_twV...) | 350 MB | 2023-06-10 | rear end, trunk open | see below |
| MR2 Spyder Rear QuarterPanel.stl (1_NEQlDP...) | 50 MB | 2023-11-27 | one rear quarter panel | see below |
| Front Bumper Data/front fully removed.stl (1IaI7tQJ...) | 50 MB | 2022 | front end, bumper + hood off | see below |
| Front Bumper Data/hood open no bumper.stl (1IjrsQ6I...) | 50 MB | 2022 | front end, hood open, bumper off | see below |
| Front Bumper Data/hood closed no bumper.stl (1Id9y9SV...) | 50 MB | 2022 | front end, bumper off | see below |
| Front Bumper Data/Hood Open (Tab Ref).stl (1a3Y6DlZ...) | 151 MB | 2023-03-20 | front end hood open | see below |
| FrontEnd.stl (14RbGhZd... / 1aDvpyPv...) | 133 MB, ASCII | 2023 | front end | not decimated (ASCII STL) |

Not used (not our scan data / not needed): Bumper Project, Aero Wing V1, Ducktail, Wing, Parts (printed parts, CAD),
`2001 Toyota MR-S S Edition ZZW30` (GameModels.ru game model = aftermarket CAD), MR2 Spyder Plug, Side Mirrors CAD,
Suspension Data (1.25 GB, not in the brief), Roof latch / roof edge detail scans, Print Evaluation hardtop revision.

## Frame conventions (after tools/level.py + ive prep)
Ground z=0, long axis Y, **nose at +Y**, rear at -Y. tools/shot.py camera az: 0 = behind the car (-Y side),
180 = in front of the nose, -90 = camera on -X side.

## Logo
`IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com/cdn/shop/files/ (6135x1059 RGBA) ->
`remotion/public/illumaesthetic_logo.png` (gitignored). The homepage itself is behind a Cloudflare challenge; the CDN path is not.

## IRL footage (not used in this scan-only reel - noted for a future 1:1-cut version)
| Dropbox folder | contents |
|---|---|
| `/2. Illumaesthetic Videos/1. Video dumps/MR2 HARDTOP` | 185 entries, 2025-07-11..16: Sony FX30 clips (`FX30504..523`, `FX30556..571`, `FX30633..649`, `FX30_4582..4605`, 67 MB-4.4 GB) + DJI Osmo clips (`DJI_202507..._00xx_D.MP4`, up to 9.3 GB, with .LRF proxies) + a `*REEL` subfolder. Hardtop fitting / mounting shoot - matches the Hardtop Mounting scan folder (2024-12/2025-07) |
| `/2. Illumaesthetic Videos/1. Video dumps/MR2 Kalvin footage` | 63 Sony FX30 clips `FX30_3993..4055.MP4` (2025-06-16/17, 67 MB-1.9 GB) with XML sidecars |
For a 1:1 cut, pick frames where the car is in the same state as a scan (hardtop on -> Full Car; roof down -> Full Car Top Down).
Not downloaded or watched for this reel.
