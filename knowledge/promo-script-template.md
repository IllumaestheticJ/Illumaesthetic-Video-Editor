# Scan-data promo script template ("build it from scan data")

Status: DRAFT, waiting for owner approval (2026-11-14). Once approved, every scan-data promo uses this
structure. Reference: `3_square_meter_home_design` (54 s, 1080x1920, 60 fps). A narrated build-up:
an empty room gets filled one object at a time, and every object arrives on its own spoken line. Each
line is also shown as a caption.

## What we copy from the reference
- **Format:** 9:16, about 45-55 s, one continuous camera that drifts slowly. No hard scene changes
  except the 1:1 IRL->scan cut.
- **Mechanic:** start empty, then add **one element per line**. Parts drop or fly in, settle with a small
  bounce, and the camera keeps moving.
- **Arc:** hook ("let's build...") -> the problem -> one piece at a time -> the payoff -> CTA.
- **Captions = narration, word for word.** One short line (3-9 words) per caption, all lower case, no full stop.
  Each caption stays up for about 1.5-2.5 s.
- **Caption style:** a white rounded pill with small black text, centred, near the bottom
  (~80 % down the frame, clear of the TikTok caption zone). This replaces the Inter/off-white HUD
  label on these promos only. Owner to confirm.
- **Voice:** a calm, matter-of-fact preset voice at a fast pace, with music under it (duck the music about 9 dB).

## House rules that still apply (knowledge/lessons.md)
- No captions over IRL footage. An optional IRL hook shot gets the voice only, and its caption
  comes in after the 1:1 cut.
- No made-up numbers. Every figure has to come from the files: measurements from the scan, version
  numbers from the folder names. Never show triangle counts.
- Label every teardown or build step with its title only. Don't number the steps ("MOD 01").
- Only claim what the scan shows. Render each scan before writing a line about it.
- Scan look: satin silver on pure black. End on the logo card at a large size (about 700 px of 1080).

## Slots
| Block | Time | Line pattern | Slot source |
|---|---|---|---|
| HOOK | 0-4 s | "let's build a [CAR]" / "using nothing but scan data" | car name |
| PROBLEM | 4-9 s | "but to make parts that actually fit" / "you need the real car, in 3D" | fixed |
| SCAN BUILD | 9-30 s | one line per scan file: "first, the whole car" / "[PART], scanned on its own" | engineering Drive scan list |
| DETAIL | inside SCAN BUILD | "every [panel gap / badge / bolt]" | only details a render shows |
| DESIGN PAYOFF | 30-46 s | "then we design on top of it" + one line per designed part | build folder (STL/CAD) |
| CTA | 46-54 s | "this is the [CAR] scan data" / "[CTA]" -> logo | owner |
