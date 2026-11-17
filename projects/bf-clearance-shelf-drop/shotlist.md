# BF video 5 of 8: "Clearance Shelf Drop" (shot list v2, NOT APPROVED)

Status: plan only. Nothing is rendered until the owner approves it in chat.
Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`.

v2 changes:
- Characters are now Del & Eps (the owner's Epsilon+ mascots, per `projects/_blackfriday/MASCOT_AND_PRICES.md`) instead
  of Pip & Gus.
- The BF prices come from the owner's BF doc.
- The look is the Del & Eps "same material as the car" silver on black, with Team Livery A colour on the characters.

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

## Characters: Del & Eps (Epsilon+)
From MASCOT_AND_PRICES.md. Concept sketches only: I searched Drive and Dropbox for "Del", "Eps", "mascot" and
"turnaround" and found no model, rig or turnaround, so building them is part of this plan.
- **Look rule:** they are built at 1:1, they scan in (a laser sweep builds them from wireframe to silver), and the car
  stays the brightest thing in frame. They are under 15k tris each and share one rig.
- **Colour: Team Livery A** (the page's recommended base; the owner hasn't picked, so this is my default, Q5):
  - Del: petrol teal #0f5c63 with signal orange #ff7a1a.
  - Eps: electric violet #6b3cff with hi-vis yellow #ffd21f.
  - A part washes violet while Eps handles it and orange while Del checks it.
- **Roles here:** Del drives the forklift (calm, dry; he never hypes or quotes numbers). Eps rides the forks with the
  handheld scanner (laser blue) and does the tag flips. No lip-sync is needed: Del has a moustache, and Eps's visor
  eye-marks pulse when he talks.
- **Voice:** music only by default. An optional line can go on the last carbon beat, Del: "Fourteen. Then it's
  gone." That line quotes a live number, so it is only used if the count is still 14 on posting day (Q6).
- **End sting (optional, +1.5 s):** Eps pats his pockets ("Where's my 10 mm?"), and Del holds it up.

## Music candidates (real tracks only: none generated, none reused)
Tracks already used by other reels are excluded: the John Wick medley, M.O.O.N. "Paris", Sector Shift, the "Going Up
North", East City, South City and Riders uploads, the GT2 licence track, and the rest of `projects/*/project.yaml`.
1. A track from Dropbox `/Moosic` (29 tracks: GT2, Juiced, NFSU...) that is not already used: 115-130 BPM, a kick on
   every beat, and a drop about 2 s in.
2. If the ad will be boosted, a track from the TikTok/IG Commercial Music Library, because paid ads need cleared audio.
3. Tag flips go on the snare, or on a "ka-ching" accent if the track has one.
Mix to -14 LUFS with true peak below -1 dBFS. Start from the song's beginning, or 2 kicks before the drop.

## Shot table
Times assume 120 BPM (1 beat = 0.5 s) and will be re-snapped to `ive beats`. Every cut sits on a measured kick.

| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.0 | 2.0 | 1-4 | Forklift POV, 1.6 m, 24 mm, forks in the bottom of frame, slow push | Dark warehouse aisle: racking in satin grey, aisle lamps, Epsilon+ boxes. Del's teal glove on the wheel; Eps on the forks | Del & Eps (new build, `tools/mascots.py`, from the concept artifacts MyfYpve1ho7AhiTSzvRCFf / E2AUcUQJsG5a937FCorTQD). Warehouse: new `tools/warehouse_env.py` | The light banks snap on one per beat. Del and Eps scan in (a laser sweep from wireframe to their livery) on beats 2-3 | `BLACK FRIDAY` lit sign on the racking (in-world, no data) | cut on beat 4 | Blender Cycles |
| 2 | 2.0-3.5 | 1.5 | 4-7 | Same POV; the pallet slides in and stops centre-frame | FG2 front lip on a pallet, with a hanging tag | `part_front_lip` in `eps-honda-civic-fg2-v10.glb` (CDN; sha256 a7094b28c397...; Drive zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7), lookbook material | Eps sweeps it (blue laser; the lip washes violet). **The tag flips on beat 6** | `FG2 CIVIC FRONT LIP` / ~~$150~~ -> `$79.99` / `IN STOCK` (owner BF doc + Shopify stock > 0) | **hard 1:1 cut** on beat 8 | Blender Cycles; the tag is a 3D card textured from `store_snapshot.json` |
| 3 | 3.5-4.5 | 1.0 | 8-9 | Locked to the lip framing, pull back 15 % | FG2 scan with the lip, house silver on black | `Civic FG2 Full Car (LQ).stl` 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH + `FG2 Race Lip.stl` 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd (same frame) | Reveal the nose | none | cut on beat 10 | Cycles `--look silver` |
| 4 | 4.5-6.0 | 1.5 | 10-12 | POV; the pallet enters from the left | Integra rear trunk lip, gloss black | `part_duckbill` (= trunk lip) in `eps-acura-integra-de-v29.glb` (sha256 4bc2e068a4c9...; ships `body_duckbill_stock`) | Del leans out and checks it with calipers (orange wash); the tag flips on beat 11 | `INTEGRA TRUNK LIP` / ~~$100~~ -> `$40` (owner doc) | hard 1:1 cut on beat 13 | Cycles |
| 5 | 6.0-7.0 | 1.0 | 13-14 | Same lip framing, rear 3/4, 10 deg orbit | Integra lookbook CGI car with the trunk lip | `eps-acura-integra-de-v29.glb` (stock duckbill hidden), or the DE5 `eps-acura-integra-type-s-de5-v19.glb` (Q4) | Orbit | none | cut on beat 15 | Cycles |
| 6 | 7.0-8.5 | 1.5 | 15-17 | POV; the forks lift a pallet up into frame | WRX VB front lip | `WRX VB NBR Front Lip Uncut.stl` Drive 1FcMcvYcdXTIcdtiHf9ogIKp8fZKvcx7H (the VB GLB v12 has no lip part) | Eps sweeps it; the tag spins to its red clearance side on beat 16 | `WRX VB FRONT LIP` / ~~$99.99~~ -> `$79.99` (owner doc) | hard 1:1 cut on beat 18 | Cycles |
| 7 | 8.5-9.5 | 1.0 | 18-19 | Same framing, front 3/4 low, push in 10 % | VB scan with the lip, silver | `Subaru WRX VB (2022+)/Scan Files/Full Car.stl` (1251 MB) + lip STL; clip check | Push in | none | cut on beat 20 | Cycles `--look silver` |
| 8 | 9.5-11.5 | 2.0 | 20-23 | The POV brakes; tilt up to a top-shelf bay in a spotlight | GR Corolla V1 lips: a PU pallet and a short carbon stack | `part_front_lip` (V1 / Zenki; not `_v2` or `_2025`) in `eps-toyota-gr-corolla-v23.glb` (sha256 ee3643bea3d4...); a carbon material on a copy. Optional: the stack is 14 boxes | Del brakes hard and the forks dip. Both tags flip on beat 22 | `GR COROLLA V1 LIP` / PU ~~$215~~ -> `$129` / CARBON ~~$600~~ -> `$330` (owner doc; carbon pending Q1) | hard 1:1 cut on beat 24 | Cycles |
| 9 | 11.5-14.0 | 2.5 | 24-28 | Same lip framing, then a pull back | GR Corolla full scan with the V1 lip (silver); Eps (micro mode, about 1:10) stands on the lip end | `Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` (836 MB) + the V1 lip in the GLB/CAD frame (stock lip zone cut, the kit_nest2 rule) | The lip lands on beat 25. Eps holds up 1 finger to camera | `ONLY 14 LEFT IN CARBON` (Shopify Carbon Fiber `inventoryQuantity`, re-read on the render and posting days), on black beside the car, not over it | cut on beat 29 | Cycles + Remotion text |
| 10 | 14.0-16.0 | 2.0 | 29-32 | Static | Epsilon+ wordmark (about 720 px wide) + `EPSILON.PLUS` | Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | Wordmark in on beat 29 | `BLACK FRIDAY CLEARANCE` / `EPSILON.PLUS` (no dates until the window is set) | end, or the sting | Remotion |
| 11 (optional) | 16.0-17.5 | 1.5 | 33-35 | Medium two-shot | Del & Eps by the forklift | Same build | 10 mm gag: Eps pats his pockets, and Del holds up the socket | none | end | Cycles |

Rules this plan keeps:
- No IRL footage, so no text goes over IRL. The tags are in-world CGI props.
- Every transformation is a hard cut on a beat.
- No shot is reused.
- Every price and count is from the owner doc and the live store, saved in a snapshot.
- Kit parts keep their lookbook materials; scans stay as captured.
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
| Del & Eps | concept artifacts MyfYpve1ho7AhiTSzvRCFf (v0.1), E2AUcUQJsG5a937FCorTQD (v0.2 colour) | concept only; **model/rig missing, so it is built in this plan** |
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
5. **Del & Eps colour:** I've defaulted to **A, Team Livery**. OK? Building them (two characters under 15k tris, one
   rig, scan-in effect) is the biggest job in this video. Is a Blender build OK?
6. **Voice:** music only, or Del's one line ("Fourteen. Then it's gone.")? Should the 10 mm end sting go in (+1.5 s)?
7. **Warehouse:** is a CGI warehouse OK? If you'd rather film a pass down real racks, price tags over that footage would
   break the no-text-over-IRL rule, so please say explicitly if you want that for this ad.
8. **Music:** which track?

## Production steps (after approval)
1. `ive log` the answers. Snapshot the Shopify prices, compare-at prices and inventory, plus the BF prices, into
   `projects/bf-clearance-shelf-drop/store_snapshot.json`. The tag textures are built only from it.
2. Music: `ive beats` (kick-anchored). Re-snap the shot table.
3. Build Del & Eps: Blender procedural build, one shared rig, a scan-in shader, Team Livery A, and the actions point /
   hold / drive / sweep. Use the Pip & Gus pipeline as the technical precedent only. Turntable check before animating.
4. Build the warehouse env + forklift. Import the lips from the GLBs/CAD with lookbook materials. Make the tag cards and
   the flip animation.
5. Render the shelf shots (2, 4, 6, 8) and keep each lip's camera. Render the 1:1 car shots (3, 5, 7, 9) from the same
   cameras. Place each lip from its design frame, cut the stock zone, and run a clip check. Renders go in the
   background, one at a time, with the scans decimated out-of-core.
6. Remotion: the shot 9 count text and the end card. `ive assemble` 9:16 at 30 fps; mix to -14 LUFS / TP < -1 dBFS;
   verify the cuts against the kicks.
7. Contact sheet, the frames around every cut, and `review.md` from `training/rubric.md`.
8. On posting day, re-read the stock. If the carbon count has changed, re-render only the Remotion text.
