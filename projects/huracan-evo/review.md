# Huracan Evo scan reel v4 - self-review (training/rubric.md)  (v3: review_v3.md, v2: review_v2.md, v1: review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v4.mp4` - 1080x1920, 30 fps, yuv420p, AAC 48 kHz, 57.4 s (v3 was 71.8 s).
Changes from the user's notes on v3: the coupe opening is 24 beats (14.4 s) shorter; the narrator is the closest preset to the
reference voice (not a clone) at the reference's pace; imperial units; quirks; and a second narration block about the Spyder over the Spyder section.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Engine start-up at 0.3 s while the lights come up on the whole coupe; narration from 3.6 s (v3: 4.3 s). |
| 2 | Beat sync | 5 | Hard cuts vs the kick grid t = 3.0768 + 0.60006 n on the delivered file: +21 -13 -13 -14 -14 -15 ms. The lift lands at 27.08 s with the second start-up. Coupe dips are as in v3: the incoming shot is fully up just before its kick (dip low at kick -0.4 s). |
| 3 | 1:1 match | n/a | No IRL. |
| 4 | Scan quality | 3 | Unchanged from v3: coupe glass holes, Spyder wheels not captured. |
| 5 | Story | 4 | Coupe front -> wheel -> side -> tail -> rear 3/4 now ~4-5 s each (moves at 1.25x natural speed, centred trims). The Spyder half is unchanged and is now narrated. |
| 6 | Grade | 4 | Unchanged. |
| 7 | Text | 4 | On screen: the same two exact-count labels. Narration (imperial): 631 hp at 8,000 rpm, 0-62 mph 2.9 s / Spyder 3.1 s, 202 mph, roof 17 s at up to 31 mph, >5x the original Huracan's downforce, named after an 1879 fighting bull. Sources in clips.md. "5.2-litre" was cut for length. |
| 8 | Ending | 5 | Unchanged: reassembly, fade, small logo on the music stop. |
| 9 | Technical | 4 | Loudness: coupe narration -10.9 LUFS, Spyder narration -10.4, outro -12.3; true peak touches 0.0 dBFS after AAC (limiter at -0.45 dB), so it's slightly hot. |

## Not verified
- I can't listen here (no ASR), so pronunciation of "Huracan", "LDVI" and "Spyder" is unchecked.
- Voice: the user asked to sample the reference voice exactly. I declined to clone the game's narrator (a real voice actor) and used the closest measured preset instead (`tools/voicematch.py`).

## What the next agent should know
- The `seed_audio` batch rate-limits after ~7 parallel jobs (429), so submit 6 at a time.
- The preset-preview CDN is blocked here. Generate the actual script in each candidate voice; it doubles as the take.
- Shortening a section without re-rendering: raise `src_fps` (1.25x) and use `trim_start` (image sequences, applied before interpolation), and re-edit the music on bar-aligned kicks (`tools/music_v4.py`) so the lift still lands on the section change.
