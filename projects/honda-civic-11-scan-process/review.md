# Honda Civic EK scan-process reel v3 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/civic_ek_scan_process_v3.mp4` — 1080×1920, 30 fps, 31.30 s, H.264 yuv420p + AAC. Earlier: review_v1.md, review_v2.md.
v3 = feedback on v2: don't reuse music other agents used → "THE DEATH" (Sworra), TikTok Commercial Music Library EDM 7-day #2,
not used by any project (grep of projects/ + training/); re-cut to its 128 BPM grid. Visuals as v2 (nothing comes off the car).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | powdering shot over the build + snare fill → 1:1 cut to the scan on the drop kick (3.20 s) |
| 2 | Beat sync | 5 | 5 cuts on kicks within ±18 ms (tools/cutcheck.py); the cut into the software beat is on the downbeat where the track breaks out (no kick by design); scan sweep starts on the re-entry kick |
| 3 | 1:1 match | 4 | cam_A 18.3 mm / cam_B 28 mm (unchanged); scan wipers differ from the shoot |
| 4 | Scan quality | 5 | intact full-car scan only |
| 5 | Story | 5 | powder → scan → handheld scanner pass (scanner visible on the door) → scan orbit → software (in the music break) → sweep → listing |
| 6 | Grade | 4 | HLG tonemapped; software beat is an upscaled viewport crop |
| 7 | Text | 5 | 24,997,508 triangles (STL header); EXTERIOR SCAN / HONDA CIVIC EK HATCHBACK |
| 8 | Ending | 5 | sweep → listing grey (morph done before the dissolve) → listing; title, logo, URL last; video ends where the track drops out (73.18 s) |
| 9 | Technical | 5 | 31.30 s; frame-accurate cut holds |

## Learned this round
- Check other projects' music (title / song_clip_id in project.yaml + editlogs) before picking — standing rule now.
- Agents all draw from the same CML trending chart; the top few get taken fast. Genre filters (EDM, HIP_HOP/RAP) surface unused tracks.
- Place a software/text-free beat inside the track's break and start the next scan move on the re-entry kick.
