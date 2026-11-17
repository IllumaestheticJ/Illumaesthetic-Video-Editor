# Reviewer rules for scan reels, by topic

Compiled 2026-11-17 from all 754 feedback notes on every branch (`projects/*/feedback.jsonl`), plus
`knowledge/lessons.md` and the parent-session relays. Each rule gives the user's words and the project it came from.
When two notes conflict, the later note wins, and the conflict is written out. `knowledge/lessons.md` still overrides this file.

## 1. Only real scan data (the most repeated complaint)

- **Show nothing that was not scanned.**
  - "improperly cut and hallucinated scans" (subaru-sti-blobeye v2).
  - "Rear trunk data is made-up" (honda-s2000).
  - "we never pulled the EK bumper" (honda-civic-11-scan-process).
  - A part comes off only if a separate scan of it, or a scan of the car with it removed, exists and registers.
  - An opening (hood, trunk, door) is shown only if a scan of that open state exists.
- **Every removal starts with the state scans.** With no part scan, show each state scan alone, as captured, as a 1:1
  swap on a kick. Never use a carved or composited stand-in (sti-blobeye v3).
- **Leave out state scans with ragged openings.**
  - "trunk open scan should be removed cause it looks bad; doorsill scan should be removed" (c5-corvette v3).
  - Render every state alone before planning.
  - Drop any scan whose opening edge is ragged at every framing.
- **Add only what was asked.**
  - "wtf did you do to the door - the door-off state scan should not have been added" (toyota-gr-corolla v6).
  - When a request names scans ambiguously, list the candidate files and ask.
- **Use every scan that exists.** The user repeatedly found scans we had missed:
  - trunk open, mirrors, lamps (GR86);
  - gas cap, doorsill (C5);
  - frunk trim, under-hood plastics (Ferrari 296);
  - underbody, floor, wheel houses (GT3 RS, A90, MR2 Spyder);
  - suspension geometry (A90, QX80);
  - fog lights and reflectors (WRX VB);
  - bumper sub-parts (WRX VB, Revuelto);
  - the GT3 "bumper removed" rear scan, which was in the engineering drive and not the project folder.

  List the WHOLE Drive folder and its sub-folders into `clips.md`. Then search the engineering drive by name variants
  ("bumper removed", "cannard"/"canard") and look in the 3D artist's `Projects_` folder.
- **Use the right version of the car.**
  - "Complete Car 1/2 is the facelift bumper - don't use it" (GR Corolla).
  - "wrong front lip (V1); it should be the V2" (gr-corolla-reel).
  - Read the folder names, and render each candidate full-car scan's front side by side.
- **Never invent numbers or show triangle counts.**
  - "No one cares about triangle count" (huracan-evo, c5-corvette-scan-process).
  - Label text comes from file names and state names only.

## 2. Cutting panels out of the full-car scan

- **Cut on the real shut lines.**
  - "the lines where the front bumper and trunk were cut ... are not correct" (cappuccino).
  - "the hood cutout line is incorrect", "the rear trunk is not cut right" (miata-nd).
  - "rear trunk isn't cut out correctly", "the hood is cut wrong" (GR Corolla).
  - "fender cut isn't cut correctly" (A90).

  Methods are in `scan-cutting.md`. Never use a distance threshold or a box.
- **A removed part takes ONLY its own skin.**
  - "the front end scan is missing a huge chunk of the car" (GR Corolla v5).
  - "the fender removed scan took too much of the chassis off with it" (A90 v4).
  - "Side mirror coming off took a part of the window with it" (400Z).
  - "Hood-opened scan cuts too much of the windshield out" (GR86).
  - "the rear trunk scan takes a chunk of the tail light with it" (miata-nd).
- **...and ALL of its skin: no leftovers.**
  - "parts of the old bumper are still visible on the car" (GR86, Miata NA, Frontier).
  - "bits of the rear trunk left behind" (GR86 v7).
  - "still has leftover bumper" (WRX VB).
  - "no parts may be left behind on the car" (A90).
- **A removed part comes off WHOLE.** "the front bumper was missing a chunk from it" (GR Corolla v6). Fill the part scan
  with the car faces the cut removed. Never trim a part's ragged edge for tidiness.
- **What sits under a removed part must still be there.** "the scan data underneath the engine bay must still be there as the
  parts come off" (GR Corolla). "the scan of what is underneath the bumper should be there instead of blank space"
  (a90-supra-scan-process).
- **Clean every artifact.**
  - "Delete/hide the artifacts from the full car scan" (C5).
  - "the rear wing artifacts on one of the trunk scans" (miata-nd).
  - "artifacts of the hood that aren't cleanly cut out" (sera).
  - "front bumper has a ton of artifacts" (WRX VB).
  - "random floating ... piece in the air" (QX80).
- **Wheels must be round and solid.** "the wheels are oddly cut flat" (Revuelto). "Wheels cannot clip into the body" (Frontier).
- **Don't crop a state scan's surroundings.** "the exhaust scans need the surround scan to be more present, too much of it is
  cut off" (Revuelto).
- **When the full-car scan is weak in an area, take that area from another full-car scan of the same car version**
  (GR Corolla v7, "use the other full car scan").

## 3. Order and nesting (how the car really comes apart)

- **Children wait for their parent.**
  - "Nothing should come off the bumper until the bumper itself comes off" (400Z).
  - "parts on the bumper must not come off until the bumper itself is off" (GR Corolla).
  - "Corner markers should not come out until the bumper comes off" (cappuccino).
  - "remove the front bumper first, then pull the grille" (WRX VB).

  Child parts travel with their parent, then leave it the way they are really removed.
  "The corner markers come out of the car from the front" (cappuccino).
- **Hinged panels open on their hinges FIRST.**
  - "the hood needs to hinge open THEN come off" (GR86), and the trunk "the same way (hinge open, then off)".
  - "Hood needs to open normally (hinge) to show its underside" (Frontier).
  - "we don't show the hood opening - add it" (GR Corolla).
  - On the front: hood first, then the bumper ("Open the hood first, THEN pull the bumper out", cappuccino).
- **Doors and lids never detach unless they were really removed.** "the doors lifting off and the trunk lid lifting off are
  hallucinated - ... the parts must only open on their hinges, never detach" (Civic 11). The two hood rules don't
  conflict:
  - On the GR86 and GR Corolla the user asked for hood and trunk to hinge open, then come off.
  - On the Civic, doors and the trunk only open.
  - So hinge open first, and take a panel off only when the user asked or a removed-state scan shows it off.
- **Two scans of the same part are one part.**
  - "there are two side skirts" (GT3 RS: upper and lower files were the same skirt).
  - "BRZ and GR86 rear bumpers are the same - don't need to do the splitting thing" (GR86 v8).
  - Compare part scans against each other before casting them.
- **Different parts stacked together come off together, then split, without clipping each other** (GR86 v7/v8, BRZ + GR86
  front bumpers).
- **Exhaust after the rear bumper** (Revuelto). **Stock part off before a replacement goes on** (QX80 skirts).
- **Travel around the car once** (front -> side -> rear), with no ping-pong (all-reels V2 brief).

## 4. Motion and framing

- **Parts never pass through each other or the body.**
  - "the parts clip into the car" (GT3 RS).
  - "When the rear bumper moves off the car it clips with the tail lights and rear wing" (Revuelto).

  Route each part out past the silhouette, then up and over. Check it numerically with `pathcheck.py` / `clipcheck.py`.
- **Every part stays on screen while it moves.** "Some parts, when coming off the car, are going off the screen" (Revuelto).
  Parked parts are fully in the frame or fully out of it.
- **Move parts into clear background.** "A part being removed is hard to see when the rest of the scan is behind it" (GT3 RS
  scan process). Often move them toward the camera, so their mounting side shows (C5).
- **Get removed parts completely out of the way of what comes next.**
  - "move the brake/parts completely out of the way" (A90).
  - "the console is blocking what's underneath" (A90).
  - Parts that fly off end more than 4 m away.
- **Spin only to show a scanned backside.** "Don't spin or flip parts unless the move is there to show the viewer the
  backside" (C5, GT3 RS, Lola). Rotate bumpers about the vertical axis, not end over end (240SX).
- **No turntables or orbits that show nothing new.** "Rotations are again wasted" (Miata NC/NA). The exception is a requested
  360, which shows something new (GR Corolla: 360 of the finished car with the kit installing; 360 of a hero aftermarket part).
- **Hold on what a removal exposed.**
  - "the side skirt comes off and then immediately cuts away, its just a bad practice" (miata-nd).
  - "it says 'door flare' but you can't see anything come off" (WRX VB).
- **Frame on the section.**
  - "focus on the removed areas and where the useful data is" (C5).
  - "front bumper framed on the front while it comes off, THEN move on to the rear" (Miata NC).
  - "exploded view is too wide" (Ferrari 296).
- **The opening shot shows the WHOLE car, moving from frame 1.** "Video starts off too cropped" / "Car is clipped at the
  beginning" (Ferrari 296, IS300, Miata NA, Mazda 3).
- **No jump cuts.** Two nearly identical angles cut together read as "a weird cut" (miata-nd). Either change the angle a lot,
  or start the next shot exactly on the last camera key of the previous one.
- **No filler cutaways.** "The slow cut on the wheel at 0:20 is completely unnecessary" (cappuccino). "the wheel close-up
  is unnecessary" (miata-nd). "the zoom into the trunk is unnecessary" (Miata NA). "the two shots at 17 seconds are
  pointless" (rx7-fc).
- **Long thin parts:** roll the camera so the long axis runs up the 9:16 frame (A90 tail lamps).

## 5. Labels

- **Every scanned part gets a beat and a name.**
  - "make sure all parts are highlighted" (GR86, Macan).
  - "Highlight and label each unique scan section" (Frontier).
  - "as the flares and side skirts come off, list them" (WRX VB).
  - "GT3RS include the labels".
  - "label each teardown step" (huracan-evo).
- **Labels are short and factual.** Say what the scan is used for where that helps (Miata NC). Use no step or mod numbers
  ("Do not count the mod numbers", Frontier), no redundant qualifiers ("'scanned separately' is redundant", WRX VB), and
  no triangle counts.
- **Name the brand when the user names it.** "include the brand name on the new intercooler" (GR Corolla).
- **Never put text over IRL footage.** Put labels in clear black. Full-frame scan shots get a dark plate behind the label.

## 6. Pacing and length

- "the video needs to move faster" (GR86); "make the whole thing faster", "intro way too slow" (Miata NA);
  "too long, focuses too long on the wrong things" (sti-blobeye); "paced too slowly" (Civic 11); "starts off too slow"
  (GT3 vs GT3 RS); "last scenes held too long" (S2000).
- "if the video needs to be shorter, make it shorter" (Miata NA). Revised reels settled at **about 20-25 s** (GD trio 20.4 s,
  Miata NA v5 20.6 s, Civic 11 v5 24.9 s). The approved Revuelto v5 is 44.6 s because every section in it was requested.
  The rule is that length follows content: never stretch holds to fill bars.
- Keep the pace even. "The front feels rushed and the whole thing is not the same pacing" (huracan-evo).
- A 1:1 reveal must not settle and wait for the drop. "the pause is a little too long" (Frontier); "doesn't hold for so long
  waiting for the drop" (QX80).

## 7. Music and audio

- **Real music, never generated or library slop.**
  - "This is slop music" (MR2 SW20).
  - "No generated tracks - use real music" (QX80).
  - "THE DEATH ... is awful - change it to a real, trending song" (Civic scan process).

  Use the user's track when supplied. Otherwise pick from Dropbox `/Moosic`. Gran Turismo 2 and NFSU2 tracks have been
  approved.
- **Don't reuse a track another reel already used.** Check `projects/*/project.yaml` and the editlogs first.
- **Start the song from its beginning** ("its the trending side", miata-nd; Revuelto; Miata NA), unless the user gives an
  offset (GT3 RS "after the ~2:50 mark"; Frontier "around 1:50"). Make sure the start doesn't miss the drop ("misses the
  drop", miata-nd).
- **Loudness: about -14 LUFS, true peak below -1 dBFS.** "is the music way too loud and blown out?" (Revuelto);
  "Music too loud" (400Z). Measure after the final mux.
- **Every cut on a measured kick or hit, checked on the decoded audio of the delivered file.** Methods are in `music-and-timing.md`.
- **No YouTube downloads.** The container is blocked, and getting around YouTube's bot check is not allowed. Ask for the file.

## 8. Ending, logo and CTA

- **Logo:** "logo too small" came up on 9 reels at 270-460 px. Use **640-760 px of 1080** (720 is standard).
  - Keep it short: "the Illumaesthetic logo takes too long" (Civic 11).
  - Epsilon reels end on the Epsilon logo (MR2 Spyder, Civic 11).
  - The Lola reel has no website URL.
- **End sequence:** reassembly, then a fade, then the logo. Don't hold the last scenes.
- **Store CTA (requested on the 240SX, Miata NA, Miata ND, Sera, Ferrari 296, GT3 vs GT3 RS and WRX VB reels):**
  - The final scan shot lands **1:1 on the product listing's cover photo** ("needs to match the frame of the website cover
    photo", Miata NA).
  - Then it zooms out to a screenshot of the **mobile** product page, with "scan data now available".
  - "The CTA is wrong. It should be like the 240SX style videos" (GT3 vs GT3 RS). Text CTAs alone are wrong.
  - Put the CTA high on the frame ("available now is too low", Ferrari 296).
  - Change the dropdown in the VIDEO, never on the real product (Ferrari 296).
- A contact line under the logo is fine when asked ("contact us for your engineering/scanning needs", GR Corolla).

## 9. Look

- House look: silver on black. Car colours only when asked: "start with the car being red (cause ferrari)", "less saturated,
  more pastel" (Ferrari 296); "make the car pink" (Miata NA).
- Kit parts keep their real materials: "Diffuser should be black" (MR2 Spyder).
- **Number plates:** blur or flatten them only on the IS300 ("Only is300"), and on any reel where the user asks in that
  reel's chat (Macan: "Hide/blur/remove the rear plate on this reel").
- **"60 FPS" means true 60 fps renders**, not interpolation. Say which one you delivered (GT3 vs GT3 RS, Ferrari 296, QX80).

## 10. Builds, kits and aftermarket parts

- Place kit parts accurately from the design files, in the car's frame. Check them at their mounting edge.
  - "all the kit parts are placed on incorrectly" (Civic 11 v4).
  - "the full lip kit and wing are improperly placed" (GR Corolla).
  - Engineering's frame is not ours: use ICP on their reference car scan first.
- Nest kit parts into the scan by the stock-panel footprint. Never leave black seams, and never let old parts clip
  through the new ones ("Front grille installation still clips with the old parts", Frontier).
- A hero aftermarket part gets a quick 360, then its install (GR Corolla intercooler). Kit parts go on during the
  reassembly, after the parts they replace come off (GR Corolla WRC wing).
- Plan first with a director agent. "the cutting/organisation is a mess - have a separate agent plan out the shots, then
  reshoot everything" (Civic 11 v4).
