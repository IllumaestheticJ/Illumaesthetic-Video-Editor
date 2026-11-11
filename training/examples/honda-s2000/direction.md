# Honda S2000 AP1 - scene direction (v6)

Scene-director stage (`.claude/agents/scene-director.md`). Stage 2 (shot plan) is `director.md`.
Inputs: lessons.md (all), style-guide, Temerario notes, clips.md, project.yaml/v4, editlog, feedback, review,
director_report (its durations ignore `frames:`; v4 real lengths = frames/30), contact sheets of every render
(`/home/user/media/work/s2k/direct/sheetA-D.png`), numpy splats of the scans (`direct/brem_front.png`, `brem_top.png`,
`bumper_front_vs_inner.png`), plus the coordinator's second brief (user feedback A-D, which overrides the first brief).

## Standing constraints for this version
- **Only real separate part = front bumper (`Bumper Only`).** Only real opened state = **Bumper Removed** (`comp_front.blend`:
  car minus bumper + Bumper Removed structure, hood CLOSED).
- **No hood animation at all** (user D): the hood was never captured open and is not a part scan. `hood.blend`,
  `comp_fronthood.blend`, `hopen` and every render with a raised hood (s5_front_open, s6_structure, s8/e*) are withdrawn.
  The Hood Open scan's radiator-support data is the same front structure Bumper Removed shows: not used.
- No trunk, no `S2000 trunk.stl`, no Scans_2/3 (unchanged).
- Labels ARE now allowed (user C) - only over scan shots of the Bumper Removed section, plain words backed by the file
  names, only naming parts visible in the 2 mm render. No numbers.
- Every wide shot shows the whole car with margins; every detail shot fills the frame with its named section (user A).
- Each section appears in ONE continuous run (user B).

## Step 1 - feature inventory
| Region | Scan(s) | What is really there | States | Parts | Signature | Quality | Score |
|---|---|---|---|---|---|---|---|
| Front | car4/front2 (full car), Bumper Only, Bumper Removed | headlights, fog/turn lamps in the bumper, long hood. Bumper Removed (splat `brem_front.png`): horizontal **bumper beam** across the nose with bolt bosses, vertical **radiator-support** uprights and lower crossmember, headlight backs, a centre post, ducting/side shrouds left+right, a round component on the car's right | **bumper removed (real, registered p50 1.47 mm)** | **front bumper** (inner face: numpy splat shows the +Y-facing inner skin captured across the full width, holes round the centre intake - confirm with one render from behind) | headlights, long hood | 2 mm crops good; stringy debris low under the support; one scanned wheel boxed out | **5** (only region with a state + a part) |
| Side (left) | mid2 (2 mm) | "S2000" fender badge, mirror, door handle, door shut lines | none | none | badge, mirror | good; **no wheels** - empty arches are black voids | 3 |
| Rear | rear2 (2 mm) | ducktail lip, tail lamps, rear plate recess, exhaust tips (debris) | none (trunk scan withdrawn) | none | ducktail + tail lamps, short deck | good lamps; exhaust debris; check plate legibility | 2 |
| Top | car4 | hardtop, long-hood / short-deck plan view | - | - | proportions | clean | 2 |
| Wheels | - | not scanned | - | - | - | empty arches | 0 (keep cameras >=1.2 m high, 3/4) |
| Engine bay / hood | Hood Open (front ~1 m only) | bay behind support unscanned; hood never captured open | none usable | none | - | void | 0 - not shown |

## Step 2 - order
Travel one way round the car: **whole (front-left) -> left side -> rear -> over the top -> front**, and the front is ONE
continuous section from b28 to the end, so the richest region gets the drop (b32) and ~50 % of the runtime.
- Opener: whole car, front-left 3/4 (the reviewer liked this start; it shows the long hood and the badge side), moving from frame 1.
- The lap: front-left -> left flank (badge/mirror/handle, gliding rearward) -> rear 3/4 swinging behind -> right tail lamp ->
  top-down pass that descends onto the front-right -> front section. Camera azimuth increases monotonically; no ping-pong.
- Front section (hero): headlight close-up in the drums-out break -> **bumper comes off ON the drop** -> move in and hold on
  the beam / radiator support (labels) -> two more structure angles -> the bumper shown off in black space (inner face if the
  render confirms) -> bumper returns and **locks on b76** -> whole car pulls back, fade -> small logo.
- Explode ladder rung reduced to what exists: one part. No hood, no trunk, no multi-part explode.

## Scene list
| # | scene | scans used | feature shown | section | why here | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | W1 opener | car4 | whole car, long hood + badge side | whole | strongest-looking end + reviewer liked it | b0-8 | front-left 3/4, whole car with margins (re-render: v5 s1 clips the nose from frame 19) |
| 2 | S1 flank | mid2 | S2000 badge, mirror, door handle | side | continues the lap from front-left toward the rear | b8-12 | reuse s4b frames 0-21 (after 22 the empty arch shows) |
| 3 | R1 rear wide | car4 | ducktail / short deck, tail lamps, hardtop | rear | lap reaches the rear | b12-16 | left-rear 3/4 swinging to dead behind (re-render: v5 s2 clips from frame 19) |
| 4 | R2 tail ECU | rear2 | right tail lamp + ducktail edge | rear | rear close-up next to its wide | b16-20 | reuse s4_tail frames 0-26 |
| 5 | T1 top | car4 | plan view, proportions, hardtop | top | carries the camera over the car to the front-right | b20-28 | reuse s7_top **reversed** (top-down -> high front-right 3/4) |
| 6 | F0 lamp | front2 | left headlight + bumper lamps | front | quiet detail in the drums-out break, sets up the front | b28-32 | reuse s3_lamp frames 0-26 |
| 7 | F1 bumper off | comp_front + bonly | bumper leaves, structure revealed | front | the one real state lands on the DROP | b32-40 | front-right, whole front end, push in after the bumper drops out of frame |
| 8 | F2 beam | comp_front | bumper beam + radiator support (centre) | front | hero hold, label | b40-48 | straight-on, slightly high, slow push |
| 9 | F3 right end | comp_front | beam end, bracket, shroud/duct (car's right) | front | second detail angle | b48-54 | low front-right close slide |
| 10 | F4 overhead | comp_front | top of beam, support upper tie bar, headlight backs | front | third angle, from above | b54-60 | high, ~60 deg down, lateral slide |
| 11 | F5 bumper show | comp_front + bonly | the bumper part, inner face | front | part shown off in clear black | b60-68 | front-centre high ~50 deg down |
| 12 | F6 return | comp_front + bonly | bumper slides home, LOCK b76 | front | honest "reassembly" of the one part | b68-76 | low front-left 3/4 |
| 13 | F7 out | comp_front + bonly (locked) | whole car, fade | whole | Temerario end: assembled car, fade | b76-80 | high front-left 3/4 pull-out, fade last 9 frames |
| 14 | logo | logo_card | small logo | - | - | b80-37.2 s | reuse logo_card_v4.mp4 (71 frames) |

## Music map (138.05 BPM, B 0.43463 s, kick 0.0565 s; cut frame = round((0.0565+n*B)*30))
groove b0-27: exterior lap, 4-8 beat shots (as v4, which the reviewer liked) | drums out b28-31: headlight close-up |
**DROP b32 (13.965 s): bumper comes off** | groove b32-64: structure holds + bumper show | drumless rising outro b65-83: bumper
drifts back, **slams home on b76** | b80 logo through the hard stop b84 (36.565) | end 37.2 s (frame 1116).

## Diff vs v5 (project.yaml)
| v5 shot | v6 | why |
|---|---|---|
| s1_front | replaced by W1 (re-render, same move, pulled back) | used frames 21-74 clip the nose on the left edge (measured: car touches x=0 from frame 19) - user A |
| s2_rear | replaced by R1 (re-render) | clips from frame 19; also a long orbit (rotation lesson) - now 4 beats with a purpose (lap to the rear) |
| s3_lamp | kept, moved to b28-32 | front detail belongs in the front section (user B) |
| s4_tail | kept, b16-20 | - |
| s4b_flank | kept, trimmed to frames 0-21 | later frames end on the black empty arch (dead black where the subject should be) |
| s5_front_open | dropped -> F1 re-render | hood lift is fake (user D); framing crops the left fender |
| s6_structure | dropped -> F2/F3/F4 | hood up (fake) |
| s7_top | kept, reversed, b20-28 | becomes the transport over the car to the front |
| e1..e8 / s8_explode | dropped | hood (and in v4_old the trunk lid) in the explode; multi-part explode does not exist |

## Open questions for the editor (do not guess)
1. Render ONE 2 mm frame of `bonly` from behind (camera at +Y looking -Y): is the inner face clean enough to show? If ragged,
   F5 drops the tip (translate only) and its label becomes "FRONT BUMPER".
2. In the first F2/F3/F4 preview: confirm what you can name. My splat shows a horizontal beam with bolt bosses and vertical
   uprights + lower crossmember; label words below depend on that (fallback "FRONT STRUCTURE").
3. Check s4_tail frames 0-26 at full res for a legible plate (lesson) before reuse.
4. IRL footage of the S2000 being scanned is still missing: slot in director.md.
