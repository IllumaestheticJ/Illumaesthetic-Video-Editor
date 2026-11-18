# BF 1/8 civic-parts-rain: draft v0 notes

**Owner, 2026-11-17 (relayed by the parent): no Del & Eps, typical Epsilon+ branding only.** v0 was assembled after this note arrived, so it has no characters. Nothing was spent on Higgsfield.

v0 is a quick, preview-quality first draft. The owner asked "have all the agents make a quick short first draft", relayed by the parent session on 2026-11-17. Output: `/home/user/media/work/out/bf-civic-parts-rain_v0.mp4` (media is not committed).

## What's in it (26.5 s, 1080x1920, 30 fps)
| Time | Shot | Source |
|---|---|---|
| 0.00-16.25 | One continuous take on the silver FE1 scan. Website-kit parts rain like bills; "BLACK FRIDAY" title. Ron's production parts seat on the hits: front lip 10.96 (the drop), side skirts 12.37, rear lip 14.50, Sport Wing 15.53, each with a short label. The rain falls away after the rear lip; the camera ends on render 7's view. | FE1 facelift scan (Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ), Ron's STLs + wing.002, lookbook GLB fe-facelift-v9 |
| 16.25-16.60 | IRL flash: a close push on the real installed front lip (EPSILON tag) | Dropbox `FE Civic Sedan install tutorial/Video Jun 16 2026, 7 54 08 PM.mov`, 0.00-0.33 s |
| 16.60-19.79 | Hard 1:1 cut to Ron's render 7, with a 3% zoom OUT | Drive 1KHccoGDROajdOmue_ie8XU56mz-GSeFu |
| 19.79-21.55 | Lookbook FE in Rallye Red, kit paint-matched, painted parts raining behind it. Offer text: "BLACK FRIDAY / 30% OFF / THE FULL KIT", the parts line, and "PAINT-MATCH AT FULL PRICE". | eps-honda-civic-sedan-fe-facelift-v9 |
| 21.55-23.14 | Lookbook FL in Boost Blue, front lip + skirts + Sport Wing, same text | eps-honda-civic-hatch-fl-facelift-v8 |
| 23.14-26.50 | Epsilon+ wordmark (720 px) + "SHOP DEALS NOW / WWW.EPSILON.PLUS"; fade | Drive `EPSILON+ Logos/Epsilon+ Logo.png` |

## Assumptions (my defaults for the open questions; the owner can change any of them)
1. **FL rear lip is left off the FL car.** The BF sheet marks it "No deal" (pre-order), so "30% off the full kit" stays true.
2. **"PAINT-MATCH AT FULL PRICE" fine print is on.** The BF sheet takes 30% off the base price only for paint-matched parts.
3. **Colours:** FE Rallye Red R513 and FL Boost Blue Pearl B637P. These are RGB approximations; no paint data is in the repo.
4. **Music:** "FREAKED OUT" by Fat Papi & prodshushy (TikTok CML, song_clip_id 7644353784302340112), from the song's start. The full 158 s file came from the CML preview URL. BPM measured at 112-113, syncopated, so cuts sit on measured onset peaks rather than a beat grid. Lyrics not checked.
5. **No characters** (owner). The intro is carried by the rain and the "BLACK FRIDAY" title.
6. **Install flash:** the small clips in the install folder are finished-car shots. The real hands-on install clips are 0.5-0.75 GB, so v0 uses a finished-lip close-up instead.
7. **Wing:** Ron's wing.002 (the v5 wing, the same one render 7 shows) on the scan, and the lookbook duckbill on the CGI FE. That wing.002 is the Si Factory Duckbill version is NOT verified yet.
8. **Wheels:** the scan keeps its scanned wheels, so they change to Ron's gold wheels on the cut to render 7.
9. **Length:** 26.5 s, because the song starts from its beginning (house rule) and its intro is 11 s. Starting nearer the drop would bring it to ~18 s, but needs the owner's OK to break the "from the beginning" rule.
10. **Prices:** only "30% OFF THE FULL KIT", per the owner. No dollar figures, stock counts or dates.

## Known v0 quality limits
- Preview renders: 540x960 Cycles at 10-16 samples, upscaled to 1080x1920; no motion blur.
- A faint outline of the hood hole-fill patch is visible on the scan.
- The rain is a keyed tumble with no collision sim; it is placed so it clears the car and the camera path.

## Checks run (on the delivered mp4, 2026-11-17)
- File: 1080x1920 h264 + AAC, 30 fps, 795 frames = 26.50 s.
- Cut/seat sync vs onsets measured on the **decoded** audio (tools/check_v0.py). All are within 14 ms (half a frame = 16.7 ms):
  flash +13, render-7 cut -5, FE +2, FL +7, end card -14, lip +7, skirts -1, rear lip -1, wing -4 ms.
- Loudness -14.0 LUFS integrated, true peak -2.4 dBFS, LRA 3.1 LU.
- Take: 488 frames, no black/unlit frames (luma min 28 vs median 34-41). The 309-479 re-render splices seamlessly (diff at 308->309 equals its neighbours; 479->480 0.23).
- Framing: the first contact checks found the car's tail cut at the skirt/rear-lip seats and the CGI FE nose on the frame edge. Both were re-rendered (take keys widened, CGI camera pulled back). The contact sheet of the first/middle/last frame of every shot now shows the whole car in frame.
- The 1:1 end of the take vs render 7: car width 940 px both, overlay checked (renders/fit/overlay.jpg).
- Text: 80 px margins checked by measurement (title 125 px, "30% OFF" ~90 px, parts line 86 px).
- No text over the IRL flash.


## v0.2 changes (output `bf-civic-parts-rain_v0.2.mp4`) (owner notes on v0, 2026-11-17)
1. **"Too many parts clip in and out of the screen."** The rain is rebuilt in screen space (`tools/rain.py`). Every part enters fully above the top edge, falls straight down inside the side margins and leaves fully below the bottom edge. Respawns happen only off screen, and camera moves and zooms can no longer push a part across an edge. The rain finishes falling before the cut.
2. **"Don't home the parts - they must naturally fall on the car as if that was the plan."** Each kit part keeps its final orientation and falls along one straight line under gravity, from out of frame, landing exactly on its beat (`tools/falls.py`).
   - Fall lines: wing straight down; skirts 70 deg; lips 60 deg.
   - The lip, skirts and rear lip tuck under the body, so a pure vertical drop would pass through it. The lines are chosen so any contact with the scan happens only inside the last step between two frames, which is never rendered (`tools/fall_depth.py`).
   - The camera is near-frontal at the lip landing and nearly behind at the rear-lip landing, so both lips drop in from the top of the frame.
3. **"Cut the short section showing the badge."** The IRL flash is removed, and the take now cuts 1:1 to render 7 on the 16.25 s hit.

### v0.2 checks (delivered file `bf-civic-parts-rain_v0.2.mp4`, 26.5 s)
- Sync on the decoded audio: render-7 cut +13 ms, FE +2, FL +7, end card -14, lip +7, skirts -1, rear lip -1, wing -4.
- -14.0 LUFS, true peak -2.4 dBFS. 488 take frames, none dark.
- Edge test on the rendered take (anything on the 3 px side columns): 11 of 488 frames, down from 35 on the first v0.2 render. All 11 are kit parts falling into view through the top corners: lip 1 frame, skirts 8 (2 m long, diagonal entry), rear lip 2. No part pops in or out mid-frame; the rain never touches a side edge. The offer shots have 0.
- Hero falls (tools/falls.py): the frame before each impact is beyond the zone where the part could touch the scan: lip 0.55 vs 0.50 m, skirts 0.35 vs 0.30, rear lip 0.59 vs 0.54, wing 0.29 vs 0.06.
- Known: in the offer shots, rain sometimes passes behind the offer text.

## v0.3: safe zones (owner rule 2026-11-17, knowledge/safe-zones.md)
- All text and the wordmark are centred on the safe area (x 484), inside x 48-920 / y 285-1440. `scripts/safezone_check.py --text-boxes text_boxes_v0.3.json` reports "text boxes: OK" (exit 0).
- Render 7 is now 860 px wide, centred at x 484. The take's last 46 frames are refit to match (lens 132.6, shift 0.124/0.042); frames 420-441 are pixel-identical to v0.2, so the splice is invisible.
- The CGI cars are shifted left and up (shift_x 0.05, shift_y 0.12) to clear the like/share rail, with the parts line below them.
- Known: in the side view at the skirt landing (~12 s) the car's tail reaches slightly into the right rail. There is no text there.
- Sync and loudness are unchanged (±14 ms, -14.0 LUFS, TP -2.4 dBFS).

## v0.4 (owner notes on v0.3: first scene too long, parts snap on the beat, falling parts a bit blurred, parts bigger)
- Music from song 9.25 s: the first landing is 2.07 s in, and the video is 15.67 s (470 frames). This overrides the "from the beginning" house rule at the owner's request.
- Landings on four consecutive post-drop grid hits: lip 11.320 (frame 62), skirts 12.365 (93), rear lip 13.436 (126), wing 14.495 (157). The 1:1 cut to render 7 is on 15.534 (189), FE 17.459 (246), FL 19.792 (316), end card 21.554 (369).
- Rain is 1.6x bigger with faster falls (2.2-3.2 s), rendered as its own layer (car and kit held out on a transparent film) and blurred 5 px in comp (premultiplied). Same for the offer shots.
- Checks: sync within -17..+10 ms on the decoded audio. Loudness -14.0 LUFS after remixing the audio at +0.7 dB (this part of the song is louder than the first 26 s). safezone_check text boxes OK.

## v0.5 fonts (owner rule, knowledge/fonts.md)
- Headlines and offer ("BLACK FRIDAY" title, "30% OFF", "THE FULL KIT") use **Unbounded 700 as a stand-in for Akira**. The Akira file has not been supplied, and the repo only has Unbounded 300-700, so 800-900 was not available.
- Small header, part labels and parts line: Unbounded 500. Fine print: Unbounded 400.
- Next to the wordmark: "SHOP DEALS NOW" in Unbounded 400 and "WWW.EPSILON.PLUS" in Unbounded 300.
- Checks: -14.0 LUFS, sync unchanged, safezone text boxes OK.

## v0.6 (owner notes 2026-11-18: "change text to Paint matching available"; "make the parts fall at constant speed so it looks like natural rain")
- Fine print is now "PAINT MATCHING AVAILABLE" (Unbounded 400).
- Hero parts fall at a constant speed along the same straight lines (no gravity ramp): 10 m/s, or the v_min that keeps the last pre-landing frame clear of the body (front lip 16.5, rear lip 18.8 m/s). Frame before impact vs contact zone: lip 0.55/0.50, skirts 0.36/0.30, rear lip 0.63/0.54, wing 0.33/0.06 m. The rain already fell at constant screen speed. Re-rendered take frames 12-157 only (both layers).
- Headlines in **Akira Expanded Super Bold** (owner licence; file gitignored): BLACK FRIDAY 804, 30% OFF 847, THE FULL KIT 750 px wide (limit 872). All glyphs present.
- Checks: sync -17..+12 ms on decoded audio; -14.0 LUFS, peak -3.0 dBFS; safezone text boxes OK; edge test 8 frames (hero parts entering through top corners only, was 11).

### Lookbook fitment check (BF6 lesson, 2026-11-18)
Point-to-surface distance from each shown lookbook part to body/trim/underbody (Blender BVH), plus seam close-ups (workbench, part in red):
| GLB | part | min | closest 10 % within |
|---|---|---|---|
| FE v9 | front lip | 0.0 | 2.2 mm |
| FE v9 | side skirts | 0.0 | 1.4 mm |
| FE v9 | rear lip | 0.0 | 2.4 mm |
| FE v9 | wing (duckbill) | 0.0 | 3.7 mm |
| FL v8 | front lip | 0.0 | 2.2 mm |
| FL v8 | side skirts | 0.0 | 1.4 mm |
| FL v8 | sport wing | 1.0 | 4.1 mm |
All within the ~5 mm rule; close-ups show no floating gap or poke-through. No re-seat or re-render needed.

## Readability audit of v0.6 (owner rule 2026-11-18: slow down text sections; min 2.5 s for 1-3 words +0.4 s/extra word, >=3 s for prices)
Fully readable time = from end of fade-in to start of fade-out (comp.py env()).
| Text | Words | Needs | v0.6 has | |
|---|---|---|---|---|
| BLACK FRIDAY (intro title) | 2 | 2.5 s | 1.47 s | FAIL |
| FRONT LIP label | 2 | 2.5 | 0.77 | FAIL |
| SIDE SKIRTS label | 2 | 2.5 | 0.83 | FAIL |
| REAR LIP label | 2 | 2.5 | 0.77 | FAIL |
| SPORT WING label | 2 | 2.5 | 0.87 | FAIL |
| BLACK FRIDAY / 30% OFF / THE FULL KIT (price) | 6 | 3.0 (price) | 3.83 | ok |
| CIVIC FE · LIP · SKIRTS · REAR LIP · WING | 7 | 4.1 | 2.2 | FAIL |
| CIVIC FL · LIP · SKIRTS · WING | 5 | 3.3 | 1.6 | FAIL |
| PAINT MATCHING AVAILABLE | 3 | 2.5 | 3.83 | ok |
| SHOP DEALS NOW / WWW.EPSILON.PLUS | 3+1 | 2.5 | 2.33 | FAIL |

Plan for v0.7: title held to ~2.6 s (comp only); part labels build up into a list that stays until the cut, and the take holds 2 more bars after the wing landing so SPORT WING gets >=2.5 s (extra take frames); offer shots lengthened to FE >=4.3 s and FL >=3.5 s (longer, slower CGI pans); end card text >=2.7 s. Cuts move to later onset peaks; video grows from 15.7 s to about 21 s.
**Update 2026-11-18 (owner via parent):** the timing rule is revised to 1.8 s for 1-3 words, +0.3 s per extra word, 2.2 s for prices. It applies only to new videos or to versions already being changed. The v0.7 re-cut above is DROPPED; v0.6 stays current. Apply the revised minimums only if the owner asks for other changes.
