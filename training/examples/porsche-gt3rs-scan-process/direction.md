# Direction - Porsche 911 GT3 RS (992) scan-process reel, v2

Scene director, 2026-11-11. Inputs: clips.md, project.yaml (v1 timeline, measured kicks), editlog.jsonl, feedback.jsonl,
tools/shots.sh, contact sheets of every v2 render (`/home/user/media/work/gt3rs/renders/{s1,x1a,s2,xs2,x2b,x3}`, sheets in
`/tmp/claude-0/sd/`), `python -m ive director` report (director_report.md). x3 was still rendering (57/93 frames) when sheeted.

**Verdict: keep the v1 order. Every scene's content and position already follows the scan inventory; v2 reuses all six
renders unchanged. No re-render is needed for the order.** The user's notes on this reel ("This is good", spin only
useful backsides, check framing, parts into clear background) are already in the v2 renders and are not touched.

## 1. Feature inventory

Full car: Artec, 24,999,999 tris (STL header), prepped at 3 mm; front wheels removed for every post-cut shot (car is on the
lift with them off), returned as parts in the reassembly. Frame: +x front, centre y = -0.45, right side = -y.
All 12 part scans overlay the car (overlay render, editlog 06:50). No state scans (no hood-open, no bumper-off), no GT3 RS exhaust.

| region | signature features (seen in renders) | parts (registered) | states | weak data | richness |
|---|---|---|---|---|---|
| Front | hood vent louvres, wide front intake, DRL headlights, lip | front_lower_lip, front_grille_trim, front_bumper_strake (pair), hood_vent_fins_x3 = **4** | none | x-ray head-on is busy (scanned cabin shows through); hood fins are small in a head-on frame | 4 parts + signature hood vents -> **2nd** |
| Right side | front-fender louvre vent, rear-quarter intake, mirror, swan-neck wing tip, rear wheel | fender_vent, rear_qpanel_intake_1 = **2** (both with useful backsides: clips / mounting) | none (front arch empty = wheel off, real) | open front arch is a hole by design (car on lift) | 2 parts -> short scene |
| Rear / left | swan-neck wing + DRS, diffuser, rear-quarter intake, skirt | rear_diffuser_1, rear_diffuser_trim_outer, rear_bumper_strake (L), side_skirt_upper (L), side_skirt_strake (L), rear_qpanel_intake_2 (L) = **6** | none | rear plate area not close-framed (no plate issue seen at this size) | 6 parts + wing -> **richest** |
| Top / engine / interior | - | - | none | no engine-bay or open-lid scan | no scene |
| Wheels | rear wheels on the scan; front wheels as parts | wheel_FR, wheel_FL (cut from the full car) | wheel-off = real lift state | dark rims not inspected close | reassembly only |

Not shown / not claimed: Drive's rear bumper, diffuser-2, inner trims, lower skirt, hood vent interfaces, underbody/DRS,
door handles, gas cap (not prepped). No exhaust.

## 2. Scene order (from the inventory)

Fixed anchors (footage + two solved 1:1 cameras, user-approved): IRL head-on -> 1:1 @3.80 (camA) ... IRL crew @11.42 ->
1:1 @14.14 drop (camC) ... reassembly to the listing angle -> dissolve @31.93.

| # | scene | scans used | feature shown | why here (inventory) | beats (128 BPM, 1 bar = 1.875 s) | camera note |
|---|---|---|---|---|---|---|
| 1 | irl_headon | v_0130_125744 0.77-4.53 | real car on the lift, head-on | fixed opener; ends on the solved frame | 3.80 s (2 bars) | handheld settles; no text |
| 2 | scan_headon (s1) | car_noFW | whole front, silver; front wheels off like the real car | 1:1 #1 must start from camA; the front carries 4 parts + the hood vents (2nd-richest), so the reel opens on the aero end | 3.80-7.63 (2 bars) | camA, slow pull 0.12, ease-out; HUD triangle count |
| 3 | xray_front (x1a) | car_carved_noFW + lip, grille trim, strakes, hood fins, fender vent | front aero parts leave into clear background (down / up), fender vent spins (mounting back) | region's close detail sits next to its wide shot; same view = the matched shot keeps going | 7.63-11.42 (2 bars) | x1a_start (head-on), pull 0.18 |
| 4 | irl_crew_scan | v_0130_125720 2.63-5.33 | crew scanning the front-right arch, pull back to the right side | fixed; travel turns the front-right corner | 11.42-14.14 | ends on the solved frame (camC) |
| 5 | scan_side (s2) | car_noFW | right side, silver, empty front arch | 1:1 #2 must start from camC on the drop | 14.14-15.13 (hold, 1 s) | camC static |
| 6 | xray_side (xs2) | carved + fender vent, rear_qpanel_intake_1 | the two right-side parts lift up and spin (both backsides useful) | right side = 2-part region -> one short scene, 2 bars | 15.13-18.81 | camC, pull 0.25 |
| 7 | irl_scanner | v_0130_125732 0.2-3.97 | live scan on the handheld's screen | breather while the travel turns the rear corner; keeps x2b -> x3 adjacent (see diff) | 18.81-22.55 | IRL, no text |
| 8 | xray_rear (x2b) | carved + 6 rear/left parts | diffuser, trim, rear strake, skirt, skirt strake, left intake; wing in frame | **richest region** -> the last and longest explode before the payoff; leads straight into the reassembly with parts already out | 22.55-26.38 | rear-left 3/4, orbit -12 deg |
| 9 | xray_reassembly (x3) | carved + all 12 parts + both front wheels | everything translates home on the dense kicks | the biggest musical moment (dense 26.4-30.5) carries the richest action: all 14 pieces home | 26.38-32.43 (dissolve 31.93) | x3_start -> orbit 30 deg onto cam_listing, morph to listing grey |
| 10 | website | webzoom_gt3rs_v1.mp4 | listing, title, logo, URL | end card | 31.93-38.4 | - |

Travel: front (2-3) -> front-right corner IRL (4) -> right side (5-6) -> IRL insert while turning the rear corner (7) ->
rear-left (8) -> orbit to the listing angle (9). One direction around the car, no ping-pong.

## 3. Music map

| kick (s) | frame @30 | scene starting | note |
|---|---|---|---|
| 0.00 | 0 | irl_headon | music start |
| 3.80 | 114 | scan_headon | strongest onset = 1:1 #1 |
| 7.63 | 229 | xray_front | silver -> x-ray on the same view |
| 11.42 | 343 | irl_crew_scan | back to IRL |
| 14.14 | 424 | scan_side | drop = 1:1 #2 |
| 15.13 | 454 | xray_side | first kick after the drop: x-ray switch |
| 18.81 | 564 | irl_scanner | |
| 22.55 | 677 | xray_rear | |
| 26.38 | 791 | xray_reassembly | parts home on 27.32 27.72 28.25 29.14 29.52 30.13 (keyed in shots.sh x3) |
| 31.93 | 958 | website (dissolve 0.5) | |

## 4. Diff vs the v1 timeline

| change | why |
|---|---|
| **Order: none.** | Inventory-driven order = the existing order: opener on the aero front (fixed by 1:1 #1 anyway), one-way travel front -> right -> rear-left, richest region (rear/left, 6 parts) last before the reassembly, reassembly on the densest section. |
| Considered and rejected: move irl_scanner to 22.55 and x2b to 18.81 | would put the IRL insert between the rear explode and the reassembly; x2b ends with the rear parts out and x3 starts fully exploded - that continuity is worth more than an uninterrupted scan run. The insert at 18.81 sits where the travel turns the rear corner. |
| Considered and rejected: shorten s1 to 1 bar and slow x1a | the 1:1 landing + triangle HUD needs its 2 bars; slowing x1a by interpolation softens the explode. |
| Considered and rejected: other IRL clips (125414 underbody tilt-up, 125703, 125651) | 125414 needs a new solve and a new opener; 125703/125651 repeat the front-right arch already shown by 125720. No new information. |
| Content: v2 renders replace v1 (x1a, xs2, x2b, x3) | already done by the editor for the user's spin + clear-background notes. |
| Add `focus:` tags to every clip in project.yaml | director report: no focus tags (see director.md for the values). |

Render reuse: s1, s2, x1a, xs2, x2b reused as-is; x3 reused when its render finishes (check all 93 frames for luma
drop-outs and that frame 93 matches cam_listing). **Re-renders required: none.**

## 5. Open questions for the editor
1. The fender vent explodes and spins in both x1a (small, screen-left of the head-on) and xs2 (the hero of that shot).
   Acceptable as two angles on one part (front vs side), but it is the only repeated part action. If the user flags it,
   the fix is one xs2 re-render (57 frames) with the fender vent left home and the intake framed larger - spec in director.md.
2. In xs2 the rear-quarter intake ends small at the left edge (~5 % of frame width); its spin barely reads. Same re-render would fix it.
3. x3 was mid-render when reviewed: confirm frames 58-93 (morph to listing grey, end pose) before assembling.
