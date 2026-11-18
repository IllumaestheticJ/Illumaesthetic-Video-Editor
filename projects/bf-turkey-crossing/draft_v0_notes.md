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

## v0.3 (owner: low-poly brown hen with a turkey tail + greeting/sale copy)
- **Hen:** `build_turkey_hen` (TURKEY_STYLE=hen). It's our own faceted model with an 11-slab turkey fan tail.
- **Card A:** "WISHING OUR DRIVERS A" (Unbounded 500) + HAPPY / THANKSGIVING (Akira), 18.023-21.181.
- **Card B:** BLACK / FRIDAY / SALE (Akira) + "UNTIL (END DATE)" placeholder (Unbounded 500, set with env BF_UNTIL), 21.181-25.239.
- **End card:** logo on 25.239, URL 0.2 s later, ends 27.04 + 0.4 s fade.
- **Checks:** 16.6 s, -13.9 LUFS, peak -4.1 dBFS, safe-zone text boxes OK.
- **Output:** `/home/user/media/work/out/bf-turkey-crossing_v0.3.mp4`.
- **Rebuild:**
  1. `TURKEY_STYLE=hen RDIR=.../renders_v03 tools/render_v0.sh`
  2. `BF_UNTIL="UNTIL <date>" python tools/compose.py --tag v0.3x --renders .../renders_v03`

## v0.4 (owner: ends Nov 30; logo + site in the same scene)
- Card B now reads BLACK / FRIDAY / SALE / UNTIL NOV 30.
- The Epsilon+ wordmark (720 px) and WWW.EPSILON.PLUS join it on the feather road scene at 22.982, over a soft dark band. There's no separate black logo card any more.
- It fades from the 25.239 hit.
- s6 was extended to f444 (frames 433-444; the camera holds its end pose).
- Checks: 14.8 s, -14.1 LUFS, peak -4.2 dBFS, safe-zone text OK.
- Output: `/home/user/media/work/out/bf-turkey-crossing_v0.4.mp4`.

## v0.5 (owner: OSRS assets from the owner's turkey.blend)
- **Turkey:** the OSRS Big Evil Chicken with its own tail, in turkey browns (TURKEY_STYLE=evil, OSRS_EVIL).
- **Trees:** 14 OSRS tree crowns on low-poly trunks (OSRS_TREES).
- **After the hit:** the OSRS feathers burst out and fall, and the OSRS bones lie on the road (OSRS_PROPS).
- **Assets:** extracted to `/home/user/media/bf-turkey-crossing/userblend/`, never committed.
- **Unchanged from v0.4:** text, timing and the logo scene.
- **Checks:** 14.8 s, -14.1 LUFS, peak -4.2 dBFS, safe-zone text boxes OK.
- **Output:** `/home/user/media/work/out/bf-turkey-crossing_v0.5.mp4`.
