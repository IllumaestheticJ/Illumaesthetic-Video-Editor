# Huracan Evo scan reel (Temerario style) - sources

No IRL footage in this reel (scan only, no text) - brief: "Temerario-style scan reel".

## Reference
| id | source | notes |
|---|---|---|
| temerario | Dropbox `/2. Illumaesthetic Videos/1. Video dumps/240SX scanning (completed)/Video Jul 22 2026, 10 47 58 AM.mov` | 1440x1920 24 fps h264 SDR, 39.8 s, **no audio**. Timeline read from 1 s contact sheets (see training/references/README.md addendum) |
| oct31 | same folder, `Video Oct 31 2026, 1 30 46 PM.mp4` | approved 240SX IRL reel - **music source** (95.7 BPM, 22.75 s), same track the 240SX scan reel used |

## Music
`/home/user/media/huracan-evo/music/huracan_music.wav` = oct31 audio, `[0, 15.697)` + `[5.596, end]` (16 beats repeated,
12 ms crossfade on measured onsets) = 32.855 s. `ive beats` grid unbroken across the splice (beat 20 lands at 15.697).
Dropbox has no other music: an audio search only finds DJI field-mic WAVs (Corvette, Fuji Speedway).

## Scans (Drive `Lamborghini Huracan` / subfolder named **"Huracan Evo Spider"**, all dated 2026-08-31, one Artec frame)
| file | tris | what it is |
|---|---|---|
| Huracan Evo Full Car (1c5joOWEq...) | 24,999,942 | full car incl. ground; levelled + cropped -> car.blend (3 mm) |
| All Parts Removed (1bQaV0Iz...) | 9,000,003 | body with bumpers / skirts / fender / cowls removed - exploded-view base |
| front bumper (1bvo0tN5...) | 4,000,015 | front bumper skin |
| Rear Bumper (1bb8Dd8A...) | 7,999,727 | rear bumper |
| Side Skirts (1bjB2dg9...) | 3,999,953 | one side only (-X = car's right) |
| Fender (1bcStx15...) | 4,000,001 | one front fender (-X side) |
| Hood Only (1KVMHkfA...) | 4,999,999 | hood, closed position |
| top / left / right cowl | 4.37M / 1.26M / 3.61M | under-hood cowl panels; register to "Hood Open Cowl Exposed" |
| Hood open, bumper off, fender on (1bXAucyq...) | 6,000,027 | front-end state scan |
| Front End No Bumper Hood Open (1boFEAz2...) | 6,000,041 | front-end state scan |
| Front Wheel Wells (1bQSEAfC...) | 5,000,062 | wheel-well state |
| Hood Open Cowl Exposed (1cHbXkZ1...) | 5,000,013 | extra state (not in brief, same folder/date) |
| Side Skirt, Bumper, Cowl Mounting REF (1c0ZX0kv...) | 6,999,988 | mounting reference state |

Registration: every part checked against the full car (tools/regcheck.py) - median 2.5-3.4 mm at 8 mm decimation, no
corrections needed. Overlays: `/home/user/media/huracan-evo/chk/reg_*.png`. The 2023 "(New)" folder was not needed.

## Frame conventions (after tools/level.py)
Ground = Z 0, nose at -Y, +X = car's left. Camera azimuth in tools/shot.py: 0 = in front of the nose, +90 = car's left (+X),
-90 = car's right (-X, the side the skirt/fender part scans exist for).
