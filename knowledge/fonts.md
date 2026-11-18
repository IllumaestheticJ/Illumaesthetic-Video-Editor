# Fonts (owner rule, 2026-11-17)

The owner's words: "use our akira font when it looks nice, if the text is right next to our logo, it should be a different font that matches the style/aesthetic". This applies to every Epsilon+ reel, from now on.

## The rule
- **Akira (Akira Expanded)** is the house display font. Use it for headlines, offers and prices (BLACK FRIDAY, 30% OFF, $385) wherever it looks good: short, uppercase, large text.
  Don't force it where it doesn't read: long lines, small labels, or dense was/now tables. Use the companion font there.
- **Next to the logo, use a different font.** The Epsilon+ wordmark is itself drawn in a heavy extended face very like Akira. Akira text beside it competes with and duplicates the logo. So the URL, tagline or any line on the logo card uses the companion font.
- **Companion font: Unbounded** (SIL OFL, in the repo at `assets/fonts/unbounded/`, weights 300-900). Its rounded, wide letters match the wordmark's round S, O and C.
  - **300-400** is for the URL and lines under the logo.
  - **500** is for part labels and small UI text.
  - Comparison sheet: `knowledge/font-pairing-test.jpg`. Michroma was rejected because its "%" reads as "°/o". Syncopate and Krona One also work but are second choice.
- Keep the same safe zones as always (`knowledge/safe-zones.md`).

## Where the Akira file is
- **Drive:** `EPSILON+ Logos/AkiraExpanded-SuperBold.otf`, file ID **1nrF80enolDd9HAu5807kv5XIx0cUSDya** (uploaded 2026-11-18). SHA-256: `5b152fce677108fbd40a42447fa6ee531164348d1510c0805bc27180f44a5775`.
- **Licence:** the owner confirmed on 2026-11-18 that Epsilon+ holds a **commercial licence** for Akira Expanded. The file itself is the "Demo" build (its internal name is "Akira Expanded Demo"); the commercial licence covers its use in ads.
- **Install** it at `assets/fonts/akira/AkiraExpanded-SuperBold.otf`. That folder is **gitignored: never commit the font** (licence). Download it with the Drive tool (download_file_content) and check the SHA-256.
- **One weight only (Super Bold).** Its glyphs are A-Z, a-z, 0-9 and `$ % & + - . , : ! ? @ # ( ) /`.
  - **There is no arrow (→) or any other non-ASCII glyph.** For was/now prices, strike through the old price or use two lines. Check every string renders, with no tofu boxes.
- **Use:** headlines, offers, big prices and the countdown number. **Not** next to the logo: that text stays Unbounded 300-400. Small labels stay Unbounded 500.
