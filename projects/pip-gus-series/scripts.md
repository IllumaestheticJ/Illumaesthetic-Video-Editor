# Pip & Gus: explainer series, draft scripts (v0.1, 2026-11-16)

These are drafts for owner review; nothing is produced yet. Each episode is one common question about car 3D scanning or 3D printing.

## Series format
- The template is the IS350 explainer ("The usual way"): about 40 s at 9:16, made of three parts.
  1. **Cartoon (about 25-32 s).** Pip asks the question. Gus shows the hard or wrong way, dry and only slightly annoyed. A running gag escalates, and Pip finds the "better way".
  2. **Real footage (about 4-6 s, longer only if it earns it).** Illumaesthetic doing it, ending on a hard 1:1 cut from the real car to the scan where one fits.
  3. **End cards.** The teaser card ("FULL VIDEO ON OUR CHANNEL" with a clip in a frame), then the logo card.
- **Characters** (locked spec in `projects/scan-tedium-explainer-reel/characters/design.md`):
  - **Pip** (kid, voice Kiki): curious and impatient; always asks the question; gets excited at the end.
  - **Gus** (dad, voice Harrison): knows the job, matter-of-fact, mildly annoyed that it's tedious, never angry.
  - Shared look: dot eyes, no eyebrows (expressions are eye shapes only), no arms, cel-shaded shop.
- **Running gags that carry across episodes:**
  - the pile of peeled dots in the corner;
  - the wall clock that spins;
  - Gus's goggles;
  - Pip's line "I saw an Illumaesthetic video…" before the cut to real footage. Vary it per episode so it doesn't get stale.

**Rules** (from `knowledge/lessons.md` and the IS350 reels):
- No invented numbers. Every number on screen must be sourced, and lines marked [VERIFY] need the owner's confirmation before production.
- No competitor or scanner brand is named or mocked.
- No text over real footage; captions go on the cartoon half only.
- The real-to-scan transition is always a hard 1:1 cut on a beat, never a dissolve.
- No time reveals unless the owner OKs it.

---

## Ep 1. "Why do you spray the car?"
**Question people ask:** what's the white powder, and is it bad for the paint?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Why is the car… white?" | The cartoon sedan, half-dusted, looks like a powdered donut. Pip pokes it and it leaves a fingerprint. |
| 2 | GUS | "Shiny paint confuses the scanner." | Close: the scanner cone hits the glossy door, and the light bounces off in cartoon zig-zags. "?" icons pop out of the scanner. |
| 3 | GUS | "Black paint, chrome, glass… it can't see any of it." | Quick inserts: a black bumper with no scan, chrome trim reflecting Gus's face, a window the cone passes straight through. |
| 4 | PIP | "So you paint it?" | |
| 5 | GUS | "Dust it. It wipes right off." [VERIFY: the owner's spray type and how it's removed] | Gus "dusts" with a comically huge powder puff; a cloud covers the whole shop. |
| 6 | PIP | (coughing) "…There has to be a less messy way." | Only Pip's dot eyes show in the white cloud; they blink. |
| 7 | PIP | "Wait. Illumaesthetic does it in like one coat." [VERIFY wording; no time number] | Pip pulls out his phone and it fills the frame. |

**Real footage:** the IS350 front being sprayed (`lexus-is350-speedrun-long` E14 / R3 spray shots), a hard 1:1 cut to the scan, the teaser and the logo.
**Footage in hand:** yes (IS350).
**Open questions for the owner:**
- What spray do you use, and how does it come off?
- Do you ever scan without spray?

---

## Ep 2. "Can't you just 3D print the scan?"
**Question people ask:** I bought the scan, so why can't I just print a part from it?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "We have the scan! Let's print a lip!" | Pip, excited, drags the car scan onto a cartoon 3D printer. |
| 2 | GUS | "That's a scan. It's a skin." | Zoom into the scan and it turns into a sea of tiny triangles. Pip's eyes go wide. |
| 3 | GUS | "Millions of tiny triangles. No thickness. No edges." | Gus flicks the surface and it wobbles like cling film. |
| 4 | PIP | "So… print it anyway?" | |
| 5 | GUS | "Sure." | The printer prints a paper-thin, wobbly ghost of the car's nose. It flops over. |
| 6 | GUS | "The scan is the reference. You design the part on it." | Gus draws a clean, solid lip that hugs the scan; it snaps on with a "click". |
| 7 | PIP | "So you need the scan to make it fit?" | |
| 8 | GUS | "Every curve." | |
| 9 | PIP | "Then where do I get one?" | Pip's eyes do ^ ^. Cut. |

**Real footage:** a real car to its scan (1:1 cut), then a designed part sitting on the scan (Epsilon Plus or mirror-project CAD on the scan), then the logo with **SCANS AVAILABLE AT ILLUMAESTHETIC.COM**.
**Footage in hand:**
- Scans: yes.
- Part-on-scan renders: the mirror package has an STL-vs-STEP deviation map; to confirm.
- [VERIFY] which part designs the owner allows us to show.
**Note:** this is the best "why buy a scan" episode, so it pairs naturally with the logo card's call to action.

---

## Ep 3. "Why not print the whole bumper?"
**Question people ask:** if you can print parts, why not print a whole body kit?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Print the whole bumper!" | Pip points at the tiny cartoon desktop printer, then at the huge bumper. |
| 2 | GUS | "On that?" | The printer is about the size of a toaster. |
| 3 | GUS | "We'd have to cut it into pieces." | The bumper is sliced like bread; the pieces print one by one while the clock spins (running gag). |
| 4 | GUS | "Then glue it. Then sand it. Then hope it doesn't melt in the sun." [VERIFY: the owner's view on printed exterior parts and heat] | A cartoon sun beats down; the glued bumper droops like a clock in a Dalí painting. |
| 5 | PIP | "Is it done yet?" | Callback to Ep 0. |
| 6 | GUS | "…No." | |
| 7 | PIP | "How does Illumaesthetic do it?" | |

**Real footage:** the owner's real process. [VERIFY] Are printed parts prototypes and test fits, with production parts made another way? Show only what is true.
**Footage in hand:** unknown. Look in the Dropbox scan-process folders for test-fit or print footage.
**Risk:** this one makes the most claims about production methods. Write the final lines only after the owner explains the process.

---

## Ep 4. "How do you scan under the car?"
**Question people ask:** how do you get the wheel wells, sills and underside?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "You scanned the outside. What about under there?" | Pip peeks under the cartoon car; it's dark, with a single dot eye blinking back (a spider? keep it cute). |
| 2 | GUS | "Jack it up." | Gus jacks the car; it rises one click at a time, slowly (clock gag). |
| 3 | GUS | "Then lie on the floor." | Gus lies flat, scanner pointing up, goggles down. |
| 4 | GUS | "For a while." | Time-lapse: Gus in different floor poses, like a chalk outline, upside down, asleep. |
| 5 | PIP | "Is that the best position?" | |
| 6 | GUS | "…It's *a* position." | A deliberate nod to the real host's line "It's a crazy position" in the long-form. [VERIFY the owner is OK with the callback] |
| 7 | PIP | "I saw a video where they did the whole thing!" | |

**Real footage:**
- `lexus-is350-speedrun-long` E50 (lying on the floor scanning under the front) and E56 (under the car, sill and underside).
- The SC_INS_WHEEL / SC_INS_SILL scan inserts.
- A 1:1 cut on the wheel arch if a solved pair exists.

**Footage in hand:** yes (IS350 long-form). This is the easiest to produce next, because the teaser clip already comes from here.

---

## Ep 5. "Is a scan really that accurate?"
**Question people ask:** is a scan really better than measuring the car?

| # | Who | Line | Picture |
|---|---|---|---|
| 1 | PIP | "Why not just measure the car?" | Pip holds a tape measure taller than he is. |
| 2 | GUS | "Go ahead." | Pip tries to measure a curved fender; the tape won't bend, then springs back and wraps around him. |
| 3 | GUS | "Cars aren't boxes. Nothing's straight." | Gus traces a curve in the air; the curve keeps changing direction. |
| 4 | PIP | "Calipers?" | Pip, tangled, holds out calipers. |
| 5 | GUS | "For one point. You need all of them." | The car fills with thousands of points, which become a solid scan. |
| 6 | PIP | "All of them?!" | Pip's eyes pop to 1.3×. |
| 7 | GUS | "That's the scan." | |

**Real footage:** a real car to its scan (1:1 cut). If the owner has sourced data, add a deviation or check overlay.
- The IS350 footprint check is in `lessons.md`: the scan measured 4,527 mm against a spec-sheet 4,520 mm. It's a real, sourced comparison and could be the on-screen proof. [VERIFY with the owner before using any number on screen.]

**Footage in hand:** scans yes; a deviation overlay would need building.

---

## Suggested order
1. **Ep 4 (under the car):** all footage in hand, and it continues from the teaser.
2. **Ep 2 (scan vs printing):** the strongest call to action for selling scans.
3. **Ep 1 (spray).**
4. **Ep 5 (accuracy):** needs an owner-approved number or none.
5. **Ep 3 (whole bumper):** needs the owner to explain the production process first.

## Production notes
- **Reuse:** the Part A Blender scene and rig (`projects/scan-tedium-explainer-reel/tools/partA_scene.py`, `partA_anim.py`), the voice pair (ElevenLabs v4: Kiki for Pip, Harrison for Gus, emotion tags, no speed-ups), and the full-reel build (`tools/full_build_v2.py --v3`).
- **New props per episode:**
  - Ep 1: powder puff and cloud;
  - Ep 2: triangle-mesh zoom and printer;
  - Ep 3: printer, sliced bumper and melting sun;
  - Ep 4: jack and floor poses;
  - Ep 5: tape measure and calipers.
- **Estimated cost per episode:**
  - one voice generation (about 1 credit);
  - one music bed (about 6 credits per variation, or reuse);
  - about 2.5-3 h of cel-shaded rendering per 30 s;
  - assembly about 30 min.
