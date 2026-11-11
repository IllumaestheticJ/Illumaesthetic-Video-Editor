# Scene direction - Lexus IS350 (plate 9JTY488) scan-process reel, v1 -> v3 revision

Stage 1 (scene-director). Format stays **240SX-style**: IRL -> 1:1 cut -> scan, twice, then x-ray -> listing.
This file covers which scan scenes exist and in what order. `director.md` gives the shot-by-shot plan.

What I looked at (contact sheets, not file names):
- `renders/s1_front` (60 f), `s2_rear` (90 f), `s3_xray` (68 f): 12-frame sheets plus full-res crops of S2 f1/f52 (reflector pocket) and S3 f68 / S1 f1.
- Match frames `match/f54_264.png` and `match/f42_1135.png`, with the v1 9:16 window (607.5 px of 1920) and a 1.6x window drawn on them.
- `out/is350_scan_process_v3.mp4` (1 fps sheet) and `out/webzoom_is350.mp4`.
- Music `music/is350_reel_d25.wav`: kick (40-120 Hz) and hat (2-4 kHz) energy on every grid beat n = 0.50004 n.

## 1. Feature inventory (this car only)

| Scan / region | What the render shows | Data | Richness |
|---|---|---|---|
| Full car `Lexus 4IS IS350 Full Car.stl` (24,999,992 tris, STL header) | whole car, levelled and cleaned, silver | 4 mm decimation for wide shots | base for every shot |
| **Front** | F Sport spindle mesh grille, scanned mesh by mesh (black holes only behind the mesh openings), headlights, corner vents, mirrors. Front-left wheel spokes captured | good, dense | **signature region**: richest exterior detail. Has the 1:1 IRL match (FX30554 f264) |
| **Side (+x side, all cameras are on this side)** | door handles, sills, trunk-lip spoiler tips, front wheel good. **Rear wheel is a ragged partial / mostly empty well** (S3 f68) | front half good, rear wheel weak | medium. Show it only while moving, never hold on the rear wheel |
| **Rear** | trunk lid, lip spoiler, plate (legible 9JTY488, same as the real plate in the IRL), diffuser fins, two exhaust tips, lower side vents | good | has the 2nd 1:1 IRL match (FX30542 f1135) and the only part data |
| Part: `Lexus 4IS reflector.stl` (408,984 tris) | rear reflector from the +x lower rear vent beside the exhaust. **Both faces scanned**: lens face, and a clip side with 3 mounting tabs (S2 f52 full res) | registered (spliced, editlog) | the only explode candidate. Its back is worth showing (tabs), so one half-turn is justified |
| State: `Lexus 4IS reflector removed.stl` (5,226,241 tris) | the empty vent pocket, spliced into the car by surface distance | **pocket has ragged black coverage holes** (S2 f52) | weak. Show the pocket small, at the top of the frame. Do not push in on it |
| States that do NOT exist for this car | no bumper-removed, hood-open, trunk-open or door-open scan. The `2026 IS350 Facelift` set is a different car (end card only, per user) | - | rules C/D: no removal section, no opening, no "BUMPER REMOVED" label |
| Top / engine bay / interior / underside | not captured as separate data. Sprayed glass is a closed shell | - | no scenes |

Richness: **front** (signature detail + match) > **rear** (match + the only part + state) > **side** (pass-through, weak rear wheel) > top/bay (none).

## 2. Scene order and why

The order of the IRL halves is fixed by the footage: the front match (walk-out, FX30554) opens and the rear match (crew scanning the rear, FX30542) comes second.
The end is fixed by the listing: S3 must land on the listing 360-viewer pose camP_L, a front-left 3/4 on the +x side at 9.25,-6.2,4.08.
With both ends fixed, the only order that shows every section once is:

**front (S1) -> [shop inserts] -> rear + reflector (S2) -> side, travelling forward to the whole-car hero (S3) -> listing.**

The scan camera makes **one lap of the +x side**: front, rear, then forward along the side to the front-3/4.
No section is shown twice.

Why not front -> side -> rear (the v1 S1 orbit turned toward the side):
- S1's 20 deg orbit swings from the grille toward the +x front 3/4. On the wider canvas its end frame would be close to the listing pose that ends the reel, which is a repeated view.
- S3 then crosses the same side again.

So S1 stays on the front only, and the side is shown once, inside the S3 swoop.

| # | scene | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | IRL walk-out (FX30554 f193-264) | - | the real powdered car, front | fixed opener. The real hit is on the drop | 6 (n0-6) | **widen the window**: full-height 16:9 window, W 1063 (1.75x v1; 972 = 1.6x also works), x0 ~385 so the car is centred. Measured car span x 500-1328 of 1920. Blurred fill above and below |
| 2 | **S1 front** | full car | spindle mesh grille, headlights, corner vents (one focus: the front fascia) | richest region, on the **drop** (n6, the biggest musical moment) | 8 (n6-14) | 1:1 from the wide crop camera, then a slow straight push. **No orbit.** |
| 3 | IRL spray (FX30549) | - | powder going on | process insert | 2 | reuse |
| 4 | IRL scanner screen (FX30547) | - | live scan on the scanner screen | process insert | 3 | reuse |
| 5 | IRL rear scan (FX30542 f1052-1135) | - | crew scanning the rear bumper | fixed 2nd match | 7 | **widen**: last window x0 0, W 1063 (pan from x0 ~857 -> 0). The car's far corner is cut off by the source frame itself, which is unavoidable |
| 6 | **S2 rear + reflector** | full car with the reflector-removed scan spliced in, plus the reflector part | the rear reflector, out of its vent: lens face, then its clip side | the only part and state of this car | 12 (n26-38) | 1:1 wide, then push down to the lower +x corner. The part drops into black below the bumper and makes **one 180 deg turn** to show the tabs |
| 7 | **S3 x-ray -> hero** | same base, reflector returns home | the reflector seats, then the **side** (one pass) and the whole car | the travel back along the side to the listing pose. Hero rung of the ladder | 8 (n38-46) | path from S2's last pose to camP_L. Morph to listing clay |
| 8 | Listing (WebZoom) | - | the IS350 scan listing, the 2026 bumper dataset, logo, URL | CTA | 9 (n46-54 + fade) | **hard 1:1 cut** on n46 (no dissolve) |

Ladder rungs left out on purpose, because there is no data for them:
- No bumper or panel removal.
- No hood or trunk opening.
- No top-down shot. The car's top is plain glass and roof, with no feature to show from above.
- No multi-part explode. There is only one part.

## 3. Music map (measured on the wav)

| n | time (s) | what it is | scene that starts |
|---|---|---|---|
| 0 | 0.000 | kick | IRL walk-out |
| 4-5 | 2.0-2.5 | kick break (the drop's 1-beat gap) | - |
| **6** | **3.000** | **drop** (kick back, hats +) | **S1 front: 1:1 cut** |
| 14 | 7.000 | phrase start | IRL spray |
| 16 | 8.001 | bar | IRL scanner |
| 19 | 9.501 | off-beat with a hat accent (kept from v1) | IRL rear scan |
| 26 | 13.001 | bar downbeat | **S2 rear: 1:1 cut** |
| 30 | 15.002 | phrase start (start of the repeated 16 beats) | reflector half-turn starts |
| 38 | 19.002 | phrase start (kick 18.1) | S3 x-ray |
| **46** | **23.002** | phrase start, **strongest kick in the reel (19.1)** | **listing: hard cut** |
| 50 | 25.0 | bar | WebZoom lands full width |
| 54 | 27.002 | last kick | music fades 0.6 s |

All cut points are kept from v1. The only change is that the ~23.0 s transition becomes a hard cut on n46 instead of a 0.5 s dissolve.

## 4. Diff vs the current timeline (v1/v3)

| scene | change | why | render |
|---|---|---|---|
| IRL walk-out | wider window on a 9:16 canvas with blurred fill | v1 clipped both mirrors and bumper corners. The director report flags its first frame as "too cropped" | **re-crop** (tools/irl.py, no Blender) |
| S1 front | 20 deg orbit -> straight push on the front fascia, from the wider 1:1 | the orbit turned toward the side and the listing pose, so it showed the side twice and nearly repeated the end. User: no wasted rotations | **re-render** (needed anyway for the wider canvas) |
| IRL spray, IRL scanner | none | full-bleed close-ups with nothing to widen | **reuse as-is** |
| IRL rear scan | wider window, pan ends on x0 0 | wider crop at the 1:1 (brief) | **re-crop** |
| S2 rear | wider 1:1 start, then a push in to the reflector corner. Part drops 0.25 m into black. 360 deg Z spin -> one 180 deg turn plus a hold on the clip side | v1's reflector was ~100-200 px and dipped out of the bottom edge (f36-44). The 360 deg spin spent a second turn showing nothing new | **re-render** |
| S3 x-ray | new start pose and part offset (= S2's new end). End pose camP_L and clay morph unchanged. 4.5 s -> 4.0 s | must start exactly where S2 ends. The dissolve overlap is gone | **re-render** (68 -> ~63 frames, one job) |
| x-ray -> listing | 0.5 s dissolve -> **hard cut on n46** | brief: "strong final cut into the listing". The frames are pixel-matched (0.3 px), so the cut reads as the house 1:1 device: the car stays and the page appears | assembly only |
| Listing | unchanged clip, now starts on the cut | zoom lands on n50, URL in by ~26.5 s, ends on the last kick + fade | **reuse as-is** |
| HUD | counter unchanged. Reflector labels re-timed and re-placed on black next to the part in the new S2 | the part's position changes | re-render Remotion overlay (cheap) |

Nothing is dropped and nothing is added. Total stays 27.57 s.

## 5. Open questions for the editor (none blocking)
1. Wide-window size: 1.6x (972 px) or your existing 1.75x (camW_A, 1063 px)? Both keep the whole front in. I planned for 1063, re-centred to x0 ~385, because camW_A's x0 434 leaves 66 px on the left and 169 px on the right.
2. The spray and scanner inserts stay full-bleed between the two blurred-fill IRL shots. If that mix looks inconsistent on the sheet, put them on the same canvas too. That is an editor's call; it does not affect timing.
3. The scan plate reads 9JTY488 in S1 and S2. The real plate is on screen in both IRL shots anyway, so there is no deplate pass unless the user asks for one.
