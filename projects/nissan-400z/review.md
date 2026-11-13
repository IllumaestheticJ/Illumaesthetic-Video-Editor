# Nissan 400Z scan reel — v3 self-review (2026-11-12)

Output `/home/user/media/work/out/nissan_400z_scan_v3.mp4`: 1080x1920, 30 fps, h264 yuv420p, AAC, 1320 f (44.00 s).

## User feedback on v2 → v3 changes
- **"Logo needs to be bigger"**: card logo 340 → 640 px wide, fades in on the 41.172 kick, ends on the 44.03 phrase.
- **"Side mirror coming off took a part of the window with it"**: the parts.py diff had flagged door-glass triangles
  (|x| 765–783 mm; glass scans differently between sessions) as mirror. Fitted the glass plane, dropped everything within
  8 mm / inboard from both mirror parts, rebuilt comp_explode with the trimmed parts, re-rendered N2 and s8b. Checked: the
  mirror lifts off alone, the window stays on the door.
- **New music (album audio from 19:50)**: 128 BPM, 14 s quiet intro, drop 14.031. Intro = N0 (7.27 s) + H (6.7 s), both
  re-rendered with longer moves; bumper-off hero on the drop; cuts on measured half-rise onsets.
- Also: N2 re-rendered at native 30 fps (minterpolate left ghost trails on the fast mirror); s8b re-render cleared its old
  dark f101-112 tail.

## Cut timing (cutcheck, broadband half-rise)
219 −11 ms vs the 7.311 intro kick (cutcheck's ±120 ms window picks a stronger non-kick hit at 7.194) · 420 −3.6 · 534 +10.8 ·
701 +3.6 · 785 −14.7 · 870 +12.5 · 1010 −5.2 — all within ±½ frame.

## Scores (1–5)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 3 | Quiet 14 s intro (user's music choice); car orbits under the fade from frame 1, but the first big moment is at 14 s |
| 2 | Beat sync | 5 | 7/7 hard cuts within ±½ frame |
| 3 | 1:1 match | N/A | scan only |
| 4 | Scan quality | 4 | mirror/glass fixed; bay and radiator capture noise is real; N2 wheel spokes have scan holes |
| 5 | Story | 4 | unchanged section order, hero on the drop |
| 6 | Grade | N/A | |
| 7 | Text | 5 | two factual labels over scan only |
| 8 | Ending | 4 | reassembly locks near the 37.43 kick, fade, bigger logo on 41.17, ends on the phrase at 44.03 |
| 9 | Technical | 5 | spec correct, no dark/dup frames at cuts, no interpolation ghosting on N2 |

## For the next agent
- parts.py diffs pick up glass/trim that scanned differently between sessions; fit and strip the glass plane before using a
  door-mounted part, and look at the part alone from the side before rendering.
- Fast small parts ghost under minterpolate: render those shots at native 30 fps.
- s5_tail -> N3 still joins two close badge framings (see v2 notes).

---

# Nissan 400Z scan reel — v2 self-review

Output: `/home/user/media/work/out/nissan_400z_scan_v2.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p, AAC, 1151 frames (38.37 s).
Scope: scan-only Temerario-style reel. There is no IRL footage, so criteria 3 and 6 are N/A.

## What changed from v1
These changes follow the v2 brief and addendum A–D relayed from the user.

- **Order, from scan features (direction.md and director.md):**
  1. Whole car.
  2. Engine bay, from the real Hood Open scan.
  3. Front bumper removed: grille out, then shell out. This is the hero section.
  4. Structure, from the 2 mm "Bumper and hood removed" scan, with two labels.
  5. Right mirror off.
  6. Tail detail.
  7. Wing off.
  8. Reassembly.
  9. Fade to black, then a small logo.

  Travel runs front → side → rear with no ping-pong, one sequence per section, and no reused shots.
- **Removed or opened states:** each one is shown only from its own registered scan. There is no animated hood opening and no trunk shot, because there is no trunk scan.
- **Labels:** exact wording, over scan shots only.
  - FRONT BUMPER REMOVED / SCAN: BUMPER AND HOOD REMOVED
  - CRASH BEAM / BEHIND THE FRONT BUMPER, shown over the visible beam
- **Renders:** persistent data was off for every new shot.
- **Luma dropout check:** every new shot is clean. The s8b reused render has a dark tail at frames 101–112; it is unused and faded to black (logged).
- **Cut timing:** measured against the decoded audio with the broadband 1 ms RMS half-rise (`tools/cutcheck.py`).

  | Cut frame | Offset (ms) |
  |---|---|
  | 112 | +12.3 |
  | 222 | −11.1 |
  | 333 | −5.1 |
  | 499 | −9.5 |
  | 579 | −15.9 |
  | 665 | −13.7 |
  | 801 | +1.6 |

  All are within ±½ frame (16.7 ms). The first assembly had five cuts at 17–28 ms, all one frame off; I retimed N0, H and N3.
- **Framing (first, middle and last frame of every shot):**
  - N3: the wing left the top of the frame for about 2 s, so the lift was reduced. Its left tip was then clipped at the end of the shot, so the end camera was widened from f35 to f27.
  - N0: the whole car stays in frame from the first frame.

## Scores (1–5)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | The car is orbiting under a 1.2 s fade-in; motion is visible by about 0.6 s. A fade-in, not a hard open. |
| 2 | Beat sync | 5 | 7/7 hard cuts within ±½ frame of the measured onset. |
| 3 | 1:1 match | N/A | No IRL footage in this reel. |
| 4 | Scan quality | 4 | Silver on black. Scan noise in the bay and on the radiator is real capture, not cleaned. The N2 wheel spokes show scan holes. |
| 5 | Story | 4 | Whole car → bay → bumper off → structure → mirror → rear → wing → reassembly. Bumper-removed data is the hero section and is labelled. |
| 6 | Grade | N/A | Scan only. Uniform ×0.955 gain. |
| 7 | Text | 5 | Two labels, factual, no numbers, over scan only. Legible at phone size; the full sub was checked at f493. |
| 8 | Ending | 4 | s8b reassembly fades out from 31.5 s, then a 0.8 s black lead, then a small 340 px logo, with the music fading 1.2 s. |
| 9 | Technical | 4 | Spec is correct. The reel is 1151 frames, not 1152: the first clip comes out one frame short, which is a known assembler behaviour. No black or duplicate frames at cuts. |

## Known weaknesses for the next agent
- **Rear jump cut:** s5_tail (a reused v1 push-in) ends on almost the same badge framing that N3 starts on. I started N3 six source frames in so the wing is already lifting on the cut. It still reads as a continuation more than a new shot. Next time, render the tail and wing as one continuous move.
- **Engine bay into bumper hero:** H ends wider and closer than N1a starts. The cut steps back a little; it is acceptable but not a clean progression.
- **Frame-diff cut detection:** cutcheck flags the fast part exits in N1a (frames 280–331) as cuts. Read the cut list against the timeline, not blindly.
