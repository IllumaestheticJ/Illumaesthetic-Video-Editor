# L1 thumbnails (1280x720 JPG + PNG, designed at 2560x1440)

Files: `/home/user/media/work/is350-long/thumb/thumb_{A,B,C}.jpg|png` (+ `_320x180.png` proofs, `_2560.png` masters, `thumb_options.jpg` contact). JPGs and the contact image are in `preview/`. Source script: `tools/make_thumbs.py` (re-run `python3 -I make_thumbs.py [A|B|C]`; swap in a different scan still via `scan_name`). All JPGs < 300 KB.

## Sources
- Scan: `renders/B5_stills/B5_front34_hero_alpha.png` (front-left 3/4; plate already flattened; contrast curve added). Side profile (`B5_side_profile_alpha.png`) was checked and rejected: the rear well is ragged and fully visible. `B5_halfhalf_FX30554` had not landed when I finished: swap it into A if it arrives (A already uses the same FX30554 11.011 s frame, so it is the natural upgrade).
- A: IRL = FX30554 @ 11.011 s (the solved match frame, Rec709 via `fx3a_slog3cine_to_709.cube`), 1080p proxy upscaled 1.33x lanczos + light unsharp. The plate (9JTY488) is pixelated and blurred.
- B: IRL = FX30541 @ 28 s (host, clear smile, thumbs up), graded the same way, crop upscaled 1.33x.
- C: scan only.
- Logo omitted everywhere (it carries its own red; the brief wants red on one element only). Add it small at top-left if the owner wants it.

## Text and why each number is true
| thumb | text | basis |
|---|---|---|
| A | "32 MIN" / "BET WAS 15" (15 in red) | 32 min elapsed = owner; the bet was 15 min = owner and said on camera (541 @ 26 s). |
| B | "15 MIN?" struck through in red, "32 MIN" | same two facts; strike = the bet vs the result. |
| C | "32 MIN" / "THEN IT CRASHED" (CRASHED in red) | 32 min = owner; the crash is in the brief and title. No more than that is claimed. |
No scanner specs, no triangle count, no "20 MIN" (kept off to avoid a second number). Text is only on black, never on IRL footage (CLAUDE.md rule), set in JetBrains Mono ExtraBold (numbers) and Inter Display Black (words), off-white #e8ecf2 with the single red #e22525. Nothing important sits in the bottom-right corner.

## Recommendation: B
Only B has a human face (clear readable expression), a visible conflict (bet crossed out vs the real time) and the scan as payoff, which is the strongest click logic for a story-led title. Runner-up A (clearest "real car becomes scan" hook, and it matches the video's signature 1:1 cut). C is the cleanest brand image but gives the least story.

## Alternative text (two per concept)
- A: "32 MIN, NOT 15" / "15 MIN BET. 32 MIN."
- B: "BET: 15. REAL: 32" / "15 MIN? TRY 32"
- C: "32 MIN + A CRASH" / "15 MIN BET. 32 MIN." (do not add "20 MIN" without also showing 32).

## Known weaknesses
- B's thumbs-up face reads happy, not "it crashed"; FX30541 @ 26 s is a more surprised alternative (same shot). The "15 MIN?" line is the smallest text and is only just legible at 320x180.
- Scan has ragged right-rear wheel arch visible at right in all three (hidden-ish at small size). Scan material is flat light grey, not the satin silver of the video renders (the stills are what exist).
- Source IRL is 1080p proxy upscaled; softness is acceptable at 1280 but an A or B from the 4K originals would be crisper.
- "BET WAS 15" in A is the second-smallest text at 320x180.

---
# v2: built on the guess (owner: "around how fast people think it takes"). Concepts D, E, F
Files: `thumb_D|E|F.jpg|png` (+ `_320x180.png`, `_2560.png`) in `/home/user/media/work/is350-long/thumb/`; contact `thumb_options_v2.jpg`; JPGs + contact copied to `preview/`. v1 files kept. 32 and 20 are NOT shown in D/E/F. No triangle counts anywhere. Plate blur removed (owner v2); `thumb_A` was regenerated without the blur.

## Guess text and transcript source (`transcripts/FX30541.json`)
- "2 HOURS?": "Two hours." 2.4 s and "I'll say two hours." 17.5-18.1 s (a crew member, not the host).
- "30 MIN?": "Maybe 30 minutes." 22.1-22.7 s (the man in the black polo).
- "15 MIN?": host, "I think I can do it in less than the length of a YouTube video... 15 minutes" 26.3-28.9 s (+ 541 @ 26 s per brief).
Note: the three guesses come from three different people; no thumbnail attributes them to the host except E's "15 MIN?", which is his own line.

## Concepts
- D: scan hero (B5_front34_hero) + three equal "tags" (2 HOURS? / 30 MIN? / 15 MIN?) so the viewer picks; the only red is a stopwatch glyph (drawn, not footage).
- E: host FX30541 @ 26.6 s (questioning, looking up; 1080p proxy, upscaled 1.33x) + huge "15 MIN?" (red "?"), small scan. Alt: swap the text to "2 HOURS?" (arguable claim) but then the face would imply the host said it.
- F: "HOW LONG?" + red "00:00" in a black band (no text over footage); below it FX30554 @ 11.011 s real car split diagonally with the `B5_halfhalf_FX30554` scan (landed; onion check shows it registers 1:1). Small guesses line "2 HR · 30 MIN · 15 MIN" in the band. The typographic "00:00" replaces the real phone-stopwatch frame (FX30541 72-75 s): the phone is sharp but the frame is mostly bokeh and only 1080p.

## Pick: E for CTR (face + one argue-able number), D as the clearest "pick one" mechanic, F as the on-brand 1:1 reveal. Recommend E.
Alt text: D "2 HR? 30 MIN? 15 MIN?" / "HOW LONG? + 3 tags"; E "2 HOURS?" / "LESS THAN 15?" (not true: he said 15, avoid); F "HOW FAST?" / "00:00 GO".
Weaknesses: F's guesses line is unreadable at phone size (decorative); F/E IRL is soft 1080p; plate legible in F by owner's choice; D has no human; scan stills are flat grey with a ragged right-rear arch.

---
# v3: F developed (owner: keep F, add the 3D scanner picture, say "3D scan")
Files: `thumb_F1|F2|F3.jpg|png` (+ `_320x180.png`, `_2560.png`), contact `thumb_options_v3.jpg` (JPGs + contact in `preview/`; all JPGs < 300 KB). Code: `tools/make_thumbs.py` (`split_base`, `scanner_cut`, `concept_F1..F3`).
Common: black top band (text only there), real car left / silver scan right, diagonal seam, registered 1:1. Car half rebuilt from the **4K** FX30554 @ 11.011 s (graded with `fx3a_slog3cine_to_709.cube`) and the `B5_halfhalf_FX30554` scan (onion-checked). Plate unblurred (owner rule). Red = the "00:00" stopwatch text only. Bottom-right corner empty of anything key. No numbers beyond the guesses 2 HOURS / 30 MIN / 15 MIN (transcript FX30541 2.4, 17.5, 22.1, 26.3 s).
Scanner picture source: **FX30545 4K @ 84 s** (`-noautorotate`), the white handheld unit with its screen ("Opening project" UI, blue power ring), no hands, no brand logo visible. FX30555 (host holding it) was tried: the white body against bright sky/building with dark lens holes did not grab-cut cleanly, so it was dropped. Cut-out: luminance threshold on the blurred 4K frame, morphological close, largest contour filled, opened/eroded 5 px, 1.2 px feather; edges checked at 100 % (clean on the rim; the far/left end of the body is naturally out of focus in the source). Subtle drop shadow added.
| | wording | scanner | extras |
|---|---|---|---|
| F1 | HOW LONG TO / 3D SCAN A CAR? | cut-out, large, foreground bottom-left (partly over the road and the car's front-left) | none |
| F2 | 3D SCAN A CAR / IN ___ MIN? | cut-out, smaller, bottom-left | three big guess tags 2 HOURS? / 30 MIN? / 15 MIN? on the black scan side |
| F3 | HOW FAST CAN WE / 3D SCAN THIS? | picture-in-picture photo (FX30545 @ 104 s: hands on the scanner, its screen showing the car being built), top-left over the road | none |
Pick: **F2** (says what is timed, keeps the owner's "what people THINK" idea with legible tags, scanner recognisable). F1 is the cleanest; F3 shows the scanner in use but the screen content is small.
Weaknesses: scanner body's left end is soft/pale against the sand road (it is out of focus in the source); scanner overlaps the car's front-left corner in F1/F2; tags in F2 are 12 px tall-ish at the 320x180 proof (readable, small); the plate is partly covered by the seam/scanner in some variants; F3 PiP covers the left road area; "___" blank in F2 reads as a gap at phone size.

---
# v4: F2b / F2c, whole scanner standing on its base (owner: "put the bottom of the scanner back in")
Source frame: `/home/user/media/work/is350-long/thumb/scanner4k/f_010.jpg` (FX30542, about 5-6 s of the lead's 4 fps extract, Rec709 graded, 4K): the full handheld unit on its base on the workbench, sharpest of f_008-f_013 with the least spray-gun overlap. Matte: hand polygon + grabCut refinement + luminance clean-up for the black base vs bench, grip loop kept see-through, 1 px choke + 1.6 px feather, edges checked at 100 %. Only reconstruction: the rear end of the body is hidden by the spray gun's grille in every frame, so the rear is closed with a simple rounded cap (a ~50 px shave of white surface at 4K); nothing else invented. Own soft ground shadow added; the bench contact shadow is not used. Matte inputs saved in `tools/matte/`; `leo_cut()` / `stand_on_ground()` in `tools/make_thumbs.py`.
- F2b: scanner 665 px wide (26 % of frame), standing at the left, clear of the headlight and plate. F2c: 790 px, overlapping the car's lower-left bumper corner for depth. Title, red 00:00 and the four tags (2 HOURS? / 30 MIN? / 15 MIN? / LONGER?) unchanged; bottom-right empty.
- Weaknesses: scanner is a touch softer than the 4K car (shallow depth of field in the source); its shooting angle/lighting differ slightly from the road scene; spray-gun-hidden rear end is a simple cap; ground shadow is subtle.
