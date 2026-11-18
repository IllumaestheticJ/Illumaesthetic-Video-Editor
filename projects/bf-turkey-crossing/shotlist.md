# BF 10 - "turkey-crossing" - shot list

Planned 2026-11-18. v0 is a quick draft built on the default answers below; the owner's notes drive v0.1+.

## Concept (one line)
A cute cartoon turkey waddles onto a country road, stops mid-lane and looks at the camera. Headlights appear. A V2-kitted GR Corolla charges in, and on the music's drop there's a cartoon **POOF**: a white puff cloud and a burst of feathers, with no turkey left on screen. Feathers drift down over the empty road, the sale text slams in (Akira), and the reel ends on the Epsilon+ wordmark and WWW.EPSILON.PLUS.

**Owner's concept (verbatim):** "have a cute turkey crossing the road and then a GR corolla running over it and then the sale text".

## Tone
Cute, cartoony slapstick, not gory: no blood, no body, no squash. The hit itself is never shown, only the "poof". The turkey is a one-off gag character, not a mascot (owner rule: no Del & Eps / mascots).

## Length and format
- 9:16, 1080x1920, 30 fps, about **12.2 s**.
- Music at -14 LUFS, true peak below -1 dBFS. Every cut lands on a measured hit.

## Music
| # | Track | Source | Why |
|---|---|---|---|
| **1 (v0)** | **"TRANSFORMATION" - PhonkFlux** (49.5 s) | TikTok CML song_clip_id **7634998460610005008** (Higgsfield `tiktok_music_trending`, EDM 7-day US #97, 2026-11-18) | Cowbell phonk at ~133 BPM. The cowbells drop out at 13.52 s while the 808 builds, then everything slams back in at **16.227 s**, which is the impact. It is in no other reel. |
| 2 | "Akon's Beautiful Day (David Guetta & Hypaton Remix)" | CML 7462481016674846721 | Brighter and funnier, but it has a lyric hook. |
| 3 | "Kawaii pop ending" - bunkiman | CML 7608391706480314385 | The cutest option, but it has no drop: the impact would need a hard music stop. |

Not used: "Invincible" and "Ghosts 'n' Stuff" (both used in earlier reels; the owner disliked Ghosts).

**Measured hits** (spectral-flux onsets, 30-90 / 150-1100 / 3k-10k Hz, decoded from the CML preview file):
- Bar grid: 1.80 s (beat 0.4505 s).
- Video t=0 is track 10.812 s.
- Hits in the track: 12.650, 13.516 (cowbells out), 14.419, 15.322, **16.227 (drop)**, 18.023, 18.929, 19.827, 21.630 s.

## Shot table
Frame numbers are at 30 fps from video t=0 (track 10.812 s).

| # | Time (s) | Frames | Beat | Camera | Subject | Source asset | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-1.84 | 0-55 | hit 10.812 to hit 12.650 | Low road-level (0.25 m), 35 mm, side-on across the lane | Turkey on a country road; autumn trees, fence and verges | Procedural low-poly turkey (built in Blender, `tools/turkey.py`) | The turkey waddles right to left across the lane, bobbing its head, tail fan wobbling | none | cut on hit | Blender Cycles |
| 2 | 1.84-3.61 | 55-108 | 12.650 to 14.419 | Push-in to a medium close-up, eye level with the turkey | Turkey mid-lane | turkey | The turkey stops on the centre line. When the cowbells drop out (13.516 s, f81), its head snaps to camera, it blinks twice, and there's a tiny head tilt | none | cut on hit | Blender |
| 3 | 3.61-4.51 | 108-135 | 14.419 to 15.322 | Low reverse shot down the road, 50 mm, the turkey's eye view | GR Corolla charging in, headlights on | `eps-toyota-gr-corolla-v23.glb` (V2 lip, skirts and spats; V1, canards and wing hidden; plates stay) | The car grows fast toward the lens, wheels spinning, motion blur | none | cut on hit | Blender |
| 4 | 4.51-5.41 | 135-162 | 15.322 to **16.227** | Close-up on the turkey's face | Turkey, lit by the headlights (a light sweeps across it) | turkey | Its eyes go huge and its feathers puff up | none | **hard cut on the drop** | Blender |
| 5 | 5.41-7.21 | 162-216 | **16.227 (impact)** to 18.023 | Wide low road shot, 24 mm, slight camera shake on impact | The car blasts through the frame | GLB + turkey | **Proposed gag:** frame 162 is a 2-frame white flash, then a cartoon **POOF** cloud (white puffs) where the turkey stood, plus about 60 feathers bursting out. The car exits the frame. The puff clears and the turkey is gone; the feathers float down | none | cut on hit | Blender |
| 6 | 7.21-9.02 | 216-270 | 18.023 to 19.827 | Static low shot of the empty road, feathers drifting through the frame | Feathers settling on the road | Blender plate | "BLACK FRIDAY" slams in on 18.023; "SALE" punches in on 18.929 (f243) | **BLACK FRIDAY / SALE** (Akira Expanded) - v0 default, see Q1 | cut on hit | Blender plate + PIL text |
| 7 | 9.02-12.2 | 270-366 | 19.827 to end | Black card | Epsilon+ wordmark at 720 px, with WWW.EPSILON.PLUS under it | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | The logo lands on 19.827, the URL on 21.630; music fades out over the last 0.8 s | **WWW.EPSILON.PLUS** (Unbounded 300, beside the logo) | fade | PIL |

**Softer alternative for the impact (Q2):** at f162 the turkey springs straight up out of frame (a cartoon jump, "boing"). The car passes underneath and only a puff of feathers flies off. The turkey lands back on the road behind the car, bald-ish and dazed, then waddles off. Same timing, same beats.

## Text rules applied
- The whole reel is CGI. There is no IRL footage, so there is no text-over-footage issue.
- Text appears only on shots 6-7, inside x 48-920 and y 285-1440.
- Akira is used for the offer only. The URL beside the logo uses Unbounded 300.
- **No invented numbers.** The v0 text is "BLACK FRIDAY SALE" (no figure). If the owner picks the GR Corolla lines, they come from the BF sheet, which confirms both (PRICES.md):
  - V2 lip $285 to $199.50, skirts $400 to $280, spats $175 to $122.50 (all 30 %), giving **"V2 KIT 30% OFF"**.
  - V1 lip PU 40 %, carbon 45 %, skirts 40 %, spats 40 %, giving **"V1 UP TO 45% OFF"**.
- No dates and no stock counts.

## Assets
| Asset | Status | Where |
|---|---|---|
| GR Corolla lookbook GLB (V2 kit) | downloaded, 5,192,780 bytes | CDN `eps-toyota-gr-corolla-v23.glb` (also in Drive zip 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) |
| Turkey | **built procedurally in Blender** (no third-party model or licence) | `projects/bf-turkey-crossing/tools/turkey.py` |
| Country road environment | built procedurally | `tools/scene.py` |
| Akira Expanded Super Bold | installed (SHA-256 5b152fce...a5775 matches), gitignored | `assets/fonts/akira/` |
| Unbounded 300 | in repo | `assets/fonts/unbounded/` |
| Epsilon+ wordmark | downloaded | Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Music | claimed in MUSIC.md | CML 7634998460610005008 |

The car paint in v0 is Supersonic Red, as in BF6 v0, with the V2 kit in black PU.

## Open questions for the owner
1. **Sale text:** "BLACK FRIDAY SALE" (v0), or the GR Corolla offers "V2 KIT 30% OFF" + "V1 UP TO 45% OFF" (as in BF6)?
2. **The gag:** the POOF + feather burst with the turkey gone (v0), or the softer version where the turkey jumps clear, only its feathers fly, and it waddles off dazed?
3. **Music:** keep "TRANSFORMATION" (PhonkFlux), or swap?
4. **Car colour:** Supersonic Red (v0), or the white Castrol #24 livery car?
