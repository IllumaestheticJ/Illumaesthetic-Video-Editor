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

# v0.5 (2026-11-17): real SFX, lip kits, widebody, even turntables, fonts

Owner feedback: "have the preview windows orient the cars the same way, and use the same exact sound effects as the video";
"use the actual epsilon lip kits for the platforms"; "The Integra also has different speeds it goes at"; "add the lip kits and
the DE4 widebody car into the list of cars". Plus the font rule relayed by the parent (knowledge/fonts.md).
Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.5.mp4` (27.2 s). Tools: `tools/compose_v05.py`,
`tools/render_turntable.py`, `tools/extract_sfx.py`.

- **Integra speed/orientation bug (v0.2-v0.4):** its 48 turntable angles were rendered in 3 chunks, and each chunk used its own
  end index as the full-turn count (16, 32, 48), so the step size changed between chunks. `render_turntable.py` now takes the
  full-turn count and a separate START/END. All four cars share the same angle per index.
- **Lineup previews:** every tile uses the same front-3/4 angle (index 16).
- **Lip kits:** lookbook `part_front_lip`, `part_side_skirts`, `part_rear_lip` (Civics) / `part_rear_spats` (Integra) are shown, in a
  black finish (the sheet lists them as unpainted PU), with the stock rear diffuser pieces hidden where the rear lip replaces them.
  The Integra is now the DE4 lookbook model `eps-acura-integra-de-v29.glb` (the Type S model has no lip kit parts).
- **Fourth car, "Integra Widebody" (DE4):** the same model with `part_fender_flares` in black (sheet: "Fender Flare Widebody – DE4 · PU").
  Its 10 colours cycle on half-beats. The price slot still shows the Sport Wing price.
- **New on-screen lines (from the sheet):** "FRONT LIP + SKIRTS 30% OFF" (Civic FE/FL and Integra front lip and side skirts are 30 %;
  rear spats are 40 % and the FL hatch rear lip has no deal, so the line names only lip + skirts) and "WIDEBODY FLARES 50% OFF" ($800 -> $400).
- **SFX are the reference clip's own sounds.** `extract_sfx.py` aligns every instance of a menu sound in the owner's 7-minute clip and
  takes the median, so the music under it cancels. Confirm chime: 161 instances, residual music about -16 dB; the "select car" sound
  is the same sample (correlation 0.95). Back sound: 16 instances, residual about -8 dB (band-limited to 250-3500 Hz to hide it).
  No cursor-move sound was found in the reference, so there is none.
- **Fonts:** Unbounded 800/900 stands in for Akira on prices, offers, BUY, LINEUP and tile titles; Unbounded 300/400 for the URL
  (next to the logo). Car names stay in the serif, small labels in Inter. Akira file still needed from the owner.
- **Checks:** -14.0 LUFS, peak -1.4 dBFS (the first mix was -12.1 LUFS / +1.0 dBFS; SFX lowered 5 dB). 51 click/colour events vs music
  onsets: mean -4.8 ms, max 25 ms. Safe-zone sheet looked at: clean; content bbox x 48-924, y 288-1444 (4 px grid).

# v0.6 (2026-11-17): paint-matched kits, both prices, centred, even pace

Owner feedback on v0.5: lip kits/flares "Paint matched like wing"; widebody "Show both prices"; "Video needs to be centered, and the
changing speed should be evened out"; "The color should only reference the color of the car - so gloss black should be on a black car".
Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.6.mp4` (29.3 s). Tools: `tools/compose_v06.py`, `tools/render_turntable.py`.

- **Kits and flares paint-matched:** the turntable mask has a third channel (B = lip kit / flares). They take the car colour on every
  paint screen. Turntables re-rendered to `ttp/` (the render script now skips frames that exist, after two container restarts).
- **Gloss Black base-wing screen** is now a black car (#0b0b0d) with black wing and kit, so the named colour is always the car's colour.
- **Widebody shows both prices:** WING ($350 base / $800 paint-matched, $850 Platinum White) and FLARES $400 (~~$800~~).
  The sheet has only the unpainted-PU flares price; no paint-matched flares or Integra lip price exists, so $400 shows beside painted flares.
- **Centred:** the menu box is scaled to 760 px wide and centred on x = 540 (x 160-920, y 433-1440). The end wordmark is centred at 720 px.
- **Even pace:** every colour change is one beat (0.4286 s) on all four cars; the widebody's half-beat cycle is gone.
- **Checks:** -14.0 LUFS, peak -1.4 dBFS. Content bbox x 160-920, y 436-1440, centre x 540. Colour-change gaps 0.428-0.429 s throughout.
  Safe-zone sheet looked at: clean.

# v0.7 (2026-11-17): Type S as the 3rd entry, real model logos

Owner: "the DE4/5 (3rd entry) should be the Type S instead of the non-widebody integra"; "also use the real civic/integra logos"
(the owner pasted both logo images in chat). Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.7.mp4` (29.3 s).
- **3rd entry = Integra Type S (DE5):** lookbook `eps-acura-integra-type-s-de5-v19.glb`, Sport Wing only (the model has no lip kit
  parts, so no "FRONT LIP + SKIRTS" line on that screen). The 4th entry stays the DE4 widebody with kit + flares.
- **Logos:** the owner's Civic and Integra wordmarks (recovered from the chat images to `logo/civic_alpha.png`,
  `logo/integra_alpha.png` in the media folder; media is not committed) replace the serif car names on the car screens and the lineup
  tiles. The variant line under each logo is Unbounded 600: "HATCHBACK · FL2 / FL5", "SEDAN · FE", "TYPE S · DE5", "WIDEBODY · DE4".
- **Checks:** -14.0 LUFS, peak -1.4 dBFS; content bbox x 160-920, y 436-1440; safe-zone sheet looked at: clean.

# v0.8 (2026-11-18): Integra wordmark without the Acura badge

Owner: "remove the acura badge from the integra". The badge is cropped off the owner's logo (`logo/integra_alpha.png`; the original
is kept as `integra_with_badge_alpha.png`), on the car screens and the lineup tiles. `tools/compose_v08.py`; output
`/home/user/media/work/out/bf-paint-match-roulette_v0.8.mp4`. Otherwise identical to v0.7.
Checks: -14.0 LUFS, peak -1.4 dBFS; content bbox x 160-920, y 436-1440 (same layout as v0.7).

## v0.9 — car centred on screen (owner: "can you center the car on the screen as well")
- `tools/compose_v09.py`. Turntable moved down so the car sits on the frame centre (x 540, y ~960); logo/variant stay above it.
- Info rows tightened below the car to stay inside the safe box (y <= 1440): bullets, colour name/code, swatches, CHANGE COLOR, price (label now above the crossed-out price), BUY, bottom bar.
- Timeline, colours, prices, music, SFX and mix unchanged from v0.8.
- Checks: 29.30 s, -14.0 LUFS, true peak -1.4 dBFS; safe-zone sheet looked at (nothing in red/amber); car, lineup, widebody two-price and offer screens checked for overlaps - none.
- Note: the car's silhouette centre still drifts about +/-25 px sideways as it turns (perspective of a turntable); its average is on the centre line.
- Still open: Akira font file (Unbounded stand-in), paint-matched flare/lip prices, FE Platinum White price is derived, Championship White hex approximate.

### v0.9 re-render (owner: "the car looks like its off the left"; "check all the colors again - DE4 didn't come in tiger eye pearl")
- Bug since v0.6: the turntable `.resize((CAR_W, CAR_H))` had been swallowed into a trailing comment, so the 720 px render was pasted unscaled at the left edge of the box (car ~66 px left of centre and ~17 % too small). Fixed; `CAR_Y = 635`. Measured car centre now x 516-568 (turntable drift), y ~965-980.
- Colours re-checked per car against factory palettes:
  - Civic hatch FL2/FL5 (12): all are hatch or Type R colours - kept.
  - Civic sedan FE (11): all are sedan / Si colours - kept.
  - Integra Type S DE5 (10): kept (Tiger Eye Pearl is Type S only).
  - Integra widebody DE4 (9): Tiger Eye Pearl removed. Car screens now end on beat 59; offer screen is one beat longer; length unchanged (29.30 s).
- Unverified from the web check: 2025+ colours (Solar Silver, Urban Gray, Double Apex Blue) on the DE4 are taken from Acura's 2026 refresh announcement; year-by-year Civic lists were only partly confirmed.
- Checks: -14.0 LUFS, -1.4 dBFS; safe-zone sheet (18 frames) looked at - clean.

### v0.9 re-render 2 (owner: "can you move the cars slightly up in the shot?")
- `CAR_Y` 635 -> 585 (car ~44 px higher in frame, centre y ~925); nothing else changed.

### v0.9 re-render 3 - Akira Expanded swapped in (owner licence confirmed 2026-11-18, knowledge/fonts.md)
- Font from the owner's Drive (EPSILON+ Logos), SHA-256 verified, installed in gitignored `assets/fonts/akira/` (not committed).
- Akira now sets the big prices, `$`, BUY, LINEUP and the two offer pills (`U()` returns Akira for weight >= 800 and size >= 30, at 0.95x so line widths match the old stand-in, with a 0.10x baseline shift).
- Still Unbounded: crossed-out prices, CHANGE COLOR / BLACK FRIDAY buttons and other small labels, www.epsilon.plus and the URL under the wordmark. "Sport Wing" title stays serif (reference look).
- All Akira strings asserted ASCII; stills checked - no tofu. -14.0 LUFS / -1.4 dBFS; safe-zone sheet clean.

## v0.10 - Epsilon+ plates on the rear of every car (owner: "can you put epsilon plates on all the rear of the cars")
- `tools/render_plate.py`: extra turntable layer `p_XX.png` (RGBA) per car - a US-size plate (305 x 152 mm, black, white border, the
  Epsilon+ wordmark from `logo/banner_black.png`) placed on the rear surface by ray casts and rendered with the car as a holdout,
  so it is hidden correctly as the car turns. ~30-60 s per car; the b/w/m passes were not re-rendered.
- Plate centre heights (from `tools/plate_probe.py` rear ortho views; rear is +Y): FL hatch z 0.76, FE sedan 0.74, Type S 0.57
  (bumper), DE4 widebody 0.575 (covers the model's blank plate). A recess whose top edge overhangs (hatch) gets a vertical plate.
- `tools/compose_v10.py` = v09 + plate layer alpha-over after the colour tint. Lineup tiles are front views, so no plate there.
- Workbench renders do not work in this container (no EGL/Vulkan) - probes use Cycles.
- Checks: 29.30 s, -14.0 LUFS, -1.4 dBFS; safe-zone sheet clean; rear frames checked on all four cars, plate readable.

### Fitment check of the lookbook parts shown (heads-up from BF6, 2026-11-18) - `tools/seat_check.py`
Nearest distance from part vertices to the body surface (mm): min / 5th percentile.
- Civic hatch FL: wing 1.0 / 2.1, front lip 0.0 / 2.0, skirts 0.0 / 0.8, rear lip 0.0 / 2.4
- Civic sedan FE: wing 0.0 / 1.0, front lip 0.0 / 2.0, skirts 0.0 / 0.7, rear lip 0.0 / 1.4
- Integra Type S DE5: wing 0.0 / 3.4
- Integra DE4 widebody: wing 0.0 / 0.1, front lip 0.0 / 1.2, skirts 0.0 / 1.7, rear spats 0.0 / 0.9, flares 0.0 / 0.3
All parts touch the body (nothing floats like the GR Corolla spats at ~16 mm); no re-seat, no re-render.
Limit: this is an unsigned distance, so it shows gaps, not how deep a part clips into a panel; no clipping is visible in the turntables at 720 px.

## v0.11 - text held for slow readers (owner rule 2026-11-18, knowledge/lessons.md [timing]; relayed by parent)
`tools/compose_v11.py` (= v10 with longer text holds; picture content unchanged). 46.0 s (v0.10: 29.3 s). Beat = 0.4286 s.

| Text | v0.10 | v0.11 | Rule minimum |
|---|---|---|---|
| Lineup, first time (4 tiles with prices) | 1.29 s | 3.43 s (8 beats) | 3 s (prices) |
| Lineup, when returning between cars | 0.86 s | 1.71 s (4 beats) | 3 s - **still short**; same text as the first time |
| Base-wing price screen per car ($315 / $350) | 0.86 s | 3.00 s (7 beats) | 3 s |
| Paint-matched price per car ($715 / $800) | 3.9-5.1 s | 3.9-5.1 s | 3 s |
| Colour name + code | 0.43 s each | 0.43 s each | 2.5 s - **not met** (42 names x 2.5 s = 105 s; needs owner call) |
| Platinum White special price ($765 / $850) | 0.43 s | 0.43 s | 3 s - **not met** (same reason) |
| Offer screen (2 offer lines + 2 prices) | 2.14 s | 4.29 s (10 beats) | ~4 s |
| End card (wordmark + URL) | 1.79 s | 3.07 s | 2.5 s |

- Music: same track from 0 s, cut to 46.0 s with a 0.6 s fade (`music_v11.wav`, +3 dB like v06); final mix gain 4.2 dB.
- Colour changes stay one per beat (owner: "changing speed should be evened out"; the roulette is the concept).
- Checks: 46.03 s, -14.0 LUFS, -1.2 dBFS; safe-zone sheet (12 frames) clean.

### v0.11 withdrawn (owner, 2026-11-18: "undo the changes for this one")
The slow-reader holds are NOT applied to this video. **v0.10 (29.3 s, `tools/compose_v10.py`) is the current version.** `compose_v11.py` removed (it is in git history).

### Shared Drive "Claude Videos" (2026-11-18, scripts/vdrive.py)
- Restart cache `work/bf-paint-match-roulette/`: `ttp_fl`, `ttp_fe`, `ttp_de5`, `ttp_wb` (turntable passes b/w/m/p), `assets` (music, sfx, logo, plate, colours.json), `glb`, `akira_font`. After a container restart: `python scripts/vdrive.py restore bf-paint-match-roulette`.
- Delivery: v0.10 in `deliveries/bf-paint-match-roulette/`.
- Local clean-up: kept v0.8, v0.9, v0.10 mp4s; removed older mp4s, the superseded turntables (`tt`, `ttk`, `ttp/de4`) and test stills.

## v0.12 - sound effects put on the beat (owner: "does the beat still match up? looks like it desyncs around halfway")
Measured (2026-11-18):
- Music: steady 140 BPM over the 29 s used, no drift (grid within ~15-20 ms of the hits all the way through).
- Picture: every colour change / navigation cut within one frame (+-15 ms) of the grid, start to end. No drift.
- **Bug:** the recovered menu sounds have ~68-70 ms of lead-in before their click; the code assumed 6 ms, so every
  click sounded 62 ms after its cut since v0.3. From about the middle the riff becomes syncopated (strong hits on
  the "and" / 16ths, tempogram shows 185 BPM = dotted-8th accents), so there is no on-beat hit to mask the late click
  and it reads as drifting. Fix: `compose_v12.py` measures each sample's attack and places the transient on the cut
  (measured after: 0 ms error).
- Other sections of the track were checked for a straighter 29 s: the first 29 s (current) is already the best;
  the song repeats about every 55 s.
- Picture identical to v0.10. Checks: 29.30 s, -14.0 LUFS, -1.6 dBFS, safe-zone sheet clean.
