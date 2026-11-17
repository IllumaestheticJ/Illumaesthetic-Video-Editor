# Pip & Gus Ep 5 (files step; v0.2 Ep 8): "STL or STEP? Mesh vs NURBS". Script v4 (for owner approval)

9:16, 1080x1920, 30 fps, about 35.5 s in total.
- **Cartoon:** about 0-27 s.
- **Real footage:** about 27-32 s.
- **Closing card:** 32-35.5 s. It carries the logo and the question text, with the hand-off to Ep 6 as voice only.

**Series position (v0.4, owner 2026-11-17; see "Series order and transitions" in `projects/pip-gus-series/scripts.md`):**
- This is the **files** step of making Pip's bumper.
- Ep 4 ("Can't you just 3D print the scan?") ends with Pip asking "If the scan's a mesh, what do you design in?".
- This episode opens on Ep 4's mesh on the laptop, with Pip repeating that question.
- It ends over the logo card with the lead-in to Ep 6 (SeamForge, the cutting step).

There is no "FULL VIDEO" teaser card (owner, 2026-11-16).

**Owner answers (2026-11-16):**
- Show any project, ideally one with both .stl and .stp versions.
- Yes, we offer scan-to-STEP resurfacing.
- The deviation map is colour only.
- End the video with the question "Do you design in CAD or in mesh?".

Status: **DRAFT. No voices or renders until the owner approves.** Open questions are marked [VERIFY] and listed at the bottom.

## v4 changes (series order v0.4, 2026-11-17)
- **Renumbered to Ep 5.** The callback now points to Ep 4, and the hand-off to Ep 6.
- **New hand-off line:** Gus now says "It's bigger than the printer."
- **The cartoon prop is now Pip's bumper** (the series through-line), not a mirror shell. "Bigger than the printer" only works for a bumper.

## v3 changes (series reorder, 2026-11-17)
- **New opening:** the Ep 3 (now Ep 4) callback replaces the envelope/"manufacturer wants a STEP" gag. Line 2 is now "Not the mesh. STL is just triangles."
- **Line 8 still lands:** "Print the mesh, send the STEP" now answers the opening question directly.
- **Ending:** the voice-only hand-off to the next episode is added over the closing card.

## What changed from the series draft (scripts.md v0.2)
- **Cut "a hundred flat bits".** It reads as a number, so the line is now "terrible to edit" and the picture does the explaining.
- **Merged lines 3 and 4 into a pair:** "Perfect for scans. Perfect for printing." / "Terrible to edit." This gives Gus a dry rhythm, and the slight annoyance lands on "terrible".
- **Line 8 is more concrete.** It is now "Print the mesh, send the STEP", which answers Pip's opening problem.
- **Added the "Is it done yet?" / "...No." running gag** on the scan-to-STEP rebuild. It shows the rebuild is slow without giving a time.
- **Added Pip's phone hand-off,** with a new line for this episode, going into the real footage.
- **The hole edit is shown with a slider that has no numerals.** No dimension appears on screen.

## Dialogue

| # | t (s) | Who | Line (emotion tag for v4) | Picture | Caption |
|---|---|---|---|---|---|
| 1 | 0.2-3.0 | PIP | [curious] "If the scan's a mesh, what do you design in?" | Callback to Ep 4: Pip's bumper scan mesh on the shop laptop. Pip leans in at the screen | yes |
| 2 | 3.2-6.2 | GUS | [matter-of-fact] "Not the mesh. STL is just triangles." | Gus taps the screen. Camera dives in until the surface is all flat triangles | yes |
| 3 | 6.4-8.6 | GUS | "Perfect for scans. Perfect for printing." | Mesh drops into the unbranded cartoon printer, which prints it fine. A small tick pops up | yes |
| 4 | 8.7-10.0 | GUS | [slightly annoyed] "Terrible to edit." | Gus's floating hand drags one edge, and a ragged clump of triangles tears along with it | yes |
| 5 | 10.3-13.0 | GUS | "STEP is NURBS. Smooth math surfaces." | The same bumper re-forms as a few clean glowing patches with crisp edges | yes |
| 6 | 13.1-16.2 | GUS | "Change a hole, a thickness, a fillet... it just updates." | A slider (no numbers) grows a bolt hole, then the wall thickens and an edge rounds. Each change updates cleanly | yes |
| 7 | 16.4-17.4 | PIP | [curious] "So which one?" | Pip looks between the two bumpers | yes |
| 8 | 17.5-21.0 | GUS | "Scan in mesh. Design in NURBS. Print the mesh, send the STEP." | A loop board: SCAN (STL) → CAD (STEP) → PRINT (STL) / MANUFACTURER (STEP) | yes |
| 9 | 21.2-22.8 | PIP | [curious] "Can you turn a scan into a STEP?" | | yes |
| 10 | 22.9-25.0 | GUS | [weary] "You rebuild it. Surface by surface." | Gus lays patches over the scan mesh one at a time. The wall clock starts to spin | yes |
| 11a | 25.0-25.7 | PIP | [impatient] "Is it done yet?" | | yes |
| 11b | 25.8-26.2 | GUS | "...No." | | yes |
| 12 | 26.3-27.6 | PIP | [excited] "Illumaesthetic does that. Look!" (owner confirmed the service) | Pip holds up the phone. Camera pushes into the screen until the real footage fills the frame (hard cut on a beat) | yes |

That is about 80 spoken words, which fits in about 27 s at the pilot's pace with no speed-up.

**Pronunciation in the v4 prompt:**
- STL is spelled out ("S-T-L").
- STEP is said as a word ("step"), not spelled out.
- NURBS is said "nurbs".
- Check Illumaesthetic in the take; the owner has accepted the v4 pronunciation before.

## Real footage (about 27-32 s, no text, no VO, music only)

| t (s) | Shot | Source |
|---|---|---|
| 27.6-29.0 | Real footage of the bumper or car (still open: no NSX or F100 footage found in Dropbox) | TBD |
| 29.0 (beat) | **Hard cut** to the bumper STL scan in the house silver look (1:1 if real footage of this bumper exists) | Drive: `NA1 NSX/NA1 Bumper.stl` (about 125 MB, a raw scan) |
| 29.0-30.6 | Same camera: the mesh's triangles give way to the resurfaced STEP patches | Drive: `NA1 NSX/NA1 Bumper.stp` |
| 30.6-32.0 | The STL-vs-STEP deviation map: **colour only, no legend, no numbers** | Computed from the two files |

**Project choice (owner, 2026-11-17: "use a bumper - not ioniq"):** the NA1 NSX bumper. It is the best scan + STEP pair on the Drive. Other bumper pairs:
- **F100 bumper:** `F100 Bumper-Whole.stl` (scan) and `F100 Bumper-Whole_R1.stp`.
- **NSX lower front end:** `NSX Lower Front End.stl` (500 MB scan) and its `.stp` (2023).
- **Nissan bumper:** `Nissan Bumper.stl` and `.stp` (2022).
- **Model 3 front bumper:** scans and a `-3dp.stp`.

## End cards
- **32-35.5 s, closing card (the last frame of the video):**
  - The Illumaesthetic logo, with **DO YOU DESIGN IN CAD OR IN MESH?** under it (owner request, 2026-11-16).
  - Fjalla One on the dark plate; this is a card, not text over footage.
  - No other call to action.
  - **Voice only (no captions, no new text), the hand-off to Ep 6:**
    - PIP [excited] "Design's done. Hit print!"
    - GUS [matter-of-fact] "It's bigger than the printer."
  - **Check:** the series rule says the ending is voice only with no new text, and your question text is still on this card. I've kept both, since the question was your request; say if the text should go.

## Rules this script follows
- **No numbers:** no number on screen or in dialogue, and no tolerances, hours or prices. The deviation-map legend is only shown if the owner OKs it (Q3); its values come from the file.
- **No brands:** no CAD, slicer, scanner or printer brand.
- **No text over real footage:** captions are on the cartoon only.
- **Real-to-scan transition:** a hard cut on a beat, with no dissolve.
- **Voice and look:** Gus stays dry and only slightly annoyed, and Pip goes from frustrated to curious to excited. Characters are the locked spec: dot eyes, no brows, no arms, nametags.

## Superseded
- **Ioniq 5 mirror and Tokyo Auto Salon footage:** dropped (owner, 2026-11-17: "use a bumper - not ioniq"). The history is in `editlog.jsonl`.
- **Open item:** real footage of the chosen bumper or car. Dropbox has nothing under "NSX" or "F100".
