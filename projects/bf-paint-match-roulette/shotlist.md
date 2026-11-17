# BF 4/8: Paint-match roulette — shot list (PLAN, awaiting approval)

Session: Black Friday video 4 of 8, slug `paint-match-roulette`. Planned 2026-11-17. Nothing has been rendered yet.

**Owner's concept, verbatim:** "Paint-match roulette. Rapid cuts across every paint-matched Sport Wing color: Boost Blue,
Championship White, Sonic Gray and the rest, each on its car. The text reads "Base Wing 30% off, Paint Match Available""

**In one line:** a silver scan turns into the gloss-black base wing, then a roulette spins through every paint-match colour
that the live store sells for each Sport Wing, always on the car that colour belongs to, and lands on "Paint Match Available".

**Target length:** about 22.8 s with FL + FE + Integra (13 bars at 140 BPM). With the FL wing only, about 15.9 s: sections C and D
are dropped and the end card moves up.

---

## 1. Store facts (live Shopify, "Epsilon+ Aerodynamics", re-checked 2026-11-17 by this session)

| Wing (product GID) | Base = "Generic Gloss Black" | Paint-matched | Paint options on the store (name - code) |
|---|---|---|---|
| Sport Wing – Honda Civic Hatchback (FL2/FL5, 2022+) `gid://shopify/Product/8023666163756` | $450 (FL5 variant compare-at $550) | $850 | Championship White NH0, Boost Blue Pearl B637P, Sonic Gray Pearl NH877P, Rallye Red R513, Crystal Black Pearl NH731P, Lunar Silver Metallic NH830M, Platinum White Pearl NH883P, Solar Silver Metallic NH932M, Urban Gray Pearl NH912P, Meteorite Gray Metallic NH904M, Sand Dune Pearl YR662P, Smokey Mauve Pearl RP61P (**12 paints** + gloss black = 13 options) |
| Sport Wing – Honda Civic Sedan (FE 2022+) `gid://shopify/Product/8043606540332` | $450 | $850 (Wingless) / $900 (Si duckbill; Platinum White $900 on both) | Platinum White Pearl NH883P, Sonic Gray Pearl NH877P, Meteorite Gray Metallic NH904M, Lunar Silver Metallic NH830M, Solar Silver Metallic NH932M, Crystal Black Pearl NH731P, Blazing Orange Pearl YR659P, Rallye Red R513, Aegean Blue Metallic B593M, Blue Lagoon Pearl B645P, Urban Gray Pearl NH912P (**11 paints**) |
| Sport Wing – Acura Integra (DE4/DE5, 2023+) `gid://shopify/Product/7386931298348` | $500 (wing) / $600 (wing + trunk lip) | $950-$1,000 / $1,050-$1,100 | Majestic Black Pearl NH893P, Platinum White Pearl NH883P, Lunar Silver Metallic NH830M, Urban Gray Pearl NH912P, Liquid Carbon Metallic NH885M, Performance Red Pearl R568P, Apex Blue Pearl B621P, Double Apex Blue Pearl B649P, Solar Silver Metallic NH932M, Tiger Eye Pearl YR651P (**10 paints**) |

Corrections to the shared brief: the FL wing has 12 paints plus gloss black (the brief's "13 Honda colours"), and the Integra has
10 paints plus gloss black (the brief's "11"). Stock is negative or zero on every wing variant (made to order or backordered), so
**no stock or scarcity text anywhere**. No prices appear on screen unless the owner gives the Black Friday prices (see Q2).

## 2. Asset inventory

| Asset | Exact source | Status | Notes |
|---|---|---|---|
| FL lookbook GLB | `https://cdn.shopify.com/s/files/1/0036/2250/2435/files/eps-honda-civic-hatch-fl-v8.glb` (sha ec2d2b2b2e209ae6), local `/home/user/media/bf-paint-match-roulette/glb/` | **found** | **FL2 hatch body** with a lip kit (not an FL5 Type R). Meshes include `part_sport_wing` and `part_front_lip` / `part_side_skirts` / `part_rear_lip`. The wing and the body share ONE material, `paint`, so a single colour change paints the car and its wing together (= paint-matched). For the base wing, put `plastic_gloss` on `part_sport_wing`. |
| FE lookbook GLB | `.../eps-honda-civic-sedan-fe-v10.glb` | **found** | `part_sport_wing` + `part_sport_wing_duckbill` (Si duckbill fitment), `body_rear_diffuser_stock`. Same single `paint` material. |
| Integra lookbook GLB | `.../eps-acura-integra-type-s-de5-v19.glb` (DE5 Type S, 19 MB, clearcoat). Also on the lookbook: `eps-acura-integra-de-v29.glb` (DE4) | **found** (DE5); DE4 to fetch | `part_sport_wing` + `part_duckbill`. The Type S has its own factory wing area, so check which body the owner wants (Q6). |
| FL/FE facelift GLBs | `eps-honda-civic-hatch-fl-facelift-v8.glb`, `eps-honda-civic-sedan-fe-facelift-v9.glb` | **to-request** | The CDN returned 404. Pull them from Drive `Website Files/Epsilon-final-GLBs-2026-10-15.zip` (id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) if needed. Not needed for the plan below. |
| Paint colours (hex + finish) | Lookbook configs from `lookbook-frames-927fc403.json` / `-a8da60cb.json` -> `lb-honda-civic-hatch-fl-*.json`, `lb-honda-civic-hatch-fl-facelift-*.json`, `lb-honda-civic-sedan-fe(-facelift)-*.json`, `lb-acura-integra-type-s-de5-*.json`, `lb-acura-integra-de-*.json` | **found for every store colour except FL Championship White NH0** | e.g. Boost Blue #0a7ee8 pearl, Sonic Gray #6e7886 pearl, Rallye Red #c8102e gloss, Tiger Eye #c86a1f pearl. The website has no Championship White config, but real photos cover it (row below). The lookbook also lists Morning Mist and Boost Blue for the FE: **not used**, because the FE wing doesn't sell them. |
| Real photos of painted wings | epsilon.plus listing images (cdn.shopify.com/s/files/1/0036/2250/2435/files/...) | **found** | FL5 Type R: Championship White `civic-type-r-fl5-sport-wing-white-rear-quarter.jpg`; Boost Blue `civic-fl5-sport-wing-blue-rear-quarter.jpg` / `civic-type-r-fl5-sport-wing-blue-garage.jpg`; Rallye Red `civic-type-r-fl5-sport-wing-red-rear-quarter.jpg`. FE: Rallye Red `DILL7196.jpg` / `DILL7458.jpg`. I looked at each one and the wing is painted body colour. **Rejected:** `acura-integra-de4-sport-wing-white-rear-quarter.jpg`, where the wing is black (not paint-matched). The grey Integra photos are on hold until the paint name is confirmed (Q7). |
| Full-car scans | Engineering Drive `Honda Civic (11th Gen)` (10Ci7sUypOlHypCK7lW2bsSPSAsazcH14): FL2 `Honda Civic Sport (FL2)/FL2 Full Car.stl` (+ `civic Civic Hatch Rear End` = FL2_5); FE1 `civic Facelift FE1 Full Car.stl` (1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ). Integra `Acura Integra Type S/Integra Type S Full Car.stl` | **found** (FL2 / Integra file ids still to look up) | FL2 caveat from honda-civic-11/clips.md: the rear wheel is broken and the roof has a hole. Shot 2 is framed high on the trunk, on the side whose rear wheel is intact. If no framing hides the damage, use the FE1 scan for the hook. Scan data stays as captured. |
| Sport Wing design/scan files | Drive `Sport Wings` (1U8ifDyr3fc48dLVyIUxwK-hjNws8kviM, install guides), `Sport Wing` (1-atZHtOZCLujn-XCXXhcKk-uh10Oaz8E), `Integra Sport Wing` (1DkLmfcaf9XlzlrTWOXSD-vhOW9Et1o05), FL2 `Trunk Wing Scans/` | **found** (not needed) | The shot plan only uses the lookbook `part_sport_wing`, which is placed by the website. In the scan shot the same mesh is nested into the scan (projects/toyota-mr2-spyder kit_nest2.py method). |
| Characters | Pip & Gus: `git show origin/claude/pip-gus-ep0-intro:projects/scan-tedium-explainer-reel/characters/design.md`, the rig in that project's `tools/partA_scene.py` / `partA_anim.py` / `nametag_tex.py`, and the series rules in `projects/pip-gus-series/SESSION_BRIEF.md` | **found, but these are Illumaesthetic mascots** | No Epsilon-specific character files were found. Pip and Gus wear Illumaesthetic name badges, and the lineup "painter" extra exists only as a concept image (Higgsfield job 2094da79-...), with no rig. Their rules: no arms (floating mitten hands), dot eyes, no eyebrows, cel-shaded EEVEE, Gus never angry or sad. Q5 asks whether they may appear in an Epsilon+ ad. |
| Music | Dropbox `/Moosic/YTDown.com_YouTube_Media_LqdZ9inIAR4_Gran-Turismo-2-Arcade-Mode-Theme_005_128k.m4a` (id:ihAynaYnO_4AAAAAAACRvg) | **found, unused by any reel** | Real track (GT2 OST). Kicks start at 0.51 s with no intro. Measured on 40-120 Hz peaks: **140 BPM, beat 0.4286 s, bar 1.714 s, downbeats D_n = 0.512 + 1.714·n**. `ive beats` reports half tempo (69.8). |
| Logo | Drive `EPSILON+ Logos` (white wordmark, ~720 px wide) | to fetch | Use the Epsilon+ wordmark, not the Illumaesthetic logo. |

Music candidates. Each one was checked against `projects/*/project*.yaml` and `editlog.jsonl`. Other Black Friday sessions may
pick from the same folder, so the parent should de-duplicate:
1. **GT2 "Arcade Mode Theme"** (recommended). Upbeat and game-show-like, which suits a "roulette", and it starts on a kick.
2. Juiced OST "Way Out West - Killa". Unused, 129 BPM, but it has a 30 s intro, so the start-from-the-beginning rule fails for a 20 s reel.
3. Kirby "Dream Land" theme. Unused, playful, but off-brand for aero parts.

Every other track in `/Moosic` is already used by a reel.

## 3. Shot table (FL + FE + Integra version; times from the measured 140 BPM grid, re-measured per cut before assembly)

Shared camera rules: "**R-cam**" is a rear 3/4, high (pitch about 18°), 40 mm, with the wing near the frame's upper third and the
whole car at 85-90 % of the 1080 width. The roulette renders for each car use ONE locked R-cam with only a ~2 % push-in, so the
paint swap is the only change. Each car's R-cam puts its wing at the same screen position, so the car-to-car swaps also read as
1:1. Text is Remotion, Epsilon type, **only on render frames**. Photos carry no text.

| # | Time (s) | Dur | Beat | Camera | Subject | Source asset | Action | On-screen text (source) | Transition in | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.000-2.226 | 2.23 | song start -> D1 | Cel-shaded medium, slight push | **Pip** (only if Q5 = yes) | Pip rig (scan-tedium tools), new booth set | Pip's floating hands yank a slot/roulette lever. A swatch wheel spins and blurs on the last beat. | none | - | Blender EEVEE (cel) |
| 2 | 2.226-3.940 | 1.71 | D1 (kick) | FL R-cam, push-in 3 % | FL2 **scan** in house silver, with the lookbook Sport Wing nested in silver | FL2 Full Car.stl + `part_sport_wing` from eps-honda-civic-hatch-fl-v8.glb (nested like kit_nest2.py) | Scan reveal | none | hard cut | Blender Cycles |
| 3 | 3.940-5.654 | 1.71 | D2 | same camera as 2 (1:1) | FL2 GLB, Platinum White body, **gloss black base wing** | eps-honda-civic-hatch-fl-v8.glb (`part_sport_wing` -> `plastic_gloss`) | Hard 1:1 cut scan -> CGI on the kick, push continues | "BASE WING 30% OFF" (owner text; pending Q2/Q3) | **hard 1:1 cut** | Blender Cycles + Remotion |
| 4 | 5.654-6.511 | 0.86 | D3, 2 beats | photo, slow 3 % Ken Burns | FL5 Type R, **Boost Blue** wing | civic-fl5-sport-wing-blue-rear-quarter.jpg | Roulette starts: photos of the owner's named colours | none (IRL photo) | hard cut | footage edit |
| 5 | 6.511-7.368 | 0.86 | 2 beats | photo | FL5 Type R, **Championship White** | civic-type-r-fl5-sport-wing-white-rear-quarter.jpg | - | none | hard cut | footage edit |
| 6 | 7.368-8.225 | 0.86 | D4, 2 beats | photo | FL5 Type R, **Rallye Red** | civic-type-r-fl5-sport-wing-red-rear-quarter.jpg | - | none | hard cut | footage edit |
| 7 | 8.225-9.082 | 0.86 | 2 beats | FL R-cam (locked) | FL2 GLB, **Sonic Gray Pearl** body + wing | FL GLB, `paint` = #6e7886 pearl | Locked-camera roulette begins | "PAINT MATCH AVAILABLE" (owner) + chip "SONIC GRAY PEARL · NH877P" (store) | hard cut | Blender + Remotion |
| 8-15 | 9.082-12.510 | 8 × 0.429 | D5 -> D7, 1 beat each | FL R-cam (locked) | FL2 GLB in: Crystal Black Pearl NH731P, Lunar Silver Metallic NH830M, Platinum White Pearl NH883P, Solar Silver Metallic NH932M, Urban Gray Pearl NH912P, Meteorite Gray Metallic NH904M, Sand Dune Pearl YR662P, Smokey Mauve Pearl RP61P | FL GLB + lookbook hex per colour | Spin speeds up: paint swaps on every kick | same header; chip name + code per shot (store) | hard cuts | Blender + Remotion |
| 16-25 | 12.510-14.653 | 10 × 0.214 | D7, half-beats | FE R-cam (wing at the same screen spot) | FE sedan GLB in: Platinum White, Sonic Gray, Meteorite Gray, Lunar Silver, Solar Silver, Crystal Black, Blazing Orange, Aegean Blue, Blue Lagoon, Urban Gray | eps-honda-civic-sedan-fe-v10.glb (wingless trunk fitment = `part_sport_wing`) | Car swaps 1:1 on the wing, then a fast spin | "CIVIC SEDAN SPORT WING · 11 HONDA COLOURS" (store count), no per-shot names (too fast to read) | hard cut | Blender + Remotion |
| 26 | 14.653-15.938 | 1.29 | 3 beats | photo, 3 % Ken Burns | FE, **Rallye Red** wing (real) | DILL7196.jpg | The FE spin lands on a real car | none | hard cut | footage edit |
| 27-34 | 15.938-17.652 | 8 × 0.214 | D9, half-beats | Integra R-cam (wing at the same spot) | Integra GLB in: Majestic Black, Platinum White, Lunar Silver, Urban Gray, Liquid Carbon, Performance Red, Apex Blue, Solar Silver | eps-acura-integra-type-s-de5-v19.glb (or DE4 v29, Q6) | Car swap and fast spin, Acura colours only | "INTEGRA SPORT WING · 10 ACURA COLOURS" (store count) | hard cut | Blender + Remotion |
| 35 | 17.652-18.081 | 0.43 | D10, 1 beat | Integra R-cam | Integra in **Tiger Eye Pearl YR651P** | Integra GLB | Slowing | chip "TIGER EYE PEARL · YR651P" | hard cut | Blender + Remotion |
| 36 | 18.081-19.366 | 1.29 | 3 beats | Integra R-cam, 3 % push | Integra in **Double Apex Blue Pearl B649P** | Integra GLB | Landing on the last colour | chip "DOUBLE APEX BLUE PEARL · B649P" | hard cut | Blender + Remotion |
| 37 | 19.366-21.080 | 1.71 | D11 | FL R-cam, slow 10° orbit | FL2 GLB, Rallye Red, painted wing | FL GLB | Hero end shot | "BASE WING 30% OFF" / "PAINT MATCH AVAILABLE" (owner) | hard cut | Blender + Remotion |
| 38 | 21.080-22.794 (+ decay) | 1.71 | D12 | - | Epsilon+ wordmark, ~720 px, on black | Drive EPSILON+ Logos | Fade in, hold, out on the decay | wordmark | hard cut | Remotion |

FL-only version: shots 16-36 are dropped and shot 37 starts at D7 (12.510), so the video ends at about 15.9 s. Without Pip (Q5 = no),
shot 1 is dropped, everything moves 2.226 s earlier, and the music still starts at 0. The scan shot then opens on the first kick.

Rules checked against this plan: 9:16; a hard 1:1 cut, never a dissolve; every cut on a measured kick or hat (the half-beat cuts
in 16-34 need a transient on each 8th note, or they fall back to 1-beat cuts with fewer colours, Q8); no text over the real photos;
no numbers that are not from the store; plates stay; the logo is the Epsilon+ wordmark at ~720 px; nothing is clipped (check the
first, middle and last frames of every shot); the wing stays inside the frame above the bottom 20 % caption zone.

## 4. Open questions for the owner

1. **Which wings?** FL only (the colours you named are FL colours), or FL + FE sedan + Integra? The table above shows all three. FL only gives about 15.9 s.
2. **Black Friday price.** "Base Wing 30% off": should prices appear (FL/FE $450 -> $315, Integra $500 -> $350), or the words only? The FL5 gloss-black variant already shows a $550 compare-at on the store. Is the 30% taken off $450 or $550?
3. **"Base Wing" = the Generic Gloss Black variant** ($450 FL/FE, $500 Integra)? Is the Integra "Sport Wing + Rear Trunk Lip" combo ($600) included in the 30%? Does the discount cover painted wings?
4. **"Each on its car," strictly.** The FL lookbook model is an **FL2** hatch, and the store sells all 12 colours for both FL2 and FL5. My understanding is that Boost Blue and Championship White are Type R (FL5)-only factory colours. Is that right? The plan shows those two only on the real FL5 photos and renders the other colours on the FL2 model. Some colours may also be FL2-only (e.g. Smokey Mauve, Sand Dune). Fine on the FL2 render?
5. **Characters.** Pip & Gus are *Illumaesthetic* mascots with Illumaesthetic badges; I found no Epsilon-specific characters. May Pip open this Epsilon+ ad (shot 1, no voice), with the badge swapped to Epsilon+ or kept? Or should we skip characters here?
6. **Integra body:** DE5 Type S model (v19) or the DE4 model (v29)? The wing listing says DE4/DE5.
7. **Grey Integra listing photos:** which paint is that car (Urban Gray / Liquid Carbon / Solar Silver)? With a name, it can be the Integra landing shot instead of a render.
8. **Pace:** are half-beat cuts (about 6 frames each) OK for the FE/Integra spins, or should every colour get at least one beat (about 5 s longer)?
9. **Colour labels on photos:** the photos carry no text (house rule). Should the photo shots have a black band below the photo that carries the colour name, or no name at all?
10. **Music:** is the GT2 "Arcade Mode Theme" OK?

## 5. Production steps (after approval)

1. `ive log` each answer. Create `project.yaml` from `_template`. Re-check every price and colour list on the store on the day of the render.
2. Fetch the FL2 / Integra scan file ids from Drive and download them. Prep the scans (level, ground crop, plate untouched) and nest `part_sport_wing` into the FL2 scan (kit_nest2.py method). Check the nesting in a close-up at the trunk mounting edge.
3. Blender scene per car: import the lookbook GLB, use the house studio rig and AgX, make one locked R-cam per car, and match the wing's screen position across the three cameras. Script `paint` colour swaps from the lookbook hex + finish table (pearl/metallic flake via coat + metallic; watch the lesson on saturated reds and blues turning salmon/cream under AgX). Render one 1-beat still sequence per colour (a 2 % push only), one at a time, in the background.
4. Shot 2/3: render the scan and the GLB from the same camera path, and check that they overlap 1:1 with an onion overlay.
5. Photos: Ken Burns on an extended canvas (fg2-race-car canvas.py), no text.
6. Pip shot (if approved): rig from the scan-tedium project, cel EEVEE, owner approval of a still before animating.
7. Remotion: header, colour chip, end card, wordmark (720 px). Every string comes from the store table above.
8. Assemble on the measured grid. Verify cuts on the decoded audio of the delivered file (±½ frame). Mix at -14 LUFS, true peak < -1 dBFS.
9. First/mid/last contact sheet for every shot, director pass, self-score with the rubric in review.md, then archive, commit and push.
