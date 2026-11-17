# BF 7/8 - "miata-mr2-night-meet" - shot list (PLAN, awaiting user approval)

Planned 2026-11-17. Nothing rendered. Production starts only after the user approves this plan in chat.

## Concept (one line)
Moody night parking-lot meet: an Epsilon-kitted MR2 Spyder (ZZW30) and NC Miata under sodium lamps. Each part gets a beat,
each car makes one hard 1:1 cut into its silver scan with the Epsilon fiberglass part landing on the scan, then the
"Fiberglass 20% off" card (fiberglass parts only) and the Epsilon+ wordmark.

## Target
- 9:16, 1080x1920, 30 fps, **~22-24 s** (short-form; two cars + card + logo need a little more than 20 s).
- Ends on the Epsilon+ wordmark (Drive `EPSILON+ Logos`) at about 720 px wide. Not the Illumaesthetic logo.

## Music candidates (real songs only; not generated; not used by another reel)
The tracks other reels have already used are excluded: the GT2 East City / South City / license tracks, M.O.O.N. Paris,
FREAKED OUT, Prisoner, Sector Shift, the NFSU2 track (MR2 SW20 v3), Going Up North, Buckshot, Alkitran, Riders and the
original city-pop MR2 track.
1. **Kavinsky - "Nightcall"** (night-drive synthwave). Slow, moody intro with a hard kick entry, which suits a sodium-lamp lot.
2. **M83 - "Midnight City"**. The famous synth-horn hook gives strong accents to cut on.
3. **A night/phonk track from the TikTok Commercial Music Library** (Higgsfield `tiktok_music_trending`). This is the
   licensed route for paid ads. Snare every 2 beats = clean cut grid.
The user must supply or approve the file. Downloading from YouTube is not possible here. Start from the song's beginning,
mix at -14 LUFS with true peak below -1 dBFS, and fit the beat grid to kick peaks, not `ive beats` alone (lessons L96, L185, L257).
**Timings below use a placeholder grid of 120 BPM (1 beat = 0.5 s)** and will be re-snapped to measured hits once the track is chosen.

## Shot table
Legend: CGI = epsilon.plus lookbook GLB in the night-lot environment. SCAN = engineering-Drive scan in the house satin
silver on black, with the GLB kit part nested by `kit_nest2.py`. Labels (Remotion `ScanHUD`) appear only on SCAN shots or
cards, never on IRL footage, with at most two items on screen.

| # | time (s) | dur | beat | camera | subject | source asset (exact) | action | on-screen text (source) | transition out | render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-1.5 | 1.5 | b0-3 | low front-3/4, 35 mm, slow push-in 8 % | MR2 nose under one sodium lamp, wet asphalt | `eps-toyota-mr2-spyder-v19.glb` (part_front_bumper, part_eyelids, part_hood_vents visible; red paint) in `tools/city_env.py` lot variant. **If** the 2025-07-24 night-meet footage shows the MR2, this shot becomes that IRL clip | headlights flick on, camera eases in | none | **hard 1:1 cut on b3** (CGI -> scan, same camera) | Blender Cycles |
| 2 | 1.5-3.5 | 2.0 | b3-7 | same camera, continues the push-in | MR2 silver scan | Drive `MR2 Spyder Scan Data/Full Car Top Down.stl` (id 1F1JS1meWgjj3xeYpM8Su-FV6bZC07H1X) + GLB `part_front_bumper` nested over `body_front_bumper_stock` | the stock bumper zone comes off **whole** (falls out of frame), the Epsilon bumper drops in and seats on b5 | "FRONT BUMPER" / "FIBERGLASS" (Shopify product type + tag) | hard cut | Blender |
| 3 | 3.5-4.5 | 1.0 | b7-9 | macro, headlight height, lateral slide | MR2 headlight eyelids | GLB `part_eyelids` (CGI) | lamp flare slides across the eyelid edge | none | hard cut | Blender |
| 4 | 4.5-5.5 | 1.0 | b9-11 | top-down 3/4 over the hood, 50 mm (never straight overhead, lesson L416) | MR2 hood vents | GLB `part_hood_vents` replacing `body_hood_vent_stock` (cut the way the lookbook does it, per the MR2 v4 reviewer fix) | rain beads, heat shimmer from the vents | none | hard cut | Blender (**pending Q2**) |
| 5 | 5.5-7.0 | 1.5 | b11-14 | low side track, rear-to-front, at wheel height | MR2 side skirt/fender combo | GLB `part_side_skirts` (over `body_fender_cut_stock` + `trim_fender_liner_stock`) | the lamp reflection rolls along the skirt | none | hard cut | Blender |
| 6 | 7.0-8.5 | 1.5 | b14-17 | rear-3/4 low, slow rise | MR2 rear: spats + duckbill, taillights | GLB `part_rear_spats`, `part_duckbill` | the taillights glow; the camera rises to show the duckbill | none (the duckbill is ABS, so no "fiberglass" label) | hard cut on the downbeat (car change) | Blender |
| 7 | 8.5-10.0 | 1.5 | b17-20 | low front-3/4, mirrored composition of shot 1 | NC Miata nose under the next lamp | `eps-mazda-mx5-nc-v19.glb` (part_front_bumper, part_fender_cuts; Rubystar `#a61f59`); kit config in Q5 | pop-up of the headlight glow, camera eases in | none | **hard 1:1 cut on b20** (CGI -> scan) | Blender |
| 8 | 10.0-12.0 | 2.0 | b20-24 | same camera; front-framed (NC reviewer: frame the front while the bumper comes off) | NC silver scan | Drive `Mazda Miata NC` (117x9LQvHdB1J88dcs8H8bagCL9DTstfK): Full Car 1KnzXa391W0DCdSqmQe3i2IZEjGv17CLe + Front Bumper Off (Hood Closed) 1LGmOpWaPGVPgkBQeO-CQVBrkv7Qb9vTA as the part-off state; GLB `part_front_bumper` | the stock bumper comes off **whole** (bumper-only scan 1LAwZsiIJwyL_-aGAqISgfvIO92hZRjek as the moving part), the Epsilon bumper slides in | "FRONT BUMPER" / "FIBERGLASS" | hard cut | Blender |
| 9 | 12.0-14.0 | 2.0 | b24-28 | front-wheel close-up, slow 15 deg orbit | NC fender cuts on the scan | same NC scan + GLB `part_fender_cuts` | the fender's stock zone lifts off, the Epsilon fender cut drops on | "FENDER CUTS" / "FIBERGLASS" | hard cut | Blender |
| 10 | 14.0-15.5 | 1.5 | b28-31 | CGI, same lens as #9 | NC fender cut at night, wheel/tyre | GLB `part_fender_cuts` (CGI) | the lamp reflection travels over the fender cut | none | hard cut | Blender |
| 11 | 15.5-17.5 | 2.0 | b31-35 | wide, high 3/4, slow crane-down | both cars parked nose-to-nose in the lot | both GLBs in the lot. **Optional cameo (Q3):** Pip with his handheld scanner at the NC fender, Gus with goggles up beside him (Blender toon rig, `projects/scan-tedium-explainer-reel/tools/partA_scene.py`, Illumaesthetic badge) | cars sit under the lamps, light rain. Cameo: Pip sweeps the scanner and Gus gives a nod (no voice) | none | hard cut | Blender (+ EEVEE toon pass for the cameo) |
| 12 | 17.5-20.5 | 3.0 | b35-41 | static card | "FIBERGLASS 20% OFF" | Remotion card over a darkened, blurred still of shot 11 (CGI, not IRL) | title on b35, then the part list on b37: MR2 Spyder (front bumper, side skirt/fender combo, rear spats, headlight eyelids, [hood vents]) and NC Miata (front bumper, fender cuts, [side skirts, rear spats, canards]) | wording from the owner; part names from Shopify titles; **no prices or stock counts** unless the user gives the Black Friday prices (Q1, Q4) | hard cut | Remotion |
| 13 | 20.5-23.0 | 2.5 | b41-46 | static | Epsilon+ wordmark ~720 px + "epsilon.plus" | Drive `EPSILON+ Logos` | lands on the last downbeat and rides the decay | "epsilon.plus" | end | Remotion |

The scan shots (2, 8, 9) keep the plates as scanned (plates are flattened only on the IS300) and use the scan only as
captured. Removed parts come off whole and leave the frame entirely (end more than 4 m away). Nothing comes off a bumper
before the bumper itself.

## Asset inventory
| asset | status | path / id |
|---|---|---|
| MR2 lookbook GLB `eps-toyota-mr2-spyder-v19.glb` (part_front_bumper, part_eyelids, part_hood_vents, part_side_skirts, part_rear_spats, part_duckbill, + body_*_stock) | found (re-download) | Drive `Website Files/Epsilon-final-GLBs-2026-10-15.zip` id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7, or the epsilon.plus lookbook CDN |
| NC lookbook GLB `eps-mazda-mx5-nc-v19.glb` (part_front_bumper, part_fender_cuts, part_side_skirts, part_rear_spats, part_canards, part_gt_wing...) | found (re-download); **NC `body_*_stock` names not yet listed** | same zip |
| MR2 GLB-to-scan fit + nesting | found (code) | `projects/toyota-mr2-spyder/tools/kit_export.py`, `kit_align.py`, `kit_nest2.py`; outputs need regenerating (no media on disk) |
| NC alternative CGI: `Miata NC Complete Kit.glb` (664 MB) | found (parent ASSETS.md), not yet opened. Compare with the lookbook GLB; use whichever matches the store parts | Drive 1ZGgplW790QltSuHm_8xqWqGl8h_eucyn |
| NC GLB-to-scan fit + nesting | **missing** (new work) | adapt the MR2 tools to the NC |
| MR2 scan | found | Drive folder `Toyota MR2 Spyder` 1Apk8IymqNIM5osub5qZzzQxO7airXf8G; Full Car Top Down.stl 1F1JS1meWgjj3xeYpM8Su-FV6bZC07H1X |
| NC scans (full car, bumper only, bumper-off states) | found | Drive 117x9LQvHdB1J88dcs8H8bagCL9DTstfK (ids in shots 8-9) |
| Night environment | found but weak | `projects/toyota-mr2-spyder/tools/city_env.py` (expressway, via `cgi_drive.py`). The reviewer said it was "very low detail": a **parking-lot variant with more detail** is new work |
| Real night-meet footage | **to verify** | Dropbox `/Footage Library/Videos/Shoot Sessions/2025-07-24 Night meet/` (4 .mov, ids ihAynaYnO_4AAAAAAACRoA / ...CTIQ / ...CTIA / ...CRmg) and `Events & Meets/2025-07/2025-07-24 21.28.30.mov` (ihAynaYnO_4AAAAAAADCtg); `2025-08-10 Night shoot` (5 clips). Cars unknown: previews were blocked, so these must be downloaded and sheeted |
| Real MR2 at night (shop, not a lot) | found | Dropbox `MR2 HARDTOP` dump, DJI_20250715210710_0030 + FX30633-649 (Jul 15 2025, 21:06-21:43) - shop interior with crew, so it does not fit "parking-lot meet" |
| Real NC footage | found, not night | `2026-08-05 Pink NC Miata` (6-7:23 PM); `4. Photoshoots/NC Miata/` stills |
| Style reference | found | Dropbox `/5. Claude Training/Good Reels (Epsilon)/NFSU2 car lot - 1440p.mp4` (ihAynaYnO_4AAAAAAACHHQ) |
| Epsilon characters | **none exist** | Pip & Gus (branches `claude/pip-gus-ep0..ep9`) are Illumaesthetic mascots with an Illumaesthetic badge. Spec: `projects/scan-tedium-explainer-reel/characters/design.md`; Higgsfield refs Gus 31001f1d-..., Pip 9cbf5fb5-...; rules: never make Gus sad, sage `#619f73` only |
| Epsilon+ wordmark | found | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) |
| Music | **to request** | see candidates |
| Black Friday sale prices / dates | **to request** | - |

## Live store facts (Shopify "Epsilon+ Aerodynamics", checked 2026-11-17; list prices, USD)
- MR2 Spyder ZZW30, fiberglass, made to order: Front Bumper $900, Side Skirt Fender Combo $700, Rear Bumper Spats $350,
  Headlight Eyelids $100, **Hood Vents $400 (vents only) / $470 (vents + relocation brackets)**: the product exists and is
  ACTIVE and published on epsilon.plus since 2023-07-24 (re-checked after the parent's `ASSETS.md` said there was no hood-vent product, which is wrong). Also a fiberglass Hardtop (preorder deposit $50).
- MR2, not fiberglass: Rear Duckbill $220 (**ABS**, stock 10); Diffuser V1+ $750 (aluminium); TC Wing $1,100.
- NC Miata, fiberglass, made to order: Front Bumper $1,100 (bumper/lip) / $800 (top only) / $350 (lip only); Fender Cuts
  $300 / $350 (+ fin); also **Side Skirts $500, Rear Spats NC1 $250, Canards $200** (all tagged fiberglass).
- Every fiberglass line shows 0 or negative inventory (made to order / backordered), so no "only X left".

## Open questions for the user
1. **Card scope.** Should "Fiberglass 20% off" cover only the parts in the owner's concept (MR2 bumper, skirt/fender,
   spats, eyelids; NC bumper, fender cuts), or every fiberglass line (+ MR2 hood vents and hardtop; + NC side skirts, rear
   spats, canards)? Is the discount automatic or a code? And the sale dates?
2. **MR2 hood vents.** The store lists them as fiberglass ($400/$470) and they are in the lookbook GLB (`part_hood_vents`).
   OK to give them shot 4 and put them on the card?
3. **Characters.** No Epsilon characters exist; Pip & Gus are Illumaesthetic-badged. Use them as a silent cameo in shot 11
   ("Illumaesthetic scans it, Epsilon makes it"), or leave them out of this Epsilon ad? Should the badge change?
4. **Prices on the card.** Show the list price struck through next to 20 %-off prices (for example $900 -> $720), or
   only "20% OFF"? We will show only numbers you approve.
5. **NC kit configuration.** The lookbook NC default carries the GT wing, canards, etc. Show only the bumper + fender cuts,
   or the full lookbook kit? (A wing is fine only if it is in that car's lookbook kit.)
6. **Duckbill (ABS).** It is in the concept, so shot 6 shows it, but with no fiberglass label and not on the card. Does it
   have its own Black Friday offer?
7. **Footage.** Shall I download and sheet the 2025-07-24 "Night meet" and 2025-08-10 "Night shoot" clips to see whether
   either car is in them? If neither is, the meet is all CGI + scan; or can someone shoot 10 s of the two real cars in a
   lot at night?
8. **Music.** Pick one of the candidates (or upload a file).

## Production steps (after approval)
1. Download both GLBs (Drive zip) and the MR2/NC scans to `/home/user/media/bf-miata-mr2-night-meet/`; decimate out-of-core
   (≤4 mm full car, ≤2 mm close-ups); list the NC GLB's `part_*`/`body_*_stock` nodes.
2. Fit the GLBs to the scans (`kit_export.py` -> `kit_align.py`, body ICP; check pitch from tyre contacts); run
   `kit_nest2.py` for both cars; render front/side/rear checks of every part on the scan before animating.
3. Build `tools/lot_env.py` from `city_env.py`: parking lot, wet asphalt, sodium + one cyan neon, light rain, more detail
   (the reviewer said "very low detail"); keep window emission ~1-1.5. Approve a still before rendering.
4. Music: user-chosen track -> kick-peak grid; re-snap the table; write `project.yaml` with `section:`/`focus:` per clip.
5. Run the scene-director pass (`projects/<p>/direction.md`) and `ive director`; framing checks at 30 %, then finals one at a
   time in the background (persistent data off), with a per-frame luma scan.
6. Solve the 1:1 cuts as the same Blender camera across CGI -> scan (exact by construction); for IRL, a landmark PnP solve
   plus an onion check.
7. Remotion: labels (ScanHUD), the FIBERGLASS 20% OFF card, the Epsilon+ wordmark card.
8. `ive assemble`; check every cut against the decoded audio (≤ half a frame), mix -14 LUFS / TP < -1 dBFS; contact sheet +
   frames ±2 around each cut; self-score `review.md`; deliver; record feedback; archive; commit + push.
