# Honda S2000 AP1 scan reel — self-review (v3, `/home/user/media/work/s2k/out/honda_s2000_v3.mp4`)

Scored with `training/rubric.md` before delivery. Measured on the delivered file (tools/cutcheck.py + frame diffs).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Turntable is moving on frame 1 (s1 starts 1.4 s into its render; v1 barely moved for 0.8 s). No transformation in the first 1.5 s; this is a scan-only Temerario-style reel, so the hook is the scan detail itself |
| 2 | Beat sync | 5 | 9 cuts on bar lines of the 138.05 BPM kick grid, errors −15.8…+14.6 ms (all within ½ frame). Hood lifts on the drop (b32), panels separate b49 and lock b76 (motion keys on beats) |
| 3 | 1:1 match | n/a | No IRL footage by brief. Stand-in check: every state scan is registered to the full car (hood/fender p50 1.47 mm; trunk scan rigid-zone ICP) and the panels land back exactly where they were cut |
| 4 | Scan quality | 4 | Silver on pure black, 2 mm close-ups show the fender badge, mirror, lamp detail. Minus: the car was scanned without wheels (empty arches), the bay behind the radiator support is unscanned (kept in shadow by a front camera + 40° hood), some stringy scan debris under the radiator support in s5/s8, dusty-capture speckle on the state-session bumper |
| 5 | Story | 4 | Turntables → close-ups → front opens → trunk opens → top-down → exploded → logo, as briefed. Only three panels have scan data (bumper, hood, trunk lid), so the explode is thinner than the reference's |
| 6 | Grade | 5 | No IRL; AgX, no colour; background matches the logo card black |
| 7 | Text | 5 | None, by brief (the S2000 badge is scanned geometry) |
| 8 | Ending | 4 | Logo on the last downbeat (b80, 34.83 s); the track hard-stops at 36.57 s under the logo and the reverb tail fades with it (−41 dB at the end). After the lock (33.1–34.8 s) the assembled car sits small and right of centre |
| 9 | Technical | 5 | 1080×1920, 30 fps, yuv420p, AAC 320k, faststart, 1152 frames = 38.400 s; no duplicated cut frames (fixed vs v1), no black frames (s8 re-rendered) |

## Versions
- v1 (`ive assemble`): every cut frame duplicated A's last frame; s8 frames 17–211 rendered unlit (persistent-data fault) — not delivered.
- v2 (concat assembler): cut frames clean, s8 still broken — not delivered.
- v3: s8 re-rendered with persistent data off, wider orbit and livelier drift. Delivered.

## What the next agent should try
- Ask whether a wheels-on scan of this car exists; it would allow the reference's low side profile.
- A scan of the open hood or the engine bay would let the hood open fully.
- Re-frame the 1.7 s after the explode lock (push in on the assembled car) — the only weak framing in the cut.

# v4 — after reviewer feedback ("beginning is great, last scenes held too long")
`/home/user/media/work/s2k/out/honda_s2000_v4.mp4`, 1116 frames = 37.2 s.
- The 13.9 s exploded shot is now 7 shots of 4-8 beats (e1 separation, e2 high side, e3 low front looking up, e4 floating
  hood close-up, e5 high rear, e6 return + lock on the cut, e8 push-in on the locked car). Sub-shots render windows (t0) of
  the same part animation, so panel positions stay continuous across cuts. Logo 3.6 s -> 2.4 s; the video ends 0.6 s after
  the track's hard stop.
- Beat sync re-checked on the file: 15 cuts, all within ±16 ms (first v4 pass had hand-picked 52/53-frame shots that
  drifted to +38 ms; fixed to round(beat*30)).
- Scores changed: Story 5 (back half now has the front half's rhythm), Ending 5 (no small off-centre hold, short logo).
- Open: reviewer wants an IRL opening (S2000 being scanned) with a 1:1 cut; footage is on YouTube only, which this
  environment cannot reach - waiting for the raw clip on Dropbox.
