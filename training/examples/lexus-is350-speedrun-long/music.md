# L1 music

## Source and licence
- **Source:** owner-supplied upload, received 2026-11-12. Audio extracted from the upload's video as two halves (`part1.m4a` 599.6 s, `part2.m4a` 587.0 s), 128 kbps AAC, 44.1 kHz stereo. Title shown in the upload: "speed up - fun/epic video game music for try hard".
- **Joined** sample-accurately into `/home/user/media/work/is350-long/music/mix_full.wav` (44.1 kHz s16, 1185.588 s = 19.76 min): part2 starts at part1 sample 26398720 (598.610 s); the overlap is 0.998 s (not 1.6 s), NCC 0.99. Not in git.
- **Licence:** the owner supplied it; the upload's video shows it is a third-party compilation of game music; rights/clearance for YouTube not confirmed.
- Quality caveat: 128 kbps AAC source (re-encode of a re-encode). Fine under speech, soft on transients; beat grids below are measured on this file.
- The earlier plan to generate a bed (Higgsfield balance 0.63 credits vs 17.44 for 120 s) is superseded; no credits spent.

## Pieces in the mix (`mix_segments.json`)
Boundaries are fade dips/digital silence. Tempo = kick-band (40-120 Hz) beat-comb fit; `ive beats` not used (it half/1.5x-errs on these).
| id | mix time (s) | BPM | key (est.) | LUFS | mid share* | notes |
|---|---|---|---|---|---|---|
| P1 | 0 - 121.5 | 149.97 | C minor | -18.3 | 42% | steady, fade 113.5-121.5 |
| P2 | 126.5 - 283.0 | 148.0 | D minor | -17.2 | 42% | bright, weak grid |
| P3 | 286.5 - 347.0 | 158.77 | n/a (sub-bass) | -15.4 | 3.5% | pulse, from digital silence |
| P4 | 348.5 - 647.0 | 150.00 | D min/G/C/A min | -13.8 | 25% | 300 s driving, flat; may hold several pieces at 150 BPM |
| P5 | 648.0 - 811.0 | 86.0 (172) | C major | -15.5 | 20% | calm, fade 804-811 |
| P6 | 813.5 - 958.0 | 87.0 | D major | -14.1 | 38% | bright |
| P7 | 962.0 - 1096.5 | 148.0 | G major | -17.4 | 29% | breakdowns ~1022, ~1078; fade 1090-1096.5 |
| P8 | 1100.5 - 1185.59 | 189.85 (94.9) | G/C major | -16.3 | 34% | quiet intro, lift 1113.4, breakdown 1154.5-1169, cut off at mix end |
*share of spectral energy 500-3000 Hz = speech band. **Vocals / lead melody:** not verifiable by analysis. No sustained vocal formants were looked for beyond this share; pieces with >=35% (P1, P2, P6, P8) probably carry a lead melody and would fight speech: listen before using under talking. P3/P4/P5 are the least masking.

## Recommended map (5-7 min presenter video)
| use | piece, mix in -> out | why | beats file |
|---|---|---|---|
| host intro / talking bed | **P5** 648.0 -> 811.0 (loop 16 bars from 681.954; fade 804-811) | calm, 20% mid | `beats_p5_intro_bed.json` |
| clock-pulse / tension bed | **P3** 286.5 -> 347.0 (loop 8 bars from 301.402) | sub-bass pulse, nearly no mid; only 60 s so loop it | `beats_p3_clock_pulse.json` |
| scanning-against-the-clock montage | **P1** 8.0 -> 113.5 (loop 16 bars 40.466 -> 66.07), extend with **P4** 356 -> 642 (crossfade on a bar line, both exactly 150.0 BPM) | steady drive, firm grid | `beats_p1_montage.json`, `beats_p4_montage_ext.json` |
| result reveal | **P8** 1100.5 -> 1154.5: 12.9 s quiet intro, lift at ~1113.4 (+5 dB); optional pause in breakdown 1154.5-1169.0, second lift 1169.0 | the only clear lift in the mix | `beats_p8_reveal.json` |
| outro | **P7** 1082.3 -> 1096.5 (G major like P8, native 6 s fade) | resolved fade; P8 itself has no ending | `beats_p7_outro.json` |
Time the reveal cut to the lift at 1113.4 by ear (P8 grid drifts 31 ms between thirds; confidence medium-low).

## Caveats
- Bar 1 (downbeat) is unverified in every piece; loops/crossfades are multiples of 4 beats from the in point. Check by ear.
- P5, P8 tempo grids are weak (kick conc 0.04 / 0.11); P4 has no verified repeat. P1, P3, P7 are solid (drift < 5 ms).
- Loudness is -14 to -18 LUFS per piece: duck 10-15 dB under the host (target music about -26 to -30 LUFS under speech).

---
# v2 music (2026-11-13) - crash set-piece and fixed hits
Everything is built from the owner's `mix_full.wav` only, plus a generated 1 Hz clock tick and hit/riser sound design that is itself processed owner audio.
**Nobody has listened to any of it.** All checks below are measurements (onset detection, ebur128), not listening.
Files: `/home/user/media/work/is350-long/music/v2/` - `music_v2_map.json` (section -> file, timeline in/out, anchor, gain), `beats_*.json` per segment. Timeline times are pre-beat-snap (edl_v2.json).

| section | timeline | file | piece | anchor (error, broadband / kick band) |
|---|---|---|---|---|
| cold open, title, answers | 0:00-0:24.95 | `intro_p5.wav` (+`intro_p5_long.wav`, 40 s, unducked) | P5 calm, 20% mid | silent from 24.89; no grid (P5 weak) |
| spray, drop on "go" | 0:23.95-1:15.83 | `spray_p7.wav` | P7 148 BPM -> 147.64 (x0.9976) | go 24.95: -1.3 / +7.7 ms (hit_big baked); landing 47.71: -6.0 / 0.0 ms (kick on the landing) |
| crash tense build | 1:14.33-1:25.10 | `crash_tense.wav` (+`_long`, 16 s) | P3 | hard stop at file end 10.77 s |
| crash drone + tick bed | 1:25.10-1:55.79 (+3 s tail) | `crash_bed.wav` + stems | P3 slowed | ticks on phone seconds (93.96 + k), onset err <= 0.8 ms |
| C_07 ticks + riser | 1:39.19-1:42.19 | `crash_c07_ticks_riser.wav` | sound design | - |
| release + main | 1:55.79-4:00.77 (+25 s tail) | `main_p4.wav` | P4 150 BPM -> 149.8 (x0.99867) | release: -0.2 / +7.8 ms; end (bar 78): -4.3 / +0.7 ms |
| "Time." sting | 4:01.07 | `time_sting.wav` | P3 kick boom | -5 ms design offset corrected |
| end montage | 4:15.02-4:41.52 | `montage_p1.wav` | P1 149.98 BPM | cuts vs eighth grid: worst 52 ms (see json `cut_snap`) |
| hero + conclusion + end card | 4:41.52-5:11.67 | `hero_outro_p8.wav` | P8 (x0.993) | lift 281.52: +0.2 / +7.2 ms; final hit 5:06.67: -1.0 / +1.0 ms |
Overlays: `hit_big` 0:05.80, `hit_small` 0:32.38 and 0:55.42, `riser_landing_3p78` from 0:43.93 (boom lands 0:47.71). hit_big is also baked into the spray/main/hero starts.
The kick-band onset of a baked boom reads ~7 ms late (slow 40-120 Hz rise); the broadband onset is the audible anchor.

## How the crash cue was built
- Tense (a): P3's 158.8 BPM sub pulse resampled with a tape wind-up (speed 1.0x -> 1.65x, i.e. pitch and pulse rise to ~262 BPM), level -20 -> 0 dB, plus a P4 high-band shimmer over the last 4.5 s and a half-speed P3 sub swell. It ends full-level with a 3 ms de-click, so it stops dead at 1:25.10.
- Bed (b): P3 at 0.5x and 0.25x, low-passed and tanh-saturated (so the harmonics are audible on laptop speakers), as a 10 s seamless loop; silent for the first 4.75 s (room tone, power-down SFX, dead silence), drone swells in at the card (1:29.85). Separate 1 Hz tick stem synced to the phone seconds. C_07 gets its own accelerating ticks + reversed P4 riser.
- Release (c): P4 downbeat on "Now." 1:55.79 with a hit_big slam; the 312 beats (78 bars) to 4:00.77 are fitted by a 0.13 % speed change, so the cut to TM_01 is also on a bar line.

## Speech sections and pieces
Speech-band (500-3000 Hz) share of the source piece: P3 3.5%, P5 20%, P4 25%, P7 29%, P8 34.5%, P1 42%.
Under speech: intro (P5), spray (P7; lines at 25.69-32.38, 36.18-43.93, 53.71-55.42, 67.92-74.33), crash (P3, ~3%), main (P4: 140.34-179.80, 185.3-189.0, 198.4-204.25, 210.25-220.21, 227.31-231.77), conclusion 288.52-298.67 (P8, the weakest choice under speech: duck 12-14 dB or crossfade to P7). Music-only: montage (P1, melody allowed), hero 4:41.52-4:48.52.

## Extending when the beat snap shifts times
Each beats json has an `extend` rule. Short version: spray/hero/montage have a loop block of 8-16 bars with similarity 0.84/0.85/0.95; the bed repeats exactly every 10 s (ticks are a separate 1.0 s stem); main has a 25 s tail handle (source keeps playing, trim at a bar line, no verified loop); tense can be trimmed from the head (16 s version provided). The anchors (go, landing, "crashed", "Now.", "Time.", lift) are fixed; everything else moves.

## Unverified / caveats
- Not listened to. Whether the tape wind-up reads as dread, whether the slam reads as a release, and whether P8's lift is audible as a lift (it rises over ~1 s, not a hard drop) are all unknown.
- Beat-grid confidence: P7 and P1 good (rms 10 / 19 ms); P4 weak (only 44% of onsets on the grid, rms 35 ms: cut on bars, not beats); P8 and P5 have no grid (onset lists only).
- Montage: the script cut times are multiples of 0.25 s; no 150 BPM grid puts them on beats (best eighth grid worst 52 ms). Editor should snap to the listed eighths.
- Bar 1 (downbeat) is unverified in P7 and P1; P4's was picked from chroma novelty.
- P8 starts at 190 BPM (felt 95) and the montage is 150: the hero is a hard music change by design.
- Licence unchanged: owner-supplied third-party game-music compilation, YouTube clearance not confirmed.

---
# v5 music (2026-11-13) - ONE continuous track (replaces v2-v4 scoring)
Owner: "the constant music changing is incredibly distracting". Rebuilt from P4 only (the 300 s, 150 BPM piece of the owner mix; it is an exact 360-beat / 144.000 s loop played twice). Picture locked to `timeline_v4.json` (315.023 s). **Unheard**: all checks are measurements.
Files in `/home/user/media/work/is350-long/music/v5/`: `music_v5_full.wav` (stereo 44.1 kHz, exactly 315.023 s, t=0 = timeline 0, UNDUCKED), `music_v5_crash_drone.wav`, `music_v5_crash_ticks.wav` (same length, aligned), `music_v5_map.json`, `music_v5_strip.png` (waveform + spectrogram with anchors).

## Structure in plain words
Thin low-band P4 warming up under the opening, opens to full band on "go" (18.147); plays straight through spray and scan (landing 40.874 on a strong beat); from 67.59 the same piece tape-winds up (speed 1.0 -> 1.8x, rising level) through its own build bars and stops dead on "crashed" 78.5075, exactly where its loop drop would have hit; silence (drone + tick stems, derived from slowed calm P4 bars) until "Now." 109.1115, where P4 re-enters on that drop bar and then plays on to the end: through Try again, the hard parts, a filter dip (not silence) under "Time" 235.99-246.96 that reopens as the build into the results card, the montage on P4's loud bars and build/breakdown bars, the loop drop again on the hero lift 274.691, the low-mid bars under the conclusion, a 3-bar pull-back and the final hit on the end card 310.018 with a reverb ring to ~314.4 s.
Audible piece changes: 0 (v4 had 8). Deliberate dynamic events: the crash stop and the "Now." re-entry (owner's crash drama), plus the Time dip and the ending.

## Anchor errors (ms, rendered file; grid phase from kick-band / broadband onsets)
go +6.4 / +2.0; landing -1.5 / -17.8; Now. +24.8 / -13.7 (one-sided); Time -17.7 / +8.3; card in +10.6 / +11.4; card out +7.9 / -1.4; lift +18.5 / -5.4; end hit -0.9 / +1.8.
Montage cuts (kick-fitted local grid): beats 6.0, -9.8, 2.0, -4.7; eighths -4.1, -8.6, -1.5. Cuts 1 and 3 sit on a beat with no kick (build bars). Nearest single onset is ambiguous (+-40 ms: P4 is a dense 16th pattern).
Tempo of the output: 150.44 BPM (opening to crash), 150.85 (Now. to card), 150.07 (card to lift), 149.5 (lift to end): at most 0.6 % tempo steps, continuous.

## Edits inside P4 and checks
- Jump back 56 beats (k398 -> k342) at 160.02, inside the T_08 speech over calm bars; loop wrap k568 -> k208 at 249.92 (identical audio, 12 ms crossfade). Step/loudness ratios at the edit points 0.15 and 0.86 (typical 0.61): no clicks measured.
- Crash gap is digital silence (max |x| 0.0). Peak 0.857 (stereo). Section LUFS: opening -19.7, spray -13.1, Now-Time -13.9, dip -20.5, card -16.3, montage -13.8, hero -13.1, conclusion -14.0, end card -21.9.
- Under speech the source bars used have 7-24 % speech-band share except P_04 (24-43 %), H_07, H_10/11, H_14 (33-43 %, worst): suggested ducks per section are in `music_v5_map.json` (-10 dB calm bars, -12 to -17 dB melodic bars).

## Caveats
Not listened to. The wind-up reaches +10 semitones (may read shrill). The end ring is a synthetic reverb of the final beat. Montage cuts 1 and 3 land on beats without a kick.
