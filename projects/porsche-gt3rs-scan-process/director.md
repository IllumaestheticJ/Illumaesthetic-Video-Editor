# Director shot plan - GT3 RS (992) scan-process reel, v2

Stage 2 after direction.md (scene order kept, nothing re-ordered). Times are on the measured kicks in project.yaml.
Part timings = explode keys in tools/shots.sh (fraction of render length) mapped onto the slot.
Total length and all cut points unchanged (cuts @ 3.80 7.63 11.42 14.14 15.13 18.81 22.55 26.38, dissolve 31.93).

## Shot table

| section | shot id | start-end (s) | focus | camera | part action (s) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole (IRL) | irl_headon | 0.00-3.80 | the yellow car on the lift, head-on | handheld, settles onto camA frame (4.500 s) | - | real car first; lands the 1:1 | footage |
| front | scan_headon | 3.80-7.63 | whole front as scan (wheels off like the car) | camA (16.65 mm), pull 0.12 ease-out, look-at 1.0,-0.45,0.6 | - ; HUD triangle count 24,999,999 (use a label, not the easing counter) | the 1:1 itself + "this is the data" | reuse s1 |
| front | xray_front | 7.63-11.42 | front aero kit: lip, grille trim, strakes, hood fins | x1a_start (head-on), pull 0.18 ease-in-out | lip down 7.83-9.19; grille trim down 7.94-9.39; strakes down 7.94-9.27; hood fins up 8.02-9.39; fender vent up 8.02-9.39, z-180 spin 9.50-11.24 | 4 front parts leave into black; same view continues the match (silver -> x-ray = new information) | reuse x1a |
| side (IRL) | irl_crew_scan | 11.42-14.14 | crew scanning the front-right arch | handheld pull back to camC frame (5.300 s) | - | shows the process; carries the drop | footage |
| side | scan_side | 14.14-15.13 | right side, empty front arch | camC static | - | 1:1 #2 on the drop | reuse s2 |
| side | xray_side | 15.13-18.81 | the two right-side vents and their mounting backs | camC, pull 0.25, look-at -0.4,-0.9,0.8 | intake 1 up 15.36-16.69, z180 spin 16.80-18.62; fender vent up 15.50-16.80, z-180 spin 16.91-18.62 | both parts have useful backsides (clips/mounting); spin allowed per user rule | reuse xs2 |
| process (IRL) | irl_scanner | 18.81-22.55 | the live scan on the handheld screen | handheld | - | the only shot of the data being captured; bridges the turn to the rear | footage |
| rear | xray_rear | 22.55-26.38 | rear aero: diffuser, diffuser trim, rear strake, skirt, skirt strake, left intake (wing in frame) | x2 rear-left 3/4, orbit -12 deg | diffuser down 22.74-24.16; trim down 22.86-24.27; rear strake down-left 22.86-24.27, z180 spin 24.27-26.19; skirt down 22.93-24.27; skirt strake up 22.93-24.27, spin 24.39-26.19; intake 2 up 23.01-24.39, spin 24.46-26.19 | richest region (6 parts), parts below/above in clear background | reuse x2b |
| whole | xray_reassembly | 26.38-32.43 | all 14 pieces returning home | x3_start -> orbit 30 deg onto cam_listing, look-at 0,0,0.6 | lip, grille, wheels home by 27.32; strakes + hood fins 27.72; fender vent + intake 1 28.25; diffuser + trim 29.14; rear strake + skirt 29.52; skirt strake + intake 2 30.13; morph to listing grey 30.73-31.68 | payoff on the dense kicks; ends on the listing angle | reuse x3 (when finished) |
| end | website | 31.93-38.40 | listing, title, logo, URL | webzoom | - | product + where to buy | reuse |

Add to project.yaml as `focus:` on each clip: irl_headon "car on lift", scan_headon "front scan", xray_front "front aero parts",
irl_crew_scan "crew scanning front-right arch", scan_side "right side scan", xray_side "fender vent + quarter intake",
irl_scanner "live scan screen", xray_rear "rear aero parts", xray_reassembly "all parts home", website "listing".

## Cut list
Nothing is removed from v1/v2. Checked and kept:
- "Repeated views" in director_report.md (scan_headon~xray_front, scan_side~xray_side, xray_reassembly~website) are
  deliberate: the matched shot keeps going on the same camera (style guide) and the reassembly ends on the listing angle
  to dissolve into it (lessons, 240SX v3). Each pair changes look/state, so no frame repeats information.
- Fender vent appears in x1a and xs2 (two angles, both spin). Kept for v2; see the optional re-render below.

## Hold list (> 0.75 s)
| shot | hold | reason |
|---|---|---|
| scan_headon | ~0.8 s near-static at the end of the ease-out pull | the HUD triangle count reads; the x-ray switch lands on 7.63 |
| scan_side | 0.93 s static | the 1:1 on the drop must sit still to read as the same car; x-ray switch on the next kick 15.13 |
| website | 1.5 s at the end | logo + ILLUMAESTHETIC.COM read time, music fade |

## Render budget
- Frames to render at 15 fps: **0**. Reused unchanged: s1 (58), x1a (58), s2 (16), xs2 (57), x2b (60), x3 (93, finishing).
- Before assembly: per-frame mean-luma scan of x3 (Cycles black-frame lesson) and a look at its last frame vs the listing.
- Optional, only if the user flags the duplicate fender vent or the small intake: re-render xs2 (57 frames, ~1 job) with
  `M="rear_qpanel_intake_1"` (fender vent stays home via `rest`), same camC start (required by 1:1 #2), `--move pull` reduced
  to ~0.10 so the car stays larger, and a larger intake offset re-checked with tools/explode_check.py so it ends in clear
  background above the rear quarter at >= 10 % of frame width. Keep the z180 spin (useful backside).
