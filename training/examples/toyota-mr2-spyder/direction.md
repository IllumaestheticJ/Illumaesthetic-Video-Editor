# MR2 Spyder v3 scene direction (scene-director, 2026-11-12)

Replaces the 2026-11-11 direction (v2 plan). Answers the v2 review: front bumper data, rear engine data and underbody
data "not properly shown"; then a quick removed-state showcase -> Epsilon kit install on the scan -> 1:1 hard cut to the
car driving (CGI, no clean real driving shot exists) -> logo.

Looked at before writing: lessons.md (all), clips.md, review.md, feedback.jsonl, director_report.md, shots.py, the v2
contact sheet (s12/s13/s14 first/mid/last), and fresh orthographic quicklooks (tools/quicklook.py) of `bumper_part`,
`fbumper` (old diff bumper), both underbody scans, HoodDuct, Hood Open, Rear End trunk open, `base`, and the fitted
lookbook kit + body. Numbers below marked (measured) come from those meshes. Camera values are starting points for the
30 % previews, not finals.

Frame: metres, ground z=0, nose +Y, tail -Y, car's left = -X. Camera: 24 mm-wide sensor on 9:16 (huracan shot.py), so
frame width = dist x 24 / lens (50 mm: 0.48 x dist; 40 mm: 0.60; 35 mm: 0.69) and frame height = 1.78 x that.

## 1. Feature inventory

| region | data (registered) | what it really shows (looked at) | state / part backing | weak spots | used in |
|---|---|---|---|---|---|
| whole car | `car` Full Car 2 mm, hardtop on | clean skin, wheels captured, plate present (kept: plate rule = IS300 only) | stock state | - | S1 first beat only |
| front | `base` front (Hood Duct Data: bumper off + hood open), `hood` (hinged), **`bumper_part`** (FrontEnd.stl, 280k tris, 3.8 mm median) ; dense "front End" / "Hood Open" skins (1.3 mm) | bumper part: clean outer skin, grille opening, lamp cut-outs, both wrap-around ends. Behind it: upper nose panel with emblem, cross member, coolers/lines, lamp buckets, front compartment under the hood. Hood Duct scan also captured the hood underside (bracing + liner) | hood closed/open; bumper on/off; "hood open + bumper on" (Hood Open scan); "hood open + bumper off" (Hood Duct Data) | **bumper part is outer skin only** (measured: 4 % of its area faces rearward, 53 % forward) - no inner face to show; lower nose of the base is ragged (v1/v2 reviews) | **S1 hero** (richest: 1 real part + 2 states) |
| underbody front | `under_front` Kouki and Undertray | undertray panel, front subframe / cross members, lines running aft, one arch with the wheel off | scan of the underside as captured | dense only for y > +0.75 m; thin and ragged from y 0 to +0.75; carries its own bumper + fender skin | S2a |
| underbody rear | `under_rear` Rear Underbody | exhaust pipe + transverse muffler, engine/gearbox underside, driveshafts, rear arms, rear bumper underside, wheels on | as captured | dense only for y < -0.9 m; sparse -0.9..-0.2; stray geometry (measured: z down to -0.10 m, x out to +0.98 m, z up to 1.03 m = body skin) | S2b |
| rear / engine bay | `base` rear (Rear End trunk open, 1.45 mm) + `rearlid` (hinge fit -66 deg, 11 mm) | lid open with its underside captured, engine top, strut brace, tail lamps, mesh grilles | lid closed/open | lid is outer skin (hinge only, never detached) | **S3** |
| top / cabin | `hardtop` part, roof-down car in `base` | seats, tube roll bar | hardtop on/off | hardtop underside not scanned | S4a only (scanned top leaves, Epsilon top lands) |
| kit | lookbook `eps-toyota-mr2-spyder-v19.glb`, body ICP 6.8 mm | front bumper, hardtop + window, side skirts, rear spats, duckbill, diffuser, eyelids, hood vents, TC wing on stands | lookbook parts (not scans) - shown in red paint so they never read as scan data | fit 6.8 mm: scan skin can poke through; Epsilon bumper starts at y +1.45 m, the stock bumper wrapped back to +1.33 m (measured) | S4a, S4b |
| not used | 2022 Front Bumper Data (18 % fit), Suspension Data (not fetched), Tab Ref, old diff `fbumper` | - | never shown or implied | - | - |

Rule D check - every opening/removal in the plan and its scan: hood hinges (Hood Open / Hood Duct Data), front bumper off
(Hood Duct Data + FrontEnd part), rear lid hinges (Rear End trunk open), hardtop off (Full Car Top Down). No doors, no
wheel removal, no lid or hood detached, no bumper inner face, no hardtop underside.

## 2. Order and music map

Travel is one loop with no return: **nose (above) -> under the nose -> under the tail -> tail (above) -> kit install rear
then front -> same front pose driving.** The opener frames the front because the front carries the most data (inventory).

Grid: beat n at 0.344 + 0.4915 n s (music time); reel t = music t - 0.344; cut frame = round(14.745 n) at 30 fps.
My own coarse per-beat low-band check of `mr2_eastcity.wav` agrees with hits at n = 8, 16, 24, 47, 48, 72; in the busy
section (n >= 32) the low accents fall on **n = 35, 39, 43, 47, 51, 55 and 62**, and n = 64 reads as the arrangement
dropping back to the intro groove rather than a big hit. Part landings are therefore placed on 35 / 39 / 43 / 47. All of it
gets re-measured on the decoded audio.

| # | shot | n | reel s | out frames | section (rule B) | the ONE thing to look at |
|---|---|---|---|---|---|---|
| S1 | front hero | 0-16 | 0.00-7.86 | 0-236 | front | the real front bumper coming off and what is behind it |
| S2a | under front | 16-20 | 7.86-9.83 | 236-295 | underbody front | undertray + front subframe |
| S2b | under rear | 20-24 | 9.83-11.80 | 295-354 | underbody rear | exhaust / drivetrain underside |
| S3 | engine bay | 24-32 | 11.80-15.73 | 354-472 | rear / engine bay | the engine bay under the hinged lid, close |
| S4a | kit rear | 32-40 | 15.73-19.66 | 472-590 | whole (kit, rear 3/4) | red Epsilon parts landing on the silver scan: wing/duckbill, spats, diffuser, hardtop |
| S4b | kit front | 40-48 | 19.66-23.59 | 590-708 | whole (kit, front 3/4) | skirts, vents, eyelids, then the Epsilon bumper closing the open nose ON n 47 |
| C1 | CGI drive, front | 48-55 | 23.59-27.03 | 708-811 | whole (CGI) | same car, same pose, now painted and moving |
| C2 | CGI drive, rear | 55-66 | 27.03-32.44 | 811-973 | whole (CGI) | rear kit in paint, car pulls away |
| L | logo | 66-72(+0.35 s) | 32.44-35.77 | 973-1073 | - | logo |

Removed-state showcase = S1 hood/bumper (n 1-16) + S3 = 11.3 s, plus 3.9 s of underbody. Kit 7.9 s. Drive 8.9 s incl. fade.

## 3. Scenes

Part-move notation: offset [x,y,z] m from home, or hinge deg; times are beats n (shot fraction = (n - shot start) / length).

### S1 front hero (n 0-16, one continuous push from the whole car into the nose; no cut at n 4)
| | |
|---|---|
| objects | n 0-1: `car` alone (clean). From the frame the hood starts (n 1): `base` + `hood` + `bumper_part` + `hardtop` (home) + `rearlid` (home); `car` hidden. Old diff `fbumper` is never loaded |
| part moves | hood hinge 0 -> 53 deg, n 1 -> 4.5 (a transformation inside the first second). **Bumper starts ON n 8**: n 8 -> 9.5 forward to [0,+0.50,0] (clears the wrap-around ends), n 9.5 -> 11 down to park [0,+0.50,-0.95] (below the nose, in black, fully in frame), n 11.5 -> 13.5 sinks to [0,+0.50,-2.6], then hidden. Translate only - no tip, no spin |
| camera | n 0: az -155, el 10, dist 8.6, target [0,0.10,0.55], 50 mm - whole car, ~87 % of width, moving from frame 1. n 4.5: az -160, el 13, dist 5.6, target [0,1.00,0.75] (open hood top at z ~1.58 stays in). n 7.5: az -166, el 12, dist 4.3, target [0,1.55,0.45] - nose ~82 % of width, 1.3 m of black below for the bumper. n 12: az -172, el 18, dist 2.3, target [0,1.55,0.50]. n 16: az -173, el 20, dist 2.1, same target (slow creep = the hold, 1.97 s) - the structure between the lamp buckets fills the width |
| labels | `HOOD OPEN` / `SCANNED CLOSED + OPEN`, frames 37-96, low band. `FRONT BUMPER REMOVED` / `SCANNED ON THE CAR + AS A LOOSE PART`, frames 140-229, top band (the bumper passes through the lower third). No component name until someone has read it off the n 12-16 frames; candidates only if clearly visible |
| hand-off | ends looking down-in at the nose; S2a starts directly below the same nose. State left behind: hood open, bumper off |

### S2 underbody (n 16-24, two 4-beat shots, same heading logic: under the nose looking aft, then under the tail looking forward)
| | S2a under front (cut ON n 16) | S2b under rear (n 20) |
|---|---|---|
| objects | `under_front` ALONE (no car, no base), under-light 0.4 | `under_rear` ALONE, cleaned of stray geometry, under-light 0.4 |
| camera | start az 180, el -40, dist 2.3, target [0,1.15,0.20], 35 mm -> end az 180, el -46, dist 1.9, target [0,0.95,0.20]. Camera is below ground level (no floor in the scene); the underside recedes up the portrait frame | start az 0, el -40, dist 2.3, target [0,-1.30,0.25], 35 mm -> end az 0, el -46, dist 1.9, target [0,-1.15,0.25] |
| framing intent | undertray + subframe fill the width; bumper corners and arches cropped on purpose; top of frame must end before the thin data at y < +0.75 | muffler + exhaust at the bottom, drivetrain filling the middle; top of frame ends before the sparse zone at y > -0.9 |
| label | `UNDERBODY SCAN` / `FRONT UNDERTRAY + SUBFRAME`, frames 240-292 | `REAR UNDERBODY` / `EXHAUST + REAR SUSPENSION`, frames 299-351 |
| hand-off | hard cut nose -> tail under the car | camera is below and behind the tail; S3 starts above and behind the same tail |

Never el = -90 (roll flip). Never one glide nose-to-tail: the middle 1.6 m of the floor is thin in both scans.

### S3 engine bay (n 24-32)
| | |
|---|---|
| objects | `base` + `rearlid` + `hardtop` (home) + `hood` (open, off-frame); bumper stays off (hidden) |
| part moves | **lid hinge starts ON n 24**: 0 -> -59.4 deg, n 24 -> 26.5. Hinge only |
| camera | n 24: az -14, el 30, dist 3.4, target [0,-1.35,0.80], 40 mm - whole tail in frame (lamps, grilles; ~83 % of width). n 27: az -10, el 42, dist 2.4, target [0,-1.30,0.80]. n 28.5: az -7, el 50, dist 1.85, target [0,-1.30,0.72]. n 32: az -6, el 52, dist 1.70, same target - bay fills the width (frame 1.0 m wide), raised lid underside across the top. Close hold n 28.5-32 = 1.7 s (v2 stopped at 2.9 m) |
| label | `ENGINE BAY` / `SCANNED WITH THE REAR LID OPEN`, frames 405-468; band chosen from the frames (lid is rising in the top band until n 26.5) |
| hand-off | cut on n 32 straight back along the same sight line to the S4a wide; the lid is seen closing |

### S4 kit install - see section 4

## 4. Kit install choreography (n 32-48, two 3/4 shots, kit parts in the car's red paint on the silver scan)

Body under the kit = `base` + scanned `hood` + `rearlid` (silver). Parts that are waiting are already floating in black,
fully in frame, from the first frame of their shot (no pop-ins); only the hardtop enters from above the frame.

| n | event | from -> to | lands on |
|---|---|---|---|
| **S4a rear-left 3/4** | camera n 32: az -20, el 22, dist 9.4, target [0,-0.10,0.60], 50 mm -> n 40: az -28, el 28, dist 9.0 (whole car ~87 % of width on both ends) | | |
| 32 -> 33.5 | stock restore: rear lid hinges shut; hood hinges shut (far end) | -59.4 -> 0 deg; 53 -> 0 deg | - |
| 32.5 -> 34.5 | **scanned hardtop leaves**: straight up into the black, hidden once out of frame | [0,0,0] -> [0,-0.1,+4.6] | - |
| 33.5 -> 35 | duckbill + TC wing kit (one move) | [0,-0.4,+1.2] -> home | **35** (accent) |
| 35.5 -> 37 | rear spats + diffuser (one move) | [0,-0.8,-0.25] -> home | 37 |
| 37 -> 39 | **Epsilon hardtop** (with its window) comes down from above the frame | [0,0,+4.6] -> home | **39** (accent) |
| 39 -> 40 | hold, camera still moving | | |
| **S4b front-left 3/4** | camera n 40: az -152, el 20, dist 9.0, target [0,0.10,0.60], 50 mm -> n 47: az -161, el 14, dist 8.05, target [0,0.20,0.50] -> n 48: az -162, el 14, dist 8.0 (linear, never stops) | | |
| 40.5 -> 42 | side skirts rise from below (one mesh, both sides, never crosses the body) | [0,0,-0.7] -> home | 42 |
| 42 -> 43 | hood vents | [0,+0.2,+0.9] -> home | **43** (accent) |
| 44 -> 45 | eyelids | [0,+0.3,+0.6] -> home | 45 |
| 45 -> 47 | **Epsilon front bumper** closes the open, bumper-off nose - the pay-off of S1 | [0,+0.5,-0.95] (same park spot the stock bumper left from) -> [0,+0.5,0] -> home | **47** (strong hit) |
| 47 -> 48 | complete car, one beat, camera drifting into the cut pose | | cut ON **48** |

The stock bumper never returns: the nose stays in its scanned bumper-off state from n 8 until the Epsilon bumper lands.
Label: `EPSILON AERO KIT` / `BUILT ON THE SCAN DATA`, frames 487-575 (S4a only; band from the frames). No part specs.

**Pose the CGI inherits (last scan frame = first CGI frame): az -162, el 14, dist 8.0, target [0,0.20,0.50], lens 50,
sensor 24, relative to the car; camera angular rate ~1 deg/beat continuing.** Car ~85 % of width, road will run up the frame.

## 5. CGI drive (lookbook model complete, same fit as the kit, real 30 fps, hard cut, no dissolve, no text)

| | C1 (n 48-55, 103 frames) | C2 (n 55-66, 162 frames) |
|---|---|---|
| start | the inherited pose, car already at speed on the first frame: road and light bars streaming, wheels spinning, headlamps on | cut on the n 55 accent to the same (left) side behind the car: az -16, el 10, dist 7.5, target [0,-0.20,0.55], 50 mm |
| move | camera leads the car and lets it close in: -> az -170, el 8, dist 6.6, target [0,0.30,0.50]. Whole car in frame throughout; light bars pass on 51 | locked follow n 55-60 (duckbill, wing, spats, diffuser, tail lamps); from n 60 the car pulls away (dist 7.5 -> ~22), strongest light pass on the n 62 accent; fade to black n 64 -> 66 as the music drops to the intro groove |
| notes | road plane at the model's tyre bottom (measured z = -0.037 m in the scan frame), not z = 0. Motion blur on (wheel at ~160 deg/frame would strobe without it) | C2 is the only rear view of the finished car; it is not a repeat of S3 (close, stock) or S4a (install) |

Logo: card ~720 px wide, fades in from n 66 (0.3 s), cut to black just after the n 72 hit, music tail 0.35 s.

## 6. Cut list, holds, render budget

Cuts (frame): 236, 295, 354, 472, 590, 708 (1:1), 811, 973, end 1073 = 35.77 s. Plain concat with exact `frames:`.
Holds: S1 n 12-16 on the bumper-off structure (1.97 s); S3 n 28.5-32 on the engine bay (1.72 s); S4b n 47-48.

| shot | slot (30 fps) | 15 fps renders (+3 tail margin) | note |
|---|---|---|---|
| S1 | 236 | 121 | persistent data off (hinge + part moves) |
| S2a | 59 | 33 | camera only |
| S2b | 59 | 33 | camera only |
| S3 | 118 | 62 | persistent off |
| S4a | 118 | 62 | persistent off |
| S4b | 118 | 62 + the exact n 48 pose frame as a real render | persistent off |
| **scan total** | | **373 (+1)** | under 400; ~25 spare for real 30 fps in-betweens of the n 45-47 bumper landing if minterpolate smears it |
| C1 + C2 | 265 | 265 at 30 fps | game model, not in the scan budget |

Reuse from v2: none (every v2 shot has the diff bumper, the wrong order of states or the far engine-bay framing).
Logo card must be rebuilt at 720 px (v2 was 380).

`ive director` is expected to flag S4a/S4b/C1/C2 against each other and against S1 (whole-car silhouettes). Reviewed here:
S1 = stock states at the nose, S4 = kit install, C = finished car; each section's removed-state data still appears once.

## 7. Where this departs from the brief (said, not silently followed)

1. **Hood opens before the bumper comes off** (v2 did bumper first). The registered states are "hood open, bumper on" and
   "hood open, bumper off"; "bumper off, hood closed" exists only in the 2022 scans that do not register.
2. **The bumper is not tipped to show its back.** The FrontEnd part is an outer skin only (measured), so there is no inside
   to show and no inside/outside claim.
3. **Underbody sits between the front and the engine bay**, not after the rear, and is two short shots, not a glide: it keeps
   one trip around the car and stays off the thin mid-floor data. Front then rear, as asked.
4. **Kit install is two 3/4 shots, not one orbit.** A side-on whole car in 9:16 needs ~10 m and reads tiny; an over-the-top
   arc hits the overhead roll flip.
5. **Length 35.8 s, not 36-38 s.** The track calms at n 64 and hits at n 72; ending the logo on 72 is the natural end.
   Longer option: hold C2 to n 72 and bring the logo in on that hit (reel ~37.8 s, drive 11.8 s) - I do not recommend it.
6. **Showcase is 11.3 s + 3.9 s underbody** against the 12-14 s target, because the underbody was asked for as well.
7. **No scanned-hardtop / cabin scene of its own**: the scanned top just leaves in S4a. It was not in the v2 complaints and
   the time went to the three things that were.
8. **Wheel-off front arch (in `under_front`) gets no shot**: one corner, partial fender skin, and no beats to spare.
9. One interim state has no scan of its own: **hood closed + bumper off** in S4a/S4b (wide, ~7 s). Both part states are
   scanned; the combination is not registered. If that is not acceptable, the alternative is to land the Epsilon bumper
   first in S4b and the vents after.

## 8. Risks to check in previews (first / middle / last frame of every shot, edge-touch test)

1. S1 n 0-1 -> n 1 swap from `car` to `base` + parts: any visible jump in the wide (bumper part sits 3.8 mm median off).
2. S1 n 12-16: ragged lower nose / black holes inside the close frame; move the target up or sideways until the frame is
   clean structure. Read the frame before naming any component.
3. S1 bumper path: clip check against the fenders while it pulls forward; parked bumper fully inside the frame at n 11.
4. S2: strays in `under_rear` (below z 0, beyond x +0.86, body skin above ~0.6 m) and floor strips in `under_front`;
   bumper skin in `under_front` contradicts the bumper-off state - keep it at the frame edge or crop it. Under-light
   level (0.4 worked on the 992; 1.0 blew out). Confirm the label nouns on the frames.
5. S3: lid rising through the label band; legibility of the bay at 1.7 m (hinge fit is 11 mm - look at the lid edge).
6. S4: scan skin poking through red parts (6.8 mm fit) - remove scan triangles under each part's `body_*_stock`
   footprint when it lands; gap between the Epsilon bumper (from y +1.45) and the stock seam (+1.33) showing bumper-off
   structure at the corners; parked parts fully in frame; hardtop fully out before the Epsilon top enters.
7. 1:1 cut: onion of the last scan frame over the first CGI frame (body outline, wheel centres, ride height); pin the light
   rig to one bbox; the last scan frame must be a real render, not an interpolated or cloned one.
8. CGI: wheel strobing, road speed vs wheel speed, whole car inside the frame at the C1 end and C2 start.
9. Per-frame luma scan of every scan shot; every label read on its first, middle and last frame; every cut re-measured on
   the decoded audio (accents at 35 / 39 / 43 / 47 / 55 / 62 are from a coarse check).

## 9. Open questions (not guessed)

1. Do the **duckbill and the TC wing** belong to one lookbook configuration, or are they alternates? If alternates, show
   only the lookbook default and land it on n 35.
2. **End card**: Illumaesthetic logo (assumed, 720 px) or the Epsilon+ wordmark, since the last 16 s are the Epsilon kit?
3. Is the Epsilon **hardtop** in the lookbook the same product as the "Hardtop Mounting" scans were made for? Only affects
   whether a label may say so; no label claims it now.
4. Should the dense "Hood Open" scan (bumper on, front compartment contents) replace the base's fill for n 4.5-8 of S1?
   Only worth it if the base shows a black hole under the open hood at that distance.
