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
Mixed by `tools/mix.py` into `/home/user/media/huracan-evo/vo/soundtrack_v2.wav` (project music). Generated on Higgsfield:
- `vo/engine.mp3` - Mirelo SFX, 6 s generic V10 start + revs (generated, NOT a recording of this car).
- Narrator: Seed Audio, preset female voice "Imogen" (3811e986-...). The game's narrator voice was NOT cloned (real voice
  actor, no consent) - same delivery style, different voice.
- v2 (`vo/narration4.wav`, car only - user: "don't talk about the scan, talk about the car"; "use the Huracan coupe"):
  "Lamborghini Huracan EVO Coupe. A naturally aspirated five-point-two-litre V10, six hundred and forty metric horsepower.
  All-wheel drive, rear-wheel steering. Zero to one hundred in two-point-nine seconds. Top speed: three hundred and
  twenty-five kilometres per hour."  Raw take 21.5 s (0.5-0.8 s pauses) -> pauses trimmed to 0.24 s + atempo 1.08 -> speech 1.31-18.0 s.
  Sources: Lamborghini media release 7 Jan 2019 (640 PS/470 kW at 8,000 rpm, 600 Nm, AWD + rear-wheel steering, LDVI),
  0-100 2.9 s / 325 km/h consistent across spec sites. 640 is PS, so the script says "metric horsepower".
- v1 (`vo/narration2.wav`) also said "Every panel, scanned. Twenty-five million triangles" - removed on feedback.
- Rejected takes: narration.wav (40 s, speech_rate -12), narration3.wav (24 s, longer script).

## Body: 2026 set = SPYDER, 2023 set = COUPE (corrected in v3)
Centre-line roof height, 250 mm bins nose->tail (mm):
- 2026 'Huracan Evo Spider' folder: 580 696 787 828 925 1024 1108 1164 1190 1197 1194 1178 **1025** 1001 987 946 904 941 - one-bin
  drop of 153 mm behind the cabin (soft top -> engine deck) = Spyder. (v2 wrongly called this the coupe - no coupe to compare.)
- 2023 'Huracan Evo Coupe Scan Data (New)' Full Car (1TtT2j6ZZPNjEIWPKbiRl2YgW_FFKcGka, 15M tris): 545 664 757 796 902 1003 1094
  1153 1172 1173 1169 1148 1103 1066 1027 985 927 955 - smooth glass fastback = coupe. Own levelling (level2023.json),
  2 mm, cropped, prepped standalone -> coupe2.blend. Unlike the 2026 scan its wheels ARE captured (spokes/rims read).

## NFSU2 car-lot reference (v3)
Dropbox `/5. Claude Training/Good Reels (Epsilon)/NFSU2 car lot - clean audio.mp4` (67 s) and `- 1440p.mp4` (110 s),
1206x2622 60 fps phone screen recordings of Need for Speed Underground 2.
- 10-31 s (clean): story cutscene, female narrator (the game's Rachel Teller, voiced by Brooke Burke) over music; voice band
  ~180-240 Hz, conversational/intimate delivery. Used as a STYLE reference only - no cloning.
- 34-54 s (clean): car lot - dark garage, car on a lit turntable platform, static elevated front-3/4 camera, car rotates;
  audio: dead air (34.5 s), sharp engine start (35.5 s: crank, bark, rev flare), idle, rev blips on each car swap.

## v3 audio (`tools/mix.py` -> `vo/soundtrack_v3.wav`)
- Music: reel_track_a with the groove (k32-k60) repeated once, spliced 60 ms before the kick peaks, 15 ms xfade ->
  `music/track_a_ext.wav` 56.85 s; kick grid unbroken (88 kicks, resid 5.5 ms median), music stops at 52.88 s.
- `vo/engine_start1.mp3` (6 s) at 0 s, `vo/engine_start2.mp3` (4 s) at 19.03 s so its catch lands on the 19.28 lift. Generated.
- `vo/narration5.wav` (preset 'Imogen', pitch -1): "Check this out. The Lamborghini Huracan EVO Coupe. Naturally aspirated V10,
  six hundred and forty metric horsepower, all the way to eight thousand RPM. All-wheel drive. Zero to a hundred in
  two-point-nine. Yeah... you're gonna want this one." Pauses -> 0.30 s, atempo 1.04, at 0.9 s -> speech ~1.1-18.3 s.

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
