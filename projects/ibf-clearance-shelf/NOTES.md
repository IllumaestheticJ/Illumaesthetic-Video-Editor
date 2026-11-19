# R5 ibf-clearance-shelf: notes

Owner concept: "Clearance shelf. One continuous pan across the shelf with price tags popping up:
VB WRX front lip $79.99, Supra lenses $72, B-grade S13 bezels $62.72, GTR grille $105."

## v0 (2026-11-19): quick draft, NO real shelf pan yet
- **Footage gap:** there is no clearance-shelf pan in Dropbox (searched file names and image content for shelf, bezel,
  grille, 240sx, lens; the shelf photos are random shop racks). v0 fakes the pan: four "bays" side by side and the camera
  moves left to right without stopping (slows near each item to 15 % speed, never holds). When the real pan is filmed it
  replaces the bays and the tag timing stays.
- **Bays:**
  1. VB WRX front lip: real clip, the 2023 Illumaesthetic reel `Vb lip voiceover.mov` 15-19 s, cropped below its
     burned-in captions (so it is soft: about 1.7x upscale).
  2. Supra lenses: real clip, `Supra Tail Light Footage/Video Jul 07 2026, 4 35 00 PM.mov` from 12.5 s (bench test,
     smoked lenses over the heart housings, lights switch on during the pan). Please confirm these are the **tinted
     clear** lenses.
  3. S13 bezel B-grade: **FOOTAGE NEEDED placeholder**. The only bezel videos are carbon-fibre (not B-grade), so not used.
  4. S13 GTR grille: **FOOTAGE NEEDED placeholder** (no clip or photo found).
- **Tags:** one hanging price tag per music bar (2.6 s), BLACK FRIDAY strip, item name (Unbounded 700), price in Akira.
  The first tag is on screen at 0.18 s. Prices from `projects/_illum-bf26/PRICES.md` only.
- **End card (10.4-15.6 s):** BLACK FRIDAY CLEARANCE, all four prices, ENDS NOV 30, Illumaesthetic logo,
  WWW.ILLUMAESTHETIC.COM (Unbounded 400).
- **Music:** "Free Smoke" - TheTrapLabb (TikTok Commercial Music Library), from the drop at 27.71 s, 92.3 BPM.
- **Length:** 15.6 s, 1080x1920, 30 fps.

## Open questions for the owner
1. VB WRX lip is an Epsilon+ product: keep it on this Illumaesthetic shelf? (Built in for now.)
2. Until the shelf pan is filmed, may the bezel and grille bays use the store product photos?
3. Are the smoked lenses in the Supra bench clip the tinted clear variant?

## Filming instructions for the real pan
- One slow continuous pan, left to right, **8-10 s**, phone vertical, 4K at 30 or 60 fps, 1x lens, no zoom.
  Gimbal or slow walk; the camera never stops.
- About 1 m from the shelf, lens at item height.
- Item order: 1) VB WRX front lip (if it stays), 2) Supra tail light lenses, tinted clear only, 3) S13 radio bezel,
  B-grade only, 4) S13 GTR grille. About 2 s per item. Start already framed on item 1 (the price must show by 2 s);
  slow down on the last item for 1 s.
- Clear the shelf: no other radio bezels, no CorsoMotion, Ghozt or preorder boxes, no clear (non-tinted) Supra lenses.
- Light: shop lights on plus one soft light from the camera side. No windows or backlight behind the shelf; tilt the
  tinted lenses so they don't mirror the light.
- Shoot 3 takes.

## v0 checks
- 1080x1920, 30 fps, 468 frames = 15.6 s. Loudness -13.8 LUFS integrated, true peak -3.0 dBFS.
- Safe zones: `safezone_check.py --text-boxes` OK and the sheet was reviewed (all text inside x 48-920 / y 285-1440).
- Reading time: each price tag 2.30 s fully on screen (minimum 2.2 s); end card 4.95 s.
- First price on screen at 0.18 s.
- Build: `projects/ibf-clearance-shelf/tools/build_v0.py`.
