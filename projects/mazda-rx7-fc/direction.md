# Mazda RX-7 FC3S — scene direction v2 (scene-director, 2026-11-11)

Revision v1 -> v2. Inputs: lessons.md (all), style-guide, clips.md, project.yaml, editlog, sibling v1 feedback
(no rx7 feedback.jsonl yet; the standing "all v1 reels" notes apply), the user's v2 brief + addendum (relayed
2026-11-11), contact sheets of every render in `/home/user/media/work/rx7/renders/*` (12-24 frame tiles, read),
`ive director` report (`/tmp/rx7dir/director_report.md`), and my own checks of the scan files (below).
Shot-level camera / part / label numbers: `director.md`.

## 1. Feature inventory (from the scan files, not the model's spec sheet)

| region | scans (all registered at identity, 1.1-2.9 mm median) | what the data really shows (checked) | weak data | score |
|---|---|---|---|---|
| **Front / nose** | full car (fr_2mm close-up crop), **Front Face** part (face_clean, 0.50 M tris after prep), **Hood Off Bumper Off** (hobo) | Bumper part: outer AND **inner face scanned** (inward-facing area 0.58 m2 vs outward 0.64 m2; 93 % of 20 mm bins have an inner layer; splat `/tmp/rx7dir/face_back.png` shows the inside with the indicator/intake openings). Under it (hobo, ortho splat `/tmp/rx7dir/hobo_front.png`): **radiator support** (upper tie bar z~0.75, uprights), a full-width **lower beam at bumper height** (z~0.47-0.50, y up to 2.01) with end **brackets**, hoses/lines, a finned unit low on the car's left (not labelled: identity not certain). Pop-up headlight lids: **down in every scan** (dark recesses in s4). | pop-ups-up state does not exist | **5** (1 part + 1 state + signature lids) |
| **Hood / engine bay** | **Hood Up** (hup, propped 44.4 deg, hinge fit 2.6 mm), **Hood Off Bumper Off** (hobo), hood panel cut from the full car (hood_v2) | Hinge-opened hood lands on the captured Hood Up pose; engine bay is real Hood Off capture (s6 frames 33-60 show bay structure). Hood part is **outer skin only** (inward area 0.012 m2 of 1.67) -> translate, never flip. | prop rod only in hup | **4** (2 states) |
| **Rear** | **Rear Bumper Removed** (rbr), rear bumper cut from the full car (rbumper_v2) | Behind the bumper (ortho splat `/tmp/rx7dir/rbr_rear.png`): a full-width **crash beam** at z 0.48-0.67 with **four slotted mounting points** and end brackets; tank/spare shape below. Bumper part is **outer skin only** (inward 0.005 m2) -> translate only. Rear spoiler on the hatch is clean. | **tail-lamp lenses = holes**, **rear glass = hole**, **licence plate legible** just above the beam (z 0.72-0.88) | **3** (1 state) |
| Side | full car (fr_2mm) | right mirror, A-pillar, door shut lines, sill — clean 2 mm detail (s5) | window glass speckle on the mirror | 2 |
| Wheels | full car | upper tyre sidewall lettering, 4-spoke rim face, arch/suspension (s3 from frame 22 on) | **hub centre + lower rim speckled** | 1 |
| Top | full car | roof/hatch from above | **rear glass is a large hole** (dominates s7) | 0 -> cut |
| Interior | none | — | — | — (no scene) |

Composite checks (prep): `comp_explode` keeps every full-car cell of the rear end except 11 of 430 at ground level (the rbr crash
beam fills the bumper opening), and its front stops at y 2.01 m = the hobo radiator support -> **no blank space** under either
bumper. Fender tops are present on both sides (tri density left/right within 10 % of the full car; the see-through look of the
far fender in s8 f_0120 is the inner liner seen from above, not a hole). `comp_hood` = car minus hood with the real bay under it.
Not used: Hood Down Bumper Off (redundant with Front Face), FC3S 2025 full car (other session/frame). No hatch/trunk-open scan
exists -> **no hatch shot**. No pop-ups-up scan -> pop-ups are never shown raised.

## 2. Scene order (travel front -> side -> rear, each section once, then reassembly)

Richest region = front (Front Face part + Hood Up + Hood Off Bumper Off + signature lids) -> it opens the reel and owns the
whole drum section (9.07-21.52 s, the track's strongest snares, flux 1.0-1.14). The breakdown (21.52-33.41) carries the
travel down the side, the rear bumper section and the reassembly.

| # | scene | section covered | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | Opener | WHOLE car (front 3/4) | full car | whole car, pop-up nose leading | front = strongest feature end; addendum A: whole car with margins, motion from frame 1 | 8 | s1 frames 1-41 only (nose clips the edge from 2.93 s), reframed in post to 56-76 % width, 12 % margins |
| 2 | Nose | FRONT (on the car) | fr_2mm | pop-up lids (down), indicators, Front Face bumper on the car | close-up next to its wide; sets up the bumper that comes off in #5 | 8 | s4 full render, slowed |
| 3 | Hood opens | HOOD / ENGINE BAY | comp_hood + hood on fitted hinge | hood rises to the captured Hood Up angle, bay appears | real Hood Up state; drums enter 9.07 | 6 | s6 reused |
| 4 | Hood off | HOOD / ENGINE BAY (same sequence, seamless) | comp_hood + Hood Up panel | hood lifts off into black, camera moves over the engine bay | Hood Off capture exists; continuous with #3 (no visible cut at 12.46) | 7 | NEW, starts on s6's exact camera |
| 5 | Front bumper off | FRONT BUMPER REMOVED | comp_explode + Front Face | bumper slides toward camera, tips its scanned inner face up | Front Face inner face is scanned (93 % bins) -> flip justified | 4 | NEW, low-high front 3/4 |
| 6 | Behind the front bumper | FRONT BUMPER REMOVED (same section) | comp_explode (hobo) | radiator support, lower crash beam, brackets | hero beat (addendum C); held 2.8 s to read | 5 | NEW, push-in |
| 7 | Wheel | WHEELS | fr_2mm | tyre sidewall, rim face, arch | travel FR corner -> side; weak hubs -> short, speckled frames skipped | 3 | s3 window |
| 8 | Mirror | SIDE | fr_2mm | mirror, A-pillar, door | side has no states -> short | 2 | s5 window |
| 9 | Rear bumper off + crash beam | REAR BUMPER REMOVED | comp_explode (rbr) + rear bumper | bumper pulls back toward camera and down out of the way; push onto crash beam + mounting points | only rear state; skin-only part -> translate | 8 | NEW, rear-right 3/4 -> close |
| 10 | Reassembly | WHOLE car (high rear 3/4, different subject: parts returning) | comp_explode + 3 parts, car4 after lock | rear bumper, front bumper, hood fly home from their parked poses; lock on the 32.28 hit; fade | Temerario: progressive explode over several angles -> reassembly -> fade | 8 | NEW, car length runs up the 9:16 frame |
| 11 | Logo | — | logo card (rebuilt small, ~35 % width) | — | small logo after a fade (sibling v1 notes; v1 card is 82 % width) | 7 | not a Blender render |

The progressive explode is #4 (hood) -> #5/#6 (front bumper) -> #9 (rear bumper), each part off in its own section and its own
angle, parts staying off until #10 brings all three home. Nothing separates "all at once".

## 3. Music map (grid 9.067 + k*0.5661; per-beat flux measured: snares on odd k ~1.0, even k 0.6-0.9)

| cut (s) | frame @30 | k | flux | scene starting | note |
|---|---|---|---|---|---|
| 0.000 | 0 | — | — | 1 opener | soft intro |
| 4.533 | 136 | -8 | 0.35 | 2 nose | v1 cut, intro bar line |
| 9.067 | 272 | 0 | 0.85 | 3 hood opens | v1 cut, drums enter (hood moves 9.63 -> 11.90, on k1/k5 snares) |
| 12.463 | 374 | 6 | 0.83 | 4 hood off (seamless join) | v1 cut point kept as the render join; hood lifts on 13.03 (k7, 1.00) |
| 16.426 | 493 | 13 | 1.09 | 5 front bumper off | v1 cut (16.433) |
| 18.691 | 561 | 17 | 1.07 | 6 behind front bumper | v1 cut (18.7) |
| 21.521 | 646 | 22 | 0.86 | 7 wheel | v1 cut, breakdown (kick out) |
| 23.220 | 697 | 25 | 1.00 | 8 mirror | NEW cut (strong snare) |
| 24.352 | 731 | 27 | 1.07 | 9 rear bumper | NEW cut (strong snare); bumper pulls 25.48 (k29, 1.06) |
| 28.881 | 866 | 35 | 1.00 | 10 reassembly | NEW cut; hood locks on 32.277 (k41, v1 lock time) |
| 33.409 | 1002 | 43 | 1.01 | 11 logo | v1 cut kept |
| 37.400 | 1122 | — | — | end | total length kept |

Dropped v1 cut: 11.333 only (the hood sequence is held — Ferrari 296 rule: hold the section, don't cut away mid-action — and
the wheel moved to the side section). 12.463 stays as a render join with no visible jump. Added: 23.220, 24.352, 28.881, all
strong snares in the breakdown, for the side -> rear -> reassembly travel.

## 4. Diff against the v1 timeline

| v1 clip | v2 | why |
|---|---|---|
| s1_front34 0-4.5 | **reused**, frames 1-41 only, post reframe (scale 0.88) + slowed | v1 showed the nose clipped from 2.93 s (bbox x max 809/810); addendum A |
| s2_rear34 4.53-9.07 | **dropped** | `ive director`: same view as s1 (IoU 0.75, corr 0.81); the rear gets its own section in #9 |
| s3_wheel 9.07-11.33 | **reused**, moved to 21.52, window 1.47-3.17 s | side travel after the front; skips the speckled-hub opening frames |
| s4_nose 11.33-12.46 | **reused**, moved to 4.53, full render slowed to 4.53 s | front detail next to the front wide |
| s6_hood 12.46-16.43 | **reused**, moved to 9.07, 0-3.40 s | drums enter on the front's first state |
| s5_mirror 16.43-18.69 | **reused**, moved to 23.22, window 2.27-3.40 s | side section (cowl/glass speckle frames skipped) |
| s7_top 18.69-21.52 | **dropped** | rotating top-down (sibling note: wasted rotation) dominated by the rear-glass hole |
| s8_explode 21.52-33.41 | **dropped / replaced** | all parts out at once in one wide orbit (user v2 brief item 2); replaced by #4, #5, #6, #9, #10 |
| logo 33.41-37.4 | **rebuilt small** (~35 % width), same timing | v1 card is 82 % of the width |

Reuse: s1 (reframed), s3, s4, s5, s6 — all luma-checked frame by frame (no dark frames: worst step 1.7).
New renders: #4 s9_hoodoff, #5 s10_fbumper, #6 s11_fsupport, #9 s12_rbumper, #10 s13_reassemble (~290 frames, ~58 min serial).

## 5. Hood decision (addendum D)
Keep s6's move: it is the full car's own hood panel on the hinge fitted to the captured Hood Up scan (axis + 44.4 deg,
2.6 mm median), so the motion is the real rigid panel and its end pose is captured data, not an invented opening. From the join
at 12.463 s on, #4 uses the **captured Hood Up hood panel** (cut from hup.blend, see director.md) instead of the rotated closed
skin, so the hood the viewer sees lifted off is the scanned open hood; at 9:16 the 2.6 mm swap is sub-pixel. Lifting it off is
backed by the Hood Off Bumper Off capture. A pure "cut to the Hood Up scan" would show the prop rod and pop, and add nothing.

## 6. Open questions for the editor / user (not guessed)
1. Rear licence plate is legible in rbr (directly above the crash beam, in frame at the end of #9). Standing rule says plates
   stay unless asked (IS300 only) — confirm with the user, or deplate (subaru-sti-blobeye/tools/deplate.py) before rendering #9.
2. The finned unit low on the car's left behind the front bumper looks like a cooler but is not labelled; name it only if the
   team confirms what it is.
3. Tail-lamp lens holes sit at the top corners of #9's end frame; check the preview and lower `target` z by 0.05 if they read as
   black blotches.
