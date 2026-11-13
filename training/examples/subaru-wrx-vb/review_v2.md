# Subaru WRX VB scan reel v2: self-review (training/rubric.md)

Output: `/home/user/media/work/wrx/out/subaru_wrx_vb_v2.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p + AAC, 35.4 s (1062 frames). v1 review: `review_v1.md`; v1 timeline: `project_v1.yaml`.

v2 follows the V2 brief and addendum A-D. The order comes from this car's scan features (`direction.md`, `director.md`) and travels front → side → rear with no ping-pong:
1. Whole car, moving from frame 1.
2. Hood scoop.
3. FRONT BUMPER REMOVED: the bumper and plate flip to show their scanned inner face, the garnish follows, and the camera ends low on the scanned structure.
4. Right-side cladding comes off one part per bar (front flare, door flare, rear flare, skirt), ending on a wide that shows every removed part.
5. REAR BUMPER REMOVED with the same grammar.
6. Reassembly rear → side → front, locking on the beat.
7. Fade, then a small logo.

What was checked:
- Per-frame mean-luma scan of every v2 render. The largest frame-to-frame step is 0.10 (side_off, a flare leaving the frame) and 0.235 in front_off (the bumper leaving). No dropouts.
- Contact sheets of the first/mid/last frames (`chk/v2_finals.jpg`, `chk/v2_ends.jpg`).
- Frames around every cut plus both label frames (`chk/v2_cuts.jpg`).
- `tools/cutcheck.py` against the decoded audio of the delivered mp4.
- `ive director` repeat check.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | The whole car in a moving front-right 3/4 from frame 1, cut on the first hit (5.27 s). The ambient intro still carries the first 5 s. |
| 2 | Beat sync | 5 | Cut minus onset (decoded delivered audio): +4.7, −16.7, −5.3, +14.7, −9.3 ms, all within ½ frame. Two cuts were moved one frame after the first measurement (−50 / −43 ms). The logo cut at 32.13 s is under the fade. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 4 | Silver on black. The bumper-removed states show real scanned structure (front crash structure; rear beam, exhaust and hangers). Persistent data is off for every keyed shot. Real scan gaps remain at the cowl and inside the scoop. |
| 5 | Story | 4 | Each section appears in one continuous sequence (addendum B), the bumper-removed states are the hero beats (C), and nothing opens without a state scan: no trunk, hood or door (D). The director flags front_off/side_off as a similar view: the front shot ends low on the right of the front end and the side shot starts at the front-right wheel. This is the intended front→side travel, with different parts removed. |
| 6 | Grade | 5 | One AgX house look; the logo is on the same black. |
| 7 | Text | 5 | Two factual labels over scan shots only: "FRONT BUMPER REMOVED" and "REAR BUMPER REMOVED", each with "SCANNED STRUCTURE BEHIND IT". No numbers. |
| 8 | Ending | 4 | The reassembly locks, then a 0.7 s fade; the small logo arrives on the 32.13 s downbeat. Total 35.4 s. |
| 9 | Technical | 4 | Spec-correct, no black frames, per-clip `src_fps = 30N/(slot+4)`. The rear close-up end frame is cropped on both sides on purpose (detail of the exposed structure). One assembler hold frame remains before each cut. |

## Things the reviewer may push on
- The rear close-up is tight: the body is cut at both frame edges to show the structure large.
- The removed flares float above the car in the side wide; they are not laid out on the floor.
- The hood-scoop clip is reused from v1 (it appears once in this reel).

## For the next agent
- Do not load already-removed parts into later section shots, not even parked far away: low cameras still see them at the top of the frame. Leave them out and bring them back only for the reassembly.
- Run `tools/cutcheck.py` on the delivered file, not just the grid. In this track the grid was off by 30-50 ms at two drops, and one-frame duration shifts fixed it.
- Frame-diff "cuts" inside a shot (parts leaving the frame) also show up in cutcheck; match them against the timeline before acting.
