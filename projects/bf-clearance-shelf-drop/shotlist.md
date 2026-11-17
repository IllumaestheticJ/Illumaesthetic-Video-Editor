# BF video 5 of 8: "Clearance Shelf Drop" (shot list, NOT APPROVED)

Status: plan only. Nothing is rendered until the owner approves it in chat.
Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`.

## Concept in one line
A forklift POV rolls down a CGI Epsilon+ warehouse aisle. Four lips come into frame on a pallet one at a time, and each
hanging price tag flips from its list price to the sale price. Each part then hard-cuts 1:1 onto its car, and the video
ends on the Epsilon+ wordmark and store CTA.

Owner's concept, verbatim: "Clearance shelf drop. The warehouse POV. A pallet of GR Corolla V1 lips, Integra trunk lips
and FG2/VB lips with price tags flipping from full price to clearance as each one comes into frame. Use real low counts
like "only X left" to push urgency."

## Target length and format
- About 18 s (36 beats at 120 BPM; re-snapped to the real track's grid). 9:16, 1080x1920, 30 fps.
- Hook in the first 2 s: the first tag flip lands on beat 4.

## What the live store says (Shopify "Epsilon+ Aerodynamics", read 2026-11-17)
| Part (handle) | Variant | Price | Compare-at (store's "was") | Stock | What the store really supports |
|---|---|---|---|---|---|
| Front Lip - GR Corolla Zenki (V1) `pre-order-epsilon-front-lip-toyota-gr-corolla-e210-2023` | Polyurethane | $215 | $215 (no markdown) | 69 | In stock, not marked down |
| same | Carbon Fiber | $600 | $600 (no markdown) | **14** | The only lowish count. Not marked down |
| Front Lip - Civic FG2 `epsilon-front-lip-honda-civic-coupe-fg2-2006-2008` | Polyurethane | **$150** | **$285** | 64 | Already marked down $285 -> $150 on the store |
| Rear Trunk Lip - Integra DE4/DE5 `epsilon-rear-trunk-lip-acura-integra-de4-de5-2023` | ABS Gloss Black | **$100** | **$200** | -18 (backorder, CONTINUE) | Already marked down $200 -> $100, but **backordered** |
| same | Paint-matched (10 colours) | $300 | none | 0 to -1 | Made to order / backorder |
| [CLEARANCE] Front Lip - WRX VB `vb-wrx-front-lip` | Polyurethane | $99.99 | none | -15 (backorder) | Titled clearance, no "was" price, **backordered** |

Discounts: no Black Friday 2026 discount exists yet. The active codes are dealer, customer and one-off codes; past
BF discounts were BF2023 (15 % in-stock / 20 % 3-piece front lip, expired). Several of these lips carry the tag
`laborday-exclude` (GR Corolla V1, FG2, Integra trunk lip, VB). So the owner must give the BF price for each part.

### The honest problem with "only X left"
- Only **14 carbon GR Corolla V1 lips** is a real, smallish number. 69 / 64 are healthy, and the Integra and VB lips are
  negative (backordered), so "only X left" would be false for them.
- Counts change daily. Re-read them on the render day and on the posting day, and refuse to post if the number on
  screen no longer matches.

Proposed true wording (each tag shows at most two lines, and every value is re-read from Shopify):
| Part | Top line (flip from -> to) | Urgency line |
|---|---|---|
| FG2 lip | ~~$285~~ -> $150 (store's own compare-at), or the BF price if lower | `IN STOCK` |
| Integra trunk lip (gloss black) | ~~$200~~ -> $100 (store's own compare-at), or the BF price | `BACKORDER: RESERVE YOURS` (no count) |
| WRX VB lip | `CLEARANCE $99.99` (no strike-through: the store has no "was" price) | `BACKORDER` (no count). Or drop it (Q3) |
| GR Corolla V1 lip | ~~$600~~ -> BF price (carbon), ~~$215~~ -> BF price (PU) | **`ONLY 14 LEFT IN CARBON`** (live count) |

## Music candidates (real tracks only: none generated, none reused)
Tracks already used by other reels are excluded: the John Wick medley, M.O.O.N. "Paris", Sector Shift, the "Going Up
North", East City, South City and Riders uploads, and the GT2 licence track. I can't license music, so the owner picks:
1. A commercially cleared track from the TikTok/IG Commercial Music Library at posting time: 115-130 BPM, a hard
   kick on every beat, and a drop about 2 s in. Preferred, because paid/boosted BF ads need cleared audio.
2. An owner-supplied track (as with the GR Corolla and Cappuccino reels), which must not be one of the tracks above.
3. If the track has a cash-register / "ka-ching" accent, the tag flips go on it. Otherwise they go on the snare.
Mix to -14 LUFS with true peak below -1 dBFS, starting from the song's beginning (or from 2 kicks before the drop, as
the FG2 lesson allows).

## Shot table
Times assume 120 BPM (1 beat = 0.5 s) and will be re-snapped to `ive beats` of the chosen track. Every cut sits on a
measured kick.

| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.0 | 2.0 | 1-4 | Forklift-driver POV, 1.6 m high, 24 mm, forks in the bottom of frame, slow push down the aisle | CGI warehouse aisle: racking, pallets wrapped in film, Epsilon+ boxes. Gus drives the forklift (only his mitten hands on the wheel and the goggles' sage lenses in the mirror). Pip rides on the pallet | Characters: Pip & Gus rig + design, `projects/scan-tedium-explainer-reel/characters/design.md` and `tools/partA_scene.py` (branch `claude/pip-gus-ep9-aesub`). Warehouse: new Blender build, `tools/warehouse_env.py` | Lights flicker on one bank at a time on beats 1-3. Pip pops up on beat 4 (^ ^ eyes) | `BLACK FRIDAY` sign on the racking (in-world CGI text, no data) | cut on beat 4 | Blender EEVEE cel-shaded (pilot look) |
| 2 | 2.0-3.5 | 1.5 | 5-7 | Same POV; a pallet slides in from the right and stops centre-frame at 1.1 m | FG2 front lip on a pallet, with a hanging price tag | Lip: `part_front_lip` in `eps-honda-civic-fg2-v10.glb` (CDN, sha256 a7094b28c397...; Drive zip id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) | Tag swings in, then **flips on beat 6** | `FG2 CIVIC FRONT LIP` / ~~$285~~ -> `$150` / `IN STOCK` (Shopify `epsilon-front-lip-honda-civic-coupe-fg2-2006-2008`: price, compareAtPrice, inventoryQuantity>0) | **hard 1:1 cut** on beat 8 (lip keeps size/position) | Blender EEVEE; the tag is a 3D card textured from store data |
| 3 | 3.5-4.5 | 1.0 | 8-9 | Locked to the same lip framing | FG2 scan with the lip fitted, house silver on black | Scan `Civic FG2 Full Car (LQ).stl` Drive 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH + `FG2 Race Lip.stl` 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd (same frame as the scan, per projects/fg2-race-car/clips.md) | Pull back 15 % to reveal the car's nose. No text | none | cut on beat 10 | Blender Cycles `--look silver` |
| 4 | 4.5-6.0 | 1.5 | 10-12 | POV continues; the next pallet enters from the left | Integra trunk lip (gloss black) on a pallet | `part_duckbill` in `eps-acura-integra-type-s-de5-v19.glb` (sha256 4eb01375eebf...). **Confirm it is the trunk-lip product** (Q6). Fallback: Drive folder `Integra wing lip kit` 1dSqALujjLoTSTH_fryIi6yPp0qJGOtiC | Tag flips on beat 11 | `INTEGRA TRUNK LIP` / ~~$200~~ -> `$100` / `BACKORDER: RESERVE YOURS` (Shopify `epsilon-rear-trunk-lip-acura-integra-de4-de5-2023`, ABS Generic Gloss Black) | hard 1:1 cut on beat 13 | Blender EEVEE |
| 5 | 6.0-7.0 | 1.0 | 13-14 | Same lip framing, rear 3/4 | Integra Type S lookbook CGI car with the trunk lip, in lookbook paint | `eps-acura-integra-type-s-de5-v19.glb` (whole car, lookbook materials). Scan alternative: `Acura Integra Type S/Integra Type S Full Car.stl` (1240 MB, Drive engineering) | Slow orbit of 10 deg | none | cut on beat 15 | Blender Cycles |
| 6 | 7.0-8.5 | 1.5 | 15-17 | POV; a pallet rises up from below on the forks | WRX VB front lip | Lip CAD: `WRX VB NBR Front Lip Uncut.stl` Drive 1FcMcvYcdXTIcdtiHf9ogIKp8fZKvcx7H. **The VB lookbook GLB (v12, sha 5ee83049bfca) has no lip part.** Confirm this STL is the [CLEARANCE] product (Q3) | Tag spins on beat 16 to the red CLEARANCE side | `WRX VB FRONT LIP` / `CLEARANCE $99.99` / `BACKORDER` (Shopify `vb-wrx-front-lip`) | hard 1:1 cut on beat 18 | Blender EEVEE |
| 7 | 8.5-9.5 | 1.0 | 18-19 | Same framing, front 3/4 low | VB scan with the lip, silver on black | `Subaru WRX VB (2022+)/Scan Files/Full Car.stl` (1251 MB) + lip STL. Placement from the design file's frame; check it doesn't clip | Push in 10 % | none | cut on beat 20 | Blender Cycles `--look silver` |
| 8 | 9.5-11.5 | 2.0 | 20-23 | POV stops; the camera tilts up to a top shelf, one bay in a spotlight | GR Corolla V1 lips: one carbon and one PU on a pallet. The carbon pallet visibly holds a short stack | `part_front_lip` (= V1 / Zenki 2023; v2 and 2025 are separate parts) in `eps-toyota-gr-corolla-v23.glb` (sha ee3643bea3d4...). The carbon material is applied to a copy. Optional: render the stack as 14 boxes to match the live count | Gus brakes hard (forks dip; Pip's eyes pop 1.3x). Both tags flip on beat 22 | `GR COROLLA V1 LIP` / ~~$600~~ -> `$[BF CF]` / ~~$215~~ -> `$[BF PU]` (owner's BF prices, Q1) | hard 1:1 cut on beat 24 | Blender EEVEE |
| 9 | 11.5-13.5 | 2.0 | 24-27 | Same lip framing, then a pull back | GR Corolla full scan with the V1 lip, silver on black | `Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` (836 MB) + V1 lip placed from the GLB/CAD frame (the GR Corolla project's alignment) | Lip lands on the scan on beat 25 (the stock lip zone is cut first: the kit_nest2 rule) | `ONLY 14 LEFT IN CARBON` (Shopify Carbon Fiber variant inventoryQuantity, re-read on the render and posting days). Shown on the black background beside the car, not over it | cut on beat 28 | Blender Cycles + Remotion text |
| 10 | 13.5-15.5 | 2.0 | 28-31 | Wide, high, looking down the aisle | All four pallets in the warehouse; Pip and Gus beside the forklift, both happy (Gus's ^ ^ eyes; never sad) | Same scene as shot 1 | Pallets drop to the floor on beat 28; the lights go full on beat 30 | `BLACK FRIDAY AT EPSILON.PLUS` (in-world banner) | cut on beat 32 | Blender EEVEE |
| 11 | 15.5-18.0 | 2.5 | 32-36 | Static | Epsilon+ wordmark (about 720 px wide) + CTA | Drive `EPSILON+ Logos` (Epsilon wordmark, per the lessons) | Wordmark in on beat 32, hold to the end | `EPSILON.PLUS` (+ the BF date range if the owner gives one) | end | Remotion |

Rules this plan keeps:
- No IRL footage, so no text goes over IRL.
- The tags are in-world CGI props.
- The real-to-scan style transformations are hard cuts on beats, never dissolves.
- No shot is reused.
- No invented numbers: every price and count comes from Shopify on the render day.
- The kit parts keep their lookbook materials.

## Asset inventory
| Asset | Path / ID | Status |
|---|---|---|
| FG2 lookbook GLB (`part_front_lip`) | cdn.shopify.com/.../eps-honda-civic-fg2-v10.glb, local `/home/user/media/bf-clearance-shelf-drop/glb/` | **found** |
| GR Corolla lookbook GLB (`part_front_lip` V1, `_v2`, `_2025`) | eps-toyota-gr-corolla-v23.glb, downloaded | **found** |
| Integra DE5 lookbook GLB (`part_duckbill`, `part_sport_wing`) | eps-acura-integra-type-s-de5-v19.glb, downloaded | **found**; that `part_duckbill` is the trunk lip is to be confirmed |
| WRX VB lookbook GLB | eps-subaru-wrx-vb-v12.glb, downloaded | found, but **it has no front lip part** |
| VB lip CAD | `WRX VB NBR Front Lip Uncut.stl` 1FcMcvYcdXTIcdtiHf9ogIKp8fZKvcx7H | found; that it is the sold product is to be confirmed |
| FG2 lip CAD + LQ scan | 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd / 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH | **found** (used in fg2-race-car) |
| GR Corolla / Integra Type S / VB full-car scans | knowledge/car-inventory.md paths | **found** (listed; not downloaded yet) |
| GR Corolla V1 lip CAD (Drive `Corolla V1 & V2 Lip Kit` 1-wEi9unNtRyXDMQlOsgNZWAE0IIhW685) | Drive | found, as a fallback for the GLB part |
| Pip & Gus (design, rig, Higgsfield refs, voices: Pip = Kiki, Gus = Harrison) | branch `claude/pip-gus-ep9-aesub`: `projects/scan-tedium-explainer-reel/`, `projects/pip-gus-series/SESSION_BRIEF.md` | **found**. They are **Illumaesthetic** mascots (Illumaesthetic name badges); **no Epsilon-specific characters were found** |
| Warehouse footage | Dropbox search ("warehouse", "pallet", "inventory", "shelf"): no warehouse video. Only `Jackie/Graphics/Fulfillment and production warehouse.png` (a graphic) and the `*Unsorted Video Dump/China/` folder (about 30 iPhone clips + photos from Apr 2026; the search tags one photo as a warehouse; **not reviewed**, because the previews are blocked by the proxy) | **missing / to-request** |
| Warehouse CGI environment | to be built (`tools/warehouse_env.py`, following mr2 `city_env.py`: racking, pallets, film wrap, lights, boxes) | to build |
| Epsilon+ wordmark | Drive `EPSILON+ Logos` | found (in the lessons); file to fetch |
| BF prices, BF dates | owner | **to-request** |
| Music | owner / commercial library | **to-request** |

## Open questions for the owner
1. **BF prices:** what is the Black Friday price for each lip? The store has no BF discount yet. The FG2 ($285 -> $150)
   and Integra gloss-black trunk lip ($200 -> $100) are already marked down on the store, and the GR Corolla V1 (PU $215
   / CF $600) is not. Is the V1 lip actually going to clearance, or just on sale?
2. **"Only X left":** the only real low count is **14 carbon GR Corolla V1 lips**. Is `ONLY 14 LEFT IN CARBON` OK, with
   no counts on the others (64 / 69 in stock; the Integra and VB lips are backordered)? Shall I use `IN STOCK` /
   `BACKORDER` instead of counts there?
3. **VB lip:** it is already [CLEARANCE] at $99.99 but backordered (-15), and the store has no "was" price, so there is
   nothing true to flip from. Keep it with a `CLEARANCE` tag (no strike-through), give me its old price, or drop it?
   Also confirm `WRX VB NBR Front Lip Uncut.stl` is the product sold.
4. **Integra trunk lip** is backordered (-18). Is a clearance ad for a backordered part OK? Which variant goes on the
   tag: gloss black $100, or paint-matched $300? Does the lookbook's `part_duckbill` match the trunk lip?
5. **Warehouse:** no warehouse footage exists in Dropbox. Is a CGI warehouse OK (my recommendation)? Or can you film a
   10-s pass down your real racks? If you film it, price tags over real footage break the no-text-over-IRL rule: do you
   explicitly want tags over real footage for this ad? (The CGI plan avoids the conflict.) Is the `China/` Apr 2026
   folder a factory/warehouse visit I may use?
6. **Characters in an Epsilon+ ad:** Pip & Gus wear Illumaesthetic badges. Use them here with Epsilon+ badges, keep
   the Illumaesthetic badges, or leave them out? Should they speak (one line, for example Pip: "Everything must go!"),
   or stay silent with only the music?
7. **Music:** which track (cleared for ads)?
8. Is the end CTA `EPSILON.PLUS` + BF dates, and what are the dates?

## Production steps (after approval)
1. `ive log` the approved answers. Re-read the Shopify prices, compare-at prices and inventory, and save the snapshot
   to `projects/bf-clearance-shelf-drop/store_snapshot.json` (the tag textures are built only from it).
2. Music: `ive beats`, with the kick-peak anchored grid. Re-snap the shot table.
3. Build the warehouse env + forklift in Blender EEVEE cel-shaded from the pilot's `partA_scene.py`. Import the lip
   parts from the GLBs/CAD with lookbook materials. Make the tag cards (front/back textures from the snapshot) and the
   flip animation.
4. Render the shelf shots (2, 4, 6, 8) and save each lip's camera. Render the matching 1:1 scan/CGI shots (3, 5, 7, 9)
   from the same camera, with each lip placed from its design frame, the stock lip zone cut, and a clip check.
   Renders are in the background, one at a time; decimate the scans out-of-core first.
5. Remotion: the shot 9 count text and the end card (Epsilon+ wordmark, 720 px).
6. `ive assemble` 9:16 at 30 fps; mix to -14 LUFS / TP < -1 dBFS; verify the cut times against the kicks.
7. Look at a contact sheet and the frames around every cut. Self-score with `training/rubric.md` into `review.md`.
8. On the posting day, re-check the stock counts. If the carbon count has changed, re-render the shot 9 text (Remotion
   only).
