# Suzuki Cappuccino - scene direction v2 (scene-director, 2026-11-11)

Inputs read: CLAUDE.md, knowledge/lessons.md (all), style-guide.md, clips.md, project.yaml, cuts.json, editlog.jsonl,
review.md, director_report.md, shots.py, tools/shot.py, the user's v2 brief (9 points) and the follow-up feedback (A-D,
overrides the brief where they conflict). No feedback.jsonl exists yet. Contact sheets of every v1 render dir (6 frames per
shot) and native-res crops of s06 f59 (front, bumper off + hood up) and s07 f45 (rear, bumper off + trunk up) were looked at;
sheets in the scratchpad, not committed.

## Step 1 - feature inventory (from the scans, not the model name)

| region | scans | what the data shows (seen in v1 renders) | quality | richness |
|---|---|---|---|---|
| FRONT (bumper) | Front Bumper.stl (part, 0.78M tris @2 mm), Front Bumper Lights.stl (part, 2 small lamps, x +-0.55 m, z 0.32-0.37), state Front Bumper Off, Hood Open | bumper skin **inside + outside** (area-weighted normals +Y 29 % / -Y 26 % = both faces captured); inner face has **mounting tabs/brackets** (visible in s06 f59). Behind it: lower front structure - a horizontal lower cross-member/core-support panel with openings, a cylindrical unit on the right, the underside of the nose panel | good; grille openings in the bumper skin are holes; the structure panel has black scan speckle | **highest** (2 parts + state) |
| ENGINE BAY | state Front Bumper Off, Hood Open; hood cut from full car + hinge fitted to the captured sliver (-52 deg, 13 mm) | engine top with intake tract, cam cover, plumbing, strut tops, cowl; one fender + headlamp in the state scan | good; hood **underside not scanned** (outer skin seen from below), propped hood only a 9k-tri sliver | high |
| SIDE / WHEELS | Full Car.stl | 6-spoke wheels, tyres with sidewall lettering, door, hardtop; profile | upper rim crisp, **lower rim/hub speckle**; no side parts or states; no interior | low (signature wheel only) |
| REAR | Rear Bumper.stl (part, 0.87M tris), states Rear End All Removed (bumper off) and Rear End Trunk Open (bumper on, lid propped, partial) | rear bumper skin, **inside + outside** (normals +Y 37 % / -Y 34 %); behind it: rear panel with tail-lamp backs, **wiring along the panel**, a **pipe running under the rear panel (exhaust)**; boot interior; trunk lid cut from full car, hinge fitted to the captured sliver (+63 deg, 12 mm) | rear panel ragged in places (holes); lid underside not scanned | high (1 part + 2 states) |
| TOP | Full Car.stl | hardtop roof, planform | nothing new vs side/whole | low - no own section |
| INTERIOR / UNDERSIDE | none | - | not scanned | none - never shown |

Signature features of THIS scan: tiny kei proportions + long hood/short deck (whole car), oval headlamps with the two
bumper lamps under them, 6-spoke wheels, the hardtop. Not scanned as states: doors, roof panels, wheels off.
Unused on purpose: Rear Bumper Trunk Open (same capture as Rear End Trunk Open), New Turn Signal (design part).

## Step 2 - order (front data first, then side, then rear; each section ONE continuous sequence)

Travel: front-right 3/4 whole car -> nose -> engine bay -> right front wheel -> rear -> (finale over the top / left side).
The FRONT (2 parts + state) is the richest region, so the hood opening of the front state lands ON the drop (15.272 s),
inside a held shot (no cut needed in the 13.84-15.27 break). The two bumper-removed states are the hero beats (feedback C):
each gets its own long section where the bumper comes off and the camera moves in on what is behind it and holds.

| # | scene / section covered | scans used | feature shown | why here | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | WHOLE (opener) | car2 (2 mm full car) | whole car, front-right 3/4, fully in frame with margins | front carries the strongest data, so the opener frames that end; v1 openers were cropped (24 mm sensor at 4.4-5 m clipped the car) | b0-8 (8) | 8.4 -> 7.4 m, 40 mm, slow 20 deg arc + push, moving from frame 1 |
| 2 | FRONT: bumper + lamps, then what is behind | base, fb_nolights, Front_Bumper_Lights, hood (shut) | headlamp + bumper lamp in place -> lamps out -> bumper out and tipped (inner face, mounting tabs) -> push in and HOLD on the exposed front structure | hero beat 1 (feedback C); a region's close-ups next to its wide | b8-28 (20) | low nose close -> elevated nose+bumper frame -> bumper inner face -> structure hold |
| 3 | ENGINE BAY | base, hood (hinge), parts in s2 end pose | hood swings up to its captured angle ON the drop, push into the bay | state scan's richest content gets the drop; follows the front without a cut back | b28-40 (12) | high front, el 26 -> 55 (hood edge-on, underside not the subject) |
| 4 | WHEELS (side) | car2 | front-right wheel, 6 spokes, tyre | only side data worth a frame; weak lower rim -> 4 beats; travel continues down the right side | b40-44 (4) | REUSE v1 s04_wheel |
| 5 | REAR: bumper, what is behind, trunk | base, Rear_Bumper, trunk (hinge) | rear bumper out and tipped (inner face) -> push in and HOLD on rear panel / wiring / exhaust -> trunk lid up to its captured angle, look into the boot | hero beat 2 (feedback C); second-richest region, longest held shot after the front | b44-62 (18) | rear-right close -> elevated tail+bumper -> structure hold -> side-high into the boot |
| 6 | FINALE a: layers rise (top) | exploded set | trunk lid, rear bumper, then hood/front bumper/lamps rise into layers above the car | Temerario progressive explode; brief 7; high angles = the only 'top' coverage | b62-68 (6) | high rear-left -> crane over the top (never straight down) |
| 7 | FINALE b: reassembly + fade | exploded set -> car2 swap | whole layered car from the left, parts fly home staggered, clean car, fade | new angle (left side never shown); ends on whole car not repeating the opener (front-right) | b68-76 (8) | high left side -> left-rear 3/4, whole car with margins |
| 8 | LOGO | logo card | small logo (~35 % width) | final two hits under it | b76-end (5.6) | static |

Section coverage (feedback B): WHOLE s1 (+ finale, exploded, different angles); FRONT s2 only; ENGINE BAY s3 only;
WHEELS/SIDE s4 only; REAR s5 only; TOP s6 only (finale). No section is revisited outside its sequence.

## Music map (126 BPM, beat n = 0.033 + n x 0.47619 s; cuts on even beats)
| scene | starts | music |
|---|---|---|
| 1 | 0.000 (b0) | intro kicks, fade up 0.5 s |
| 2 | 3.843 (b8) | accented kick |
| 3 | 13.366 (b28) | last accent before the break (13.84-15.27); hood swings ON the drop b32 = 15.272 inside the shot |
| 4 | 19.081 (b40) | accent |
| 5 | 20.985 (b44) | accent |
| 6 | 29.557 (b62) | accent |
| 7 | 32.414 (b68) | accent; clean-car swap on b74 = 35.271 |
| 8 | 36.224 (b76) | logo before break 2 (36.70-37.18); hits 37.653 / 38.129 under it; end 38.89 |

## Text (feedback C overrides the original "no text" brief)
Short factual labels, ScanHUD label style (Inter Display, off-white, max two on screen, enter on a beat, leave >= 0.25 s
before the cut, outside the car silhouette, out of the bottom 20 %). Only things visible in the renders/scans:
- Confirmed in v1 renders: FRONT BUMPER REMOVED, MOUNTING POINTS (bumper inner tabs, both bumpers), ENGINE BAY,
  REAR BUMPER REMOVED, TRUNK OPEN (state captured).
- Conditional - add only after the editor sees it clearly in the new close-up frame: EXHAUST (pipe under the rear panel;
  likely), CRASH BEAM (the horizontal lower front member - from v1 resolution I cannot tell a bumper reinforcement beam from
  the radiator core support, so default label is none), WIRING (rear panel).
- No numbers, no specs. No labels in the opener, wheel shot, finale or on the logo.

## Hinged lids vs states as captured (feedback D)
Keep the hinge swing. Both lids are real (cut from the full-car skin) and each swings on the axis fitted to the lid sliver
of the registered open-state scan, stopping at the **captured** angle (hood -52.0 deg, trunk +62.9 deg; v1 stopped at 90 %).
Showing the states "as captured" would show the car with the hood/trunk lid **missing** (only 9k/30k-tri slivers exist),
which implies a removed-lid state that was never scanned. Both open states exist and register (2-2.7 mm), so the opening is
not faked. Constraint: frame so the lid underside (unscanned) is edge-on or out of frame.

## Diff vs v1 timeline
| v1 shot | v2 | why |
|---|---|---|
| s01_side | dropped | cropped (24 mm sensor at 4.4-4.6 m), and a side profile is a repeat of the whole-car view (report IoU 0.82 vs s02) |
| s02_front34 | replaced by new s1 opener | cropped rear; turntable |
| s03_rear34 | dropped | rear exterior turntable = ping-pong before the front story; rear is told once in s5 |
| s04_wheel | **kept as-is**, moved to 19.08 s | right content; detail fills the frame |
| s05_lamp | merged into s2 (its first beats) | same subject as the bumper/lamps removal |
| s06_frontopen | split into s2 (bumper) + s3 (engine bay), both new, close | v1 was one wide orbit, parts small; hood at 90 % |
| s07_trunk | replaced by s5 (new, close) | wide; now bumper inner face + structure hold + trunk |
| s08_top | dropped | rotating top-down showed nothing new (lesson: no wasted rotations) |
| s09_explode / s10_float / s11_reassemble | replaced by s6 + s7 (new) | wide, parts small, three shots of one view (IoU 0.75/0.70), held too long |
| logo | re-made smaller (~35 % width) | Temerario: small logo; v1 card ~75 % width |

## Open questions for the editor (don't guess)
1. CRASH BEAM label: render s2's hold frame first; if a distinct horizontal reinforcement beam reads, add it; else no label.
2. EXHAUST label: confirm the pipe under the rear panel in s5's hold frame.
3. Both bumpers' inner faces: normals say both sides scanned - confirm with one still each (lesson 240SX) before the tip.
