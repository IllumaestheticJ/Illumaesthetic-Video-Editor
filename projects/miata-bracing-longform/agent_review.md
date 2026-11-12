# Independent review: MiataBracing_review_v2.mp4 (9:42.3, script v2)

Reviewed 2026-11-12 against `Strut Spread.xlsx`, all 9 PDFs (39 pages rendered), the cards, contact sheets of every
narrated IRL shot and every card, `build.py` TL/NAR, and the owner transcript. No existing file was modified.

## Verdict
1. **Not ready for voice.** Every tower number and percentage matches the xlsx, but the conclusions lean on gaps (0.2-0.5 mm) that the data cannot rank, and a ninth PDF the editor did not use gives a different answer for the fender braces.
2. Two picture errors must be fixed before anyone else sees it: a wrong burned-in title inside the fender-only section (5:09.6) and the rough cut's "How to read the heatmaps" card (4:03.7), whose scale and text contradict the maps that follow.
3. Voice is close; it needs fewer "So ..." openers, some of the owner's rhetorical questions, and shorter lines under IRL shots. The static PDF cards (about 5 of the last 6.6 minutes) are the weakest part; a short CGI/motion list is below.

## Blocking issues

**B1. A second tower measurement exists and disagrees (not in clips.md, script, or cards).**
`NB Miata Scan Fender Brace Jacked Engine Bay_Distance Measurement.pdf` p3 (dated 05-03-2026): "3D Dist: Control 948.382 / Fender Brace 949.073 / Dev 0.691", measured strut-top centre to strut-top centre.
The xlsx / 07-03-2026 report gives the same pair as 960.948 -> 961.185 = +0.237.
- Same two scans, different measurement points: +0.691 vs +0.237 mm. That 0.45 mm spread is as large as the whole gap between fender braces (0.237) and strut tower brace (0.731).
- By the 0.691 figure the fender braces cut the spread about 59 % (0.691/1.695, mixed definitions, indicative only), i.e. level with the strut tower brace's 57 %, not "86 %".
- Consequence: "fender braces did the most", "86 percent", "the data says do the fender braces first" (5:18.8, 6:24.9, 8:37.5, 9:28.8, cards `takeaways`, `chart`) are not safe until the owner/engineer says which measurement is right and why the two differ.

**B2. Ranking and mechanism claims the data does not support.**
- 9:28.8 "the data says do the fender braces first" contradicts 7:35.1 "I'm not going to sit here and tell you one is better" and 7:04.6 (strut tower brace has "the cleaner heat map for the whole car"). The script ranks at the end what it refused to rank a minute earlier.
- 8:37.5 "Once the front of the car is already tied together, the next brace just doesn't have as much left to do": a mechanism presented as fact. Diminishing returns would give both <= fender-only; the xlsx has both (0.436) *worse* than fender-only (0.237). The honest reading is "no measurable gain from the second brace; gap is inside what one scan can resolve".
- `takeaways` card calls 74 % vs 86 % "about the same" (0.199 mm) while the narration treats 57 % vs 86 % (0.494 mm) as a real result. Pick one standard.
- 9:04.5 "what it takes to stop it": nothing stopped it; smallest braced spread is 0.237.
- Three-decimal millimetres are quoted as if the method resolves them. No repeat scan exists to show the noise floor (see open questions).

**B3. Whole-body heat maps: brace effects are asserted from maps that mostly show panels and alignment.**
Scales checked on p2 of each exterior report: unbraced 15.000/-15.000, fender-only 14.994/-14.997, strut-only 15.000/-15.000, both 8.000/-8.000. Editor's scale statements are correct. I also matched map pixels to each report's own colour bar (approximate, +-1-2 mm, wheel-well noise included):
- 4:36.0 "That's the car twisting": interpretation. `Jacked Exterior_Heatmap` p2/p4 show one side inward (right side rear third median about -7.6), the other outward (left side rear third median about +10.6, p95 +14). That is consistent with twist, but equally with how the two scans were best-fitted; the alignment method is not in any report. Say "that's what twisting would look like".
- 5:36.2 "the front of the car is pretty much all green and light blue **now**": the unbraced front was already green/light blue (p4 hood region about 90 % within 2.5 mm). "Now" implies an improvement the maps do not show.
- 5:52.2 (`h_fender_top`, `Fender Brace Only Jacked_Heatmap` p4): the rear deck/trunk is yellow-orange on **both** sides (rear third median about +7.7), where the unbraced p4 has it light blue (about -1.4). The line "they're not really going to do anything for the trunk" skips that this view looks *worse* than unbraced there. A trunk lid is a hinged panel, same logic the script applies to the door at 7:55.
- 6:48.6 "everything is within about two and a half millimeters, front to back" (`Strut Tower Jacked Exterior_Heatmap` p2/p4): overstated. On a +-15 scale light blue runs to about -5 and green to about +3.5. My estimate: 69-90 % of the surface within 2.5 mm, 89-99 % within 5 mm; roof/hood patches reach +3 to +5. Say "a few millimeters".
- 6:48.6-7:12.3 presents the clean strut-only map as the brace's doing. A bar across the engine bay taking the rear quarter from +10-14 mm to under 3 mm, while it did *less* at the towers, is not credible without saying "one scan, we can't explain it".
- 7:55.2 door hot spot (`Fender and Strut Jacked Up Exterior_Heatmap` p2, upper view): supported as far as it goes. The door is hottest at its rear (latch) edge, +5 to +6 on the +-8 scale, green at the hinge edge, which fits "how it was closed". But the lower rear of the **front fender**/sill is also red (+7 to +8) and the script ignores it; that fender was removed for the brace install (4:46-5:09), so it is a refit, not chassis.
- 4:03.7 "green and light blue means it pretty much didn't move": on the +-15 reports that band is roughly -5 to +3.5 mm, three times the entire 1.695 mm tower result. A viewer will notice the maps cannot see the effect the table is about. Needs one line.
- "about ten", "five to ten", "two and a half", "a couple of millimeters" are colour reads, not values in the files (house rule: no invented numbers). Phrase them as "on this scale".

**B4. Wrong burned-in title in the fender-only section, 5:09.0-5:10.1.**
The fender IRL span (rough cut 298.59-322.28) ends on the first second of the fender+strut scanning shot; from about 5:09.6 the source title "Scanning Fender Brace + Strut Brace" is on screen under "and then we scan it", two sections before the strut tower brace is introduced. The same shot continues at 7:12.3. Fix: end that span at rough cut ~321.1 (cut 5:08.9). clips.md's "scanner over the brace (bumper off)" does not describe this shot; no scanner-over-brace shot is in the cut.

**B5. Legend card at 4:03.7-4:20.3 (rough-cut still) contradicts what follows.**
- Its scale is +-8.0 mm; the next six heat cards are +-15. At 7:55 the narration then says "this one only goes to eight instead of fifteen", after the viewer was taught eight.
- Its colour ramp centres green on 0; the reports put 0 at the green/light-blue boundary.
- Its text asserts things the pages do not show: "Blue zones: seen at the front of the car near the jacked corner" (unbraced p2/p4: front is green/light blue, blue is at the rear of one side); "A mostly green heatmap means the brace is working"; "classic torsional flex".
Replace it with a new card built from the real colour bar.

**B6. Line lengths assume 2.9 words/s; the clone test read 2.2 (editlog 10:06).**
- Only 3:04.3 is over 3 words/s as written (15 words / 4.9 s = 3.05).
- At 2.2 words/s these IRL shots run out of picture: 3:04.3 (needs 6.8 s, has 4.9), 3:23.8 (28.2 / 22.8), 4:46.4 (28.6 / 23.7, less after B4), 6:02.0 (29.1 / 22.9), 7:12.3 (8.2 / 7.9).
- `dur()` counts "960.948" as one word; spoken it is six or seven. Card holds for number lines (3:46.6, 5:18.8, 6:24.9, 7:20.2, 8:19.8) will be short. Time cards from the generated audio, not word count.

## Non-blocking issues

Picture vs words
- 3:04.3: "first up is our control scan" repeats what the owner says on camera at 2:21-3:03 ("scan this NB on the ground as a control", "let's get started and scan the factory car"). Shorten.
- 2:36 owner says "a total of four scans"; the table has five states. One line fixes it.
- Which corner is never said. Footage 3:26-3:40: jack under the right-side sill, front right wheel in the air (confirm with owner).
- 4:46.4: the fender is already off in the first frame; "the fender comes off" lands 18 s later. Later sections show fender and bumper back on with no mention. Say it goes back on.
- 3:23.8 "The only thing we're changing is the bracing": fenders, bumper, hood and doors were also removed/opened between scans. Fine as intent; it is why B3 matters.
- 6:02.0: bumper/fender on, title "Installing the strut tower and scanning" until about 6:10.5: consistent with the line. 7:12.3: title and bumper-off match "both". 5:10.1-5:18.8: matches.
- Burned-in rough-cut titles sit over IRL footage at 3:04-3:09, 3:24-3:26 ("Scanning the Stock Miata" a second time, now over the jack), 4:47-4:53, 6:02-6:10, 7:12-7:20. CLAUDE.md "Never: put text over IRL footage"; lessons.md (rough-cut source: only spans with no burned-in titles). Ask the team for clean exports or get the owner's OK.
- 7:55.2 holds one card 24.6 s for four ideas; 8:37.5 holds 27 s; 7:20-9:42 is 2 min 22 s of stills with no footage and no audio bed.
- The both-braces section shows only the side card; the other three states get side + top.

Cards
- `w_jacked`, `w_strut`: the state scan is drawn at about 60 % of the control's size and its dimension text is tiny; `w_fender`, `w_both` are near full size. Normalise.
- Every heat card: stray red square and "15.000" under the left colour bar and a loose vertical tick under the right view (crop slivers; review.md already notes it). Colour-bar numbers are unreadable at video size.
- Dark-blue speckle in windows and wheel wells is missing data, not deflection; three of four jacked reports have the wheels removed from the mesh, strut-only has them. Mask or say so.
- `caveats` and narration: "about a millimeter and a half" for 1.695; say 1.695 or "about 1.7".
- End card "YES. AND YOU CAN MEASURE IT." is stronger than one car / one scan allows.

Terms
- "stock" means the car (3:04, 9:28) and the unbraced jacked state (4:20 "on the stock car", 5:18 "when stock it was", 7:20 "less than stock", 8:19). Use "control" for on the ground and "no bracing" for jacked unbraced; fix card titles "Stock, Jacked (No Bracing)" too.
- "width of the engine bay" / "strut towers spread" / "that movement": pick "strut tower width" and "spread".
- "strut tower brace" is consistent in narration; the source title says "strut tower" and "Strut Brace", the chart says "Fender + strut".
- "heat map" (narration) vs "heatmaps" (legend).

Voice (transcript 46-183 s vs NAR)
- "So": 13 of 27 lines open with it, 18 sentence starts. The owner's rate per word is similar (7 in 473), but never line after line; here every data card opens "So with ...".
- "actually" 10 times (owner 3 in 473 words, about 1.5x); "just" 10 (owner 3).
- Missing: the owner's questions ("How much does it work exactly?", "But can we measure the difference?"). None in 1079 words.
- Still written: "everything else gets compared to it"; "color in the difference"; "it's kind of a different story"; "the braces don't just stack on top of each other"; "there's a few things we can take away from this"; "boxes in a corner that's open from the factory"; "Which makes sense, because ...".
- Owner's real pace is about 3.45 words/s; the clone at 2.2 will sound slow next to 0:46-3:03.

House rules to confirm
- lessons.md [audio]: "don't clone a real person's voice". Here the owner asked for their own voice and approved the test line; record that consent as feedback.
- lessons.md [text]: "Narration units in imperial" (from a spec-sheet reel). v2 dropped the inch conversion; ask.

## Line-by-line rewrites
Numbers unchanged. IRL lines sized for 2.5 words/s or less. [confirm] = needs the owner's yes.

| Cut time | Current | Proposed | Why |
|---|---|---|---|
| 3:04.3 | All right, so first up is our control scan, car on the ground, completely stock. | All right, so here's our control. Car on the ground, bone stock. | 3.05 w/s; repeats 2:21-3:03 |
| 3:09.2 | So what we're actually measuring here is the width of the engine bay ... everything else gets compared to it. | What we're measuring is the width across the engine bay, from one strut tower to the other. On the ground, that's 960.948 millimeters. That's our baseline. So it's five scans total, this one, and then four on the jack. | drops "So ... actually"; fixes four vs five |
| 3:23.8 | Next, we're going to jack up one corner ... The only thing we're changing is the bracing. | Now we jack up the front right corner to a very specific height, and we check it with a tape measure so it's the same every time. Lift one corner like this and you're twisting the whole chassis. From here on, same corner, same height. All we change is the bracing. | names the corner [confirm]; 51 words for 22.8 s |
| 3:46.6 | So with no bracing at all and one corner jacked up, the engine bay goes from 960.948 to 962.643 ... | No bracing, one corner in the air, and the strut towers go from 960.948 to 962.643. That's 1.695 millimeters wider, just from jacking up one corner. | "So" opener; one term |
| 3:58.4 | So that 1.695 is the number we're trying to beat with the bracing. | That 1.695 is the number the braces have to beat. | "So" |
| 4:03.7 | ... So green and light blue means it pretty much didn't move. Red means it moved outward, and dark blue means it moved inward. | For the rest of the car, we lay the jacked up scan over the control scan and color in what's different. Green and light blue is the small stuff, a few millimeters either way. Yellow to red means it moved outward. Dark blue means it moved inward. And this scale goes out to fifteen millimeters, so it's not going to show you a millimeter at the strut towers. That's what the measurement is for. | B3, B5: band is about -5 to +3.5 mm; sets the scale before 7:55 |
| 4:20.3 | And on the stock car, it actually moves quite a bit. On one side, the rear quarter is going orange and red, which is about ten millimeters ... | With no bracing, it moves a lot. On one side, the door and the rear quarter go dark blue. On the other side, that same area goes orange and red, so ten millimeters or more on this scale. | "stock"; follows the card left to right; rear quarter reads 10-14 |
| 4:36.0 | So one side is going out and the other side is going in. That's the car twisting, and this is what we're going to compare every brace against. | One side in, the other side out. That's what you'd expect from a car that's twisting. Just keep in mind this is the outside of the car. Doors, the top, the trunk, those can shift on their own. | interpretation as fact; sets up the door at 7:55 |
| 4:46.4 | So first we're going to throw on the fender braces ... boxes in a corner that's open from the factory. So the fender comes off, the brace gets bolted in, and then we scan it. | First we're going to throw on the fender braces from Goodwin Racing. The fender has to come off for these. They bolt in behind it, from the door hinge area down to the chassis, so they triangulate that whole corner. Then the fender goes back on, and we scan it. | "open from the factory" is not in the data; fender already off at 4:46; 50 words; [confirm fender refitted] |
| 5:10.1 | Then it's the same corner, same jack height, and we scan the engine bay again. | (keep) | fits, 1.7 w/s |
| 5:18.8 | So with just the fender braces on the car, we're at 961.185. That's only 0.237 over our control, when stock it was 1.695. So about 86 percent of that movement is just gone. | With just the fender braces, we're at 961.185. That's 0.237 over our control. With no bracing it was 1.695, so that's about 86 percent less. | "stock"; "just gone" overstates; hold until B1 is answered |
| 5:31.0 | And the crazy part is, these braces don't even touch the strut towers. | (keep) | true to the footage, sounds like the owner |
| 5:36.2 | If we look at the heat map, the front of the car is pretty much all green and light blue now ... | On the heat map, the front of the car is green and light blue. The back is still moving. One side is going yellow and orange, so somewhere around five to ten millimeters on this scale. | "now" implies a change the unbraced map does not show |
| 5:52.2 | Which makes sense, because these braces are all the way at the front of the car. They're not really going to do anything for the trunk. | And from the top, the trunk and the rear deck are yellow and orange too, and they weren't before. Is that the braces? I doubt it. They're all the way at the front of the car, and a trunk lid is a panel that can sit a little different from scan to scan. | B3: this view is worse than unbraced at the rear; adds an owner-style question; or cut the card |
| 6:02.0 | Next up is the strut tower brace by itself ... jack it up to the same height and scan it. | Next up is the strut tower brace by itself. No fender braces on the car for this one. This is the one everyone does first, because it's such an easy mod. It bolts to the top of both strut towers and ties them together. Same corner, same height, scan it. | 64 -> 50 words for 22.9 s |
| 6:24.9 | So with just the strut tower brace ... it actually did less for them than the fender braces did. | With just the strut tower brace, we're at 961.679. That's 0.731 over our control, about 57 percent less than no bracing. So it's doing something. But here's the interesting part. This brace bolts right to the strut towers, and on this test the fender braces did more. | scopes the claim to this test; hold until B1 |
| 6:43.3 | So 0.731 for the strut tower brace, and 0.237 for the fender braces. | 0.731 for the strut tower brace. 0.237 for the fender braces. | "So" |
| 6:48.6 | But then if you look at the heat map, it's kind of a different story ... within about two and a half millimeters, front to back. | But look at the heat map. With the strut tower brace on, pretty much the whole car is green and light blue, front to back. So we're talking a few millimeters, not ten. | "two and a half" not supported |
| 7:04.6 | So out of the two braces by themselves, this one actually has the cleaner heat map for the whole car. | Out of the two braces by themselves, this is the cleaner heat map. Why would a brace in the engine bay clean up the back of the car? Honestly, I don't know. It's one scan. | B3: do not credit the brace |
| 7:12.3 | And then for the last scan, we've got both of them on the car together, same jack height. | And then the last scan. Both of them on the car together, same corner, same height. | 15 words for 7.9 s |
| 7:20.2 | So with both braces on ... or about 74 percent less than stock. So that's better ... but it's actually not better than just the fender braces. | With both braces on, we're at 961.384. That's 0.436 over our control, about 74 percent less than no bracing. Better than the strut tower brace by itself. Not better than just the fender braces. | "stock"; tics |
| 7:35.1 | Now, the difference ... But what it does tell us is that the braces don't just stack on top of each other. | Now, those two are only about two tenths of a millimeter apart, and we only did one scan of each. So I'm not going to tell you one beats the other. What I can tell you is, adding the second brace didn't make it any better. | "don't just stack" is a mechanism; this is the observation |
| 7:55.2 | One thing to point out ... The door is showing up hot, but that's a door, it's on hinges, so that's most likely just how it was closed and not the chassis moving. | One thing on this heat map, the scale is different. This one only goes to eight millimeters, not fifteen, so the same colors mean smaller numbers. Most of the car is within a couple of millimeters. The hot spot is the door and the bottom of the fender. The door's on hinges, and that fender came off for the brace. So that's most likely how they went back on, not the chassis moving. | adds the fender hot spot; split over two cards (side, then top) |
| 8:19.8 | So does chassis bracing actually do anything? Yes, it does, and we can actually measure it. Stock, with one corner jacked up ... | So does chassis bracing actually do anything? On this car, on the jack, yes. With no bracing, the strut towers spread 1.695 millimeters. Fender braces, 0.237. Strut tower brace, 0.731. Both, 0.436. | keeps the title's "actually", drops the second; scoped |
| 8:37.5 | So there's a few things ... Once the front of the car is already tied together, the next brace just doesn't have as much left to do. | So what do we take away from this? Number one, every setup cut that movement by more than half. Number two, on this test the fender braces did the most for the strut towers, more than the strut tower brace everyone does first. And number three, they didn't add up. Both together was no better than the fender braces alone. | removes the unsupported mechanism; question opener |
| 9:04.5 | Now, keep in mind ... about a millimeter and a half ... and what it takes to stop it. | Now keep in mind, this is one car, one scan of each setup, and it's a jack, not a corner at the track. The differences between the braces are fractions of a millimeter, so I wouldn't rank them off this. The most the strut towers moved was 1.695 millimeters. But that's where your front suspension bolts to the car, and now we know how much it moves. | exact number; "stop it" is false |
| 9:28.8 | So if you've got a stock NB and you're only going to do one of these, the data says do the fender braces first ... | So if you've got a stock NB, which one would I do first? On this test, the fender braces did the most up front. But it's one test. Let us know in the comments what you want us to measure next. | B2: recommendation was stronger than the data |

Card text to change with it: `takeaways` #3 subline -> "Both together: 0.436 mm, no better than fender braces alone (0.237 mm)"; `caveats` add "Differences between braces are fractions of a millimetre"; `end` -> "ON THIS CAR, ON A JACK: YES."; all titles "Stock, Jacked (No Bracing)" -> "No Bracing, Jacked".

## CGI and graphics plan
All scans: decimate first (exterior 25M -> about 2M, bay 5M -> about 1M) and put all five in ONE frame (prep the control, the rest with `--like`), or deviations are meaningless. Cycles CPU: plan stills plus short moves; one render at a time in the background. On-screen numbers only from the xlsx/PDFs.

| # | Where | What it shows | Scan files | Compute | Risk | Priority |
|---|---|---|---|---|---|---|
| 1 | 4:03.7 | New "how to read" card: the real +-15 colour bar, three plain labels, a note that the last report is +-8 | none (Remotion) | none | none; removes B5 | must |
| 2 | 3:58, 5:31, 6:43, 7:35, 8:19 | Animated table and bar chart: rows add one at a time, bars grow, the 1.695 bar stays as reference | none (Remotion) | none | ScanHUD `counter` stops at 99.9 % of the value (lessons): use fixed labels for 960.948 etc. | must |
| 3 | 3:09, 3:46, 5:18, 6:24, 7:20 | Engine-bay scan in house silver, top-down, with a dimension line drawing tower to tower; the state scan cross-fades in on the same camera, label changes 960.948 -> 962.643 | 5 engine-bay STLs | align the four jacked bays to the control; place the line where report p2 puts it | our own measurement will not reproduce 960.948 exactly: draw the line, print the report's number, never ours; endpoints need the engineer (and B1) | must |
| 4 | 4:20-4:46, 5:36-6:02, 6:48-7:12, 7:55 | Deviation heat map on the real scan, ONE scale (+-15) for all four states, same three cameras (both sides, top), slow 10-15 degree push, 4-6 s each | 5 exterior STLs | align each jacked scan to the control; signed closest-point distance per vertex; bake to vertex colour; emission shader | alignment: our best-fit may not reproduce the reports' colours. Gate: reproduce the unbraced p2/p4 pattern within about 2 mm first; if not, stay with cleaned PDF crops. Doors, soft top, trunk lid, hood, wheels moved between scans: grey them out and say so | must if the gate passes |
| 5 | 8:19 or after 7:55 | 2x2 split screen: the four states, same camera, same scale | renders from #4 | none extra | inherits #4; makes the strut-only anomaly obvious, so the narration must own it | should |
| 6 | 4:36 | Exaggerated deflection: control scan displaced along its normals by the unbraced deviation x20, top view, label "movement exaggerated 20x" | control + unbraced exterior | field from #4; no vertex correspondence needed | reads as real if the label is small; hinged panels must be frozen | should |
| 7 | 3:04.3 | House 1:1 hard cut from the static front shot (about 3:08) to the control scan | control exterior | camera solve (knowledge/match-cut.md) | that span carries a burned-in title; needs a clean export; no beat to cut on | should |
| 8 | 0:14-0:23 | Intro scenes 1-2 on the real NB scan: load arrows at the wheels, tower-to-tower line on the engine-bay scan | control exterior + bay | none; schematic arrows, no numbers | keep "illustration, movement exaggerated"; scene 3 (fixed roof vs open top) stays 2D, no fixed-roof scan exists | nice |
| 9 | 4:46-5:09 | Where the fender brace sits, highlighted on the scan | a fender-off scan, if one exists | none | no such scan is listed; do not fake a fender coming off (lessons: removals only from scanned states) | nice, only with data |
| 10 | n/a | Strut-tower close-up maps (bay reports p3) | - | - | no clear braced/unbraced difference; agree with the editor: leave out | skip |

Budget guide: #1-#2 no Blender time; #3 five stills plus cross-fades; #4 twelve shots (4 states x 3 views), emission-only shading at low samples; do #4's gate test on one state before committing.

## Open questions for the owner
1. Which tower measurement is the real one: 960.948 -> 961.185 (+0.237, xlsx) or 948.382 -> 949.073 (+0.691, Distance Measurement PDF p3)? What points does each use, and do the other three states have the second measurement?
2. Is there any repeat scan of the same state (or the two control scans: engine-bay control and ground control) to show how much two scans of an unchanged car differ? Without it, 0.2-0.5 mm gaps cannot be ranked. Do you want the Artec Leo's accuracy stated, and from which document?
3. How were the exterior scans aligned to the control (whole-body best fit, or a chosen region)? This decides whether "one side out, one side in" is twist.
4. Which corner was jacked (footage looks like front right, jack under the right sill), and was the height re-measured for every run?
5. Were the fenders and bumper back on for the fender-only and both-braces exterior scans? Was the trunk opened between scans? Were doors opened?
6. Are you comfortable saying on camera that you can't explain why the strut-only body map is the cleanest?
7. End recommendation: keep "fender braces first" in the softened form, or end on "bracing works, we can't rank them yet"?
8. Can the team export the IRL shots without the burned-in section titles?
9. Inches as well as millimetres in the narration?
10. Confirm on record that the clone is your own voice and you approve its use for the full narration.

## Sign-off pass on v3

Checked: script.md v3, `build.py` rates, the two new clips.md sections, `work/exterior_stats.json`, `bay/towerspread.json`, and v3 contact sheets at 5:37-5:43, 8:17-8:28 and one frame of each new or changed card. I did not re-run `heat.py` or `towerspread.py`; the body percentages and strut-top figures are taken from the editor's output files.

**Verdict: not approved yet. Five wording changes (below), then approved for owner review with no further pass from me.**

### (a) B1-B6
| # | Status | Note |
|---|---|---|
| B1 second tower measurement | partly | The conflict is recorded and goes to the owner, and the recommendation is gone. But "by this measurement" is spoken only once (5:50.2); the conclusions still state the xlsx result unqualified. |
| B2 ranking / mechanism | resolved | No recommendation, no "left to do", no "stop it"; `takeaways` #3 now quotes both numbers. |
| B3 heat-map claims | resolved | "Twisting" hedged, "now" removed, trunk line owns the rear deck, strut-only map left unexplained ("It's one scan"), fender hot spot added, colour reads replaced by computed shares. |
| B4 wrong title at fender tail | resolved | 5:37-5:42 is clean; "Scanning Fender Brace + Strut Brace" first appears at about 8:21, inside the both section. |
| B5 legend card | resolved | New card uses the real ±15 bar with zero at the green/light-blue boundary and no interpretive text. |
| B6 line lengths | partly | All IRL lines are now 2.44 words/s or less. At the clone's 2.2 words/s, 3:04.3 still needs 5.5 s against 4.9 s and 5:19.8 needs 22.7 s against 21.7 s. Card holds still come from word count; time them from the audio. |

### (b) New problems in v3
1. **The strut-top cross-check undercuts three unqualified conclusion lines.** `towerspread.json`: no bracing +0.36 to +0.45 mm, fender braces only +0.73 to +0.97 mm (and the PDF's +0.691). By that measure the fender braces did not reduce the spread at all, and the unbraced spread is about 0.4 mm, not 1.695.
   - 10:00.4 "every setup cut that spread by more than half" is true only for the xlsx engine-bay width. Not defensible as a bare takeaway; same for card `takeaways` #1 and the #2 subline "Towers: fender braces spread least".
   - 10:57.4 "the car moved less with either one": not defensible for the fender braces. Strut-top spread is larger than unbraced, and the body share within 2.5 mm is 60 % against 58 %, which the script itself calls "basically the same" at 6:28.0.
   - 7:17.1 "on this test the fender braces did more" needs the same qualifier as 5:50.2.
2. **The four spoken body percentages (58 / 60 / 91 / 74) are defensible**, with two conditions. They agree in order and rough size with my colour-bar read of the PDFs. But they are our own calculation from the STLs, not values in the xlsx or PDFs, so the script.md header ("Every number is from `Strut Spread.xlsx` and the nine PDF reports") is now false, and the video should say once that these are computed from the scans. "Body" includes doors, soft top and glass; the 4:57.1 line already says so, which is enough.
3. `exterior_stats.json` labels the thirds the opposite way to the clips.md table (json: jacked front 3.65, rear 0.44; clips.md: front 0.44, rear 3.65). Nothing spoken depends on it, but fix one before anyone quotes it.
4. 5:37-5:40: "Then the fender goes back on" plays over the fender visibly off with the brace being bolted. Still needs the owner's confirmation that it was refitted before the scan (open question 5).
5. No other new picture/word mismatch found. `w_jacked` is now drawn at matching size; the both section has side + top cards.

### (c) Lines to change before owner review
| Where | Change to |
|---|---|
| 7:17.1 | "... This brace bolts right to the strut towers, and by this measurement the fender braces did more." |
| 9:39.6 | "So does chassis bracing actually do anything? On this car, on the jack, by this measurement, yes. With no bracing, the engine bay spread 1.695 millimeters. Fender braces, 0.237. Strut tower brace, 0.731. Both, 0.436." |
| 10:00.4 | "So what do we take away from this? Number one, by the engine bay width, every setup cut that spread by more than half. Number two, the two ways of looking at it don't agree. By the engine bay width, the fender braces did the most. On the heat map of the whole car, the strut tower brace was the cleanest. And number three, they didn't add up. Both together was no better than the fender braces alone." Card `takeaways`: #1 "By engine bay width, every setup cut the spread by more than half"; #2 subline "Engine bay width: fender braces spread least. Whole-body map: strut tower brace is cleanest". |
| 10:57.4 | "So which one would I do first? Honestly, off this one test, I can't tell you. What I can tell you is the engine bay spread less with every setup we tried. Let us know in the comments what you want us to measure next." |
| script.md header | "Tower widths are from `Strut Spread.xlsx` and the PDF reports; the four body percentages are our own calculation from the exterior scans (tools/heat.py)." Add the same disclosure once on screen or in the 4:57.1 line ("... by our own math on the scans, a little under sixty percent ..."). |

Owner question 1 should now say plainly: if the strut-top measurement is the right one, the fender-brace section and all of section 5 need rewriting, because by that measure the fender braces did not reduce the spread.
