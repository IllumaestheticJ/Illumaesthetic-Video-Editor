# BF video 5 of 8: "Clearance Shelf Drop" (shot list v3, NOT APPROVED)

Status: plan only. Nothing is rendered until the owner approves it in chat.
Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`.

v3 (2026-11-17): Del & Eps now follow the owner's LOCKED look (`knowledge/characters/del-and-eps/README.md`,
reference image `del-eps-model-sheet.jpg`, commit 4298535 on `claude/clever-shannon-u8rv5l`):
- arcade-racing-game 3D style;
- the scans stay silver and the characters are the only colour in frame;
- they are made as Higgsfield images/clips from the model sheet and composited over Blender renders of our scans.
This replaces v2's "Team Livery A" and the Blender character build.

v2 changes:
- Characters are now Del & Eps (the owner's Epsilon+ mascots, per `projects/_blackfriday/MASCOT_AND_PRICES.md`) instead
  of Pip & Gus.
- The BF prices come from the owner's BF doc.
- The look was v2's Team Livery A (superseded by the v3 locked look above).

## Concept in one line
A forklift POV rolls through a dark Epsilon+ warehouse. Eps sweeps each pallet with his handheld scanner, and the sweep
flips its price tag from the old price to the BF clearance price. Each lip then hard-cuts 1:1 onto its car, and the
video ends on "ONLY 14 LEFT IN CARBON" and the Epsilon+ wordmark.

Owner's concept, verbatim: "Clearance shelf drop. The warehouse POV. A pallet of GR Corolla V1 lips, Integra trunk lips
and FG2/VB lips with price tags flipping from full price to clearance as each one comes into frame. Use real low counts
like "only X left" to push urgency."

## Target length and format
- About 18 s (36 beats at 120 BPM; re-snapped to the real track's grid). 9:16, 1080x1920, 30 fps.
- Hook: the first tag flip lands on beat 4 (2.0 s).

## Prices and stock (owner BF doc + live Shopify, read 2026-11-17)
BF prices are from the owner's "Black Friday 2026 Discounts: TL;DR" (artifact 29kGfJ2WPdSAg5QpezXfva). The sale is not
live on the site yet, and the window is not set, so no dates go on screen.

| Part (Shopify handle) | Store now (price / compare-at / stock) | BF price (owner doc) | Tag: from -> to | Urgency line |
|---|---|---|---|---|
| GR Corolla V1 lip, PU (`pre-order-epsilon-front-lip-toyota-gr-corolla-e210-2023`) | $215 / $215 / 69 | $129 (40-45 % clearance) | ~~$215~~ -> **$129** | none |
| GR Corolla V1 lip, carbon (same handle) | $600 / $600 / **14** | 45 % off = **$330** (my arithmetic; confirm, Q1) | ~~$600~~ -> **$330** | **ONLY 14 LEFT IN CARBON** (live count) |
| FG2 lip (`epsilon-front-lip-honda-civic-coupe-fg2-2006-2008`) | $150 / **$285** / 64 | flat $79.99 | ~~$150~~ -> **$79.99**, or ~~$285~~ (Q2) | `IN STOCK` |
| Integra rear trunk lip, ABS gloss black (`epsilon-rear-trunk-lip-acura-integra-de4-de5-2023`) | $100 / $200 / **-18 (backorder)** | $40 (60 %) | ~~$100~~ -> **$40** | none (Q3) |
| Integra rear trunk lip, carbon | **no carbon variant on the store** | $96 (doc: $240 -> $96) | only if the variant goes live (Q3) | none |
| WRX VB lip [CLEARANCE] (`vb-wrx-front-lip`) | $99.99 / none / **-15 (backorder)** | flat $79.99 | ~~$99.99~~ -> **$79.99** | none (Q3) |

Conflicts I need you to settle (from the doc itself):
- The doc's "Not on sale" list includes "anything on preorder or backorder", but the Integra trunk lip (-18) and the VB
  lip (-15) are backordered on the store today.
- The GR V1 handle is named `pre-order-...`, but the lip is in stock (69 / 14), so I read it as in stock.
- The only real low positive count is 14 carbon GR V1 lips. The doc notes that last year's BF window sold 33 front lips,
  so 14 can sell out. The count is re-read on the render day and the posting day.

## Characters: Del & Eps (Epsilon+), LOCKED look
Source: `knowledge/characters/del-and-eps/README.md` + `del-eps-model-sheet.jpg` (branch `claude/clever-shannon-u8rv5l`,
commit 4298535; I viewed the sheet: front, 3/4, side and back of both).
- **Del (δ, dad):**
  - Short salt-and-pepper boxed beard (no moustache, no flat cap); headset over a petrol-teal cap with an orange brim.
  - Teal crew shirt with orange shoulders and stripes, teal cargo pants, grey knee pads, black/orange boots.
  - A yellow masking-tape roll on his belt. Low, slow, short sentences.
- **Eps (ε, son):**
  - Violet cap worn backwards (yellow brim at the back), headset, dark visor with two glowing yellow eye marks.
  - Violet shirt with yellow shoulders, white shorts over dark leggings, white sneakers.
  - Handheld scanner (dark grip, two cyan lenses). Bright, fast.
- **No lip-sync** is needed for either: Del's beard covers his mouth, and Eps's expressions are his eye marks.
- **Colour rule:** the characters are the ONLY colour in frame. Everything else is silver/grey on black: the warehouse,
  the racking, the pallets, the lips (silver scan/CAD look) and the cars. The tags are off-white with black type. The
  scanner light is cyan #6fc3d6.
  - This overrides my earlier "lookbook materials" choice for the lips. If you want the lips in their real finish (gloss
    black / carbon), that breaks the character colour rule, so it is Q5.
- **Roles:**
  - Eps sweeps each pallet with the scanner (a cyan beam), which flips the tag.
  - Del walks the aisle with the masking tape and "tags" the last carbon bay.
  - The forklift POV is the camera; nobody's hands are on the wheel, which avoids a tricky composite.
- **Production path (owner):** Higgsfield GPT Image 2.6 stills / short image-to-video clips with the model sheet as the
  reference element. Background removed, then composited over the Blender silver renders, with the same camera angle
  matched by eye and a contact shadow added in Blender.
  - About 6 character plates: Eps scanning x3 angles, Del with tape, Eps micro-mode on the lip, and the 10 mm gag.
  - I'll quote the Higgsfield credits before spending more than about 5.
- **Voice:** music only by default. An optional single Del line goes on the carbon beat: "Fourteen. Then they're
  gone." It quotes the live count, so it is used only if it is still 14 on posting day (Q6).
- **End sting (optional, +1.5 s):** "Where's my 10 mm?" Del holds it up. The README's `del-eps-10mm-socket-gag.jpg`
  is the reference frame.

## Music candidates (real tracks only: none generated, none reused)
Tracks already used by other reels are excluded: the John Wick medley, M.O.O.N. "Paris", Sector Shift, the "Going Up
North", East City, South City and Riders uploads, the GT2 licence track, and the rest of `projects/*/project.yaml`.
1. **Claimed in `projects/_blackfriday/MUSIC.md`: "LUXURY" - Baby thug** (TikTok Commercial Music Library, cleared for
   ads, song_clip_id 7496578190397114385, 107 s). Backup: "Diamonds on me" - Capivara Dj (7634619894408087553).
   Neither is used by any reel. Its BPM and drop are not measured yet (`ive beats` after download). Nearly every
   `/Moosic` track is already used, or claimed by another BF video.
2. If the ad will be boosted, a track from the TikTok/IG Commercial Music Library, because paid ads need cleared audio.
3. Tag flips go on the snare, or on a "ka-ching" accent if the track has one.
Mix to -14 LUFS with true peak below -1 dBFS. Start from the song's beginning, or 2 kicks before the drop.

## Shot table
Times assume 120 BPM (1 beat = 0.5 s) and will be re-snapped to `ive beats`. Every cut sits on a measured kick.

| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.0 | 2.0 | 1-4 | Forklift POV, 1.6 m, 24 mm, forks in the bottom of frame, slow push | Dark warehouse aisle, all silver/grey: racking, aisle lamps, Epsilon+ boxes. Del and Eps (the only colour) walk in from the side of frame | Del & Eps: Higgsfield plates from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`, composited. Warehouse: new `tools/warehouse_env.py` (silver look) | The light banks snap on one per beat. Eps raises the scanner on beat 3 | `BLACK FRIDAY` lit sign on the racking (in-world, no data) | cut on beat 4 | Blender Cycles + composite |
| 2 | 2.0-3.5 | 1.5 | 4-7 | Same POV; the pallet slides in and stops centre-frame | FG2 front lip on a pallet, with a hanging tag | `part_front_lip` in `eps-honda-civic-fg2-v10.glb` (CDN; sha256 a7094b28c397...; Drive zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7), silver | Eps (composited) sweeps it with a cyan beam. **The tag flips on beat 6** | `FG2 CIVIC FRONT LIP` / ~~$150~~ -> `$79.99` / `IN STOCK` (owner BF doc + Shopify stock > 0) | **hard 1:1 cut** on beat 8 | Blender Cycles; the tag is a 3D card textured from `store_snapshot.json` |
| 3 | 3.5-4.5 | 1.0 | 8-9 | Locked to the lip framing, pull back 15 % | FG2 scan with the lip, house silver on black | `Civic FG2 Full Car (LQ).stl` 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH + `FG2 Race Lip.stl` 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd (same frame) | Reveal the nose | none | cut on beat 10 | Cycles `--look silver` |
| 4 | 4.5-6.0 | 1.5 | 10-12 | POV; the pallet enters from the left | Integra rear trunk lip, gloss black | `part_duckbill` (= trunk lip) in `eps-acura-integra-de-v29.glb` (sha256 4bc2e068a4c9...; ships `body_duckbill_stock`) | Del runs a strip of masking tape across the lip (his tape roll); the tag flips on beat 11 | `INTEGRA TRUNK LIP` / ~~$100~~ -> `$40` (owner doc) | hard 1:1 cut on beat 13 | Cycles |
| 5 | 6.0-7.0 | 1.0 | 13-14 | Same lip framing, rear 3/4, 10 deg orbit | Integra car (silver look) with the trunk lip | `eps-acura-integra-de-v29.glb` (stock duckbill hidden), or the DE5 `eps-acura-integra-type-s-de5-v19.glb` (Q4) | Orbit | none | cut on beat 15 | Cycles |
| 6 | 7.0-8.5 | 1.5 | 15-17 | POV; the forks lift a pallet up into frame | WRX VB front lip | `WRX VB NBR Front Lip Uncut.stl` Drive 1FcMcvYcdXTIcdtiHf9ogIKp8fZKvcx7H (the VB GLB v12 has no lip part) | Eps sweeps it; the tag spins to its red clearance side on beat 16 | `WRX VB FRONT LIP` / ~~$99.99~~ -> `$79.99` (owner doc) | hard 1:1 cut on beat 18 | Cycles |
| 7 | 8.5-9.5 | 1.0 | 18-19 | Same framing, front 3/4 low, push in 10 % | VB scan with the lip, silver | `Subaru WRX VB (2022+)/Scan Files/Full Car.stl` (1251 MB) + lip STL; clip check | Push in | none | cut on beat 20 | Cycles `--look silver` |
| 8 | 9.5-11.5 | 2.0 | 20-23 | The POV brakes; tilt up to a top-shelf bay in a spotlight | GR Corolla V1 lips: a PU pallet and a short carbon stack | `part_front_lip` (V1 / Zenki; not `_v2` or `_2025`) in `eps-toyota-gr-corolla-v23.glb` (sha256 ee3643bea3d4...); a carbon material on a copy. Optional: the stack is 14 boxes | The forklift brakes hard and the forks dip. Del slaps a strip of tape on the carbon bay. Both tags flip on beat 22 | `GR COROLLA V1 LIP` / PU ~~$215~~ -> `$129` / CARBON ~~$600~~ -> `$330` (owner doc; carbon pending Q1) | hard 1:1 cut on beat 24 | Cycles |
| 9 | 11.5-14.0 | 2.5 | 24-28 | Same lip framing, then a pull back | GR Corolla full scan with the V1 lip (silver); Eps in micro mode (about 1:10, composited) stands on the lip end | `Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` (836 MB) + the V1 lip in the GLB/CAD frame (stock lip zone cut, the kit_nest2 rule) | The lip lands on beat 25. Eps holds up 1 finger to camera | `ONLY 14 LEFT IN CARBON` (Shopify Carbon Fiber `inventoryQuantity`, re-read on the render and posting days), on black beside the car, not over it | cut on beat 29 | Cycles + Remotion text |
| 10 | 14.0-16.0 | 2.0 | 29-32 | Static | Epsilon+ wordmark (about 720 px wide) + `EPSILON.PLUS` | Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | Wordmark in on beat 29 | `BLACK FRIDAY CLEARANCE` / `EPSILON.PLUS` (no dates until the window is set) | end, or the sting | Remotion |
| 11 (optional) | 16.0-17.5 | 1.5 | 33-35 | Medium two-shot | Del & Eps by the forklift | Same build | 10 mm gag: Eps pats his pockets, and Del holds up the socket | none | end | Cycles |

Rules this plan keeps:
- No IRL footage, so no text goes over IRL. The tags are in-world CGI props.
- Every transformation is a hard cut on a beat.
- No shot is reused.
- Every price and count is from the owner doc and the live store, saved in a snapshot.
- Scans and parts are silver, and the characters are the only colour (the locked Del & Eps rule). Scans stay as captured.
- The Epsilon+ wordmark is used, not the Illumaesthetic logo.

## Asset inventory
| Asset | Path / ID | Status |
|---|---|---|
| FG2 lookbook GLB (`part_front_lip`) | eps-honda-civic-fg2-v10.glb, downloaded to `/home/user/media/bf-clearance-shelf-drop/glb/` | **found** |
| GR Corolla lookbook GLB (`part_front_lip` V1) | eps-toyota-gr-corolla-v23.glb, downloaded | **found** |
| Integra DE4 lookbook GLB (`part_duckbill` = trunk lip, `body_duckbill_stock`) | eps-acura-integra-de-v29.glb, downloaded | **found** |
| Integra DE5 lookbook GLB | eps-acura-integra-type-s-de5-v19.glb, downloaded | found (alternative car) |
| WRX VB lookbook GLB | eps-subaru-wrx-vb-v12.glb, downloaded | found, but it has **no lip part** |
| VB lip CAD | `WRX VB NBR Front Lip Uncut.stl` 1FcMcvYcdXTIcdtiHf9ogIKp8fZKvcx7H | found; confirm it is the sold product (Q3) |
| FG2 lip CAD + LQ scan | 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd / 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH | **found** |
| GR Corolla / VB / Integra Type S full-car scans | knowledge/car-inventory.md | **found** (not downloaded yet) |
| GR Corolla V1 lip CAD fallback | Drive `Corolla V1 & V2 Lip Kit` 1-wEi9unNtRyXDMQlOsgNZWAE0IIhW685 | found |
| Del & Eps | `knowledge/characters/del-and-eps/` (README + del-eps-model-sheet.jpg, 10mm-socket-gag.jpg), branch claude/clever-shannon-u8rv5l @ 4298535; Higgsfield refs bdb1a2e8 / 069f42d6 / e3315b11 / 85f40a22 | **found** (LOCKED look). The plates are generated per shot |
| Warehouse footage | Dropbox search (warehouse / pallet / inventory / shelf): none. Unlabelled `/Footage Library/Videos/Shop & Builds/` and `*Unsorted Video Dump/China/` (Apr 2026) are not reviewed | **missing**; CGI planned |
| Warehouse CGI environment | new `tools/warehouse_env.py` (following mr2 `city_env.py`) | to build |
| Epsilon+ wordmark | 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | **found** |
| BF prices | owner BF doc 29kGfJ2WPdSAg5QpezXfva | **found** (carbon V1 $ and the backorder conflict are open) |
| Music | Dropbox `/Moosic` or a cleared library track | **to-request** |

## Open questions for the owner
1. **Carbon GR V1 lip:** your doc says 45 % off; 45 % off $600 = **$330**. Is $330 the price for the tag?
2. **FG2 tag:** the store shows $150 with a compare-at of $285. Should the tag flip from **$150** (what customers pay
   today) or **$285** (the store's "was")? I recommend $150, because it's the more honest "was" price.
3. **Backordered lips:** your doc says nothing on backorder goes on sale, but the Integra trunk lip (-18) and VB lip
   (-15) are backordered today. Will they be restocked, or should they stay in the video with no stock line? There is
   also no carbon trunk-lip variant on the store, so I show only ABS $100 -> $40 unless you add it. Is
   `WRX VB NBR Front Lip Uncut.stl` the VB lip you sell?
4. Show the trunk lip on the **DE4** lookbook car (v29) or the **DE5 Type S** car?
5. **Lip finish:** with the locked rule (the characters are the only colour), the lips render silver like the scans.
   OK, or do you want them in gloss black / carbon for this sales ad? About 6 Higgsfield character plates are needed;
   I'll quote the credits before generating.
6. **Voice:** music only, or Del's one line ("Fourteen. Then it's gone.")? Should the 10 mm end sting go in (+1.5 s)?
7. **Warehouse:** is a CGI warehouse OK? If you'd rather film a pass down real racks, price tags over that footage would
   break the no-text-over-IRL rule, so please say explicitly if you want that for this ad.
8. **Music:** is "LUXURY" (Baby thug, TikTok cleared) OK, or do you want another track?

## Production steps (after approval)
1. `ive log` the answers. Snapshot the Shopify prices, compare-at prices and inventory, plus the BF prices, into
   `projects/bf-clearance-shelf-drop/store_snapshot.json`. The tag textures are built only from it.
2. Music: `ive beats` (kick-anchored). Re-snap the shot table.
3. Del & Eps plates: Higgsfield GPT Image 2.6 (+ short image-to-video where they move), with the model sheet as the
   reference element. Quote the credits first. Remove the backgrounds, match each plate to its render camera, and
   add contact shadows in Blender. Check each plate against the sheet: Eps's cap backwards, Del's short boxed beard.
4. Build the warehouse env + forklift. Import the lips from the GLBs/CAD in the silver look (lookbook materials only if Q5 says so). Make the tag cards and
   the flip animation.
5. Render the shelf shots (2, 4, 6, 8) and keep each lip's camera. Render the 1:1 car shots (3, 5, 7, 9) from the same
   cameras. Place each lip from its design frame, cut the stock zone, and run a clip check. Renders go in the
   background, one at a time, with the scans decimated out-of-core.
6. Remotion: the shot 9 count text and the end card. `ive assemble` 9:16 at 30 fps; mix to -14 LUFS / TP < -1 dBFS;
   verify the cuts against the kicks.
7. Contact sheet, the frames around every cut, and `review.md` from `training/rubric.md`.
8. On posting day, re-read the stock. If the carbon count has changed, re-render only the Remotion text.
