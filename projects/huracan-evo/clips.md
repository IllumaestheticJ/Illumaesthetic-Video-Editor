# Huracan Evo scan reel (Temerario style) - sources

No IRL footage in this reel (scan only, no text) - brief: "Temerario-style scan reel".

## Reference
| id | source | notes |
|---|---|---|
| temerario | Dropbox `/2. Illumaesthetic Videos/1. Video dumps/240SX scanning (completed)/Video Jul 22 2026, 10 47 58 AM.mov` | 1440x1920 24 fps h264 SDR, 39.8 s, **no audio**. Timeline read from 1 s contact sheets (see training/references/README.md addendum) |
| oct31 | same folder, `Video Oct 31 2026, 1 30 46 PM.mp4` | approved 240SX IRL reel - **music source** (95.7 BPM, 22.75 s), same track the 240SX scan reel used |

## Music
**Final: `/home/user/media/work/music/reel_track_a.mp3`** (not committed) - generated for these reels by the parent session
after the user asked to "generate music that matches the beat"; 40.05 s, kick-peak grid t = 0.0768 + 0.60006*k (100.0 BPM).
Sections measured: pads/sub/pulse to 18.1 s, one dropped kick at 18.68 s, lift at 19.28 s (bar k=32, RMS +12 %), last kick
36.08 s, reverb tail to 40.05 s.
Superseded: Oct 31 approved-reel track extended to 32.855 s (`/home/user/media/huracan-evo/music/huracan_music.wav`) - Dropbox
had no other music (audio search = DJI field mics only).

## Car-select intro (user request: open like the NFS Hot Pursuit 2010 car-select - roar + female narrator reading the spec sheet)
Mixed by `tools/mix.py` into `/home/user/media/huracan-evo/vo/soundtrack_v1.wav` (project music). Generated on Higgsfield:
- `vo/engine.mp3` - Mirelo SFX, 6 s generic V10 start + revs (generated, NOT a recording of this car).
- `vo/narration2.wav` - Seed Audio, preset female voice "Imogen" (3811e986-...), 16.1 s. The game's narrator voice was
  NOT cloned (real voice actor, no consent) - same delivery style, different voice. Take 1 (`narration.wav`, speech_rate -12)
  ran 40 s with 2-4 s pauses - rejected.
Script (original, specs = Lamborghini's Jan 2019 Huracan EVO press release figures, AWD car assumed):
"Lamborghini Huracan EVO. Naturally aspirated five-point-two-litre V10, six hundred and forty horsepower, all-wheel drive.
Zero to one hundred in two-point-nine seconds, top speed three hundred and twenty-five kilometres per hour. Every panel,
scanned. Twenty-five million triangles."  (25M = Full Car STL header 24,999,942.)

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
