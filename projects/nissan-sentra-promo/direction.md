# Sentra promo — direction (v1)

Format: scan-data promo (`knowledge/promo-script-template.md`), 1080x1920, 30 fps, voice only (owner: NO music),
white caption bubble (`PromoCaption`). Script approved 2026-11-14 (`script.md`). Line windows: `timing.json`
(built by `tools/voice.py` from the voice take).

## Frame
Everything is rendered in the **design frame** of the team's review file `Sentra Review 3.blend` (front at -Y, +X = driver /
left side, ground z = -38.6 mm, level to 0.25 deg). The raw Artec scans map into it with that file's matrix for
`Bumper Removed (Headlights Back On)` (`M_br_rough.json`); the SEMA CAD STLs are already in it (trimmed ICP of all CAD
onto the car moves only 3 mm / 0.27 deg -> applied nothing). Brake parts come from `Sentra_Brakes_Review.blend`
(hub captured on the lift: suspension drooped ~115 mm, so the brake beat is its own close-up, not placed in the car).

## Feature inventory used (all files on the engineering Drive)
| Beat | Data |
|---|---|
| hero car | `Nissan Sentra SR.stl` (quadric-simplified to 6 M tris, ground + debris islands removed) |
| engine bay | `Senta SR Sentra Engine Bay.stl` (hood propped open, registers onto the car with the same matrix) |
| fog lights | `Sentra Fog 1.stl`, `Sentra Fog 2.stl` (bench scans of the rectangular lamps) |
| stock bumper off | `Senta SR bumper only.stl` + base `Senta SR Bumper Removed (Headlights Back On).stl` |
| SEMA parts | `STL/` Uncut_* : front bumper, fog/duct side inserts (Sep 16 reprint), front fenders, hood ducts x3, side skirts, rear QP (rear door + rear fender + rear bumper sides), diffuser, wing adapter |
| brake adapters | FR: `STL (to test fit)` Sep 2 -> `V3 (Sep 13)` -> `V4 (Sep 16)` on `Senta SR FR Hub` + `Front Rotor` (+ `Front Caliper`) |
| not used | 2022-23 headlight scans (owner: different car); interior console; rear state scans (no line for them) |

## Shots (one continuous scan camera from the 1:1 cut to the brake close-up)
| # | Window (s) | Line | Picture |
|---|---|---|---|
| IRL | 0-4.33 | let's build a 2026 nissan sentra SR | SEMA show clip of the finished car, voice only, no caption |
| A | 4.33-12.1 | using nothing but scan data / but to make parts... / you need the real car | HARD 1:1 cut to the same perspective, empty black. The SEMA front fender drops in where it sits on the real car, settles, turns slowly; a scan line sweeps the void and the fender lifts away |
| B | 12.1-15.3 | so first, we scan the whole car | the full-car scan builds up from the ground behind a rising scan line |
| C | 15.3-16.9 | every body line | push along the side |
| D | 16.9-18.6 | every panel gap | close on a real gap (hood/fender/headlight) |
| E | 18.6-21.6 | then the engine bay, on its own | engine-bay scan (hood open) drops into place over the front |
| F | 21.6-23.3 | and the fog lights | the two fog-lamp scans fly in and park in front of the nose |
| G | 23.3-25.4 | now we design on top of it | pull back, car turns |
| H-N | 25.4-37.1 | bumper / fog ducts / fenders + hood / skirts / rear QP / diffuser / wing | one travelling move front -> side -> rear, one part group per line |
| O | 37.1-41.2 | even the brake adapters / revised until they fit | hub close-up: test-fit adapter slots on, steps to V3, then V4 |
| P | 41.2-43.4 | this is the sentra scan data | finished build orbit |
| logo | 43.4-47.0 | get it on illumaesthetic.com | ILLUMAESTHETIC logo card (~720 px) |
