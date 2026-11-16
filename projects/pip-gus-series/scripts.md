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

## Ep 0. Intro: "Meet Pip & Gus" (owner request 2026-11-16, to be produced first)
**Purpose:** introduce the two as Illumaesthetic's official mascots, who will explain the ins and outs of 3D scanning and printing, and what Illumaesthetic does.
**Length and shape:** about 35-40 s, 9:16. Mostly cartoon. Short real-footage flashes play inside a cartoon TV or phone frame, so no text is over IRL.

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Hi! I'm Pip." | Pip pops up into frame, ^ ^ eyes. Clean shop, the cartoon sedan behind. |
| 2 | GUS | "…Gus." | Gus leans in from the side, goggles up, half-lid neutral. |
| 3 | PIP | "We're the official Illumaesthetic mascots!" | A sage banner unrolls behind them with the Illumaesthetic logo (cartoon card; logo asset). |
| 4 | GUS | "Apparently." | Pip's eyes pop; Gus shrugs with his floating hands. |
| 5 | PIP | "Illumaesthetic 3D-scans whole cars…" | Pip's phone shows a framed clip of the real IS350 scan (inside the phone, as in the explainer). |
| 6 | GUS | "…so you can design parts that actually fit." [VERIFY wording vs what the business offers: scans for sale, parts, design] | A cartoon lip snaps onto the cartoon car, "click". |
| 7 | PIP | "And we're going to show you how all of it works!" | Quick montage of upcoming episodes as cartoon flashes: powder puff cloud, triangle mesh, sliced bumper, glue tier list, sun-drooping part. |
| 8 | GUS | "Scanning. Printing. Materials. Glue." | Each word is one flash, cut on the beat. |
| 9 | PIP | "And why we spray everything white!" | Pip gets puffed white by Gus's powder puff (teases Ep 1). |
| 10 | GUS | "Ask us anything in the comments." [VERIFY CTA] | Gus points at the camera with a floating mitten. |
| 11 | PIP | "Follow so you don't miss it!" | ^ ^ eyes; the logo card. |

**End:** the logo card with **SCANS AVAILABLE AT ILLUMAESTHETIC.COM**. No teaser card, because this one introduces the series.
**Music:** the curious bed from the explainer (or a new variation), with a lift on line 7's montage.
**Voices:** Kiki and Harrison, ElevenLabs v4 dialogue, emotion tags. Pip is excited; Gus is dry but warm.
**Footage in hand:** IS350 scan renders. The episode flashes are cartoon-only, so the intro doesn't depend on future footage.

---

## Ep 1. "Why do we spray windows and black cars?": how white-light scanners work (owner request 2026-11-16; supersedes v0.1 Ep 1)
**Question:** why do you spray windows, chrome and black cars before scanning?

**The science** (general, qualitative, no numbers):
- A structured (white) light scanner projects a pattern of light onto the surface.
- One or more cameras see how the pattern bends over the shape.
- From the known angle between projector and camera, it works out each point's distance (triangulation).
- It only works if the surface scatters the light back to the camera, the way a matte surface does. The problem surfaces:
  - **Shiny or chrome:** like a mirror, it bounces the pattern away in one direction, so the camera sees nothing or a reflection.
  - **Black:** it absorbs the light, so the pattern is too dark to read.
  - **Glass:** the light goes straight through.
- A thin matte coat makes every surface scatter the same way.

[VERIFY: the owner's scanner is a structured-light type. Don't name the scanner.]

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Why do you spray the windows white?" | The cartoon sedan, windows half-dusted. |
| 2 | GUS | "The scanner shines a pattern of light on the car." | The scanner projects a sage stripe or grid pattern; it drapes over the door like a net. |
| 3 | GUS | "A camera watches how the lines bend." | A small camera icon on the scanner; a dotted line runs from projector to surface to camera, forming a triangle. |
| 4 | GUS | "From that angle, it knows how far away every point is." | The triangle flashes; points pop up on the door and build a mesh patch. Pip: ^ ^. |
| 5 | PIP | "So what's wrong with windows?" | |
| 6 | GUS | "Light goes straight through glass." | The pattern passes through the window and lands on the seat inside. A hole appears in the mesh. |
| 7 | GUS | "Chrome is a mirror. It throws the light away." | The pattern bounces off the chrome trim and hits Pip in the face. Pip squints. |
| 8 | GUS | "And black paint just eats it." | The pattern on a black bumper fades to nothing; the mesh stays empty. |
| 9 | PIP | "So you make it… not shiny." | |
| 10 | GUS | "A thin matte coat. Now everything bounces the light back." | Spray: the pattern now reads crisp everywhere; the mesh fills in, holes and all. |
| 11 | PIP | "Does it come off?" | |
| 12 | GUS | "That depends on the spray." | Hard cut on the beat; the tease leads to Ep 9. |

**Real footage:** the IS350 being sprayed (windows and grille), then a 1:1 cut to the scan, the teaser card and the logo card.
**Footage in hand:** yes (IS350 spray shots in the long-form and the R3 reel).
**Pairs with:** Ep 9 (AESUB vs alternatives). Line 12 sets it up.

---

## Ep 1-old. "Why do you spray the car?" (v0.1, superseded by the Ep 1 above; kept for reference)
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

## Ep 3. "Why can't I just print the bumper I want?" (owner 2026-11-16: make people realise that designing and printing a custom bumper still costs more than just buying one)
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

## Ep 4. "What does SeamForge do?" (brief from the SeamForge repo README, v1.46.0)
**Question:** my part is too big for my printer. Now what?

**What SeamForge is** (from `IllumaestheticJ/SeamForge` README; nothing invented):
- A standalone desktop app for Windows, macOS and Linux. It runs fully locally; nothing is uploaded.
- It cuts oversized STL and STEP models into pieces that fit your printer.
- **Auto-Slice:** one press plans the cuts, choosing the orientation that needs the fewest pieces and spacing them evenly. It has 30 built-in printer presets plus a custom size.
- **Paint the side that shows:** brush over the visible surfaces. *Optimise seams* slides the cuts away from them, and part numbers avoid them.
- **Numbers on the inside:** each piece's number is cut into a mating face, as a real engraving rather than a decal, so it's hidden once assembled and you always know what goes where.
- **Join pieces back:** click a part to see what it mates with. *Join small pieces* folds thin wafers into a neighbour.
- **Exports:** one STL per piece, each sitting on its largest cut face. Optionally it groups pieces onto build plates in number order.
- **STEP support:** it reads CAD files and sews loose faces into a closed shell first.
- **Not in the UI right now:** the Print Layout and costing. Don't promise it on screen.

[VERIFY with the owner:]
- **Availability:** public, paid or free, and where to get it. The README describes GitHub Releases builds only; there's no store or website.
- **Name:** the owner wrote "Seamforged" but the app and repo are "SeamForge". Which goes on screen?
- **Screen capture:** a clean recording of SeamForge itself. The Dropbox "Seamforged V1" clips show the manual slicer way, which makes a good "before".

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "The bumper's too big for the printer." | Pip pushes the bumper at the toaster-sized printer; it doesn't fit. |
| 2 | GUS | "So we cut it. By hand." | Gus on a laptop, with a cartoon saw cutting the bumper; pieces scatter. The clock spins. |
| 3 | GUS | "Then figure out which piece goes where." | Dozens of identical-looking grey pieces on the floor; Pip holds two and tilts his head. |
| 4 | PIP | "And the cut runs right across the front?" | The seam line runs across the visible face; Pip's eyes go flat (annoyed D-cut). |
| 5 | GUS | "…Yep." | |
| 6 | PIP | "There has to be a better way." | |
| 7 | GUS | (beat) "…We made one." | Gus pulls out the phone himself for once, reversing the gag. Hard cut on the beat. |

**Real footage** (about 6-8 s; the owner allows longer if needed):
1. "Before": the Dropbox Seamforged V1 slicer clip of a bumper hacked into many pieces across plates. It shows on a cartoon laptop screen in Part A, never with text over it.
2. SeamForge: Auto-Slice on the same bumper.
3. Painting the visible face, with the seams sliding away from it.
4. Exploded view with numbered pieces.
5. A real printed piece showing its engraved number. [VERIFY: whether this footage exists]

**End card:** the SeamForge name and where to get it [VERIFY], then the Illumaesthetic logo card.

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

## Ep 9. "AESUB vs the alternatives" (owner request 2026-11-16)
**Question:** why use a vanishing scanning spray like AESUB instead of cheaper sprays and powders?
**Naming:** the owner asked for this topic by name, so AESUB is named. Alternatives stay generic: "developer spray", "chalk spray", "dry shampoo / foot powder". No other brands are named or mocked.

**Facts** (sourced: AESUB datasheets and retailers, the Aniwaa review, Quality Magazine; see the links in the session notes):
- AESUB sprays **sublimate**: they vanish on their own, so there's no wiping.
- The time depends on the variant. Blue is under 4 h per its datasheet, and one review found parts scannable for about 1 h. Orange lasts longer, 12-24 h. Heat and airflow speed it up; a thicker coat slows it down.
- AESUB also makes a permanent white and a transparent variant.
- Non-vanishing alternatives (developer, chalk spray, DIY powders) stay until you clean them off.

[VERIFY with the owner:]
- which AESUB variant(s) they use on cars;
- whether they've used alternatives, and what happened;
- any on-screen time. Default: no numbers on screen; say "a few hours".

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "You said it comes off. How?" | Callback to Ep 1: the car is sprayed matte. |
| 2 | GUS | "This one doesn't come off. It disappears." | The cartoon AESUB-style can (generic can, sage label "VANISHING"). The coat fades away like morning frost. Pip's eyes pop. |
| 3 | PIP | "Then why does anyone use anything else?" | |
| 4 | GUS | "Price." | A vanishing can next to a big cheap can; the cheap one has a coin icon. |
| 5 | GUS | "The cheap stuff works. Developer spray, chalk, even dry shampoo." | Three generic cans; each coats the car fine and scans fine (✓ icons). |
| 6 | GUS | "But then you have to clean it." | Gus wipes, and wipes; powder in the panel gaps, badges and grille; the cloth goes grey. The clock spins (running gag). |
| 7 | PIP | "Is it done yet?" | |
| 8 | GUS | "…No. There's still some in the grille." | |
| 9 | GUS | "And a thick coat adds thickness to your scan." | A cartoon side-section: a fat chalk layer puffs the surface out. [VERIFY: keep qualitative] |
| 10 | PIP | "So vanishing spray wins?" | |
| 11 | GUS | "Mostly. It costs more…" | |
| 12 | GUS | "…and on a hot day it vanishes while you're still scanning." | The cartoon sun; the coat fades mid-scan; holes appear; Gus re-sprays one panel. |
| 13 | GUS | "So you scan fast. Or spray again." | |
| 14 | PIP | "Scan fast. Got it." | ^ ^ eyes. Hard cut on the beat. |

**Scorecard** (cartoon board, icons only):

| | Vanishing (AESUB) | Developer / chalk / DIY |
|---|---|---|
| Clean-up | none | wipe and wash, residue in gaps |
| Coat | thin | can go on thick |
| Cost | higher | lower |
| Time window | limited, shorter in heat | stays until cleaned |

**Real footage:** the IS350 spray, then the sprayed car (and ideally the same car later, clean, with no wiping). [VERIFY] whether there's footage of the coat having vanished. Then the teaser card and the logo card.
**Pairs with:** Ep 1 (how white-light scanners work), which sets up "does it come off?".

---

## Suggested production order
0. **Ep 0 (intro / mascots):** first; all cartoon plus scan renders.
1. **Ep 1 (spray):** all footage in hand.
2. **Ep 2 (print the scan):** the strongest scan-sales call to action.
3. **Ep 3 (whole bumper):** the real slicer recordings already exist; needs the owner's process confirmed.
4. **Ep 8 (STL vs STEP):** needs a real resurfacing project to show.
5. **Ep 7 (materials), Ep 5 (glue) and Ep 6 (printers):** need the owner's recommendations and some printing footage.
6. **Ep 4 (SeamForge):** brief done from the repo; needs availability, the on-screen name and a screen capture.

## Owner questions (one list)
1. **Ep 1:** spray type and removal.
2. **Ep 2:** which part designs we may show on a scan.
3. **Ep 3:** what you print vs make another way, and your honest "when is printing worth it".
4. **Ep 4:** SeamForge availability, price and where to get it; "SeamForge" vs "Seamforged" on screen; a clean screen capture.
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
