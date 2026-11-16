# Pip & Gus: explainer series, draft scripts (v0.2, 2026-11-16)

These are drafts for owner review; nothing is produced yet. Each episode answers one common question about car 3D scanning or 3D printing.

**Owner decisions (2026-11-16):**
- Kept from v0.1: Spray (Ep 1) and "Can't you just print the scan?" (Ep 2).
- Kept and deepened: "Why not print the whole bumper?" (Ep 3), now explaining why it isn't cheap or worth it.
- Dropped: under the car, accuracy.
- Added: the Seamforged app, glueing prints, big vs small printers, materials for car parts, and NURBS vs mesh (STEP vs STL).

## Series format
- The template is the IS350 explainer ("The usual way"): about 40 s at 9:16, made of three parts.
  1. **Cartoon (about 25-32 s).** Pip asks the question. Gus shows the hard or wrong way, dry and only slightly annoyed. A running gag escalates, and Pip finds the better way.
  2. **Real footage (about 4-6 s, longer only if it earns it).** Illumaesthetic doing it, with a hard 1:1 real-to-scan cut on a beat where one fits.
  3. **End cards.** The teaser card ("FULL VIDEO ON OUR CHANNEL" with a clip in a frame), then the logo card.
- **Characters** (locked spec in `projects/scan-tedium-explainer-reel/characters/design.md`):
  - **Pip** (kid, voice Kiki): curious and impatient; asks the question; gets excited at the end.
  - **Gus** (dad, voice Harrison): knows the job, matter-of-fact, mildly annoyed that it's tedious, never angry.
  - Shared look: dot eyes, no eyebrows (expressions are eye shapes only), no arms, cel-shaded shop.
- **Running gags:**
  - the pile of peeled dots in the corner;
  - the spinning wall clock;
  - "Is it done yet?" / "…No.";
  - a growing shelf of failed prints (new, used from Ep 3 on);
  - Pip's phone hand-off before the real footage. Vary the line per episode.

**Rules:**
- No invented numbers. Lines marked [VERIFY] need the owner's confirmation; general-knowledge claims are kept qualitative (no temperatures, prices or print hours on screen unless the owner supplies them).
- No competitor, printer or scanner brand named or mocked. Slicer screens are shown without brand UI or are re-drawn in the cartoon.
- No text over real footage; captions go on the cartoon half only.
- The real-to-scan transition is a hard 1:1 cut on a beat, never a dissolve.

---

## Ep 1. "Why do you spray the car?" (approved)
**Question:** what's the white powder, and is it bad for the paint?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Why is the car… white?" | The cartoon sedan, half-dusted, looks like a powdered donut. Pip pokes it and leaves a fingerprint. |
| 2 | GUS | "Shiny paint confuses the scanner." | The scanner cone hits glossy paint and bounces off in cartoon zig-zags; "?" pops out of the scanner. |
| 3 | GUS | "Black paint, chrome, glass… it can't see any of it." | Inserts: a black bumper with no scan, chrome reflecting Gus's face, a window the cone passes through. |
| 4 | PIP | "So you paint it?" | |
| 5 | GUS | "Dust it. It wipes right off." [VERIFY: spray type and removal] | Gus "dusts" with a giant powder puff; a cloud fills the shop. |
| 6 | PIP | (coughing) "…There has to be a less messy way." | Only Pip's dot eyes show in the cloud; they blink. |
| 7 | PIP | "Wait. Illumaesthetic does it in like one coat." [VERIFY wording; no time] | Phone hand-off. |

**Real footage:** the IS350 spray (long-form E14 / R3 spray), a 1:1 cut to the scan, the teaser card and the logo card.
**Footage in hand:** yes.

---

## Ep 2. "Can't you just 3D print the scan?" (approved)
**Question:** I bought the scan, so why can't I just print a part from it?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "We have the scan! Let's print a lip!" | Pip drags the car scan onto a cartoon printer. |
| 2 | GUS | "That's a scan. It's a skin." | Zoom in: the scan turns into a sea of tiny triangles. Pip's eyes go wide. |
| 3 | GUS | "Tiny triangles. No thickness. No edges." | Gus flicks the surface; it wobbles like cling film. |
| 4 | PIP | "So… print it anyway?" | |
| 5 | GUS | "Sure." | The printer makes a paper-thin ghost of the car's nose; it flops over onto the failed-print shelf (gag starts). |
| 6 | GUS | "The scan is the reference. You design the part on it." | Gus draws a clean, solid lip that hugs the scan; it snaps on with a "click". |
| 7 | PIP | "So you need the scan to make it fit?" | |
| 8 | GUS | "Every curve." | |
| 9 | PIP | "Then where do I get one?" | Pip's eyes do ^ ^. Cut. |

**Real footage:** a real car to its scan (1:1 cut), then a designed part on the scan, then the logo with **SCANS AVAILABLE AT ILLUMAESTHETIC.COM**.
**To confirm:** [VERIFY] which part designs we may show on a scan.

---

## Ep 3. "Why not just print the whole bumper?" (approved; owner: explain why it isn't cheap or worth it)
**Question:** if you can print parts, why not print a whole bumper or body kit and skip buying one?

The argument is built as a running tally of hidden costs. Each line adds an icon to a "bill" that keeps growing on the cartoon wall. The bill is pictures only: no prices or hours on it.

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Just print the bumper! Plastic is cheap!" | Pip holds one spool of filament proudly. |
| 2 | GUS | "One bumper?" | Gus wheels in a stack of spools taller than Pip. Bill icon 1: spools. [VERIFY: the owner's typical filament use for a bumper, or keep it qualitative] |
| 3 | GUS | "It doesn't fit on a printer. So it's printed in pieces." | The bumper is sliced like bread; the pieces print one by one while the clock spins. Bill icon 2: clock. |
| 4 | GUS | "One piece fails overnight…" | A piece comes out as spaghetti and goes onto the failed-print shelf. Bill icon 3: the spaghetti. |
| 5 | GUS | "…then glue, filler, sanding, primer." | Montage: glue, filler, a sanding cloud, primer. Bill icons 4-7. |
| 6 | PIP | "Is it done yet?" | |
| 7 | GUS | "…No. Then the sun hits it." | The cartoon sun beats down; a printed bumper in the wrong plastic slowly droops (callback to Ep 7). |
| 8 | GUS | "And a curb." | A curb taps the bumper; it cracks along a glue seam. Bill icon 8: a cracked seam. |
| 9 | PIP | (looking at the bill, which now reaches the floor) "…So when IS it worth printing?" | |
| 10 | GUS | "Prototypes. Test fits. Small parts. That's where printing wins." [VERIFY: the owner's actual position] | Gus holds up a small printed test piece; it clicks onto the car perfectly. Pip's eyes do ^ ^. |

**The point:**
- Printing a full bumper costs material, many print hours across many pieces, failed prints, and hours of glueing and finishing.
- The result can still be weaker and less heat-resistant than a production part.
- Printing is great for test fits, prototypes and small parts.

[VERIFY] The owner's real process: what is printed and what is made another way. Final lines are written only after the owner confirms.

**Real footage:**
- The owner's slicer screen recordings in Dropbox, `/2. Illumaesthetic Videos/1. Video dumps/Seamforged/Seamforged V1/`, show a bumper cut into dozens of pieces across many build plates. That's a perfect, real "this is what one bumper turns into" shot.
- Then a real test-fit part.

---

## Ep 4. "What does Seamforged do?" [NEEDS OWNER BRIEF]
**Question:** what is Seamforged, and why would I use it?

**What I know:** the only material is the owner's screen recordings in Dropbox: `/2. Illumaesthetic Videos/1. Video dumps/Seamforged/Seamforged V1/` (2026-08-23, 3 clips).
- They show large car parts (a bumper and body panels) being cut by hand into many printable pieces in a slicer, then laid out across many build plates.
- I couldn't find the app online, so I have no feature list.
- **[VERIFY] I need the owner's one-paragraph description:** what Seamforged does, its 2-3 key features, who it's for, where to get it, and whether it's free or paid. The draft below assumes it automates splitting a big part into printable pieces with seams or joints that line up. If that's wrong, the beats change.

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "The bumper's too big for the printer." | Pip pushes the bumper at the printer; it doesn't fit. |
| 2 | GUS | "So we cut it. By hand." | Gus with a cartoon saw cutting a virtual bumper on a laptop; pieces scatter. |
| 3 | GUS | "Every cut. Every piece. Every plate." | The laptop screen fills with dozens of pieces on dozens of plates (re-drawn from the real recordings). The clock spins. |
| 4 | PIP | "And they line up after?" | Two printed pieces meet with an offset step and a gap. Pip's eyes go flat (annoyed D-cut). |
| 5 | GUS | "…Mostly." | One piece goes onto the failed-print shelf. |
| 6 | PIP | "There has to be a better way." | |
| 7 | GUS | (deadpan, beat) "…There's an app for that." | Gus pulls out the phone himself for once; a reversal of the running gag. |

**Real footage:** Seamforged in use. [VERIFY] Screen capture of the app doing the split, then printed parts joining up.
**Call to action:** a Seamforged card. [VERIFY: name and logo, URL or store, availability]

---

## Ep 5. "How do you glue prints together?"
**Question:** what's the best way to join printed pieces?

The structure is a "glue tier list": Gus tries each method on two printed blocks, and Pip rates it with his eyes.

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "It printed in pieces. Now what?" | Two printed halves of a part. |
| 2 | GUS | "Superglue. Fast. But brittle." | Gus glues; it grabs instantly; Pip taps it; it snaps. Pip: squint. |
| 3 | GUS | "Two-part epoxy. Strong, fills gaps. Slow." | Mixing two blobs; the clock spins; the joint holds when Pip hangs off it. Pip: ^ ^. |
| 4 | GUS | "Plastic welding. Melt the same plastic into the seam." | A hot tool melts filament into a V-groove along the seam; it fuses into one piece. Pip's eyes pop. |
| 5 | GUS | "Some plastics you can solvent-weld." [VERIFY: which materials the owner uses this on; ABS/ASA with acetone is the common case, PLA isn't] | A brush wipes the seam; the halves melt together. A "not for every plastic" stamp. |
| 7 | GUS | "And pins or keys so they line up." | Printed dowels or dovetails click the halves into alignment before glueing. |
| 8 | PIP | "Which one do you use?" | |
| 9 | GUS | "Depends on the part." [VERIFY: the owner's actual preference per use] | Cut to real. |

**Real footage:** [VERIFY] the owner joining printed parts (epoxy or a welding pen on a seam). If none exists, a short shoot is needed.
**Accuracy note:** all method claims here are general and widely documented, with no numbers. The owner should confirm which methods they actually use and recommend.

---

## Ep 6. "Big printer or small printer?"
**Question:** should I buy a big-format printer or a regular one for car parts?

The structure is a side-by-side duel: Gus runs a big printer and Pip runs a small one. Each line scores a point on a cartoon scoreboard (icons, not numbers).

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Bigger printer, bigger parts!" | Pip next to a huge printer, tiny by comparison. |
| 2 | GUS | "Fewer pieces. Fewer seams. Less glue." | The big printer makes a large panel in one go. Point to BIG. |
| 3 | GUS | "But it costs more, takes more space…" | A cartoon wallet empties; the printer barely fits through the shop door. Point to SMALL. |
| 4 | GUS | "…and one failed print wastes a lot more." | A huge spaghetti failure lands on the failed-print shelf; the shelf bends. Point to SMALL. |
| 5 | PIP | "Small ones are fast and cheap." | |
| 6 | GUS | "And you can run a few at once." | Three small printers side by side, all printing. Point to SMALL. |
| 7 | GUS | "But more pieces means more seams." | The pieces pile up and there's more glue (callback to Ep 5). Point to BIG. |
| 8 | PIP | "So which one wins?" | The scoreboard is tied. |
| 9 | GUS | "Depends on the part." [VERIFY: the owner's real setup and advice] | |

**Real footage:** the owner's printer(s) running, if available. [VERIFY] what printers the shop uses (brands not named on screen), and whether to say "we use both".
**Accuracy note:** the trade-offs are qualitative and general. No build volumes, prices or speeds on screen unless the owner supplies them.

---

## Ep 7. "What plastic should I use for car parts?"
**Question:** which filament is right for a car part?

The structure is "the car torture test": each material faces the things a car does to a part (sun, heat, impact, flex).

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "I printed a vent in PLA!" | Pip proudly fits a sage-coloured part to the cartoon car. |
| 2 | GUS | "Park it in the sun." | The sun; the PLA part slowly droops. Pip's eyes go worried. |
| 3 | GUS | "PLA is easy to print. It just doesn't like heat." | |
| 4 | GUS | "PETG handles more heat and it's tougher." | The PETG part survives the sun; it gets a dull look over time (no claim on screen, just survives). |
| 5 | GUS | "For outside the car, ASA. It's made for sun and weather." | ASA in sun and rain: unchanged. Pip: ^ ^. [VERIFY: the owner's go-to exterior material] |
| 6 | GUS | "Nylon and carbon-fiber blends for stiff, strong brackets." | A bracket under a cartoon weight holds. |
| 7 | GUS | "Flexible stuff, like TPU, for seals and bumpers that bend." | A TPU strip squashes and springs back. |
| 8 | PIP | "And the hard ones to print?" | |
| 9 | GUS | "They warp, they need an enclosure… they're worth it." [VERIFY] | The cartoon printer gets a box over it; Gus nods. |

**Real footage:** [VERIFY] printed parts on a real car (a test fit or vent). An Epsilon Plus or shop part if the owner OKs it.
**Accuracy note:**
- The material traits are standard and qualitative: PLA has low heat resistance; PETG is tougher and more heat-tolerant; ASA is UV- and weather-resistant; ABS and ASA need an enclosure; nylon/CF is stiff and strong; TPU is flexible.
- No temperatures on screen. The owner should confirm the recommendations they stand behind.

---

## Ep 8. "STL or STEP? Mesh vs NURBS"
**Question:** what's the difference between STL and STEP files, and when do you use which?

The structure is two "languages": Gus explains with a cartoon translator gag.

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "The manufacturer wants a STEP file. I sent an STL." | Pip holds up an envelope; it comes back stamped "?". |
| 2 | GUS | "STL is a mesh. Triangles. Like the scan." | Zoom into a mesh: triangles everywhere. |
| 3 | GUS | "Great for scans and for printing." | Mesh → printer: it prints fine. Thumbs-up icon. |
| 4 | GUS | "But you can't really edit it. Every curve is a hundred flat bits." | Gus tries to move one edge and a ragged patch of triangles comes with it. |
| 5 | GUS | "STEP is NURBS. Real math curves." | The same part rebuilt as smooth, glowing surfaces with clean edges. |
| 6 | GUS | "That's what CAD and manufacturers want. You can change a hole, a thickness, a fillet." | Gus types a new hole size; it updates perfectly. |
| 7 | PIP | "So which one?" | |
| 8 | GUS | "Scan in mesh. Design in NURBS. Print from the mesh you export." | A three-step loop: scan (STL) → CAD (STEP) → print (STL) or manufacture (STEP). |
| 9 | PIP | "And turning the scan into STEP?" | |
| 10 | GUS | "That's the hard part." [VERIFY: the owner's resurfacing service, if it's offered] | Cut to real. |

**Real footage:**
- The mirror-package workflow is the real version: an STL scan, Class-A resurfacing to a STEP solid, and an STL-vs-STEP deviation map (see the mirror-package skill / Drive mirror folders).
- [VERIFY] which project the owner allows us to show.

**Pairs with:** Ep 2. Ep 2 is "a scan is a reference"; Ep 8 is the file-format follow-up.

---

## Suggested production order
1. **Ep 1 (spray):** all footage in hand.
2. **Ep 2 (print the scan):** the strongest scan-sales call to action.
3. **Ep 3 (whole bumper):** the real slicer recordings already exist; needs the owner's process confirmed.
4. **Ep 8 (STL vs STEP):** needs a real resurfacing project to show.
5. **Ep 7 (materials), Ep 5 (glue) and Ep 6 (printers):** need the owner's recommendations and some printing footage.
6. **Ep 4 (Seamforged):** blocked until the owner describes the app.

## Owner questions (one list)
1. **Ep 1:** spray type and removal.
2. **Ep 2:** which part designs we may show on a scan.
3. **Ep 3:** what you print vs make another way, and your honest "when is printing worth it".
4. **Ep 4:** what Seamforged does, its features, audience, where to get it, and price.
5. **Ep 5:** which joining methods you use and recommend.
6. **Ep 6:** your printer setup and advice.
7. **Ep 7:** your go-to materials (exterior vs interior vs brackets).
8. **Ep 8:** the project to show for STL to STEP, and whether you offer resurfacing.
9. **Footage:** do you have printing, glueing or test-fit footage, or do we need a short shoot?

## Production notes
- **Reuse:** the Part A Blender scene and rig, the ElevenLabs v4 voice pair (Kiki and Harrison, emotion tags, no speed-ups), the music approach (a generated, curious bed with a lift on the hand-off), and the full-reel build (`tools/full_build_v2.py --v3`).
- **New recurring props:** a cartoon printer (unbranded), the failed-print shelf, filament spools, and the bill and scoreboard boards.
- **Estimated cost per episode:**
  - voices: about 1 credit;
  - music: about 6 credits per variation;
  - rendering: about 2.5-3 h of cel-shaded animation per 30 s;
  - assembly: about 30 min.
