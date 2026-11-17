# Pip & Gus Ep 2: "Can't you just 3D print the scan?" (script v1, for owner approval)

9:16, 1080x1920, 30 fps, **about 36-37 s**. Concept approved by the owner. This version is tightened from
`projects/pip-gus-series/scripts.md` (Ep 2). Nothing gets voiced or rendered until the owner approves it.

**Question the episode answers:** "I bought the scan, so why can't I just print a part from it?"
**Answer in one line:** a scan is a skin (a surface of tiny triangles with no thickness). It's the *reference*: you design
the part on it, and the scan is what makes the part fit.

## Shape and timing (estimates; final timing comes from the voice take, with no speed-ups)
| Part | Time | What |
|---|---|---|
| A. Cartoon | about 0-28 s | 13 lines, word-by-word captions (Fjalla One; Pip sage #619f73, Gus #ecefec, dark plate) |
| B. Real footage | about 28-33 s | phone hand-off, then real car, then a **hard 1:1 cut on a beat** to its scan, then the designed part on the scan. No text. |
| C. Logo card | about 33-36 s | plain Illumaesthetic logo, no text, no teaser card (owner 2026-11-16/17) |

## Part A: cartoon
| # | Who (delivery tag) | Line | Picture |
|---|---|---|---|
| 1 | PIP [excited] | "We got the scan! Let's print a lip!" | Pip shoves the glowing cartoon car scan onto an unbranded cartoon printer. ^ ^ eyes. |
| 2 | GUS [flat] | "That's a scan. It's a skin." | Gus pulls the scan off again; push in until the nose becomes a sea of tiny triangles. Pip's eyes go wide. |
| 3 | GUS [matter-of-fact] | "Tiny triangles. No thickness." | Gus flicks the surface with a floating mitten; it wobbles like cling film. |
| 4 | PIP [impatient] | "So... print it anyway?" | Pip nudges the printer. |
| 5 | GUS [dry] | "Sure." | Gus drops the scan into the cartoon slicer (no brand UI). The preview is an empty build plate: no layers, nothing to slice. The wall clock starts to spin (series gag). |
| 6 | PIP [impatient] | "Is it done yet?" | Pip slumped on a stool, clock hands whirring, staring at the printer, which hasn't moved. |
| 7 | GUS [deadpan] | "...There's nothing to print." | Gus slides out the empty build plate and sets it on a new, empty shelf: the **failed-print shelf** (gag starts here with literally nothing on it, filled from Ep 3). Pip's eyes: flat cut. Gus's eyes: half-lid. |
| 8 | GUS [patient, slightly tired] | "The scan is the reference. You design a part *on* it..." | Gus draws a clean, solid new lip that hugs the scan's curve; it turns solid and snaps onto the cartoon car: "click". |
| 8b | GUS [matter-of-fact] | "...or reverse-engineer the original from it." | Gus traces the stock bumper trim on the scan; the traced lines turn into a clean solid copy of the original part, which pops out next to the car. |
| 9 | PIP [curious] | "So the scan is what makes it fit?" | Pip peers along the seam: zero gap. |
| 10 | GUS [matter-of-fact] | "Every curve." | Gus runs a mitten along the bumper line; small sparkle at the seam. |
| 11 | PIP [excited] | "Ooh! Illumaesthetic does both!" | Pip whips out the phone and holds it up to Gus. The screen plays the real car (Part B's first shot). |
| 12 | GUS [dry, slightly impressed] | "...Of course they do." | Gus leans in; the camera pushes into the phone until the screen fills the frame. Hard cut on the beat. |

Changes from the series draft (and why):
- Dropped "No edges." It's vague and easy to argue with; "Tiny triangles. No thickness." is the accurate core claim.
- Owner (2026-11-16): "you technically can't even print the scan at all." So nothing gets printed. A surface with no thickness
  has no volume to slice: the slicer shows an empty plate and the printer never moves. The old "paper-thin ghost lip" gag was wrong
  and is gone.
- Lines 6-7 use the series "Is it done yet?" gag, and the answer is "...There's nothing to print." The empty build plate going onto
  the brand-new failed-print shelf is the visual joke.
- Lines 7 and 8 split the joke from the explanation, so the empty plate gets its own beat.
- New hand-off (lines 11-12), varied per the series rule: Pip finds that Illumaesthetic does both (designing on the scan and reverse
  engineering), and Gus's "Of course they do" keeps him dry, not angry.
- Line 8 is split into 8/8b to cover both uses of a scan (owner, 2026-11-16).
- No numbers anywhere in the cartoon (no triangle count, no sizes, no times).

## Part B: real footage: the white GT350 bumper job (owner photos, 2026-11-17; aim 5 s, no text)
The owner's own job is this episode's story told for real. A crashed car's bumper was destroyed. Illumaesthetic scanned the car and the
broken bumper, reverse-engineered the bumper on the scan, and printed it, and it fits. That is lines 8b-10 of the cartoon, so Part B
is the proof. Media (not committed): `/home/user/media/pip-gus-ep2-print-the-scan/photos/IMG_0763-0774.jpeg`.

| Beat | Shot (photo) | What it shows |
|---|---|---|
| 1 | IMG_0763 (or 0764) | the crash: front bumper torn off |
| 2 | IMG_0770 | scanning the stripped front end |
| 3 | IMG_0773 | the broken bumper's scan |
| 4 | IMG_0774 | the reverse-engineered bumper (green) on the car scan |
| 5 | IMG_0766 -> IMG_0767 | the printed bumper on the car, fitted (close, then the whole car) |

- One shot per beat (about 1 s each), slow push-ins on the stills, a hard cut on every beat. No dissolves and no text.
- Shots 4 -> 5 are the scan-to-real moment. A true 1:1 perspective cut needs the scan + CAD rendered from the camera of IMG_0766
  (`ive solve`), which is only possible if the scan and bumper files are available (Q4). Otherwise it's a plain hard cut on the beat.
- The photos are 4:3 (1440x1080). A 9:16 crop is only about 600 px wide, so this needs the full-res originals or a different
  framing (Q5).
- Check before use: plates and bystanders in the crash photos (police SUVs, passing cars), and the people in IMG_0770/0769.

## Part C: logo card (the ending)
Plain Illumaesthetic logo (about 720 px wide on 1080), no line under it. Owner's choice (2026-11-17).
No "FULL VIDEO ON OUR CHANNEL" teaser card (owner rule 2026-11-16: only when a matching full video exists).

## Voices, music
- Voices: one Higgsfield `elevenlabs_v4` dialogue call. Pip = Kiki (`2d51d9d0-b2a4-5e8b-9c63-f310adafd5f7`), Gus = Harrison
  (`573e5163-59b3-4926-aab1-951ef2985f81`), emotion tags as above, no speed-up. The take goes to the owner before animation.
- Music: a curious, inquisitive generated bed (ElevenLabs Music v2.5 via Higgsfield), with a lift on the phone hand-off (line 12).
  Not game or battle music, and not the pilot's track (each reel gets its own music).

## [VERIFY] open questions for the owner
1. ~~Real footage~~ answered (owner 2026-11-17): the GT350 bumper reverse-engineering job (photos). See Part B and Q4-Q7.
2. ~~Line 8~~ answered (owner 2026-11-16): "you design the part on it, or you remake/reverse engineer the part - Illumaesthetic
   can do both." Line 8 now covers both, and Pip's line 11 is "Ooh! Illumaesthetic does both!"
3. ~~Ending~~ answered (owner 2026-11-17): plain logo card, no teaser card.
4. **GT350 files:** are the car scan and the reverse-engineered bumper (STL/STEP) on the Drive? With them, shot 4 -> 5 becomes a true
   1:1 cut from the scan to the printed bumper.
5. **Video and originals:** is there video of this job in Dropbox, or the full-resolution photos? These are 1440 px wide, which is
   soft once cropped to 9:16.
6. **Ep 3 overlap:** Ep 3 argues against printing a whole bumper, and this job is a printed whole bumper. Was it the final part, a
   test fit, or a one-off because the part can't be bought? The answer decides whether Ep 2 shows it as the result.
7. **OK to show:** the crash photos (the police scene in the background) and the person scanning?
