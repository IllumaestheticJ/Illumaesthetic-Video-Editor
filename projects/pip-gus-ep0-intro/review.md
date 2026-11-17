# Ep 0 "Meet Pip & Gus" — self-review (v1, v2)

Output: `pip_gus_ep0_v1.mp4` — 1080×1920, 30 fps, 1252 frames (41.73 s), h264 yuv420p + AAC 48 kHz, faststart.
Master −14.1 LUFS / −2.0 dBTP (dialogue −14.1, music −21.3).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Gus waves with happy arc eyes on "Hi, I'm Gus" at 0.3 s; Pip pops in at ~2 s. Nothing transforms in the first 1.5 s. A wave is motion, not a reveal. |
| 2 | Beat sync | 4 | 10 of 14 cuts land +0.4 frames from a 100 BPM beat. H1–H4 cut on Gus's spoken words "Scanning. Printing. Materials. Glue." (logged choice), so they sit 3–5 frames off the grid. |
| 3 | 1:1 match | 4 | Three IRL→scan hard cuts inside Pip's phone (Lola, C5, MR2). The cuts were taken from the existing reels, so they keep those reels' matches. The key is clean (no magenta), with a per-frame corner pin. They are small on screen, so the match reads as an "inside the phone" moment. |
| 4 | Scan quality | 4 | Scan halves come from the existing reels: silver-on-black, no debris visible at phone size. |
| 5 | Story | 4 | Who they are → what Illumaesthetic does (scan → sell scans → design → print) → what the series covers → question to the viewer. The design step is shown as a lip part, not a CAD screen. |
| 6 | Grade | 4 | Only phone-sized IRL inserts, which are consistent. The cartoon stays in the house greys and sage. |
| 7 | Text | 4 | Word-pop captions of the spoken script only. No numbers were invented: the only figure on screen is the C5 reel's own triangle count, which sits on the scan. `picture.json`: text_over_footage_alpha_max = 0.0. Captions sit under faces in every shot. |
| 8 | Ending | 5 | Logo card at 37.83 s (a beat) with WHAT QUESTIONS / DO YOU HAVE? at 76 px in ink white (enlarged from 44 px grey in review). The music's final chord is at 40.83 s and rings out with a −3 dB duck. |
| 9 | Technical | 5 | All 1135 cartoon frames present, no black or duplicate frames at cuts (checked frame pairs at all 14 cuts). |

## Fixed during review
- A/B: raised hands rendered off-frame. Fixed with forward-up arm raises; Gus waves with his inner hand.
- G: a falling "?" cast a shadow across Gus's face (frames 690–693). Question marks no longer cast shadows.
- J: Gus looked weary on "…There's a lot to cover". The cause was not the blink: it was the 0.2×accent stress squint on "There's". Both are now suppressed for Gus on line 10 (owner rule: Gus is never sad).
- Logo card CTA was too small for the closing question. Added optional `ctaSize`/`ctaInk` to ReelGfx `logo`.
- Build bug: `picture()` reused `video.mp4` on a frame-count match, so a new overlay was silently ignored. It is now keyed on the overlay file, the newest frame mtime and the phone insert (`video.key`).

## For the next agent
- Check expressions frame by frame on every line where Gus pauses. Lid values from accent and blink can read as sad even when no expression is set.
- The gfx cache hash now covers `ExplainerGfx.tsx`, `ReelGfx.tsx` and the props. If you edit another component, check the overlay actually re-rendered.

## v2 (2026-11-17)
- Owner approved series v0.4's voice-only tag. Pip says "Can I just print the bumper I want?" over the logo card at 38.42 s, leading into Ep 1 (the bumper episode). The owner's "What questions do you have?" line and the logo text are kept.
- The tag fits before the final chord, so the length is unchanged (41.73 s). Whisper hears it word for word in the final mix. It was level-matched to line 11 (both -14.5 LUFS); master -14.0 LUFS / -2.0 dBTP.
- Criterion 8 (Ending) stays 5: the logo card is still on the beat, and the chord rings after the tag.
