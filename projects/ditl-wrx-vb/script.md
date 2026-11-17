# DITL #1: "day in the life: average wrx owner" (VB): script v2, 2026-11-17

Step 1 deliverable for the series brief (`projects/ditl-series/BRIEF.md`). **Nothing has been generated or uploaded,
and no credits were spent.** I ran free `get_cost` preflights only. Waiting on the owner.

## Owner decisions in v2 (2026-11-17, relayed by the parent)
- **Production: all Blender, minimal Higgsfield** (owner in this chat). Every shot is a Blender render (Cycles CPU,
  posterized and crunched in the edit), and the phone and Accessport screens come from Remotion. Higgsfield is used
  only for the voice take.
- **DAM**, not "DAMM".
- **Real brands are OK:** Affirm, Honda Odyssey, BMW, Cobb Accessport. (The account isn't an LLC account and isn't
  monetized.)
- **Runtime up to 55 s:** the traits come back, in about 8 scenes, with tight pacing and no padding.
- **Affirm at 30 % APR shows on the Epsilon checkout.** The joke is that it's the lowest APR he can get. This is the
  owner's call. For the record: the live epsilon.plus product pages run Shop Pay Installments (0 % and 15 % APR plans),
  not Affirm. The owner chose to show Affirm anyway, so the video doesn't state our real terms.

**Runtime:** about 47.5 s, 9:16, 1080x1920, 30 fps. Eight scenes, hard cuts, no dissolves, abrupt end.
**Title bar (whole video):** `day in the life: average wrx owner` (lowercase, white on black, top). Confirm the wording
(Q1).
**Premise:** the car is perfect and everything else in his life is not. His VB wears the full Epsilon kit and the
WRC wing, and it is the one genuinely good-looking thing in every frame it's in.

## The character
He dropped out of high school and went straight into the Marines. He still says "semper fi", now mostly to his
pistons. He vapes. He worries about his ringlands constantly and checks DAM on the Accessport like a heart monitor.
He owes $115,000 on Affirm at 30 % APR, and every mod, the Epsilon kit included, went on it. He is sure an intake and
a tune can gap anything on the road. He is exactly like the BMW guys.

Character design (owner's note): white or Filipino. In first person that means the skin tone of the hands and arms
(Q4). **No joke touches ethnicity.** The Marines beats stay affectionate: the Corps is the one thing in his life that
works, and the jokes land on him and the car, never on the service.

## Script (lines, speaker, delivery tags)
Voices: Higgsfield `elevenlabs_v4` dialogue mode, preset voices only (no cloning), one call with emotion tags, never
sped up. HIM: a young male, mid-20s, slightly raspy. RECRUITER: a booming, warm Marine. BMW GUY: a smug male, 30s.
MOM: a flat, tired female. The take goes to the owner before animation. Check the first and last 10-50 ms of the
take.

| # | Scene | Who | Line (tag) |
|---|---|---|---|
| 1 | 2 | HIM | [whispering, tender, ear on the hood] "Ringlands... semper fi." |
| 2 | 3 | HIM | [quick, relieved exhale] "DAM's at one. We're good." |
| 3 | 4 | RECRUITER | [booming, delighted] "Welcome to the Corps, son!" |
| 4 | 4 | HIM | [eager, too fast] "Do I get a WRX?" |
| 5 | 4 | RECRUITER | [beat, warm] "...You get a signing bonus." |
| 6 | 5 | HIM | [proud, like he won something] "Thirty percent. Lowest they'd give me." |
| 7 | 6 | BMW GUY | [suspicious, nodding at the car] "That tuned?" |
| 8 | 6 | HIM | [smug] "Intake and a tune." |
| 9 | 6 | BMW GUY | [smug, identical] "Same." |
| 10 | 7 | HIM | [smug, leaning out the window] "You might wanna sit this one out, ma'am." |
| 11 | 7 | MOM | [flat, zero interest] "...Okay." |
| 12 | 8 | HIM | [tiny, broken whisper, after a long silence] "...ringlands?" |

That is 12 short lines, about 50 words. Most of the comedy is picture and SFX, like the reference.

## Shot table
Times are the target; the voice take sets the final timing. **Music:** a real licensed track (TikTok CML via
`tiktok_music_trending`, or one the owner uploads), loud under scenes 1-6 like the reference's bed. It **cuts dead at
the red light** (32.0 s). Scenes 7-8 are dialogue, engine and room tone only. Everything is **Blender** unless noted;
faces are low-poly heads with **flat painted face textures swapped per beat**, the reference's horror-face style.

| # | Time | Dur | Location | POV action (his arms are always in frame) | Others' reaction | Dialogue | SFX | Product, and the asset it comes from | Method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-4.0 | 4.0 s | Bedroom, 5:00 AM. A mattress on the floor, a WRX poster, dog tags and a vape on the nightstand | The alarm goes off. A hand slaps it, misses, slaps it again. The same hand grabs the vape without looking and takes a huge hit. The cloud fills the whole room (posterized blob). | None | (music) | Alarm, slap slap, vape crackle, long exhale | None | Blender |
| 2 | 4.0-9.0 | 5.0 s | Cracked apartment lot at dawn; a dumpster, a stack of shipping boxes | Walks out. His WR Blue VB sits in the lot spotless, the only clean thing in the world. He kneels with his ear on the hood. The dog tags swing into frame, and he knocks twice, gently, like a door. | None | L1 | Footsteps, knock knock, a dog-tag jingle | **His car:** VB with the Epsilon front bumper, rear bumper, side skirts and "WRC Wing – Subaru WRX/STI (VB, 2022+)". `epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb` (`part_front_bumper`, `part_rear_bumper`, `part_side_skirts`, `part_wrc_wing`; `part_duckbill` **off**; he buys it in scene 5) | Blender |
| 3 | 9.0-15.0 | 6.0 s | Driver's seat, parked | He boots the **Cobb Accessport** on the dash: a big **DAM 1.0** readout. He leans in, kisses the screen and pats the dash. The phone in the cupholder buzzes: **"Affirm · Payment due · Balance $115,000.00 · 30% APR"**. His thumb swipes it away instantly without looking. It's a reflex. | None | L2 (before the buzz) | Accessport chime, kiss, pat pat, buzz, swipe | Accessport (a generic low-poly unit with the Cobb wordmark) and the Affirm notification | Blender + Remotion screens |
| 4 | 15.0-21.0 | 6.0 s | **Flashback:** a high school classroom, then the recruiting office across the hall. Grade it extra crunchy, with no "years ago" text | A test paper on the desk. The hands put the pencil down, stand up and walk out mid-test, straight through the door into a Marine Corps recruiting office. He gets an instant salute and returns it, with the vape still in his hand. | The teacher's face: slow horror. The recruiter's face: overjoyed. | L3, L4, L5 | Chair scrape, door, a bugle sting under L3 | None | Blender |
| 5 | 21.0-27.5 | 6.5 s | Present day, his bed at night, lit by the phone | Phone: the **epsilon.plus** product page for **"[BACKORDER] Rear Duckbill - Subaru WRX (VB, 2022+)"** ($125.00, the live store price). Add to cart, then checkout. The payment step shows **Affirm**, a single plan, **30% APR**. His thumb hovers for a second, then he smashes **Place order**. | None | L6 (on the APR) | Tap, tap, a "cha-ching", a tiny fanfare | **The Epsilon checkout** + the duckbill (a render of `part_duckbill` from the GLB as the product image) | Remotion (store UI recreated from the live page) + Blender hands/phone |
| 6 | 27.5-32.0 | 4.5 s | Gas station, 93 octane | He holds the pump nozzle up proudly. At the next pump, a **BMW** guy with the exact same posture is also holding up his nozzle. They lock eyes over the pumps. A long silent stare. Both faces slowly warp into mirrored horror: he is looking at himself. | The BMW guy mirrors him exactly | L7, L8, L9 | Pump click, a fluorescent hum, then silence on the stare | His car (kit) in the foreground, against the BMW at the next pump | Blender (low-poly generic BMW sedan with the roundel, no exact model) |
| 7 | 32.0-38.0 | 6.0 s | Red light on a four-lane road. **Music cuts dead.** A beige **Honda Odyssey** idles next to him: a mom driving, a kid in the back | He rolls the window down, revs twice, and leans out smugly. His left arm drums on the door. | The mom turns her head slowly: a flat face, one blink. The kid presses his face to the glass, grotesquely squished. | L10, L11 | Window motor, 2 revs, turn-signal tick (the comedic clock) | His own door and the Epsilon side skirt visible below the window line | Blender (low-poly Odyssey, H badge, no exact model) |
| 8 | 38.0-47.5 | 9.5 s | Same road, the light goes green | Both hands snap to the wheel and shifter. Full send: the camera pitches back, the tach flicks up, and the BOV goes "pssh". The Odyssey **glides past on the left**, effortless. The kid waves out the rear window as it pulls away. He lifts. The tail lights shrink to dots. Room tone. He looks down at the Accessport: **DAM 0.88**. Long silence. His hand rests on the dash. Hard cut on the last word. | Kid waves; mom never looks over | L12 | Engine scream, BOV, gear crunch, the Odyssey's calm hum fading, one cooling-fan tick | The WRC wing endplate in the rear-view mirror, and the Accessport | Blender + Remotion (Accessport screen) |

**End:** a hard cut to black after L12 at about 47.5 s, like the reference (Q3 asks whether to add an Epsilon wordmark
card instead).

## What changed from v1, and why
- **Runtime 23.5 s to about 47.5 s, 3 scenes to 8.** The owner allowed up to 55 s, so most traits got their own beat,
  each 4-6.5 s with a hard cut and nothing padded.
- **The dropout and the Marines are back as one flashback (scene 4).** He walks out of a test straight into the
  recruiter's office. The punchline is his "Do I get a WRX?" and the recruiter's kind "...You get a signing bonus",
  which also explains how he could afford anything. The joke is on him, not the Corps.
- **Debt is split in two:** the $115k notification he swipes away (scene 3), and the checkout where 30 % APR is the
  "lowest they'd give me" (scene 5, owner's joke). He finances a $125 duckbill at 30 %, which also puts a second
  Epsilon product on screen.
- **BMW guys get their own scene (6):** the gas-pump mirror stare, so "no better than the BMW guys" is shown, not
  said.
- **The Odyssey pull stays last (scenes 7-8)**, where it hits hardest: the music cuts dead at the light, and the
  gap is followed by the DAM drop and "...ringlands?", which closes the loop from scenes 2 and 3.
- **Cut from v0, still out:** the drive-thru rumble video, the meet with someone else's kitted car, the CEL ending.

## Asset inventory
| Asset | Status | Source / plan |
|---|---|---|
| VB with the Epsilon front/rear bumper, side skirts, WRC wing, and the duckbill (separate) | **found** | `epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb` (attached via `add_repo`; nodes in `showroom/models/cars/subaru-wrx-vb.md`) |
| WR Blue paint | **found** (approx.) | `glb_ref_render.py` colour `wrblue`; confirm or use the store's paint-match swatch |
| Look test (kit, WR Blue, posterized) | **made** (local) | `/home/user/media/ditl-wrx-vb/look_*.png`, `look_sheet.jpg` (media, not committed) |
| Duckbill product page + checkout | **to make** | Remotion, laid out like the live epsilon.plus product page; title and $125.00 from the live store (checked 2026-11-17); product image = Blender render of `part_duckbill`; Affirm step per the owner |
| Cobb Accessport screen, Affirm notification | **to make** | Remotion |
| FPS arms (vape, dog tags, pencil, pump nozzle, thumb poses) | **to make** | Blender: one low-poly rigged arm pair, skin tone per Q4 |
| Sets: bedroom, lot, car interior, classroom + recruiting office, gas station, road | **to make** | Blender low-poly, flat colours, posterized in the edit |
| Honda Odyssey, BMW sedan | **missing** | Low-poly stand-ins modelled in Blender, with the H badge and the roundel; not exact models |
| Characters: teacher, recruiter, BMW guy, mom, kid | **to make** | Low-poly bodies + flat painted face sheets (2-3 expressions each), the reference's style, original designs |
| Voice take | **to make** | `elevenlabs_v4` dialogue, 4 preset voices, one call (after approval) |
| Music | **to pick** | TikTok CML (check it's not used by another reel) or an owner upload |
| SFX | **to make/find** | Royalty-free or synthesized locally |
| Epsilon+ wordmark (only if Q3 is yes) | **found** | Drive `EPSILON+ Logos` |

## Credit estimate (owner: Blender, minimize Higgsfield)
Balance 290.46 credits for all six videos (checked today). For reference, from free `get_cost` preflights: Kling 3.0
costs 8.75 per 5 s and Seedance 2.5 costs 35 per 5 s, so an AI version of 47 s would run about 80-330 credits.

| Item | Credits |
|---|---|
| All 8 scenes: Blender + Remotion, local | 0 |
| Voice take (12 lines, 4 voices, one dialogue call) | ~3-4 |
| One retake if needed | ~3-4 |
| **Total** | **~3-8** |

The only thing sent to Higgsfield is the script text for the voice. The cost is build time: 6 low-poly sets, 2
stand-in cars and 5 face sheets. I'd build in the order 2 → 3 → 7/8 → 5 → 6 → 1 → 4, so the product shots are
locked first.

## Open questions for the owner
1. **Title text:** `day in the life: average wrx owner`, or "DITL of average WRX owner"?
2. **The duckbill at checkout:** it's the one kit part his car is missing, and its live listing title starts
   "[BACKORDER]". Show the real title and badge, or should he check out a different part (e.g. the GT wing, $1,990)?
3. **End card:** a hard cut to black on "...ringlands?" like the reference (my pick), or the Epsilon+ wordmark card
   (about 720 px, about 2 s)?
4. **Hands:** lighter or medium-brown skin (your note: white or Filipino)?
5. **Voice:** OK to spend about 3-4 credits on the voice take once the lines are approved?
6. **Music:** do you have a track in mind, or should I pick one from the TikTok Commercial Music Library?
7. **DAM 0.88 after the pull:** the drop is a prop for the joke (DAM falls when the ECU sees knock), not a claim about
   the car. Is it OK, or should the screen just flash or blink?

## Look test (local, no credits)
`/home/user/media/ditl-wrx-vb/look_front34.png`, `look_rear34.png` and the posterized pair `look_sheet.jpg` (media,
not committed). These are Cycles CPU renders of `eps-subaru-wrx-vb-v3.glb` with the kit (duckbill off, WRC wing on),
in WR Blue, posterized to about 5 levels per channel. The Epsilon bumpers, skirts and the WRC wing all stay readable
in the crunchy look. The banding in the grey backdrop is the look-test floor, which the lot will replace.
