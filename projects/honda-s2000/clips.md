# Honda S2000 AP1 — Temerario-style scan reel: sources

Scan-only reel (no IRL footage, no text). Sibling of ferrari-296 / huracan-evo / a90-supra.
Reference: `training/references/README.md` → `v_jul22_1047_58` (Temerario).

## Scan data (engineering Drive, folder `Honda S2000 AP1` 10Q5kPEu4yl3060o7KJfT0gwaF_uvxe1M → `Scans/`)
| File | Drive id | Tris | Used | Notes |
|---|---|---|---|---|
| Honda S2000 AP1 Scans_1.stl | 10RVc_CUrggUkvuurjmfpdNAi0Sj4Avvm | 24,975,039 | **full car** | Identical mesh to `S2000 Full Car Scans_1.obj` (10PuH0AVHEeeKuUxBKvq-5TpOcAg0kDK1): same face count, vertices equal to <0.001 mm. Hardtop on, **no wheels**, no ground. |
| S2000 Full Car Scans_1.obj | 10PuH0AVHEeeKuUxBKvq-5TpOcAg0kDK1 | 24,975,039 | (dup) | suggested in the brief; the STL is the same data and needs no conversion |
| AP1 S2000 SD.obj (+jpg/mtl) | 10QXutlcLAjn_GQshHr5ZlPpRf00em6FH | 5,000,000 | no | lower-res textured copy |
| Front End Scans/s2k bumper Front End.stl | 1CA85HLhvuHfK9VQBC6qDOn1cD7Np5nCX | 4.0M | registration anchor | own frame; scanned floor removed (tools/deground.py) |
| Front End Scans/s2k bumper Bumper Only.stl | 1C_h5t-qTXwxTP7mgItJ52mScY4NUBQRe | 4.0M | **exploded/bumper part** | 1.6 mm from Front End (same frame) |
| Front End Scans/s2k bumper Bumper Removed.stl | 1CbshrHf-u4SjpQg1sK3Hq41tqZjAv-Vi | 4.0M | **front structure** | crash beam / radiator support; its one scanned front wheel is boxed out |
| Front End Scans/s2k bumper Hood Open.stl | 1CHTyEdP0iyENC71d2p2OUZW2tyxHls_k | 4.0M | radiator support / bay | only the front ~1 m; the raised hood was not captured; bay behind the radiator support unscanned |
| S2000 trunk.stl | 1dAu7IH14x7NNK-zO_P8EBANQe7cBc_Pm | 3.5M | **NOT USED (v5)** | v1-v4 treated it as a trunk-open capture (interior fill + fitted lid hinge); reviewer: "rear trunk data is made-up" - no real open-trunk scan of this car exists, so no trunk opening and no lid in the explode |
| Honda S2000 AP1 Scans_2.stl | 10RsWP99vLvkTspSfw-j6kEk9RX1fPq0a | 2.0M | no | loose bumper (inner+outer), does not register to the car or Bumper Only |
| Honda S2000 AP1 Scans_3.stl | 10SPxSk4wYL-x1ztTHOIuOqa_dlF2_rCN | 1.0M | no | thin lip strip, not a stock part (possible aftermarket) |
| S2000 Shop Scene.blend | 1VqfOC557mccq6E6AZPOT6xZaeMsr5V5_ | — | no | not needed |

## Frames / transforms (all files in `/home/user/media/honda-s2000/`, not in git)
- `lvl/level.json`: raw Artec → levelled mm (PCA + low points per quadrant; nose −Y). Car length 4,111 mm after debris
  drop (spec 4,135), wheel-arch centres 2,400 mm apart (= wheelbase).
- `prep/car4.json`: the one canonical prep (mm→m, z +0.090). Every other blend is prepped `--like` it.
- `match/T_frontend_z.json`: Front End session → levelled car (RANSAC/FPFH + ICP on hood/fender tops, p50 1.47 mm).
  The state session's bumper sits ~25 mm further forward than the full car's (refitted) → never mixed.
- `match/T_trunk_z.json`: trunk scan → levelled car (5/5 RANSAC tries agree; rear-zone 39 % < 3 mm, rest is interior).
- `match/panels_px.json`: hood + trunk-lid outlines traced on the 2 mm top-down render. `match/lid_hinge.json`: fitted hinge.

## Prepared blends (`prep/`)
car4 (4 mm full car), front2/rear2 (2 mm crops for close-ups), comp_fronthood (bumper+hood off, structure + bay),
comp_fronthood is also the exploded-view base from v5; parts bonly / hood. (comp_trunk, comp_explode, lid: v1-v4 only, withdrawn.)

## Logo
`IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com/cdn/shop/files (6135×1059 RGBA) →
`remotion/public/illumaesthetic_logo.png` (gitignored).

## Shots (tools/shots.py → tools/shot.py, renders in `/home/user/media/work/s2k/renders/final/`)
v5: s1_front, s2_rear, s3_lamp, s4_tail, s4b_flank, s5_front_open, s6_structure, s7_top, explode e1 (s8) / e2_side / e3_low / e4_hood / e5_fronthigh / e6 (s8) / e8_locked, logo card.
