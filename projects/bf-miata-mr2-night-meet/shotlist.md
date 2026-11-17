# BF 7/8 - "miata-mr2-night-meet" - shot list

> **v1 (user feedback on v0.1): both cars start STOCK and the sale parts install one at a time; see `draft_v1_notes.md` for the
> shot order actually rendered.** The table below is the original plan.
>
> **2026-11-17 owner decision (MASCOT_AND_PRICES.md e05c325): no Del & Eps in the BF videos; typical Epsilon+ branding instead.**
> The character beats below are removed: shots 2 and 8 are scan-only, and shot 10 is the two kitted silver scans with the label
> "MR2 SPYDER + NC MIATA / EPSILON+ · FIBERGLASS AERO". Draft v0.1 follows this.
 (PLAN, awaiting user approval)

Planned 2026-11-17. Nothing rendered. Production starts only after the user approves this plan in chat.

## Concept (one line)
Moody night parking-lot meet: an Epsilon-kitted MR2 Spyder (ZZW30) and NC Miata under sodium lamps. Each sale part gets a beat;
each car makes one hard 1:1 cut into its silver scan, where the Epsilon part lands. both kitted scans share
a silver hero shot, then the 20 % card (sale parts only; the MR2 front bumper is excluded) and the Epsilon+ wordmark.

## Target
- 9:16, 1080x1920, 30 fps, **~22-24 s** (short-form; two cars + card + logo need a little more than 20 s).
- Ends on the Epsilon+ wordmark (Drive `EPSILON+ Logos`) at about 720 px wide. Not the Illumaesthetic logo.

## Music candidates (real songs only; not generated; not used by another reel)
Already used, so excluded: every unused-looking /Moosic track is taken (Grits "My Life Be Like" = Lola, "Real Motorious
City" = Civic 11, Megalomaniac = QX80, FILMMAKER = 400Z, John Wick medley / Kim Petras / Kirby = other BF videos, GT2
themes, Paris, Riders, Get Low, Killa, The Streets, Buckshot, Alkitran, Sector Shift, Blood Code, Thunder, Baby Got Brap).
**Claimed in `projects/_blackfriday/MUSIC.md` (provisional):**
1. **"Tokyo Midnight" - ChilliZone** (TikTok Commercial Music Library, song_clip_id 7667576607158323217, 173 s).
   It is licensed for ads and the title and mood fit a night meet.
2. Backup: **"In the Urban Shadows" - Shiba Beats** (CML 7405070490777159697, 204 s).
3. The user's own pick (e.g. Kavinsky "Nightcall" or M83 "Midnight City") as an upload: the file can't be fetched here.
The user must supply or approve the file. Downloading from YouTube is not possible here. Start from the song's beginning,
mix at -14 LUFS with true peak below -1 dBFS, and fit the beat grid to kick peaks, not `ive beats` alone (lessons L96, L185, L257).
**Timings below use a placeholder grid of 120 BPM (1 beat = 0.5 s)** and will be re-snapped to measured hits once the track is chosen.

## Shot table
Legend: CGI = epsilon.plus lookbook GLB in the night-lot environment. SCAN = engineering-Drive scan in the house satin
silver on black, with the GLB kit part nested by `kit_nest2.py`. Labels (Remotion `ScanHUD`) appear only on SCAN shots or
cards, never on IRL footage, with at most two items on screen.
**Characters:** none (owner, e05c325). Typical Epsilon+ branding only.
**MR2 front bumper is NOT on sale** (owner's BF doc), so it is never featured, labelled or listed. It stays on the car only
as part of the kit (Q2).

| # | time (s) | dur | beat | camera | subject | source asset (exact) | action | on-screen text (source) | transition out | render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-1.5 | 1.5 | b0-3 | low side-front 3/4 at wheel height, 35 mm, slow push-in 8 % | MR2 front fender + skirt under a sodium lamp, wet asphalt | `eps-toyota-mr2-spyder-v19.glb` (red paint) in the `lot_env.py` night lot (from `tools/city_env.py`). **If** sheeting finds the MR2 in the 2025-07-24 night-meet footage, this shot becomes that IRL clip | headlights flick on; the lamp reflection rolls along the skirt | none | **hard 1:1 cut on b3** (CGI -> scan, same camera) | Blender Cycles |
| 2 | 1.5-3.5 | 2.0 | b3-7 | same camera, the push-in continues | MR2 silver scan | Drive `MR2 Spyder Scan Data/Full Car Top Down.stl` (1F1JS1meWgjj3xeYpM8Su-FV6bZC07H1X) + GLB `part_side_skirts` over `body_fender_cut_stock` + `trim_fender_liner_stock` | The stock fender/skirt zone comes off **whole** and leaves frame; the Epsilon skirt/fender combo drops in and seats on b5 | "SIDE SKIRT / FENDER COMBO" (Shopify title) | hard cut | Blender |
| 3 | 3.5-4.5 | 1.0 | b7-9 | macro, headlight height, lateral slide | MR2 headlight eyelids | GLB `part_eyelids` (CGI) | a lamp flare slides across the eyelid edge | none | hard cut | Blender |
| 4 | 4.5-5.5 | 1.0 | b9-11 | high 3/4 over the hood, 50 mm (never straight overhead, lesson L416) | MR2 hood vents | GLB `part_hood_vents` replacing `body_hood_vent_stock` (cut the way the lookbook does it, per the MR2 v4 reviewer fix) | rain beads, heat shimmer from the vents | none | hard cut | Blender (on sale: $400 -> $320) |
| 5 | 5.5-7.0 | 1.5 | b11-14 | rear-3/4 low, slow rise | MR2 rear: spats + duckbill, taillight glow | GLB `part_rear_spats`, `part_duckbill` | the taillights glow; the camera rises over the duckbill | none | hard cut on the downbeat (car change) | Blender |
| 6 | 7.0-8.5 | 1.5 | b14-17 | low front-3/4, mirroring shot 1's composition | NC Miata nose under the next lamp | `eps-mazda-mx5-nc-v19.glb` (Rubystar #a61f59) or `Miata NC Complete Kit.glb` (Drive 1ZGgplW790QltSuHm_8xqWqGl8h_eucyn), whichever matches the store parts; kit config Q5 | the headlight glow comes up, camera eases in | none | **hard 1:1 cut on b17** (CGI -> scan) | Blender |
| 7 | 8.5-10.5 | 2.0 | b17-21 | same camera, framed on the front (NC reviewer: frame the front while the bumper comes off) | NC silver scan | Drive `Mazda Miata NC` (117x9LQvHdB1J88dcs8H8bagCL9DTstfK): Full Car 1KnzXa391W0DCdSqmQe3i2IZEjGv17CLe, Front Bumper Off (Hood Closed) 1LGmOpWaPGVPgkBQeO-CQVBrkv7Qb9vTA as the part-off state, Bumper only 1LAwZsiIJwyL_-aGAqISgfvIO92hZRjek as the moving part; GLB `part_front_bumper` (+ `part_canards` if on sale and in the kit) | the stock bumper comes off **whole** and leaves frame; the Epsilon bumper slides in and seats | "FRONT BUMPER" (Shopify title) | hard cut | Blender |
| 8 | 10.5-12.5 | 2.0 | b21-25 | front-wheel close-up, slow 15 deg orbit (one move, nothing "wasted") | NC fender cuts on the scan | same NC scan + GLB `part_fender_cuts` | the stock fender zone lifts off whole; the Epsilon fender cut drops on | "FENDER CUTS" (Shopify title) | hard cut | Blender |
| 9 | 12.5-14.0 | 1.5 | b25-28 | low side track along the NC | NC side skirt + rear spat at night | GLB `part_side_skirts`, `part_rear_spats` (CGI) | the lamp reflection travels from the skirt to the spat | none | hard cut | Blender |
| 10 | 18.33-21.66 (v0 times) | 3.3 | hit | wide, high 3/4, slow crane-down (silver world) | both silver scans side by side on black, each with its Epsilon sale parts nested | MR2 Full Car Top Down.stl + NC Full Car with the GLB parts | slow crane-down hero of both kitted cars | "MR2 SPYDER + NC MIATA" / "EPSILON+ · FIBERGLASS AERO" | hard cut | Blender |
| 11 | 16.5-19.5 | 3.0 | b33-39 | static card | sale card | Remotion card over a darkened, blurred still of shot 10 (CGI, not IRL) | title on b33, part list on b35, in two columns: **MR2 Spyder** side skirt/fender combo, rear spats, headlight eyelids, duckbill, hood vents; **NC Miata** front bumper, fender cuts, side skirts, rear spats, canards | title wording Q1; tier and parts from the owner's BF doc (20 %: "MR2 parts, NC Miata bumper/fenders/skirts/spats/canards"), part names from Shopify; prices from the BF liquidation sheet, format per Q4; **no dates** (the sale window isn't set) | hard cut | Remotion |
| 12 | 19.5-22.0 | 2.5 | b39-44 | static | Epsilon+ wordmark ~720 px + "WWW.EPSILON.PLUS" | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | lands on the last downbeat and rides the decay. Optional motto line "For every ε, there's a δ." | "WWW.EPSILON.PLUS" | end | Remotion |

The scan shots (2, 7, 8) keep the plates as scanned (plates are flattened only on the IS300) and use the scan only as
captured. Removed parts come off whole and leave the frame entirely. Nothing comes off a bumper before the bumper itself.
The characters never sit inside a part's path, and their hands touch real surfaces at 1:1.

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
| Epsilon characters | **not used** (owner, e05c325: no Del & Eps in BF videos) | - |
| Epsilon+ wordmark | found | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) |
| Music | **to request** | see candidates |
| BF prices | found (the owner's source of truth) | `projects/_blackfriday/PRICES.md` + `bf_liquidation_pricing.csv` (Claude Sheet "Black Friday 2026 Liquidation Pricing", Pricing tab); every MR2/NC FRP part and the duckbill are at 20 %; the MR2 front bumper is "No deal"; sale dates not set |

## Live store facts (Shopify "Epsilon+ Aerodynamics", checked 2026-11-17; list prices, USD)
- MR2 Spyder ZZW30, fiberglass, made to order: Front Bumper $900, Side Skirt Fender Combo $700, Rear Bumper Spats $350,
  Headlight Eyelids $100, **Hood Vents $400 (vents only) / $470 (vents + relocation brackets)**: the product exists and is
  ACTIVE and published on epsilon.plus since 2023-07-24 (re-checked after the parent's `ASSETS.md` said there was no hood-vent product, which is wrong). Also a fiberglass Hardtop (preorder deposit $50).
- MR2, not fiberglass: Rear Duckbill $220 (**ABS**, stock 10); Diffuser V1+ $750 (aluminium); TC Wing $1,100.
- NC Miata, fiberglass, made to order: Front Bumper $1,100 (bumper/lip) / $800 (top only) / $350 (lip only); Fender Cuts
  $300 / $350 (+ fin); also **Side Skirts $500, Rear Spats NC1 $250, Canards $200** (all tagged fiberglass).
- Every fiberglass line shows 0 or negative inventory (made to order / backordered), so no "only X left".

## Open questions for the user
Settled by the owner on 2026-11-17 (via the parent session):
- Prices come from the "Black Friday 2026 Liquidation Pricing" sheet (`projects/_blackfriday/PRICES.md`,
  `bf_liquidation_pricing.csv`). Every item the sheet prices is on sale, including made-to-order and backordered parts.
- MR2 hood vents are on sale ($400 -> $320, or $470 -> $376 with brackets).
- The MR2 front bumper is "No deal".
- No stock counts on screen.

Still open:
1. **Card wording.** The 20 % tier includes the ABS duckbill, and the fiberglass MR2 front bumper has no deal, so
   "Fiberglass 20% off" isn't accurate. Use **"20% OFF - MR2 SPYDER + NC MIATA AERO"** (my suggestion), keep "Fiberglass
   20% off" and drop the duckbill from the card, or something else?
2. **MR2 front bumper ("No deal").** It is part of the lookbook kit. Keep it on the CGI car but never feature or label it
   (current plan), or swap it for the GLB's stock bumper (`body_front_bumper_stock`) so the ad shows no non-sale part?
3. ~~Del & Eps~~: removed by the owner (no characters in BF videos).
4. **Price format on the card.** Using the sheet (Current -> BF 2026):
   - MR2: skirt/fender combo $700 -> $560, rear spats $350 -> $280, eyelids $100 -> $80, hood vents $400 -> $320
     ($470 -> $376 with brackets), duckbill $220 -> $176.
   - NC: front bumper + lip $1,100 -> $880 (top only $800 -> $640, lip only $350 -> $280), fender cuts $300 -> $240
     (+ fin $350 -> $280), side skirts $500 -> $400, NC1 rear spats $250 -> $200, canards $200 -> $160.
   Show the full struck-through list, one headline price per car, or just "20% OFF"?
5. **NC kit configuration.** Show bumper, fender cuts, skirts, spats and canards only (no GT wing; GT wings are not on sale)?
6. **Footage.** Shall I download and sheet the 2025-07-24 "Night meet" and 2025-08-10 "Night shoot" clips for the real cars?
7. **Music.** Is "Tokyo Midnight" (ChilliZone, CML) OK, or would you rather upload your own track?

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
