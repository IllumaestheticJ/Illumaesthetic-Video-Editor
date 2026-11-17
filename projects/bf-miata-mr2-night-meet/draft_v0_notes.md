# bf-miata-mr2-night-meet: draft v0 / v0.1 notes (2026-11-17)

**v0.1** (`/home/user/media/work/out/bf-miata-mr2-night-meet_v0.1.mp4`) re-cuts v0 with no Del & Eps (owner, e05c325; the
relayed instruction reached this session only after v0 was rendered).
- Shots 2 and 8 are scan-only. The shot 8 label moved below the car.
- Shot 10 is the two kitted silver scans with "MR2 SPYDER + NC MIATA / EPSILON+ · FIBERGLASS AERO".
- Loudness and cut frames are unchanged: 24.1 s, -14.2 LUFS, TP -1.8 dBFS.
- The 1.5 Higgsfield credits spent on the v0 stills are not reused. Item 5 below applies to v0 only.

The user said "go" in chat after the owner asked (via the parent session) for a quick, short first draft from every BF agent.
The draft is preview quality: Cycles CPU at 540x960, 12-16 samples, rendered at 15 fps, each frame doubled to 30 fps and
upscaled to 1080x1920.

Output: `/home/user/media/work/out/bf-miata-mr2-night-meet_v0.mp4` (media is not committed).

## Assumptions (my defaults for the open questions; each one needs owner confirmation)
1. **Card title:** "BLACK FRIDAY / 20% OFF / MR2 SPYDER + NC MIATA AERO". The tier includes the ABS duckbill and the MR2
   front bumper has no deal, so "Fiberglass 20% off" was not used.
2. **Prices:** the full list, struck-through Current Price -> BF 2026 Price, from `projects/_blackfriday/PRICES.md` /
   `bf_liquidation_pricing.csv`.
   - MR2 Spyder: skirt/fender combo $700 -> $560, rear spats $350 -> $280, eyelids $100 -> $80, hood vents $400 -> $320,
     duckbill $220 -> $176.
   - NC Miata: bumper + lip $1,100 -> $880, fender cuts $300 -> $240, side skirts $500 -> $400, NC1 rear spats
     $250 -> $200, canards $200 -> $160.
   - No dates, no stock counts.
3. **MR2 front bumper ("No deal"):** stays on the CGI car (it is part of the lookbook kit) but is never named, labelled or
   listed.
4. **NC kit:** bumper + lip, fender cuts, side skirts, rear spats, canards. No GT wing, brake ducts or tire spats.
5. **Del & Eps:** three Higgsfield GPT Image 2.6 stills (medium quality, transparent background), with
   `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg` as the reference image. Cost: 1.5 credits (balance before:
   285.28). Job ids:
   - 4d50ffbf (Eps scanning)
   - 2f63562d (Eps pointing)
   - c58331a5 (Del hands Eps the 10 mm)

   They are composited as flat 2D cut-outs with a soft contact shadow; they are not 3D-placed at 1:1 scale yet. The 10 mm
   sting is silent and is a still pose, not animated.
6. **Music:** "Tokyo Midnight" by ChilliZone (TikTok CML, song_clip_id 7667576607158323217), claimed in MUSIC.md.
   - The full 173.5 s file came from the CML preview URL.
   - It starts at 0 s, the track's beginning.
   - The cuts sit on the half-rise attacks measured in the source wav: 1.920, 4.380, 5.187, 5.997, 7.684, 9.305,
     11.830, 14.436, 16.069, 18.331 and 21.663 s. `ive beats` strong onsets ran ~100-150 ms late on this track.
   - The video ends at 24.1 s on the logo, with a 1.4 s fade.
7. **Night lot:** fully CGI. It is a new simple procedural lot (wet asphalt, sodium spot lamps, haze, dim buildings, cyan
   neon), not the MR2 reel's `city_env.py`. No real night-meet footage was sheeted for v0.
8. **Labels:** short scan labels (part name + "car · FIBERGLASS") in PIL with Inter Display / JetBrains Mono, not the
   Remotion ScanHUD. The card and logo are PIL frames too.

## Known v0 shortcuts / problems to fix in v1
- **Scan-to-model fit:** a new quick PCA + trimmed ICP (`tools/scan_to_glb.py`).
  - NC median fit is 14 mm.
  - The MR2's median reads 49 mm because the open interior and roll bar inflate it. The outline matches in projection
    checks, but it is not a precise fit.
- **Stock zones:** "comes off" = scan triangles within 30 mm of the lookbook stock and part surfaces (`tools/cutparts.py`).
  This is not the shut-line trace or the removed-state scans the lessons ask for. The NC bumper does not use the
  bumper-only scan, and the cut edges and gaps around the arches are visible.
- **Wheels:** the scan wheels (10-spoke MR2, NC) differ from the lookbook wheels, so the 1:1 CGI -> scan cut changes the
  wheels.
- **MR2 nose:** the scan shows the stock front intake while the CGI car carries the Epsilon bumper.
- **Look:** kit parts on the scan use the same silver as the scan.
- **Quality:** preview res and samples, interpolation-free 15 -> 30 fps frame doubling (motion steps are visible).

## Checks run on the v0 file
- **Format:** 1080x1920, 30 fps, 24.1 s, h264 + AAC.
- **Cuts:** frame-diff cuts land exactly on the planned frames (58, 131, 156, 180, 231, 279, 355, 433, 482, 550, 650,
  723).
- **Audio sync:** measuring the attacks in the final mix was inconclusive on this syncopated track. The cut times were
  measured on the source wav, which is muxed from 0 s with a static gain, so sync is correct by construction within one
  frame. A kick-band grid fit (lessons L96/L185) should confirm it in v1.
- **Loudness:** -14.2 LUFS integrated, true peak -1.8 dBFS (static -0.7 dB gain + limiter; one-pass loudnorm overshot to
  +0.9 dBFS TP after AAC).
- **Contact sheet:** `/home/user/media/bf-miata-mr2-night-meet/work/contact_v0.jpg`. All shots read, and no car is off
  screen in shot 10 after a re-frame.
- **Known tight crops:** shot 5 crops the MR2's rear left edge, shot 7 crops the NC nose as the bumper lands, and shot 9
  is close on the NC door.
