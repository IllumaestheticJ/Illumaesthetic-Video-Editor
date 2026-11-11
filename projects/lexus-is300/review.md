# Lexus IS300 (first gen) scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/work/is300/out/lexus_is300_v2.mp4` — 1080x1920, 30 fps, 37.37 s, scan only.
v1 feedback: "Same first draft issues as the others. Need to focus on specific sections better. Car is clipped at beginning."
Plus the shared V2 brief / addendum (front → side → rear, one sequence per section, bumper-off hero, real state scans only,
progressive explode → reassembly → fade → small logo, exact-data labels).

Order (section per shot, see direction.md): whole car orbit (whole) → front-right wheel (wheel) → headlight/grille (front)
→ front bumper drops off on the drop, push in on the intercooler (front, hero) → side skirt slides out, bare sill (side)
→ rear bumper back + tipped to show its scanned inner face, trunk lid lifts off the Rear Trunk Open state (rear)
→ top-down progressive explode, reassembly on the triple hit, rear-left 3/4 hold, fade (whole) → small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car in frame from frame 0 with a steady orbit (director flags 1.9 s "dead" because the car is ~6 % of the frame; frame diffs show constant motion) (-26 → -58°, 14-25 % margins). First part movement is still at 10.5 s (front bumper on the drop) — the opening is the reveal. |
| 2 | Beat sync | 4 | Cut frames measured on the delivered file: 158/197/275/471/588/745 = plan; low-band kick onsets on the decoded audio sit 0.2-0.8 frame before each cut (all within ±1 frame). 941 is the fade-to-black into the logo, not a hard cut. One cloned frame before each cut (assembler cut hold). |
| 3 | 1:1 match | n/a | No IRL footage. |
| 4 | Scan quality | 3 | 2022 Artec scan: open glass, wiper/cowl scraps, front bumper part is derived (ragged lower edge visible when it drops). Plates flattened in geometry (front on car/car2/fbumper, rear on lid) per the IS300-only note. |
| 5 | Story | 4 | Sections travel front → side → rear, each in one sequence; bumper-removed intercooler is the hero beat with a hold; the trunk is only opened because a Rear Trunk Open state scan exists. Director flags s5 ~ s7 as a similar composition: kept on purpose as a front/rear pair (logged). |
| 6 | Grade | 4 | House satin silver on black, -0.5 EV; every frame luma-checked (no dark/black frames; peaks 247-255). |
| 7 | Text | 4 | Five short labels, one at a time, over black only, exact facts from the scan folder (part removed / state scanned). No numbers. Sub-lines type on and finish before each label leaves. |
| 8 | Ending | 4 | Parts lift on b40, land on 44/45/46, car settles (0.9 s hold), fades on the scan, small logo on black fades out with the track. |
| 9 | Technical | 4 | 1080x1920, 30 fps, yuv420p, AAC, faststart. 1121 frames (planned 1122; the lost frame is the final black frame). Persistent data off, no black frames inside shots. Nothing touches the frame edge except the side close-up (deliberate crop of the rear half of the car). |

## What changed vs v1
- Opening is the whole car with margins, orbiting from frame 0 (v1 clipped the car).
- Structure by section, front → side → rear, instead of turntables then generic close-ups; no repeated orbit views (v1 rear 3/4 and top-down removed).
- Front bumper off is the hero: drops down and away on the drop, camera pushes in on the front-mount intercooler and holds.
- Rear bumper tipped to show its scanned inner face; the side skirt only translates (its backside is not useful).
- Labels added (exact data only), over black.
- Ending: progressive explode → reassembly → fade → small logo.

## Notes for the next agent
- First full renders still clipped parts that moved TOWARD the camera (front bumper, rear bumper). Move removed parts down/away from the lens, and render 30 % stills at the frames where parts are at max offset, scanning the 2-px border for luma > 40 before queuing finals.
- `ive director` caught a near-static opener the eye missed on stills (motion 0.22 → dead frames). Run it on every cut before delivery, not only on v1.
- `shots.py still` accepts `FRAMES=1,35,52` to render specific frames.
