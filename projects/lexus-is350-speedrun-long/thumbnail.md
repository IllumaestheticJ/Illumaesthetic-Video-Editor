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
