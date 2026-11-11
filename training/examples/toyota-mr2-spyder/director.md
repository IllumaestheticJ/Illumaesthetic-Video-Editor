# MR2 Spyder v3 shot plan (director, 2026-11-11)

Keeps the scene order of `direction.md` (nose -> roof -> tail, each section once). Applies the v2 brief and user
feedback A-D. Reel = 33.64 s at 30 fps (music `start: 3.155`, see direction.md section 3). Cut frames are
round(reel_t * 30) on the kick grid; plain concat (`projects/honda-s2000/tools/concat_assemble.py`, `frames:` per clip).

## Shot table

| section | shot | slot (reel s) | frames @30 | focus | camera | part action (shot fraction t / beat) | why it earns its seconds | source |
|---|---|---|---|---|---|---|---|---|
| whole car | s1_wide | 0.000-4.286 | 129 | the whole hardtop car | low side profile, slow drift toward the nose (as rendered) | none; `fade=t=in:st=0:d=1.0` | whole car, motion from frame 1, 66-69 % width with margins | **reuse** f0001-f0054, `src_fps: 12.05` |
| wheels | s4_wheel | 4.286-6.428 | 64 | front wheel + arch | as rendered; cut on strong hit 7.441 (music) | none | the one extreme close-up; front corner before the front opens | **reuse** f0001-f0036, `src_fps: 15.7` |
| front (HERO) | s12_front | 6.428-12.857 | 193 | the front with the bumper off, then the front compartment | front-left, pushes in and rises 12 -> 44 deg el, lens 50 | bumper slides out toward the lens-left into black (t .04-.30), hood swings up on its fitted hinge (t .50-.74, starts n 24) | feedback C hero: what is behind the bumper, held 6.4 s with labels | **NEW** 80 fr @12 fps |
| side + top | s13_top | 12.857-19.285 | 193 | hardtop off -> roof-down cabin | -X side at the door line, cranes up 28 -> 66 deg el, az drifts 12 deg only | hardtop lifts straight up out of the top of frame (t .08-.34); hidden from t .45 | the only top/cabin scene; clean 1.15 mm roof-down data | **NEW** 80 fr @12 fps |
| rear | s14_rear | 19.285-25.714 | 192 | tail, then the open engine bay | rear-left 3/4, push then crane 16 -> 50 deg el | lid swings up on its hinge (t .333-.60, starts ON strong hit 24.583) | the only rear scene: tail detail + lid + bay | **NEW** 80 fr @12 fps |
| whole car | s15_reassemble | 25.714-30.535 | 145 | the car closing up | wide rear-right 3/4, 30 -> 46 deg az, 26 -> 12 deg el | bumper back .02-.30, hood shut .06-.36, hardtop drops in .18-.55, lid shut .34-.62, clean car2 from .68; `fade=t=out:st=4.38:d=0.45` | Temerario reassembly + fade; new angle (not opener, not rear scene) | **NEW** 61 fr @12 fps |
| - | logo | 30.535-33.635 | 93 | small logo | - | - | final hit | reuse `logo_card_v2.mp4` |

Frames: 129 + 64 + 193 + 193 + 192 + 145 + 93 = 1009. New-shot `src_fps = (N-1)/(slot + 0.1)`: s12/s13/s14 = 12.1, s15 = 12.2.

## Shot specs (drop into shots.py; same conventions: az 0 = behind (-Y), 180 = in front, -90 = camera on -X; t = shot fraction, smoothstep between keys unless `lin`)

```python
FB_OUT   = [-0.38, 1.00, -0.08]          # bumper parked in black, ahead of the nose and toward the lens-left
HOOD_UP  = H_HOOD["open_deg"] * 0.9       # 53.07 deg (same as v2 OPEN)
LID_UP   = H_LID["open_deg"] * 0.9        # -59.43 deg
TOP_UP   = [0, -0.10, 3.0]                # out of the top of frame in s13
TOP_HIGH = [0, 0.0, 7.5]                  # out of frame at s15 dist 8.2 (portrait half-height ~6.6 m)
FRONT_OPEN = {"fb": {"off": FB_OUT}, "hood": {"off": [0,0,0], "deg": HOOD_UP}}
R12 = {"fps": 12, "persistent": False}

# 3 FRONT HERO (12 beats). Hardtop ON, lid shut.
shot("s12_front", 6.70, EXP, [
    dict(t=0,    az=-152, el=12, dist=4.2, target=[0, 1.35, 0.55], lens=50),
    dict(t=0.30, az=-158, el=18, dist=3.8, target=[0, 1.45, 0.50], lens=50),   # bumper clear: look into the opening
    dict(t=0.50, az=-162, el=26, dist=3.3, target=[0, 1.35, 0.55], lens=50),
    dict(t=1,    az=-170, el=44, dist=2.7, target=[-0.15, 1.15, 0.60], lens=50)],  # down into the front compartment
  {"fb":   [dict(t=0, off=[0,0,0]), dict(t=0.04, off=[0,0,0]), dict(t=0.30, off=[-0.30, 0.80, -0.05]),
            dict(t=0.62, off=FB_OUT, lin=True), dict(t=1, off=FB_OUT)],
   "hood": [dict(t=0, off=[0,0,0], deg=0), dict(t=0.50, off=[0,0,0], deg=0), dict(t=0.74, off=[0,0,0], deg=HOOD_UP),
            dict(t=1, off=[0,0,0], deg=HOOD_UP)],
   "top":  [dict(t=0, off=[0,0,0])], "lid": [dict(t=0, off=[0,0,0], deg=0)]},
  light_ref="base", extra=R12)

# 4 SIDE + TOP (12 beats). Front stays open.
shot("s13_top", 6.70, EXP, [
    dict(t=0,    az=-70, el=28, dist=3.4, target=[0, -0.25, 0.95], lens=40),
    dict(t=0.45, az=-74, el=40, dist=3.3, target=[0, -0.28, 0.85], lens=40),
    dict(t=1,    az=-82, el=66, dist=3.0, target=[0, -0.30, 0.55], lens=40)],
  {"top":  [dict(t=0, off=[0,0,0]), dict(t=0.08, off=[0,0,0]), dict(t=0.34, off=TOP_UP), dict(t=1, off=TOP_UP)],
   "fb":   [dict(t=0, off=FB_OUT)], "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP)],
   "lid":  [dict(t=0, off=[0,0,0], deg=0)]},
  light_ref="base", extra=dict(R12, visible={"top": [0, 0.45]}))

# 5 REAR (12 beats). Lid starts ON the strong hit (t = 4/12).
shot("s14_rear", 6.70, EXP, [
    dict(t=0,     az=-38, el=16, dist=3.6, target=[0, -1.55, 0.70], lens=40),  # tail lamps + grilles fill the width
    dict(t=0.333, az=-32, el=20, dist=3.3, target=[0, -1.50, 0.72], lens=40),
    dict(t=1,     az=-22, el=50, dist=2.8, target=[0, -1.20, 0.75], lens=40)], # down into the engine bay
  {"lid":  [dict(t=0, off=[0,0,0], deg=0), dict(t=0.333, off=[0,0,0], deg=0), dict(t=0.60, off=[0,0,0], deg=LID_UP),
            dict(t=1, off=[0,0,0], deg=LID_UP)],
   "fb":   [dict(t=0, off=FB_OUT)], "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP)], "top": [dict(t=0, off=TOP_UP)]},
  light_ref="base", extra=dict(R12, visible={"top": [0, 0]}))

# 6 REASSEMBLY (9 beats) -> clean car, fade in assembly.
shot("s15_reassemble", 5.05, dict(EXP, **CAR), [
    dict(t=0, az=30, el=26, dist=8.2, target=[0, 0.10, 0.80], lens=40),
    dict(t=1, az=46, el=12, dist=7.0, target=[0, -0.05, 0.60], lens=40)],
  {"fb":   [dict(t=0, off=FB_OUT), dict(t=0.02, off=FB_OUT), dict(t=0.30, off=[0,0,0]), dict(t=1, off=[0,0,0])],
   "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP), dict(t=0.06, off=[0,0,0], deg=HOOD_UP), dict(t=0.36, off=[0,0,0], deg=0),
            dict(t=1, off=[0,0,0], deg=0)],
   "top":  [dict(t=0, off=TOP_HIGH), dict(t=0.18, off=TOP_HIGH), dict(t=0.55, off=[0,0,0]), dict(t=1, off=[0,0,0])],
   "lid":  [dict(t=0, off=[0,0,0], deg=LID_UP), dict(t=0.34, off=[0,0,0], deg=LID_UP), dict(t=0.62, off=[0,0,0], deg=0),
            dict(t=1, off=[0,0,0], deg=0)]},
  light_ref="base", extra=dict(R12, visible={"base": [0, 0.68], "fb": [0, 0.68], "hood": [0, 0.68], "lid": [0, 0.68],
                                             "top": [0.12, 0.68], "car": [0.68, 1.01]}))
```

Render check before the full run (`--res-pct 30 --samples 8 --frames` first/middle/last + t .30/.60): feedback A on each.
- s12: bumper must stay whole in frame until it leaves by the bottom/left edge in one move; if it hangs half-clipped at
  t 1, extend FB_OUT to [-0.6, 1.4, -0.1] (and use the same FB_OUT in s13-s15). The ragged lower nose must sit at the bottom
  of frame, not centre; if black holes fill the middle at t .3, raise el at t .30 to 24.
- s13: front parts must not poke into the frame edges at t 0 (if they do, target y -0.35). Hardtop gone by t .45.
- s14: plate stays blank (it is in s5); open hood must not clip at a frame edge (it should be outside the frame).
- s15: whole car + bumper + falling hardtop in frame with >= 60 px margins on first, middle and last frame.
- Every render: per-frame mean-luma scan (persistent data off already).

## Labels (Remotion ScanHUD, JetBrains Mono caps, off-white #e8ecf2, one item at a time, top-left x 80 px / y 200 px of
1080x1920; check they sit on black, outside the silhouette, on the s12/s13/s14 test frames)

| text | shot | in (reel s / music n) | out (reel s / music n) | support |
|---|---|---|---|---|
| FRONT BUMPER REMOVED | s12 | 7.500 / n20 | 9.643 / n24 | Hood Duct Data (bumper off, 2.0 mm) |
| HOOD OPEN | s12 | 10.178 / n25 | 11.250 / n27 | Hood Duct Data (hood open) |
| STRUT TOWER | s12 | 11.250 / n27 | 12.589 / n29.5 | strut top mount visible in the opened front (s7a f36 crop) |
| HARDTOP REMOVED | s13 | 15.535 / n35 | 17.142 / n38 | Full Car Top Down |
| ROLL BAR (only if confirmed on the s13 end frame) | s13 | 17.410 / n38.5 | 19.017 / n41.5 | tube hoop behind the seats in the roof-down scan |
| REAR LID OPEN | s14 | 21.964 / n47 | 23.571 / n50 | Rear End trunk open (1.45 mm) |
| ENGINE BAY (confirm on the s14 end frame, else omit) | s14 | 23.571 / n50 | 25.446 / n53.5 | engine visible under the lid |

No labels on s1_wide, s4_wheel, s15 or the logo. No numbers.

## Cut list (v2 -> v3)
- s2_front34: nose clipped at the left edge f1-60; turntable. s3_rear34: turntable, clipped both ends; rear repeats REAR.
- s5_tail: hardtop on, cannot follow the hardtop removal; its tail view is now s14 t 0-.33.
- s6_hardtop: front closed after the front has opened; nose clipped f68.
- s7a + s9a, s7b + s9b: same section twice each (and s7b clips the open hood at the right edge) - merged into s12 / s14.
- s8_top: rotating top-down, repeats every section. s10_float: bumper clipped left on every frame, repeats every part.
- s11_reassemble: ends on the opener-family front 3/4; clipped bumper at the start.

## Hold list (> 0.75 s with little part motion)
- s1_wide 0-4.29 s: whole car, 1 s fade + slow drift; the opener, nothing to cut to yet.
- s12 t .74-1 (1.7 s): hood is up and still; camera keeps craning down into the compartment while STRUT TOWER reads.
- s13 t .45-1 (3.5 s): parts still; camera crane from door line to top-down cabin is the content (HARDTOP REMOVED / ROLL BAR).
- s14 t 0-.333 (2.1 s): lid shut; camera pushes on the tail lamps/grilles (the rear exterior, replaces s5) until the strong hit.
- s15 t .68-1 (1.5 s): clean car settles and fades - the end hold; keep it no longer.
- logo 3.1 s (unchanged).

## Render budget
- New: s12 80 + s13 80 + s14 80 + s15 61 = **301 frames** at 12 fps (75 %, 12 spp) = ~60-70 min, one at a time.
  This is ~20 % over the 250-frame guide; 12 fps instead of 15 is what keeps it near one hour.
- Reused unchanged: s1_wide f0001-0054, s4_wheel f0001-0036, logo_card_v2.mp4.
- If the budget is hard-capped at 250: render s13 and s14 as 8 beats (6.70 -> 4.55 s, 55 frames each; s14 lid at t .25)
  and start the music at n 14 (7.441 s, opener fades up on the strong hit): 80 + 55 + 55 + 61 = 251 frames.
