# Day in the life of an average track guy (video #2): script v1

Status: **APPROVED by the owner (2026-11-19)**, including the ✱ edits. The owner will give further edits on the final
cut. No credits have been spent and nothing has been uploaded yet.

**Title band (lowercase white on black, 1:1 picture below):** `day in the life of an average track guy`
**Him:** He owns an FK8 Civic Type R (manual only) with the TC wing, a splitter, tow hooks and number decals. He wears
a race suit everywhere. He is *so* ready for track and has **never once been behind the wheel on one**. Every detail
on screen keeps that true: nothing may imply he has ever driven a lap (owner, 2026-11-19).
**Format:** about 33 s, 30 fps, hard cuts on a 1.58 s grid, **no music** (exaggerated SFX and noises only, as on the WRX video), minimal voice, and
a hard cut to black. No Epsilon branding; the checkout is a generic store.

## Script

| # | Time | Duration | Location | POV action | Others | Dialogue / VO | SFX | Product / asset | Method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.2 | 2.2 | Bedroom | He slaps the alarm and is already in his race suit and helmet. He shovels cereal at the closed visor and the milk splashes everywhere on the beat. | none | none | alarm, slap, visor clack, splash | none | Blender |
| 2 | 2.2-3.8 | 1.6 | Phone | A track-day sign-up page. His thumb hovers over **Register**, trembles, then swipes away to the store. ✱ | none | none | hesitation drone, swipe | none (generic track-day form, readable in a tight shot) | Blender + screen comp |
| 3 | 3.8-5.3 | 1.5 | Phone | Cart: "[BACKORDER] TC Wing - Honda Civic Type R/Sport FK7/FK8 · $1,200.00". He hammers Confirm about 10 times and the phone shakes. | none | none | cha-ching on every tap | live store listing (re-check before render) | Blender + screen comp |
| 4 | 5.3-8.5 | 3.2 | Driveway | He rips the box open, pulls the wing out and **chucks it at the car**. It slams onto the hatch on its swan necks. He kisses the endplate. | none | none | box rip, whoosh, slam, choir | TC wing built from configurator `gt-wing-mesh.json` + `base-meshes.json` on `honda-civic-type-r-fk8-r2.glb` | Blender (product shot) |
| 5 | 8.5-10.1 | 1.6 | Garage wall | The hands straighten a shelf of trophies. Every plaque reads **ATTENDEE** (track days, a "drivers' meeting", a parking-lot meet), plus one bowling trophy. | none | none | reverent hum | none | Blender (plaque text readable) |
| 6 | 10.1-11.7 | 1.6 | Driver's seat | A five-point harness clicks over a hoodie, gloves go on, and he starts a lap timer on the phone mount. | none | none | harness clicks, timer beep | FK8 interior from GLB (if modelled) | Blender |
| 7 | 11.7-13.2 | 1.5 | School zone | The lap timer ticks at walking pace past a 15 mph sign. The crossing guard stares with a flat face. | crossing guard: deadpan | none | timer beeps, kids | none | Blender |
| 8 | 13.2-14.8 | 1.6 | Speed bump | The splitter scrapes. | none | HIM (satisfied): "Aero's working." | crunch | FK8 GLB | Blender |
| 9 | 14.8-16.4 | 1.6 | Roundabout | He takes the roundabout like a hairpin: heel-toe blips at 12 mph, the wheel steering realistically (owner, 2026-11-19: no side-to-side sawing). A cyclist overtakes him and cuts in ahead. | cyclist: doesn't look | none | rev-matching blips, bike bell | none | Blender |
| 10 | 16.4-18.0 | 1.6 | Office car park | The wing clips the height bar (bonk). He nods slowly, approvingly. | none | none | bonk | TC wing on FK8 | Blender |
| 11 | 18.0-21.1 | 3.1 | Parked, window down | He leans out, gloves still on. | coworker: deadpan, then horror face push-in | COWORKER: "Do you actually race?" HIM: "Next season." COWORKER: "You said that last season." ✱ (two beats of silence) | room tone only | none | Blender |
| 12 | 21.1-22.7 | 1.6 | Tyre | A pressure gauge on a tyre with full tread and the moulding nibs and sticker still on. He writes the reading on his glove. | none | none | gauge hiss, marker squeak | none | Blender |
| 13 | 22.7-24.3 | 1.6 | Phone | The weather app shows one cloud. He gasps and throws a blanket over the wing. | none | none | gasp, thunder sting | TC wing | Blender + screen comp |
| 14 | 24.3-27.0 | 2.7 | Track gate | Every SFX in his world cuts dead; cars howl past inside. His hand flicks the indicator and he does a U-turn. | gate marshal: waving him in | none | engines past, indicator ticks, sad trombone | none | Blender |
| 15 | 27.0-33.0 | 6.0 | Parked (track car park) | Slow push-in on the rear-view mirror: his face for the first time, helmet on. He mouth-revs and **rows the 6-speed shifter through the gears, left foot pumping the clutch**, completely stationary. The timer reads `--:--`. | none | HIM (whispering): "...next season." | mouth "braaap", shifter clunks | FK8 interior | Blender |

Then a hard cut to black.

✱ Suggestions approved by the owner: the coworker's comeback in shot 11, and a trembling
thumb in shot 2 so the Register beat reads in 1.6 s. If shot 11 needs the room, merge shots 2 and 3 into one phone
beat (about 3.1 s).

## Owner notes applied (2026-11-19)
- Shot 5: the trophies say **ATTENDEE**, not PARTICIPANT. PARTICIPANT implies he has tracked; he hasn't.
- Shot 15: **fake manual shifts**, not paddles. The FK8 Type R is manual only.

## Asset inventory
| Asset | Status | Source |
|---|---|---|
| FK8 Civic Type R car | found (to attach) | Epsilon-Site `wing-configurator/data/models/honda-civic-type-r-fk8-r2.glb` / `-r3.glb` |
| TC wing (blade, endplates, swan-neck bases) | to build | Epsilon-Site `wing-configurator/data/gt-wing-mesh.json`, `base-meshes.json` (the configurator's own meshes; never an approximation) |
| Price / title | to re-check | live Shopify store (was $1,200.00, 66.5 in, backorder on 2026-11-18) |
| Hands, people, sets, face decals, frame/title band | to copy and parametrise | `projects/ditl-wrx-vb/tools/` (`ditl_kit.py`, `faces.py`, `textures.py`, `sound.py`, `frame.sh`) |
| Race suit sleeves and gloves on the POV hands | to make | Blender |
| Track-day form, cart, weather app screens | to make | generic and unbranded, readable in a tight shot |
| FK8 engine sound (high-revving turbo four) | to find | SFX library |
| Music | none | owner: no music, SFX only |
| Voices | decided | Bram (HIM), Harrison (COWORKER), Higgsfield `elevenlabs_v4` dialogue mode, as on WRX |

## Credit estimate
- **A. All Blender plus voice (recommended, as for WRX):** voice only. WRX spent about 5.6 credits for 3 takes on
  `elevenlabs_v4`; this script has 4 lines, so expect about 4-8 credits. The exact figure comes from a `get_cost`
  preflight before any generation.
- **B/C. AI video for character acting:** preflight needed per clip. Not recommended: the WRX video worked without it, and
  the shared budget is about 295 credits for six videos.

## Owner answers (2026-11-19)
- (a) No financing gag: a track LARPer has money but no skill.
- (b) Voices: reuse Bram (HIM) and Harrison (COWORKER).
- (c) Script approved; edits will come on the final product.
- (d) No music: exaggerated SFX and noises only.

## Next step
The voice take: 4 lines on `elevenlabs_v4`, about 4-8 credits. Before generating, run a `get_cost` preflight and get the
owner's go-ahead on that figure in chat. The take goes to the owner before any animation.
