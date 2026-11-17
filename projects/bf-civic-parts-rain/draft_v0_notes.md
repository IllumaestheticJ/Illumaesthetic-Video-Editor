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
