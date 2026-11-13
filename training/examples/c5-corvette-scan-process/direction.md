# C5 scan-process reel - scene direction (v3, all-reels brief + user notes 2026-11-11)

## Feature inventory (registered to the 2023 full car unless noted)
| region | scans | states / parts | richness |
|---|---|---|---|
| rear | full car rear fascia; 'Rear bumper removed' (body, 8,028,053 tris, ICP 0.7 mm); 'rear bumper inside' (inside of the cover, sits ~5 mm under the skin) | rear bumper OFF state + rear bumper part (skin + scanned inside, mounting side) | 1 state + 1 part |
| front / right side | 'fender and bumper removed', 'front bumper removed', 'front bumper' (inside+outside), 'Fender outer' + 'Fender Inner' | stripped-front state + 2 parts with scanned insides; real teardown footage + 1:1 cut | richest: 1 state + 2 parts + IRL |
| hood | 'C5 Supplement Hood Open' does NOT register (FPFH fitness 0.05) | none - never show the hood open | - |
| signature | pop-up headlamp nose, CORVETTE rear fascia, quad taillights | shown in A (rear) and the listing end pose (front-left 3/4) | |

## Scene order (travel rear -> right side/front -> whole car; no ping-pong)
| scene | scans | feature shown | why here | kicks | camera |
|---|---|---|---|---|---|
| irl_open | 0056 | real stock rear 3/4 | brief: open on real footage; only stock-state frame (hood out of shot) | 0-K0 | real (native portrait, already full frame - cannot widen) |
| scan_AR (NEW, replaces A + R) | full car (rear-stripped + rear bumper part) | 1:1 rear, pull back to rear 3/4, rear bumper slides back toward the camera and turns its mounting side to the lens, rear-removed structure underneath | opening is at the rear, so the rear data plays here: one held rear section instead of A then a separate R later (v2/v3 showed the rear 3/4 twice) | K0-K7 (7.6 s) | cam_A -> rear 3/4 az 150 el 13 d 5.0 -> slight orbit to az 140 el 17 |
| irl_fender / irl_bumper / irl_stripped | 0059, 0060, 0078 | crew pulls the front fender and bumper | real teardown leads into the richest region | K7-K9, K9-K11, K11-K12 | 0078 crop widened to 1158x2058 (was 1000x1778) |
| scan_B | stripped front + fender + front bumper | 1:1 stripped right front; fender lifts above its arch and turns to show its scanned inside; bumper glides toward the camera turning its mounting side to it | richest region gets the longest held scan beat; camera stays on the front section | K12-K17 (5.5 s) | cam_B_wide -> right-front 3/4 |
| scan_C | stripped front+rear (x-ray) + 3 parts | parts translate home, orbit through the nose to the listing hero angle, morph to listing grey | reassembly closes the teardown; ends on the listing pose | K17-K22 (+0.5 s dissolve) | as v3 (reuse C2) |
| website | listing | title -> page -> logo -> URL | brief: shorter end, strong final cut | ~K22 to 31.2 s (5.7 s, was 7.1) | WebZoom |

## Diff vs v2/v3
- Dropped: separate scan_R (merged into scan_AR); irl_parts 0074 (fender inside shown in scan_B already - same subject twice).
- Re-render: scan_AR (new, 115 frames), scan_B (new wider crop -> new start camera, 84 frames). Reused: C2 + C2_clay, all IRL clips, webzoom (re-rendered shorter only).
- All renders persistent-data OFF; luma checked on every frame.

## Addendum (user feedback for all reels: crops, redundancy, bumper-removed hero beats, no faked openings)
Section coverage - each section appears in ONE continuous sequence:
| shot | section | covers |
|---|---|---|
| irl_open | rear (real) | stock rear 3/4 |
| scan_AR | whole car -> rear | 1:1 rear, whole car rear 3/4 (fully in frame), rear bumper mounting side, push-in on the exposed rear structure ('Rear bumper removed' scan) + labels |
| irl_fender / irl_bumper / irl_stripped | front (real) | crew removing fender + front bumper |
| scan_B | front / right side | 1:1 stripped front, fender inside, front bumper mounting side, push-in on the exposed nose structure + labels |
| scan_C | whole car (x-ray) | reassembly orbit ending on the listing angle - the only whole-car pass after the opening |
| website | listing | end card |
No hood, trunk or door shots: no open-state scan of this C5 registers (hood-open supplement failed).
Crop check: first / middle / last frame of every scan shot reviewed at 25-30 % before the finals.

## v5 (user: Z06 engine bay anyway, more scans, no roof cockpit after the roof leaves, no triangle counts)

| beats | t (s) | shot | focus |
|---|---|---|---|
| 80-84 | 0-2 | IRL 0056 | rear pass, ends on solved frame |
| 84-100 | 2-10 | AR | 1:1 cut; rear bumper mounting side; bumper-removed structure |
| 100-106 | 10-13 | T (trimmed) | targa lifts, underside; cut as it leaves |
| 106-120 | 13-20 | IRL fender / bumper / stripped | crew work |
| 120-130 | 20-25 | B4 | 1:1 cut; fender inside, bumper mounting points, stripped nose |
| 130-138 | 25-29 | E | Z06 engine bay scan, own frame, look-down drift |
| 138-142 | 29-31 | head lamp, turn signal | front lighting parts, 1 s each |
| 142-152 | 31-36 | door panel on -> removed | same camera, state cut on beat 146 |
| 152-154 | 36-37 | fuel door | rear quarter, fuel door open |
| 154-158 | 37-39 | U | underbody, x-ray |
| 158-172 | 39-46+ | C -> listing | reassembly, dissolve into listing, URL on final hit |

Not used: C5 Interior and left doorsill (fragmentary at every angle), standalone Door Cover (redundant with door-panel-on).
