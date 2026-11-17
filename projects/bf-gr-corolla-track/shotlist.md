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
| 6 | 7.0-9.0 | 2.0 | bar 5 | Front 3/4 high, slow 15 deg orbit | Black card: V2 kit parts (lip, both skirts, both spats) floating in the silver look | KIT CAD | Parts settle into an exploded line-up above the bottom 20 % | **"BLACK FRIDAY" / "V2 KIT 30% OFF"** (owner's wording; scope per Q2) | cut on downbeat | Blender + Remotion text |
| 7 | 9.0-11.0 | 2.0 | bar 6 | Side tracking at sill height, 50 mm, a rolling shot | Side skirt and rear spat at speed down the straight | GLB | The skirt leads the frame; the spat passes at the end of the shot | none | cut on downbeat | Blender |
| 8 | 11.0-13.0 | 2.0 | bar 7 | Same framing as shot 6 (mirrors card 1) | Black card: V1 lip, skirts and spats | GLB V1 nodes (`part_front_lip`, `part_side_skirts`, `part_rear_spats`) in the silver look | Same line-up move as shot 6 | **"V1 UP TO 45% OFF"** (owner's wording; scope per Q3) | cut on downbeat | Blender + Remotion text |
| 9 | 13.0-15.0 | 2.0 | bar 8 | Low rear 3/4, static; the car passes the lens | GR Corolla blasting past, then away into the braking zone | GLB | The rear spats read as it passes; it leaves the frame on the last beat | none | dip to black on downbeat 9 | Blender |
| 10 | 15.0-18.0 | 3.0 | downbeat 9 | Static | Epsilon+ wordmark card, ~720 px wide, plus "EPSILON.PLUS" | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | Logo on the downbeat, held, music fade | "EPSILON.PLUS" (store URL; optional per Q6) | end | Remotion / ffmpeg |

**Optional character beat (only if the user says yes, Q5):** a 2-beat insert between shots 8 and 9.
- Pip (cel-shaded, `projects/scan-tedium-explainer-reel/tools/partA_scene.py` rig) leans in at the edge of the V1 card, eyes go ^ ^ (excited), and Gus, matter-of-fact, appears behind him.
- No dialogue, so no voice cost.
- The cost is a cel-shaded style break and their Illumaesthetic nametags inside an Epsilon ad.

## What the text rules mean here
- No text appears over any real or CGI driving shot. Both offers sit on black scan cards (shots 6 and 8), which is the brief's alternative.
- No prices, stock counts or specs on screen, only the owner's discount wording. Prices checked live on 2026-11-17 are kept here for reference only:

| Product (store name) | Price | Stock |
|---|---|---|
| Front Lip V2 - GR Corolla (Zenki, E210, 2023-2024) | $285 PU | 64 |
| Side Skirts V2 - GR Corolla (E210, 2023+) | $400 | 67 |
| Rear Spats V2 - GR Corolla (E210, 2023+) | $175 | 35 |
| Front Lip - GR Corolla (Zenki) [= V1] | $215 PU / $600 CF | 69 / 14 |
| Side Skirts - GR Corolla [= V1] | $275 | 27 |
| Rear Spats - GR Corolla [= V1] | $125 | 20 |
| Canards | $320 | backorder (-2) |

- No compare-at discounts are set in the store yet.
- The V1 products are not called "V1" on the store. A card that says "V1" won't match the listing names, so see Q3.

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
| Epsilon characters | **none exist** | Pip & Gus are Illumaesthetic mascots (git only: scan-tedium-explainer-reel + pip-gus-ep* branches) |
| Music | candidates listed | TikTok CML (Higgsfield), not yet downloaded |

## Open questions for the user
1. **Footage.** There is no real track or autocross clip of the V2 car. Which do you want?
   - **(a) CGI track** (recommended, this plan);
   - **(b)** you send real track or autocross clips;
   - **(c)** cut from the posted "GR COROLLA ROLLERS" street edit. It's street, not track, it's already posted, and some shots look CGI.
2. **"V2 kit 30% off"** covers which listings: lip, skirts and spats only? Canards too? The Kouki (2025+) lip ($285)?
3. **"V1 up to 45% off"**: which V1 items and variants get 45%, and which get less? Is "V1" the right word on the card, given the store calls them "Front Lip / Side Skirts / Rear Spats" without "V1"?
4. **CGI paint.** The real V2 car is the white Castrol/Motegi #24 livery (the GLB ships a `livery_castrol` material). Do you want that livery, which puts Castrol branding in the ad, or a plain paint, e.g. Supersonic Red as in the earlier reel?
5. **Pip & Gus** are Illumaesthetic mascots with Illumaesthetic nametags. Should they appear in this Epsilon ad (the optional 2-beat cameo, no dialogue)? Or did "Epsilon characters" mean something else?
6. **End card.** Wordmark alone, or with "EPSILON.PLUS" / "BLACK FRIDAY" under it?
7. **Music.** Pick one of the four candidates, or name your own real track.

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
