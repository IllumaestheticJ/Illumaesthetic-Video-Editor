# Huracan Evo scan reel v13 - self-review (training/rubric.md)  (older: review_v12 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v13.mp4` - 1080x1920, 30 fps, AAC, 46.8 s.
Change from the user's note on v12: "the front feels rushed - the whole thing is not the same pacing. re-pace the whole video -
make it longer if it needs to be". Narration take unchanged from v12.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Unchanged: engine start-up and lights-up reveal, speech from 3.4 s. |
| 2 | Beat sync | 5 | 10 scan cuts on the kick grid of the delivered file: +22 (drop, 13.28 s), then -12..-14 ms. Logo on the last kick, 43.88 s. |
| 3 | 1:1 match | 4 | Coupe -> Spyder stealth cut: IoU 0.887 with the re-rendered 36-frame push; frame difference at the cut 3.2 (other cuts 31-68). |
| 5 | Story / pacing | 4 | Playback speed per shot: wheel 1.0x, side 1.2x, push 0.8-1.0x, Spyder opener 1.15x, front bumper 1.22x, hood 1.2x, side 1.2x, rear bumper 1.0x, decklid 0.8x, exhaust 1.0x, wheel well 0.8x, explode 1.06x, reassembly 1.0x (v12: 1.5-2.0x in the opening and front, 1.0x in the rear). Opening shots 3.0 s each, every labelled teardown step 3.0 s. No frozen runs. |
| 7 | Text | 4 | Seven title-only labels, 2.25 s each, on black. |
| 8 | Ending | 4 | The speech ends at 35.3 s; the last 8.5 s before the logo (wheel well, explode, reassembly) are music and picture only. |
| 9 | Technical | 4 | Every frame lit. Speech -13.3 LUFS, peak -1.0 dBFS. |

## Not verified
- I can't listen here, so the narration against the new picture timing is unheard.

## What the next agent should know
- "Not the same pacing" = uneven playback speeds between sections. Tabulate frames-used / duration / 15 fps for every shot and keep
  them within about 0.8-1.2x; give every equivalent step the same number of beats, and re-render a shot longer rather than slow it
  below ~0.8x or squeeze it above ~1.2x.
- Re-pacing moves the drop: rebuild the music from an earlier source bar (`tools/music_v13.py`) so the drop still lands on the cut.
