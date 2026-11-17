# "Day in the life of the average ___ owner": series brief

Written by the parent (master) session on 2026-11-17. There are 6 videos and one session per video. The parent
session does the final inspection of every cut and holds the series-wide decisions.

Parent session ID: `session_01KS3BnjWt7yPCihfhKkVHD2`. Report there with `send_message`.

## The ask (owner's words, condensed)
"We are going to make a set of funny, comedic, satirical, stereotypical and erratic videos like the one provided,
using this video as similar as possible. First person, in the style of 'day in the life of XX car owner'.
Over the top. Stealth insert Epsilon products, such as the WRX body kit/wing, or the TC wing."

## The reference clip (owner upload, not in the repo)
A 720x1280, 30 fps, 24.2 s clip. It is not committed, because media is never committed. Ask the owner to attach it in
your chat if you need to watch it. What the parent measured:
- `reference/reference_contact_sheet_2fps.jpg`: 48 frames at 2 fps.
- `reference/reference_audio_spectrogram.png`: the audio.
- **Look:** a low-poly "simulator" video game, posterized and crunchy. A first-person POV with bare arms always in
  frame, doing strange things. The other characters are low-poly with flat painted faces that make big distorted
  horror expressions.
- **Title bar:** a persistent black bar at the top with white lowercase text ("noah simulator"). It stays on the
  whole time.
- **Structure:** 3 locations in 24 s. Hard cuts at 3.17 s and 8.73 s, found with scene detection.
  1. 0-3.2 s, cold open: running down a suburban street after someone.
  2. 3.2-8.7 s, errand: a drive-thru window, and the hands fumble something at the worker.
  3. 8.7-24 s, one long escalation: a restaurant counter. The hands press a big "money" box, then poke the cashier's
     face over and over while she makes horrified faces. It ends abruptly, with no punchline card and no CTA.
- **Audio:** about 0-11.5 s is a loud music bed with a voice over it. After that, dialogue/voice plus SFX over room
  tone. It is not transcribed (speech-to-text could not be installed here); ask the owner what the voice says if
  it matters.
- **Do not copy:** their title, the restaurant name and signage, their characters, or the "skullmug" watermark.
  Copy the format, the pacing and the energy. The content stays original (house rule: no recreations of an
  existing game or video).

## Series format (parent decisions; the owner can override)
- **Frame layout (measured on all 3 owner references, 2026-11-17):** 1080x1920 canvas, black, with the game picture a
  **1080x1080 square at y=420-1499**. The title sits in the black band above (two lines if long); black below. Render
  the game shots 1:1, not full-bleed 9:16.
- **Look:** early-2000s game, photo-ish textures, realistic hands, soft light (NOT hard posterization). Talking
  characters move their mouths. 2-4 s per shot. Owner reference clips: /home/user/media/ditl-wrx-vb/ref/ in the WRX
  session (not committed): "noah simulator", "bad day simulator", "your friend who loves hypotheticals".
- 30 fps, **up to 55 s** (owner, 2026-11-17), as many locations as the story needs with tight pacing, a hard cut between scenes, no dissolves.
- Top title bar for the whole video, lowercase white on black: **`day in the life: average <car> owner`** (the
  owner's wording is "DITL of average WRX owner"; confirm the exact title text with the owner).
- First person: the viewer IS the owner. Their arms and hands are always in frame and act erratically.
- The other characters react with deadpan or horror. The humour is satire of the owner archetype, never of the
  Epsilon product. **The Epsilon part is always the one thing that looks genuinely good** (the "aspirational
  object").
- **Stealth insert:** the product is in the shot and accurate (our part geometry, real part names, live prices),
  but with NO Epsilon logo, wordmark, store UI or end card (owner, see Owner answers). The link goes in the post caption.
- Abrupt ending on a gag (hard cut), like the reference.

## Owner answers (2026-11-17)
- Real brand names are OK (Affirm, Honda Odyssey, BMW, Cobb...): not posted on an LLC account, not monetized.
- Max length 55 s.
- WRX: use "DAM" (Accessport Dynamic Advance Multiplier).
- **No Epsilon branding (series-wide, owner via the WRX session):** no Epsilon+ watermark, logo, end card or epsilon.plus
  store UI. The products appear (accurate parts, real part names, live prices) without it being obvious they are
  from Epsilon. Checkout screens are a generic unbranded store. End on a hard cut to black.
- Title style: "Day in the life of an average <car> owner".
- Affirm at checkout is OK ("Shop Pay is technically under Affirm": Shop Pay Installments is powered by Affirm).
- Music: real tracks; the owner may upload commercial tracks (e.g. Illenium-style EDM) since the account is unmonetized.
- Voices: show the owner the Higgsfield voice options (previews) before generating.

## House rules that apply (from CLAUDE.md and knowledge/lessons.md: read them)
- **Never invent numbers on screen or in narration:** no downforce figures, lap times, prices or specs unless they
  are sourced. Prices only from the live Shopify store (Shopify MCP, store "Epsilon+ Aerodynamics").
- **Music:** real music only, no generated tracks. The owner rejected generated music as "slop". Licensed options:
  the TikTok Commercial Music Library via Higgsfield `tiktok_music_trending`, or a track the owner uploads. Mix at
  -14 LUFS with true peak below -1 dBFS. Cut on measured hits.
- **Voices:** no cloning of real people. The precedent is the Pip & Gus series (branches `origin/claude/pip-gus-ep*`,
  e.g. `git show origin/claude/pip-gus-ep0-intro:projects/pip-gus-ep0-intro/script.md`): Higgsfield
  `elevenlabs_v4` dialogue mode with emotion tags, one call per dialogue take, and the voice take goes to the owner
  **before** animation. Check the first and last 10-50 ms of every take for clipped phonemes (lesson from
  epsilon-wing-configurator v5).
- **Product accuracy:** Epsilon parts come from our own models (below), never an AI's guess at the part. AI may
  stylise a frame, but the kit/wing silhouette must stay right.
- Log every decision with its reason: `python -m ive log projects/<p> "<what>" --why "<why>"`.
- Look at your own output (frames, contact sheets) before reporting anything as good.

## Spending (important: shared account)
- The Higgsfield account has about **295 credits** for ALL six videos (checked 2026-11-17).
- **Do not upload anything to Higgsfield or any other external service, and do not generate anything, until the
  owner approves it in your chat.** The owner stopped the parent's first upload. Ask first: say what you would
  upload (our renders? the reference frames?) and give a credit estimate (`get_cost: true` preflight).
- Local work (Blender, ffmpeg, Remotion) needs no approval.

## Assets
- **Epsilon showroom car GLBs** (private repo `IllumaestheticJ/Epsilon-Site`; attach it with `add_repo`, read
  access): `showroom/models/eps-<car>-v<N>.glb`. These are game-model cars with `body_*_stock` parts plus
  `part_*` Epsilon parts, documented in `showroom/models/cars/<car>.md`. Available: subaru-wrx-vb (WRC wing, front
  bumper, rear bumper, side skirts, duckbill), toyota-gr86-zd8, honda-civic-fg2, mazda-mx5-nc and others (`ls`).
- **Wing configurator models:** `wing-configurator/data/models/*.glb` (car models incl. honda-s2000, mazda-mx5-na,
  honda-civic-type-r-fk8, honda-civic-fg2, subaru-wrx-vb) plus wing/base/cradle meshes in `wing-configurator/data/`
  (`gt-wing-mesh.json`, `base-meshes.json`, `cradle-meshes.json`). The TC wing is built there. Precedent:
  `projects/epsilon-wing-configurator`.
- `tools/glb_ref_render.py`: Blender (Cycles CPU; EEVEE has no GPU here) reference render of a showroom GLB,
  stock vs kit, any paint colour. Usage: `blender -b --python tools/glb_ref_render.py -- kit white 140 12 out.png`
  (variant, colour, azimuth, elevation, output path). Example output: `reference/wrx_vb_stock_vs_kit_glb.jpg`.
- Our scan data (silver look) and shop footage: see `knowledge/sources.md`, `knowledge/car-inventory.md`. Probably
  not needed for this series, which is a game-look world.
- Characters: `knowledge/characters/del-and-eps` (the Epsilon characters, arcade-racing-game style). They are not
  the protagonist here (the POV owner is), but a cameo is the owner's call.

## Production approach (open: the owner decides; propose a recommendation in your chat)
- **A. Blender:** a low-poly world built in Python, our GLB cars flat-shaded and posterized, FPS arms, characters
  with swappable flat face textures. It is fully controllable and product-accurate, but slow to build, and facial
  acting is hard.
- **B. Higgsfield AI video** (e.g. Seedance 2.5 omni_reference with start_image, Kling 4.0, Grok Video 1.5): fast,
  good at erratic POV acting and faces, weaker on consistency and on product accuracy.
- **C. Hybrid (the parent's recommendation):** Blender renders of our GLB cars and parts are the start frames and
  references; AI animates the character/POV action; any shot where the product is the focus stays a Blender
  render (or is checked frame by frame against it). Posterize and grade everything the same way in the edit so it
  reads as one game.

## Your deliverable, step 1 (in your own chat; stop after this and wait for the owner)
`projects/ditl-<slug>/script.md` with:
1. the script, revised to be funnier and tighter: lines, who says them, and the delivery tags;
2. a numbered shot table: time, duration, location, POV action, other characters' reactions, dialogue/VO, SFX,
   the exact product and the asset path it comes from, and the method (Blender / AI / hybrid);
3. the asset inventory (found / missing / to make);
4. a credit estimate per approach;
5. open questions for the owner.

Optionally (local only, no credits): 1-3 Blender look-test frames of the car and product in the simulator look.

Commit and push to branch `claude/sleepy-cannon-1dulxu` (`git pull --rebase` first: six sessions share it, each in
its own `projects/ditl-<slug>/` folder; never touch another session's folder or `projects/ditl-series/`, which the
parent owns). Never open a PR. Then reply in your chat with a short summary and your questions, and send the parent
a one-paragraph status with `send_message` to `session_01KS3BnjWt7yPCihfhKkVHD2`.

## Later steps (after owner approval in your chat)
Voice take, then owner check, then animation/renders, then assembly. Then send the cut to the parent for final
inspection BEFORE you tell the owner it is done. After that: `ive feedback`, `review.md` against
`training/rubric.md`, `ive archive`, commit, push.

## The six videos (draft scripts v0, reviewed by nobody yet; each session owns one)
Product names are exact listing titles from Epsilon-Site.

| # | Slug | Trope | Hero product |
|---|---|---|---|
| 1 | `ditl-wrx-vb` | average WRX owner (VB) | Epsilon WRX VB kit (front bumper, rear bumper, side skirts) + "WRC Wing – Subaru WRX/STI (VB, 2022+)" |
| 2 | `ditl-time-attack-larper` | average time attack LARPer | "TC Wing - Honda Civic Type R/Sport FK7/FK8" on swan necks |
| 3 | `ditl-s2000` | average S2000 owner | "TC Wing - Honda S2000 AP1/AP2" |
| 4 | `ditl-gr86-brz` | average GR86 / BRZ owner | ZN8 Front Lip + Side Skirts + Rear Spats (opt. "GT Wing – Subaru BRZ / Toyota GR86 (ZN8, 2022+)") |
| 5 | `ditl-miata-na` | average Miata owner (NA) | "TC Wing - Mazda Miata NA" |
| 6 | `ditl-civic-fg2` | average "built not bought" Civic owner (FG2) | "TC Wing - Honda Civic Si Coupe FG2" (or GT Wing FG2) |

Stock note: the site shows "TC WINGS ARE ON BACKORDER". Ask the owner whether TC-wing videos go out now. The ZN8
front lip shows a [BACKORDER] variant. The WRX VB front lip is on [CLEARANCE]. Check the live store before
anything stock-related goes in the video.

### 1. average WRX owner (VB)
- **0-3 s, driveway at dawn.** Hands hit a vape and blow the cloud onto a WR Blue stock VB. He kneels with his ear
  to the engine and knocks twice. VO, whispering: "ringlands... still with us."
- **3-9 s, coffee drive-thru.** He holds his phone out the window playing a "boxer rumble" video at full volume,
  nodding along. Barista: "Sir, that's coming from your phone." Him: "New engine doesn't rumble. I bring my own."
- **9-24 s, meet parking lot.** He parks crooked across two spots, slaps his own fender cladding: "I hate the
  cladding." The camera snaps to the next car: a VB on the full Epsilon kit with the WRC wing. The hands go wild,
  stroking the lip and tapping the wing. Its owner's face warps in horror: "please stop touching my car." The hands
  keep patting. Hard cut: a phone screen with the kit in the cart, thumb pressing a huge green BUY button. Hard
  cut: check-engine light. End.

### 2. average time attack LARPer
- **0-3 s, bedroom.** He wakes up in a full race suit, helmet on, and the hands try to eat cereal through the visor.
- **3-9 s, commute.** A lap timer runs on the phone mount in a school zone. A speed bump scrapes the splitter
  (crunch). VO, satisfied: "aero's working."
- **9-25 s, office parking garage.** The wing clips the clearance bar. He backs up and nods: "downforce." Coworker:
  "do you actually race?" "Next season." "You said that last season." Silence. He turns to the wing and the hands
  gently stroke the TC Wing endplate (Epsilon logo in frame). Whispering: "she's real though." End: he sits parked,
  doing imaginary paddle shifts and mouth-revving "braaap", with the timer at `--:--`.

### 3. average S2000 owner
- **0-3 s, garage.** The cover comes halfway off. He looks outside: one cloud. The cover goes back on. "Not today."
- **3-9 s, gas station, a sunny day.** He wipes his fingerprints off the pump and hisses at a passer-by. Stranger:
  "nice Miata." A long distorted scream.
- **9-24 s, cars and coffee.** He guards the car with his arms out and explains "nine thousand RPM" to a kid, who
  walks away. An AP1 vs AP2 argument escalates. The other S2000 has the Epsilon TC wing; the hands poke it. Voice
  cracking: "...is that the Epsilon one?" A nod. He looks at his car, at the wing, at his car. Hard cut: home, car
  under the cover, one raindrop. End.

### 4. average GR86 / BRZ owner
- **0-3 s, bedroom.** He bows to a poster of an old hatchback on the wall.
- **3-9 s, on-ramp.** Mid-rev, the POV sags. VO, pained: "the torque dip... I felt it in my soul."
- **9-25 s, parking lot.** An identical car parks next to him. "Mine's a Toyota." "Mine's a Subaru." A third and a
  fourth identical car pull in. The only one anyone can tell apart wears the Epsilon lip, skirts and spats; everyone
  slowly turns to look. He tries to drift out at 5 mph, yanks the e-brake, and the car just stops. Whispering:
  "Tokyo." End.

### 5. average Miata owner (NA)
- **0-3 s, driveway.** A 6'4" guy folds himself in, knees past the wheel. VO: "fits perfect."
- **3-9 s, highway, top down.** Rain. He doesn't put the top up, soaked and staring ahead. A minivan passes him.
  "Momentum car."
- **9-24 s, Miata meet.** He waves at every Miata and they all wave back (frantic hand-wave cuts). He blinks the
  pop-up headlights to say hello. Someone asks "why not a faster car?" and every Miata blinks its headlights at
  them at once. Final shot: his NA with the Epsilon TC wing, so light the wing looks like it's holding it down. He
  pats it: "mostly wing now." End.

### 6. average "built not bought" Civic owner (FG2)
- **0-3 s, porch.** Five cheap marketplace boxes. The hands rip them open: zip ties, a mystery splitter, a sticker
  sheet.
- **3-9 s, curb.** The splitter is held on with zip ties. A pothole knocks it off and it skids down the road. VO:
  "built not bought."
- **9-25 s, parking lot / meet.** He haggles a "used but like new" part with a stranger, the hands holding out a
  crumpled bill. Then an Epsilon box is delivered. The hands slow down and open it reverently (angel choir). The
  TC wing comes out clean, he installs it, and it's the only straight panel on the car. A friend: "is that... real?"
  He shields the wing with both arms. End.
- Voice note (WRX, 2026-11-17): the preset voice "Cody" fails on Higgsfield `elevenlabs_v4` (refunded); it works only on Seed Audio, which has no emotion tags. Check a voice works on v4 before building a dialogue take around it.
