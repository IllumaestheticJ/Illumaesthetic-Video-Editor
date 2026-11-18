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

## v0.4: whole-dollar prices + % off (user: "take out the cents for prices, show what that equates to in % off")
- The cards now read FRONT LIP $285 → **$200**, SIDE SKIRTS $400 → **$280**, REAR LIP $285 → **$200** and SPORT WING $450 → **$315**.
  Each card has a sage **30% OFF** badge.
- **$199.50 is rounded up to $200**, so the video never shows less than checkout. The rounding makes $285 → $200 work out
  to 29.8 %, but the badge shows the sheet's 30 % tier, which is the real discount at checkout ($199.50). Owner option: set
  the store sale price to $199 or $200 so card and checkout match exactly.
- `safezone_check`: text boxes OK. Audio and cut frames are unchanged.

## v0.5: pacing (user: "the scene right before Ron's render takes a bit too long. in general have clips match the beat")
- The hold after the kit locks drops from a full bar (2.15 s) to **one beat (0.54 s)**.
- Every clip now starts and ends on a measured hit of the song's grid, and each is a whole number of beats:

  | Clip | Beats | Time |
  |---|---|---|
  | T1 teardown | b0-24 (24 beats) | 0-12.93 s |
  | T2 top view and fly-home | b24-33 (9 beats; lock on the kick entry, b32) | 12.93-17.77 s |
  | Ron's render | b33-37 (4 beats, one bar) | 17.77-19.90 s |
  | End card | b37-42 (5 beats) | 19.90-22.60 s |

- **Measured on the decoded output:**

  | Cut | Frame | Offset |
  |---|---|---|
  | T1 → T2 | 388 | +2 ms |
  | Kit lock | 517 | +2 ms |
  | T2 → Ron | 533 | -3 ms |
  | Ron → card | 597 | +7 ms |

  -14.0 LUFS, TP -2.8 dBFS. `safezone_check` OK.
- The T2 opening drift is stretched slightly (13.435-14.466 played over 12.93-14.466), so T2 can start on b24. The wing card now ends at 12.80 s.

## v0.6 (wheels and tyres in scan silver)

- User: "have the wheels and tires be white like the rest of the scan". Every `wheel_*` material slot now uses the scan's silver material. T1 (202 frames) and T2 (91 frames) were re-rendered at the same draft settings.
- Cuts and timing are unchanged from v0.5 (frames 388/517/533/597). 22.6 s, -14.0 LUFS, true peak -2.8 dBFS. Safe-zone text boxes are OK.
- The contact sheet confirms silver wheels in every scan shot. Ron's 1:1 end render still has his gold wheels, so the hard cut reveals the gold wheels, which is the real product finish. If they should stay silver through the cut, Ron's scene can be re-rendered with silver wheels (about 10 min).

## v0.7 (font and layered end text)

- **Font:** Unbounded Black/ExtraBold (Google Fonts, OFL) on all text. Akira Expanded is personal-use only and isn't in the brand Dropbox or Drive. If Epsilon holds a commercial Akira licence, swap the TTF paths in `tools/overlays_v0.py`.
- **End:** the black end card is gone, and Ron's 1:1 render plays to the end.
  - On the C3 kick: the Epsilon+ wordmark and "BLACK FRIDAY" appear behind the car. The roof and wing hide the lower part of "FRIDAY".
  - One beat later: the "30% OFF THE CIVIC FE KIT" pill appears in front of the doors, with "WWW.EPSILON.PLUS" on the floor.
  - The car matte comes from `tools/ron_mask_v0.py` (same camera, transparent film). It is used above the floor line (y 1088) only, because the floor glow is in the alpha.
- 22.6 s, -14.0 LUFS, true peak -2.8 dBFS, safe-zone text boxes OK. The cuts are unchanged from v0.6.

## v0.8 (owner font rule, knowledge/fonts.md)

- URL under the logo: Unbounded 400. Part names and struck was-prices: Unbounded 500 (repo `assets/fonts/unbounded/`).
- BLACK FRIDAY, the offer pill, the BF prices and the % OFF pills use Unbounded 900 as a **stand-in for Akira**. The owner still needs to supply the Akira file, then swap it into `font("b")`.
- -14.0 LUFS, true peak -2.8 dBFS, safe-zone text boxes OK. Timing is the same as v0.7.

## v0.9 (Akira)

- Akira Expanded SuperBold is the owner's licensed file: Drive 1nrF80enolDd9HAu5807kv5XIx0cUSDya, SHA-256 5b152fce... verified, in the gitignored `assets/fonts/akira/`. It is used for BLACK FRIDAY (opening tag and end headline), the offer pill, BF prices and % OFF pills.
- Unbounded 400 for the URL beside the logo; Unbounded 500 for part names and struck was-prices.
- Every glyph is present (no tofu; the strings are ASCII only). The headline auto-fit at 170 px and the offer at 42 px. Safe-zone text boxes OK, -14.0 LUFS, true peak -2.8 dBFS.
- The owner approved v0.8 apart from the font, so v0.9 is the final of this draft pass. Production quality (full-res renders, nesting) is still the v1 list above.

## v0.10 (end text off the car) and v1 full-res queue

- v0.10: the offer pill and URL sit below the car on the floor; nothing covers the car. The headline stays behind the roof and wing. Safe zones OK.
- The user approved v0.10 for full resolution. `queue_full.sh` (media dir):
  - Ron's still at 100 % / 128 spp, plus its matte.
  - T2 then T1 at 1080x1920, 32 spp + OIDN, real 30 fps.
  - The scan was re-prepped at 2.5 mm clustering (`CELL=0.0025 SCENE=scene_full`). At 5 mm the full-res frame showed speckles on the hood and headlight edges; 2.5 mm is clean at the same ~70 s/frame.
- Assemble with: `VER=v1 RFPS=30 T1DIR=r/T1full T2DIR=r/T2full RON=r/ron7_portrait_full.png MASK=r/ron7_mask_full.png`.

## v0.11 (longer end, garage background)

- The end runs to beat 48 (25.83 s), so the text is on screen ~5.9 s (was 2.7 s). A 4% push-in on Ron's shot starts at 1.0 on the 1:1 cut frame. -14.1 LUFS, true peak -3.9 dBFS, safe zones OK.
- Ron's end shot is in a procedural plain garage (`tools/garage_v0.py`, `GARAGE=1`): grey walls, a dark lower band, dark low-spec concrete floor (the camera at 0.38 m makes a glossy floor a mirror), LED tube rows. Full res, 128 spp. The matte is now car-only.
- The scan shots are still silver on black (the full-res queue was already running). Waiting on the user whether the garage should go in the scan shots too.
- Final assembly: `VER=v1 RFPS=30 T1DIR=r/T1full T2DIR=r/T2full RON=r/ron7_garage_full.png MASK=r/ron7_mask2_full.png END_S=25.825 PUSH=0.04`.
