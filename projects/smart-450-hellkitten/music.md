# S3 music

**Track:** "HARDER THAN HARD TECHNO" - IMHAPPY, TikTok Commercial Music Library (EDM, US 7-day trending, 2026-11-12),
song_clip_id `7566061980668463121`. Not used by any earlier project (checked project.yaml / editlogs / lessons).
**Licence:** CML = licensed for TikTok brand posts only. Use for the TikTok post; attach the same sound when posting. NOT cleared for YouTube/IG/other.
**Why not generated:** Higgsfield balance was 0.63 credits; a 28 s ElevenLabs Music v2.5 generation costs 4.07. No credits spent.
**File:** `/home/user/media/work/smart-450/music/smart450_short.wav` (44.1 kHz stereo, 29.6 s) = source track 35.0-64.6 s, 1.0 s fade out from 28.6, -6 dB + limiter. Source m4a (204 s) alongside as `harder.m4a`. Not in git.
**Measured:** 159.64 BPM (P = 0.37583 s). Grid t = 1.499 + 0.37583 n. `ive beats` says 161.5 BPM / 0.372 s: ~1 % fast, do not use.
The kick is a rolling 16th pattern, so a kick-band fit is weak; the grid is anchored on the 3 drops (1.499 / 13.526 / 28.559 = exactly 32 and 40 beats apart).
**Loudness:** -9.6 LUFS integrated, true peak -4.4 dBFS, 0 clipped samples (the source is hot, -4.6 LUFS, and decodes >0 dBFS). LRA 6 LU.
**Vocals:** none audible in structure (techno); 300-3400 Hz band sits 10 dB under the full mix (no sustained vocal formants). Spectral check only.

## Structure (clip time)
| t (s) | what |
|---|---|
| 0 - 1.50 | pre-drop riser, hits at ~1.12 and ~1.32 (quiet, -12 LUFS-ish) |
| **1.499** | **DROP 1** (hook, within 1.5 s); hard kick + bass until 12.02 |
| 12.02 - 13.526 | break 1, kick out (4 beats) |
| **13.526** | **DROP 2** to 22.55 |
| 22.55 - 28.559 | break 2: kick out, pad/riser 6 s; sparse build hits at 27.03, 27.78, 28.16 |
| **28.559** | **DROP 3 = logo card on this downbeat**; tail fades 28.6-29.6 |
Cut on drops/breaks; inside drops cut every 2 beats (0.752 s) or on bar lines (1.503 s). Details in `beats.json` next to the WAV.

## Extend / shorten
Repeat whole 8-beat blocks (3.0066 s) inside a drop section (e.g. beats 36->44) with a 12 ms crossfade; break 2 can be shortened by removing whole beats from its pad middle. Reel is ~25 s: trim by starting later is NOT possible (drop is at 1.5 s); trim the end by moving drop 3 earlier via removing 8-beat blocks from drop 2.
