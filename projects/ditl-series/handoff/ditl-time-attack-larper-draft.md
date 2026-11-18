# Video #2 draft script (handed over from the WRX session, 2026-11-18)

Status: a DRAFT. The owner said "hand this script to that session" but has NOT approved the content.
Format: as approved for the WRX video: first person, about 33 s, hard cuts on a 1.58 s grid, 3 short voice lines, hard
cut to black, no Epsilon branding.

**Title:** "Day in the life of an average track guy"
**Character:** a Civic Type R with a huge wing, a splitter, tow hooks and number decals. He wears a race suit
everywhere and has never done a lap. He says "next season" every season, and blames the tyres, the weather and "the
setup".

| # | Time | Shot |
|---|---|---|
| 1 | 0.0-2.2 | Bedroom: the alarm slap; he wakes up already in his race suit and helmet; the hands try to eat cereal through the visor, and milk goes everywhere on the beat. |
| 2 | 2.2-3.8 | Phone: a track-day sign-up page; his thumb hovers over Register, then swipes away to the cart. |
| 3 | 3.8-5.3 | Phone cart: he adds the TC Wing and hammers Confirm ten times. |
| 4 | 5.3-8.5 | Driveway: he rips the box open, pulls the wing out and chucks it at the car; it slams onto the hatch; he kisses the endplate. |
| 5 | 8.5-10.1 | Garage wall: the hands straighten a shelf of trophies; every one says PARTICIPANT or is from bowling. |
| 6 | 10.1-11.7 | Getting in: a five-point harness over a hoodie, gloves on, and a lap timer started on the phone mount. |
| 7 | 11.7-13.2 | School zone: the lap timer runs at walking pace; the crossing guard stares with a flat face. |
| 8 | 13.2-14.8 | Speed bump: the splitter scrapes (crunch). HIM, satisfied: "Aero's working." |
| 9 | 14.8-16.4 | Roundabout: the hands saw at the wheel, heel-toe feet; a cyclist overtakes him. |
| 10 | 16.4-18.0 | Office car park: the wing clips the height bar (bonk); he nods slowly. |
| 11 | 18.0-21.1 | Parked, window down. COWORKER: "Do you actually race?" HIM: "Next season." The coworker's face goes deadpan. |
| 12 | 21.1-22.7 | Tyre check: a gauge on a tyre with full tread and the sticker still on; he writes the pressure on his glove. |
| 13 | 22.7-24.3 | Weather app: one cloud icon; he gasps and covers the wing with a blanket. |
| 14 | 24.3-27.0 | Track entrance: the music cuts dead; cars howl past inside; his hand reaches for the indicator and signals a U-turn. |
| 15 | 27.0-33.0 | Slow push-in on the mirror: his face seen for the first time, helmet on, parked; mouth-revving, imaginary paddle shifts; the timer reads --:--. HIM, whispering: "...next season." Hard cut to black. |

**Sound:** a high-revving turbo four, blow-off, lap-timer beeps, the splitter crunch, the bonk, a choir when the wing
lands, a sad trombone at the U-turn, and silence at the gate.
**Product:** "[BACKORDER] TC Wing - Honda Civic Type R/Sport FK7/FK8", $1,200.00, 66.5 in only (live store, checked
2026-11-18). The owner has been told it's on backorder.
**FK8 model:** Epsilon-Site `wing-configurator/data/models/honda-civic-type-r-fk8-r2.glb` / `-r3.glb` (they exist).

**Open with the owner:** (a) does he get debt/financing numbers like the WRX guy? (b) voices: reuse Bram (HIM) and
Harrison (the coworker), or new ones? (c) approval of the script itself.

**Lessons from #1** (projects/ditl-wrx-vb/editlog.jsonl, feedback.jsonl, review.md):
- Measure the song's BPM and first hit before fixing the cut grid.
- Forms and signs must be readable in a tight opening shot, or the owner says the scene "doesn't explain what's
  going on".
- Hands that hit an object must be parented to that object's space, not the camera's.
- The owner wants parts pulled from the box and thrown onto the car.
- No floating badges, no heads through roofs, real wheels, game textures and crunch on every preview.
- A signature must sit on the paper.
- The engine sound specific to the car mattered to the owner.

**Reusable tools:** projects/ditl-wrx-vb/tools (shots.py, ditl_kit.py, faces.py, textures.py, sound.py with music
modes, frame.sh).
