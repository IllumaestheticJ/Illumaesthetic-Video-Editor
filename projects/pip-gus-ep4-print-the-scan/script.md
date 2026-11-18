# Pip & Gus Ep 4: "Can't you just 3D print the scan?" (script v1, for owner approval)

Was Ep 2 (v0.2), then Ep 3 (v0.3). Series v0.4 (owner 2026-11-17: "bumper first, then the steps of creation"): this is the **design**
step. Ep 1 is "Why can't I just print the bumper I want?" ("...but if you insist"). Eps 2-3 scan the car. This episode opens on the
finished scan on the laptop with Pip repeating Ep 3's last question. The part being designed is **Pip's bumper from Ep 1**. It ends with Pip
asking Ep 5's question (STL vs STEP) over the logo card, voice only. The branch keeps its old name, `claude/pip-gus-ep2-print-the-scan`.

9:16, 1080x1920, 30 fps, **about 37-38 s**. Concept approved by the owner. This version is tightened from
`projects/pip-gus-series/scripts.md` (Ep 4, was Ep 2). Nothing gets voiced or rendered until the owner approves it.

**Question the episode answers:** "I bought the scan, so why can't I just print a part from it?"
**Answer in one line:** a scan is a skin (a surface of tiny triangles with no thickness). It's the *reference*: you design
the part on it, and the scan is what makes the part fit.

## Shape and timing (estimates; final timing comes from the voice take, with no speed-ups)
| Part | Time | What |
|---|---|---|
| A. Cartoon | about 0-30 s | 14 lines, word-by-word captions (Fjalla One; Pip sage #619f73, Gus #ecefec, dark plate) |
| B. Real footage | about 30-35 s | phone hand-off, then the GT350 with its bumper gone, a **hard 1:1 cut on a beat** to its scan, then the bumper and a lip designed on the scan. No text. |
| C. Logo card | about 35-38 s | plain Illumaesthetic logo, no text, no teaser card; Pip asks Ep 5's question over it (voice only) |

## Part A: cartoon
| # | Who (delivery tag) | Line | Picture |
|---|---|---|---|
| 1 | PIP [eager] | "OK, it's scanned. Can we print it now?" | Opens on the finished scan on Gus's laptop (callback to Ep 3's ending). Pip bounces beside it. |
| 1b | PIP [excited] | "My bumper! Print my bumper!" | Pip shoves the glowing cartoon car scan off the laptop onto an unbranded cartoon printer. Her bumper sketch from Ep 1 is taped to the wall behind. ^ ^ eyes. |
| 2 | GUS [flat] | "That's a scan. It's a skin." | Gus pulls the scan off again; push in until the nose becomes a sea of tiny triangles. Pip's eyes go wide. |
| 3 | GUS [matter-of-fact] | "A mesh of tiny triangles. No thickness." | Gus flicks the surface with a floating mitten; it wobbles like cling film. |
| 4 | PIP [impatient] | "So... print it anyway?" | Pip nudges the printer. |
| 5 | GUS [dry] | "Sure." | Gus drops the scan into the cartoon slicer (no brand UI). The preview is an empty build plate: no layers, nothing to slice. The wall clock starts to spin (series gag). |
| 6 | PIP [impatient] | "Is it done yet?" | Pip slumped on a stool, clock hands whirring, staring at the printer, which hasn't moved. |
| 7 | GUS [deadpan] | "...There's nothing to print." | Gus slides out the empty build plate and sets it on the **failed-print shelf**, next to the spaghetti print from Ep 1 (the shelf keeps filling up through Ep 9). Pip's eyes: flat cut. Gus's eyes: half-lid. |
| 8 | GUS [patient, slightly tired] | "The scan is the reference. You can remake the original from it..." | Gus traces the stock bumper on the scan; the traced lines turn into a clean solid copy of the original, which clicks into place. |
| 8b | GUS [matter-of-fact] | "...or design a new one *on* it." | Gus pulls Pip's sketch off the wall and draws her bumper over the scan; it hugs every curve, turns solid and snaps on: "click". This is the bumper Pip has wanted since Ep 1. |
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
  the failed-print shelf (next to Ep 1's spaghetti) is the visual joke.
- Series v0.4: opens on Ep 3's question, designs Pip's bumper from Ep 1 (line 8b; was a lip), and sets up "mesh" for Ep 5's question.
- Lines 7 and 8 split the joke from the explanation, so the empty plate gets its own beat.
- New hand-off (lines 11-12), varied per the series rule: Pip finds that Illumaesthetic does both (designing on the scan and reverse
  engineering), and Gus's "Of course they do" keeps him dry, not angry.
- Line 8 is split into 8/8b to cover both uses of a scan (owner, 2026-11-16). Reverse engineering comes first and the new design
  second, so the order matches the real GT350 job in Part B (bumper remade, then a lip built off the scan).
- No numbers anywhere in the cartoon (no triangle count, no sizes, no times).

## Part B: real footage: the white GT350 job (owner photos + Drive scans, 2026-11-17; aim about 5 s, no text)
This is the owner's own job, and it is the design step for real:
- **Remake the original:** the crash destroyed the bumper, and that bumper no longer exists. Illumaesthetic scanned the car and reverse-engineered
  the bumper on the scan.
- **Build off the scan:** a new front lip (tan) was then designed on the scan.
Media (not committed): `/home/user/media/pip-gus-ep4-print-the-scan/photos/IMG_0763-0781.jpeg`; scans and CAD on the Drive (clips.md).

| Beat | Shot | What it shows |
|---|---|---|
| 1 | IMG_0763 (or 0764), photo | the crash: front bumper torn off |
| 2 | IMG_0770, photo | scanning the stripped front end (bumper off) |
| 3 | **hard cut on the beat** -> render of the bumper-off scan (`GT350_Lip.blend`), same front-right corner as IMG_0770, slow push | the same car, now the scan |
| 4 | same render, continuing | the reverse-engineered bumper (green) slides on and settles (remake the original) |
| 5 | render, low three-quarter | the designed lip (tan) slides in under the bumper and hugs the curve (design a new part on it) |

Renders use the owner's `GT350_Lip.blend` (Drive, Ron's "GT350 Bumper" folder, uploaded 2026-11-18): the car scans, the
reverse-engineered bumper and the lip are aligned there. The look matches the owner's screenshots (Workbench studio light,
lavender scan, green bumper, tan lip, dark grey background). `tools/partB_render.py`.
The cut from IMG_0770 is a hard cut on the beat, **not a true 1:1**. The photo is a close, steep 1440 px still of a partial
corner, and the solve didn't hold (raycasts fell through scan gaps, and the features were ambiguous). A true 1:1 needs a video
frame or a full-res photo with the whole corner in view.

- One shot per beat (about 1 s each), hard cuts on the beat. No dissolves and no text.
- The 1:1 cut uses the *bumper-off* scan state, which is what IMG_0770 shows, so car and scan match exactly.
- **Not in this episode (owner 2026-11-17: "not the final photos"):** the printed bumper fitted on the car (IMG_0765/0766/0767). Those, and
  the 46-piece print split on the Drive (`Bumper/Slice Test`), are kept for the Ep 9 finale. This episode stops at the design.
- Scan look (owner 2026-11-17: "you can use the GT350 Blender photos in here"): the scan beats are the owner's own Blender views
  (lavender scan, green bumper, tan lip) instead of the house silver. The screenshots are small landscape images (1115-1457 px wide,
  about 400 px in a 9:16 crop), so each view is re-created at full resolution in the same Blender look from the Drive files, matching
  the screenshot's angle. The screenshot itself is the fallback. Beat 3's 1:1 render uses the same look so beats 3-5 match.
- Still excluded: IMG_0779-0781 (viewer toolbars, mm labels).
- Owner OK'd showing the crash photos and the person scanning (2026-11-17). Still blur any readable plates.
- Resolution: only beats 1-2 are photos (1440x1080, about 600 px wide in a 9:16 crop). The full set is in the owner's WhatsApp, and the
  owner can save it if needed.

## Part C: logo card (the ending)
Plain Illumaesthetic logo (about 720 px wide on 1080), no line under it. Owner's choice (2026-11-17).

**Over the logo card, voice only (series v0.4):** PIP [curious] "If the scan's a mesh, what do you design in?" This leads into Ep 5
(STL vs STEP), and Gus's line 3 ("A mesh of tiny triangles") sets up the word. No caption: the logo card stays plain.
No "FULL VIDEO ON OUR CHANNEL" teaser card (owner rule 2026-11-16: only when a matching full video exists).

## Voices, music
- Voices: one Higgsfield `elevenlabs_v4` dialogue call. Pip = Kiki (`2d51d9d0-b2a4-5e8b-9c63-f310adafd5f7`), Gus = Harrison
  (`573e5163-59b3-4926-aab1-951ef2985f81`), emotion tags as above, no speed-up. The take goes to the owner before animation.
- Music: a curious, inquisitive generated bed (ElevenLabs Music v2.5 via Higgsfield), with a lift on the phone hand-off (line 12).
  Not game or battle music, and not the pilot's track (each reel gets its own music).

## [VERIFY] open questions for the owner
1. ~~Real footage~~ answered (owner 2026-11-17): the GT350 job, with the bumper reverse-engineered and then a lip built off the scan. See Part B.
2. ~~Line 8~~ answered (owner 2026-11-16): "you design the part on it, or you remake/reverse engineer the part - Illumaesthetic
   can do both." Line 8 now covers both, and Pip's line 11 is "Ooh! Illumaesthetic does both!"
3. ~~Ending~~ answered (owner 2026-11-17): plain logo card, no teaser card.
4. ~~GT350 files~~ found on the Drive (clips.md): car scans in Engineering Design / Ford Mustang Shelby GT350 (S197); bumper + lip in
   Ron's Folder / GT350 Bumper.
5. ~~Video/originals~~: in the owner's WhatsApp; they'll save the folder if needed.
6. ~~Whole-bumper overlap~~ (owner 2026-11-17): printing the whole bumper is worth it when that bumper no longer exists. This is now Ep 1's "...but if you insist".
7. ~~OK to show~~: yes (owner 2026-11-17).
8. ~~The lip, for real~~: yes, on the Drive (owner 2026-11-17).
9. ~~Spoiler check~~ (owner 2026-11-17): use the GT350 Blender views here, not the final photos.
