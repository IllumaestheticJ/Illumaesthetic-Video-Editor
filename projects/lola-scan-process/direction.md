# Lola scan-process reel — direction v3 (scene-director + director stages)

The scene-director agent isn't registered in this session (it was added mid-session), so the editor followed
`.claude/agents/scene-director.md` and `director.md` by hand.

Inputs:
- User on v2: "remove illumaesthetic.com" and "clean up footage at end (or a trailer 1:1)". No trailer file is available.
- Parent all-reels brief (2026-11-11).
- `director_report.md`.
- Contact sheets of every render. The luma check on s1_A, s2_B_v2 and s4_wing found no dropouts; the car stays at about 180 luma throughout.

## Feature inventory
| scan | shows | signature features | states / parts | weak data |
|---|---|---|---|---|
| Lola 1 Exterior (21,696,194 tris) | whole dusty AE86 hatch, no wing | Watanabe-style wheels, hatch glass, side mirror | none (no open/removed scans) | glass slightly ragged |
| Lola 1 Interior (25,188,507 tris) | gutted cabin + roll cage, registered `--like` the exterior | cage, bare floor | inside surface of the same body, not a removed part | fragmentary outer edges |
| Lola 2 Full Car (49,997,072 tris, 4 mm decimated) | Bennett Racing wing car | GT wing + uprights, pop-ups, wide arches | none | holes in the grille/pop-up housings, under the front bumper |

The richest region is Lola 1, with two registered scans (inside + outside). It gets the biggest moment: 1:1 cut B into the lift on a strong kick.

## Decisions
- **(a) Lola 1 "outside lifts off inside" (s2_B_v2): keep.**
  - No part removal is implied. These are two scans of the same body: the outer surface and the inner surface/cage.
  - Lifting the outer one reveals real scanned data underneath, so there is no blank space. The label says what it is: "INSIDE + OUTSIDE · LOLA 1 SCANNED".
  - It translates only. The v2 spin was removed because the shell's underside is not worth a spin.
- **(b) Lola 2 travel.** IRL Lola 2 shows the wing being sprayed. So the scans go **wing (rear) → whole car (pull out)**, not front → rear → front: it continues the subject the IRL shot showed and travels from detail to whole car.
- **(c) Ending, "don't hold too long".**
  - The hero goes from 5.97 s to 3.23 s, which removes the 0.9 s of dead frames the director report flagged.
  - The logo lands on the re-drop (24.374 s), not 26.778 s.
  - The reel is now 27.6 s.
- **Cut list (v2 → v3):**
  - `screen_color`: software UI, mouse cursor and a ground-scrap shadow (messy).
  - `scan_front`: clipped on both sides, holes in the grille and under the bumper (weak data).
  - `scan_hero` (orbit, car cut off on the right): replaced by `s3_hero_v3`, the whole car centred with a slow push-in and no orbit.
  - The URL on the end card.
- **IRL crop widening (brief #9): not possible here.**
  - The glasses footage is 3:4 portrait, and the 9:16 crops already use the full sensor height (spray 1116×1984 of 1488×1984).
  - A wider frame would need bars, so the crops are unchanged.
- **"Label what the scan is used for": not added.** The files don't say what the film uses the scans for, so a label would be invented.

## Final timeline (30 fps; each cut = round(kick × 30); first clip one frame short)
| # | shot | src | focus | start–end (s) | frames |
|---|---|---|---|---|---|
| 1 | irl_spray | sel/spray.mp4 12.5→14.9 | powder sweep, Lola 1 side | 0.000–2.444 | 72 |
| 2 | scan_A | s1_A | same view as scan (1:1 A on the drop) | 2.444–5.190 | 83 |
| 3 | irl_scanner | sel/scanner.mp4 5.833→9.433 | handheld scanner, rear 3/4 | 5.190–8.795 | 108 |
| 4 | scan_B | s2_B_v2 | 1:1 B → outside lifts off inside | 8.795–13.421 | 139 |
| 5 | irl_interior | sel/interior.mp4 1.5 | scanning the cage | 13.421–14.797 | 41 |
| 6 | screen_register | sel/sr_register.mp4 ×2 | interior fragments aligning | 14.797–16.161 | 41 |
| 7 | irl_lola2 | sel/lola2_irl.mp4 3.25 | spraying Lola 2's wing | 16.161–18.396 | 67 |
| 8 | scan_wing | s4_wing | the same wing as scan, uprights | 18.396–21.142 | 82 |
| 9 | scan_hero | s3_hero_v3 | whole Lola 2, push-in; counter | 21.142–24.374 | 97 |
| 10 | logo | end_card_v3.mp4 (logo only) | brand | 24.374–27.600 | 97 |

Hold list (> 0.75 s):
- The scan holds carry motion (orbit, lift, push).
- The scanner clip plays out its action (brief: "let the action play out").
- The logo card holds for the fade.

Renders: all reused. The only new one is `s3_hero_v3` (90 frames), already rendering.

## Addendum A–D (parent, 2026-11-11): cropping, redundancy, bumper data, openings
- **Sections, each in ONE continuous sequence:**
  - Lola 1 driver-side front 3/4: irl_spray → scan_A.
  - Lola 1 rear 3/4 + interior: irl_scanner → scan_B → irl_interior → screen_register.
  - Lola 2 rear/wing: irl_lola2 → scan_wing.
  - Lola 2 whole car, front 3/4: scan_hero.
  - `ive director` flagged no repeated views.
- **Cropping:**
  - `scan_wing` was re-rendered as `s4_rear_v3`. The rear 3/4 holds the whole rear end and wing at about 70% of the width with margins; the v2 shot clipped the bumper at the left edge and had an empty bottom half.
  - `scan_hero` is `s3_hero_v3`, with the whole car centred.
  - `scan_A` and the start of `scan_B` keep the IRL framing because they are the 1:1 match frames. `scan_B` then pulls back to the whole inside + outside pair.
  - First/middle/last frames of every shot are checked before assembly.
- **Wider IRL crops:** blocked by the source. The 3:4 glasses frames are already cropped at full height. The only way to go wider is to letterbox, which is a question for the user.
- **Bumper-removed, trunk, hood, door states (C, D):** no such scans exist for either Lola, so none are shown. No opening is faked.
