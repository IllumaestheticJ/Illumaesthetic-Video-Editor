# BF 1/8: "civic-parts-rain" shot list (DRAFT v2.1, no characters)

**Owner, 2026-11-17 (relayed by the parent):** no Del & Eps in any BF video; typical Epsilon+ branding only. Every character shot, cameo and sting is removed.

Planned 2026-11-17. Nothing is rendered until the owner approves this plan in chat.

**Owner answers (in chat, 2026-11-17):** both FE and FL; either front lip; **Si Factory Duckbill** wing; on-screen offer "30% off" (no dollar figures); ignore the Civic backorders; **paint-matched** parts; Ron's renders are OK; **real music**; **yes** to the install flash; end CTA **"SHOP DEALS NOW · WWW.EPSILON.PLUS"**.

**Owner concept (verbatim):** "Civic with parts Raining. Slow pan Civic FE or FL with the lip kit parts falling down (like dollar bills raining over the screen but with parts instead) 'Black Friday: 30% off the full kit.'"

**One line:** one slow pan around a silver Civic FE scan while Epsilon kit parts rain down like dollar bills. A quick flash of a real install, then a hard 1:1 cut to the finished car. The offer runs over two painted lookbook cars in the rain, the FE sedan and then the FL hatch, and the video ends on the Epsilon+ wordmark with "SHOP DEALS NOW · WWW.EPSILON.PLUS".

**Format:** 1080x1920, 30 fps, **about 18-19 s** (8 bars at about 120-128 BPM; the exact beat times are measured once the track is picked).

**Cars: FE and FL (owner).** The scan story (shots 1-3) uses the FE, because only the FE has a clean scan with Ron's parts registered on it. The FL appears in the painted lookbook offer shot (4b). Reasons, all from the files:
- The FE1 facelift full scan is the clean capture. The FL2 hatch scan has a broken rear wheel and a hole in the roof (honda-civic-11/clips.md).
- Ron's production STLs for the FE lip, skirts and rear lip are already registered on this scan (rigid ICP, median 1.4 mm, honda-civic-11 v5, approved). His FL rear lip (EP-HC11HB-RLV1-PU) exists on Drive but has never been registered.
- The FL rear lip is a PRE-ORDER listing.
- Ron's 7 finished FE renders and the red FE Si photoshoot exist.

---

## Music candidates (to confirm)
The track must be real and licensed, never generated, and not used by an earlier reel. Already used: `honda-civic-11_track.mp3` (generated) and Le Castle Vania (see projects/*/project.yaml). It starts from the song's beginning and is mixed at -14 LUFS with true peak below -1 dBFS.
- Each BF video uses a different track: claim it in `projects/_blackfriday/MUSIC.md` before settling. GT2 "Arcade Mode Theme" is taken by BF 4; BF 3 is considering "Get Low" (NFSU) and Juiced "Killa".
- **Real music (owner).** Every `/Moosic` track is already claimed by other BF videos (MUSIC.md), so the candidates come from the TikTok Commercial Music Library (Higgsfield `tiktok_music_trending`, HIP_HOP/RAP, 7-day US chart, read 2026-11-17). None of them is claimed in MUSIC.md:
  1. **"FREAKED OUT" - Fat Papi & prodshushy** (song_clip_id 7644353784302340112, 158 s, chart #6). Provisionally claimed: bouncy and flex-y, fits the "money raining" joke.
  2. "Double Apple" - David Cutter Music (7413011603664259088, 104 s, #8).
  3. "Zero Doubt" - VibeTune (7571420626649581569, 112 s, #51).
  BPM and lyrics are not checked yet; the pick is confirmed after `ive beats` and a listen for a hard kick from bar 1.
- If the owner has a song in mind, it takes priority.
- Beat labels below (B1 = first downbeat, 4 beats per bar) are placeholders until `ive beats` plus the kick-peak fit are run on the chosen track.

## Shot table
Times assume 2.0 s bars (120 BPM) and will be re-timed onto measured kicks. Camera frame is the honda-civic-11 scan frame: front +Y, car's left -X, floor z=0. All 3D is Blender 5.3 Cycles CPU in the silver-on-black scan look, unless the row says otherwise.

| # | Time | Dur | Beat | Camera | Subject | Source asset (path / ID) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-4.00 | 4.0 | B1-B8 | Low front-left 3/4 (az ~25, h 0.6 m, f35). Slow pan to the left side (az ~25 -> 70) with ease, car ~85-90 % of frame width | Stock FE1 scan, silver; parts raining | Scan: `civic Facelift FE1 Full Car.stl` (Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ), prepped as in honda-civic-11 (car4.json frame, 4 mm). **Rain:** lookbook GLB `eps-honda-civic-sedan-fe-facelift-v9` pieces `part_front_lip`, `part_side_skirts`, `part_rear_lip`, `part_sport_wing` (zip Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) | Parts are already falling on frame 1 (the hook). About 40-60 instanced copies tumble and flutter down like bills, in 3 depth layers: in front of, beside and behind the car. A denser burst lands on B1 and B5. No part touches or passes through the car (collision check per frame). | "BLACK FRIDAY" in on B3, out before B8 (owner's wording) | none; continuous take | Blender (rain = keyed tumble/flutter sim, motion blur) + Remotion title |
| 2 | 4.00-10.00 | 6.0 | B9-B20 | Same take. Pan continues down the left side and round to a rear-left 3/4 (az 70 -> ~140) | Four "hero" parts drop out of the rain and seat on the car | **Seated parts = Ron's production files**, placed with honda-civic-11 `tools/kit_parts2.py` (ron_to_scan.json): front lip `EP-HC11KK-FLV1-PU.stl` (1JXqMKjxm_9vHX3nDcxUPjDnarMpSE8LI), skirts `Side Skirt LH/RH - EP-HC11-SSV1-PU-LH/RH.stl` (1hsIKloafHdmqjKf40Qy7hqg17gWlpMVM / 1YFnrIOQsMQuHiLwquamkHJ6pyr3ydX68), rear lip `EP-HC11SD-RLV1-PU.stl` (1yMCICyK4xGrTQzSvaHkzj_JbjAN_T0Y6), Sport Wing = **Si Factory Duckbill** version (owner). `wing.002` from `Honda Civic Sedan 2022-render.blend` (1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ) was used in v5. First check it is the duckbill version. If it isn't, find Ron's duckbill wing file; failing that, use the lookbook `part_sport_wing_duckbill` and check its fit on the trunk with a red overlay. Placement uses Ron's files, NOT the lookbook (the lookbook parts sat 7-8 cm off in honda-civic-11 v4). Ron's frame comes from `Civic 11th gen lip kit review.blend` (19ySWB7EGGFfgjQNo-3tOxTTIoKiv0E3w) | Each part falls flat and spinning like the rain. The four parts seat by themselves on the hits (Blender, Ron's positions), . Seating hits: lip on B9, left skirt on B11 (right skirt seats unseen), rear lip on B14, wing on B17. The rain thins after each landing and stops by B19. Parts are white satin, as in the approved v5 (gloss black disappears on black). | Optional HUD label per landing, e.g. FRONT LIP / SIDE SKIRTS / REAR LIP / SPORT WING (product names from the Shopify titles). Max one at a time, kept out of the car silhouette | none; same take ends on the solved pose of shot 3 | Blender (car, rain, parts) + Remotion labels |
| 2b | 9.50-10.00 | 0.5 | B20 (1 beat) | Install-video framing | Real install flash (owner: yes) | Dropbox `/1. Epsilon Plus Videos/1. Video dumps/FE Civic Sedan install tutorial/` `FECivicLipInstall-Final.mp4` or `FECivicWingInstall-Final.mp4`, best ~0.5 s of hands seating the part | Hands push the lip or wing home, on the beat. The take before it is shortened by 0.5 s | **None** (IRL) | Hard cut on B21 | Footage edit |
| 3 | 10.00-12.00 | 2.0 | B21-B24 | **Hard 1:1 cut on B21** to the pose where shot 2 ended (the 1:1 layer is matched to shot 2's last frame, across the flash) | The finished kitted FE | **Owner OK'd Ron's renders:** `7FinalSedanFL.jpg` (1KHccoGDROajdOmue_ie8XU56mz-GSeFu); its camera is already solved (honda-civic-11 v5, IoU 0.87). It is the default unless a finished photo is better. Other option: a finished photo of the red FE Si with all four parts fitted, rear-left 3/4 (Dropbox `/1. Epsilon Plus Videos/4. Photoshoots/FE Civic Si`, id:2nzlLXSF_sUAAAAAAAAHyg; also `/3. Epsilon Motorsports/Photoshoot/FE1`). Camera solved from landmarks (FG2 photo procedure). Check that render 7's wing is the duckbill. If it isn't, use another of Ron's renders or a photo that shows the duckbill | Hold with **no push-in** (owner disliked the push-in on the last photo in de5-configurator); at most a gentle zoom OUT (FG2 lesson for landscape photos). Payoff: the parts that rained are now on a real car. | **None** (no text over IRL) | Hard cut on B25 | Footage/photo edit (ive assemble); Blender still for the 1:1 layer |
| 4a | 12.00-13.50 | 1.5 | B25-B27 | Low front-left 3/4, slow pan (mirrors shot 1, so the video bookends) | Painted lookbook CGI **FE** sedan with the full kit, **paint-matched** | Lookbook GLB `eps-honda-civic-sedan-fe-facelift-v9` (body + `part_front_lip`, `part_side_skirts`, `part_rear_lip`, `part_sport_wing_duckbill`), with body and parts in the same paint (default **Rallye Red R513**, sold for all four FE parts) | A short, lighter burst of painted parts falls behind the car, none in front of the text zone. | **"BLACK FRIDAY"** / **"30% OFF THE FULL KIT"** (owner: "30% off", no dollar figures). Subline "FRONT LIP · SIDE SKIRTS · REAR LIP · SPORT WING". Small fine print **"Paint-match at full price"**, because the BF sheet takes 30% off the base price only (Q2). No stock counts, no dates. Text in the black above the car, 80 px inside the edges; it stays up across 4a and 4b | Hard cut on B28 | Blender + Remotion text |
| 4b | 13.50-15.00 | 1.5 | B28-B30 | Same camera move, mirrored (front-right 3/4) | Painted lookbook CGI **FL** hatch with its kit, paint-matched | Lookbook GLB `eps-honda-civic-hatch-fl-facelift-v8` (part names to read at export; ASSETS.md doesn't list them). Default paint **Boost Blue Pearl B637P**, an FL colour sold for the FL wing, lip and skirts | Same rain burst. | Same text continues. **The FL rear lip is a pre-order and "No deal" in the BF sheet**, so by default the FL is shown with lip + skirts + Sport Wing only (Q1) | Hard cut on B31 | Blender + Remotion |
| 5 | 15.00-18.50 | 3.5 | B31-B37 | Static | Epsilon+ wordmark card | `EPSILON+ Logos/Epsilon+ Logo.png` (Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W, folder 1eubx28c6OHGQVRYQC7um676DnlKhQavC), wordmark ~720 px wide on black | Wordmark lands on B31, and **"SHOP DEALS NOW · WWW.EPSILON.PLUS"** (owner) appears under it on B32. Music tail and fade | "SHOP DEALS NOW · WWW.EPSILON.PLUS" (owner's wording) | end | Remotion |

Rules checked: every cut and landing is on a measured hit; the one transformation cut (shot 2 -> 3, across the 1-beat install flash) is a hard 1:1 cut, never a dissolve; there is no text over the install flash or the photo/render; the scan is shown as captured (no panels removed, plate kept); parts sit at Ron's design positions; and the first, middle and last frames of every shot will be contact-sheeted for clipping before assembly.

## Asset inventory
| Asset | Where | Status |
|---|---|---|
| FE1 facelift full-car scan | Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ (1.25 GB) | **found**. Must be re-fetched and re-prepped: this container is fresh and `/home/user/media/honda-civic-11/` is gone. Rebuild with the honda-civic-11 tools (deground, patch_holes, fill_top, car4.json). |
| Ron's production lip / skirts / rear lip STLs | Drive ids above (folder 1q8GuJJ7KepKaNKf_3_irSn023RIPRL4s) | **found** |
| Ron's design + render scenes (wing.002, registration) | `Civic 11th gen lip kit review.blend` 19ySWB7E..., `Honda Civic Sedan 2022-render.blend` 1Q8maWoJ... | **found**. kit/ron_to_scan.json must be recomputed (ICP), since it was in deleted media. |
| Lookbook GLB FE facelift (v9), also FE v10, FL v8 / FL facelift v8 | zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7 (203 MB) | **found** (part names verified in honda-civic-11 `tools/glb_export.py`) |
| Ron's finished renders 1-7 | Drive folder `Final-Sedan-FL` 1CB7uZjUwrs-4jYlyR1fVaEH5-mGD9s6v | **found** |
| Finished photos of the kitted FE | Dropbox `4. Photoshoots/FE Civic Si`; `3. Epsilon Motorsports/Photoshoot/FE1` | **found, still to check**: does a photo show all four parts in their finished state, at a solvable rear-left 3/4, and is it the facelift front end? |
| FL rear lip production STL | `Uncut-EP-HC11HB-RLV1-PU (Sep 14).stl` 1zW9GkWyhuWufaeZO6wfzIZ3RwJR3R8TU | found; not needed (the FL appears only as a lookbook CGI car) |
| FL2 full scan | `Full Car Hatchback FL2_5.stl` 1uY7W6y5hYD8g7xHUb6vlSzDITxOIWeqj | found; has defects (rear wheel, roof hole) |
| Epsilon+ wordmark | `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | found |
| FE install footage (optional, before the 1:1 cut) | Dropbox `/1. Epsilon Plus Videos/1. Video dumps/FE Civic Sedan install tutorial/` (`FECivicLipInstall-Final.mp4`, `FECivicWingInstall-Final.mp4`, 6 short drafts) | found (parent's ASSETS.md), clips not yet watched |
| FE painted photos | Drive `11th Gen Civic/FE1/FE2/Painted` 1lqmrDTe9JGETK_3B7mkB_1vnIk-ep2L_ (61 files) | found, colour unknown, to check |
| Epsilon mascots Del & Eps | `knowledge/characters/del-and-eps/` | **not used**: owner, 2026-11-17 (relayed by the parent): "tell all the black friday agents to not use del & eps, just typical branding content" |
| Pip & Gus | pip-gus-ep* branches | not used (they are the Illumaesthetic mascots); their Blender procedural build is only the technical precedent |
| Music | TikTok CML: "FREAKED OUT" 7644353784302340112 (provisional), "Double Apple" 7413011603664259088, "Zero Doubt" 7571420626649581569 | **found; owner to pick** |
| FL lookbook GLB | `eps-honda-civic-hatch-fl-facelift-v8` in the GLB zip | found (name in car-inventory.md); parts to list at export |

## Prices: BF 2026 Liquidation Pricing sheet (owner decision 2026-11-17)
Source: Claude Sheet "Black Friday 2026 Liquidation Pricing", Pricing tab (snapshot `projects/_blackfriday/bf_liquidation_pricing.csv`, rev 25; rules in `projects/_blackfriday/PRICES.md`). The owner said to use it "even if the stock is not right", so backordered items ARE on sale. The crossed-out price is "Current Price" and the sale price is "BF 2026 Price". Re-read the live sheet before final render.

| FE "full kit" part (sheet row) | Was | BF 2026 | Paint-matched (base discount only) |
|---|---|---|---|
| Front Lip – Civic FE/FL Kouki · Unpainted PU (or Zenki, same price) | $285 | **$199.50** | $485 → $399.50 |
| Side Skirts – Civic FE/FL · Unpainted PU | $400 | **$280** | $800 → $680 |
| Rear Lip – Civic Sedan (FE) · Unpainted PU | $285 | **$199.50** | $485 → $399.50 |
| Sport Wing – Civic Sedan FE · Wingless or Si Duckbill, Gloss Black | $450 | **$315** | $850 → $715 |
| **Total** | **$1,420** | **$994** (exactly 30% off) | $2,620 → $2,194 (~16%) |

The owner's on-screen line is "30% off" with no dollar figures, and backorders are ignored (owner). The table is kept as the record of what the line rests on.

- **FL:** the "(PRE-ORDER) Rear Lip – Civic Hatch (FL)" is **No deal** (0%, ships early 2027), so an FL "full kit" is not 30% off: lip $199.50 + skirts $280 + wing $315 + rear lip $285 = $1,079.50 vs $1,420 (24%). The FE is the only car where the line "30% off the full kit" holds exactly.
- **Kit-bundle note:** the sheet's Lip Kits tab prices a kit bought together at only 10% off, and PRICES.md says not to feature "kit price" deals. "30% off the full kit" here means each part is 30% off.
- No stock counts and no sale dates on screen (dates not set yet).
- Store oddity (live Shopify read, 2026-11-17): several paint-matched FL2 and FE-duckbill wing variants have a compare-at price *lower* than the price (e.g. FL2 painted $850, compare-at $650). This matters only if the store's own strike-through is filmed or shown.

## Open questions for the owner (remaining)
1. **FL rear lip:** it's a pre-order and your BF sheet gives it "No deal". By default I'll show the FL hatch with front lip + side skirts + Sport Wing and **no rear lip**, so "30% off the full kit" stays true. Or should I show it anyway?
2. **Paint fine print:** with paint-matched parts, your sheet takes 30% off the base price only, and the paint charge stays full price. A painted FE kit comes out ~16% off ($2,620 → $2,194). I've added small fine print, "Paint-match at full price", under "30% OFF THE FULL KIT". Keep it, or drop it?
3. **Car colours:** Rallye Red for the FE and Boost Blue for the FL by default (both are sold as paint-match colours for those parts). Any other picks?
4. **Song:** pick one of the three TikTok-library tracks above. I've provisionally claimed "FREAKED OUT"; I'll check BPM and lyrics before locking it.


## Production steps (after approval)
1. Fetch the FE1 scan, Ron's STLs and .blends, and the GLB zip into `/home/user/media/bf-civic-parts-rain/`. Rebuild the prepped car and `ron_to_scan.json` with the honda-civic-11 tools, and check the registration with a red overlay (lessons).
2. Export the lookbook part pieces (`glb_export.py`) and build the rain set: instanced copies with randomised tumble and flutter, plus a per-frame no-intersection check against the car.

3. Pick the music and measure it (`ive beats`, kick-peak grid, onset check). Fix the landing frames and the cut frames.
4. Solve the shot-3 camera (photo landmarks, or reuse the render-7 solve). Key the one continuous take (shots 1-2) so it ends exactly on that pose.
5. Run test renders at 30 % (shots 1-2, 4). Make a contact sheet of the first, middle and last frames, and check clipping and parts out of frame. Then do the final renders in the background, one at a time; check for black or unlit frames.
6. Remotion: the title, the optional labels, the offer card and the wordmark (~720 px).
7. Assemble, mix at -14 LUFS / TP < -1 dBFS, run cutcheck against decoded audio, and write review.md with the rubric. Deliver and log feedback.
