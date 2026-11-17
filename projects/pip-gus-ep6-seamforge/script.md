# Pip & Gus Ep 6: "What does SeamForged do?" (script v5, for owner approval; was Ep 4)

9:16, 1080x1920, 30 fps, about 38 s. Branch `claude/pip-gus-ep4-seamforge` keeps its old number. Status: **owner answered the open questions (2026-11-16); waiting on script approval**. No voices or renders until this script is approved.

Every app claim comes from the `IllumaestheticJ/SeamForge` README (v1.46.0, commit a807c0a). Print Layout and costing are
hidden in the UI right now, so neither is mentioned or shown. [VERIFY] marks what only the owner can answer.

**Question:** my part is too big for my printer. Now what?

**Series position (series order v0.4, owner 2026-11-17: the steps of making a bumper, in order):** step **cutting**, between
Ep 5 (STL vs STEP, files) and Ep 7 (big vs small printer). Ep 5 ends with Gus: "It's bigger than the printer." This episode opens
on that bumper file, too big for the bed, and ends with Pip over the logo card asking Ep 7's question: "It's cut! Which printer
do we use?" Still works on its own: line 1 restates the problem.

## Part A: cartoon (about 22 s, word-by-word captions)

Owner 2026-11-17: drop the seam-across-the-front beat (a seam shows there regardless). Say instead that by hand it takes forever
to cut, number and place every piece on the print bed. "Forever" is carried by the clock gag, with no time figure.

| # | Who | Line | Eyes | Picture |
|---|---|---|---|---|
| 1 | PIP | "It's bigger than the printer..." | worried | Callback to Ep 5: on Gus's laptop the bumper file hangs far outside the printer's build-volume box. The small unbranded printer beside it. |
| 2 | GUS | "So we cut it up. By hand." | flat, neutral | Gus's laptop plays the real slicer clip (cropped to the 3D view): pieces hacked off one by one. The wall clock starts to turn. |
| 3 | GUS | "Number every piece..." | flat | Gus writes a number on each grey piece with a marker; the pile keeps growing. |
| 4 | GUS | "...then lay each one flat on the print bed." | slightly weary | Gus places pieces one at a time onto a row of cartoon build plates that runs off-screen. |
| 5 | PIP | "Is it done yet?" | impatient | Pip slumped on a stool (series running gag); Gus keeps placing pieces in the background. |
| 6 | GUS | "...No." | flat, eyes on his work | Gus doesn't look up: he is still placing pieces on the build plates (owner: make it clear he is still setting up the beds). Clock spins like a fan behind him. |
| 7 | PIP | "There has to be a better way." | impatient | Pip to camera. |
| 8 | GUS | "...We made one." | half-lid, a little proud | Gus pulls out the phone this time; the screen shows the SeamForged app. |
| 9 | PIP | "Show me!" | ^ ^ excited | Push into the phone; hard cut on the beat to Part B. |

Changes in v5: removed "Then figure out which piece goes where" and "And the seam runs right across the front?" / "Yep.";
added the cut / number / place-on-the-bed beats and the "Is it done yet?" / "...No." gag. Voices regenerated: take v2, Higgsfield job 37e7501f.

## Part B: the app (about 7 s, no text over it, no VO, music only)

Part B now answers Part A beat for beat: cut, number, place on the bed. Painting the visible side is dropped (owner: seams show regardless).

| # | ~s | Shot | Source |
|---|---|---|---|
| B1 | 1.8 | **Auto-Slice** on the GR86 rear bumper: one press, the cut planes appear and it splits into coloured pieces. (cut) | Agent records SeamForged |
| B2 | 1.8 | **Exploded** slider: pieces pull apart, part numbers engraved on the mating faces. (number) | same |
| B3 | 1.8 | **Build plates, Plan plates**: every piece stands on a cut face and lands on the beds. (place on the bed) | same |
| B4 | 1.6 | The real printed GR86 piece turned in hand, showing its engraved number. | Owner's footage (recording) |

Capture notes:
- Model: `Bomex GR86 - Rear Bumper Uncut.stl` (engineering Drive, 282 MB), the same bumper the printed piece comes from. The file name
  and the app's top bar (which reads "SeamForge") are cropped out; no maker or brand on screen.
- The printer dropdown shows brand presets; use a custom size or crop the left panel.
- "Before" (owner OK): Dropbox `Seamforged V1/2026-08-23 13-30-22.mp4`, cropped to the 3D viewport, on Gus's laptop in line 2.

## End cards (about 3-6 s)

Owner rule (2026-11-16): videos do not need to link to a YouTube video; the "FULL VIDEO ON OUR CHANNEL" teaser card is
optional and only used when a matching full video exists. There is no full SeamForge video, so no teaser card by default.

1. **App card** (about 3 s): dark plate, sage bar, the exploded numbered pieces from B3 in a framed window,
   **SEAMFORGED** / **COMING SOON** (owner: work in progress, will release soon; no price or link).
2. **Logo card** (owner, 2026-11-16: no CTA required; this episode is not about a scan we sell). No text. Over it, Pip's
   voice only: **"It's cut! Which printer do we use?"** (lead-in to Ep 7, big vs small printer; series rule: no new text for it).

## Music, voices
- Curious generated bed (series approach), lift on line 8's hand-off.
- Kiki (Pip) and Harrison (Gus), ElevenLabs v4 dialogue, one call including the logo-card line, emotion tags, no speed-up. The take goes to the owner before animation.

## Owner answers (2026-11-16)
1. On-screen name: **SeamForged**. (The app's top bar still reads "SeamForge"; it is cropped out of the capture so only one name is on screen.)
2. Work in progress, will release soon: app card says **COMING SOON**, no price or link.
3. The agent records the screen capture itself.
4. Footage of a printed piece with its engraved number exists; ask the owner for exactly what is needed.
5. The Seamforged V1 slicer clip is OK on Gus's laptop.

## Owner notes (2026-11-17)
- Series reordered (v0.4): this is Ep 6, the cutting step. Opens on Ep 5's "It's bigger than the printer."; ends with Pip:
  "It's cut! Which printer do we use?" (supersedes the v0.3 links).

## Still open
- Owner approval of voice take v2.
- Plates: the README's Build plates tab (Plan plates / Export plates) is in the UI, so Ep 7 can open on SeamForged's plates.
- The model to record: ideally the same bumper as in the slicer clip, so before and after match.
