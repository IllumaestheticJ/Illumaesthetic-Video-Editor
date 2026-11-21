# gta6-mr2-spyder: self-review

## v1 (2026-11-20)
Output: `/home/user/media/work/out/gta6-mr2-spyder_v1.mp4`, 1080x1920, 30 fps, 39.3 s (1,105 shop frames + 2.5 s card).
Brief: the Civic reel (`projects/gta6-customs`, v19) for the MR2 Spyder kit, lookbook game model, lore-accurate name.

What was checked by looking (delivery size): one frame per purchase (11) with the pop-up up; one frame from each of the 20 whips; the
list, respray, exit and card; a strip of the whole reel; every clean plate. Twice: after the first composite and after the fixes.
What was checked by measurement: frame count against the timeline; the event list; speech band (300-3000 Hz) after every purchase
(back at room tone, -54 dB) and at the mechanic's line (-26 dB, once, at 34.97 s). Not checked by ear: I cannot hear.

Rubric (1-5; the scan-reel criteria that do not apply are marked n/a)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 3 | list for 1 s, first whip at 1.0 s, first purchase at 1.7 s; same opening as the Civic reel |
| 2 | Beat sync | n/a | no music cut; game sounds on the frame of each action |
| 3 | 1:1 match | n/a | |
| 4 | Car in scene | 3 | covers the game's car in every view; reads as a clean render in a photoreal shop, larger against the room than a real MR2 |
| 5 | Story | 4 | stock silver > eight parts one by one through the list > respray to Solar Yellow > lowered > 6-spoke wheels > line > card |
| 6 | Grade | 3 | capture A sunny, capture B overcast, as in the Civic reel |
| 7 | Text | 4 | catalogue prices, live wallet 4,780 > 0, game titles kept; the hardtop's 50 is labelled as a deposit |
| 8 | Ending | 2 | **placeholder**: white wordmark on black; the owner's palm-sunset image is not in Dropbox. No radio bed either |
| 9 | Technical | 4 | 1080x1920, 30 fps, yuv420p, AAC, faststart; forward frames only; nothing sharp held in whips but lettering and the game's panels |

Holds up
- Every part is entered from the list and left back to it; bought rows carry the marker; the cursor moves down one each time.
- Each part is in frame on its own camera and appears with the game's purchase sound, "Applied" and the drawn "Purchased" pop-up.
- Stats panel, car tag, wallet, EPSILON+ badge and price on all eight part screens, built by one function.
- No scrap of the game's car at any purchase frame after the second pass.

Weak, known
- **End card and radio are missing** (files not supplied). The reel is not final until they are in.
- **Length against the radio clip**: the shop section is 36.8 s; the Honey FM clip has 28.8 s of music. It cannot cover the section unbroken.
- The MR2 is drawn larger than life against the room (camera moved in until it covers a 5.2 m game car). Most visible on the list screen.
- Eyelids are a small change on a front view 3.7 m away; the diffuser is dark under a dark tail. Both read, neither is striking.
- Spats and diffuser share the rear camera, bumper and eyelids the front camera: two pairs of similar shots.
- Rear view: the tail fills the frame and the roof is cut by the top edge; the title sits over the car with a halo.
- Hardtop is seen from behind and above (the roof camera could not be covered); the change is a black fabric roof turning body colour.
- Background beside the car is invented in every view (1-9 % of the frame): mirrored wall and floor; soft behind the wheel close-up.
- Respray screen: the swatch row and counter overlap the car's nose, as the game's block does on its own car.
- The model wears Toyota and MR-S badges under a Karin tag. Stock wheels are the model's stand-ins (not the OEM design).
- Eleven purchases and twenty camera moves in 37 s is busy; part screens are 1.8 s.
- Parts are fibreglass-only in the catalogue: prices are for unpainted parts, shown paint matched.

Final pass (same day): after the fixes the whole section was composited again twice; all 11 purchase frames and one frame of each of the
20 whips were looked at again at delivery size. Left in: a few-pixel mirrored copy of the game's "..." icon beside the stats panel on the
two rear-view screens; the wallet icon is absent on the wheel screen.

## v2 (2026-11-20) - after the owner's review of v1
Owner: "need to start with stock bumper"; "hood needs to be cutout for the hood vents"; "fender needs to be trimmed for new skirts"; "the rear
TC spoiler needs to be added"; "the rear tail light needs the original OEM textures put back in"; "some of the asset blurring needs to be done
better / artificially filled"; "the rear diffuser being added needs to change the exhaust position so it clears"; "at the 0:01 transition, the
aftermarket bumper flashes on the car"; "the polygon quality of the model is also visibly low"; "relabel 'Diffuser V1+' to rear diffuser".

What changed (edit log has each with its reason): a corrected copy of the game model (`tools/reel_model.py`): smooth shading, hood cut under the
vents, fender trimmed from the owner's scan of the cut piece, right-side skirt, TC wing from the kit file, raised exhaust with the diffuser,
the rip's lights texture on the tail lamps. TC Wing is a ninth purchase ($1,100, BACKORDER badge; wallet 5,880 > 0). Whips show the car as it is
before each purchase and the part screen holds that state 0.67 s. "Rear Diffuser". Fills keep their sharpness (seam only softened). End card on
the owner's palm-sunset image (arrived on their Drive). Every still and whip rendered again.

Lessons
- I delivered v1 with a whip that showed the next part early, to save renders. A reused render must match the state at that moment; "a blur
  hides it" was wrong for a bumper.
- I took the game model as given. Its notes said plainly that the hood cut-outs were "not modelled" and the wing "not exported", and the first
  renders showed flat shading and plain red lamps. Those were questions to raise before rendering 114 images, not after.
- A selection made per connected piece judged by its first face skipped most of the tail-lamp faces; list what is in the volume first.

Output: `/home/user/media/work/out/gta6-mr2-spyder_v2.mp4`, 1080x1920, 30 fps, 44.6 s (1,263 shop frames + 2.5 s card).
Checked by looking (delivery size): all 12 purchase frames; one frame of each of the 22 whips, the first one for the stock bumper; the splice
at frame 1150 (the compositor was killed for memory 76 frames from the end: caches now 8-bit, tail rendered and joined, frame count 1,263);
the card on the owner's image; tail lamp, hood openings and exhaust in close studies before the full render.
Checked by measurement: speech band back at room tone after each of 12 purchases; the line once at 40.23 s. Not checked by ear.
Still weak: no radio bed (clip not supplied; shop section 42.1 s against 28.8 s of music); the MR2 larger than life against the room; the
wing's finish (black) and the exhaust placement are mine; the stock car shows a dark gap behind the front wheel arch at the sill (in the
published model, not asked about); background beside the car invented in every view; a small mirrored game icon beside the panel on the rear view.

## v3 (2026-11-21) - radio bed
Owner: "I added music to Moosic folder for the background GTA6 radio" (a 98.5 s phone screen recording of a YouTube "GTA VI Club Radio" mix).
Output: `/home/user/media/work/out/gta6-mr2-spyder_v3.mp4`, 44.6 s. Picture as v2; sound = v2 + the radio as one unbroken bed (edit log).
Measured: bed about -32 dB between events, purchases and the line 5-7 dB over it, music's break on the cut to the card. Not checked by ear:
level, how muffled it sounds, and whether the phone recording carries any notification sound are for the owner to judge.

## v4 (2026-11-21)
Owner: "too loud, needs to be background radio volume". Radio bed 9 dB lower (about -40 dB between events); picture and other sound as v3.
Output: `/home/user/media/work/out/gta6-mr2-spyder_v4.mp4`. Lesson: a level copied from another reel does not carry over to a denser track.
