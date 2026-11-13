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
