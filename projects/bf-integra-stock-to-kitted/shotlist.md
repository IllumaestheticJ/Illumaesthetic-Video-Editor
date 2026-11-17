# BF 2 of 8: integra-stock-to-kitted (shot list for approval)

**Status: PLAN ONLY.** Nothing is rendered until the user approves this in chat.
Planned 2026-11-17. Prices and stock were re-checked on the live Shopify store "Epsilon+ Aerodynamics" the same day.

## Concept in one line
The real stock-state scan of our white Integra (DE4 A-Spec) rolls past Del & Eps on black. On the drop there is a hard 1:1 cut to the same car rolling past for real, now wearing the lip, skirts, spats and Sport Wing. Then the four parts from the website model land as a kit, with Del & Eps at 1:10 scale on them, followed by the price card and the Epsilon+ wordmark.

## Owner's concept (verbatim)
> Stock → kitted. One cut on a beat. A stock Integra drives past the camera, and on the drop it passes again with the lip, skirts, spats and Sport Wing. Then the price card: "Full kit, 30% off."

## What exists for "two passes, one cut" (checked before choosing a method)
| Need | Found? | What it is |
|---|---|---|
| Real footage of the KITTED Integra driving | **Yes** | Dropbox `/2. Illumaesthetic Videos/OLD/Completed/Acura Integra DE4 DE5/integra roller/`, 15 DJI clips shot 2024-03-24, 3840x2160 at 29.97 fps, Rec.709. White DE4 with plate 9CHB735, fitted with the lip, skirts, spats and white Sport Wing. I looked at 0370 (rear 3/4, camera car behind) and 0371 (side-on tracking, all four parts in view). |
| Real footage of the STOCK Integra driving | **No** | I did not find any. The 2024-01-30 `Integra scan` clips show the car parked and being scanned at night. The other 13 roller clips have not been looked at yet; those I sampled are all kitted. |
| Scan of this car in its stock state | **Found, still to verify** | Engineering Drive `Integra 2023/Spoiler_/Integra A_spec_scan_full_relocated.stl` (id `123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV`, 914 MB, 2024-03-18). The car was scanned before the kit existed; the posted `Integra Kit.mov` shows the same plate being scanned. I still need to render it and confirm there is no prototype lip or other kit on it. |
| Website GLB (lookbook) | **Yes** | `eps-acura-integra-de-v29.glb` (sha 4bc2e068a4c9e42c, same as the lookbook JSON). Nodes: `part_front_lip`, `part_side_skirts`, `part_rear_spats`, `part_sport_wing`, `part_duckbill` + `body_duckbill_stock`, `part_fender_flares`. Lookbook entries `lb-acura-integra-de-*.json` (e.g. 015f28d1c3 = Lunar Silver). The "de5-configurator" branch the brief names does not exist; that work is on `claude/adoring-pascal-lu0o87` (`projects/de5-configurator`, the DE5 Type S GT Wing). |

**Method:** scan to real, the house 1:1 cut, used in the reverse direction (precedent: Nissan Frontier v6 ends the scan shot on the solved camera of the first IRL frame).
- Pass 1 is the real scan of the stock car, silver on black. Its camera ends exactly on the camera solved from the real frame.
- Pass 2 is the real kitted footage, starting on that same frame.
- The kit "appears" at the cut and nothing else moves.

This needs no CGI street environment and no stock driving footage, and both passes are the same car.

## Target length
About 17.5 s (41 beats at 140 BPM). This is short-form, inside the brief's 10-25 s.

## Music candidates (TikTok Commercial Music Library, real tracks, none used by another reel)
I checked every candidate against the song_clip_ids in the other projects' editlogs. Each one starts from the song's beginning, as the brief requires.

| # | Track | song_clip_id | Why |
|---|---|---|---|
| 1 (recommended, **claimed** in `projects/_blackfriday/MUSIC.md`) | "140" by Lil Texas | 7597234501887166481 | Quiet intro, then the first hard low hit at ~6.89 s (measured on the CML preview). ~139.5 BPM. The intro carries the stock pass with no cut, and the drop lands on the 1:1 cut. It is a hard track; if that is too aggressive for a sale ad, use #2. |
| 2 | "BLACK FRIDAY" by NUMMA | 7427572790179563521 | On-theme title. Its big hit is at ~16.7 s (~128 BPM), so the stock pass would have to run ~16 s, or the video would start before the song does. That breaks "start from the beginning" unless the user OKs it. |
| 3 | "Electric Youth" by Chris_record | 7421090393491785729 | #1 EDM in the US 7-day chart. Steady kick from 0 s with no drop, so the cut would sit on a bar accent instead of a drop. Weaker. |

I have not used "THE DEATH", "Prisoner", "Time Back", "FREAKED OUT", "Invincible" or "Ghosts 'n' Stuff"; other reels already use them. BF 6 already claimed "Electric Youth", so #3 is out unless they release it. All times are from the 40 s preview. I re-measure on the licensed full track (kick-peak grid, `music_grid.py`) before cutting.

## Shot table
Times assume track #1: beat = 0.4286 s, drop at 6.89 s = beat 16. They are re-fitted to the measured grid before rendering. "No text" means none, by rule, on every IRL shot.

| # | Time (s) | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-3.43 | 3.43 | 0-8 (intro) | Low front 3/4, 0.6 m high, slow push as the car rolls toward and past the lens | STOCK car, front end: bare stock bumper and sills. **Del & Eps** stand at the roadside at 1:1, in silver (they scan in with the laser sweep during beats 0-2, per the v0.1 rule). Eps points his scanner at the car as it passes; Del watches. | Scan `Integra A_spec_scan_full_relocated.stl` (Drive `123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV`), silver on black; Del & Eps low-poly models (to build) | Car translates past on black; faint floor reflection sells the motion | None | Hard cut on beat 8, only if the track has a hit there (measure); otherwise shots 1+2 become one continuous move | Blender (ive prep/render, silver look) + character models |
| 2 | 3.43-6.89 | 3.46 | 8-16 | Side tracking at the camera-car height of DJI 0371, panning tail → nose so the frame lands on the solved pose | STOCK car, side: plain sills, no spats, stock trunk | Same scan | Camera **ends exactly** on `cam_0371.json`, solved from the 0371 cut frame. Key the pose 2 frames early and hold it. | None | **HARD 1:1 CUT ON THE DROP** (6.89 s) | Blender |
| 3 | 6.89-10.32 | 3.43 | 16-24 (drop) | Real camera car alongside; the 9:16 window slides along the car nose → tail at constant scale | KITTED car, same pose: the lip, skirts, spats and wing appear at the cut | DJI `DJI_20240324162540_0371_D.MP4` (Dropbox id `ihAynaYnO_4AAAAAAAAK5A`), from the solved frame | Window shows the lip first, then the skirt, then the spat and the Sport Wing as the clip rolls | None (IRL) | Hard cut on beat 24 | Footage edit (crop 1215x2160 window from 4K, conform 29.97 → 30) |
| 4 | 10.32-12.03 | 1.71 | 24-28 | Real camera car behind, rear 3/4 | KITTED car from behind: Sport Wing, spats, diffuser | DJI `DJI_20240324162511_0370_D.MP4` (Dropbox id `ihAynaYnO_4AAAAAAAAK4w`), ~4.0-5.7 s (wing closest) | Car rolls toward the camera car | None (IRL) | Hard cut on beat 28 | Footage edit |
| 5 | 12.03-13.71 | 1.71 | 28-32 | Black studio, 3/4 from above (~30 deg) | The four products from the website model, with **Del & Eps in micro mode (~1:10)**: Eps rides the Sport Wing endplate, Del stands on a spat strake | `eps-acura-integra-de-v29.glb` nodes `part_front_lip`, `part_side_skirts`, `part_rear_spats`, `part_sport_wing`, in lookbook materials. Wing in gloss black (the price the card quotes) unless the user wants Platinum White like the car. Del & Eps in livery A (Del teal #0f5c63 / orange #ff7a1a, Eps violet #6b3cff / yellow #ffd21f). | One part drops into its place in a kit layout on each beat (28, 29, 30, 31); each part washes violet as Eps's beat lands, then settles to its real material. One pose per character (hold up / point). No spins (lesson). | Optional: part name + BF price under each part (owner's TL;DR, below). Only if the user wants per-part prices. | Cut on beat 32 | Blender (GLB + characters) + Remotion text |
| 6 | 13.71-15.43 | 1.71 | 32-36 | Same as 5, held | The kit layout | Same render | Card text lands on beat 32 | **"Full kit, 30% off"** (owner's wording). The confirmed tiers put the spats at 40-45 %, so the wording needs a decision, see Q1. | Cut on beat 36 | Remotion over the shot 5 render |
| 7 | 15.43-17.57 | ~2.1 | 36-41 | n/a | Epsilon+ wordmark, ~720 px wide, centred | Drive `EPSILON+ Logos` (exact file to locate; Epsilon wordmark, not Illumaesthetic) | Lands on beat 36 and rides the decay | Optional `epsilon.plus` under the logo, if the user wants a CTA | End | Remotion |

### The 1:1 cut, in detail (`knowledge/match-cut.md`)
1. **Pick the frame.** Choose a calm frame of 0371 (the camera car steady relative to the car) where the body shows rigid landmarks spread in depth:
   - both wheel centres;
   - the mirror;
   - the door handles;
   - the A-pillar base;
   - the tail-lamp tip.

   The lip, skirts, spats and wing must NOT be used as landmarks: the scan has none of them.
2. **Solve.** Solve on the full 3840x2160 frame with free focal (the DJI lens is unknown), then build the 9:16 crop camera with lens shift as a fraction of the image WIDTH (lessons IS350 / Miata Grimace). Target RMSE ≤ 3 px. Verify with an onion overlay, not the score.
3. **Stance.** The real car is lowered on aftermarket wheels. The posted `Integra Kit.mov` suggests it was already like that when scanned, but I need to check the arch gaps at the solved view (400Z v9 method). If the stance differs, say so; do not fake it.
4. **Wheels.** The scan's wheels do not spin. At the cut the spokes differ; that is acceptable.
5. **Timing.** The scan camera settles ~0.5 s before the drop, not 1.5 s (QX80 v7h).

## Asset inventory
| Asset | Path / ID | Status |
|---|---|---|
| Stock-state scan, DE4 A-Spec (this car) | Engineering Drive `Integra 2023/Spoiler_/Integra A_spec_scan_full_relocated.stl`, `123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV` (914 MB). Same folder: `..._rear_relocated.stl` (`123Y2-ZNV3EB_kLdZ_sBjglAutc6nhyb1`), `..._trunk_relocated.stl` (`1247g2k9gixm_f9jzBYDvoKhXhiQnCs8g`) | **found**; to verify stock state + plate legibility. The original export is Engineering `Acura Integra 2021+/Integra ASpec.stl` (`1bx1Rrjxnz8jI6mIDFBL_y44dmcYHVufx`, 2024-01-08). It is byte-for-byte the same size as the relocated file, so it is the same mesh in another frame, and it is dated before the kit existed. The same folder holds state scans: `Integra ASpec Trunk Open.stl` (`1F5z5BSy771p1J3dESgJ7PfcvJpm5iDe8`), `... Side Skirt.stl` (`1fJy6xJxfzuPrtKCGUVSomPrGfkjJgN0w`), `... Rear.stl` (`1F3lfr0FnH6_S5VsyZ2uEy5WGXnICcp6e`), `... Integra Diffuser.stl` (`1NxYio4tmc9ghfvHP-CXbNBzMBIs8NZ6d`). This plan uses the relocated file (the frame the kit was designed in). The Type S scan is not used: the lip, skirts and spats are DE4-only. |
| Website GLB, DE4 | `cdn.shopify.com/.../eps-acura-integra-de-v29.glb` (downloaded to `/home/user/media/bf-integra-stock-to-kitted/glb/`); also inside Drive `Epsilon-final-GLBs-2026-10-15.zip` (`12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7`) | **found** |
| Kit part CAD (cross-check only) | Drive `A Spec Printing Files/`: `A_Spec_FR_Lip_full_with Logo.stl` (`1285EGMJTqVpQFhUCd3VGOf2MiTkDjTkn`), `A_spec_sideskirt_left/right_V1_full_with_logo.stl` (`128u8cvey9g4YvIYEqSxvoZxpMBmqejgv` / `128GAe8iFzX0CzmequHdpiyTLlLmw6iwq`), spats folders (stock / aero diffuser); `Integra Sport Wing Scan .stl` (`1s5ggkKLZPmIdofrnGhpy-upbbcNw6rTq`) | **found** (GLB parts are used on screen) |
| Kitted driving footage | Dropbox `.../Acura Integra DE4 DE5/integra roller/` 0362-0376 (2024-03-24) | **found**; 0370/0371 checked, the other 13 still to sheet |
| Kitted footage, vertical (backup) | Dropbox `/2. Illumaesthetic Videos/1. Video dumps/*Posted Raw Videos/2024 Finished Video/Jackie/Posted/integra kit.mov` (`ihAynaYnO_4AAAAAAAAFjQ`), 1080x1920. Front 3/4 roll-by 13.8-16.1 s and side pass 17.2-19.5 s have no burned-in text. It is a posted edit, so it is fallback only. | **found** |
| Stock driving footage | none found | **missing**; not needed by this plan |
| Epsilon characters: **Del (δ) & Eps (ε)** | Owner's concept pages: v0.1 https://claude.ai/artifact/MyfYpve1ho7AhiTSzvRCFf and v0.2 colours https://claude.ai/artifact/E2AUcUQJsG5a937FCorTQD, summarised in `projects/_blackfriday/MASCOT_AND_PRICES.md`. These are concept sketches only: there is no model, rig or turnaround. Pip & Gus are the Illumaesthetic mascots and are NOT used here (owner's decision). | **concept found; models missing (to build)** |
| Epsilon+ wordmark | Drive folder `EPSILON+ Logos` (per lessons.md) | **to locate** |
| Music | TikTok CML (Higgsfield `tiktok_music_trending`); previews in `/home/user/media/bf-integra-stock-to-kitted/music/` | **candidates found**; licensed full track to fetch after approval |

## Live store facts (Shopify, 2026-11-17)
| Product (handle) | Variant on the car | List price | Stock |
|---|---|---|---|
| Front Lip – Acura Integra (DE4, 2023+) (`epsilon-front-lip-acura-integra-de-2023`) | Polyurethane | $285 | 26 |
| Side Skirts – Acura Integra (DE4, 2023+) (`epsilon-side-skirts-acura-integra-de4-2023`) | Polyurethane | $400 | 61 |
| Rear Spats – Acura Integra (DE4, 2023+) (`epsilon-rear-spats-acura-integra-de4-2023`) | OEM Stock (A) / OEM "Aero" diffuser (B) | $175 | 30 / 38 |
| Sport Wing – Acura Integra (DE4/DE5, 2023+) (`epsilon-wing-acura-integra-de-2023`) | Gloss black / Platinum White Pearl NH883P (the car) | $500 / $1,000 | backordered (-10 / -2) |
| Sport Wing + Rear Trunk Lip combo (same listing) | Gloss black / painted | $600 / $1,050-$1,100 | backordered |

### Confirmed BF tiers (owner's doc "Black Friday 2026 Discounts: TL;DR", https://claude.ai/artifact/29kGfJ2WPdSAg5QpezXfva, via `projects/_blackfriday/MASCOT_AND_PRICES.md`)
- **Front lip and side skirts: 30 %.** $285 → $199.50, $400 → $280.
- **Integra rear spats: 40-45 % clearance**, not 30 %. The exact percentage for the Integra spats is not stated: $175 → $96.25 (45 %) or $105 (40 %).
- **Sport Wing: 30 % on the base only**; the paint charge stays full. Gloss black $500 → $350; painted $1,000 → $850.
- **Sport Wing + Trunk Lip combo:** gloss black $600 → $385. Rear trunk lip alone: 60 %.
- **Nothing on preorder or backorder is on sale.** The live store shows the Sport Wing at negative inventory (gloss black -10). Its listing still says "Available Now, Ready to Ship". See Q1.
- **The sale window is not set yet.** No dates on screen.

My arithmetic, not for screen unless approved:

| Kit | Was | BF | Overall discount |
|---|---|---|---|
| Lip + skirts + spats + gloss black wing | $1,360 | $925.75-$934.50 | 31.3-31.9 % |
| Lip + skirts + spats + wing/trunk-lip combo | $1,460 | $960.75-$969.50 | 33.6-34.2 % |

So "Full kit, 30% off" understates the deal slightly. It is true as "at least 30 %", but not as a flat 30 % on every part. Nothing on screen will show a stock count.

## Open questions for the user
1. **Card wording.** Under the confirmed tiers, the lip, skirts and wing base are 30 %, but the Integra spats are 40-45 %. The kit comes out 31-32 % off ($1,360 → ~$930 with the gloss black wing). Which card do you want?
   - (a) "Full kit, 30% off", as the owner wrote it;
   - (b) "Full kit, 30%+ off";
   - (c) "Full kit, 30% off" plus "was $1,360 → $9xx", once you confirm the spats percentage and whether the trunk lip / combo is in the kit.

   Also: the Sport Wing shows negative stock (backordered) on the store, and backordered items are excluded from the sale. Is the wing in the sale?
2. **The stock pass is the real scan of this car (silver on black), not real driving footage.** No footage of the car driving stock exists; its stock state only exists as the Jan-2024 scan. Is scan → real OK for "it passes again"? The other option is the website GLB with the parts hidden, in a CGI street. That is more work and would match the real street less well.
3. **Music:** "140" by Lil Texas (drop ~6.9 s, hard), or the on-theme "BLACK FRIDAY" by NUMMA? NUMMA's drop is at ~16.7 s, so it needs a longer stock pass or starting mid-song.
4. **Del & Eps.** They exist only as concept sketches. I plan two appearances, both in the scan world, never over real footage:
   - shot 1 at 1:1, roadside, in silver, scanning in;
   - shots 5-6 at 1:10 on the parts, in livery A, which I default to since nobody has picked one.

   The cheapest path that holds the look is low-poly Blender models (<15k tris), one static pose each plus the laser scan-in, with no rig and no voices. OK? Or would you rather a turnaround sheet is approved first? Is livery A right?
5. **Wing colour on the kit card:** gloss black (the $500 base, cheapest to show) or Platinum White like the real car?
6. **Spats:** the GLB has one spat version and the store has two. Which version is on the white car? Should the card show both?
7. **Per-part prices on the kit layout (shot 5): yes or no?** Should the end card carry `epsilon.plus`?

## Production steps (after approval)
1. `ive log` each approved answer. Fetch the full licensed track; build the kick-peak grid; lock the drop frame and every cut to round(t*30).
2. `ive fetch-drive 123P7-gaQN2jAWDxyVNjugX3KsWf6D0MV`.
   - Decimate out-of-core (914 MB Artec).
   - Level it (RANSAC, `huracan-evo/tools/level.py`).
   - Prep once and pin it with `--like`.
   - Render front, side and rear silver checks to confirm the stock state.
   - Look at the plate in the scan.
3. Sheet all 15 roller clips. Pick the 0371 cut frame and the 0370 window. Grade check: DJI Rec.709, no LUT expected.
4. Solve the camera on the 0371 frame (≥8 body landmarks spread in depth, free focal), build the 9:16 crop camera, and check the onion overlay plus the stance at the arches.
5. Build Del & Eps at low poly from the v0.1/v0.2 sketches; the Pip & Gus procedural Blender build is the technical precedent. Send the user a turnaround still before using them.
6. Render shots 1-2 (scan, silver look) ending on the solved camera. Check per-frame luma for black-frame dropouts. Check the first, middle and last frames.
7. Render shot 5 from the GLB: four parts, lookbook materials, `part_fender_flares` and `part_duckbill` hidden unless Q1 includes the trunk lip.
8. Build shots 6-7 in Remotion. Text comes only from the owner's wording and live Shopify data, re-checked on the day of render.
9. Assemble with the concat assembler (exact frames per clip, hard cuts only). Mix at -14 LUFS with true peak below -1 dBFS. Verify cut times against the decoded audio (≤ ½ frame).
10. Self-score with `training/rubric.md`, then `ive archive`, commit and push.
