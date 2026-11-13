# S3 "Scanning a Smart car down to its skeleton": scene direction

Scene director, 2026-11-13. 9:16, 1080x1920, 30 fps, **26.6 s** (798 frames). Mostly IRL, three scan shots, two design stills, logo.
Read: brief.md (incl. the 2026-11-13 Hellkitten section), clips.md, scan_shots.md, music.md, beats.json, pitch S3, feedback.jsonl, editlog, lessons.
Looked at: the A1/A2/A3 preview frames (`scan3d/look/pv_*`), the A1 onion (`match/check_str_v1852_56_26.0.jpg`), the state splats,
all six design stills, and first/mid/last frames I pulled from every IRL span used below (not tonemapped, 9:16 window drawn on).
Not looked at: finished A1/A2/A3 renders (A1 17/39, A2 17/75, A3 0/39 when written), anything assembled.

## 1. Feature inventory

### What was scanned (all four states share one Artec frame; ICP moves < 1.1 mm, editlog)
| scan (STL header count) | what it holds | cast? | why |
|---|---|---|---|
| Full Car Assembled (29,997,021) | body panels on, no window glass, soft top open, wheels on | yes, A2 first 4 beats | the only "body on" state; whole car reads cleanly in the preview |
| Fully Stripped (29,998,690) | doors, front clam, bumpers, lamps off: door-aperture frame with diagonal braces, front structure (cross beam, lamp openings, cooling pipes), bare rear | yes, A1 / A2 / A3 | richest state: this is the "skeleton" of the title and the state every late clip shows |
| Clam and Trunk Mounting (19,995,154) | partial capture (splat: side and front, ragged at the rear) | no | no shot rendered from it; partial captures only work when they fill the frame; no trunk-open scan confirmed, so no trunk beat (rule D) |
| Door Card Top Edge (14,996,696) | partial capture of the door area (splat: nose and roof missing) | no | same; the door aperture is already A1's subject |

Weak data: A1 match is loose on the folded soft top and cabin clutter (silhouette median 13 px, p90 61 px, tool says FAIL; braces, sill,
handle cup, fuel cap within 5-15 px). A2's rendered end pose (4.8 s) clips nose and tail. A3's last frame puts the right arch on the frame edge.
No plate on the car. No Hellkitten scan exists: the Hellkitten appears only as the design stills.

### What is on camera (by region and state)
| region | assembled / powder (16:32-16:45) | stripped (16:59 onward) |
|---|---|---|
| whole | v_1632_12 0.0-1.2 (front 3/4, black, intact) | v_1852_56 25.3-27.4 (shell, steadiest), v_1729_10 0.0-0.4 |
| front | v_1634_19 14-16 (spray, black to grey) | v_1852_56 6-8 (on the jack), v_1722_25 24-27 (spray), 32.5-37 (screen goes matte), v_1724_26 1:46.5-1:49.5 (scanner) |
| side | v_1634_19 6.0-8.8 (mist on door) | v_1857_58 0.3-4.8 (hand on the braces) |
| rear | v_1634_51 0-2.5 (tail lamp spray), v_1724_26 10.3-13.5 (scanner screen over the rear window) | v_1712_33 19.0-19.9 (dead-on bare rear) |
| parts off the car | - | v_1852_56 20.8-21.7 (panels on floor), v_1659_53 1.5-3.2 (inside of a panel, moulding marks) |
| scanner | v_1724_26 10.3-13.5 (live green screen, large) | v_1729_10 0.6-1.6 (Projects list with car thumbnails) |
Not on camera anywhere: a panel leaving the car in one take. A2's state swap is that beat.

### Design stills (CGI, `/home/user/media/smart-hellkitten/design/`, 1440x1440)
Blueprint.jpeg: grey side view, the Smart drawn inside the new body, nose left. RenderDay1: red car, rear 3/4, rooftop car park, kitten
decal on the door, car = 51 % of the still's width. Street1/2: car small or motion-blurred. Night1: car tiny. Night2: front 3/4, lit lamps, car 30 % of width.
**Pick: RenderDay1.** Largest car, the decal explains the name, a full-height 9:16 window holds the whole car, and it faces the same way as the Blueprint.

### Richness score
Stripped whole car / side frame: 2 states + 1:1 match + best steady footage = richest. It gets drop 1 (the 1:1) and drop 2 (the state swap).
Stripped front: 1 scan detail + 4 IRL spans = second; it carries the run into the payoff. Assembled car: one state, one chapter of 2-beat shots.

## 2. Length and music

**Remove two 8-beat blocks and take 8 more beats of the drop from the source track.** Picture runs 26.59 s; logo downbeat at 25.552 s.

Original grid: t = 1.499 + 0.37583 n (n = 0 at drop 1). Fitted grid: **T(m) = 1.499 + 0.37583 m**, m = -4 ... 64.
| removed / added | original beats | clip time | why |
|---|---|---|---|
| removed | n 4-12 (drop 1) | 3.002-6.009 | the measured loop point in beats.json; the splice sits under the picture cut at m 4 |
| removed | n 58-66 (break 2, pad middle) | 23.297-26.304 | 6 s without a kick is too long here; keeps the kick-out at n 56 and the build hits at n 68/70/71 |
| added | n 72-80 (drop 3 continues) | source 63.559-66.566 | the render lands ON drop 3 and the logo gets the next downbeat. Measured on harder.m4a: full kick level holds from 63.56 s to at least 73.7 s |

Music v2 from `harder.m4a` (source time = clip time + 35.0), 12 ms crossfades at the two joins, same -6 dB + limiter chain (`level=disabled`):
`35.000-38.002` + `41.009-58.297` + `61.304-67.606`, 1.0 s fade out from 66.60. Length 23.588 + 3.006 = 26.59 s. Re-run the onset check across both joins.

Mapping: m <= 4 is n = m; m 4-50 is n = m + 8; m >= 50 is n = m + 16.

**Fallback with the existing WAV only (no new audio):** remove just n 4-12 from `smart450_short.wav`. Same 26.59 s, same picture cuts.
Break 2 is then 16 beats: A3 tail, Blueprint and render ride the pad, the build hits fall at m 60/62/63 inside the render, logo on drop 3 at m 64.
Weaker (the render enters with no hit) but needs nothing new.

| m | T (s) | frame | music | picture |
|---|---|---|---|---|
| -4 | 0.000 | 0 | riser | S1 |
| -2 | 0.747 | 22 | riser (hits 1.12, 1.32) | S2 |
| **0** | **1.499** | **45** | **DROP 1** | **S3 = A1, the 1:1 cut** |
| 4 | 3.002 | 90 | drop 1 (splice) | S4 |
| 8 | 4.506 | 135 | drop 1 | S5 |
| 10 | 5.257 | 158 | | S6 |
| 12 | 6.009 | 180 | | S7 |
| 14 | 6.761 | 203 | | S8 |
| 16 | 7.512 | 225 | | S9 |
| 20 | 9.016 | 270 | break 1, kick out | S10 = A2, body on |
| **24** | **10.519** | **316** | **DROP 2** | **A2 state swap (inside the shot)** |
| 30 | 12.774 | 383 | drop 2 | S11 |
| 32 | 13.526 | 406 | | S12 |
| 34 | 14.277 | 428 | | S13 |
| 36 | 15.029 | 451 | | S14 |
| 38 | 15.781 | 473 | | S15 |
| 40 | 16.532 | 496 | | S16 |
| 44 | 18.036 | 541 | | S17 |
| 46 | 18.787 | 564 | drop 2, last 2 beats | S18 = A3 |
| 48 | 19.539 | 586 | break 2, kick out | (A3 continues, label up) |
| 52 | 21.042 | 631 | build hit | S19 Blueprint |
| 54 / 55 | 21.794 / 22.170 | 654 / 665 | build hits | (Blueprint) |
| **56** | **22.545** | **676** | **DROP 3** | **S20 Hellkitten render** |
| **64** | **25.552** | **767** | **final downbeat, fade** | **S21 logo** |
| end | 26.593 | 798 | | |

## 3. Scenes in order

Order logic: cold open on the richest feature (stripped shell, 1:1 into its scan on drop 1), then the process in true order
(intact, powder, scan, comes apart, powder and scan again), then the payoff (scan detail, Blueprint, render, logo).
Travel: assembled chapter front -> side -> rear; stripped chapter rear -> front, and it stays on the front to the end.
Crop windows are source pixels on the upright frame; all are scaled to 1080x1920. x0 values are read off 640 px-wide frames: accurate to about 30 px, check them.
Audio: "under" = shop sound about 14 dB below the music; "up" = about 6 dB below. Scan shots and stills are music only.

| # | m (beats) | T in-out (s) | source, in-out (s) | section | 9:16 framing | viewer learns | audio |
|---|---|---|---|---|---|---|---|
| S1 | -4 to -2 (2) | 0.000-0.747 | v_1852_56 20.80-21.53 | parts on floor | punch-in, window 576x1024 at y0 56 (drops the doorway vehicles and their plates at the top); the camera pans, so track x0 700 -> 910 -> 1210 | this car is in pieces | shop under |
| S2 | -2 to 0 (2) | 0.747-1.499 | v_1852_56 25.27-26.033 | stripped side | fixed window 607.5x1080 at **x0 760** (the solved match window; no tracking, no stabilising). Must end on the 26.0 s frame: trim `in`, never `out` | the bare shell and its door frame | shop under, hard out on the cut |
| S3 | 0 to 4 (4) | 1.499-3.002 | **A1** shot time 0.00-1.50 | stripped side (scan) | as rendered; frame 1 is the solved camera | the same frame as a 3D scan | music only |
| S4 | 4 to 8 (4) | 3.002-4.506 | v_1857_58 1.20-2.70 | stripped side | window 608x1080, x0 520 -> 600 (fingertip, diagonal brace and regulator inside) | the braces are real; scale of a hand | shop under |
| S5 | 8 to 10 (2) | 4.506-5.257 | v_1632_12 0.00-0.77 | whole, assembled | window 608x1080 at x0 370: nose, both lamps, screen, front wheel; the tail is out of frame on purpose (the whole car is 1000 px wide, a 9:16 window is 608); keeps the bystander out | rewind: the car before, black and intact | shop under |
| S6 | 10 to 12 (2) | 5.257-6.009 | v_1634_19 14.50-15.23 | front, assembled | window 608x1080, x0 560 -> 450 (headlamp and the black-to-grey edge) | powder: black paint turns matte grey | shop up (spray) |
| S7 | 12 to 14 (2) | 6.009-6.761 | v_1634_19 6.90-7.67 | side, assembled | window 608x1080 at x0 500 (gun, mist, door) | the mist itself | shop up |
| S8 | 14 to 16 (2) | 6.761-7.512 | v_1634_51 0.15-0.88 | rear, assembled | native vertical, no crop | tail lamp goes matte | shop up |
| S9 | 16 to 20 (4) | 7.512-9.016 | v_1724_26 11.00-12.50 | rear + scanner | 3:4 centre crop 990x1760, x0 85 (5 % left of centre so the scanner housing stays whole) | the scanner: green = captured | shop under |
| S10 | 20 to 30 (4 + 6) | 9.016-12.774 | **A2** shot time 0.067-3.833; swap (shot time 1.60) on frame 316 | whole (scan) | as rendered; whole car in frame at every frame used, see request R1 | the scan with the body on, then the body is gone | music only |
| S11 | 30 to 32 (2) | 12.774-13.526 | v_1659_53 1.90-2.67 | part off the car | **rotation fix** (`-noautorotate`, then `hflip,vflip`), window 608x1080 at x0 540 (moulding marks centred) | what came off: the inside of a body panel | shop under |
| S12 | 32 to 34 (2) | 13.526-14.277 | v_1712_33 19.05-19.78 | rear, stripped | window 608x1080 at x0 540: rear window, exposed loom, exhaust; tail lamps cut at both edges on purpose | the bare rear | shop under |
| S13 | 34 to 36 (2) | 14.277-15.029 | v_1852_56 6.00-6.77 | front, stripped | window 608x1080, x0 600 -> 630 | front end off, nose on the jack | shop under |
| S14 | 36 to 38 (2) | 15.029-15.781 | v_1722_25 24.60-25.33 | front, stripped | 3:4 window 1125x2000 hard right (x0 379); if a bystander shows top right, use 978x1739 at x0 526, y0 261 | the bare structure gets powdered too | shop up |
| S15 | 38 to 40 (2) | 15.781-16.532 | v_1722_25 35.00-35.77 | front (windscreen) | 3:4 centre crop 1125x2000 at x0 190 | glass turns matte so the scanner can see it | shop up |
| S16 | 40 to 44 (4) | 16.532-18.036 | v_1724_26 107.30-108.80 | front, stripped | punch-in 849x1510, bottom-aligned (y0 250, drops the people in the doorway), x0 about 240 | scanning the bare front | shop under |
| S17 | 44 to 46 (2) | 18.036-18.787 | v_1729_10 0.60-1.37 | scanner result | window 608x1080 at x0 590: the screen with three car thumbnails is whole, the lens end is cut | the scan is on the device | shop under |
| S18 | 46 to 52 (6) | 18.787-21.042 | **A3** shot time 0.00-2.233 | front, stripped (scan) | as rendered; frames 1-34 only (frame 39 has the right arch on the edge) | the front structure in detail | music only |
| S19 | 52 to 56 (4) | 21.042-22.545 | Blueprint.jpeg | design | car is 1114 px wide: crop x 98-1308, scale to 1080 wide, pad top and bottom with the still's own flat grey (sample it; no blur). 3 % push-in | the new body drawn over this Smart | music only |
| S20 | 56 to 64 (8) | 22.545-25.552 | RenderDay1.jpeg | design | window 810x1440 at x0 310 -> 778x1383 at x0 326, y0 44 (4 % push, car fully in frame with about 20 px side margin at the end) | what the scan is for | music only |
| S21 | 64 to end | 25.552-26.593 | logo card | - | about 650-720 px wide (lessons: smaller was "too small") | - | music tail |

### On-screen text (scan shots and CGI stills only; never on IRL; two items at most)
Use ScanHUD `label` (not `counter`: it stops at 99.9 %), `shadow: true`, sub never empty. Numbers are the STL header counts.
| shot | title / sub | in - out (frames) | where |
|---|---|---|---|
| A1 | none | - | 45 frames is too short to read a count and the cut should land clean |
| A2, body on | `BODY ON` / `29,997,021 TRIANGLES` | 273 - 312 | black band above the car, y about 250-420 |
| A2, body off | `BODY OFF` / `29,998,690 TRIANGLES` | 316 - 378 (on with the swap) | same place, so only the words change |
| A3 | `FRONT END OFF` / `CLAM MOUNTING POINTS` | 586 - 626 (enters on the kick-out) | top band, y about 150-330; check all of its window against the car |
| Blueprint | none | - | the picture explains itself |
| RenderDay1 | `HELLKITTEN` / `DESIGN RENDER` | 699 (m 58) - 760 | lower left on the asphalt, above the bottom 20 %; check it against the yellow arrow, else top with a dark plate |
"DESIGN RENDER" stays on for the whole label: it is what tells the viewer this is not a photo. No Dodge / Charger / Hellcat wording on screen.
A3's sub is only allowed if the clam mounts are visible in the finished A3 frames; if not, use `29,998,690 TRIANGLES`.

### Section check (rule B)
Stripped side: S2-S3-S4, once. Assembled front, side, rear: S6, S7, S8, once each. Parts off the car: S1 (many on the floor) and S11
(one panel's inside face, macro) are different subjects. Stripped rear: S12. Stripped front: S13-S18, one run. Whole car: S5 (IRL, assembled) and
S10 (scan, both states). Scanner: S9 (live capture) and S17 (result list) are different screens.
A2's rendered push ends on the door aperture, which S2-S4 already covered. It is cut at shot time 3.83 s, before that close-up.
The pitch's hand-on-structure shot moved from the end to S4 so the door frame is one sequence.
Clips used in more than one span, never the same frames: v_1852_56 (S1, S2, S13), v_1634_19 (S6, S7), v_1722_25 (S14, S15), v_1724_26 (S9, S16).
Not used: v_1620_30, v_1633_51, v_1640_44, v_1645_19, v_1728_34.
No camera rotation exists to fill time: A1 drifts 16 cm, A2 is a state swap and push, A3 a short slide.

## 4. Requests to the 3D agent (none blocks the cut)
- **R1, A2.** Frames 26-75 were not rendered when this was written, and `sample()` in shot.py is piecewise, so frames 1-25 do not depend on the last key.
  Re-key the last key before A2 resumes: from the swap to shot time 3.83 s keep the whole car in frame with at least 40 px margin and turn toward
  the nose (az 52 -> about 38) so the front structure opens up into A3. No door-aperture close-up. Only frames 1-61 are used.
  If A2 stays as specified, it is still usable to 3.83 s only if nothing touches the frame edge; otherwise play the post-swap part at 2/3 speed
  (src_fps 10 for that part, shot time 1.60-3.10).
- **R2, A1.** Only frames 1-23 are used, plus handles: stopping A1 at frame 27 frees CPU for A3.
- **R3, A3.** Check frames 1-34 for edge touches (right arch). Confirm what the label may name.
- **R4, optional.** A fourth scan shot: the Stripped scan in side view, nose left, posed to the Smart inside Blueprint.jpeg, for a second 1:1 cut
  scan -> Blueprint at m 52. It would make the payoff read at once. Skip it if CPU is short; S18 -> S19 is a plain cut on the build hit.

## 5. Cut list for the editor
Cut k sits on the frame in column 1 (= round(T x 30)). Give every clip an exact frame count; first clip one frame short if `ive assemble` is used
(lessons), or use `projects/honda-s2000/tools/concat_assemble.py` with `frames:`. All cuts are hard cuts. HLG clips tonemapped; the 3:4 clips are SDR.
| start frame | frames | id | src | in (s) | notes |
|---|---|---|---|---|---|
| 0 | 22 | S1 | v_1852_56 | 20.800 | tracked punch-in, top 56 px dropped |
| 22 | 23 | S2 | v_1852_56 | 25.267 | out = 26.033 exactly; window x0 760 fixed |
| 45 | 45 | S3 | a1_match_str | 0.000 | 15 fps source, interpolated; first output frame = render frame 1 |
| 90 | 45 | S4 | v_1857_58 | 1.200 | |
| 135 | 23 | S5 | v_1632_12 | 0.000 | |
| 158 | 22 | S6 | v_1634_19 | 14.500 | |
| 180 | 23 | S7 | v_1634_19 | 6.900 | |
| 203 | 22 | S8 | v_1634_51 | 0.150 | native vertical |
| 225 | 45 | S9 | v_1724_26 | 11.000 | |
| 270 | 113 | S10 | a2_body_on_off | 0.067 | swap must show on output frame 316: measure it in the assembled file; replace the blended frame at the swap (freezeframes, c5 lesson); do not move it with `speed:` |
| 383 | 23 | S11 | v_1659_53 | 1.900 | rotation fix |
| 406 | 22 | S12 | v_1712_33 | 19.050 | |
| 428 | 23 | S13 | v_1852_56 | 6.000 | |
| 451 | 22 | S14 | v_1722_25 | 24.600 | |
| 473 | 23 | S15 | v_1722_25 | 35.000 | |
| 496 | 45 | S16 | v_1724_26 | 107.300 | |
| 541 | 23 | S17 | v_1729_10 | 0.600 | |
| 564 | 67 | S18 | a3_detail | 0.000 | |
| 631 | 45 | S19 | design/Blueprint.jpeg | - | still, 3 % push |
| 676 | 91 | S20 | design/RenderDay1.jpeg | - | still, 4 % push |
| 767 | 31 | S21 | logo card | - | |
| 798 | | end | | | |
Audio: music v2 (section 2) from frame 0. Shop sound from each IRL clip's own span, 2-frame fades at each end, cut to silence on frames 45, 270, 564.
Deliver the shop-sound stem separately as well: the owner reviews the language himself (feedback.jsonl), so nothing is censored.
Before assembly: first / middle / last contact sheet of all 21 shots (rule A); per-frame luma scan of A1-A3; `ive director` after assembly.
After assembly: check every cut against the kicks decoded from the delivered file, and frames 44/45 side by side.

## 6. Risks
1. **The 1:1 cut is loose** (tool FAIL, p90 61 px on the soft top and cabin). It lands on the loudest hit of the reel; if it reads soft at full
   size, nothing else in the reel can replace it. Judge frames 44 and 45 by eye before anything else.
2. **A1, A2 and A3 are not finished** and A3 has not started. The cut needs A1 to frame 27, A2 to frame 61, A3 to frame 34.
3. **Music v2 is new audio.** The extension was checked only as per-beat level on the source, not by ear, and neither join has been auditioned
   (the break-2 join is inside a riser and may step in pitch). The fallback WAV edit keeps the picture cut unchanged.
4. **Crop windows are estimates** from small frames. S1 (fast pan, plates at the top of the doorway), S5 and S12 (car wider than the window) and
   S14 / S16 (bystanders near the top edge) need the contact-sheet check.
5. **Shop sound**: S9, S14, S15, S16 come from the clips clips.md marked "do not use" for bystander talk; the owner's later note says keep it.
   I did not listen to these spans. Two-beat snippets of speech may sound like noise; the owner decides.
6. **S9 is out of order in fact**: the only large scanner-screen footage was shot during the stripped session. The window shows the rear glass and
   soft top, where the two states look alike, but it is not footage of the first scan.
7. **Logo is 1.04 s.** Lessons favour about 2.4 s; a longer hold needs a longer fade from the source.
8. Three clips carry wrong rotation tags; only v_1659_53 (S11) is used. Third-party marks in frame: DRIFTER stickers (S8, S9, S12), a
   wall poster (S15), the moulding block with a part number (S11).

## 7. Open questions
- Is "CLAM MOUNTING POINTS" right for what A3 shows? (Wording from the 17:12 narration and the scan file name; I have only seen 30 % previews.)
- Credit the designer on the render label, or name only? Default here: name only.
- The earlier editlog entry says Challenger-style, the owner says Charger. Nothing on screen depends on it; the caption will.
