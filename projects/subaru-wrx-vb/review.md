# Subaru WRX VB scan reel v1: self-review (training/rubric.md)

Output: `/home/user/media/work/wrx/out/subaru_wrx_vb_v1.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p + AAC, faststart, 35.47 s (1064 frames).

What was checked:
- A contact sheet of every final shot (`chk/final_q1.jpg`, `final_s5.jpg`, `final_s7.jpg`), plus full-size frames for s3/s4/s5/s7.
- A per-frame max-luma scan of every render: minimum 255 in all seven shots, so no black frames.
- Frames −2..+1 around all 7 cuts (`chk/cuts.jpg`).
- Cut positions measured from frame differences.
- A static-frame scan for interpolation clones.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | The 3/4 turntable moves from frame 1. The track opens on an ambient intro: the first hit is 5.22 s and the drop is 11.25 s, so the visual hook carries the first 5 s alone. Scan-only brief, so there is no IRL→scan transformation. |
| 2 | Beat sync | 5 | The measured cuts are at frames 157, 261, 338, 421, 547, 631, 966. Against the kick grid (5.224, 8.707, 11.252, 14.044, 18.232, 21.024, 32.191 s) the errors are +9, −7, +15, −11, +1, +9, +9 ms, all within ½ frame. The explode separates on the 22.42 s downbeat inside s7 and locks on 30.80 s. |
| 3 | 1:1 match | n/a | Scan-only reel (Temerario style), no IRL footage. |
| 4 | Scan quality | 3 | Silver on black (car luma median 165, background 7), with no ground or debris. Both licence plates were flattened (privacy). Weak spots, all real scan gaps: ragged black holes along the wiper cowl (s4, s6) and inside the hood-scoop mouth (s4). The far front wheel shows under the car in the s3 close-up. The bumper's inner edges are ragged in flight in s5. |
| 5 | Story | 4 | Order: front 3/4 turntable, rear 3/4 orbit, wheel close-up, hood scoop, front end comes off (bumper with blank plate and garnish slide clear and show the scanned crash structure), top-down, exploded view (bumpers, garnish, flares and skirt lift into layers above the car while the camera orbits, then lock home), logo. The trunk-open beat was dropped: the No-Trunk / VB Trunk states only reached a 10.8 mm median hinge fit and an incomplete lid mask (editlog). |
| 6 | Grade | 5 | One AgX house look throughout; the logo card is on the same black. |
| 7 | Text | 5 | No text (per the brief); logo only. |
| 8 | Ending | 4 | The logo cuts in on the 32.19 s downbeat, the music fades from about 33 s, and the reel ends at 35.47 s with a 0.8 s fade. The last second peaks at −16.8 dB. |
| 9 | Technical | 4 | 1080x1920, 30 fps, yuv420p, AAC, faststart, no black frames. Interpolation clone tails were removed with per-clip `src_fps = 30N/(slot+4)`. One held frame remains before each cut; this is the assembler's cut frame and is also present before s1's cut, which has surplus frames. |

## Things the reviewer may push on
- There is no trunk-open shot. "Front end off" stands in for the "hood, trunk or panels open" beat.
- The explode only has part scans for bumpers, garnish, flares and skirt. There is no hood, door or fender part, so the body shell stays put.
- The ambient 5 s before the first hit is long for a reel opening.
- Music: the generated track sent by the coordinating session, starting at 0.

## For the next agent
- Turn Cycles persistent data off for any shot with keyed parts (`tools/shot.py` here does this automatically). Still scan max luma per frame.
- With 15 fps renders plus minterpolate, set `src_fps = 30*N/(slot_frames+4)` per clip. Otherwise each shot ends on 1–2 cloned frames, which show as a stall right before the cut.
- Licence plates in Artec scans keep embossed characters. Flatten them by plane projection in a box (`tools/flatten_plates.py`) and check with a close-up render.
- `tools/sheet.py` now samples N frames per directory. The old version tried to tile every frame of a final render and overflowed PIL's maximum image size.
