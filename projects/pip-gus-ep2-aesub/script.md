# Pip & Gus Ep 2: "AESUB vs the alternatives": script v3 (2026-11-17, awaiting owner approval)

**Series position (v0.3 order):** this is Ep 2 (it was Ep 9). It follows Ep 1, the spray episode, and leads into Ep 3, "Can't you just 3D print the scan?". The folder was renamed from `pip-gus-ep9-aesub`; the branch name stays `claude/pip-gus-ep9-aesub`.

**Question:** Why use a vanishing scanning spray like AESUB instead of dry shampoo or foot powder?

**Status:**
- v2 included the owner's answers to the v1 questions (see `feedback.jsonl`).
- v3 changes only the first and last lines, for the series transitions.
- No voices, music or renders until the owner approves v3.

## Running time (target)

| Part | Length |
|---|---|
| Cartoon | about 28-30 s |
| Real footage | about 5 s |
| Logo card | 3 s |
| **Total** | **about 37 s** |

## Owner facts this script rests on
- **Variants:** the owner uses AESUB Violet in the spray gun and AESUB Orange in spray cans. The cartoon uses an Orange spray can.
- **Pronunciation:** "AESUB" is said "AY-EEE-Sub". The TTS text gets a respelling; the captions keep "AESUB".
- **Alternatives:**
  - The owner's alternatives are dry shampoo and talc foot powder.
  - They work, but have to be wiped off, and the owner calls them "crummy".
  - No product brand is named; "foot powder" is said instead of the brand the owner mentioned.
- **Thickness:** usually not relevant on car scans, so the line is dropped.
- **Heat:**
  - The coat does vanish mid-scan on hot days.
  - That includes Violet, and is worse with Orange and Blue.
  - No times are given.
- **Main selling point:** vanishing spray is most useful when you don't want to wipe down an expensive car.
- **Cost:** "Price" is said only as a relative reason, with no amounts.

## Dialogue

| # | Who | Line (captions) | Picture |
|---|---|---|---|
| 1 | PIP | "Does that spray stay on forever?" | Opens on the sprayed car from Ep 1 (same prop and state). Pip repeats Ep 1's last question and looks up at Gus. |
| 2 | GUS | "Not this one. AESUB just disappears." | Gus holds an orange spray can with a plain "AESUB" text label (no logo copy). The coat fades off the hood like morning frost, in X-shaped patches like the real footage. Pip's eyes pop (O O). |
| 3 | PIP | "Then why use anything else?" | |
| 4 | GUS | "Price. Dry shampoo or foot powder works too..." | Two plain, unbranded bottles: DRY SHAMPOO and FOOT POWDER, each with a coin icon. Each coats a door, and the scan comes out fine (sage ✓). |
| 5 | GUS | "...but then you have to wipe it all off." | Gus wipes, and wipes. Powder sits in the panel gaps, badges and grille, and the cloth goes grey and crummy. The wall clock spins (running gag). |
| 6 | PIP | "Is it done yet?" | Pip bounces, impatient. |
| 7 | GUS | "...No. Still some in the grille." | A small weary sigh. Close-up of the grille, still dusty. |
| 8 | PIP | "So vanishing spray wins?" | |
| 9 | GUS | "On an expensive car you don't want to touch? Every time." | A gleaming cartoon exotic, with sparkles, rolls in. Gus's cloth hovers near it, and he puts it away. |
| 10 | GUS | "But on a hot day, it can vanish mid-scan." | A cartoon sun. The coat fades while Gus scans, holes open in the mesh, and Gus re-sprays one panel. |
| 11 | GUS | "So you scan fast." | Deadpan look to camera. |
| 12 | PIP | "Scan fast. Like this?" | ^ ^ eyes. Pip holds up the phone (the hand-off gag). Hard cut on the beat to the real footage. |
| 13 | PIP (voice only, over the logo card) | "OK, it's scanned. Can we print it now?" | The logo card, with no new text and no caption. It leads into Ep 3. |

### Voice direction (ElevenLabs v4 dialogue, one call, no speed-up)
- **Pip (Kiki, voice_id 2d51d9d0-b2a4-5e8b-9c63-f310adafd5f7):**
  - curious on line 1;
  - impatient on line 6;
  - excited on line 12;
  - eager on line 13 (recorded in the same dialogue call).
- **Gus (Harrison, voice_id 573e5163-59b3-4926-aab1-951ef2985f81):**
  - matter-of-fact;
  - a small weary sigh before "...No.";
  - dry on line 10;
  - never angry or sad.
- **TTS text for line 2:** "AY-ee-sub" (or the closest spelling that reads as AY-EEE-Sub). Check the take by ear.

### Pros and cons board (lines 8-10, cartoon, icons only, no numbers)

| | Vanishing (AESUB) | Dry shampoo / foot powder |
|---|---|---|
| Clean-up | none, it's gone on its own | wipe it all off, and it ends up in the gaps |
| Cost | higher | lower |
| On a hot day | can vanish mid-scan | stays |

### Captions
- Word by word, cartoon part only.
- Fjalla One on a dark plate.
- Pip in sage #619f73; Gus in #ecefec.

## Real footage (about 5 s, no text)
All shots are IS350 speedrun footage already in Dropbox. The owner confirmed there are spraying shots there.

| Shot | Source | Length | Content |
|---|---|---|---|
| R1 | FX30541, about 96.8 s | about 1.5 s | The spray gun hits the front bumper and grille. |
| R2 | FX30554, 9.05-11.05 s | about 2.0 s | The walk-out to the powdered car, then a hard 1:1 cut on the beat to the scan. This reuses the long-form's matched front pair (solved frame 264). |
| R3 | FX30553, 39.5-42.5 s | about 1.5 s | Close-up of the hood, with the powder already clearing in X-shaped marks. |

**Order:** spray, then scan, then it vanishes.

## End cards
Real footage, then the Illumaesthetic logo card. There is no teaser card and no call to action (owner, 2026-11-16).

Pip's line 13 plays over the logo card as voice only. The logo card stays about 3 s, long enough for the line to finish.

## Music
- A new curious, inquisitive generated bed (ElevenLabs Music v2.5 via Higgsfield), with a lift on line 12.
- It must not be game or battle music.
- It must not reuse another episode's track.
