# Illumaesthetic house style — scan videos

Derived from the approved references in `training/references/` (numbers measured with
`python -m ive analyze`). Update this file when a reviewer promotes feedback to a rule.

## Formats
| Deliverable | Size | fps | Length |
|---|---|---|---|
| Reel / Short / TikTok (default) | 1080×1920 (9:16) | 30 | 15–30 s |
| Long-form chapter | 3840×2160 or 1920×1080 | 24/30 | — |

iPhone footage from the shop arrives as **HEVC HLG (arib-std-b67), rotated −90°**. Always tonemap to
SDR Rec.709 (`ive assemble` does this automatically; `ive frame` does it for stills). Never mix
an un-tonemapped HLG clip with SDR renders — it looks washed out next to the scan.

## Pacing (measured)
| Reference | Shots | Avg shot | Notes |
|---|---|---|---|
| 240SX IRL reel (Oct 31, approved) | 6 in 22.8 s | 3.8 s | cuts on the beat, logo card at the last downbeat |
| Corolla reel (Good Reels) | 3 in 7.8 s | 2.6 s | every cut is a 1:1 perspective cut |
| Civic reel (Good Reels) | 14 in 13.6 s | 1.0 s (median 0.6) | 4.5 s CG hook, then rapid-fire IRL details |
| Temerario scan reel | 1 continuous | — | one long scan move, no cuts, ~40 s |

Rules of thumb:
- **Cut on the beat.** Run `ive beats <music>`; a shot is usually 4 beats (≈2.5 s at ~96 BPM).
  Detail montages can drop to 1 beat per shot.
- **Hook in the first 2 s**: open on the transformation. 240SX v1 waited 8 s for the 1:1 cut and
  the reviewer asked for it up front (v2 cuts at 1.82 s). Default: ~2 beats of IRL, then the cut.
- **End on the ILLUMAESTHETIC logo card** on the final downbeat (reuse the card from an approved edit).

## The 1:1 perspective cut (signature transition)
In every approved reel the transformation shot is a **hard cut** where the car keeps exactly the
same size, position and perspective while everything else changes (CG → real, stock → modified,
IRL → scan). No dissolve, no wipe, on a beat. See `knowledge/match-cut.md` for the procedure.
Optional variants (use sparingly, max once per video): `flash` (2-frame bloom on the cut) and
`scanline` (cyan wipe, for "scanning" moments).

## Scan look (Temerario reference)
- **Satin metallic silver** on **pure black** (`--look silver`, background ≈ 0.004). Not white clay.
- Lighting is soft studio from above + rim; the background never shows lights or a floor.
- Scan micro-detail must read: use ≤4 mm decimation for full-car shots, ≤2 mm for close-ups.
- Moves are slow and continuous: orbit 15–35° or push-in 10–15% over a shot, ease-in-out.
- Let the matched scan shot *keep going* into the next beat of the story (e.g. the part you were
  looking at comes off) instead of cutting away — reviewer request on 240SX.
- Exploded views (parts sliding off along one axis) are the money shot for "what we scan / what we make".
- No ground: scanned asphalt, paint lines and wheel stops must be cleaned (`ive crop` + `--drop-islands`).

## Text / HUD (Remotion `ScanHUD`)
- Only on scan shots, never over IRL footage.
- Max two items on screen. Enter on a beat, leave before the cut.
- Only **true numbers from the data** (triangle counts from the STL header, lengths measured
  from the scan). Never invent scanner specs, tolerances or accuracy figures.
- Typeface: Inter Display (titles, tracking +6) / JetBrains Mono (data), off-white `#e8ecf2`.
- Keep text out of the car silhouette and 80 px inside the frame edges.

## Grade
- IRL night footage: hable tonemap from HLG, no extra saturation. Keep the sodium-light warmth.
- Scan renders: AgX view transform, no colour; let the IRL footage carry colour.
