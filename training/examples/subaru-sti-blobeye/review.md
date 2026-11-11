# Self-review — Subaru Impreza STI GD "blobeye" scan reel (v2)

Deliverable: `/home/user/media/work/sti/out/subaru_sti_blobeye_v2.mp4`. 1080×1920, 30 fps, 39.23 s, scan only, with labels only on the bumper-removed hero.

Order (one way round the car, rear → side → front): whole-car rear 3/4 orbit → wing lifts off over the wing-off trunk scan → left skirt drops off over the "sideskirt removed" sill → front-left wheel → hood lifts off into a held descent over the engine-bay scan → **front bumper off, camera pushes into the intercooler core and slides to the piping (hero, 8 s, two labels)** → exploded state (all four removed parts) → staggered reassembly → fade → small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car with motion from frame 1 (v1 s2 rear orbit reused). The first transformation (wing off) comes at 3.2 s. |
| 2 | Beat sync | 5 | All 8 cuts were measured on the DECODED audio of the delivered file. Each sits 7–11 ms before a kick attack, under half a frame (16.7 ms). The v1 152 BPM grid was wrong: the track is 150 BPM, a kick every 0.400 s. The cuts were re-snapped after the first v2 assembly measured 65–125 ms off. |
| 3 | 1:1 match | n/a | No IRL footage in this brief. Panels seat exactly by construction (carved from the full car). |
| 4 | Scan quality | 4 | Registered state scans sit under every removed part (wing-off rear 1.7 mm, sill 2.1 mm, engine bay 1.6 mm, bumper/hood-removed about 2 mm p50). Minor: thin wiper/antenna slivers near the cowl in the wheel and bumper shots, and scan speckle on the glass. |
| 5 | Story | 5 | Progressive disassembly. Each section appears in one continuous sequence, and removed parts stay removed. Only states with registered scans are shown: the hood lifts OFF (no hood-open scan) and the trunk/doors stay shut (no open-state data). |
| 6 | Grade | 5 | One look throughout: AgX at −0.5 EV, satin silver on black. Every shot passed the per-frame luma dropout check (min/neighbour ≥ 0.96). |
| 7 | Text | 5 | Labels appear only on the hero: "FRONT BUMPER REMOVED / FRONT-MOUNT INTERCOOLER" and "INTERCOOLER PIPING / BUMPER-REMOVED SCAN". They sit on black below the subject, with no numbers. The first label enters on the 25.24 s kick. |
| 8 | Ending | 4 | Exploded state 1.6 s, then reassembly with the last lock on a kick, a fade 34.01–34.80, and a 280 px logo from 35.2 through the final hit to silence. The logo hold of about 4 s covers the music tail. |
| 9 | Technical | 5 | yuv420p, AAC, faststart. Persistent data was off for every moving shot. The only repeated frames are the assembler's 1-frame cut holds, with no tail freezes (src_fps slack). |

## Director report
- No dead seconds in any scan clip, and every clip carries section/focus tags.
- One flag, **S2_wing ~ S5_hood (IoU 0.90)**. This is a false positive: the frames compared are the rear end-on (trunk lid, wing off) and the front end-on (hood and scoop). The silhouettes mirror each other but the sections differ (rear vs engine) and the content differs, so I kept both.

## Framing checks (addendum A)
- First/mid/last contact sheets were checked for every shot.
- Three shots were re-rendered after the check:
  - S3 had a black lower half and a stray parked skirt.
  - S7a had the hood and car tail clipped at the right edge, then the cluster too small.
  - S7b started with the bumper touching the left edge.
- The parked wing in S6 frames 1–57 was painted out (tools/mask_top.py).

## Known weaknesses
- The S1 opener is v1's render. The car is small (about 55 % width) with the wing as the subject; a tighter re-render (r 4.6 m) would hook harder.
- The S7a exploded state is still a wide 9:16 frame of a long cluster, with black above and below. A vertical stack layout for parked parts would fill portrait better.
- The S4 wheel shot is only 1.6 s, the shortest section.

## Data honesty
- Every panel comes from our scans: hood, bumper, wing and skirt carved from `Blobeye Full Car.stl`.
- Openings show the `bumper removed`, `hood removed`, `GD Scan Engine Bay`, `Rear Wing data` and `Sideskirt removed` scans as captured, registered with box-ICP and pinned with `--like car4.json`.
