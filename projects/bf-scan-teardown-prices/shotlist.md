# BF 8/8: "scan-teardown-prices" shot list (DRAFT, waiting for the owner's approval)

Planned 2026-11-17. Nothing is rendered until the owner approves this plan in chat.

**Owner concept (verbatim):** "Scan teardown reel. If you have a 3D scan of the Integra or the Civic, a silver-on-black scan
reel where the kit parts come off, float apart with their prices and fly back on. This fits the scan-reel style you've used before."

**One line:** a silver FE1 Civic Si scan on black wears the full Epsilon kit. On the beat each kit part comes off in turn: lip,
skirts, rear lip, then wing. Each one floats clear under its price tag. The whole kit hangs exploded around the stock car, flies
home and locks on a downbeat. A hard 1:1 cut goes to Ron's finished render, and the reel ends on the Epsilon+ wordmark with the
Black Friday line.

**Format:** 9:16, 1080x1920, 30 fps, **about 19 s** (9.5 bars). Format is Temerario-style, so it follows
`.claude/skills/temerario-scan-reel/`: scan only, no shop footage, silver on black, real music from the song's start, and every
cut on a measured hit.

---

## 1. Which car: the Civic FE1 (recommended), not the Integra

| | Civic 11 FE1 Si facelift | Integra DE5 Type S | Integra DE4 A-Spec |
|---|---|---|---|
| Full-car scan | `civic Facelift FE1 Full Car.stl` (1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ), already prepped in honda-civic-11 | `Integra Type S Full Car.stl` (1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5, 1.24 GB) + `..._scaled to match with typeS rescan.stl` (110D0FSdHdCh63FepsRQEqnWItygsUr5G) + `TypeS Rescan typeS rescan.stl` (10eR0dVkan3A_2iPDbvO1AzjFXvjK_77I); hood-vent part/state scans | **Found today, not in car-inventory.md:** `Integra ASpec.stl` (1bx1Rrjxnz8jI6mIDFBL_y44dmcYHVufx, 914 MB) = `Integra A_spec_scan_full_relocated.stl` (123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV, same size). Also ASpec Rear / Trunk Open / Side Skirt / Diffuser scans |
| Kit that fits it (store) | Kouki front lip, FE/FL side skirts, FE rear lip, FE Sport Wing | **Only the Sport Wing and the Rear Trunk Lip.** Front Lip, Side Skirts, Rear Spats and the fender flares are listed **DE4 only** | Front Lip, Side Skirts, Rear Spats, Rear Trunk Lip, Sport Wing (all fit) |
| Kit design files on our scan | Ron's production STLs, registered at **1.4 mm** median (honda-civic-11 v5, approved) | none registered | not registered. Candidates on Drive, unopened: `Integra A spec1.blend` (13OVeLVoJrrZvXYY7u1LBoaHN9LJh8gdM, 2.6 GB), `Integra A spec For animation.blend1` (1msh6TKOHqbTzRW6IyH3_2mHlekrJgp7R); lookbook `eps-acura-integra-de-v29` |
| Cost to get to a first frame | low: re-download and re-run v5's tools | n/a for a kit teardown | high: new prep, registration and a kit-placement check |

The FE1 is the only car where every kit part can be placed accurately *today*. The Type S scan can't carry the DE4 lip, skirts and
spats; they would be placed on bumpers they don't fit. An A-Spec version is possible later, but only after the design files are
found and registered. (Open question 1.)

**Overlap:** BF 1/8 `bf-civic-parts-rain` uses the same FE1 scan and kit. The two concepts differ (raining parts vs. a teardown),
so that's fine, but the two reels should not share a camera angle or the same Ron render. This plan ends on **render 7**
(rear-left 3/4). (Open question 9.)

---

## 2. Kit parts, prices and stock (live store, checked 2026-11-17, USD)

Store "Epsilon+ Aerodynamics" (epsilon.plus). **Every price on screen gets its BF price from you before it is rendered.**

| Part (on screen) | Listing (handle) | Variant shown | List price | Stock | Design file (Ron) on our scan |
|---|---|---|---|---|---|
| FRONT LIP | Front Lip – Honda Civic Sedan/Hatchback (KOUKI, FE/FL, 2025+) (`front-lip-honda-civic-sedan-hatchback-kouki-fe-fl-2024`) | Unpainted / Polyurethane, SKU EP-CVC11FL-FL-PU | **$285** (painted $485) | -6 (backordered) | `EP-HC11KK-FLV1-PU.stl` (1JXqMKjxm_9vHX3nDcxUPjDnarMpSE8LI). KK = kouki, which matches the facelift scan |
| SIDE SKIRTS | Side Skirts – Honda Civic Sedan/Hatchback (FE/FL, 2022+) (`side-skirts-honda-civic-sedan-fe-2022`) | Unpainted / Polyurethane, SKU EP-CVC11-SS-PU | **$400** (painted $800) | -9 (backordered) | `Side Skirt LH – EP-HC11-SSV1-PU-LH.stl` (1hsIKloafHdmqjKf40Qy7hqg17gWlpMVM), `... RH` (1YFnrIOQsMQuHiLwquamkHJ6pyr3ydX68) |
| REAR LIP | Rear Lip – Honda Civic Sedan (FE, 2022+) (`rear-lip-honda-civic-sedan-hatchback-fe-fl-2022`) | Unpainted / Polyurethane, SKU EP-FE11-RL-PU | **$285** (painted $485) | -10 (backordered) | `EP-HC11SD-RLV1-PU.stl` (1yMCICyK4xGrTQzSvaHkzj_JbjAN_T0Y6) |
| SPORT WING | Sport Wing – Honda Civic Sedan (FE 2022+) (`pre-production-prototype-sport-wing-honda-civic-sedan-fe2-2022`) | Si Factory Duckbill / Generic Gloss Black (the FE1 Si has the factory duckbill) | **$450** (painted $900) | -26 (backordered) | `wing.002` in `Honda Civic Sedan 2022-render.blend` (1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ). Confirm it's this wing (Open question 4) |

Notes for the price cards:
- **All four parts are backordered.** There is no low-stock number to show, and none will be shown. (Open question 6.)
- **Strike-through price = the list price above, not Shopify's compare-at.** Compare-at is empty on the unpainted variants, and
  inconsistent on the painted ones (FE wing Si Duckbill painted: $900 price vs $650 compare-at; FL2 painted wings $850 vs $650).
- There is no "full kit" listing, so no kit total goes on screen unless you give one (a sum of four listings is not a store price).
- The scan's Ron wheels (gold, v5) are not a store product. They get no price and no label. (Open question 5.)

---

## 3. Music candidates

The track must be real (never generated), start from its beginning, and not be used by any reel (checked against
`projects/*/project.yaml` and the editlogs on all branches). Mix at -14 LUFS with true peak below -1 dBFS.

1. **Gran Turismo 2 – Arcade Mode Theme**: Dropbox `/Moosic/YTDown.com_YouTube_Media_LqdZ9inIAR4_Gran-Turismo-2-Arcade-Mode-Theme_005_128k.m4a`
   (id:ihAynaYnO_4AAAAAAACRvg). Used by no reel on any branch. GT2 tracks have been approved before (East City, Going Up North).
2. **Kim Petras – XXX**: `/Moosic/YTDown.com_YouTube_Media_LYSvEbiV0-Y_Kim-Petras-XXX-Audio_008_128k.m4a` (id:ihAynaYnO_4AAAAAAACmaA).
   Used by no reel. Check the lyrics before using it in an ad.
3. **A commercially cleared track** from the TikTok/IG Commercial Music Library, or a track you upload. This is the right choice if
   the reel runs as a **paid** ad: the /Moosic files are YouTube rips with no ad licence. (Open question 7.)

Excluded because other reels used them: Juiced "Killa" (Sentra SEMA), FILMMAKER (400Z), Sector Shift, Megalomaniac, Alkitran,
Blood Code, "The Streets", Riders, South City, East City, Going Up North, Get Low, Brap, Thunder, the JW medley. The other BF
sessions (bf-clearance-shelf-drop, bf-miata-mr2-night-meet, bf-civic-parts-rain) haven't picked a track yet. **Two BF reels must not
end up on the same song.**

**Timing:** the times below use a **placeholder grid of 120 BPM (1 bar = 2.0 s, B = beat number)**. Keys are kept in bars, so once
the track is chosen it is a single re-snap. The grid comes from `ive beats` plus a kick-peak fit, and each cut and lock goes on a
measured kick (`music-and-timing.md`).

---

## 4. Shot table

The camera lives on the car's **left** side. The FE1 scan's right-rear wheel is only a tyre ring, and the approved v5 lap used
this side. Shots 1-5 are **one continuous Blender take** (T1), and the "cuts" between them are part beats inside that take, as in
the approved v5 `L_build`. There are three real cuts in the reel: 5→6 (a big angle change), 7→8 (a 1:1 cut) and 8→9.

| # | Time (s) | Dur | Beat | Camera | Subject | Source asset (path / ID) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-2.00 | 2.0 | B1-B4 | Front-left 3/4, slightly high, slow push-in; the whole car is in frame and moving from frame 1 | FE1 + full Epsilon kit (black PU parts, Ron's wheels) | Scan 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ, prepped as in honda-civic-11 (`prep/car4.json`, 4 mm); kit `kit/parts2/*.stl` from `tools/kit_parts2.py` (Ron → scan ICP 1.4 mm); scan nested under the kit by the GLB `body_<part>_stock` footprint (sec. 6) | Car glides in. On B3 the whole kit "unlocks": every part lifts about 2 cm and settles (the hook) | "BLACK FRIDAY" small caps, top of frame, B1-B4 (owner's campaign; final wording from you) | continuous (T1) | Blender (Cycles, silver look) |
| 2 | 2.00-4.00 | 2.0 | B5-B8 | T1 continues: drops to bumper height, front-left | Front lip | `EP-HC11KK-FLV1-PU` (1JXqMKjxm_9vHX3nDcxUPjDnarMpSE8LI) | On B5 the lip drops 6 cm, slides forward about 1.0 m into clear black in front of the bumper and parks, fully in frame, with its inner face slightly toward the lens. Stock bumper skin returns a quarter beat after it leaves | "FRONT LIP" + ~~$285~~ **$[BF]** (store listing, sec. 2), high in frame, B6-B8 | continuous | Blender + Remotion tag |
| 3 | 4.00-6.00 | 2.0 | B9-B12 | T1 tracks back along the left side at sill height | Side skirts | `EP-HC11-SSV1-PU-LH/RH` (1hsIKloafHdmqjKf40Qy7hqg17gWlpMVM / 1YFnrIOQsMQuHiLwquamkHJ6pyr3ydX68) | On B9 the left skirt slides straight out 0.7 m and drops 0.2 m. The right skirt mirrors it (hidden behind the car here, seen in shot 6). The lip parks out of frame behind the camera move | "SIDE SKIRTS" + ~~$400~~ **$[BF]**, B10-B12 | continuous | Blender + Remotion |
| 4 | 6.00-8.00 | 2.0 | B13-B16 | T1 swings to the rear-left 3/4, low | Rear lip | `EP-HC11SD-RLV1-PU` (1yMCICyK4xGrTQzSvaHkzj_JbjAN_T0Y6) | On B13 the rear lip drops 5 cm and slides straight back about 0.9 m into clear black, past the exhaust. It doesn't clip the tips (pathcheck) | "REAR LIP" + ~~$285~~ **$[BF]**, B14-B16 | continuous | Blender + Remotion |
| 5 | 8.00-10.00 | 2.0 | B17-B20 | T1 rises to rear-left, above the deck lid | Sport Wing | `wing.002` from `Honda Civic Sedan 2022-render.blend` (1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ) | On B17 the wing lifts straight UP about 0.9 m into the black above the car (it stays visible; Civic lesson: up, not toward the lens). The factory duckbill stays on the lid | "SPORT WING" + ~~$450~~ **$[BF]**, B18-B20 | **hard cut on B21** | Blender + Remotion |
| 6 | 10.00-12.00 | 2.0 | B21-B24 | New angle: high, near-top view rolled about 20°, the whole stock car centred | Exploded kit: all five pieces at once around the stock car (lip ahead, skirts both sides, rear lip behind, wing above) | same parts, parked at their shot 2-5 end poses, re-framed | Slow drift. Nothing new moves; this is the "whole kit" inventory beat. Both skirts can be seen here | "THE FULL EPSILON KIT" (no total unless you give one) | continuous into 7 (same camera key) | Blender + Remotion |
| 7 | 12.00-14.50 | 2.5 | B25-B29 | Starts on shot 6's last key, then descends to **Ron's render-7 camera** (rear-left 3/4; `Camera.006` moved into scan frame + silhouette refine, solved in honda-civic-11 v5) | Kit flies home | same | On B25 all parts fly home on their reverse paths, staggered by a quarter beat (lip, skirts, rear lip, wing), and **lock on the B29 downbeat**, nested with no seams. Hold 0.5 s | none | **hard 1:1 cut on B30** (no dissolve) | Blender |
| 8 | 14.50-16.00 | 1.5 | B30-B32 | Ron's render, static | Finished FE kit car | `Render/Final-Sedan-FL/7FinalSedanFL.jpg` (from honda-civic-11 v5) | Hold (the user disliked a push on the final photo in de5-configurator) | none | cut on B33 | Footage edit (still) |
| 9 | 16.00-19.00 | 3.0 | B33-B38 | Static card | Epsilon+ wordmark on black | `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W), about 720 px wide | Wordmark lands on B33; offer line under it on B34; the audio fades with the card from about 18.5 s | "BLACK FRIDAY" + the offer line exactly as you word it + "EPSILON.PLUS" (site domain). Fjalla One caps / Barlow, site colours #0b0c0b / #619f73 / #f2f3f1 | end | Remotion |
| 9b (option) | +2.0 | 2.0 | +1 bar | Static | Pip & Gus beside the wordmark | `origin/claude/laughing-albattani-bav6u7:projects/scan-tedium-explainer-reel/tools/partA_scene.py` + `characters/design.md` | Pip pops in (^ ^ eyes) and points at the wordmark; Gus nods, neutral and warm (**never sad**). No dialogue, so no voice and no generated music | none | end | Blender EEVEE cel |

Total: 19.0 s (21.0 s with 9b).

**Price-tag rules (Remotion, `ScanHUD` or an `overlay.json` layer):**
- Scan shots only.
- One tag on screen at a time: name + price count as one item, so the style guide's two-item limit holds.
- The tag enters on the beat after its part is clear of the car, and leaves before the next part moves.
- Placed in the top third, at least 80 px inside the frame edges and outside the car silhouette.
- Clear black background (a plate only if a part passes behind it).
- The old price is greyed and struck through; the BF price is in sage #619f73.
- No step numbers and no qualifiers.

---

## 5. Asset inventory

| Asset | Path / ID | Status |
|---|---|---|
| FE1 facelift full-car scan | Drive 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ (folder 10Ci7sUypOlHypCK7lW2bsSPSAsazcH14) | **found**: needs re-download (this container's `/home/user/media` is empty) |
| FE1 pre-facelift scan (hole-fill donor only) | 1pz9b0U7U4Mw47kUjSACcYEhOl9aXENul | found |
| Prep and fix tools (deground, patch_holes, fill_top, kit_parts2, merge30, cutcheck) | `projects/honda-civic-11/tools/` | found (in git) |
| Ron's design scene (his FE1 FL scan + kit, for the 1.4 mm registration) | `Civic 11th gen lip kit review.blend` 19ySWB7EGGFfgjQNo-3tOxTTIoKiv0E3w (2.0 GB) | **found** (the Drive ID wasn't recorded before) |
| Ron's render scene (wing.002, wheels, Camera.006) | `Honda Civic Sedan 2022-render.blend` 1Q8maWoJbcdI4tzcS2qZgp_5_BcTovXyQ (852 MB) | found |
| Production STLs: lip KK, rear SD, skirts LH/RH | 1JXqMKjxm_9vHX3nDcxUPjDnarMpSE8LI, 1yMCICyK4xGrTQzSvaHkzj_JbjAN_T0Y6, 1hsIKloafHdmqjKf40Qy7hqg17gWlpMVM, 1YFnrIOQsMQuHiLwquamkHJ6pyr3ydX68 (folder 1q8GuJJ7KepKaNKf_3_irSn023RIPRL4s) | found |
| Website lookbook GLB `eps-honda-civic-sedan-fe-facelift-v9.glb` | inside `Epsilon-final-GLBs-2026-10-15.zip` (12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7, 203 MB) | found. Used for the `body_<part>_stock` nesting footprints, the parts' real PU / gloss materials, and a second check of Ron's placement. **Not** used for placement: its body fit was 7-8 cm off in v4 |
| Ron's render 7 (end frame) + solved camera | `Render/Final-Sedan-FL/7FinalSedanFL.jpg`; camera solve in honda-civic-11 v5 (`tools/match_render2.py`, `match/ov7.jpg`) | jpg Drive ID **to-request / to look up** (the path is known, the ID isn't) |
| Epsilon+ wordmark | 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W | found |
| Live prices / stock | Shopify, sec. 2 | found; **BF prices to-request** |
| Music | sec. 3 | candidates found; **choice to-request** |
| Pip & Gus | git only (sec. 4, 9b); Illumaesthetic mascots with Illumaesthetic name badges; no Epsilon-specific characters exist | found; **use in an Epsilon ad to-request** |
| Integra DE4 A-Spec scan set (option B) | sec. 1 | found; kit design files **missing** (candidates unopened) |
| Shop footage / photos | not used: the format is scan-only, so no text-over-IRL conflict | n/a |

---

## 6. Accuracy plan: placement and nesting

- **Placement:** exactly v5's chain. Ron's FE1 FL scan is rigid-ICP'd onto ours (`kit/ron_to_scan.json`, median 1.4 mm), and every
  production STL and `wing.002` goes through that same transform (`kit_parts2.py`). Before any animation, close-up stills at each
  part's mounting edge (lip under the bumper, skirt to the sill, rear lip to the bumper, wing feet on the lid), as v5's `checks/fit5*.png`.
- **Nesting by the stock-panel footprint:** the website GLB marks which stock surface each part sits on (`body_<part>_stock`
  / `trim_<part>_stock`). I'll follow the MR2 `kit_nest2.py` method:
  - The GLB is registered to the scan (body ICP), and used only to pick the scan zone.
  - Pass A takes the scan skin inside each stock footprint (±30 mm along the normal, no lateral margin).
  - Pass B takes any scan skin that still covers a kit part, by a 200-direction depth test.
  - The cut pieces show whenever the part is OFF and hide a quarter beat before it lands. When a part is on, nothing of the old
    surface pokes through; when it is off, the stock car is whole, with no holes and no black seams.
  - Check: a red/green fit render per part + `pathcheck.py` / `clipcheck.py` for every flight path (nothing passes through the
    body, the exhaust or another part) + `edge_margins.py` (no parked part touches the frame edge).

---

## 7. Open questions for you

1. **Car:** OK to make this the **Civic FE1** (the only car with the kit registered at 1.4 mm)? The Integra Type S scan can't carry the
   DE4-only lip/skirts/spats. A DE4 A-Spec scan set does exist (new find); an Integra version would first need its kit design files found and registered.
2. **Black Friday prices** for each part: Front Lip ($285), Side Skirts ($400), Rear Lip ($285), Sport Wing ($450 gloss black).
   Is the discount the same % on all four? Should the cards show unpainted prices, or painted ($485 / $800 / $485 / $900)?
3. **Offer wording** for the opening "BLACK FRIDAY" tag and the end card (e.g. "UP TO X% OFF THE FULL KIT"), plus the sale dates if
   you want them. I'll use only the words you give.
4. **Wing:** is Ron's `wing.002` the FE Sport Wing as sold (the "Si Factory Duckbill" variant)? I'll compare it with the GLB `sport_wing` / `duckbill` before rendering.
5. **Wheels:** keep Ron's gold wheels (as approved in v5, and needed for the 1:1 cut to render 7), or the stock scanned wheels with
   no render cut (then the reel ends kit-lock → wordmark)? The wheels are not sold, so they get no price either way.
6. **Stock:** all four parts are backordered on the store. Show nothing about stock (my default), or add a "pre-order" line?
7. **Music:** GT2 Arcade Mode Theme / Kim Petras "XXX" / a TikTok Commercial Music Library track / your own? If this runs as a paid
   ad it needs a cleared track.
8. **Characters:** Pip & Gus are *Illumaesthetic* mascots (Illumaesthetic badges, cel-shaded); no Epsilon characters exist. Leave them out of
   this silver scan reel (my default), add the 2 s end tag (9b), or are the "Epsilon characters" something else?
9. **Kit colour:** real finish (black PU / gloss black wing, rim-lit so it reads on black: my default), or the white of Ron's renders (v4/v5)?
   Note BF 1/8 also uses this car; OK that both exist?

---

## 8. Production steps (after approval)

1. Re-download into `/home/user/media/bf-scan-teardown-prices/`: the FE1 scan + pre-facelift donor, Ron's two .blends, the four
   STLs, the GLB zip, and render 7. Check free disk first: the files total about 6 GB.
2. Rebuild v5's base: decimate, prep with `--like car4.json`, deground/patch/fill (honda-civic-11 tools), then `kit_parts2.py` →
   `kit/parts2/*.stl`. Re-check the ICP median (≈1.4 mm) and render fit stills at each mounting edge. Look at them.
3. Extract `eps-honda-civic-sedan-fe-facelift-v9.glb`, register it to the scan, and run the footprint nesting (a kit_nest2 adaptation).
   Render a seam check per part, on and off.
4. Music: get the chosen file; run `ive beats` + the kick-peak grid; re-snap every key in this table and log it.
5. Run the `scene-director` agent on this plan, then `python -m ive director`. Write `shots.py` (copying
   Revuelto `shots_v4.py`: keys in bars, parked poses) for T1, T2 (shots 6-7) and render 7.
6. Previews at 30 % (`scripts/preview5.sh`); `pathcheck.py` / `clipcheck.py` / `edge_margins.py`; one final-quality still for the
   kit-colour test (open question 9) → send to you if it's a close call.
7. Finals one at a time in the background (75 %, 12 spp; part moves at native 30 fps: v5's merge30 lesson). Then a luma scan of every frame.
8. Price tags + end card in Remotion from `overlay.json` (prices typed from your confirmed list, re-checked against the store that day).
9. Assemble with exact frame counts; `verify_delivery.py` (cuts on decoded audio ±½ frame, -14 LUFS / TP < -1 dBFS).
   Contact sheets at every tag and cut; frame diffs at the cuts.
10. Self-score `review.md`, record feedback, archive, commit, push.
