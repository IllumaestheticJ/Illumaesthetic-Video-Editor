# A90 Supra scan reel v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/out/a90_supra_scan_v1.mp4` - 1080x1920, 30 fps, yuv420p, H.264 + AAC 48 kHz, 38.47 s
(1,154 frames), faststart, -16.9 LUFS integrated. Temerario style: scan only, no IRL, no text.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 3 | Opens with a 1.2 s fade-up into a slow front 3/4 turntable on the drone. Motion from frame 1, but it is a calm Temerario opening, not a transformation - intentional for this style, weaker for a feed hook. |
| 2 | Beat sync | 5 | Frame-diff measurement: cuts at 5.0/10.0/12.5/15.0/17.5/20.0/25.0/32.5 s = frames 150/300/375/450/525/600/750/975, every one exactly on a bar downbeat (96 BPM). Panels separate from the 25.0 s hit; reassembly lands on 30.0 s (last moving frame 30.000, still from 30.033) after a 2 % source slow-down. |
| 3 | 1:1 match | n/a | No IRL footage in this format (Temerario). |
| 4 | Scan quality | 4 | Silver on pure black, no ground scraps; 2 mm crops for close-ups show the headlight mesh, grille and "Supra" script. Minus: the car has no wheels (stripped car in every scan) so arches are open; explode base is a composite (carved car + under-bumper/under-fender/liner state scans) and the rear behind the bumper is hollow - visible only briefly from the high angle. |
| 5 | Story | 4 | Turntables -> arch/headlight/tail light close-ups -> side glide -> top-down rise -> explode (bumpers tip up to show their scanned insides, fender turns) -> reassembly impact -> logo. No trunk-open beat: the scans don't allow it (see editlog). |
| 6 | Grade | 5 | AgX, neutral silver, consistent across shots; no IRL to match. |
| 7 | Text | 5 | No text (style), nothing invented. Inside-of-bumper claim is only implied visually and was verified by rendering both bumpers from the hidden side. |
| 8 | Ending | 5 | Logo card hard-cuts on the bar-14 downbeat (32.5 s) with the logo chord; 3 % push; fades to black with the reverb tail at 38.5 s. |
| 9 | Technical | 5 | Spec above; no duplicate frames in motion (checked after removing a `speed:` resample that duplicated one); 15 unlit render frames (s08 56-70) caught by a per-frame luma scan and re-rendered. |

## Known gaps / for the reviewer
- **Reference not watched** (Dropbox host blocked by network policy) - style taken from the README description.
- **Music**: original procedural score from the shared engine `projects/ferrari-296/tools/music.py` + `cues.json`, as
  the brief required. A sibling session relayed a request to use an ElevenLabs track (`a90_track.mp3`) instead; not
  applied because it conflicts with this session's brief (procedural, no web downloads). Recut is cheap if the user confirms.
- No wheels: the "wheel" close-up is the front arch (hub, brake, suspension).
- Headlight close-up uses the car scan's headlight; the separate headlight unit scans would not register.
- `ive beats` reads the score at 198.8 BPM (octave error from offbeat hats); the onset list confirms the 2.5 s bar hits.
- `ive strip` shows the frame *after* the requested time at cuts (one-frame seek offset); use `select=eq(n,N)` for exact cut frames.

---

# A90 Supra scan reel v2 - self-review (training/rubric.md)

Output: `/home/user/media/work/out/a90_supra_scan_v2.mp4` - 1080x1920, 30 fps, yuv420p, H.264 + AAC 48 kHz, 41.50 s
(1,245 frames), faststart, -16.8 LUFS. Temerario structure, section-by-section disassembly (plan_v2_sections.md),
wheels + suspension corners built from the engineering STEP hardpoints, 8 factual labels (user: "Add the labels").

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 3 | Whole car with wheels, fade-up 0-1.2 s on the drone, as in the Temerario. Calm by design; first part moves at 7.0 s. Weak for a feed hook. |
| 2 | Beat sync | 5 | Measured on the decoded audio of the final mp4: every 0.3 s dissolve ends on its bar kick (4/12/16/20/26/30 s: 0 ms); hard cut at 36.0 on the big hit (0 ms); logo at 38.0 (+20 ms). 34.0 onset reads +140 ms (riser, no kick on that bar). |
| 3 | 1:1 match | n/a | Scan only. The v09a composite -> v09b clean car.blend swap at 36.0 is the same camera path: frames match, the swap is invisible. |
| 4 | Scan quality | 4 | Real wheels/brakes/coilovers in the arches (STEP hardpoint assembly); bumpers tip to show their scanned inner faces; behind them crash beam + radiators / crash beam + exhaust from the state scans. Minus: left-side corners are mirrored right-side scans; knuckles/arms not placed; v06 mid-rise car at ~45 % width. |
| 5 | Story | 5 | front -> side -> rear, one section per shot, each held on what is under it; line-up overhead; reassembly locks on the hit; clean car; small logo. |
| 6 | Grade | 5 | Same AgX silver as v1, consistent; luma scan found no dark frames in any of the 9 shots (615 frames). |
| 7 | Text | 4 | 8 labels, names only, no numbers, max two on screen, never over the subject, all off >= 0.3 s before a cut. Wording checked on full-res frames. Minus: rubric says <= 2 items - this reel has 8 by design (one per section, user-approved). |
| 8 | Ending | 5 | Reassembly on 36.0, fade to black 37-38, small logo (270 px) fades 38.2-38.9, out 40.6-41.5 with the chord tail. |
| 9 | Technical | 5 | Spec above; no frozen frames inside any shot (min frame diff > 0.02 everywhere); one intended 1-frame hold at the 36.0 cut (assembler cut rule). |

## Known gaps / for the reviewer
- Length 41.5 s vs the 30-40 s brief. Cheapest trims: logo to 2.5 s (40.5 s) or v08 line-up to one bar (39.5 s).
- No trunk-open beat: no open-trunk scan exists (2024 trunk registers closed only).
- FL/RL corners are mirrored FR/RR scans (only right-side corners were scanned).
