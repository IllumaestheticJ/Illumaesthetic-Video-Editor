# bf-scan-teardown-prices: v0 quick draft (2026-11-17)

The owner said "have all the agents make a quick short first draft", relayed by the parent session. This is a preview-quality
v0 of `shotlist.md`. The plan's open questions are still open; every default taken here is listed below.

- **Output:** `/home/user/media/work/out/bf-scan-teardown-prices_v0.mp4`. 1080x1920, 30 fps, about 23.6 s.
- **Tools:**
  - `tools/prep_v0.py`: builds the scene;
  - `tools/render_v0.py`: shots T1 and T2;
  - `tools/ron_still_v0.py`: Ron's end frame;
  - `tools/overlays_v0.py`: price cards, tags, end card and character placeholders;
  - `tools/assemble_v0.py`: final mp4.

## What changed against the plan, and why

- **Scan and kit come from Ron's own design file,** not our prepped FE1 scan. `Civic 11th gen lip kit review.blend`
  (19ySWB7EGGFfgjQNo-3tOxTTIoKiv0E3w) has his copy of the FE1 facelift scan (`FE1 Fl`) and the kit pieces in one frame:
  - `FrontFL1-3` = front lip;
  - `SideDriver1/2` and `SidePass1/2` = skirts;
  - `Rear1-3` = rear lip.

  `wing.002`, the wheels `*.001` and `Camera.006(L5)` come from `Honda Civic Sedan 2022-render.blend`
  (1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ), which shares that frame. So the placement is Ron's design placement: the approved v5 chain
  without the ICP step, and no re-download of our 1.25 GB scan.
- **Scan decimation:** the file holds two 20M-face scans and OOM-killed Blender (14 GB). I loaded only `FE1 Fl` and
  vertex-clustered it at 5 mm in numpy (20.2M → 2.1M faces). Faces with centroids below z = 12 mm (floor scraps) were dropped.
  Check: none.
- **Wheels:** Ron's copy of the scan has its wheels cut out, so the car wears Ron's gold wheels `*.001` (as in v5).
  That is also what the 1:1 cut needs. They get no price and no label.
- **No nesting pass in v0.** The kit parts are add-ons (lip, skirts, rear lip, wing), and in Ron's file they sit on his scan
  as designed. The GLB `body_<part>_stock` footprint nesting from the plan is left for v1.
- **Render quality:** Cycles at 32 % resolution (346x614, upscaled to 1080x1920), 8 spp + OIDN, 15 fps, frames doubled to 30.
  Soft, aliased and noisy by design: it's a timing and story draft.
- **Kit look:** unpainted PU / gloss black (dark grey, roughness 0.42) on the house silver scan.
- **Eps's scan line:** a cyan (#6fc3d6) band sweeps the car nose to tail from 0.81 s to 2.16 s, rendered on the scan surface.

## Music (claimed in MUSIC.md)

- **Track:** Kim Petras "XXX", from `/Moosic` (id:ihAynaYnO_4AAAAAAACmaA), played from the song's start.
- **Grid:** 111.65 BPM, beats at 0.024 + 0.5374·k s.
  - The first 17 s are an intro without kicks; its hits sit on the same grid.
  - The kick enters on beat 32, at 17.235 s.
- **Re-timed to the song:** the teardown plays over the intro, and the kit flies home and **locks on the kick entry**.

| Event | Song = video s | Source |
|---|---|---|
| Kit unlocks (lift 2 cm) | 2.159 | intro hit |
| Front lip off | 4.296 | intro hit, beat 8 |
| Side skirts off | 6.432 | intro hit, beat 12 |
| Rear lip off | 9.381 | section hit |
| Wing up | 11.262 | intro hit, beat 21 |
| **Cut** T1 → T2 (top view) | 13.398 (frame 402) | onset |
| Fly home starts | 14.466 | onset, beat 27 |
| **All parts lock** | 17.235 (frame 517) | kick entry, beat 32 |
| **Hard 1:1 cut** to Ron's render | 19.390 (frame 582) | kick |
| **Cut** to end card | 20.985 (frame 630) | kick |
| End (fade in the last 0.5 s) | 23.6 | |

Loudness is set at the mux to -14 LUFS, with true peak below -1 dBFS. The measured values are in `review_v0.md`.

## Defaults taken for the open questions (plan sec. 7)

1. **Car:** Civic FE1 (the parent confirmed the backordered FE parts are on sale).
2. **Prices** are from `projects/_blackfriday/PRICES.md` (the liquidation sheet), unpainted / gloss black only:
   - FRONT LIP $285 → $199.50;
   - SIDE SKIRTS $400 → $280;
   - REAR LIP $285 → $199.50;
   - SPORT WING $450 → $315.

   No stock counts and no dates.
3. **Wording (my placeholder; replace with yours):**
   - Opening: "BLACK FRIDAY".
   - End card: Epsilon+ wordmark (720 px), "BLACK FRIDAY", "30% OFF THE CIVIC FE KIT", "EPSILON.PLUS". The 30 % is the sheet's
     tier for all four parts shown.
4. **Wing:** Ron's `wing.002` is taken as the FE Sport Wing (Si duckbill variant) the price card names. Not yet confirmed.
5. **Wheels:** Ron's gold wheels, so the end is a 1:1 cut to his render at the same camera.
6. **Stock:** nothing on screen.
7. **Music:** Kim Petras "XXX" (claimed; lyrics not reviewed for ads; a /Moosic rip, not cleared for paid ads).
8. **Del & Eps: PLACEHOLDERS.** No Higgsfield credits were spent on v0. They are cut-outs from
   `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`, keyed off its grey background, each stamped "PLACEHOLDER":
   - Eps at full size beside the car while his scan line sweeps (0.25-2.6 s);
   - Eps and Del in micro mode over the exploded top view (13.45-14.4 s).

   They are 2D stickers, not posed or lit to the shot. v1 would generate posed plates with the sheet as the reference.
9. **Kit colour:** real black finish.
10. **The "1:1" end frame is a portrait re-render of Ron's scene,** not his delivered landscape render 7. It uses his `Camera.006(L5)`
    position and direction, a 72 mm lens and a 20.25 mm sensor, Cycles 48 spp at 50 %. The scan shot ends on exactly the same camera.

## Known v0 shortcuts to fix in v1

- Full resolution and samples; real 30 fps renders for the part moves (the v5 merge30 lesson).
- No `pathcheck` / `clipcheck` run on the flight paths yet. They were checked visually on the contact sheets only.
- Footprint nesting from the website GLB `eps-honda-civic-sedan-fe-facelift-v9`.
- Real Del & Eps plates (Higgsfield, the model sheet as the reference), composited with contact shadows.
- Fjalla One / Barlow (site fonts). v0 uses Inter Display.
