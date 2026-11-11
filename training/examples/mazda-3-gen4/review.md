# Mazda 3 (gen 4) hatch scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/work/m3/out/mazda_3_gen4_v2.mp4` — 1080x1920, 30 fps, 38.2 s (1146 frames), h264 yuv420p + AAC.
v1 review kept in `review_v1.md`. v2 answers the user's v1 notes (car cropped; redundant shots of the same sections;
removed-state data must be the highlighted, labelled hero; only show states that have real scans).

Timeline (front -> side -> rear, no ping-pong; each section once):
m1 front (whole car, orbit 12->58 deg) | m2 left flank (close tracking pass) | m3 rear quarter -> tail |
m4 rear hatch: wing pops off on the drop, hold on the Wing Removed mounting points + label | m5 wing underside |
m6 top-down whole car, wing locks on b60, fade | small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Camera orbits from frame 1 (near head-on swinging to the front 3/4). Track intro is quiet so the first beat lands at 4.4 s. |
| 2 | Beat sync | 5 | Cuts measured in the delivered file's decoded audio: 4.400 / 8.767 / 15.333 / 25.133 / 28.400 / 34.933 s vs kicks 4.354-4.412 / 8.777 / 15.279 / 25.112 / 28.386 / 34.934 (within 1 frame). Wing pop on the b36 drop, wing locks on b60. |
| 3 | 1:1 match | n/a | No IRL footage in this brief. |
| 4 | Scan quality | 4 | Framing fitted numerically (whole car never clipped on wide shots, checked first/mid/last). Every frame luma-checked (no light dropouts; persistent data off for moving-part shots). Remaining: tyres are scanned as rough rings (car on jacks); grille mesh is holey; a few scan speckles on the sill in the flank pass. |
| 5 | Story | 4 | One continuous sequence per section; the removed-state scan is the hero (camera moves in and holds ~3.3 s on the real mounting holes, then shows the wing's scanned underside). OEM aero spoiler dropped (doesn't register to this car); no door/hatch/hood opening (no such scans). |
| 6 | Grade | 5 | House silver on black, AgX, consistent across shots. |
| 7 | Text | 5 | One factual label ("REAR WING REMOVED / MOUNTING POINTS") over scan-only black above the roof; no numbers. |
| 8 | Ending | 5 | Car fades out on the last kicks, then a small ILLUMAESTHETIC logo; video ends at 38.2 s where the music dies. |
| 9 | Technical | 4 | Specs met. Assembler hold frame before each cut (one repeated frame). |

## Director check (`ive director`)
- Dead frames in the old m1/m2 (3.4 s / 4.3 s) fixed by re-cutting both shots; m1~m2~m3 "same view" fixed (m2 is now a close flank pass, m3 starts on the rear quarter).
- Kept: m4 1.0 s hold (label read on the mounting points), m6 0.8 s hold (fade tail before the logo); m3~m6 similarity (rear 3/4 vs top-down reassembly — different section and purpose).
