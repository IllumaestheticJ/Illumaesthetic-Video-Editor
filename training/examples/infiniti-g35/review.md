# Infiniti G35 coupe scan reel - self-review (v2)

Output: `/home/user/media/work/g35/out/infiniti_g35_v2.mp4` - 1080x1920, 30 fps, yuv420p, AAC, 739 frames = 24.633 s.
Scan-only (no IRL, no text). Music: the track sent by the parent session, from 13.375 s (bar kick + 12 ms measured offset).

Timeline (section | shot | frames): whole s1_turntable 0-80 | front g1_lamp 80-160, g2_wheel 160-240 |
side g3_side 240-400 | rear g4_exhaust 400-480 (climax), g5_spoiler 480-560 | top s7_top 560-640 (fades out) | logo 640-739.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, orbit moving from frame 1. Car is small in the 9:16 frame (8 % cover) - whole-car rule wins over size. |
| 2 | Beat sync | 5 | cutaudio.py: 6 hard cuts at 80/160/240/400/480/560, errors +0.7/+10.3/+6.0/-2.7/-7.0/-4.3 ms vs the decoded-audio kick half-rise (max 10.3 ms < 1/2 frame). Logo enters after a fade, on the 21.333 kick. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 3 | House silver on black, lights stable (luma max jump <= 0.3 on g1/g2/g4, 1.4 g5, 3.7 g3 = camera moving onto the bright haunch). Real scan holes visible: lower rim spokes (g2), small window hole (g3 mid), grille edge sliver (g1). |
| 5 | Story | 4 | Travels front -> side -> rear -> top, each section once, contiguous (V2 rule B). No trunk/explode: no state or registered part scans exist (rules 6/D) - departs from the original brief's exploded view; logged. |
| 6 | Grade | n/a | No IRL footage. |
| 7 | Text | 5 | No text (brief). |
| 8 | Ending | 5 | Top-down fades to black over 0.4 s, then a SMALL logo (380 px) for 3.3 s; audio fades 0.3 s at the end. |
| 9 | Technical | 5 | Spec verified with ffprobe; exact frame counts per clip; no duplicate frames at cuts (next-frame diffs are slow ease-ins, all > 0); all close-ups rendered with persistent data OFF. |

## Checks run
- FIRST/MID/LAST contact sheets of every shot (`/home/user/media/work/g35/reg/v2/*.jpg`) and a +-1-frame sheet around every cut (`cuts.jpg`) - looked at.
- `ive director`: sections whole 2.67 / front 5.34 / side 5.33 / rear 5.34 / top 2.67 / end 3.3 s; no dead frames outside the logo hold;
  two "same view" flags (g1~g3, g3~g4) are silhouette-IoU false positives of frame-filling close-ups (different subjects on the sheet).

## What the next agent should learn
- `music.start` direction: a LATER start moves kicks EARLIER in the video. Measure, then shift by +mean error.
- `ive director` repeat detection is unreliable for full-frame close-ups (masks are all ~full); verify on the sheet.
- Background shell tasks die at 2 h: chain renders shot-by-shot and resume with a `frames:` list, not a full re-render.
