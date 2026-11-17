# bf-paint-match-roulette: draft v0 notes (2026-11-17)

**v0.1 (2026-11-17):** re-cut without Del & Eps (owner: "not use del & eps, just typical branding content"). Shot 1 is the silver
scan alone; the end card is the silver scan + offer text. Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.1.mp4`
(same cuts and audio as v0, so the sync and loudness checks below still hold: -14.0 LUFS, peak -3.7 dBFS). Assumption 5 below is void.

The owner said "have all the agents make a quick short first draft" (relayed by the parent session). v0 is a **preview-quality**
draft of `shotlist.md`. Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.mp4` (1080x1920, 30 fps, about 23.3 s; media is not committed).
Tools: `tools/render_v0.py` (Blender stills), `tools/compose_v0.py` (assembly + text), `tools/probe.py`.

## Assumptions (my defaults for the open questions; please correct any of them)

1. **Wings:** all three wings are in the video (FL hatch + FE sedan + Integra), with every store colour for each wing.
2. **Hook car is the FE sedan, not the FL hatch.** This is a change from the shot list. The silver scan is the wing configurator's
   decimated FE scan (`ewc-honda-civic-sedan-fe-r3.glb`, a real scan at 30k faces). The engineering full-car scans weren't downloaded
   for a quick draft. The only hatch scan on the configurator is an FL5 Type R wearing its factory wing, so it can't carry the Sport Wing.
   The lookbook Sport Wing sits on the scan in silver. For the 1:1 cut, the scan is aligned to the lookbook body by plan-view PCA
   heading (0.7°) and bbox centre, not by ICP. The cut is approximate, and the onion overlay is close but not exact.
3. **Prices on screen** come from the BF liquidation sheet (PRICES.md, rev 25 snapshot), with the old price struck through:
   Civic base ~~$450~~ $315, Civic paint-matched ~~$850~~ $715, Integra base ~~$500~~ $350, Integra paint-matched ~~$950~~ $800
   (shown only on Double Apex Blue, a $950 colour). The end card says "FROM $315". No stock counts, no dates.
4. **"Each on its car":** Boost Blue, Championship White and Rallye Red FL are the real FL5 Type R listing photos. The other FL colours are
   rendered on the lookbook FL2 hatch. FE and Integra colours are on their own lookbook cars. FE ends on the real red FE photo
   (DILL7196). Sonic Gray Pearl appears twice (once for the FE wash, once in the FL run), because it's on both store lists.
5. **Del & Eps:** these are **placeholders cut from the committed model sheet** (`knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`),
   not new Higgsfield generations. I kept spend at zero, so the frames are labelled "DRAFT v0 - placeholder". They stand static on the
   silver scan in shots 1 and 37 only (house rule: characters are the only colour in frame; the roulette has no characters).
   The "hand on the wing", the scanner sweep and the 10 mm gag are not animated in v0.
6. **Paint wash** (shot 3): a 0.6 s wipe from gloss black to Sonic Gray Pearl across the wing, travelling right to left from where Eps stands.
7. **Pace:** the FE and Integra spins use half-beat cuts (about 6-7 frames). The measured flux grid has a transient on every 8th note.
8. **No text over photos:** the photo shots carry no colour names (the band option, Q9, isn't used in v0).
9. **Music:** GT2 "Arcade Mode Theme" (Dropbox /Moosic, assigned in MUSIC.md), from 0 s, with a 0.6 s fade at the end. Grid:
   140 BPM, first beat 0.0703 s (flux autocorrelation + phase fit). Loudness: -14.0 LUFS, peak -3.5 dBFS.
10. **Logo:** the epsilon.plus site header wordmark (`Epsilon_banner_black...png`, inverted to white, 720 px), standing in for the Drive
    `EPSILON+ Logos/Epsilon+ Logo.png`.
11. **Integra body:** the DE5 Type S lookbook model (v19), with its duckbill part hidden.
12. **Kit parts hidden:** the lookbook front lip, skirts and rear lip are hidden on the Civics, so the wing is the only Epsilon part in frame.

## Preview-quality shortcuts (to fix for v1)
- 540x960 Cycles stills (16 samples, denoised), upscaled 2x. Motion is a 2-6 % digital push-in, not a camera move.
- Lighting/paint is a quick studio rig. Pearl/metallic is approximated with Principled metallic + coat.
- No Remotion: text is drawn with PIL in Inter Display.
- The scan is the configurator's decimated scan, not the engineering full-car scan.

## Checks run on the delivered file (2026-11-17)
- Length 23.285 s, 1080x1920, 30 fps, 37 shots.
- **Cut sync:** all 36 cuts measured against flux onsets of the decoded mp4 audio: mean error -2 ms, max |error| 25 ms (frame
  rounding is ±16.7 ms). The first pass read about 20 ms early, so the grid was moved +20 ms (B0 0.0903). Every cut shows a clear frame jump.
- **Loudness:** -14.0 LUFS integrated, peak -3.7 dBFS (ebur128 after the mux).
- **Framing:** I looked at the first/mid/last contact sheet. Cars are fully in frame. Long headers are auto-shrunk to fit (the first
  pass clipped "PAINT MATCH AVAILABLE" and "INTEGRA SPORT WING"). On the end card, Del & Eps were scaled down so they no longer cover the car.
- **Known v0 issues:** the 1:1 scan->CGI cut is approximate (PCA + bbox, not ICP). The Eps placeholder overlaps the scan's rear
  quarter in shot 1 and does not touch the wing. Renders are at half resolution.

# v0.2 (2026-11-17): retro car-dealership menu version

The owner sent two reference clips of a PS1-era racing game's showroom menu and said: "we want it to look like this, with change
color and the same sound effect ... the same UI, with the cars we have ... the price where the credits should be ... change color,
and then show all our color options ... keep the paint match and the sale/price in a similar way, show the navigation between cars
too, and the SFX". Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.2.mp4` (23.3 s, 1080x1920, 30 fps).
Tools: `tools/render_turntable.py`, `tools/compose_v02.py`.

## What it is
Lineup grid (3 tiles with sale prices) -> cursor clicks Civic Hatch -> car on a turntable, Gloss Black base wing, $315 (~~$450~~) ->
CHANGE COLOR through all 12 store colours ($715, ~~$850~~) -> back to the lineup -> Civic Sedan (11 colours) -> Integra (10 colours)
-> offer screen -> Epsilon+ wordmark. Clicks and colour changes land on the beat (GT2 "Arcade Mode Theme", 140 BPM).

## Assumptions and choices
1. **UI is our own drawing in the reference's layout**, not a copy of the game's art: own icons, Inter / DejaVu Serif type, no game or
   manufacturer logos. Layout matches: icon row, tabs, serif car name, turntable, colour name, swatch strip, CHANGE COLOR, the price
   where the credits sit, BUY ring, bottom bar with a back button.
2. **SFX are synthesized** (cursor tick, two-tone select, rising colour-change chirp). Both reference clips have music under the menu
   sounds, so the originals can't be lifted cleanly. If the owner has clean recordings, they can be dropped in.
3. **All colours on the lookbook models:** the 12 FL colours (including Boost Blue and Championship White) are shown on the FL2 hatch
   model. Championship White NH0 has no lookbook value; **#f6f5ee is my approximation**.
4. **Prices** from the BF liquidation sheet: base $450 -> $315 (Civics), $500 -> $350 (Integra); paint-matched $850 -> $715 and $950 -> $800.
   Platinum White is dearer on the store, so it shows $900 -> $765 (Civic Sedan) and $1,000 -> $850 (Integra): the was-price minus the
   same base discount. $850 for the Integra is in the owner's TL;DR doc; **$765 is derived, please confirm**.
5. **Recolouring:** each car has 48 turntable angles in two passes (paint black / paint white) plus a paint-and-wing mask
   (720x420, Cycles 10 samples). Colours are tinted in compositing, so the paint is a plain gloss (no metallic flake) in this draft.
6. On the base-wing screen the car body is a neutral grey with the wing in gloss black.
7. Dropped from this version: the silver scan opener, the real photos and the Remotion text style. No characters.

## Checks on the delivered file
- Loudness -14.0 LUFS, peak -1.5 dBFS (music -5 dB under the SFX mix, then +4.2 dB overall).
- 37 click / colour-change events vs measured music onsets: mean -4.5 ms, max 25 ms (frame-quantised).
- Contact sheet (44 frames) looked at: every colour appears with its name, code and price; nothing clipped. The first pass had
  the tabs over the icon row and the offer-screen price off the right edge; both were fixed.

# v0.3 (2026-11-17): safe zones

Owner rule (knowledge/safe-zones.md): no text or elements in the app buffer zones. v0.2 failed `scripts/safezone_check.py`: the
icon row and tabs were in the top zone; the price, BUY ring and bottom bar were in the bottom 480 px; the colour name and CHANGE
COLOR button were under the right rail. v0.3 (`tools/compose_v03.py`) re-lays every menu screen inside x 48-920 / y 285-1440,
which is also inside the 4:5 feed crop. Timeline, colours, prices, music and SFX are unchanged from v0.2.
Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.3.mp4`.
- Checker sheet looked at: nothing in red or amber. Measured bounding box of all non-black pixels over the whole video:
  x 48-924, y 288-1444 at a 4 px sampling grid (i.e. inside the safe box).
- Loudness -14.0 LUFS, peak -1.5 dBFS.
- Trade-off: the menu now fills about 80 % of the width and 60 % of the height, with black around it.

# v0.4 (2026-11-17): www.epsilon.plus

Owner rule: every web address reads `www.epsilon.plus`. The menu's bottom bar now says "www.epsilon.plus" (was "epsilon.plus"),
and "WWW.EPSILON.PLUS" sits under the end wordmark. `tools/compose_v04.py`; output
`/home/user/media/work/out/bf-paint-match-roulette_v0.4.mp4`. Otherwise identical to v0.3.
Checks: safe-zone sheet looked at (clean, URL and wordmark inside x 48-920 / y 285-1440); -14.0 LUFS, peak -1.5 dBFS.
