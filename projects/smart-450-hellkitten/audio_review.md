# Audio review (v3): the owner's voice and all other speech are MUTED

Owner feedback 2026-11-13: "0:04, my voice gets cut off from the music (mute my voice)". v3 removes speech from the mix by construction: shop sound is kept only under three powder shots whose spans were already speech-free in v1 (`clips.md`: no speech detected) and were re-checked for this cut with faster-whisper `medium.en` (machine transcription) on the shop-sound stem. Every other shot (S1, S2, S4, S5, S9, S12, S13, S17 and all scan shots, stills and the logo) has no shop sound at all.

| timeline (s) | shot | source clip, time (s) | what the machine heard in the stem span | gain |
|---|---|---|---|---|
| 2.27-3.00 | S6 | v_1634_19 14.50-15.23 | no words: spray hiss (ASR reads the noise as repeated letters) | +5 dB, 'up' |
| 3.00-3.77 | S7 | v_1634_19 6.90-7.67 | no words: spray hiss (ASR reads the noise as repeated letters) | +10 dB, 'up' |
| 3.77-4.50 | S8 | v_1634_51 0.15-0.88 | no words: spray hiss (ASR reads the noise as repeated letters) | +4 dB, 'up' |

## Residual risk

- The check is machine only. Quiet speech under spray hiss can be missed; listen to 5.27-8.0 s (S6-S8) once. If anything is audible, set `audio=None` on that shot in `tools/edit_shots.py` and rebuild.
- Scanner beeps were not kept: the scanner shots (S9, S17) come from clips with bystander speech and are muted.
- The meows (`stem_meows.wav`) are the only other sound besides the music. v1's table of speech rows (profanity / slur / price scan) is superseded by this mute; the v1 transcription is in `out/audio_review_raw.json` history only.
- Nobody has listened to this mix.
