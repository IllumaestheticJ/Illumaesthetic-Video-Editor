# BF 6/8 - "gr-corolla-track" - shot list (PLAN, awaiting user approval)

Planned 2026-11-17. Nothing is rendered until the user approves this plan in chat.

## Concept (one line)
A V2-kitted GR Corolla at speed on a circuit, then a quick low close-up of the V2 lip at speed. A hard 1:1 cut takes the car to its silver scan with the Epsilon V2 kit. The two offers go on black cards between shots: "V2 KIT 30% OFF" and "V1 UP TO 45% OFF". The ad ends on the Epsilon+ wordmark.

**Owner's concept (verbatim):** "GR Corolla on track. Track or autocross footage of a GR Corolla with the V2 lip, skirts and spats, with a quick close-up of the lip at speed. Captions: 'V2 kit 30% off, V1 up to 45% off.'"

## The footage problem (decide first)
There is **no real track or autocross footage of a V2-kitted GR Corolla** in Dropbox. I searched by folder and by name, and sampled frames from 10 clips.
- The track-day sessions I could identify show other cars:
  - 2025-07-23: a 240SX-type car;
  - 2025-10-24 and 2025-11-07: the yellow race car;
  - 2026-06-13: a Miata, an RX-8 and an SLK.
- Not sampled: 2026-05-16/17, 2026-09-11 and 2026-09-18..20.
- `1. Epsilon Plus Videos/1. Video dumps/ARA Rally GR Corolla/` is a scan session: the clip I sampled shows a scanner coming out of its case. It is not rally driving.
- The only moving footage of the V2 car is `/1. Epsilon Plus Videos/3. Short form/Posted/GR COROLLA ROLLERS.mov` (id:2nzlLXSF_sUAAAAAAAAGaA, 19.4 s, 2160x3840).
  - It is an already-posted finished edit of the white Castrol #24 car rolling on industrial streets, not on track. It includes a low lip close-up roller at about 10-11 s.
  - Some of its blurred shots may be CGI composites, and it already has an EPSILON+ end card.
  - I could not find its raw clips.

**Recommended plan (below): the track is CGI.** The lookbook GLB car (V2 kit) drives a Blender circuit, and the scan and the cards carry the rest. If the user supplies real track or autocross clips, shots 1, 2, 4 and 7 become footage edits and nothing else changes. See open question 1.

## Target length and format
- About 18 s (9 bars at ~120 BPM; the final grid comes from the chosen track).
- 9:16, 1080x1920, 30 fps.
- Music at -14 LUFS, true peak below -1 dBFS.

## Music candidates
Real tracks from the TikTok Commercial Music Library (licensed for brand posts), pulled 2026-11-17 from the Higgsfield `tiktok_music_trending` chart (US, 7 days).
- I checked these against every `projects/*/project*.yaml`: none has been used.
- Each starts from the song's beginning. Before cutting, I'll fit the BPM and grid to kick peaks (see lessons on `ive beats` half-time errors).

| # | Track | song_clip_id | Why |
|---|---|---|---|
| 1 | "Electric Youth" - Chris_record (EDM #1) | 7421090393491785729 | Driving EDM, a race-day feel |
| 2 | "Invincible" - Deaf Kev | 6761071663921498114 | Classic build and drop; the 1:1 cut goes on the drop |
| 3 | "Prisoner" - DIDKER (hip-hop #1) | 7361125304804542465 | Hard hits, short-form energy |
| 4 | "140" - Lil Texas | 7597234501887166481 | Very fast hardcore; only if the user wants it aggressive |

The other 7 Black Friday sessions may pick from the same chart. The parent should assign tracks so no two ads share one.

## Shot table
- Times assume a placeholder 120 BPM grid (1 beat = 0.5 s, 1 bar = 2 s) and will be re-fitted to the chosen track.
- Every cut lands on a measured hit. The IRL/CGI -> scan transformation is a hard 1:1 cut on the drop, never a dissolve.

**Source key:**
- **GLB** = `eps-toyota-gr-corolla-v23.glb` (cdn.shopify.com/s/files/1/0036/2250/2435/files/eps-toyota-gr-corolla-v23.glb, downloaded and checked: 5,192,780 bytes). It is also in Drive `Website Files/Epsilon-final-GLBs-2026-10-15.zip` (12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7).
  - V2 kit nodes: `part_front_lip_v2`, `part_side_skirts_v2`, `part_rear_spats_v2`.
  - V1 nodes: `part_front_lip`, `part_side_skirts`, `part_rear_spats`.
  - Not used: `part_canards`, `part_wing_strakes`, `part_wrc_wing`, `part_front_lip_2025`.
- **SCAN** = Drive `Toyota Corolla Hatchback (E210)/GR Corolla/GR Corolla Full Car.stl` (folder 16SiY5GVJJHCmoJxwSKIOx-82zJmqHayw), prepped as in projects/toyota-gr-corolla (car9: FARO stock bumper, wheels filled or mirrored).
- **KIT CAD** = Drive `Epsilon Production/GR Corolla V2/` (`GR Corolla V2 LIP_full with Logos_1.stl` plus the V2 skirts and spats), in engineering's frame.
  - These go into our frame with the v12b `eng_to_ours` transform (0.79 deg, (4, 59, 30) mm), as in toyota-gr-corolla/tools/shots_v14.py.
- **ALIGN** = the scan-to-GLB rigid ICP from projects/gr-corolla-reel (`scan/align.json`), which keeps the CGI car and the scan locked across the 1:1 cut.

| # | Time | Dur | Beat | Camera | Subject | Source | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.0 | 2.0 | bar 1 (pre-drop, on a real hit) | Low tracking car, ~0.4 m high, front 3/4, 35 mm, shutter blur | GR Corolla (V2 kit) exits a corner at speed on a CGI circuit | GLB, V2 parts on and V1 parts hidden; paint per Q4 | The car fills the frame within 1 s (hook); kerbs and the track blur past | none | cut on beat | Blender (Cycles, GLB + circuit env) |
| 2 | 2.0-3.0 | 1.0 | bar 2, beats 1-2 | Same rig, pushing in on the nose | Front end at speed | GLB | Camera closes to the lip line; the frame at the end is the solved match pose | none | **1:1 HARD CUT on the drop** | Blender |
| 3 | 3.0-5.0 | 2.0 | drop (bar 2 b3 - bar 3) | Exactly the shot-2 end camera, continuing the same move | Silver scan of the GR Corolla with the V2 kit CAD seated | SCAN + KIT CAD (ALIGN) | The car keeps its exact size and position across the cut; the camera keeps tracking over black; the kit reads as parts on the real car's data | Optional HUD label "EPSILON AERO V2 KIT" after it settles (product name, no numbers) | cut on beat | Blender (silver look) + Remotion label |
| 4 | 5.0-6.0 | 1.0 | bar 4, beats 1-2 | Macro, 10-15 cm off the tarmac, 24 mm, low under the lip | **Quick close-up of the V2 lip at speed** | GLB (`part_front_lip_v2`) | The lip edge and endplate fill the top half; tarmac streaks below; the car crests a kerb | none | 1:1 hard cut | Blender |
| 5 | 6.0-7.0 | 1.0 | bar 4, beats 3-4 | Same macro camera | V2 lip CAD on the scan, close-up | KIT CAD on SCAN | Same pose as shot 4; logos on the lip CAD read | none | cut on downbeat | Blender |
| 6 | 7.0-9.0 | 2.0 | bar 5 | Front 3/4 high, slow 15 deg orbit | Black card: V2 kit parts (lip, both skirts, both spats) floating in the silver look | GLB V2 kit parts in the silver look | Parts drift into the outline of the (absent) car, nose up, slow orbit | **"BLACK FRIDAY" / "V2 KIT 30% OFF"** (owner's BF doc: GR Corolla V2 PU lip, skirts, spats 30%) | cut on downbeat | Blender plate + text composite |
| 7 | 9.0-11.0 | 2.0 | bar 6 | Side tracking at sill height, 50 mm, a rolling shot | Side skirt and rear spat at speed down the straight | GLB | The skirt leads the frame; the spat passes at the end of the shot | none | cut on downbeat | Blender |
| 8 | 11.0-13.0 | 2.0 | bar 7 | Same framing as shot 6 (mirrors card 1) | Black card: V1 lip, skirts and spats | GLB V1 nodes (`part_front_lip`, `part_side_skirts`, `part_rear_spats`) in the silver look | Same move as shot 6 | **"V1 UP TO 45% OFF"** (owner's BF doc: V1 40-45 %, carbon V1 lip 45 %) | cut on downbeat | Blender plate + text composite |
| 9 | 13.0-15.0 | 2.0 | bar 8 | Low rear 3/4, static; the car passes the lens | GR Corolla blasting past, then away into the braking zone | GLB | The rear spats read as it passes; it leaves the frame on the last beat | none | dip to black on downbeat 9 | Blender |
| 10 | 15.0-18.0 | 3.0 | downbeat 9 | Static | Epsilon+ wordmark card, ~720 px wide, plus "EPSILON.PLUS" | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | Logo on the downbeat, held, music fade | "EPSILON.PLUS" (store URL; optional per Q6) | end | Remotion / ffmpeg |

**Characters: NONE (owner, 2026-11-17: "tell all the black friday agents to not use del & eps, just typical branding content").** No Del & Eps, Pip & Gus, cameos or 10 mm sting. The offer cards carry only the kit parts (silver), the offer text and the Epsilon+ wordmark at the end.

## What the text rules mean here
- No text appears over any real or CGI driving shot. Both offers sit on black scan cards (shots 6 and 8), which is the brief's alternative.
- **Prices: the owner's decision.** Use the BF liquidation spreadsheet even where its stock figures are wrong ("Black Friday 2026 Liquidation Pricing", Pricing tab; snapshot `projects/_blackfriday/bf_liquidation_pricing.csv` at commit 7ec3adf; how to re-read it live is in `projects/_blackfriday/PRICES.md`). It supersedes the TL;DR tier table and the store stock checks above.
  - The crossed-out price is the sheet's "Current Price"; the sale price is "BF 2026 Price".
  - Every item the sheet prices is on sale; only the 0% / "No deal" items are not.
  - No stock counts on screen. No sale dates on screen (the window isn't set).
- **On-screen text:** the owner's caption only, "V2 KIT 30% OFF" and "V1 UP TO 45% OFF". The sheet confirms both:

| Product (sheet name) | Current Price | BF % | BF 2026 Price |
|---|---|---|---|
| Front Lip V2 - GR Corolla Zenki · PU | $285.00 | 30% | $199.50 |
| Side Skirts V2 - GR Corolla · PU | $400.00 | 30% | $280.00 |
| Rear Spats V2 - GR Corolla · PU | $175.00 | 30% | $122.50 |
| Front Lip - GR Corolla Zenki V1 · PU | $215.00 | 40% | $129.00 |
| Front Lip - GR Corolla Zenki V1 · Carbon | $600.00 | 45% | $330.00 |
| Side Skirts - GR Corolla V1 · PU | $275.00 | 40% | $165.00 |
| Rear Spats - GR Corolla V1 · PU | $125.00 | 40% | $75.00 |

- **Optional (Q5):** a small was/now line under each card ("LIP $285 → $199.50" etc.). The figures come only from the sheet's columns. Price text goes on the black cards only.

## Asset inventory
| Asset | Status | Where |
|---|---|---|
| Lookbook GLB with V1 + V2 kit | **found** (verified node names) | CDN eps-toyota-gr-corolla-v23.glb; Drive zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7 |
| GR Corolla full-car scan + registered V2 kit, canards, wing | **found** | Drive folder 16SiY5GVJJHCmoJxwSKIOx-82zJmqHayw; Epsilon Production/GR Corolla V2/; pipeline in projects/toyota-gr-corolla (v12b) |
| Scan-to-GLB alignment | **found** (repo method; media must be rebuilt in this container) | projects/gr-corolla-reel (`scan/align.json`, tools/align_game.py precedent) |
| CGI circuit environment | **to build** | New Blender env: tarmac, kerbs, run-off, armco/tyre walls, gantry, grandstand. Precedent: projects/toyota-mr2-spyder/tools/city_env.py (lesson: low-detail envs get rejected) |
| Real track/autocross footage of a V2 GR Corolla | **missing / to request** | None in Dropbox; 4 track-day folders not yet sampled (2026-05-16/17, 2026-09-11, 2026-09-18..20) |
| Moving V2-car footage (street) | found, finished edit only | `/1. Epsilon Plus Videos/3. Short form/Posted/GR COROLLA ROLLERS.mov` (raws not found) |
| V2 kit photos (finish reference for paint and lip) | found | `/1. Epsilon Plus Videos/4. Photoshoots/Corolla GR V2 Kit/` (23 JPG + comparison PNGs); `/3. Epsilon Motorsports/Photoshoot/COROLLA/` |
| Epsilon+ wordmark | found | Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Characters | **not used (owner)** | - |
| Music | **claimed: "Electric Youth" (Chris_record)** in projects/_blackfriday/MUSIC.md | TikTok CML song_clip_id 7421090393491785729, not yet downloaded |

## Open questions for the user
1. **Footage.** There is no real track or autocross clip of the V2 car. Which do you want?
   - **(a) CGI track** (recommended, this plan);
   - **(b)** you send real track or autocross clips;
   - **(c)** cut from the posted "GR COROLLA ROLLERS" street edit. It's street, not track, it's already posted, and some shots look CGI.
2. **CGI paint.** Do you want the white Castrol/Motegi #24 livery of the real V2 car (GLB `livery_castrol`; puts Castrol branding in the ad), or a plain paint such as Supersonic Red?
4. **Captions.** OK on cards between shots (current plan), or do you explicitly want them over the driving shots?
5. **End card and prices.** Wordmark alone, or with "EPSILON.PLUS" / "BLACK FRIDAY" under it? Do you also want the sheet's was/now prices under each offer card, or the percentages only?
6. **Music.** I claimed "Electric Youth" (Chris_record, TikTok CML). Keep it, or swap to "Invincible" (Deaf Kev) / "Prisoner" (DIDKER) / your own track?

Resolved: the discount scope ("V2 kit 30% off, V1 up to 45% off") is confirmed by the owner's BF liquidation sheet; prices come from the sheet, not from store stock.

## Production steps (after approval)
1. Rebuild the media in `/home/user/media/bf-gr-corolla-track/`:
   - fetch the scan, the V2 kit CAD and the GLB;
   - re-run the toyota-gr-corolla prep (car9 + `eng_to_ours`) and the gr-corolla-reel scan-to-GLB ICP;
   - check every kit part in red over the silver car at its mounting edge.
2. Build the circuit environment and look at stills before any animation.
3. Download the chosen track, fit the kick grid, set `music.start` = 0 (song beginning), and lock the shot durations to whole frames (first clip one frame short).
4. Render one at a time, in the background, with persistent data off for animated shots. Scan every frame's luma for black frames.
5. Solve the shot-2 and shot-4 end poses, then render the scan shots from the same cameras. Verify each 1:1 cut with an onion overlay.
6. Make the Remotion cards and label, plus the end card. Read the final frame of every text.
7. Assemble with plain concat at the cut frames. Measure the cuts against the decoded audio, and loudness to -14 LUFS / < -1 dBTP.
8. Self-review (training/rubric.md), deliver, record feedback, archive, commit and push.

## v0.2 changes (user, 2026-11-17)
User's notes on v0.1: "include that the carbon canards are back in stock", "highlight the v2 parts", "use the video game GLBs instead of the scan data".

| # | Kicks | Shot | Change |
|---|---|---|---|
| 1-2 | 0-6 | CGI hook + push | Carbon canards (GLB `part_canards`, carbon material) now on the car in every CGI shot |
| 3 | 6-10 | **GLB studio highlight** (was scan) | 1:1 hard cut from the track to a black studio: the body drops to graphite and the V2 lip, skirts and spats light up (bright satin + emission ramp). Label "EPSILON+ / V2 AERO KIT" |
| 4 | 10-12 | CGI lip macro | unchanged |
| 5 | 12-14 | **GLB lip highlight** (was scan) | Same macro camera, lip highlighted. Label "V2 / FRONT LIP" |
| 6 | 14-18 | Card V2 30% OFF | unchanged |
| 7 | 18-22 | CGI side tracking | Labels "V2 / SIDE SKIRTS", then "V2 / REAR SPATS" |
| 8 | 22-26 | Card V1 up to 45% OFF | unchanged |
| 9 | 26-30 | **New: canard close-up** | Front-left corner in the black studio; the carbon weave glows in. Label "CARBON CANARDS / BACK IN STOCK" (no price: canards are not in the BF sheet) |
| 10 | 30-34 | CGI drive-past | unchanged |
| 11 | 34-40 + 1 s | Epsilon+ wordmark + EPSILON.PLUS | moved 4 kicks later; total about 20.2 s |

- Labels sit on CGI and black studio shots only. There is no real footage in this ad.
- **Stock check (live store, 2026-11-17):** "[BACKORDER] Canards / Dive Planes - Toyota GR Corolla (Zenki, E210, 2023-2024)", SKU EP-GRC-CND-CF, $320, inventory -2.
  - The store does not yet say "back in stock". The on-screen claim comes from the user.
  - Update the listing title and inventory before this ad runs.
- No scan data is used in v0.2.
