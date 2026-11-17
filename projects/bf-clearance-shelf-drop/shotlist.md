# BF video 5 of 8: "Clearance Shelf Drop" (shot list v5, awaiting final approval)

**v5 (2026-11-17): NO Del & Eps.** The owner, relayed by the parent: "tell all the black friday agents to not use
del & eps, just typical branding content" (`projects/_blackfriday/MASCOT_AND_PRICES.md` e05c325).
- Every character shot, cameo and sting is removed, and no Higgsfield credits are spent.
- Their moments are filled with branding: an Epsilon+ wordmark lightbox in the aisle, the scan-line sweep on each lip,
  the car shots and the end card.
- The character sections below are kept only as history and are void.

Status: plan only. Nothing is rendered until the owner approves this version in chat.
Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`.

## Owner answers applied in v4 (chat, 2026-11-17)
- "Only focus on the most popular lips": the video features the 2 best sellers of the concept's four lips, by "Sold
  Last 12 Mo" in the BF Liquidation Pricing sheet:
  - GR Corolla V1 lip: **31** sold;
  - Integra rear trunk lip: **16** sold;
  - dropped: WRX VB lip (14) and FG2 lip (12).
- "Use the price from what the bf liquidation chat says": every price comes from the "Black Friday 2026 Liquidation
  Pricing" sheet (https://claude.ai/artifact/BSCEWTDHHKuC9Yop5xh2X6, tab `Pricing`, column "BF 2026 Price", rev 25).
- "For backordered don't show stock line": the Integra trunk lip (ABS -18, carbon -2) gets no stock line.
- Integra car: **DE4** (`eps-acura-integra-de-v29.glb`).
- Music: my choice. It is "LUXURY" by Baby thug, claimed in `projects/_blackfriday/MUSIC.md`.
- A CGI warehouse is approved.
- ~~Del & Eps~~: removed in v5 (owner: no characters).
- Defaults where the owner didn't answer:
  - the lips are silver like the scans (the locked "characters are the only colour" rule);
  - music only, with no voice line;
  - the 10 mm sting is kept as an optional end beat.

## Concept in one line
A forklift POV rolls through a dark silver Epsilon+ warehouse. A cyan scan line sweeps each pallet, and the
price tag flips to the BF clearance price. Each lip hard-cuts 1:1 onto its car, and the video ends on "ONLY
14 LEFT IN CARBON" and the Epsilon+ wordmark.

Owner's concept, verbatim: "Clearance shelf drop. The warehouse POV. A pallet of GR Corolla V1 lips, Integra trunk lips
and FG2/VB lips with price tags flipping from full price to clearance as each one comes into frame. Use real low counts
like "only X left" to push urgency." (Narrowed to the two most popular lips at the owner's request.)

## Target length and format
- About 14 s, or 15.5 s with the sting.
- 9:16, 1080x1920, 30 fps.
- The first tag flip lands at 2.0 s.

## Prices and stock on screen
| Part | Variant | Was (sheet "Current Price" = live store) | BF (sheet) | Live stock 2026-11-17 | Stock line |
|---|---|---|---|---|---|
| Rear Trunk Lip - Integra DE4/DE5 (`epsilon-rear-trunk-lip-acura-integra-de4-de5-2023`) | ABS Gloss Black | $100 | **$40** (60 %) | -18 (backorder) | none (owner) |
| same | Carbon Fiber / Unpainted | $240 | **$96** (60 %) | -2 (backorder) | none (owner) |
| Front Lip - GR Corolla Zenki V1 (`pre-order-epsilon-front-lip-toyota-gr-corolla-e210-2023`) | Polyurethane | $215 | **$129** (40 %) | 69 | none (healthy count) |
| same | Carbon Fiber | $600 | **$330** (45 %) | **14** | **ONLY 14 LEFT IN CARBON** |

- The "was" price is the price customers pay today, not the old $200 compare-at.
- I said in v2/v3 that the store had no carbon trunk-lip variant. That was wrong: my first query only read 10
  variants, and the store does list "Carbon Fiber / Unpainted" at $240.
- The sale isn't live and has no dates yet, so no dates go on screen.
- Checked against `projects/_blackfriday/PRICES.md` + `bf_liquidation_pricing.csv` (commit 7ec3adf, the owner's source
  of truth). All four figures match.
- PRICES.md says: no stock counts on screen unless the owner asks. This video's concept is the owner's own ask ("Use
  real low counts like 'only X left'"), and in chat the owner limited it only for backordered parts. So the carbon GR V1
  line stays, as the one real positive count. If the owner says no, shot 5 runs with no text, and that is a
  Remotion-only change.
- The carbon count is re-read on the render day and on posting day.

## Music
"LUXURY" by Baby thug (TikTok Commercial Music Library, cleared for ads, song_clip_id 7496578190397114385, 107 s).
- Claimed in `projects/_blackfriday/MUSIC.md`. Backup: "Diamonds on me" by Capivara Dj (7634619894408087553).
- Times below assume 120 BPM and are re-snapped to `ive beats` (kick-anchored).
- Mix to -14 LUFS with true peak below -1 dBFS, starting at the song's start or 2 kicks before its drop.

## Characters
None: the owner removed Del & Eps from the BF videos. (The earlier section is superseded.)

## Shot table
| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.0 | 2.0 | 1-4 | Forklift POV, 1.6 m, 24 mm, forks in the bottom of frame, slow push | Dark silver warehouse aisle (racking, lamps, boxes), an empty pallet, a BLACK FRIDAY sign and an Epsilon+ wordmark lightbox | Warehouse built in `tools/shots_v0.py`; wordmark Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | A light bank snaps on with each snare; the wordmark lights on the 3rd | `BLACK FRIDAY` sign + Epsilon+ wordmark (in-world) | cut on beat 4 | Blender |
| 2 | 2.0-4.0 | 2.0 | 4-8 | POV; a pallet slides in and stops centre-frame | Integra rear trunk lip on a pallet, with a 2-line tag | `part_duckbill` (= trunk lip) in `eps-acura-integra-de-v29.glb` (sha256 4bc2e068a4c9...), silver | A cyan scan line sweeps across it; **the tag flips on the snare** | `INTEGRA TRUNK LIP` / ABS ~~$100~~ **$40** / CARBON ~~$240~~ **$96** (sheet; no stock line) | **hard 1:1 cut** on beat 8 | Cycles + composite; the tag is a 3D card from `store_snapshot.json` |
| 3 | 4.0-5.5 | 1.5 | 8-11 | Same lip framing, rear 3/4, 10 deg orbit | DE4 Integra with the trunk lip fitted (stock duckbill hidden), silver | `eps-acura-integra-de-v29.glb` (whole car, silver look; `body_duckbill_stock` hidden) | Orbit, revealing the car | none | cut on beat 11 | Cycles |
| 4 | 5.5-8.0 | 2.5 | 11-16 | POV brakes; tilt up to a spotlit top-shelf bay | GR Corolla V1 lips: a PU pallet and a short carbon stack | `part_front_lip` (V1 / Zenki; not `_v2` or `_2025`) in `eps-toyota-gr-corolla-v23.glb` (sha256 ee3643bea3d4...), silver | Forks dip; **both tags flip on the snare** | `GR COROLLA V1 LIP` / PU ~~$215~~ **$129** / CARBON ~~$600~~ **$330** (sheet) | hard 1:1 cut on beat 16 | Cycles + composite |
| 5 | 8.0-10.5 | 2.5 | 16-21 | Same lip framing, then a pull back | GR Corolla with the V1 lip, silver (scan in v1; the lookbook GLB car in the v0 drafts) | `Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` (836 MB) + the V1 lip in the GLB/CAD frame (stock lip zone cut, the kit_nest2 rule) | Pull back to the whole car | **`ONLY 14 LEFT IN CARBON`** (Shopify carbon `inventoryQuantity`, re-read on the render and posting days), on black beside the car | cut on beat 21 | Cycles + composite + Remotion text |
| 7 | 12.0-14.0 | 2.0 | 24-28 | Static | Epsilon+ wordmark (about 720 px wide) | Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | Wordmark in on beat 24 | `BLACK FRIDAY CLEARANCE` / `WWW.EPSILON.PLUS` | end | Remotion |

Rules this plan keeps:
- There is no IRL footage, so no text goes over IRL. The tags are in-world CGI props.
- Every transformation is a hard cut on a beat, and no shot is reused.
- The only prices are from the owner's sheet, and the only count is the live positive one. Backordered parts have no
  stock line.
- Scans stay as captured, and the characters are the only colour.
- The end card is the Epsilon+ wordmark.

## Asset inventory
| Asset | Path / ID | Status |
|---|---|---|
| Integra DE4 lookbook GLB (`part_duckbill` = trunk lip, `body_duckbill_stock`) | eps-acura-integra-de-v29.glb, in `/home/user/media/bf-clearance-shelf-drop/glb/` | **found** |
| GR Corolla lookbook GLB (`part_front_lip` V1) | eps-toyota-gr-corolla-v23.glb, downloaded | **found** |
| GR Corolla full-car scan | `Engineering Design/Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` | **found** (to download) |
| GR Corolla V1 lip CAD fallback | Drive `Corolla V1 & V2 Lip Kit` 1-wEi9unNtRyXDMQlOsgNZWAE0IIhW685 | found |
| Epsilon+ wordmark | 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | **found** |
| BF prices | Liquidation Pricing sheet BSCEWTDHHKuC9Yop5xh2X6, `Pricing` rows 22, 23, 45, 46 | **found** |
| Music | "LUXURY" by Baby thug (TikTok CML) | claimed |
| Warehouse env | `tools/warehouse_env.py` (to build, following mr2 `city_env.py`) | to build |

## Production steps (after approval)
1. Snapshot the sheet prices and the live Shopify stock to `projects/bf-clearance-shelf-drop/store_snapshot.json`;
   the tags and the count text are built only from it.
2. Download the track and run `ive beats`; re-snap the table.
3. Build the warehouse env + forklift + tags. Place the lips in silver from the GLBs.
4. Render shots 2 and 4, keeping their cameras. Render shots 3 and 5 from the same cameras:
   - shot 3: the DE4 car with the stock duckbill hidden;
   - shot 5: the GR scan with the V1 lip, stock zone cut, and a clip check.
   Renders go in the background, one at a time.
5. (removed: no characters)
6. Remotion count text + end card. `ive assemble`; mix to -14 LUFS; verify the cuts against the kicks; contact sheet
   and review.
7. On posting day, re-read the carbon count; if it has changed, re-render only the Remotion text.
