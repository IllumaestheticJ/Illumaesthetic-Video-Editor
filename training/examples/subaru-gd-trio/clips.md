# Subaru Impreza GD trio (bugeye / blobeye / hawkeye) scan showcase — inputs

Scan only, no IRL footage. 1080x1920. Asked for by the user after the blobeye reel v3:
"video too long, focuses too long on the wrong things" / "illumaesthetic logo too small" /
"change music to rally house - do a showcase of all 3 GD scans (blob, hawk, bug)" / "have a director agent direct the 3-car showcase".

## Music
`/home/user/media/work/music/subaru-gd-trio_rallyhouse.mp3` (not in git). Original rally house instrumental generated for this
reel (Higgsfield, ElevenLabs Music v2.5), 28.03 s, 139.98 BPM: kick every 0.42862 s, first kick t0 = 0.058 s (resid 3 ms).
- beats 0-28 (0.06-12.06 s): full groove, kick on every beat
- beats 29-31 (12.49-13.35 s): break, no kick (3 beats)
- beat 32 (13.774 s): drop, louder section, kick on every beat through beat 60 (25.775 s)
- beat 61 (26.204 s) on: tail, music gone by ~27.5 s
Per-beat table: `/home/user/media/work/gd3/music_grid.txt`.

## Scans (engineering Drive), all 4 mm, all in ONE frame
Prepped frame: metres, nose -Y, car's right -X, ground z 0, car ~4.40 x 1.95 x 1.39 m. The hawkeye and bugeye were registered
onto the blobeye (same GD shell) and prepped `--like car4.json`, so one camera frames all three identically.
| Car | File | Drive id | Prepped | Registration to blobeye |
|---|---|---|---|---|
| Bugeye (2002-03) | Bugeye Full Car.stl (941 MB) | 1TK2Ja45H-mdcsUwVO1Q3qmvyqCr-q1Zz | /home/user/media/work/gd3/prep/bug4.blend | FPFH+RANSAC+ICP, 76 % overlap, p50 2.4 mm |
| Blobeye (2004-05) | Blobeye Full Car.stl (1151 MB) | 1-4YmtPLhY5WR5MOA4Rj5O193MN3cgQsC | /home/user/media/work/gd3/prep/blob4.blend (= sti/prep/car4.blend) | reference |
| Hawkeye (2006-07) | Hawkeye Full Car.stl (1267 MB) | 1-6z6sjrNKPkje1N4Avc5ZlYbQsAvsEXY | /home/user/media/work/gd3/prep/hawk4.blend | FPFH+RANSAC+ICP, 84 % overlap, p50 1.5 mm |

What differs between the three (seen in `/home/user/media/work/gd3/chk/trio.jpg`: rows front 3/4, nose, rear 3/4; columns bug, blob, hawk):
- Face: round bugeye lamps + mesh grille; blobeye teardrop lamps; hawkeye slim lamps + three-part "jet intake" grille.
- Front bumper and hood scoop shape differ on each. Roof, doors, glass are the same shell.
- Rear: the bugeye scan has NO wing (plain trunk lid) and 5-spoke wheels; blobeye and hawkeye have the tall STI wing; the hawkeye
  also has a roof vane spoiler and different tail lamps.
- Scan quality: grille/intake openings are open holes in blob and hawk; the hawkeye front-right wheel arch has a stray fragment.

Also on the Drive (not fetched): `Hawkeye engine Bay.stl` (500 MB). Blobeye state scans: see projects/subaru-sti-blobeye/clips.md.
Fenderist "Impreza GD Bugeye" fender STLs are aftermarket CAD, not scans - not used.

## Reusable blobeye renders (15 fps PNG, 810x1440, house look) in /home/user/media/work/sti/renders/final/
s1_front34 (front 3/4 turntable, 72 f), s2_rear34 / O1_open (rear 3/4 orbit, 48 f), s3_wheel (24 f), s4_light (headlight -> scoop, 24 f),
s6_top (top-down, 71 f), s8_wing (24 f), R_wing (48 f), H_a (hood push, 30 f), E_bay (engine bay scan alone, 84 f), B_b (bumper-removed scan, 72 f).

## Render budget
Cycles CPU, ~25-33 s per frame at 810x1440 / 12 spp / 15 fps (one job at a time). 1 s of screen time = 15 frames = ~7 min.

Logo: `remotion/public/illumaesthetic_logo.png`. v3 blobeye logo was 280 px wide and the user called it too small.
