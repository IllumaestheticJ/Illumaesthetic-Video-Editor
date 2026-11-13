# Direction v3 - Toyota MR2 Spyder scan-process reel ("around the hardtop")

Scene director, 2026-11-13. Replaces v2 (summary at the bottom; full text in git history).
Read: CLAUDE.md, knowledge/lessons.md (all 922 lines), style-guide.md, clips.md (incl. the post-v2 audit), project.yaml,
editlog.jsonl, feedback.jsonl, match/*.json. Looked at: DJI_0030 at 1 s and 0.5 s steps, FX30636 12-36 s (graded),
LRF proxies m0034 / m0035 / e0044 / e0046, the existing irlH clip, first/mid/last of sA3 / sB / sX, the registration
stills v3a_* / v3b_*, v3a_on/only_ht_rear, v3a_on/only_ht_full, frameB. Music accents re-measured (section 3).

Feedback driving v3: "this is a mess, is there more MR2 scanning footage that can involve more of the car and the other
scans this car has?" then "go ahead with v3 built around the hardtop: more of the scanner clip, 1:1 cuts to the scans from
this shoot, trim-removal / hardtop-fit footage as the action, full car as context".

## 1. Feature inventory

Signature feature of THIS car at THIS shoot: the 3D-printed hardtop being test-fitted and scanned. Everything else is context.
The real car also has a scooped hood and a black rear wing; **no scan has either**.

| scan (prepped .blend, Top Down frame) | registration | what it shows (looked at) | verdict |
|---|---|---|---|
| topdown (Full Car Top Down) | base frame | whole car, roof off, roll hoop, closed louvred lid, stock hood, no wing; holes in front intake slit + lower rear grille | base for every scan shot |
| htrev1 (Print Evaluation/Mr2 hardtop revision 1, Jul 16 2025 = this shoot) | FPFH+ICP 39 % within 6 mm, 3.6 mm rms; red-over-car good | printed hardtop piece on the car + hoop, deck, louvres; ragged islands at its capture edge | use via `ht_rear` only |
| **ht_rear** (carved from htrev1, 153k tris) | seats on topdown; matches the 56.0 s frame from camB (coordinator check) | the printed piece: rear-window frame + legs on the deck, rails forward to the header (bbox y -1.03..0.20, z 0.83..1.16). **Outer/top side only - underside not scanned** | hero part. Translate only, never show its underside |
| fullcar (Full Car.stl, May 2025) | same Artec frame | the car WITH a complete smooth hardtop | end state; matches the listing hero (hardtop on) |
| **ht_full** (carved from fullcar, 258k tris) | seats cleanly on topdown (coordinator check) | complete hardtop shell, outer side | lands on the car in the last scan shot |
| roofedge (Roof Front Edge) | **false fit - landed on the hood** (coordinator correction) | - | unregistered, not used. No roof-edge / latch beat |
| latchref / latchunder | 25 % / 7 % within 6 mm, fragments | patches around header / A-pillar / cabin | not used (ragged at every framing, STI v3 lesson) |
| lid_open / rear_open_nolid (2024) | 3.2 mm rms | engine lid open | registered but **cut from v3**: not part of the hardtop story, it was half of the v2 "mess" |
| front-bumper-removed (2024), trim removed, trunk-open cover, quarter panel, Handle | do not register / not registered | - | unavailable. No state implied from them (rule D) |

Footage (all viewed):

| source | what | verdict |
|---|---|---|
| DJI_0030 28-30 s | wide: whole car front-left 3/4, crew walks to the rear with the scanner, printed piece on the car | opener (context in IRL) |
| DJI_0030 44.5-46 s | scanner screen with the live scan in the foreground, piece behind it | scanner detail |
| DJI_0030 47-50 s | scanner sweeping over the piece from above-rear (taped print sections visible) | scanner detail |
| DJI_0030 53.9-56.0 s | pull-back to the full rear, ends on the solved frame (camB) | existing clip irlB, cut B |
| DJI_0030 70-80 s | front / windscreen, 74.0 s solved (camA) | **not used** - see "cut A" below |
| FX30636 20.9-24 s | two crew lift the piece off and carry it away | existing clip irlH, the real action |
| FX30636 ~26-34 s | piece set down on the floor, underside up | new excerpt (the side the scan does not have) |
| m0035 (LRF only) ~16-50 s | hands pressing the piece's leg onto the rear deck = hardtop FIT | worth fetching (smallest relevant clip); optional upgrade, see open question 2 |
| m0034 (LRF only) 158-240 s | complete printed hardtop on the car, crew inside pushing it up | best match for the "hardtop on" scan but 475 s of 4K; optional |
| e0044-47 trim removal | door-sill / interior trim coming off | not used: its scan (Rear Interior Trim Removed) is unregistered, so the action has no scan to land on |

Region richness:

| region | states | parts | signature | quality | score |
|---|---|---|---|---|---|
| top / hardtop (over hoop + rear deck) | roof off (topdown), printed piece on (htrev1), full hardtop on (fullcar) | ht_rear, ht_full | the printed hardtop, shoot-day scan | good; piece underside unscanned | **richest - gets the drop, 3 of 3 scan shots** |
| rear | closed (+ 2024 lid open, cut) | - | louvres; wing missing | good | medium - seen in the 1:1 frame only |
| whole car | hardtop on / off | - | - | good | context: one wide, the last scan shot |
| front | closed only | none | stock hood != real scooped hood | holes | weak - no scan shot |
| side, wheels, interior, bay | none usable | none | - | - | none |

## 2. Scene order v3

One section (hardtop over the rear deck) told once, IRL and scan alternating on the same subject, then one whole-car wide
that ends on the listing. Camera position travels one way: rear (camB) -> rear-high -> rear-right 3/4 -> listing pose.
Video starts at track beat n21; frames at 30 fps from the grid (snap each cut to its measured onset, section 3).

| # | scene | scans / source | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | irl_wide | DJI_0030 28.5-29.6 s | whole car + crew with scanner + printed piece | "full car as context" comes from real footage, in motion from frame 1; shows the signature piece on the car before any close-up | 2 (n21-23) | native portrait, full frame |
| 2 | irl_screen | DJI_0030 44.5-45.6 s | scanner screen, live scan of the piece | the scanning itself; closest look at the tool | 2 (n23-25) | native portrait |
| 3 | irl_rear | DJI_0030 53.9-56.0 s (existing irlB) | scanner on the piece, pull-back to full rear | ends ON the solved frame | 4 (n25-29) | reuse as-is |
| 4 | **scan_piece (sP)** - 1:1 cut B on the drop | topdown + ht_rear | the printed piece as scanned at this shoot, seated on hoop + deck | richest region lands on the drop (n29 = biggest level jump). The 1:1 now goes to the shoot-day scan (v2 cut to the bare car, so the piece vanished) | 8 (n29-37) | starts on camB, cranes up and in until the piece fills the frame; label |
| 5 | irl_over | DJI_0030 47.5-49.6 s | scanner passing over the piece from above | same subject, same high angle as sP's end pose; more of the scanner clip | 4 (n37-41) | native portrait |
| 6 | irl_lift | FX30636 20.9-23.0 s (existing irlH, first 64 frames) | crew lift the piece off the car | the physical removal that licenses the next scan shot | 4 (n41-45) | reuse (3:4 on blurred fill) |
| 7 | **scan_off (sL)** | topdown + ht_rear | piece rising clear; roll hoop + rear deck it sits on | continues the lift across the cut on the strongest kick (n45). Part was physically removed (scene 6); state under it is real (topdown) | 4 (n45-49) | rear-right 3/4, low enough that the piece rises into black, high enough that its unscanned underside never faces the lens; label |
| 8 | irl_down | FX30636 ~27.5-29.6 s | piece set on the floor, printed underside up | completes the removal; shows in real footage the side the scan lacks | 4 (n49-53) | same grade + 3:4 treatment as irlH. Slot for m0035 / m0034 if fetched |
| 9 | **scan_on (sH)** | topdown + ht_full | full hardtop lowers onto the car, lands on n57; pull out to the whole car on the listing angle | the other hardtop state this car has (Full Car scan); whole car shown once, wide, fully in frame; ends where the listing begins, now with matching roof | 9 (n53-62) | high rear-right, whole car in frame from first frame; ends on cam_listing_v; clay morph; label |
| 10 | website | listing still (existing webzoom_mr2_v2.mp4) | listing with hardtop, title, logo, URL | dissolve completes on the last big hit (n62) | 5 (n62-67) | reuse as-is |

Sections: 1-8 = top/hardtop piece (one continuous sequence), 9 = whole car, 10 = end card. No section returns.

Left out and why:
- **Cut A (front 1:1, 74.0 s) is dropped.** (a) The frame's lower half is the scooped hood and the only front scan has a stock
  hood, so the centre of the frame changes at the cut - not 1:1 (v2 review already listed it; a Kouki splice was tried and
  broke alignment, editlog 2026-11-11). (b) The piece is on the car at 74 s, so the clip cannot follow the lift-off. (c) The
  front has no scan from this shoot. The whole car is still shown: scene 1 (real) and scene 9 (scan).
  If the coordinator wants it back, the only clean place is a prepend: start at n13, irlA last 64 frames (n13-17), then a
  topdown + ht_rear pull-back from camA (n17-21, 35 frames at 15 fps), everything else +128 frames, total 29.1 s.
- Engine-lid open / lid explode, x-ray reassembly: not hardtop story; nothing is reassembled in v3.
- Roof front edge / latch detail: no registered scan (coordinator correction).
- Trim removal: footage exists, its scan does not register.
- Triangle-count labels: banned (lessons 2026-11-13).

## 3. Music map

Track /home/user/media/mr2/music/mr2_track.mp3, grid t = 0.5145 + 0.53535 n. Re-measured 35-120 Hz rise per beat: kicks
sit on n = 1 mod 4 (n13 29, n21 18, n25 17, **n29 26 + level jump = drop**, n33 14, n37 21, n41 17, **n45 46 strongest**,
n49 19, n53 14, n57 21), last big hit **n62 (33.71 s, 43)**, decay to silence by n67-68. n23 has no kick on the grid
(v2 found the real transient ~100 ms late) - measure it. Low-band peak offsets vs grid ranged -20..+60 ms (n29 about +58 ms):
plan on the grid, cut on measured onsets.

| scene | starts on | track s | video s | frame |
|---|---|---|---|---|
| irl_wide | n21 kick | 11.757 | 0.000 | 0 |
| irl_screen | n23 (measure) | 12.828 | 1.071 | 32 |
| irl_rear | n25 kick | 13.898 | 2.141 | 64 |
| sP, cut B | **n29 drop** | 16.040 | 4.283 | 128 |
| irl_over | n37 kick | 20.322 | 8.566 | 257 |
| irl_lift | n41 kick | 22.464 | 10.707 | 321 |
| sL | **n45 strongest kick** | 24.605 | 12.848 | 385 |
| irl_down | n49 kick | 26.747 | 14.990 | 450 |
| sH | n53 kick (hardtop lands n57, frame 578) | 28.888 | 17.131 | 514 |
| website | dissolve 643 -> 658, complete on n62 | 33.706 | 21.949 | 658 |
| end | n67 + tail | 36.383 | 24.626 | 739 |

Total about 24.6 s. First 1:1 at 4.28 s (v2: 3.2 s) - the price of three scanner excerpts before the drop.

## 4. Diff against v2

| v2 scene | v3 | why |
|---|---|---|
| irl_scan_front + scan_front (sA3) | dropped | cut A, see above |
| irl_hardtop | kept, moved after the scan of the piece, trimmed to 64 frames | it now answers a scan shot instead of floating between two unrelated cuts |
| irl_scan_rear | kept, moved to before the drop | reuse as-is |
| scan_rear (sB) | replaced by sP | sB had no hardtop piece, footage frame has it |
| scan_lid (sC2), scan_xray (sX) | dropped | not hardtop; sX ended on a roof that did not match the listing |
| website | kept | reuse as-is |
| - | added irl_wide, irl_screen, irl_over (DJI_0030), irl_down (FX30636) | more of the scanner clip; the removal completed |
| - | added sL, sH | the two hardtop states this car has |

Reuse as-is: irlB_0030_1293-1343.mp4, irlH_FX30636_20.9_wide.mp4 (first 64 frames), webzoom_mr2_v2.mp4, camB.json,
cam_listing_v.json, the LUT, the music. New renders: sP, sL, sH. New IRL cuts: 3 from DJI_0030, 1 from FX30636.
Not reused: sA3, sB, sC2, sX, irlA, hud_mr2_v2.

## 5. Open questions (not guessed)

1. **Is lifting the carved piece acceptable?** Lesson (GT3 RS reviewer): a part comes off only if it was physically removed
   AND scanned in that state. Here: removed on camera (FX30636), car scanned with it (htrev1) and without it (topdown), but
   there is no loose scan of the piece - ht_rear is a difference of two scans, top side only. sL is planned as a short
   translate that never shows the underside. If a preview of ht_rear alone from the sL camera shows ragged edges or
   see-through holes, do the fallback in director.md (hard state swap on the kick, no floating part).
2. What is the hardtop in Full Car.stl (May 2025, before the print)? OEM top used as reference, or an earlier version?
   The label says only HARDTOP ON / FULL CAR SCAN until someone confirms.
3. m0035 (hands seating the piece on the deck) is the hardtop-fit footage the user named. Fetch it if a download is cheap;
   it replaces irl_down with no re-timing. m0034 158-240 s (complete printed hardtop on the car) is the better lead-in to sH
   but is a 475 s 4K file.
4. The IRL rear frame shows the real licence plate legibly (same clip v2 shipped). Lessons cover scanned plates only; flagging.
5. The real wing and the scooped hood are in no scan; the wing disappears at cut B. Unavoidable with this data.

## v2 (superseded)

v2 (2026-11-11): irl_scan_front -> cut A (sA3, topdown) -> irl_hardtop -> irl_scan_rear -> cut B (sB, topdown without the
hardtop piece) -> engine-lid open/explode (sC2, 2024 rear-end scan) -> x-ray reassembly to the listing pose (sX) -> website.
Reviewer: "this is a mess". It matched the scanning footage to 2024-25 full-car scans rather than the scans made at the
shoot, jumped front -> top -> rear, and ended on a roofless car dissolving into a listing with a hardtop.
