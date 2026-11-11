# Infiniti G35 coupe - scene direction (v2)

Stage 1 of `.claude/agents/scene-director.md`, 2026-11-11. Inputs: lessons.md (all), style-guide.md, workflow.md
"Scene direction", clips.md, project.yaml, editlog.jsonl, `shots.py`, contact sheets `/home/user/media/work/g35/reg/final_*.jpg`,
`preview_wide.jpg`, `preview_s6.jpg`, new wide previews (`renders/preview/{s1_turntable,s2_rear}` f1/mid/last), ortho
renders `reg/ortho_rear.png`, `reg/ortho_sideR.png`, and `ive director` on the v1 timeline (report in the scratchpad, not committed).
No `feedback.jsonl` exists for this project yet. The V2 brief from the parent ("All V1 videos need the same updates") overrides the
earlier constraints where they conflict: order from scan features, travel front -> side -> rear, section focus, no redundant
views, whole car in the opening, no implied data, short ending with fade + small logo, no text.

## Step 1 - feature inventory

### Scan files
| Scan | What it shows (looked at) | Usable as |
|---|---|---|
| Coupe full car, car4 (4 mm) / car25 (2.5 mm) | Whole closed coupe: aftermarket spoiler, aftermarket mesh-spoke front wheels, 5-spoke rear wheels, dual round exhaust tips (x ~ +/-0.45 m, z ~0.36 m), headlamps, door/mirror, fuel door, roof/fastback. | Every shot in v2 |
| G35 Trunk (part, 5M tris) | **Outer skin only** of the lid, scanned without the spoiler. Median 4.3 mm to the car, 53 % overlap (more than the ~3 mm "registered" threshold; the residual is explained by the spoiler band). | **Not used.** Lifting it off shows a hollow trunk: car-shell back faces and a black void (seen in `preview_s6.jpg` f31-f62). There is no trunk-open scan. |
| Panels cut from the full car (hood, front/rear bumper covers, doors+mirrors, spoiler) | Carved along seams from the CLOSED car (`segment.py`). Nothing was scanned behind them. | **Not used.** In `final_s8_explode.jpg` f12-f89 the lifted doors leave empty openings and the hood/bumpers leave ragged voids: that implies data that does not exist (V2 rule 6, honda-s2000 + honda-civic-11 rules). |
| SFP Aero G35 (partial re-scan, 3.1 mm) | Same body, roof/hood/trunk missing, other wheels | Not used (adds no panel or state) |
| Sedan bumpers / sedan SFP states | Another body; do not register (fitness 0.04-0.11) | Not used |

States: **none** (no open/removed scan of this car). Registered separate parts: **none that pass the rule** (trunk lid is outer skin
only and opening it reveals nothing scanned). So the reveal ladder has **no states rung and no explode rung**.

### Weak data (keep every frame off these)
| Where | Problem | Seen in |
|---|---|---|
| Front grille / lower intakes | Open holes with ragged engine-bay bits behind | `final_s4_lamp.jpg` f19-f47, `final_s7_top.jpg` f1-f13 |
| Tail lamp lenses | Dark lens holes | `final_s5_tail.jpg` all frames |
| Tyre contact patches (front and rear) | Speckle / ragged shreds below ~z 0.30 m | `final_s3_wheel.jpg` all frames, `ortho_sideR.png` |
| Rear 5-spoke rims | Partly uncaptured dark faces | `ortho_sideR.png` |
| Right door glass | Black hole at about y 0.0, z 1.29-1.37 m | `ortho_sideR.png` |
| Underbody at the rear corners | Shreds at x ~ +/-0.85, z 0.17-0.30 | `ortho_rear.png` |
| Plates | Flattened (deplate) - blank slabs, no detail | `final_s4_lamp.jpg`, `final_s5_tail.jpg` |
| Engine bay, interior, trunk interior | Not scanned | - |

### Region richness (states + parts + signature features + quality)
| Region | Signature features | States / parts | Quality | Score |
|---|---|---|---|---|
| Front | aftermarket mesh-spoke wheel (best detail on the car), headlamp | none | grille + intake holes, tyre speckle | 2 |
| Side (right) | mirror, door shut line + handle, fuel door, rear quarter | none | door-glass hole (avoidable) | 1 |
| Rear | aftermarket spoiler (the car's mod), dual exhaust tips, emblem | none usable | lamp-lens holes, plate slab | 2 |
| Top | fastback planform, roof | none | clean | 1 |
| Engine bay / interior / trunk | - | none | not scanned | 0 |

## Step 2 - scene order (from the inventory)

- **Opener: front, whole car.** Front and rear tie on features; the front carries the mesh wheels, which read even at whole-car size
  (the spoiler is a thin line at that size, see `preview_wide.jpg`), and the V2 travel order is front -> side -> rear. Re-rendered
  wide `s1_turntable` shows the whole car with motion from frame 1.
- **Travel once around the right side:** front (lamp, wheel) -> side (mirror -> door -> rear quarter) -> rear (exhaust, spoiler)
  -> rise over the top -> fade. No ping-pong, every close-up next to its region.
- **Biggest musical moment (26.697 climax entry) = start of the rear section**, the region with the car's mod (spoiler).
  There is no richer region: with no states/parts the climax carries the signature feature, not an explode.
- **Dropped rungs:** trunk open (s6) and exploded view (s8): no data behind the panels. The brief's ladder asked for both; the
  data rule wins (V2 rule 6, lessons honda-s2000 "Rear trunk data is made-up", GT3RS/honda-civic-11 "don't show a part coming off
  unless ... a separate scan of it in that state").
- **Dropped for redundancy:** `s2_rear` (rear-left whole-car 3/4): `ive director` measured s1 ~ s2 IoU 0.86 / corr 0.90 ("same
  view shown twice"); one whole-car 3/4 is enough. `s4_lamp`/`s5_tail` (IoU 0.93 to each other, both sit on weak data) and
  `s3_wheel` (contact-patch speckle in every frame) are replaced by re-framed close-ups.
- **Length:** 32 beats of non-redundant scan content exist; 38 s would need repeats. Music starts later at a measured kick
  (13.363 s) so the track's ending/logo timing is kept and the reel is 24.63 s.

### Scene list
| # | section | scene | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | whole (front 3/4) | s1_turntable (reuse, new wide render) | car4 | whole car, front-right 3/4, mesh wheels | V2 rule 4 + strongest front feature; motion from frame 1 | 4 | first 80 frames only (the render's last ~2.8 s is near-static) |
| 2 | front | g1_lamp (NEW) | car25 | right headlamp | front detail, framed outboard so grille/intakes/plate stay out | 4 | slow arc 60 -> 45 deg off the nose, 65 mm |
| 3 | front (wheel) | g2_wheel (NEW) | car25 | front-right mesh-spoke wheel + arch lip | best-captured detail on the car; framed above the tyre contact speckle | 4 | slide forward along the rim, 60 mm |
| 4 | side | g3_side (NEW) | car25 | mirror -> door line/handle -> fuel door + rear quarter | the side section; path dips below the door-glass hole | 8 | parallel track rear-ward, 55 mm |
| 5 | rear | g4_exhaust (NEW) | car25 | right exhaust tip in the bumper | rear section opens low on the climax entry | 4 | low push, 70 mm, plate + rear-corner shreds out of frame |
| 6 | rear | g5_spoiler (NEW) | car25 | aftermarket spoiler on the trunk lid | the car's mod = the rear's signature, rising toward the top shot | 4 | high rising arc from rear-right to centre, 40 mm |
| 7 | top | s7_top (reuse, trimmed) | car4 | fastback planform, ends straight top-down | top rung; continues the rise of g5; fade to black on its last 12 frames | 4 | in 41 (skips the grille-hole frames) |
| 8 | end | logo (re-made card) | - | ILLUMAESTHETIC, small | Temerario ending | 3.3 s | logo 380 px wide |

Each section appears in ONE continuous run: whole -> front (lamp, front wheel) -> side -> rear (exhaust, spoiler) -> top -> logo.
The front wheel is the only wheel shot (it belongs to the front run); the rear wheel only passes the bottom edge of g3's last frames and
is not a focus. No section is revisited.

**No state shots (V2 addendum C/D):** no bumper-removed hero beat - the coupe has no bumper-removed scan (the sedan bumper scans are a
different body and do not register, fitness 0.04-0.11). No trunk, hood or door opening - no registered open-state scan of this car exists,
and animating the closed scan's carved panels would fake it. So: no trunk shot, no explode.

## Music map
Track: `/home/user/media/work/music/infiniti-g35_track.mp3`, 90 BPM, beat 0.6667 s, bar kicks at 0.03 + k*2.6667 s, climax kicks
every half bar from 26.70. **Music start = 13.363 s** (measured bar kick k=5). Video time v = track - 13.363. All cuts land on
measured kicks (editlog: ... 13.37 / 16.03 / 18.70 / 21.37 / 24.03 / 26.70 / 28.04 / 29.37 / 32.03 / 33.37 / 34.70).

| scene | track in-out (s) | video in-out (s) | cut frame @30 | frames |
|---|---|---|---|---|
| s1_turntable | 13.363 - 16.030 | 0.000 - 2.667 | 0 | 80 |
| g1_lamp | 16.030 - 18.697 | 2.667 - 5.333 | 80 | 80 |
| g2_wheel | 18.697 - 21.370 | 5.333 - 8.000 | 160 | 80 |
| g3_side | 21.370 - 26.697 | 8.000 - 13.333 | 240 | 160 |
| g4_exhaust | 26.697 - 29.370 | 13.333 - 16.000 | 400 | 80 |
| g5_spoiler | 29.370 - 32.030 | 16.000 - 18.667 | 480 | 80 |
| s7_top (+fade 628-640) | 32.030 - 34.697 | 18.667 - 21.333 | 560 | 80 |
| logo | 34.697 - 38.000 | 21.333 - 24.633 | 640 | 99 |
Total 739 frames = 24.63 s; music 13.363 -> 37.997 (track silent at 38.3). Short audio fade-in (~3 frames) at the music start to
avoid a click; keep `fade_out: 0.3`. Verify each cut against kick peaks of the decoded delivered audio (V2 rule 9).

## Diff against v1 (project.yaml timeline)
| v1 | v2 | why |
|---|---|---|
| s1_turntable 5.33 s | kept, trimmed to first 2.67 s | whole car + motion; v1 report: 2.8 s dead at its end |
| s2_rear 5.33 s | **dropped** | same view as s1 (IoU 0.86); rear section now told in close-ups |
| s3_wheel | **replaced** by g2_wheel | contact-patch speckle in every frame |
| s4_lamp | **replaced** by g1_lamp | grille hole grows to a third of the frame |
| s5_tail | **replaced** by g4_exhaust + g5_spoiler | lamp-lens holes; s4~s5 IoU 0.93 |
| s6_trunk | **dropped** | opens onto a void: no trunk-open scan |
| s7_top 4 s | kept, 2.67 s from frame 41 | top rung; skips grille-hole frames |
| s8_explode 8 s | **dropped** | panels carved from the closed car leave empty openings; no part/state scans |
| logo 860 px | **re-made at 380 px** (`logo_card.py --width 380 --secs 3.3`) | V2 rule 7: small logo (~35 % of width) |
| 38.0 s, music from 0 | 24.63 s, music from 13.363 | 32 beats of non-redundant scan content |

Reuse as-is: `renders/final/s1_turntable` (the new wide render) and `renders/final/s7_top`. New renders: g1-g5 (see director.md).
**The running re-render loop (s2_rear now, s6_trunk queued) is not used by this plan** - stopping it saves ~35 min of CPU.

## Open questions for the editor / user
1. The brief asked for a trunk-open and an exploded view. Both are dropped because the data behind the panels does not exist.
   If the user still wants an explode, it needs real removed-state or panel-inside scans of this car - confirm with the user, don't fake it.
2. The trunk part scan registers at 4.3 mm median / 53 % overlap: is it the same lid (spoiler removed) or a replacement lid? Irrelevant
   for v2 but should be recorded before any future use.
3. The ortho renders in `reg/` (`ortho_rear.png`) predate deplate and show a legible plate - don't use them in any deliverable.

## Review 2026-11-11 (after v2 renders)
Looked at first/mid/last sheets of every shot and +-1 frame around every cut. Each scene shows its cast feature;
no state implied without a scan; travel reads front -> side -> rear -> top. Sections: s1 whole | g1, g2 front | g3 side |
g4, g5 rear | s7 top | logo end. `ive director` flags g1~g3 and g3~g4 by silhouette IoU only (frame-filling
close-ups) - different subjects, kept. No re-order requested.
