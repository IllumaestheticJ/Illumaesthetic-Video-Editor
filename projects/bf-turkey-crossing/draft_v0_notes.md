# BF10 turkey-crossing: draft v0 notes (2026-11-18)

Output: `/home/user/media/work/out/bf-turkey-crossing_v0.mp4` (1080x1920, 30 fps, 12.2 s). Media is not in git.
Rebuild:
1. `tools/render_v0.sh` (Blender, about 25 min, 50 %, 10 spp).
2. `python tools/compose.py --tag v0`.

Assets needed in this container:
- `/home/user/media/cars/eps-toyota-gr-corolla-v23.glb`
- `/home/user/media/bf-turkey-crossing/music/transformation.mp3` (CML preview_url)
- the logo
- Akira in `assets/fonts/akira/`

Defaults used, pending the owner (shotlist.md open questions):
- Text: BLACK FRIDAY SALE.
- Gag: POOF + feather burst, turkey gone.
- Music: TRANSFORMATION.
- Car: Supersonic Red.

## v0.1 (parent/BF6, 2026-11-18)
- V2 rear spats seated with BF6's fit (`projects/bf-gr-corolla-track/spat_v2_fit.json`).
- s5 re-rendered.

## v0.2 (new owner rule: slow down under text)
- s6 (the feather fall under the text) now plays at half speed: f216-324, 3.6 s, two bars from 18.023 to 21.630.
- "SALE" stays fully readable about 2.6 s before the cut.
- Logo on the 21.630 hit; WWW.EPSILON.PLUS in at f330 and readable 2.6 s before a 0.4 s fade.
- Total 14.0 s. Loudness -14.1 LUFS, peak -4.2 dBFS. Safe-zone text boxes OK.
- Output: `/home/user/media/work/out/bf-turkey-crossing_v0.2.mp4`.
