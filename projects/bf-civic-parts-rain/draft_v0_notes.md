# BF 1/8 civic-parts-rain: draft v0 notes

v0 is a quick, preview-quality first draft. The owner asked "have all the agents make a quick short first draft", relayed by the parent session on 2026-11-17. Output: `/home/user/media/work/out/bf-civic-parts-rain_v0.mp4` (media is not committed).

## What's in it (26.5 s, 1080x1920, 30 fps)
| Time | Shot | Source |
|---|---|---|
| 0.00-16.25 | One continuous take on the silver FE1 scan. Website-kit parts rain like bills; "BLACK FRIDAY" title; Del & Eps placeholders scan in at 5.6 s and out before the drop. Ron's production parts seat on the hits: front lip 10.96 (the drop), side skirts 12.37, rear lip 14.50, Sport Wing 15.53, each with a short label. The rain falls away after the rear lip; the camera ends on render 7's view. | FE1 facelift scan (Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ), Ron's STLs + wing.002, lookbook GLB fe-facelift-v9 |
| 16.25-16.60 | IRL flash: a close push on the real installed front lip (EPSILON tag) | Dropbox `FE Civic Sedan install tutorial/Video Jun 16 2026, 7 54 08 PM.mov`, 0.00-0.33 s |
| 16.60-19.79 | Hard 1:1 cut to Ron's render 7, with a 3% zoom OUT | Drive 1KHccoGDROajdOmue_ie8XU56mz-GSeFu |
| 19.79-21.55 | Lookbook FE in Rallye Red, kit paint-matched, painted parts raining behind it. Offer text: "BLACK FRIDAY / 30% OFF / THE FULL KIT", the parts line, and "PAINT-MATCH AT FULL PRICE". Del & Eps placeholders. | eps-honda-civic-sedan-fe-facelift-v9 |
| 21.55-23.14 | Lookbook FL in Boost Blue, front lip + skirts + Sport Wing, same text | eps-honda-civic-hatch-fl-facelift-v8 |
| 23.14-26.50 | Epsilon+ wordmark (720 px) + "SHOP DEALS NOW / WWW.EPSILON.PLUS"; a 10 mm socket falls past with the caption EPS: "WHERE'S MY 10 MM?"; fade | Drive `EPSILON+ Logos/Epsilon+ Logo.png` |

## Assumptions (my defaults for the open questions; the owner can change any of them)
1. **FL rear lip is left off the FL car.** The BF sheet marks it "No deal" (pre-order), so "30% off the full kit" stays true.
2. **"PAINT-MATCH AT FULL PRICE" fine print is on.** The BF sheet takes 30% off the base price only for paint-matched parts.
3. **Colours:** FE Rallye Red R513 and FL Boost Blue Pearl B637P. These are RGB approximations; no paint data is in the repo.
4. **Music:** "FREAKED OUT" by Fat Papi & prodshushy (TikTok CML, song_clip_id 7644353784302340112), from the song's start. The full 158 s file came from the CML preview URL. BPM measured at 112-113, syncopated, so cuts sit on measured onset peaks rather than a beat grid. Lyrics not checked.
5. **Del & Eps are placeholders, and no Higgsfield credits were spent.** They're cut-outs from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`, each tagged "PLACEHOLDER", with a 2D scan-in/out. They don't touch the car or parts. The "Del pockets the socket" hand is not in v0; only the socket and Eps's line are.
6. **Install flash:** the small clips in the install folder are finished-car shots. The real hands-on install clips are 0.5-0.75 GB, so v0 uses a finished-lip close-up instead.
7. **Wing:** Ron's wing.002 (the v5 wing, the same one render 7 shows) on the scan, and the lookbook duckbill on the CGI FE. That wing.002 is the Si Factory Duckbill version is NOT verified yet.
8. **Wheels:** the scan keeps its scanned wheels, so they change to Ron's gold wheels on the cut to render 7.
9. **Length:** 26.5 s, because the song starts from its beginning (house rule) and its intro is 11 s. Starting nearer the drop would bring it to ~18 s, but needs the owner's OK to break the "from the beginning" rule.
10. **Prices:** only "30% OFF THE FULL KIT", per the owner. No dollar figures, stock counts or dates.

## Known v0 quality limits
- Preview renders: 540x960 Cycles at 10-16 samples, upscaled to 1080x1920; no motion blur.
- A faint outline of the hood hole-fill patch is visible on the scan.
- The rain is a keyed tumble with no collision sim; it is placed so it clears the car and the camera path.
- Mascot placeholders are flat cut-outs: no depth or contact, and the same pose throughout.

## Checks run
See the end of this file, filled in after assembly.
