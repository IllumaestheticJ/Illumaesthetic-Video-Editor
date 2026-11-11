# A90 Supra scan reel - sources

Temerario-style, scan only: no IRL footage. Media in `/home/user/media/a90-supra/` (raw) and
`/home/user/media/work/a90/` (decimated / prepped / renders). Nothing here is committed.

## Reference
- `v_jul22_1047_58` Temerario reel (Dropbox `/2. Illumaesthetic Videos/1. Video dumps/240SX scanning (completed)/Video Jul 22 2026, 10 47 58 AM.mov`).
  **Not watched**: the Dropbox download host is blocked by this environment's network policy (proxy 403).
  Worked from `training/references/README.md` + `v_jul22_1047_58.json` (39.8 s, one continuous move, mean luma 29.9).

## Scans - engineering Drive `Toyota A90 Supra` > `A90 Scans` (10TMq76ZjQ4ijl8ZXBqbd0JrHuWBy4Snd)
Raw frame: Artec mm, **+X = nose**, -Y = right side, Z up. Car 4,380 mm long (X), wheelbase 2.45 m measured
from the arch gaps (front arch centre x=+1.2 m, rear x=-1.25 m). **No wheels in any scan** (stripped car).

| File | Drive id | Tris | Used as | Registration |
|---|---|---|---|---|
| Chassis Trimmed (8.4m).stl (2026-09-29) | 1-0rDmVSKimu_SMFphT3_aNR2pChtHMHH | 8,332,792 | **base car** (4 mm full shots, 2 mm corner crops for close-ups) | defines the frame |
| Chassis_(8.4m).stl (2026-10-14) | 1wAw6utLKcGwAt2ryfaiq3z-mDyHUvcs7 | 8,400,496 | not used - same scan + ~5.7k tris of junk hanging under the rear arches | identical elsewhere (KD-tree diff) |
| Supra Front Bumper Outside / Inside | 1-HOV6RT... / 1jBrX6Jb... | 1.99M / 1.99M | exploded front bumper (union of both) | on the car skin, red-overlay check |
| Supra Rear Bumper Outside / Inside | 1_zR2NPi... / 1D5S8X1o... | 2.99M / 2.99M | exploded rear bumper (union) | red-overlay check |
| Supra Fender | 1iof_P7D... | 999,568 | exploded panel: lower-rear section of the right front fender | p50 2.1 mm to the car |
| Supra Under Fender | 1XwNwgsZ... | 1.99M | explode base: structure revealed under the fender | overlay check |
| Supra Under Fender Washer Bottle | 1cbg80U5... | 2.0M | checked, not used (overlaps Under Fender) | overlay check |
| Supra Under Front Bumper | 1S2nmZf3... | 3.99M | explode base: crash structure / radiators under the front bumper | overlay check |
| Liners Trimmed Fused (1.1m) | 1eXLTdRk... | 1.12M | explode base: arch liners | overlay check |
| 2021 trunk open / no bumper trunk closed / tail light only (+ all removed, Tail Light removed not fetched) | 1Msc2y0t... / 1MfGh43c... / 1MgpPUji... | ~5M each | **not used** | partial one-corner fragments; FPFH+RANSAC best fitness 5-8 % |
| Supra Trunk (2024): Supra Rear, Trunk Lid, Trunk Lid cover open 1/2 | 1OMGHi07... 1ObxkwsL... 1Og5bDGn... 1OjShiD_... | 2.2M / 1.3M / 0.6M / 0.19M | **not used in v1** (registered, see match/r24_T.json) | global reg rmse 4.4 mm, consistent 4/4 tries; "cover open" = small trunk-interior fragments, so no clean trunk-open state |
| Headlight/supra headlight_1, Headlight Lens (2025) | 13tgQpXc... / 1CNbuAer... | 9.4M / 6.6M | **not used** | global reg unstable (fitness 0.16/0.27) |

Bomex aftermarket CAD deliberately not used (brief).

## Other
- Logo: Drive `IllumaestheticLogoColor-01.png` (1cZJj521P88T_vC2YZDJVVUCctGyNoukR) -> `remotion/public/illumaesthetic_logo.png` (gitignored).
- Music: original, `tools/music.py` (numpy/scipy), no samples.
