# Huracan Evo scan reel v6 - self-review (training/rubric.md)  (older: review_v5 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v6.mp4` - 1080x1920, 30 fps, AAC, 29.97 s. Picture is identical to v5 (same timeline).
Change: one continuous speech about the EVO (user), in a custom voice cloned from the mod creator's own narration
(`jennp_voice2.mp4`; the user attests explicit consent from the speaker), at her natural pitch, without the pitch/speed processing
v5 had.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Reference engine start-up at 0.3 s, speech from 3.0 s. |
| 2 | Beat sync | 5 | Same cuts as v5 (-12..+22 ms vs kicks). |
| 7 | Text | 4 | Spoken: EVO, named after an 1879 fighting bull, NA V10, 631 hp, AWD + rear-wheel steering, LDVI predicts your next move, >5x the original Huracan's downforce, 0-62 mph 2.9 s, 202 mph. The torque line was cut to fit 30 s without speeding the voice up. |
| 9 | Technical | 4 | Speech section -12.7 LUFS, engine -10 LUFS, peaks <= -0.4 dBFS. The clone is built from a clip with music under the voice (no stem separation available here), so some bed colour may carry into the voice. |
Other rows: unchanged from v5 (review_v5.md).

## Voice measurements (tools/voicematch.py)
- Against her source recording: F0 -0.2 st, timbre 1.1 dB; pace 3.7 onsets/s (calmer than v5's 4.3-4.8).
- Pauses are trimmed to 0.32 s (no time-stretch). seed_audio speech_rate +5 (the 0 take with the full script ran 28 s).

## Not verified
- I can't listen here, so the clone's likeness and pronunciation (Huracan, LDVI) are unchecked.

## What the next agent should know
- Only clone a voice with the speaker's consent. Files traced to a game narrator (exact F0 match to the reference, downloader encoder tag, digital-silence gaps) were refused even when renamed.
- A clean voice-only recording makes a better clone than one cut from a mix.
