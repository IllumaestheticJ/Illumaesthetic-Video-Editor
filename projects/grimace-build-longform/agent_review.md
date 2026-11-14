# Independent review of `script.md` v1 (Grimace parts build)

Reviewed 2026-11-14 against `plan.md` section 3, `coverage.md`, `clips.md`, `log/*.md`, `transcripts/all_clips.txt`,
the approved bracing script and the owner's 22 notes. Line numbers are the `#` column of the script table.

How the SYNC quotes were checked: against the small.en transcript, and the key spans of `DSCF6662`, `DSCF6573`,
`049A5439`, `049A5441` and two June clips were re-run through faster-whisper `medium.en` with word timestamps. That is
still a machine transcript. Nobody has listened to the wavs, so every "verify by ear" below is still open.

Verdict: the structure, the sponsor coverage and most of the register are good. Nine things should be fixed before the
owner reads it. Four are sponsor credits or SYNC quotes, four are explainer lines a Miata/track audience or a sponsor
would push back on, one is the length stated at the bottom of the script.

---

## A. Blocking (fix before the owner sees it)

### A1. Line 26: the grease and seals will be heard as a Whiteline credit, and the spoken "Good-Win" is cut
- The quote starts mid-sentence at "this really cool trick of silicone grease" and continues "They also gave us...".
  In the source "they" is Good-Win (named at 24 s). In the script the last brand the viewer heard is Whiteline (line 19),
  so "they" becomes Whiteline. The "(Good-Win Racing)" in the script is a note, not something the viewer hears.
- The quote ends "so thank you for that". `medium.en` hears "So thank you **Google** for that" at 48.1 s, which is almost
  certainly "thank you, Good-Win, for that". This is the same miss the owner corrected last time ("thank you good one"
  should be "thank you Goodwin").
- "seals..." hides "for the control arms" (small.en "for the controller"). No reason to cut it.
- Fix: add one VO line in front, and keep the SYNC to the end of the sentence.
  - New VO: **"And Good-Win sent us something for this job too."**
  - SYNC 6662, about 35-49.5 s: **"...this really cool trick of silicone grease for the bushings. They also gave us a bunch of OEM replacement seals for the control arms, so thank you, Good-Win, for that."** (verify the last five words by ear)

### A2. Lines 29, 34, 60: the brake kit credit drops "courtesy of Brian", and Brian is Good-Win's in the same clip
- Source, 112-141 s: "...a big brake kit from Fast Brakes, Wilwood, I believe this is a Superlite, courtesy of, oh shoot,
  courtesy of Brian, thank you Brian, and with that kit we also have stainless steel front brake lines, as well as the
  [unclear] underneath."
- At 15-20 s of the same clip the host says "we helped Brian [surname unclear] from Good-Win with his Hyper Miata kit".
  So the only spoken supplier credit for the brake kit most likely points at Good-Win. The script cuts it (line 29 stops
  at "Wilwood...") and line 60 then thanks Fast Brakes and Wilwood as if they sent parts, with no brake credit to Good-Win.
- ASK 3 mentions Brian but not this evidence. Rewrite ASK 3: **"On camera you say the big brake kit is 'courtesy of Brian', and earlier in the same clip Brian is from Good-Win. Did Good-Win supply the Fast Brakes / Wilwood kit and the lines? If so we credit Good-Win for it and name Fast Brakes and Wilwood as the makers."**
- Until answered, mark lines 29, 34 and the brake part of 60 as provisional. If Good-Win supplied it, add after line 29:
  **"And that kit came to us from Brian at Good-Win."**
- Line 34 also cuts "as well as the [unclear] underneath" (141-145 s; both models hear "the motorsport underneath").
  That is a second item on the table that nobody has identified. Listen to it. If it is a part (rotors, pads, a line
  kit), it needs a credit or a decision to leave it out. Add it to the ASK list.
- Line 34 quote itself: `medium.en` hears "brake line", small.en has no "lines" at all. Verify the word before captioning.

### A3. Lines 5 and 51: "Does this actually fit?" "No." is not where the plan says it is, and may not be an exchange
- small.en: question at 9.8 s, "No." at 14.8 s. `medium.en`: "Does this actually fit? No?" with the "No" running up to
  about 16 s, punctuated as the same speaker's question. The plan's span `5439 9.8-12` cannot contain the "No".
- Picture: the log puts hands seating the hub adapter on the back of the wheel at 0-25 s. The wheel is offered up to
  the column at 50-70 s. So at 9.8 s the thing that does not fit is the hub adapter on the wheel, not the wheel on the car.
  The plan calls this shot "wheel offered up".
- Fix: listen. If "No" is a reply about five seconds later, say so in the script ("pause trimmed") and extend the span
  to about 9.8-15.5. If it is the same person saying "No?", the gag as written is not real and needs a different line.
  Either way correct the picture description so the cold open does not promise "the wheel does not fit the car".

### A4. Line 21: "after thirty years" is a number that is in no file, and the line makes claims about Grimace's bushings
- The script header says "No numbers anywhere". The car's model year is not in any log. The logs describe the old
  bushings as "old OEM rubber" and the sleeves as "rusted" ("This is too rusted, dude"). Nothing says soft or cracked.
- It is also 39 words. Replace with two general lines:
  - **"From the factory, it's rubber. And on a car this old, that rubber gets soft and it cracks."**
  - **"So when you load the car up in a corner, it squishes. And the wheel moves around in ways you didn't ask it to."**

### A5. Lines 14 and 16: the coilover explainer is wrong about single adjustables and undersells the sponsor's damper
- Line 14, "On a cheap coilover you get one knob, and it changes both at the same time": (a) single-adjustable is not
  "cheap"; MCS sell a single-adjustable themselves, and so does every serious damper maker. The host's "cheap eBay
  coilovers" is his opinion of one specific set; the VO turns it into a category. (b) On most single adjustables the knob
  is mainly rebound, not both equally. (c) Nothing in the footage shows whether the eBay set has a knob at all.
- Line 16, "The spring is what decides how much the car leans and dives... The damper just controls how it gets there":
  roll is springs plus sway bars (the script says so itself at line 44), and "just" talks down the MCS part.
- Replacement for 14 (also splits a 35-word line):
  - **"When the wheel hits a bump and gets pushed up, that's compression. When it comes back down, that's rebound."**
  - **"On a lot of coilovers you get one knob. And on most of them that's mostly rebound, so compression is whatever you get."**
- Replacement for 15: **"On these, there's a knob for each. So if it's crashing over curbs, or floating after a bump, you can fix that one thing and leave the other alone."**
- Replacement for 16: **"And the springs are from Eibach. The springs, along with the sway bars, decide how much the car leans and dives. The dampers control how fast it gets there."**

### A6. Line 31: "The stock brakes will stop it. Once."
- This is the line most likely to fill the comments. Stock Miata brakes with good pads and fluid are widely tracked and
  raced. It is also a punchline in a copywriter's rhythm, and it is a claim about Grimace's old setup that no footage
  supports.
- Replace: **"So why a big brake kit on a Miata? It's a light car. And honestly, with good pads and fluid, the stock brakes do okay."**

### A7. Line 32: "A bigger caliper and a bigger disc can take more heat"
- Only the caliper is ever seen (6576, 6577; "Wilwood Disc Brakes" box). No disc from the kit is in any log, and many
  Wilwood kits for this car keep a stock-size disc. "Bigger disc" is therefore a claim about a sponsor's kit that the
  files do not support. A caliper also does not "take heat"; the disc and pad do.
- Replace with two lines (the original is 32 words):
  - **"The problem is doing it again and again, lap after lap. Brakes turn speed into heat, and that heat has to go somewhere."**
  - **"A big brake kit gives you a stiffer caliper and a bigger pad. So it takes a lot longer before things start to fade."**
  - Add "and a bigger disc" only if the owner confirms the kit's disc is larger than stock (add to ASK 4).

### A8. Lines 46-47: "An adjustable tie rod lets you get that angle back"
- Every tie rod is adjustable (that is how toe is set). What fixes bump steer is moving the outer pivot up or down.
  Whether the SPL set does that is not in the footage: the label is unreadable and the product name is unknown. The host
  only says it will "help tie in the steering".
- Line 46 also explains bump steer as the rod's angle alone. It is the tie rod's arc not matching the control arms'
  arc. And "connects the steering rack to the wheel" can be heard as the steering wheel. It is 41 words.
- Replace 46 with:
  - **"The tie rod connects the steering rack to the front wheel. It swings in an arc when the suspension moves, and so do the control arms."**
  - **"If those arcs don't match, the wheel steers itself a little over every bump. That's bump steer. And lowering a car usually makes it worse."**
- Replace 47 with, only if the owner confirms the SPL ends are bump-steer adjustable (new ASK):
  **"With a tie rod end like this, you can move that outer pivot up or down, and get it back where it should be."**
  If not confirmed, cut 47 and let the host's own line (45) carry what the part does.

### A9. The length at the bottom of the script is wrong, and the VO does not fit the plan's slots
- Script says "35 VO lines, about 620 words, roughly 4 minutes". Counted: **40 VO lines, about 850 words, about 5.4
  minutes** at 2.6 words/s (the plan budgeted about 430 words).
- Ten VO lines are over 30 words: 14 (35), 15 (31), 21 (39), 32 (32), 37 (35), 41 (36), 44 (39), 46 (41), 48 (37),
  60 (42). Splits are given in A4, A5, A7, A8 and section B.
- Slots that overrun (VO at 2.6 words/s plus the real length of the SYNC, against `plan.md` section 3):

| Plan slot | Given | Script needs | Over |
|---|---|---|---|
| 0:25-0:30 cold open, line 6 | 5 s | 7.7 s | 3 s |
| 2:00-2:38 G6 + G7, lines 13-16 | 38 s | 45 s | 7 s |
| 3:24-3:50 G8, lines 20-22 | 26 s | 35 s | 9 s |
| 4:30-4:42 grease, SYNC 26 + line 27 | 12 s | 21 s (22 s with the A1 lead-in) | 9-10 s |
| 5:20-5:48 G9, lines 31-33 | 28 s | 30 s | 2 s |
| 5:48-5:56 lines, SYNC 34 + line 35 | 8 s | 13 s | 5 s |
| 6:20-6:35 G11, lines 37-38 | 15 s | 20 s | 5 s |
| 7:25-7:40 sway bars, SYNC 42 + line 43 | 15 s | 17 s | 2 s |
| 8:18-8:45 G14 + G15, lines 46-48 | 27 s | 35 s | 8 s |
| 8:50-9:08 SYNC 50 (5438 12.7-39) | 18 s | 26 s as spoken | 8 s |

- About one minute over in total. Either the plan's runtime goes to about 13:15, or cut: line 16's first sentence
  (Eibach is already named in SYNC 11), line 22's first two sentences, line 33's first sentence, line 38 (the Sonoma
  section already says "bed the brakes"), and trim the pause at 20-26 s in SYNC 50. Fix the footer either way.

---

## B. Non-blocking

### B1. Facts
| Line | Problem | Replacement |
|---|---|---|
| 9 | "Stock brakes" is supported (6589: stock disc and caliper; host says "stock brakes" at 154 s). "Tired" is not in any log. | "So this is what we started with. Stock brakes, old bushings, and those eBay coilovers." |
| 17 | "Steven" is supported by audio (6731 "What are you doing, Steven?", 6574 "you can film Steven"). "Old ones out" is not on film: the logs say there is no coilover removal. The sentence pair is also a slogan. | "Here's Steven getting them on the car." (ASK 2 stays) |
| 18 | Fine. Note 6738 shows the lower mount still loose; do not put this line over that shot. | - |
| 23 | Supported (6675 "Oh no it's stuck", 6676 "This is too rusted"). | - |
| 25 | Painting is on film (6685-6687, host spraying). Cleaning is not. | "And while the arms are off the car, they get a fresh coat of paint." |
| 28 | The bushing itself going in is not on film, only the sleeve (6816). The line is fine over 6816 if "New bushing in" is not illustrated with something else. | - |
| 38 | "Let me go bed the brakes" is real (Jun 07 11:08). But it means pads or discs were new on 7 June, three months after the table was filmed and after the 21 March track day. That makes ASK 1 more important: some of these parts may only have gone on at Sonoma. Add to ASK 1: "and which went on that weekend". | - |
| 40 | Supported: 6817 shows #558, 6821 the Whiteline logo. | - |
| 41 | Checked against the bracing script: stock NB, one front corner jacked, 3D scanned, same two braces (6698). Accurate. | split, see B6 |
| 43 | The host says "sway bar reinforcement bars". "For the sway bar mounts" and the reason given are the script's inference. Keep the ASK. | If unconfirmed: "And Good-Win sent the sway bar reinforcement bars to go with them." |
| 54 | Supported (5-7 June clips, "SONOMA TURN 9" banner). | see B3 |
| 55 | Real, but it is a crew member in the paddock, context unknown. Do not caption it as being about the sponsor parts. | - |
| 62 | Offers "the full install on any of these". The plan says the installs were not filmed and cannot be re-filmed for brakes, sway bars, tie rods and rack bushings. | "Want more? Tell us what you want to see next." (approved wording from the bracing video) |

### B2. Engineering
| Line | Problem | Replacement |
|---|---|---|
| 35 | A new rubber line is not that bad, and a braided line still expands a little. | "A rubber line swells a little every time you hit the pedal, and it gets worse as it ages. A braided stainless line swells a lot less. So the pedal is firmer." |
| 48 | "That goes away" overclaims. 37 words. | "And the rack bushings. The steering rack sits on rubber mounts. So when you turn the wheel, the rack shifts sideways a little before the tires do anything." then "Stiffer bushings take most of that out. And with a manual rack, you feel all of it." |
| 13, 20, 22, 27, 33, 37, 44 | Correct as general statements. Line 27 (rubber twists, polyurethane has to rotate, so it needs grease) is exactly right. | - |

### B3. Voice
| Line | Problem | Replacement |
|---|---|---|
| 4 | Six one-word sentences. This is the "tight copywriter" pattern he rejected. | "Coilovers, brakes, every bushing on the car, bracing, sway bars, and steering." (the chips still land on the beats) |
| 6 | Too long for its 5 s slot. | "So here's all of it, what it does, and then we go to the track." |
| 10 | "Corner to corner" is a phrase, and the video goes by system, not by corner. | "So we're going to go through it one part at a time. What it is, who sent it, and what it does. And at the end, we go drive it." |
| 20 | "Not the exciting part" opens the best-served sponsor's chapter by calling it dull. | "All right, bushings. This is the stuff nobody sees. But every suspension arm on this car connects to the chassis through one of these." |
| 53 | "Let's go find out" has no object. | "So that's everything on the car. Now let's go see what it does." |
| 54 | "June. Sonoma." is a title card, not speech. | "So in June, we took it to Sonoma." |
| general | "actually" appears in VO lines 6, 10, 13, 22, 41 and in the SYNC gag. Keep it in 13 and 41. | - |

### B4. SYNC quotes
| Line | Problem | Fix |
|---|---|---|
| 7 | He restarts the sentence: "We have our pink... sorry, I'm colorblind. We have our purple Miata, colloquially known as Grimace here, with a whole bunch of upgrade parts." The script drops the second "We have our" and stops on "here", which is mid-sentence. | Caption as spoken and let it run to about 20 s ("...upgrade parts"). |
| 3 and 8 | "courtesy of Mike Kojima and MotoIQ" is heard twice in under a minute, and line 8 opens on a sentence fragment. | Cold open: stop at "...parts to throw on this car" (27.9-32.3) with the MotoIQ chip. Intro: run 27.9-43.5 as one sentence. |
| 8 | Mentions Mike Kojima's daughter. The plan asks whether she may be named or shown; the script's ASK list does not. | Add to the ASK list. |
| 11 | The first sentence takes about 12 s to say (words at 82.5, 85.2, 92.9 s, then a gap to 97.8). It needs internal cuts under the cutaways. small.en has "very, very, very neat"; `medium.en` has "and very, very neat" with no "a". | Verify the wording by ear, cut the pauses under 6574 / 6729. |
| 19 | Stops on "available from Whiteline," with the sentence still going ("as well as the Whiteline front strut tower brace"). | Let it run to about 65 s. It is also the only spoken Whiteline credit for the brace, which line 40 then picks up. |
| 29 | Stops on "Wilwood," mid-list, before "I believe this is a Superlite". | See A2. If the cut stays, cover it with 6576. |
| 36 | "domestic... supplier" removes "manufacturer or domestic" from the middle of a sentence. Meaning is unchanged (he corrects himself), but it is a jump cut. | Cover with 6582 / 6583. |
| 42 | Removes "and I'm excited to do videos on how much the fender brace and strut tower brace affect the car". Clean and harmless. | Cover the cut with 6691 / 6692. |
| 2, 12, 24, 45, 50, 55 | Match the transcripts. Line 45: small.en "before the manual steering rack", `medium.en` "for the". | - |
| 51 | "Oh, we got it" (7.6 s) comes just before the puller line in 5441, so the wheel may already be off when he says it. | Check the order makes sense before using both. |

### B5. Sponsor fairness
- All ten names in the plan are spoken at least once and each is credited for the right part, subject to A1 and A2.
- **Good-Win's knuckle support** is on the table and named by the host (25-32 s) and is in no script line. Add it to line
  43 once ASK 6 gives the name: "And Good-Win sent the knuckle support and the sway bar reinforcement bars."
- **"MCS" is ambiguous on this channel.** The previous video labelled Miata Chop Shop as "IG @MCS_Parts" at the owner's
  request. Here MCS is the damper maker. Say the full name once (lower-third or VO) and add to ASK 10: "MCS here is the
  coilover company, not Miata Chop Shop: confirm the full name, logo and handle."
- Line 60 thanks Eibach, Wilwood and Fast Brakes as if each sent parts. The files only show that their products are on
  the table. ASK 10 should ask which are partners and which are brands inside someone else's kit.
- Halo P1 ("halo by Orthene" on the label), the steering wheel brand and the hub with gold studs are already in the ASK list.

### B6. Remaining splits for the cloned voice
| Line | Replacement |
|---|---|
| 37 | "Pads and fluid are the part people skip. A track pad is made to work hot." then "And the fluid matters because if it boils, the pedal goes long. That's the one you really don't want." |
| 41 | "Now, we already did a whole video on these two. We put them on a stock NB, jacked up one corner, and 3D scanned it." then "So if you want to see how much the chassis actually moves, link's up here." |
| 44 | "A sway bar ties the left side to the right side. When the car leans, the bar twists, and it fights that lean." then "And how stiff you go in the front versus the rear changes how the car rotates." |
| 60 | "Thank you to our technology partners at MotoIQ, and to Mike Kojima, for getting us set up with all of this." then "And to Good-Win Racing, Whiteline, MCS, Eibach, Fast Brakes, Wilwood, CSG, SPL and SuperPro. Check them out to get your own." |

### B7. Additions to the ASK list
1. (A2) Did Good-Win / Brian supply the brake kit and lines?
2. (A2) What is the item "underneath" the brake lines at about 141-145 s of 6662?
3. (A7) Is the kit's disc larger than stock?
4. (A8) Are the SPL tie rod ends bump-steer adjustable?
5. (B4) May Mike Kojima's daughter be mentioned as the driver?
6. (B5) MCS full name; which of Eibach, Wilwood and Fast Brakes are partners.
7. (B1) Which parts went on at Sonoma itself.

---

## Sign-off pass on v2

Checked 2026-11-14: `script.md` v2 against sections A and B above, `coverage.md` and `clips.md`. Line numbers are the
`#` column of the v2 table. v1 was not available, so "new in v2" means "not in this review's replacement text and not
supported by the two files". No audio was listened to; every "verify by ear" above is still open.

**Verdict: FAIL, narrowly.** A1-A8 are applied. A9 is only half applied: the footer was rewritten but its counts are
still wrong. Three small edits clear it (footer, line 39, line 48).

### 1. A1-A9
| Item | Applied? | v2 line | Note |
|---|---|---|---|
| A1 | yes | 28, 29 | Lead-in VO added; SYNC runs 35-49.5 with "for the control arms" and "thank you, Good-Win"; by-ear flag kept. |
| A2 | yes, one gap | 32, 38, 68; ASK 3, 5 | Line 32 marked provisional with the "courtesy of Brian" note; ASK 3 rewritten as asked; the "underneath" item is ASK 5; line 68 carries ASK 3. Gap: line 38 (brake lines) carries only ASK 5, not ASK 3, and has no note that "lines" vs "line" is unverified. |
| A3 | yes | 5, 59; ASK 12 | Span extended to 9.8-15.5, "pause trimmed", picture corrected to hub adapter on the wheel. Line 59 has no time span. |
| A4 | yes | 22, 23 | Replacement text verbatim; "thirty years" gone. |
| A5 | yes | 14, 15, 16, 17 | Verbatim. Line 17 drops "And the springs are from Eibach", which is the cut A9 suggested. |
| A6 | yes | 34 | Verbatim. |
| A7 | yes | 35, 36 | Verbatim; "bigger disc" held behind ASK 4. |
| A8 | yes | 52, 53, 54 | Verbatim; line 54 is cut unless ASK 8 confirms. |
| A9 | **partly** | footer | Footer now admits about 13 minutes and the plan re-cut, and the SYNC 58 pause is trimmed. But the stated "45 VO lines, about 800 words" is wrong (see 4), and one VO line is still over 30 words. |

### 2. B1-B7 not applied
All B1, B2, B3, B5, B6 replacements and all seven B7 asks are in v2. Not applied:
- B3 "actually": still in VO line 24 (the review kept it only in 13 and the bracing-video line, now 46). Cosmetic.
- B4 line 42 (now 47): no note to cover the internal cut with 6691 / 6692. Edit note only.
- B4 line 29 (now 32): no note to cover the cut after "Wilwood..." with 6576. Edit note only.
- B4 line 11: "a very, very neat" is kept although one model hears no "a"; covered only by the general by-ear rule in the header.
- B5 "say the MCS full name once": deferred to ASK 10, which is the right place.

None of these matters for owner sign-off. The two cover-shot notes should reach the edit plan so they are not lost.

### 3. New unsupported fact, number or mis-credit
- **Line 48**, "...the knuckle support and the sway bar reinforcement bars to go with them": this merges two alternative
  replacements from B1 and B5. "To go with them" now attaches the knuckle support to the Whiteline sway bars, which no
  file supports (the part's name is not even clear in the audio). Use the B5 wording and stop at "reinforcement bars."
- **Line 63**, "Bed the brakes, check the wheels, and send it": "bed the brakes" is in the files; "check the wheels" is
  in neither `coverage.md` nor `clips.md`. Could not tell whether it came from v1. Low risk, but confirm it is on film
  or drop the middle clause.
- No new numbers: the VO has none, consistent with the header.
- No sponsor mis-credit: every credit matches the `clips.md` supplier table. Line 68 still thanks Eibach, Fast Brakes
  and Wilwood as senders, but is tagged ASK 3 and ASK 10, so it is provisional, not wrong. Line 67 "technology partners
  at MotoIQ" is the review's own wording; the files only say "courtesy of".
- Footer "about 3 minutes of your on-camera speech": the SYNC spans as written add up to about 3.9 minutes before the
  internal trims. Plausible after trimming, but it is an estimate, not a measurement.

### 4. Counts
Counted from the table: rows whose Type is exactly `VO`, with bracketed `[ASK]` / `[PICKUP]` tags and the stage note in
line 19 removed. The two "yours" rows (65, 66) are not counted.
- **49 VO lines, 879 words, about 5.6 minutes** at 2.6 words/s. The footer says 45 lines and about 800 words: both
  wrong. That is more VO than v1 (850 words), so the overrun against the plan grew slightly.
- Without the two full PICKUP lines (33, 57) and the PICKUP tail of 31: 47 lines, 854 words. Still not 45 / 800.
- Over 30 words: **line 39 (32 words)**, the B2 brake-line replacement. Line 10 is exactly 30; lines 16 (29) and 55 (28)
  are close.

### To clear
1. Footer: "49 VO lines, about 880 words, about 5.6 minutes".
2. Split line 39 after "...as it ages."
3. Line 48: end at "reinforcement bars." Optionally add ASK 3 to line 38 and confirm "check the wheels" in line 63.
