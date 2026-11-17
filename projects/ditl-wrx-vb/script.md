# DITL #1: "day in the life: average wrx owner" (VB): script v1, 2026-11-17

Step 1 deliverable for the series brief (`projects/ditl-series/BRIEF.md`). **Nothing has been generated or uploaded,
and no credits were spent.** I ran free `get_cost` preflights only. Waiting on the owner.

v1 is built on the owner's backstory, which the parent relayed on 2026-11-17. Where it conflicts with the v0 draft
in the brief, the backstory wins.

**Runtime:** 23.5 s, 9:16, 1080x1920, 30 fps. Three locations, hard cuts, no dissolves, abrupt end.
**Title bar (whole video):** `day in the life: average wrx owner` (lowercase, white on black, top). The exact wording
is open (Q1).
**Production (owner 2026-11-17): all Blender, minimal Higgsfield.** Every shot is a Blender render (Cycles CPU, posterized and crunched in the edit), with phone UI from Remotion. Higgsfield is used only for the voice take (and, if the owner wants, browsing the TikTok music library).
**Premise:** the car is perfect and everything else in his life is not. His VB wears the full Epsilon kit and the
WRC wing, and it is the one genuinely good-looking thing on screen. Everything around it is crunchy, cheap and
sad. We never say whether the kit is worth it, because the car answers that.

## The character
He is a young ex-Marine (dog tags, a tidy haircut, still says "semper fi"). He vapes. He worries about his
ringlands constantly and checks DAM like a heart monitor. He owes $115,000 on a pay-later app at 30 % APR, and every
mod, kit included, went on it. He is sure an intake and a tune can gap anything on the road. He thinks he is
nothing like "those BMW guys", and he is exactly like them.

Character design (owner's note): white or Filipino. In a first-person video that comes down to the skin tone of the
hands and arms, which the owner picks (Q6). **No joke touches ethnicity.** Every joke is about the WRX-owner archetype:
the vape, ringlands, DAM, the debt and intake-and-tune confidence.

## Script (lines, speaker, delivery tags)
Voices: Higgsfield `elevenlabs_v4` dialogue mode, preset voices only (no cloning), one call with emotion tags, never
sped up. HIM is a young male, mid-20s, slightly raspy. MOM is a flat, tired adult female. The take goes to the owner
before any animation. Check the first and last 10-50 ms for clipped phonemes.

| # | Who | Line (tag) |
|---|---|---|
| 1 | HIM | [whispering, tender, ear against the hood] "Ringlands... semper fi." |
| 2 | HIM | [quick, relieved exhale] "DAM's at one. We're good." |
| 3 | HIM | [smug, window down, leaning out] "I'm not like those BMW guys." |
| 4 | HIM | [smug, slower, savouring it] "Intake. And a tune." |
| 5 | MOM | [flat, zero interest] "...Okay." |
| 6 | HIM | [tiny, broken whisper, after a long silence] "...ringlands?" |

That is 6 lines and about 17 words. The jokes are mostly picture and SFX, like the reference.

## Shot table
Times are the target; the voice take sets the final timing. **Music** is a real licensed track (TikTok CML via
`tiktok_music_trending`, or one the owner uploads), loud under S1-S2 like the reference's bed (about 0-11.5 s). It
cuts dead at 10.0 s, on the cut to the red light. S3 is dialogue, engine SFX and room tone only.

| # | Time | Dur | Location | POV action (his hands and arms are always in frame) | Others' reaction | Dialogue / VO | SFX | Product, and the asset it comes from | Method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-1.8 | 1.8 s | Cracked apartment parking lot at dawn; dumpster, a stack of shipping boxes by a dented door | Right hand brings a vape up into frame and takes a long hit. He blows a huge posterized cloud across the hood of his WR Blue VB. | None | (music) | Vape crackle, long exhale | **His car:** VB on the full Epsilon kit: front bumper, rear bumper, side skirts and "WRC Wing – Subaru WRX/STI (VB, 2022+)". Clean, the only nice thing in the lot. `epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb` (`part_front_bumper`, `part_rear_bumper`, `part_side_skirts`, `part_wrc_wing`; duckbill off) | Blender: low-poly lot, GLB car, rigged FPS arm, vapour as a posterized particle/volume puff |
| 2 | 1.8-4.5 | 2.7 s | Same lot, kneeling at the front bumper | He kneels with his ear on the hood. Dog tags swing into frame, and he knocks twice on the hood, gently, like a door. | None | L1 "Ringlands... semper fi." | Knock knock, dog-tag jingle | Same car: Epsilon front bumper fills the lower frame | Blender: same set; camera drops to hood level, arm keyframed knock, dog tags on a 2-bone chain |
| 3 | 4.5-7.2 | 2.7 s | Driver's seat, parked; phone on a dash mount | The phone buzzes. A notification slides down: **"Payment due. Balance $115,000.00 · 30% APR"** (in-world app, see Q2). His thumb swipes it away instantly without him even looking. It is a reflex. | None | (music) | Buzz, swipe whoosh | None on the debt screen (Q2: keep Epsilon off the APR screen) | Blender (static phone on mount + rigged thumb) + Remotion UI on the screen |
| 4 | 7.2-10.0 | 2.8 s | Same seat | Thumb opens a tuner-style gauge app: one big dial, **DAM 1.0**, green. He leans in close, kisses the phone screen, and pats the dash twice. | None | L2 "DAM's at one. We're good." | Phone kiss, pat pat. **Music cuts dead at 10.0 s** | None | Blender + Remotion (same set-up as 3) |
| 5 | 10.0-15.0 | 5.0 s | Red light, 4-lane road. A beige **Honda Odyssey** idles in the next lane, a mom driving and a kid in the back seat | He looks left and rolls the window down. His left arm hangs out and he taps the door to the beat of nothing, then smugly pats the car's roof. | Mom turns her head slowly, a flat painted face that blinks once. The kid presses his face to the glass, grotesquely squished. | L3 "I'm not like those BMW guys." / L4 "Intake. And a tune." / L5 MOM "...Okay." | Window motor, idle burble, a turn-signal tick (the comedic clock) | His own front fender and skirt visible below the window line (Epsilon side skirt) | Blender: our car's door/skirt from the GLB, low-poly minivan, mom and kid low-poly with **flat painted face textures swapped per beat** (neutral, slow-turn, blink, squished-on-glass), like the reference's faces |
| 6 | 15.0-19.5 | 4.5 s | Same road, light goes green | Both hands snap to the wheel and shifter. POV jolts back: full send. The tach needle flicks up (an in-world gauge, no brand), BOV "pssh". The Odyssey glides past on his left, effortless, and keeps going, and the kid waves out the rear window as it pulls away. | Kid waves; mom never looks over | None | Engine scream, BOV, gear crunch, the Odyssey's calm hum fading | None | Blender: camera shake + pitch-back on launch, minivan keyframed past on the left, kid face texture swaps to the grotesque wave |
| 7 | 19.5-23.5 | 4.0 s | Same road, he has lifted | The Odyssey's tail lights shrink to dots on the horizon. Room tone. His hands slowly let go of the wheel. Last, his right hand reaches into frame and rests on the dash, tender. Hard cut on the last word. | None | L6 "...ringlands?" | Silence, a single cooling-fan tick | His wing endplate visible in the rear-view mirror (WRC wing) | Blender: road, low-poly minivan driving away, mirror reflection from the GLB; hands from shot 6's end pose |

**End:** a hard cut to black after L6 at 23.5 s, like the reference. Q4 asks whether to add an Epsilon wordmark card
(about 720 px wide, 2 s, giving about 25.5 s total).

## What I cut from the backstory, and why
- **Dropped out of high school:** cut. It has no picture in 23 s; it would need a line or a diploma prop, and it
  reads as punching down at education rather than at the car archetype. The Marines beat carries his backstory instead.
- **Marines:** kept, but small and affectionate. The dog tags swing while he listens to the engine, and he tells his
  pistons "semper fi". The joke is that he gives his ringlands the loyalty he learned in the Corps, not a dig at the
  service. No uniform, no drill, no recruiter.
- **Vape:** kept as the cold open (shot 1), and it is also how the car is first revealed.
- **Ringland worry:** it opens and closes the video (shots 2 and 7). The callback is the turning point, so it got the
  space.
- **DAM checking:** kept (shot 4), paired with the debt swipe so that one location carries two traits: he ignores the
  number that matters and worships the one that doesn't.
- **$115k at 30 % APR on Affirm, everything financed:** kept as the debt notification he swipes away. The real
  "Affirm" name and logo are held until the owner answers Q2/Q3, so the default is a neutral in-world app. The
  Epsilon kit is never shown on the debt screen (Q2).
- **"No better than the BMW guys":** one line (L3) that he says to the minivan just before he loses to it.
- **"Intake and a tune can gap anything" / gapped by an Odyssey:** kept as the closer (shots 5-7), as the parent
  suggested.
- **From v0, also cut:** the drive-thru rumble video, the cladding slap, the meet with someone else's kitted VB, the
  BUY button and the CEL ending. His car now *is* the kitted car, so the product is the aspirational object he
  already owns, and the stealth insert is in almost every shot instead of one.

## Asset inventory
| Asset | Status | Source / plan |
|---|---|---|
| VB with Epsilon front bumper, rear bumper, side skirts, WRC wing | **found** | `epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb` (attached via `add_repo`; nodes listed in `showroom/models/cars/subaru-wrx-vb.md`) |
| WR Blue paint | **found** (approx.) | `glb_ref_render.py` colour `wrblue` (0.02, 0.12, 0.55). Confirm, or use the store's paint-match swatch |
| Look-test frames (kit, WR Blue, Cycles CPU) | **made** (local) | `/home/user/media/ditl-wrx-vb/look_*.png` (media, not committed) |
| FPS arms and hands (vape, dog tags, thumb) | **to make** | Blender: one low-poly rigged arm pair (vape, dog tags, thumb poses), skin tone per Q6 |
| Apartment lot, road, red light | **to make** | Blender low-poly, posterized |
| Minivan (Odyssey) | **missing** | No GLB of ours. A generic low-poly minivan modelled in Blender, no badge unless the owner OKs the name (Q3) |
| Phone UI: debt notification, DAM gauge | **to make** | Remotion (new small composition), no real-app branding unless approved |
| Title bar | **to make** | ffmpeg/Remotion, series wording |
| Voice take | **to make** | `elevenlabs_v4` dialogue, one call (after approval) |
| Music | **to pick** | TikTok CML via `tiktok_music_trending` (check it isn't used by another reel) or an owner upload |
| SFX | **to make/find** | Vape, knocks, phone buzz, BOV, engine, minivan hum: royalty-free or synthesized locally |
| Epsilon+ wordmark (if Q4 yes) | **found** | Drive `EPSILON+ Logos` |
| Reference clip | **missing here** | Owner upload, not in repo; parent's contact sheet is enough for pacing |

## Credit estimate
Balance 290.46 credits for all six videos (checked today), about 48 per video. Free `get_cost` preflights today, for
reference: Kling 3.0 8.75 / 5 s, Seedance 2.5 35 / 5 s, GPT Image 2.6 still 0.25. A dialogue voice take is about 2.5
(Pip & Gus precedent).

**Chosen (owner): Blender only.**
| Item | Credits |
|---|---|
| All 7 shots: Blender + Remotion, local | 0 |
| Voice take (`elevenlabs_v4` dialogue, 6 lines, 2 voices) | ~2.5 |
| One voice retake, if needed | ~2.5 |
| **Total** | **~2.5-5** |

Nothing is uploaded to Higgsfield. The voice call sends only the script text. The trade-off is that faces are flat
painted textures swapped per beat, not animated acting. That matches the reference's look, so I consider it a fit,
not a loss. The cost is build time: a low-poly lot, a road, a minivan, a rigged FPS arm and 3 face sheets.

## Open questions for the owner
1. **Title text:** `day in the life: average wrx owner`, or your wording "DITL of average WRX owner"?
2. **Affirm / the APR on our product.** I checked the live store: epsilon.plus offers **Shop Pay Installments**
   (Shopify's pay-over-time, with 0 % and 15 % APR plans configured on the WRC wing and front bumper pages). There is
   **no Affirm branding and no 30 % plan** on the site. Showing "Affirm, 30% APR" on an Epsilon checkout would
   misstate our own terms, so v1 puts the $115k / 30 % APR on **his phone** (a debt notification), not on our
   checkout, and the kit never appears on that screen. OK? And do you want that app to be called **Affirm** by
   name, or a made-up look-alike?
3. **Real brands:** OK to name and show a **Honda Odyssey** (the line never says it; we'd show a minivan, badge or not
   is your call) and to say **"BMW guys"** out loud? Affirm is covered in Q2.
4. **End card:** a hard cut to black on "...ringlands?" like the reference (my pick, it's funnier), or end on the
   Epsilon+ wordmark card (about 720 px, about 2 s)? The product link goes in the caption either way.
5. **"DAMM" or "DAM":** the Accessport value is DAM (Dynamic Advance Multiplier). Spoken, it's "dam" either way;
   on the phone screen I'd write **DAM**. Keep your "DAMM" spelling? The screen shows "DAM 1.0" (a healthy reading, a
   character prop, not a product claim). OK?
6. **The hands:** lighter or medium-brown skin for his arms (your note: white or Filipino)? Dog tags OK?
7. **Voice:** OK to spend about 2.5 credits on the voice take (preset voices, script text only) once the lines are
   approved? Or would you rather record HIM yourself?
8. **Music:** do you have a track in mind, or should I pick from the TikTok Commercial Music Library (loud bed under
   0-10 s, then dead silence)?

## Look test (local, no credits)
`/home/user/media/ditl-wrx-vb/look_front34.png`, `look_rear34.png` and the posterized pair `look_sheet.jpg` (media,
not committed). These are Cycles CPU renders of `eps-subaru-wrx-vb-v3.glb` with the kit (duckbill off, WRC wing on),
in WR Blue, posterized to about 5 levels per channel. The Epsilon bumpers, skirts and the WRC wing's element and
endplates all stay readable in the crunchy look. The banding in the flat grey backdrop is the look-test floor and
will be replaced by the low-poly lot.
