# Mazda RX-7 FC3S - scene direction v3 (scene-director, 2026-11-13)

User request (verbatim): "use every scan i have for this car, re-edit to this music, add the call-to-action since this
should have had every panel replaced". Reading (parent, backed by Drive): this is the HertLife FC3S. The reel strips the
stock panels that really come off (hood, front bumper, rear bumper: registered state scans), puts the HertLife printed
time-attack kit on section by section (front -> sides -> rear), lands the finished widebody on a strong downbeat, then a
mobile CTA for the FC3S scan listing and the logo. Music: T-Pain "Hert Baby Got Brap", music_v3.json (90 BPM, bar 2.6667 s,
excerpt 18 bars = 48.0 s, drop at video 5.333).

Read for this plan: lessons.md (all, newest sections), style-guide, clips.md, project.yaml (v2), direction.md/director.md (v2),
editlog, review.md, music_v3.json, hinge.json, prep/*.json bboxes, the kit check sheet (kitcheck1.jpg, kit in red over the
car: front 3/4, side, rear 3/4), contact sheets of every reusable render (s1, s4, s6, s9, s10, s11, s12, s13; 8 frames each,
`scratchpad/cs_all_v3dir.jpg`), the listing capture `/home/user/media/work/rx7/cta/listing_mobile.png` + listing_info.json,
the HertLife Drive tree. Shot numbers: `director_v3.md`. No feedback.jsonl exists for this project.

## 1. Feature inventory

### Stock scans (S5 session, all registered in the prepped frame)
| region | scans | what the data shows (checked in renders) | weak data | score |
|---|---|---|---|---|
| Front / nose | Full car, **Front Face** part (fbumper.blend, inner face scanned, 93 % of bins), **Hood Off Bumper Off** (bay + radiator support fill in comp_explode_dp) | Front bumper comes off for real; behind it: radiator support, lower crash beam, end brackets (s11 frames). Pop-up lids down in every scan. | pop-ups-up state: none | 5 |
| Hood / engine bay | **Hood Up** (hinge fit 2.6 mm, open 44.42 deg; captured open panel = hood_up.blend), Hood Off Bumper Off | Hood opens on its real hinge to the captured angle and lifts off over a real bay (s6 -> s9 seamless) | hood part is outer skin only (no flip) | 4 |
| Rear | **Rear Bumper Removed** (rear crash bar fill in comp_explode_dp), rbumper.blend (outer skin) | Rear bumper off; crash beam with four slotted mounting points + end brackets | tail-lamp lenses and hatch glass = holes; plate already flattened (_dp) | 3 |
| Sides | Full car only | Stock fenders/doors/sills. **No scan of fenders or sills removed** -> stock fenders stay; the kit goes over them | no removal state | 1 (stock) |
| Wheels | Full car | stock wheels, hub/lower-rim specks | holes in hubs | 0 -> no scene (the kit does not change wheels) |
| Top / interior | Full car | roof; rear glass is a big hole | hole | 0 -> no scene |

Not shown, and why (see open question 1): **Hood Down Bumper Off** (same bumper-off data as Hood Off Bumper Off, with the hood
on; showing it would need bumper-before-hood order and adds nothing the viewer can see), **FC3S Full Car 2025** (other
session, not in this frame), **HertLife FC3S_scan_1.stl** (the design scan, 3.2 mm onto S5 = the same exterior as the S5 full
car; it is "used" through the kit that was designed on it).

### HertLife kit (printed time-attack kit, same frame; CAD, not scans - it is the product, not a state)
| region | kit parts (bbox from prep json) | goes on over | score |
|---|---|---|---|
| **Front** | k_fbumper (fixed-headlight openings) y 1.57-2.24, k_lights (headlights in the bumper; pop-ups deleted), k_splitter (+ fins, to y 2.35), k_canards (x +-0.98), k_hood (vented) y 0.63-2.04 | bare front (bumper off) + bay (hood off) | **5 parts** |
| **Sides** | k_side_r (x +0.62..+0.97, car's RIGHT), k_side_l (x -0.95..-0.55, car's LEFT): full-length skins = front overfender + rear overfender + sill skirt in one piece each; k_sidesplit (side splitters + fins, both sides in one object, y -0.85..0.88, z 0.27-0.49) | stock fenders/doors (kit is wider: x +-0.95 vs +-0.85) | 3 parts |
| **Rear** | k_rbumper, k_diffuser (diffuser, strakes, rear bumper side pieces, to y -2.46), k_exhaust (tips), k_wing (GT wing, endplates, uprights, z to 1.45) | bare rear (bumper off, crash beam) + hatch | 4 parts |

Note: the brief calls k_side_l the "+X side"; its bbox says x -0.95..-0.55 (car's left). Plan uses the bbox.

### Richness (states + parts + signature + quality)
Front 2 real states + 1 real part + 5 kit parts + signature pop-up nose -> **richest**; rear 1 state + 4 kit parts incl. the
GT wing -> second; sides 0 states + 3 kit parts (the width change is the widebody's signature) -> third.

## 2. Scene order

Opener = the stock car whole (front-right 3/4, the nose that the kit replaces most), moving from frame 1, over the soft
2-bar lead-in. The transformation starts ON the drop with the first real removal (hood opens on its hinge). Then travel
front -> sides -> rear, each section once: stock parts off (real state scans) -> kit parts on, framed on that section.
Finished widebody revealed on the bar-14 downbeat from the rear-left (never the opener's angle), ending on the listing
viewer's pose for the CTA.

| # | scene | scans used | feature shown | why here (inventory) | bars | camera note |
|---|---|---|---|---|---|---|
| 1 | Stock opener | full car | whole stock FC3S, pop-up nose leading | brief: whole stock car, motion from frame 1; front = richest end | 2 (0-5.333) | REUSE s1_front34_pad (low front-right turntable, margins) |
| 2 | Hood opens | comp_hood + hood on fitted hinge | hood rises to the captured Hood Up angle | first real state, starts moving ON the drop | 1 | REUSE s6 from 0.733 s |
| 3 | Hood off | comp_hood + captured open hood | open hood lifts off, camera over the bay | Hood Up + Hood Off captures; seamless with #2 | 1 | REUSE s9 from 0.533 s |
| 4 | Front bumper off | comp_explode_dp + Front Face | bumper off its mounts, tips to show its scanned inside | rule C hero; inside is scanned | 1 | REUSE s10 |
| 5 | Behind the bumper | comp_explode_dp (Hood Off Bumper Off fill) | radiator support, crash beam, brackets (labels) | rule C: hold on what is behind | 1 | REUSE s11 |
| 6 | Front kit on | comp_explode_dp + 5 front kit parts | headlights, front bumper, splitter, canards, vented hood go on in install order | richest region, 2 bars from the bar-6 phrase start | 2 | NEW c6, front-LEFT 3/4 mid-high (not s10/s11's front-right) |
| 7 | Widebody sides | + k_sidesplit halves, k_side_l, k_side_r | both side skins and splitters slide in from +-X; the car widens | sides have no removal data -> kit goes over stock; both sides only read from a high centred view | 2 | NEW c7, high front-centre, car length up the frame |
| 8 | Rear bumper off | + stock rbumper moving | rear bumper straight back, sinks away; push onto crash beam + mounting points (labels) | rule C hero (Rear Bumper Removed) | 2 | NEW c8 (s12's camera, but kit front/sides must be on: s12 shows stock fenders) |
| 9 | Rear kit on | + k_rbumper, k_diffuser, k_exhaust, k_wing | rear bumper, diffuser, tips, GT wing drops onto the hatch | second-richest region, ends the build on the bar-14 phrase | 2 | NEW c9, starts on c8's end pose, pulls back to high rear-right |
| 10 | Finished widebody | comp_explode_dp + all 11 kit parts | whole finished car, every replaced panel | final reveal on the 37.333 downbeat (4-bar phrase start) | 2 | NEW c10, rear-left 3/4 orbit ending on the listing viewer pose |
| 11 | Mobile CTA | listing_mobile.png | FC3S scan listing on a phone | user request | 1.25 | cta_card.py |
| 12 | Logo | logo card | ILLUMAESTHETIC, 760 px wide | newest lesson | 0.75 | logo_card.py |

Phrase structure: removals start on bar 2 (drop), front kit on bar 6, sides bar 8, rear bar 10, reveal bar 14, CTA bar 16.

## 3. Music map (video t; downbeat = 5.333 + k*2.6667; snares on beats 2 and 4 = downbeat + 0.667 / + 2.000)
| cut (s) | frame@30 | bar | scene | motion hits inside the scene |
|---|---|---|---|---|
| 0.000 | 0 | 0 | 1 opener | soft lead-in |
| 5.333 | 160 | 2 (DROP) | 2 hood opens | hood moving from the first frame, open by 7.600 |
| 8.000 | 240 | 3 | 3 hood off | lift starts 8.034, out of frame by 10.27 |
| 10.667 | 320 | 4 | 4 front bumper off | bumper off its mounts, tip completes at the cut |
| 13.333 | 400 | 5 | 5 behind front bumper | push onto the support; labels |
| 16.000 | 480 | 6 | 6 front kit on | lights home 17.333, bumper 18.000 (snare), splitter 18.667 (bar 7), canards 19.333 (snare), hood closes 20.667 (snare) |
| 21.333 | 640 | 8 | 7 sides | side splitters home 23.333 (snare), both skins home 24.667 (snare) |
| 26.667 | 800 | 10 | 8 rear bumper off | bumper off 28.000, gone 28.667 (snare); labels 28.667-31.8 |
| 32.000 | 960 | 12 | 9 rear kit on | rbumper home 34.000 (snare), diffuser 35.333 (snare), tips 36.000, wing lands 36.667 (snare) |
| 37.333 | 1120 | 14 | 10 FINISHED REVEAL | orbit into the listing pose, settles 42.4 |
| 42.667 | 1280 | 16 | 11 CTA | car shrinks into the phone's 360 viewer |
| 46.000 | 1380 | 17 beat 2 (snare) | 12 logo | logo to the end |
| 48.000 | 1440 | 18 | end | excerpt end |

## 4. Diff against the v2 timeline (v2 = 37.4 s on the old generated track)
| v2 clip | v3 | why |
|---|---|---|
| s1_front34_pad 0-4.53 | **reuse**, 0-5.333, src_fps 7.36 | stock opener; whole car with margins, moving from frame 1 |
| s4_nose | **drop** | front detail of the stock nose before the drop; no time in 2 lead-in bars, and the front gets 6 bars after the drop |
| s6_hood | **reuse**, in 0.733 | hood moving on the drop |
| s9_hoodoff | **reuse**, in 0.533 | seamless with s6 (same pose at the join) |
| s10_fbumper, s11_fsupport | **reuse** (re-timed) | content right; only position/speed change |
| s3_wheel, s5_mirror | **drop** | stock wheel/mirror details; the kit section covers the side; hub holes |
| s12_rbumper | **re-render as c8** | its rear-right view shows STOCK fenders, but by then the kit sides are on (continuity) |
| s13_reassemble | **drop** | reassembles the stock panels - contradicts "every panel replaced" |
| logo small 378 px | **rebuild 760 px**, 2.0 s | newest lesson |
| - | **new** c6, c7, c8, c9, c10, CTA | kit install + finished car + CTA |

New Blender frames: c6-c10, 5 x 84 = 420 frames ~ 2.3 h at ~20 s/frame (budget 3.7 h).

## 5. Open questions (not guessed)
1. "Use every scan": Hood Down Bumper Off, FC3S Full Car 2025 and the HertLife design scan (FC3S_scan_1.stl) are not shown
   (duplicates of shown data / other frame). Does the user mean those too, or "every panel scan + every kit part"? If the
   2025 scan or the HertLife scan must appear, the only honest place is a 1-bar "design scan" beat before c6 (registered at
   3.2 mm) - say so and I will re-time.
2. The listing page's dataset dropdown shows "Exterior Only (S4)" while this car is an S5. Confirm the listing sells this
   scan (or which variant to select in the capture) before the CTA claims it.
3. The listing's 360 viewer shows the STOCK car; the finale is the kit car. The CTA dissolve will read kit -> stock. OK, or
   should c10 end with a hard same-camera swap to the stock car (car4_dp) on 42.0 before the CTA?
4. On-screen name for the kit: "HERTLIFE" (Drive folder name) is the only source. No kit-name label until the user confirms.
5. The Drive also has a HertLife DRIFT kit (FC3_D.obj, Drift kit prints). v3 uses the time-attack kit only.
6. Kit colour: house silver (default in this plan) vs one satin colour so the replaced panels read at a glance (Ferrari 296 v7
   palette). Silver unless the user asks.
