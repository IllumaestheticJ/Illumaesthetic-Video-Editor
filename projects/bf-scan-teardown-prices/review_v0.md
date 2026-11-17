# bf-scan-teardown-prices v0.1 (quick draft): self-check

File: `/home/user/media/work/out/bf-scan-teardown-prices_v0.mp4`. 1080x1920, 30 fps, 708 frames = 23.6 s, H.264 + AAC 48 kHz.
No characters: the owner's no-Del-&-Eps instruction came before delivery, so v0 and v0.1 are the same file.

## Measured on the delivered file
- **Loudness:** -14.0 LUFS integrated; true peak -3.1 dBFS (ebur128 after the mux).
- **Cut sync:** the kick attack is the 40-120 Hz peak minus 45 ms, measured on the decoded audio. Every cut is within half a
  frame (±16.7 ms):

  | Cut | Frame | Offset |
  |---|---|---|
  | T1 → T2 | 402 | -5 ms |
  | Kit lock | 517 | +2 ms |
  | T2 → Ron (1:1) | 582 | -5 ms |
  | Ron → card | 629 | +12 ms |

  The music plays from the song's start, delayed 40 ms to get there.
- **Luma:** no dark or dropped frames (min 1.0 is the faded tail). There are jumps at frames 402 and 629, which are the cuts,
  and at 278, the camera whip from the side to the rear (see below).
- **1:1 end:** a 50/50 overlay of the scan's last frame on Ron's portrait render through `Camera.006(L5)` shows no ghosting.

## Looked at
`sheet_v0/contact_v0_0517.jpg`: 20 frames covering every tag and both sides of every cut.

## Known v0 issues
- Preview quality: 32 % renders at 8 spp, upscaled, and 15 fps doubled to 30, so the image is soft and noisy.
- **The 9.0-9.6 s camera whip** from the side to the rear is fast and blurs the rear-lip beat. v1 should give the move half a beat
  more, or cut there on the 9.381 hit.
- No `pathcheck` / `clipcheck` / `edge_margins` run (the scripts aren't on this branch); flight paths were checked by eye on
  the contact sheets. In the exploded top view, both skirts, the lip, the rear lip and the wing are in frame and clear of the body.
- No GLB footprint nesting yet. The parts are Ron's add-on pieces on his own scan copy.
- Inter Display instead of the site fonts (Fjalla One / Barlow).
- The offer wording is my placeholder.

## v0.2: safe-zone pass (owner rule, knowledge/safe-zones.md)
- **Before (v0.1):** `scripts/safezone_check.py` found 12 problems. All six text overlays (the BF tag and five cards) sat at
  y 145-352, in the top UI band and the 4:5 feed crop. In the exploded top view, the rear lip (a part on sale) sat in the bottom
  caption zone.
- **Fix:**
  - The tag and the price cards move down to start at y 300, inside x 48-920 / y 285-1440 and above the car.
  - The "THE FULL EPSILON KIT" tag is dropped, because the top view fills the band.
  - The top-view camera is wider (28 mm) and shifted, so every part sits inside y 285-1440. T2 frames 0-35 were re-rendered.
  - The end card was already inside the safe area.
- **After (v0.2):** text boxes OK, 0 problems. Sheet: `sz_after_v0.2.jpg`. Loudness and cut frames are unchanged
  (-14.0 LUFS, the same 402 / 517 / 582 / 629 frames).
- **Still to do in v1 (subject, not text):**
  - The car's rear or a wheel crosses the right-rail zone in the side shot (7-8 s) and the rear-left shots, including the
    1:1 end frame. Re-frame those cameras, and Ron's render with them, at full quality.
  - The moving rear lip dips under y 1440 for about half a second at the start of the descent (about 15.0 s).

## v0.3: web address (owner rule: "all agents should use www.epsilon.plus")
- The end card's URL changes from "EPSILON.PLUS" to **"WWW.EPSILON.PLUS"**. It is the only web address in the reel.
- `safezone_check`: text boxes OK. Loudness and cut frames are unchanged (-14.0 LUFS, TP -3.1 dBFS).
