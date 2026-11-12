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
