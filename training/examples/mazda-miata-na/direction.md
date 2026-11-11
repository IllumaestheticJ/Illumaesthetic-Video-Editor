# Mazda Miata NA - scene direction v2 (scene-director, 2026-11-11)

Inputs: clips.md, editlog.jsonl, feedback.jsonl, lessons.md, project.yaml (v2), tools/shots.py, director_report_v1.md,
v2 previews (`/home/user/media/work/miata/renders/preview/v2_sheet.jpg`, `v2b.jpg`, `s4_front_detail.jpg`,
`s5_trunk.jpg`, `s6_trunk_well.jpg`) - all looked at, not only named.

## Feature inventory (this car's registered data only)

| Region | States (registered) | Parts (registered) | Signature / exterior | Quality notes | Richness |
|---|---|---|---|---|---|
| Front | Front End Bumper Off (bumper off + hood propped; propped hood dropped by z<900 cut), Front End Hood Open (engine bay) | Front Bumper Only (outside + inside: tabs/ribs verified from behind) | pop-up lamp lids, bumper mouth | hood underside covers right 2/3 of lid -> camera on car's right (-X) | **3 (highest, tied)** |
| Rear | Trunk Closed / Half Open (37.5 deg) / Open (55.6 deg): lid underside + trunk well | none removable (Finish Panel = inner panel, unused) | round tail lamps, exhaust | plate flattened (ok); trunk well shows **see-through gaps** in the preview (weak floor data) | 3 states, 0 parts |
| Side | none | none | 6-spoke wheels, Toyo tyres, brakes behind the spokes, mirror, door line (full car only) | full car 4 mm, 2 mm crop exists for front-right quarter | 1 (exterior only) -> **short scene** |
| Top | none | none | hardtop, proportions | clean | used only for reassembly |
| Interior / underside | none | none | - | not scanned | **no scene** |

Hood and trunk lid were only opened, never removed: they swing on fitted hinges, never separate. Only the bumper comes off.

## Scene order (v2, revised)

Travel: whole car -> FRONT (right side) -> SIDE (right, rearward) -> REAR -> top reassembly -> logo. One direction, no ping-pong.

| # | scene | scans used | feature shown | why here | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | s1_reveal | car4 | whole car, front-right 3/4 | opener frames the end with the most data (front: part + 2 states); whole car, motion from frame 1 (v1 was cropped) | b0-8 | done; straight push |
| 2 | s2_bumper | comp_explode + fbumper_c | bumper lifts out, turns 135 deg to show its scanned inside | the only removed part; reviewer: "front bumper data first" | b8-16 | done |
| 3 | s3_hood | comp_explode + hood_full | hood opens on hinge over the real bumper-off front | Front End Bumper Off + Hood Open states; stays on the front | b16-24 | rendering; keep |
| 4 | s4_front_detail | comp_explode | close on the exposed front structure + engine bay | move in on the removed area (lesson c5) | **b24-28 (was 8 beats, now 4)** | path **reversed**: nose -> rearward, so it hands off to the side move |
| 5 | **s4b_side (new)** | comp_explode (bumper off, hood open, lid closed) | right-side wheels/Toyo tyres/brakes, mirror, door line | travel front -> side -> rear (v2 brief); side has only exterior data -> 4 beats; riser b28-31 carries it into the drop | **b28-32** | low straight dolly along -X, front wheel -> rear wheel |
| 6 | s5_trunk | comp_explode + trunk_full | trunk closed -> half -> open (the 3 captures) | rear states on the DROP; arrives from the side move | b32-40 | **mirror to rear-RIGHT (-X)** so screen direction holds (nose frame-right in s4b and s5) |
| 7 | s6_trunk_well | comp_explode + trunk_full | lid underside ribs + trunk well | move in on the opened area | b40-48 | end the crane lower/less steep: the well floor has see-through gaps |
| 8 | s7_top_home | all parts | reassembly: bumper home, hood + lid close, lock b52 | Temerario reassembly; only top view in the reel | b48-56 | keep |
| 9 | logo | logo_card_v2 | small logo | dip 0.6 s at b56, end 35.6 s | b56-end | keep |

## Music map (kick grid 0.6068 + 0.5555 n s, cut frame = round(t*30))

| beat | t (s) | frame | event | scene starts |
|---|---|---|---|---|
| b0 | 0 | 0 | intro | s1_reveal |
| b8 | 5.051 | 152 | phrase | s2_bumper |
| b16 | 9.495 | 285 | new layer | s3_hood |
| b24 | 13.939 | 418 | build | s4_front_detail |
| **b28** | **16.161** | **485** | **riser starts** | **s4b_side (new cut)** |
| b32 | 18.383 | 551 | DROP | s5_trunk |
| b40 | 22.827 | 685 | phrase | s6_trunk_well |
| b48 | 27.271 | 818 | phrase change | s7_top_home (lock b52 = 29.49 s) |
| b56 | 31.715 | 951 | phrase change | dip 0.6 s -> logo, end 1068 (35.6 s) |

## Diff against the current v2 timeline (project.yaml)

- **Added** s4b_side b28-32 (66 frames @30 = 2.20 s). Reason: v2 brief travel front -> side -> rear; current cut jumps from the
  front-right close-up straight to the rear-LEFT on the drop (crosses the line and skips the side).
- **Shortened** s4_front_detail 8 -> 4 beats (133 -> 67 frames @30). Its 8-beat path started on the front wheel (split focus) and
  repeated the bay s3 just showed; the 4-beat close keeps only the bay/structure. The wheel moves to the side scene.
- **Changed camera** s5_trunk: mirror to the car's right (-X) and start a little tighter (not another whole-car wide).
- **Changed camera** s6_trunk_well: end the crane lower and less steep (keep the lid underside + well rim, not the holey floor).
- **Unchanged**: s1_reveal (done), s2_bumper (done), s3_hood (rendering), s7_top_home, logo, all other cut points.
- Render budget: s4 (34 frames @15) + s4b (34) = the 67 frames s4 had -> **no extra render time**.

Reuse: s1_reveal, s2_bumper as-is; s3_hood let it finish. s4-s7 are not rendered yet (only 30 % previews), so the camera changes cost nothing.

## Open questions for the editor
1. Trunk captures from the right: does the lid underside / trunk well read as well from rear-right (-X) as from rear-left?
   Preview s5 + s6 first. If the right side is clearly worse, keep s5 at +X and accept the line cross on the drop (a hard cut on the drop tolerates it) - log the why.
2. s6 floor gaps: are they scan holes or shading? Look at a 100 % frame; if holes, keep the end camera above them (see director.md).
3. s4b: does the propped hood poke into the top of frame at the front wheel? Fine if it does (state continuity), not if it crops oddly.
