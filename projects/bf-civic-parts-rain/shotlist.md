# BF 1/8: "civic-parts-rain" shot list (DRAFT, waiting for the owner's approval)

Planned 2026-11-17. Nothing is rendered until the owner approves this plan in chat.

**Owner concept (verbatim):** "Civic with parts Raining. Slow pan Civic FE or FL with the lip kit parts falling down (like dollar bills raining over the screen but with parts instead) 'Black Friday: 30% off the full kit.'"

**One line:** one slow pan around a silver Civic FE scan while Epsilon kit parts rain down like dollar bills. The Epsilon+ mascots **Del & Eps** are standing in the rain at real scale beside the car: Eps catches parts and Del seats the four kit parts in their real places. A hard 1:1 cut goes to the finished car, then to the painted lookbook car in the rain with the offer, and the video ends on the Epsilon+ wordmark.

**Format:** 1080x1920, 30 fps, **about 16-18 s** (8 bars at about 120-128 BPM; the exact beat times are measured once the track is picked).

**Recommended car: FE (sedan, FE1 facelift).** Reasons, all from the files:
- The FE1 facelift full scan is the clean capture. The FL2 hatch scan has a broken rear wheel and a hole in the roof (honda-civic-11/clips.md).
- Ron's production STLs for the FE lip, skirts and rear lip are already registered on this scan (rigid ICP, median 1.4 mm, honda-civic-11 v5, approved). His FL rear lip (EP-HC11HB-RLV1-PU) exists on Drive but has never been registered.
- The FL rear lip is a PRE-ORDER listing.
- Ron's 7 finished FE renders and the red FE Si photoshoot exist.

---

## Music candidates (to confirm)
The track must be real and licensed, never generated, and not used by an earlier reel. Already used: `honda-civic-11_track.mp3` (generated) and Le Castle Vania (see projects/*/project.yaml). It starts from the song's beginning and is mixed at -14 LUFS with true peak below -1 dBFS.
- Each BF video uses a different track: claim it in `projects/_blackfriday/MUSIC.md` before settling. GT2 "Arcade Mode Theme" is taken by BF 4; BF 3 is considering "Get Low" (NFSU) and Juiced "Killa".
- **Plan:** pull 3 tracks from the TikTok Commercial Music Library with the Higgsfield `tiktok_music_trending` tool (lesson from gr-corolla). Pick ones with a hard kick from bar 1, at 115-130 BPM, so every cut and landing has a hit. Bouncy, flex-y and "money"-energy, to suit the bills-raining joke.
- If the owner has a song in mind, it takes priority.
- Beat labels below (B1 = first downbeat, 4 beats per bar) are placeholders until `ive beats` plus the kick-peak fit are run on the chosen track.

## Shot table
Times assume 2.0 s bars (120 BPM) and will be re-timed onto measured kicks. Camera frame is the honda-civic-11 scan frame: front +Y, car's left -X, floor z=0. All 3D is Blender 5.3 Cycles CPU in the silver-on-black scan look, unless the row says otherwise.

| # | Time | Dur | Beat | Camera | Subject | Source asset (path / ID) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-4.00 | 4.0 | B1-B8 | Low front-left 3/4 (az ~25, h 0.6 m, f35). Slow pan to the left side (az ~25 -> 70) with ease, car ~85-90 % of frame width | Stock FE1 scan, silver; parts raining | Scan: `civic Facelift FE1 Full Car.stl` (Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ), prepped as in honda-civic-11 (car4.json frame, 4 mm). **Rain:** lookbook GLB `eps-honda-civic-sedan-fe-facelift-v9` pieces `part_front_lip`, `part_side_skirts`, `part_rear_lip`, `part_sport_wing` (zip Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) | Parts are already falling on frame 1 (the hook). About 40-60 instanced copies tumble and flutter down like bills, in 3 depth layers: in front of, beside and behind the car. A denser burst lands on B1 and B5. No part touches or passes through the car or the mascots (collision check per frame). **Del & Eps scan in** on B3 (laser sweep, wireframe to solid) at the front-left corner, 1:1 scale. Eps (violet/yellow) looks up, delighted, holding the configurator tablet over his head like an umbrella. Del (teal/orange) is calm, with his arms full. | "BLACK FRIDAY" in on B3, out before B8 (owner's wording) | none; continuous take | Blender (rain = keyed tumble/flutter sim, motion blur) + Remotion title |
| 2 | 4.00-10.00 | 6.0 | B9-B20 | Same take. Pan continues down the left side and round to a rear-left 3/4 (az 70 -> ~140) | Four "hero" parts drop out of the rain and seat on the car | **Seated parts = Ron's production files**, placed with honda-civic-11 `tools/kit_parts2.py` (ron_to_scan.json): front lip `EP-HC11KK-FLV1-PU.stl` (1JXqMKjxm_9vHX3nDcxUPjDnarMpSE8LI), skirts `Side Skirt LH/RH - EP-HC11-SSV1-PU-LH/RH.stl` (1hsIKloafHdmqjKf40Qy7hqg17gWlpMVM / 1YFnrIOQsMQuHiLwquamkHJ6pyr3ydX68), rear lip `EP-HC11SD-RLV1-PU.stl` (1yMCICyK4xGrTQzSvaHkzj_JbjAN_T0Y6), Sport Wing = `wing.002` from `Honda Civic Sedan 2022-render.blend` (1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ). Placement uses Ron's files, NOT the lookbook (the lookbook parts sat 7-8 cm off in honda-civic-11 v4). Ron's frame comes from `Civic 11th gen lip kit review.blend` (19ySWB7EGGFfgjQNo-3tOxTTIoKiv0E3w) | Each part falls flat and spinning like the rain. **Eps catches it** (the part washes violet), **hands it to Del** (it washes orange while he checks it), and Del seats it on a hit. The handoffs are cheap, pose-to-pose (lift, hold up, place). On a 4-beat bar there is room for about one handoff per part, so the rain does the rest. Seating hits: lip on B9, left skirt on B11 (right skirt seats unseen), rear lip on B14, wing on B17. The rain thins after each landing and stops by B19. Parts are white satin, as in the approved v5 (gloss black disappears on black). | Optional Del line on screen as a caption over the scan shot, from his v0.1 lines ("Tape first." / "Measure twice, drill once."). No voice is needed, because he has a moustache and Eps has a visor (no lip-sync). Optional HUD label per landing, e.g. FRONT LIP / SIDE SKIRTS / REAR LIP / SPORT WING (product names from the Shopify titles). Max one at a time, kept out of the car silhouette | none; same take ends on the solved pose of shot 3 | Blender (+ Remotion labels) |
| 3 | 10.00-12.00 | 2.0 | B21-B24 | **Hard 1:1 cut on B21** to the same pose, slow push continues | The finished kitted FE, real | **Preferred:** a finished photo of the red FE Si with all four parts fitted, rear-left 3/4 (Dropbox `/1. Epsilon Plus Videos/4. Photoshoots/FE Civic Si`, id:2nzlLXSF_sUAAAAAAAAHyg; also `/3. Epsilon Motorsports/Photoshoot/FE1`). Camera solved from landmarks (FG2 photo procedure). **Fallback:** Ron's `7FinalSedanFL.jpg` (1KHccoGDROajdOmue_ie8XU56mz-GSeFu), whose camera is already solved (honda-civic-11 v5, IoU 0.87) | Hold with **no push-in** (owner disliked the push-in on the last photo in de5-configurator); at most a gentle zoom OUT (FG2 lesson for landscape photos). Payoff: the parts that rained are now on a real car. Option the owner asked for on de5: a 1-2 beat flash of real install footage just before this cut (Dropbox `/1. Epsilon Plus Videos/1. Video dumps/FE Civic Sedan install tutorial/`, e.g. the lip or wing install), no text. | **None** (no text over IRL) | Hard cut on B25 | Footage/photo edit (ive assemble); Blender still for the 1:1 layer |
| 4 | 12.00-15.00 | 3.0 | B25-B30 | Low front-left 3/4, slow pan (mirrors shot 1 so the video bookends) | Painted lookbook CGI FE with the full kit, rain resumes | Lookbook GLB `eps-honda-civic-sedan-fe-facelift-v9` (body + its own part_* pieces, paint material set to the chosen colour). The rain uses the same GLB parts in that paint | A short, lighter burst of painted parts falls behind the car (none in front of the text zone). Del & Eps stand by the front wheel; Eps high-fives Del. | **"BLACK FRIDAY"** / **"30% OFF THE FULL KIT"** (owner's wording, matching the owner's BF tiers in MASCOT_AND_PRICES.md). Subline "FRONT LIP · SIDE SKIRTS · REAR LIP · SPORT WING" (Shopify titles). If the wing is shown painted: a small caveat line "Wing: 30% off base price. Paint-match at full price." (owner's tier rule). Optional strike-through total **$1,420 → $994**, for the unpainted PU parts + gloss-black wing; owner must OK it, see Q3. Text in the black above the car, 80 px inside the edges | Hard cut on B31 | Blender (EEVEE or Cycles) + Remotion text |
| 5 | 15.00-17.00 | 2.0 | B31-B34 | Static | Epsilon+ wordmark card | `EPSILON+ Logos/Epsilon+ Logo.png` (Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W, folder 1eubx28c6OHGQVRYQC7um676DnlKhQavC), wordmark ~720 px wide on black | Wordmark lands on B31. End sting (the mascots' running gag): a single **10 mm socket** falls past the wordmark. Eps (off-screen) asks "Where's my 10 mm?" as a caption. Del's hand comes up from below the frame and pockets it. Music tail and fade | Optional: "EPSILON.PLUS" under the wordmark (to confirm; the wing-configurator reel ended on "try it now on epsilon.plus") | end | Remotion |

Rules checked: every cut and landing is on a measured hit; the one transformation cut (shot 2 -> 3) is a hard 1:1 cut, never a dissolve; there is no text over the photo; the mascots are not in the IRL photo shot; the scan is shown as captured (no panels removed, plate kept); parts sit at Ron's design positions; and the first, middle and last frames of every shot will be contact-sheeted for clipping before assembly.

## Asset inventory
| Asset | Where | Status |
|---|---|---|
| FE1 facelift full-car scan | Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ (1.25 GB) | **found**. Must be re-fetched and re-prepped: this container is fresh and `/home/user/media/honda-civic-11/` is gone. Rebuild with the honda-civic-11 tools (deground, patch_holes, fill_top, car4.json). |
| Ron's production lip / skirts / rear lip STLs | Drive ids above (folder 1q8GuJJ7KepKaNKf_3_irSn023RIPRL4s) | **found** |
| Ron's design + render scenes (wing.002, registration) | `Civic 11th gen lip kit review.blend` 19ySWB7E..., `Honda Civic Sedan 2022-render.blend` 1Q8maWoJ... | **found**. kit/ron_to_scan.json must be recomputed (ICP), since it was in deleted media. |
| Lookbook GLB FE facelift (v9), also FE v10, FL v8 / FL facelift v8 | zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7 (203 MB) | **found** (part names verified in honda-civic-11 `tools/glb_export.py`) |
| Ron's finished renders 1-7 | Drive folder `Final-Sedan-FL` 1CB7uZjUwrs-4jYlyR1fVaEH5-mGD9s6v | **found** |
| Finished photos of the kitted FE | Dropbox `4. Photoshoots/FE Civic Si`; `3. Epsilon Motorsports/Photoshoot/FE1` | **found, still to check**: does a photo show all four parts in their finished state, at a solvable rear-left 3/4, and is it the facelift front end? |
| FL rear lip production STL | `Uncut-EP-HC11HB-RLV1-PU (Sep 14).stl` 1zW9GkWyhuWufaeZO6wfzIZ3RwJR3R8TU | found; only needed if the owner picks the FL |
| FL2 full scan | `Full Car Hatchback FL2_5.stl` 1uY7W6y5hYD8g7xHUb6vlSzDITxOIWeqj | found; has defects (rear wheel, roof hole) |
| Epsilon+ wordmark | `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | found |
| FE install footage (optional, before the 1:1 cut) | Dropbox `/1. Epsilon Plus Videos/1. Video dumps/FE Civic Sedan install tutorial/` (`FECivicLipInstall-Final.mp4`, `FECivicWingInstall-Final.mp4`, 6 short drafts) | found (parent's ASSETS.md), clips not yet watched |
| FE painted photos | Drive `11th Gen Civic/FE1/FE2/Painted` 1lqmrDTe9JGETK_3B7mkB_1vnIk-ep2L_ (61 files) | found, colour unknown, to check |
| Epsilon mascots **Del & Eps** (owner's choice, relayed by the parent) | Concept sheets only: claude.ai artifacts v0.1 MyfYpve1ho7AhiTSzvRCFf and v0.2 colour variants E2AUcUQJsG5a937FCorTQD; summary in `projects/_blackfriday/MASCOT_AND_PRICES.md` | **design found, model/rig missing**. Searched Drive and Dropbox for Del/Eps/mascot/turnaround: no files. The build is part of this plan (see production steps). Colour **A, Team Livery** by default (Del teal #0f5c63 + orange #ff7a1a, Eps violet #6b3cff + yellow #ffd21f). |
| Pip & Gus | pip-gus-ep* branches | not used (they are the Illumaesthetic mascots); their Blender procedural build is only the technical precedent |
| Music | TikTok CML | **to-request / to pick** |

## Live store data (Shopify "Epsilon+ Aerodynamics", read 2026-11-17)
| FE "full kit" part | Unpainted / gloss black | Paint-matched | Stock (all variants) |
|---|---|---|---|
| Front Lip – Civic Sedan/Hatch **KOUKI** FE/FL 2025+ | $285 PU | $485 | -10 (backordered) |
| Front Lip – Civic Sedan/Hatch **ZENKI** FE/FL 2022-24 | $285 PU | $485 | -12 (backordered) |
| Side Skirts – Civic FE/FL 2022+ | $400 PU | $800 | -10 (backordered) |
| Rear Lip – Civic Sedan FE 2022+ | $285 PU | $485 | -11 (backordered) |
| Sport Wing – Civic Sedan FE 2022+ (Wingless or Si Factory Duckbill fitment) | $450 gloss black | $850-$900 | -36 (backordered) |
| *FL only:* (PRE-ORDER) Rear Lip – Civic Hatchback FL | $285 PU | – | -1 |
| *FL only:* Sport Wing – Civic Hatchback FL2/FL5 | $450 gloss black | $850 | -41 |

- **Owner's BF tiers** (MASCOT_AND_PRICES.md, from the "Black Friday 2026 Discounts: TL;DR" doc): Civic FE/FL PU front lips (zenki + kouki), side skirts and the FE rear lip are 30% off. The Sport Wings are 30% off the **base price only**, and the paint-match charge stays at full price. So "30% off the full kit" holds for the PU parts + base wing. FE BF prices: lip $285 → $199.50, skirts $400 → $280, rear lip $285 → $199.50, gloss wing $450 → $315; total **$1,420 → $994**. A painted FE wing would be $850 → $715 (paint charge $400 at full price; my arithmetic from the rule, to confirm). The sale dates are not set, so no dates go on screen.
- **Conflict to resolve:** the same doc says "Not on sale: anything on preorder or backorder", but every Civic 11 kit part shows negative stock (backordered) in the live store right now. The **FL rear lip is a PRE-ORDER and is not in the 30% list** (only the "Civic FE rear lip" is), so an FL "full kit" would not be fully 30% off. That is one more reason to pick the FE.
- No "full kit" bundle product exists in the store.
- On-screen dollar figures are shown only if the owner says yes, and they are re-checked against the live store once the sale is live.
- Every Civic 11 part currently shows negative stock, so there is no "only X left" anywhere.
- Store oddity seen while reading: several paint-matched FL2 and FE-duckbill wing variants have a compare-at price *lower* than the price (e.g. FL2 painted $850, compare-at $650; FE Urban Gray $850 / $400). This matters if Black Friday uses strike-through prices.

## Open questions for the owner
1. **FE or FL?** I recommend the **FE**, for the reasons above.
2. **"Full kit" = front lip + side skirts + rear lip + Sport Wing?** And for the FE:
   - the **kouki (2025+) or zenki** front lip? The scan and Ron's lip are the facelift.
   - the **Wingless or Si Factory Duckbill** wing fitment?
3. **Prices on screen?** "30% OFF THE FULL KIT" alone, or with the strike-through total **$1,420 → $994** (unpainted PU parts + gloss-black wing)? If a painted wing is shown, I'll add the caveat "paint-match at full price".
4. **Backorder vs. "not on sale":** your discount doc excludes backordered and pre-order items, and all four Civic FE parts show negative stock right now. Will they be restocked or included anyway? Should the card add any shipping wording (yours)?
5. **CGI paint colour** for shot 4? I suggest Rallye Red R513 (sold for all four FE parts, matches the red FE Si shoot), or white to match Ron's renders.
6. **Real footage:** shot 3 uses a finished photo of the kitted car (no text on it). If no FE Si photo shows all four parts in their finished state, is Ron's render 7 an OK stand-in?
7. **Del & Eps:** I'm using them as relayed (colour **A, Team Livery**, by default; tell me if you want B or C). They are silent, with captions only (no voices needed). The 10 mm socket gag is the end sting. Is that OK? They exist only as concept sketches, so a simple Blender build comes first (about 15k tris each, a few poses, no full rig).
8. **Music rule:** the scan reels require real, licensed music, but the Pip & Gus episodes use generated music. Which rule applies to this ad? Also, do you have a song in mind? (`/Moosic` holds 29 tracks; otherwise I'll send 3 TikTok CML picks.)
10. **Install footage:** on the de5 reel you wanted install footage before the 3D-to-real cut. Should I add a 1-2 beat flash of the FE lip or wing install tutorial before shot 3?
9. **End card:** wordmark alone, or with "EPSILON.PLUS"?

## Production steps (after approval)
1. Fetch the FE1 scan, Ron's STLs and .blends, and the GLB zip into `/home/user/media/bf-civic-parts-rain/`. Rebuild the prepped car and `ron_to_scan.json` with the honda-civic-11 tools, and check the registration with a red overlay (lessons).
2. Export the lookbook part pieces (`glb_export.py`) and build the rain set: instanced copies with randomised tumble and flutter, plus a per-frame no-intersection check against the car.
2b. **Build Del & Eps** (the cheapest path that holds the look): a procedural Blender build after the Pip & Gus `partA_scene.py` pattern, but with the v0.1/v0.2 design: Del's GT-wing flat cap with goggles, moustache, vest and splitter-flat shoulders; Eps's lip-brim backwards cap, strake hoodie and visor with two eye marks. Colour A, under 15k tris each, at real height (Del 1.85 m, Eps 1.70 m). Pose-to-pose only (catch, hold up, hand over, place, high-five), no full rig. Make a turnaround still and send it to the owner for approval BEFORE animating. The scan-in effect is a laser-plane reveal (wireframe to solid) in the same Cycles scene. Hands touching parts must really touch them (contact check).
3. Pick the music and measure it (`ive beats`, kick-peak grid, onset check). Fix the landing frames and the cut frames.
4. Solve the shot-3 camera (photo landmarks, or reuse the render-7 solve). Key the one continuous take (shots 1-2) so it ends exactly on that pose.
5. Run test renders at 30 % (shots 1-2, 4). Make a contact sheet of the first, middle and last frames, and check clipping and parts out of frame. Then do the final renders in the background, one at a time; check for black or unlit frames.
6. Remotion: the title, the optional labels, the offer card and the wordmark (~720 px).
7. Assemble, mix at -14 LUFS / TP < -1 dBFS, run cutcheck against decoded audio, and write review.md with the rubric. Deliver and log feedback.
