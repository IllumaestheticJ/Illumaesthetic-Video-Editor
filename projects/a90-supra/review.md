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

---

# A90 Supra scan reel v3 - self-review (training/rubric.md)

Output: `/home/user/media/work/out/a90_supra_scan_v3.mp4` - 1080x1920, 30 fps, yuv420p, H.264 + AAC, 56.2 s (1,686 frames),
-14.3 LUFS, true peak -4.9 dBFS. User-supplied track from its beginning, 21 bars (bar 2.6773 s), hard cuts on bar lines.
Brief: re-edit to this music; excruciating detail in how parts articulate and interact; incredibly detailed; scan artifacts
cut out and no parts left behind; underbody and interior highlighted; "the longer version".

| # | Criterion | Score | Evidence (tools/verify_v3.py on the delivered file) |
|---|---|---|---|
| 1 | Hook | 3 | Whole car with a camera drop for one bar, underbody from 2.7 s; first part comes off at 8.0 s. Calm opener under the riff. |
| 2 | Beat sync | 5 | 19 cuts, every one on its planned frame as one clean jump; kick attack within -36..+36 ms (about one frame) of each cut. |
| 3 | 1:1 match | n/a | Scan only. Same-camera swaps (ducts-removed state on the bar-7 cut, shell -> cabin crossfade, reassembled -> clean car) hold. |
| 4 | Scan quality | 4 | Cuts rebuilt so the removed-state scan decides each seam (build_v3); fitted panels are the car's own skin until they move; full-resolution meshes; cut edges smoothed; ~6k scrap islands dropped. Minus: fender opening and trunk-lip slot still have ragged/dark edges; the ducts-removed state is dark in its upper half (scanned with the top cover off). |
| 5 | Story | 5 | whole -> underbody -> front bumper -> radar grille nest -> crash beam -> ducts removed -> steering + brake -> suspension travel -> fender -> skirts -> sill -> cabin -> console -> rear five-link -> rear bumper -> rear structure -> line-up -> reassembly -> clean car -> logo. Each section one run; each removal followed by what it exposed. |
| 6 | Grade | 4 | AgX Medium High Contrast, exposure -0.7 (cabin -1.9): detail reads; no dark frames in any shot. Underbody shots are brighter than the rest. |
| 7 | Text | 4 | 16 labels, one per step, names only, no numbers, all legible on the delivered frames (3 on a dark plate where the scan fills the frame). Rubric's "<= 2 items" exceeded by design (reviewer rule: label each step). |
| 8 | Ending | 5 | Reassembly, invisible cut to the clean car on bar 20, fade, 720 px logo, audio fades with it. |
| 9 | Technical | 4 | Spec above, no black frames. Minus: the assembler's cloned frame leaves a 1-frame hold before 8 of the cuts. |

## Known gaps / for the reviewer
- Springs are deformed to follow the suspension travel (bench scans are at full extension); everything else moves rigidly on the
  solved hardpoints. Left-side corners are mirrored right-side scans. Front sway bar + two knuckle brackets not placed (no mate in the data).
- Steering, bump/droop and five-link travel are exact mechanism solves from engineering's STEP hardpoints, not captured motion.
- No trunk-open / hood / door states exist; the cabin is entered by a same-camera crossfade, nothing "opens".
- The A->B entry of the track falls on the front-suspension travel shot (bar 9) because the reel starts at the song's beginning.
- Length 56.2 s (user: "try the longer version"); a 16-bar cut is described in direction_v3.md.

## v3.1 (2026-11-14) - fender and rear bumper re-cut
User on v3: "fender cut isn't cut correctly, and rear bumper isn't cut correctly either - the rest is good."
Output: `/home/user/media/work/out/a90_supra_scan_v3_1.mp4` (same 56.2 s edit, music, labels and timing; -14.3 LUFS, peak -4.9 dBFS).
- Cause: build_v3 also removed car skin the removed-state scan lacked, which ran past the real shut lines (above the fender's
  top seam; into the trunk-lid edge and around the tail lamps) and left ragged openings and a dark slot under the lid.
- Fix (tools/recut_v3.py): the loose panel scan's own outline is the cut (car triangles within 5 mm of it, 12 mm vote); the
  bumper's flanks, where the loose scan spreads off the car, are decided by the bumper-off scan; islands wholly under a
  panel (number plate) leave with it. Checked on final-quality stills and on the re-rendered shots.
- Re-rendered: s10, s11, s11b, s14, s15, s16, s17, s18 (531 frames). Other 13 shots unchanged.
- Scan quality (criterion 4): 4 -> 4.5. Still open: a thin panel-gap line shows along the fender's top seam for the first
  frames of s10 (fender scan seated on the cut body), and the fender scan carries a mottled patch from the scan itself.

## v3.2 (2026-11-14) - parts out of the way during the suspension movement, console clears the tunnel
User on v3.1: "when [we] do the suspension movement areas, can you move the brake/parts completely out of the way? same with the
interior console section - it's blocking what's underneath it."
Output: `/home/user/media/work/out/a90_supra_scan_v3_2.mp4` (same 56.2 s edit; -14.3 LUFS, peak -4.9 dBFS; cuts unchanged).
- s09: the front dust shield comes off and leaves the frame first; bump/droop travel runs on the bare knuckle, strut and arms;
  hub bearing slides off at the end.
- s14: wheel, caliper, rotor and dust shield all leave the frame before the five-link travel.
- s13: the console unclips, lifts and leaves the frame; the camera holds on the tunnel and wiring, then glides to the rear deck.
- Known inconsistency: the rear dust shield is removed only inside s14 (it is back on the hub in s15-s18, seen from behind).
- s08 (steering sweep with the wheel on, then wheel/caliper/rotor off and parked) left as it was.
