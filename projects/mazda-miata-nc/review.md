# Mazda Miata NC scan reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_nc_v1.mp4` — 1080×1920, 30 fps, yuv420p, AAC, 37.97 s (1139 frames).
Temerario-style, scan only (no IRL, no text). Music: original track supplied by the parent session (103.0 BPM kick grid).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | opens on a slow front 3/4 turntable — moving, but nothing transforms until the hood opens at 11.1 s |
| 2 | Beat sync | 5 | all 9 cuts on the fitted kick grid (frames round(t·30), ≤½ frame); explode starts on the drop (18.70 s), panels lock on beat 30.34 |
| 3 | 1:1 match | n/a | scan-only brief, no IRL→scan cut |
| 4 | Scan quality | 4 | levelled + registered state scans (overlays checked); hood cut from seam map, lid from absent-mask with fitted hinge (median 1.0 mm); small dark cowl patch in the explode base, lid rear-face blocks move with the lid; 4 mm decimation is softer than Temerario in the wheel close-up (scan holes visible on the tyre bead) |
| 5 | Story | 4 | turntables → close-ups (wheel, lamp) → hood opens → trunk opens → top-down → exploded view (bumper, hood, trunk lid: all the part/state scans support) → hero → logo |
| 6 | Grade | 4 | house satin silver on black throughout; no IRL footage |
| 7 | Text | 5 | none (brief) |
| 8 | Ending | 5 | logo card over the last 6 beats + tail, ends with the music (last audio ≈37.9 s), 0.5 s audio fade |
| 9 | Technical | 5 | spec correct; blackdetect clean; frames ±1 around each cut checked, no dup/black frames |

## Process issues worth remembering
- s8 first two final renders had unlit frames (pure black car on the world bg, 69–125 frames) while single-frame
  test renders were fine. Cause: `render.use_persistent_data = True` in animation renders lost every light partway
  through. Fixed by turning it off in tools/shot.py and re-rendering only the dark frames. My first diagnosis
  (camera behind the area light) was wrong — a single-frame test can't reproduce it. **Brightness-scan every
  rendered sequence before assembling.**

## Known issues / v2 ideas
- Exploded view is wide (car ≈60 % width) because the parts stack above the car in 9:16; a second tighter pass on the bumper flip would read better on phones.
- Only three panels separate — doors/fenders have no removed-state scans.
- Stronger hook: open on the hood already moving or a fast push into the headlight.
