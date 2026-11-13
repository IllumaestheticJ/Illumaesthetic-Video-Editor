# Smart 450 "Hellkitten" reel v4: what changed from v3

Output `/home/user/media/work/smart-450/out/smart450_v4.mp4` (857 frames, 28.57 s) and `smart450_v4_meowlite.mp4` (same picture, meows 6 dB lower). Stems `stem_music.wav`, `stem_shopsound.wav`, `stem_meows.wav`. Copies in `preview/`. Rebuild: `python projects/smart-450-hellkitten/tools/build.py`.

**No placeholders remain**: a4_hellkitten (68 frames) and a5_xray (29 frames used, first 1.5 s of its 3 s) are finished renders and swapped in automatically.

- **New first shot**: a5_xray (red Hellkitten dissolving into the Smart inside it) with "THIS IS A SMART CAR?" baked in at full opacity from frame 0 (Inter Display Bold 112 px, two lines, in the clear black top band). The question "SHOULD WE BUILD THIS? / TELL US IN THE COMMENTS" is now at the end only. 4.r.1 moved into drop 3 (m 56-58); Street2 and Night2 are one beat each after it.
- **Meow drum kit**: 70 meows on 62 distinct moments (two 4-layer choirs count as 4 each): `meow_map.json` (time, sample, pitch shift, pan, gain, bar/beat, voice, kind, why). Kit: hats (first 0.16 s of a mew, off-beats), backbeat mids, "MRROW" lows doubling bar downbeats and the swap, rising 16th rolls into the scanner, the 1:1 cut, the swap and drop 3, two voices answering each other (A lower and left, B +3 semitones and right), choir on the Hellkitten reveal (m 44.5) and on the question (m 60, A C E A), stutter rolls in break 2, the long unimpressed meow on the question (m 61) as punchline, a small mew on the logo. +4 dB over v3, room reverb 14 %, kick sidechain up to -5 dB.

| section | meows |
|---|---|
| hook (m -4..0) | 4 |
| drop 1 (0..20) | 16 |
| break 1 (20..24) | 6 |
| drop 2 (24..48) | 19 |
| break 2 (48..56) | 11 |
| drop 3 + question (56..64) | 11 |
| logo (64..72) | 3 |

- **Level**: stem -19.4 LUFS, peak -3.7 dBFS; music stem -10.4 LUFS, peak -4.0. Master -10.1 LUFS, -1.2 dBFS peak. Meowlite -10.3 LUFS, -1.7 dBFS.
- **Onset accuracy**: every meow is placed on the lattice (16th grid) by sample; cross-correlating each known one-shot with the decoded stem gives a placement error of at most 0.07 ms; the mp4 decodes with 0.0 ms lag against the master. The audible onset of a one-shot (20 % crossing) sits 2-3.5 ms after the lattice time by construction. `out/meow_strip.png` shows the arrangement. Nobody has listened to it.
- **Meme cats** (owner-supplied, rights not cleared; `sfx.md`): huh_cat bottom right frames 12-44 next to the opening question; oiiaoiia_cat bottom left frames 397-441, its spin starts on the body-off swap (frame 406); yapapa_cat bottom left frames 535-585, first yell on the choir meow (frame 547); clapping_cat bottom right frames 744-766, after the long meow and before the logo. happy_cat not used (about 100 px tall in its frame). Meme audio muted (no stem_memes.wav). Keying: each clip keyed on its own measured background (huh BGR 80,193,85; the others about 0,245,0), CbCr distance with soft ramp, 1 px erode, despill, premultiplied downscale; checked on 3 frames per clip at crop size (out/meme_check_*.png) and in the cut at phone size: no green fringe or holes seen on the black cat; the spinning tabby is a dark blur by nature and looks like debris at 330 px.
- **Weaknesses**: the huh cat sits close to the x-ray car; A4 starts on A2's end camera, which clips the car at both edges for about 0.7 s before the body appears whole; meows are adult cats (no CC0 kitten recordings found, Wikimedia rate-limited); the density is high and unheard, so use the meowlite cut if it is too much; a5 is 3 s but only its first 1.5 s is used.

---
# Smart 450 "Hellkitten" reel v3 ("Should we build this?"): editor notes

Output `/home/user/media/work/smart-450/out/smart450_v3.mp4` (1080x1920, 30 fps, 857 frames = 28.57 s, H.264 High CRF 17, AAC 256k). Stems `out/stem_music.wav`, `out/stem_shopsound.wav`, `out/stem_meows.wav`, master `out/smart450_mix.wav`. Preview copy in `preview/`. Rebuild: `python projects/smart-450-hellkitten/tools/build.py`.

## Direction v3 (written before the build)
Beats m on the 160.00 BPM lattice, T(m) = 1.499 + 0.37583 m, cut frame = round(T*30). Message: a pitch asking "Should we build this?".

| shot | beats | frames | source | why |
|---|---|---|---|---|
| H1 | -4..0 | 0-44 | 4.r.1 studio render, push-in, text on the black band | the question and the Hellkitten inside 2 s (CGI, so text is allowed) |
| S5 | 0..2 | 45 | v_1632_12 intact car | drop 1: "here is the real car" |
| S6 S7 S8 | 2..8 | 68-134 | powder front, side, rear (spray hiss kept) | the car is prepared |
| S9 | 8..12 | 135-179 | scanner capturing | it gets scanned |
| S1 S13 S12 S4 | 12..20 | 180-269 | parts on the floor, front off, bare rear, hand on braces | stripped down |
| S17 S2 | 20..24 | 270-315 | scanner result, bare shell ending on the solved frame | break 1 (kick out), then the proof |
| S3 (A1) | 24..28 | 316-360 | 1:1 cut into the scan on drop 2 | "this is real engineering" |
| S10a/b (A2) | 28..40 | 361-495 | body on, swap to body off on beat 32, push | the scan with and without the body |
| S18 (A4) | 40..50 | 496-608 | a4_hellkitten: stripped scan becomes the textured Hellkitten body (PLACEHOLDER until rendered) | the answer to "what is it for" |
| R1 | 50..52 | 609-630 | Blueprint | body drawn over this Smart (break 2) |
| R2-R5 | 52..56 | 631-675 | 4.r.2, 4.r.4, 4.r.5, 4.r.6, one beat each on the build hits | quick run of renders |
| R6 R7 | 56..60 | 676-720 | RenderStreet2, RenderNight2 | drop 3 |
| R8 | 60..64 | 721-766 | RenderDay1 (strongest, decal), question on top | end on the question |
| LOGO | 64..72 | 767-856 | logo 720 px, 3.0 s | final downbeat and hold |

### On-screen wording (three options; option 1 is used)
1. Hook: "SHOULD WE BUILD THIS?" / "HELLKITTEN · DESIGN RENDER". Scan: "BODY ON" / "BODY OFF" with 29,997,021 / 29,998,690 TRIANGLES. Model: "HELLKITTEN" / "DESIGN CONCEPT". End: "SHOULD WE BUILD THIS?" / "TELL US IN THE COMMENTS".
2. Hook: "WOULD YOU DRIVE THIS?" / "SMART 450 · HELLKITTEN CONCEPT". End: "BUILD IT?" / "YES OR NO IN THE COMMENTS".
3. Hook: "BUILD IT OR BIN IT?" / "A SMART 450, REIMAGINED". End: "SHOULD WE?" / "VOTE IN THE COMMENTS".
No Dodge / Charger / Hellcat wording; no text on IRL footage.

## What the cut does (measured)
- Frame-exact: every frame of every shot sits on its timeline frame (cutpos.py); A2's swap is on frame 406 (beat 32).
- Cuts: 17 of 24 cuts are on a kick click, error -15.5 .. +14.5 ms (half a frame 16.7); the other seven are in breaks.
- Audio: master -10.0 LUFS, true peak -2.0 dBTP (WAV); delivered AAC -10.0 LUFS, -1.7 dBFS. Speech muted (audio_review.md).
- Labels: title items of 64-80 px (cap height 46-58 px at 1080 wide), mono sub 30-32 px, in the black band above the scan (checked on BODY ON / BODY OFF, hook and end frames); the end question sits on a dark plate over the buildings.
- Logo 720 px wide, held 3.0 s (8 beats), fades with the music (1.0 s).
- S1 and S6 slipped to the first sharp frame; S7 was already sharp by the Laplacian test but is a soft shot overall (low-texture floor). The first frame of the video is the sharp render H1.

## Meows
Sources and licences: `sfx.md` (three CC0 recordings: archive.org "Jorge the Cat Meowing", archive.org "meow!", one Wikimedia Commons clip by Tsester). They are adult cats pitched up 0-5.5 semitones toward the A-minor tones of the track (key A, estimated from chroma), not real kittens. 15 meows, own stem, room reverb (14 % wet), sidechain to the kick (up to -5 dB), stem peak -9.4 dBFS vs music -3.9. `meow_map.json` has time, sample, pitch shift, gain, beat/bar and the reason.

| # | s | beat | one-shot | shift (st) | peak dB | why |
|---|---|---|---|---|---|---|
| 1 | 1.69 | m 0.5 (bar 1, beat 1.5) | tiny_a | +3.0 | -14 | drop 1 = the first huge kick; a tiny polite mew answers it half a beat later, on the intact car |
| 2 | 7.70 | m 16.5 (bar 5, beat 1.5) | sad_e | +1.5 | -12 | bare rear (S12): a small sad meow after the bumper-less tail |
| 3 | 13.53 | m 32.0 (bar 9, beat 1.0) | big_f | +0.0 | -5 | THE body-off swap on the drop: where a tough car would rev, one big confident meow |
| 4 | 14.84 | m 35.5 (bar 9, beat 4.5) | short_b | +3.0 | -11 | motif A (answers the kick, off-beat) while the camera pushes in on the bare structure |
| 5 | 15.59 | m 37.5 (bar 10, beat 2.5) | short_c | +2.8 | -11 | motif B, two beats later |
| 6 | 16.34 | m 39.5 (bar 10, beat 4.5) | short_b | +3.0 | -11 | motif A again, a bar later: the repeating 2-bar motif |
| 7 | 18.22 | m 44.5 (bar 12, beat 1.5) | mid_d | +1.5 | -9 | the Hellkitten body arrives on the structure: a plain, unimpressed meow |
| 8 | 19.54 | m 48.0 (bar 13, beat 1.0) | long_i | +0.0 | -8 | break 2: the kick drops out and a lone meow sits in the gap |
| 9 | 21.79 | m 54.0 (bar 14, beat 3.0) | short_c | +2.8 | -14 | rising stutter into the render, 1/4 |
| 10 | 21.98 | m 54.5 (bar 14, beat 3.5) | short_b | +5.0 | -12 | rising stutter 2/4 (+2 semitones) |
| 11 | 22.17 | m 55.0 (bar 14, beat 4.0) | tiny_a | +7.0 | -10 | rising stutter 3/4 |
| 12 | 22.36 | m 55.5 (bar 14, beat 4.5) | chirp_j | +10.5 | -9 | rising stutter 4/4, the chirp |
| 13 | 22.55 | m 56.0 (bar 15, beat 1.0) | big_g | +0.8 | -5 | DROP 3: the Hellkitten render appears: one big confident meow exactly on the drop |
| 14 | 24.42 | m 61.0 (bar 16, beat 2.0) | long_h | -2.2 | -6 | the question 'SHOULD WE BUILD THIS?' is on screen: one long unimpressed meow |
| 15 | 25.55 | m 64.0 (bar 17, beat 1.0) | tiny_a | +3.0 | -13 | logo card: a last small mew on the downbeat |

Onset accuracy (decoded stem; the delivered mp4 decodes with 0.0 ms lag against the master): by the 20 % crossing used to trim the one-shots all meows are within 3.3 ms of the lattice (meow 11 excluded: it sits on the tail of meow 10); by a rise-slope definition within 14.8 ms (meow 2 has a slow attack), mean 5.2 ms. `out/meow_strip.png` shows waveform, spectrogram and cut marks. **Nobody has listened to this arrangement or mix**: the placement, pitch and loudness of every meow are unheard, the "ironic" timing is a design intent, and the reverb and ducking were set by numbers.

## Placeholders
S18 (A4, the Hellkitten model shot) is a placeholder: framing-preview frames held, with a PLACEHOLDER tag, until `renders/a4_hellkitten` has 68 frames; the next `build.py` swaps it in (A4 plays at 1.2x to fit 10 beats; the HUD label HELLKITTEN / DESIGN CONCEPT at 18.5 s must be re-checked against the real frames). Everything else is final. A3 was rendered but is not in this cut.

## Known weaknesses
- A4 will start on A2's end camera, but A2's end pose clips the car at both edges (R1 never re-keyed): visible in the last 1.3 s of S10b.
- The studio renders sit small in the frame (the car is wider than any 9:16 window), so H1 and R2-R5 have large black areas; R4's floor shows a lighter rectangle.
- Street and night stills are punched in 1.5-1.8x and are soft.
- Meows are adult cats pitched up; the long ones show their age.
- S6 and S7 are soft handheld shots; third-party marks as in v1 (DRIFTER stickers, wall poster, windscreen sticker).
- The 1:1 cut now lands on drop 2 instead of drop 1; it still reads as in v1 (door frame, braces, handle cup within 5-15 px; cabin and front wheel loose).

---
# v1 notes (kept)
# Smart 450 "Hellkitten" reel v1: editor self-review (training/rubric.md)

Output `/home/user/media/work/smart-450/out/smart450_v1.mp4`: 1080x1920, 30 fps, 798 frames = 26.60 s, H.264 High CRF 17, yuv420p, AAC 256k, faststart.
Plan: `direction.md`. Rebuild: `python projects/smart-450-hellkitten/tools/build.py`. Decisions: `editlog.jsonl`.

**Placeholders: none in this build.** A1 (S3, 39/39 frames), A2 (S10, 75/75) and A3 (S18, frames 1-29 used; render was still going) are finished renders.
If a scan shot is ever unfinished the build burns a small `PLACEHOLDER <id>` tag on a hold of the frames that exist plus the framing previews, and picks the real frames up on the next build.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Panels on the floor at 0 s (fast pan), the shell at 0.73 s, the 1:1 cut into the scan at 1.50 s on drop 1. Opening is a 0.73 s pan with motion blur and a tight punch-in. |
| 2 | Beat sync | 4 | All 20 cuts are frame-exact (cut k = round(T*30), checked by matching every frame of every shot in the delivered file). 17 cuts sit on a kick click: cut minus click -14.8 .. +14.5 ms (mean -2.3, half a frame = 16.7). The other three are S2 (riser hit), S10 (break, no kick) and S19 (build hit). The A2 swap is on frame 316 (measured). Caveat: the 35-110 Hz 30 % half-rise is 30-85 ms after the click on this track and unstable (rolling 16th kicks), so it is not the criterion. |
| 3 | 1:1 match | 4 | See below. Body, door frame, braces, handle cup, roof line, arch and fuel cap line up; interior and soft top do not; the front wheel is 15-20 px off. |
| 4 | Scan quality | 4 | Silver on black, no ground. The stripped scan has black holes in the cabin and sill (A1, A2, A3). A2 is small in frame for its first 1.6 s (car about 55 % of the width). |
| 5 | Story | 4 | Pieces, shell, 1:1 scan, hand on the braces, intact, powder (front, side, rear), scanner, body on/off, panel, bare rear and front, scanner result, front structure scan, Blueprint, render, logo. S9 is the stripped-session scanner footage placed in the assembled chapter (direction risk 6). |
| 6 | Grade | 4 | Every HLG clip tonemapped with the assembler's chain; mean luma of the 15 IRL shots 106-173, clipped pixels under 4 %. S11 reads blue (blue floor), S14 warm (shop lights). |
| 7 | Text | 4 | Three labels only (BODY ON / BODY OFF, FRONT END OFF, HELLKITTEN / DESIGN RENDER), none on IRL, static strings, STL header counts (29,997,021 and 29,998,690). All are clear of the car. A3's sub is fully typed for only about 10 frames. |
| 8 | Ending | 3 | Logo (720 px wide) pops in on the final downbeat, fades with the music. It is held for 1.04 s; the lessons favour about 2.4 s, and the direction allowed only 1.04 s. |
| 9 | Technical | 5 | 798 frames, no dup or dropped frames at cuts, 1080x1920, yuv420p, AAC. Master -10.0 LUFS, true peak -1.5 dBTP on the delivered AAC. |

## The 1:1 cut (frames 44 -> 45), honest read
`out/cut_44_45_side_by_side.jpg`, `out/cut_44_45_onion.jpg`. Frame 44 is the solved 26.0 s IRL frame, frame 45 is A1 frame 1 (both verified in the delivered file). The automatic check scored FAIL (median 13 px, p90 61 px); by eye:
- It reads as a 1:1 cut at phone size: same size, position and perspective for the whole body. The door-frame braces, the B-pillar handle cup, roof line, rear arch and the fuel-cap circle coincide within about 5-15 px at 1080 wide.
- It is loose in the cabin (the scan shows engine bay and a bare headliner where the clip shows the dash and soft top), the front wheel is 15-20 px off, and the lower brace is a few px off. The cut is carried by the door frame, not by the interior.
- The scan keeps moving (16 cm drift toward the nose), so the second frame already differs slightly; that is by design.

## Deviations from direction.md (all logged with reasons in editlog.jsonl)
- Music: edges snapped to the track's measured 160.00 BPM click lattice, segments resampled x1.00222 (3.8 cents slower). The direction's grid was 0.22 % slow and drifted -1 ms per beat (-45 ms by m 46).
- S1 window 504x896 at y0 184, x0 736 -> 900 -> 1100 (the direction's window shows a car's licence plate in the last frames).
- S14 window 978x1739 at x0 526, y0 261 (the direction's alternative; a bystander enters the corner of the full window).
- S17 in-point 0.48 s instead of 0.60 (the last frames were a blurred swing of the scanner).
- S10: the post-swap part plays at 0.537x (shot time 1.60-2.80); R1 was not re-keyed and the car touches the frame edge from 3.6 s. Min margin 35 px (target 40).
- S18: 0.75x (shot time 0-1.68 s); the car reaches the left edge from render frame 30. A3 sub is the triangle count, not CLAM MOUNTING POINTS (I cannot identify the clam mounts).
- S20: a 0.55 dark plate behind the label (it straddled the yellow arrow).
- Assembly: `ive assemble` is not used for the final encode (it drops every shot's first frame and shows the previous last frame twice; the swap landed on 315). `tools/concat_assemble.py` does hard cuts with exact frames; `project.yaml` is still an `ive` project and `ive director` runs on it.

## Known defects
- S1, S6 and S7 start with motion blur (handheld). S1 is a tight crop by design.
- Third-party marks in frame: DRIFTER stickers (S8, S9, S12), a wall poster (S15), a yellow sticker with Chinese characters on the windscreen (S16, S17), the moulding block "France DNF 12413" (S11).
- Shop sound is uncensored and unreviewed by ear: `audio_review.md` is a machine transcription. The music joins were not auditioned by ear either; they are phase-checked (every beat click lands on the grid across both joins, within 5 ms) and crossfaded 12 ms.
- A2 and A3 play slower than rendered (0.537x, 0.75x); the interpolation is minterpolate on a smooth camera move, no artefacts seen on the contact strips.
- The music licence is TikTok-only (music.md).

## Audio deliverables
`out/smart450_mix.wav` (master), `out/stem_music.wav`, `out/stem_shopsound.wav` (same gain as the master, pre-limiter), `out/audio_levels.json`.
Master -10.0 LUFS integrated, true peak -1.5 dBTP on the AAC (-1.8 on the WAV); music stem -10.4 LUFS, shop stem -16.5 LUFS.
