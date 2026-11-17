# bf-integra-stock-to-kitted: draft v0 - v0.6 notes

**v0.6 (2026-11-17, owner via parent: "all agents should use www.epsilon.plus"):** the end card has WWW.EPSILON.PLUS under the Epsilon+ wordmark. It is set in Barlow 700, 60 px, grey #B2B2B2, and fades in and out with the logo. The end card's content spans x 180-899 / y 921-1138, inside the safe zone. This replaces assumption 7 below ("no epsilon.plus on the end card"). Output `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.6.mp4`; sheet `_v0.6_safezones.jpg`.

**v0.5 (2026-11-17, user: "the beginning needs to convey that we are running a black friday sale, maybe flash a text behind the car to the beat"):** output `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.5.mp4`.
- **Intro (0-6.99 s, CGI only):** the words "BLACK" (white) and "FRIDAY" (sale red), in Barlow 700 at 260 px, alternate *behind* the stock scan car.
  - **Timing:** one word per hi-hat/clap hit of "140". The first hit is at 0.215 s, then every 0.43073 s (measured onsets, on the beat grid).
  - **Flash:** each word pops to full on its hit and settles to 28 % over 0.28 s.
  - **Placement:** once the car fills the frame (hit 8 onward) the word rides above its roof at y 300.
  - **Drop lead-in:** the last two hits before the drop show "BLACK / FRIDAY" with a red SALE badge, holding at 75 %.
- **Safe zone:** all text is inside x 48-920 / y 285-1440 (`_v0.5_safezones.jpg`). No text over IRL footage.
- **Unchanged:** cuts, music and loudness (-13.7 LUFS / -4.3 dBTP).

**v0.4 (2026-11-17, owner safe-zone rule):** the kit shot is scaled to 60 % and placed in x ~173-907 / y ~700-1436. The card starts at y 300. Before: `_v0.3_safezones.jpg`. After: `_v0.4_safezones.jpg`.

**v0.3 (2026-11-17, user: "zoom out a little ... it's cropped out and too close"):** output `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.3.mp4`.
- **Real clips:** the 9:16 window of the 4K clips is wider: 0371 is 1800 px (was 1215), 0370 is 2050 px (was 1080), so the whole car fits.
  - The frame is scaled into a band over a blurred, darkened fill of itself (`tools/widen.sh`).
  - 0371 pans x0 1600 → 700, nose to wing.
- **Stock pass:** re-rendered on the matching wider crop camera (sensor 16.875 mm, shift 0.322 / 0.156). The 1:1 still lines up (`render/s1_wide_check/sheet.jpg`).
- **Grey Integra:** the user asked to use footage of the grey car (the white car carries the printed version of the kit). I searched Dropbox: the 'Integra' and 'gray' searches, `Footage Library/Videos/Car Shots` (12 clips), and the Shoot Sessions folders for wing product clips and the 2025-04-17 test drives. I found no grey Integra video. The user has been asked where it is.

**v0.2 (2026-11-17, user: "change the color swatch to better match the epsilon website"):** the palette and type are read from the live epsilon.plus theme. Output `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.2.mp4`.
- **Background:** all CGI, card and logo frames use the site charcoal `#1A1A1A` (`--background` / `--button-background-primary`). The renders were redone with a transparent film and composited in post, and measure 24/24/24 after H.264.
- **Offer:** "30%+ OFF" is white on a sale-red `#F83A3A` rounded badge (the site's `--on-sale-badge-background` and announcement bar).
- **Type:** headings in the site's own Barlow 700 (`/cdn/fonts/barlow/barlow_n7…woff`), the secondary line in Barlow 400, grey `#B2B2B2`.
- **Unchanged:** cuts, music and loudness (-13.7 LUFS / -4.3 dBTP).

**v0.1 (2026-11-17):** the same cut with Del & Eps removed, on the owner's instruction relayed by the parent: "not use del & eps, just typical branding content". Output `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.1.mp4`. Timing, loudness (-13.7 LUFS / -4.3 dBTP) and cuts are unchanged. Everything below about v0's Del & Eps placeholders is superseded.

v0 is a quick, short first draft, made on the owner's instruction (relayed by the parent session 2026-11-17: "have all the agents make a quick short first draft"). The shot list's open questions were NOT answered by the user in this chat, so each one below uses my recommended default. Preview quality throughout.

Output: `/home/user/media/work/out/bf-integra-stock-to-kitted_v0.mp4` (1080x1920, 30 fps, ~17.6 s). Build: `tools/build_v0.py`; renders: `tools/shot.py` with `spec_s1.json` and `spec_s5.json`.

## Timeline (cuts on the kick grid of "140" by Lil Texas: drop 6.991 s, beat 0.43073 s)
| Frames | Time (s) | Shot | Source |
|---|---|---|---|
| 0-209 | 0-6.99 | Stock A-Spec scan, silver on black. The camera approaches from the front 3/4, passes down the side, and settles on the solved camera of the real clip ~0.6 s before the drop. | `Integra A_spec_scan_full_relocated.stl` (Drive 123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV), 3 mm decimation |
| 210-260 | 6.99-8.70 | **Hard 1:1 cut on the drop** to the real kitted car (DJI 0371 from 2.5 s). The 9:16 window eases from the nose toward the doors. | Dropbox `.../integra roller/DJI_20240324162540_0371_D.MP4` |
| 261-312 | 8.70-10.43 | Real rear 3/4: Sport Wing, spats, diffuser | `.../integra roller/DJI_20240324162511_0370_D.MP4` from 4.0 s |
| 313-468 | 10.43-15.63 | The four GLB kit parts drop into their installed positions on beats 9-12, in silver with no car body. Card text on beat 13 (v0 also had Del & Eps placeholders on beat 14, removed in v0.1). | `eps-acura-integra-de-v29.glb` part_front_lip / side_skirts / rear_spats / sport_wing |
| 469-527 | 15.63-17.60 | Epsilon+ wordmark, 720 px; the music fades out | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) |

## 1:1 match
- **Camera.** The clip was shot on a DJI Osmo Pocket 3 (read from the file's metadata). It is solved on frame 2.5 s of 0371 from 8 body landmarks: door handles, mirror, badge and shut lines. A free-focal solve was degenerate (9.6 mm, every landmark on one flat side), so I fixed the focal at 22 mm on a 36 mm sensor (the Pocket 3 is 20 mm-equivalent, plus its stabilisation crop). RMSE 4.8 px on 3840 wide; 2 points were dropped. The onion overlay (`match/onion.jpg`) lines up the glass, handles, shut lines, lamps and wheel positions.
- **Crop.** The 9:16 window is x 2200-3415, full height, of the 4K frame. The scan camera ends on that window, using lens shift 0.730 on an 11.39 mm sensor. The first S3 frame equals the solved frame (phase correlation 0.4 px).

## Assumptions (defaults for the open questions)
1. **Card wording:** "FULL KIT / 30%+ OFF", with "LIP · SKIRTS · SPATS · SPORT WING" and "ACURA INTEGRA (DE4)" underneath. No prices, stock counts or dates on screen. 30%+ is true on the liquidation sheet: lip 30 %, skirts 30 %, spats 40 %, wing 30 %; kit $1,360 → $934.50 = 31.3 %.
2. **Stock pass:** the silver scan of the real car, not CGI or footage.
3. **Music:** "140" by Lil Texas (TikTok CML 7597234501887166481), from the start of the song. The file is the CML preview, but it is the full 136 s, so no temporary bed was needed. Attach the same sound when posting. Loudness was measured after the mux; see the checks below.
4. **Kit card finish:** silver parts, so the characters carry the colour.
5. **Del & Eps: PLACEHOLDERS.** They are cut-outs of the model sheet (`knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`), labelled "PLACEHOLDER" on screen. No Higgsfield stills were generated, so v0 spent no credits. They appear only in the kit shot. Shot 1's roadside appearance needs real generated plates matched to the moving camera, so it is left out of v0.
6. **Spats:** the GLB's single spats version.
7. **No per-part prices and no `epsilon.plus` on the end card.**

## Known v0 gaps
- **Scan wheels.** The scan's wheels are patchy (dark rims weren't captured), and you can see it in the stock pass.
- **Frame rate.** The scan shots are rendered at 15 fps and each frame is doubled (a slight step in the motion). Preview quality is 50 % res, 8-12 samples.
- **Composition.** The 9:16 window of the landscape 0371 clip puts the car in the upper third, with road below.
- **Del & Eps** are placeholders, as described above.

## Checks run on the delivered file
- **Format:** 528 frames, 17.60 s, 1080x1920, 30 fps, H.264 + AAC 256k.
- **Loudness:** -13.7 LUFS integrated, true peak -4.3 dBFS (music gain 0.443; the raw track measured -7.1 LUFS / +2.3 dBTP).
- **Cuts vs kicks** (cuts measured from frame differences, kicks read from the delivered file's own audio):

  | Cut frame | Time (s) | Kick (s) | Error |
  |---|---|---|---|
  | 210 (the 1:1 drop) | 7.000 | 6.999 | +1 ms |
  | 261 | 8.700 | 8.700 | 0 ms |
  | 313 | 10.433 | 10.426 | +7 ms |
  | 469 | 15.633 | 15.624 | +9 ms |

  The last cut first measured -24 ms at frame 468 and was moved to 469.
- **Black frames:** per-frame luma of both renders shows no lighting dropouts (stock pass 32-47, kit 13-23; the kit's first frames are intentionally empty black).
- **Edges:** at rest, the kit keeps ≥ 68 px left, 230 px top and 110 px bottom at 50 % render size. The minimum right margin over the whole shot is 0 px, from parts falling in on frames 17 and 23. The stock pass crops the car on purpose: it ends on the 1:1 window.
- **Look:** contact sheet `/home/user/media/bf-integra-stock-to-kitted/review/sheet_v0.jpg`, frames around every cut.
