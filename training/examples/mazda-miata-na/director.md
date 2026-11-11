# Mazda Miata NA - director plan v2 (director, 2026-11-11)

Keeps the scene order of `direction.md` (front -> side -> rear -> top reassembly -> logo). Scan frame: nose -Y (tip y=-1.97),
tail +Y (1.97), car's right = -X, ground z=0, width 1.79 m, height 1.24 m. Camera keys = `cam(t, loc, target, focal, ease)` in
tools/shots.py (sensor 20.25 mm). Cut frames @30 = round(t*30) on the kick grid; renders at 15 fps.

## Shot plan

| section | shot id | start-end | focus | camera | part action | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | s1_reveal | b0-b8, f0-151 (5.03 s) | whole car | front-right 3/4, (-3.9,-5.9,1.35)->(-2.9,-4.9,1.15), tgt (0,-0.35,0.5)->(0,-0.9,0.5), 30 mm, straight push from frame 1 | none | the only whole-car exterior; uncropped (v1 note) | **reuse** (done) |
| front | s2_bumper | b8-b16, f152-284 | front bumper (part, scanned inside) | front-right, (-2.05,-4.7,0.95)->(-1.95,-4.6,1.0), tgt ->(0.15,-2.0,0.92) | b9 lift -> b11.5 out in clear air (0,-0.55,+0.75) -> b12-b15 turn 135 deg about X to show tabs/ribs | the one removed part; stays framed on the front while it comes off and shows its inner face | **reuse** (done) |
| front | s3_hood | b16-b24, f285-417 | hood opening over the bumper-off front end | high front-right, (-2.6,-3.9,2.3)->(-2.2,-3.4,2.15), tgt (0,-1.45,0.6) | hood opens b16.5-b19.5 on the fitted cowl hinge (-44.4 deg) | Front End Bumper Off + Hood Open states, real geometry under the removed bumper | **reuse** (let it finish) |
| front | s4_front_detail | b24-b28, f418-484 (67 f, 2.23 s) | exposed front structure + engine bay | **reversed + halved**: start at the nose (-1.55,-2.35,1.30) tgt (-0.10,-1.75,0.50) -> dolly rearward to (-1.70,-1.45,1.42) tgt (-0.20,-1.60,0.55), 32 mm, ease lin->out2 | hood held open, bumper away (not loaded) | moves in on the removed area; rearward travel hands off to s4b | **re-render** (34 f @15) |
| side | **s4b_side** (new) | b28-b32, f485-550 (66 f, 2.20 s) | right-side wheels / Toyo tyres / brakes, mirror, door line | low straight dolly parallel to the car's right side: (-2.45,-1.25,0.70) tgt (-0.40,-0.95,0.45) -> (-2.45,+1.05,0.70) tgt (-0.40,+1.35,0.45), 35 mm (~0.95 m wide x 1.65 m tall at the body: full height, tyre ~60 % of width), ease lin (moving at both cuts, rides the riser into the drop) | base comp_explode, hood(H_OPEN), lid(still): state continuity (bumper off, hood up) | side has only exterior data -> one short move, no orbit; carries the travel front -> rear; nose stays frame-right like s1-s4 | **new render** (34 f @15) |
| rear | s5_trunk | b32-b40, f551-684 | trunk lid: closed -> half -> open (3 captures) | **mirrored to rear-right**: (-2.05,4.3,1.5) tgt (0,1.35,0.65) -> (-1.75,3.8,1.6) tgt (0,1.3,0.65), 30 mm; tighter than v2 preview (no second whole-car wide) | lid b32.5 -> half 37.5 deg by b34, hold to b35.5, -> open 55.6 deg by b37 | the rear's 3 registered states on the DROP; screen direction kept from s4b | render (67 f) |
| rear | s6_trunk_well | b40-b48, f685-817 | trunk lid underside ribs + trunk well | mirrored crane behind the open lid: (-0.55,3.1,1.5) -> (-0.25,2.85,1.85), tgt (0,1.3,0.6)->(0,1.25,0.55), 30 mm, out2 | lid held open | moves in on the opened area; ends before looking straight down onto the well floor gaps | render (67 f) |
| top | s7_top_home | b48-b56, f818-950 | reassembly: bumper home, hood + lid close | top-down, front at top, (0,-0.45,6.3)->(0,-0.15,5.6), slow push | b49 -> b52: bumper slides home from in front of the nose, hood + lid close; lock b52 | Temerario reassembly; only top view; ends the story closed | render (67 f) |
| end | logo | b56-35.6 s, f951-1067 (+0.6 s dip) | small logo (470 px) | static card | fade with the music decay | short ending (sibling notes) | reuse logo_card_v2 |

### Tags for project.yaml timeline (`ive director` reads `section` / `focus`)

```yaml
- {id: s1_reveal,       section: whole, focus: "whole car, front-right 3/4"}
- {id: s2_bumper,       section: front, focus: "front bumper part - scanned inside"}
- {id: s3_hood,         section: front, focus: "hood opening over the bumper-off front end"}
- {id: s4_front_detail, section: front, focus: "exposed front structure + engine bay", dur: 2.2333}
- {id: s4b_side,        section: side,  focus: "right-side wheels, Toyo tyres, brakes, mirror, door line", dur: 2.2000}
- {id: s5_trunk,        section: rear,  focus: "trunk lid closed -> half -> open"}
- {id: s6_trunk_well,   section: rear,  focus: "trunk lid underside + trunk well"}
- {id: s7_top_home,     section: top,   focus: "reassembly: bumper home, hood + lid close"}
- {id: logo,            section: end,   focus: "small logo"}
```
Cut notes: s4 -> s4b `cut, "b28 16.161 riser"`; s4b -> s5 `cut, "b32 18.383 THE DROP - side -> rear"`. timing.json: s4_front_detail
cut 418 dur 67, s4b_side cut 485 dur 66 (secs 2.2333 / 2.2 for shots.py).

## Cut list
From v1: s1_turntable, s2_rear orbit, s7 rotating top-down, s8_explode orbit (rotations showing nothing new; IoU repeats
s1~s2 0.82, s5~s6 0.88); s3_wheel / s4_lamp 1.1 s inserts (off-area; the wheel returns in s4b as part of the travel);
v1 explode lifting hood and lid off (they were never removed); 860 px logo 4.4 s.
From the v2 plan: s4 first half (opened on the front wheel = split focus, and repeated s3's bay framing for 4 more beats);
s5 rear-LEFT whole-car wide (crossed the line on the drop and was a second whole-car wide after s1).

## Hold list (> 0.75 s)
- s3 b19.5-b24 (2.5 s): hood fully open, camera push continues - the viewer reads the engine bay under the lifted hood.
- s5 b34-b35.5 (0.83 s): lid parked at 37.5 deg - that is the real Half Open capture, not an in-between.
- s5 b37-b40 (1.67 s): lid open, push continues - the drop's energy carries it; s6 then moves in.
- s7 b52-b56 (2.2 s): locked car, push continues into the dip - the closing image; not longer (sibling "ending held" notes).

## Render budget (15 fps, one Blender at a time, ~15-20 s/frame)
Reused unchanged: s1_reveal (77 f), s2_bumper (68 f), s3_hood (in progress, ~67 f), logo card.
To render: s4_front_detail 34 + s4b_side 34 + s5_trunk 68 + s6_trunk_well 67 + s7_top_home 67 = **270 frames (~68-90 min)** -
identical to the plan before (s4 at 67 frames); the side scene costs nothing extra. Preview s4b, s5, s6 at 30 % first
(open questions in direction.md: right-side trunk coverage, well-floor gaps, propped hood in s4b's top edge).
After each final: per-frame mean luma check (persistent-data blackouts), then `python -m ive director` for repeated views.
