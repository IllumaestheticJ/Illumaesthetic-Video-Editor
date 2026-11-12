# Huracan Evo scan reel v5 (30 s cut) - self-review (training/rubric.md)  (older: review_v4/v3/v2/v1.md)

Output: `/home/user/media/work/out/huracan_evo_v5.mp4` - 1080x1920, 30 fps, AAC, 29.97 s.
From the user's notes on v4: 30 s total with the scan data sooner (Spyder teardown from 10.3 s, was 27.1 s); the reference
clip's engine start-up used exactly; the jet-like generated start-up removed; a lower voice.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Reference engine start-up from 0.3 s as the lights come up on the coupe; narration from 3.1 s. |
| 2 | Beat sync | 5 | Hard cuts vs the kick grid on the delivered file: +22 -11 -11 -12 -12 -12 ms. The lift (Spyder opens) is at n12 = 10.28 s, and the logo is on the music stop at 27.08 s. |
| 3 | 1:1 match | n/a | |
| 4 | Scan quality | 3 | Unchanged (coupe glass holes, Spyder wheels not captured). |
| 5 | Story | 4 | Coupe select -> wheel -> side, then Spyder front opens -> front bumper (label) -> hood -> fender/skirt -> rear bumper (label) -> explode/reassemble -> logo. Spyder moves play at 1.3-2x, so the parts move briskly. |
| 6 | Grade | 4 | Unchanged. |
| 7 | Text | 4 | Labels FRONT BUMPER / 4,000,015 TRIANGLES and REAR BUMPER / 7,999,727 TRIANGLES (the rear label is 1.4 s, short). Narration is imperial, with quirks and a Spyder block. |
| 8 | Ending | 4 | The logo holds 2.9 s (shorter than v4's 4 s) under the reverb tail and fades with the audio. |
| 9 | Technical | 4 | Loudness: -10 LUFS engine, -11 LUFS narration, peaks below -0.4 dBFS. Every frame lit. |

## Not verified / flagged
- The engine start-up is the game's audio, cut from the user's own screen recording of NFS Hot Pursuit Remastered (hp_1138 1.70-6.60 s). It's used as asked; flagged to the user as third-party game audio.
- Voice: Vesper at pitch -3 (~136 Hz, about 5 st below the reference narrator, which measured 182-186 Hz). v4 already matched the reference F0, so "too high" was perceived brightness or age. Unheard by me.

## What the next agent should know
- "Too high-pitched" can come after an F0 match: perceived pitch includes brightness/formants. Go 3-5 st under the reference rather than matching its F0.
- Generated engine SFX can read as a jet/turbine. Check band energy: a real start-up is ~65-70 % below 200 Hz; the rejected one had 57 % in 200-1k Hz.
- 30 s structure that works for scan reels: about 3 s engine start + 7 s of hero/IRL-equivalent, then the lift into the scan teardown at about 10 s, with the logo on the music stop at about 27 s.
