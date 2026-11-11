# Game-menu reel: "pick your car" with Epsilon kit cars

A reel that plays a real game's car-select sequence (cutscene → menu → scrolling cars → select)
with the game's own UI and sound, but the cars on the showroom floor are Epsilon kit cars rendered
from the site's GLBs. First project: `projects/nfs-carlot/`.

**Status (2026-11-11): every step below was run for `projects/nfs-carlot` v1. The user's review of v1
is still to come; fold its lessons in here.**

## 1. Inputs to collect before anything else
- **The game capture.** The exact UI and SFX only exist in a real capture, so nothing past step 3
  can start without it. Check Dropbox and Drive first; if it is not there, ask the user for it in
  the *first* message, not after an hour of prep. Routes, best first:
  1. **The user records it** and drops the file in Dropbox (a phone screen recording of a YouTube
     playthrough at its top quality was good enough for v1). For NFS Underground 2 they can play
     `nfsu2.xyz` (a browser port of the PC game) and screen-record: about five minutes from
     "Start New Career" to the car lot on any computer with a real graphics card. The site ships
     without the licensed songs, so the menu sounds come out clean.
  2. **Play it here** with `tools/game_driver.js` (see "Running a browser game here" below). Menus
     and the garage run at 40+ fps; the open world runs at about 5 fps on software graphics, so
     anything that needs driving first is the hard part.
  3. **YouTube** (tried 2026-11-11, do not repeat): with `www.youtube.com` allowed, `yt-dlp
     --js-runtimes node` reads titles and formats, so it is fine for *finding* a video. The media
     comes from `rrN---sn-….googlevideo.com` and is redirected to a second such host; each needs
     its own approval. Even with the hosts allowed, the partial download failed (ffmpeg could not
     open the stream through the proxy) and direct ranged pulls were refused by the session's
     safety check. The plain downloader (no ffmpeg) then got `HTTP 403` from YouTube's own
     servers: that is YouTube's bot protection, not our network, and switching player clients to
     get past it is not allowed here. `archive.org` is not reachable either. Ask the user to
     download or record the clip on their own machine.
- **The car list**, in menu order, and for each car which kit parts are on or off.
- **Rights.** The capture's footage, UI, sound effects and any licensed menu music belong to the
  game's publisher / the labels. Tell the user once; it is their call for a brand account.

### Capture: what to ask for
One continuous recording, game audio only (no commentary, no overlay, no watermark):
1. the cutscene leading into the menu (for NFS Underground 2: the 350Z pulling into the car lot);
2. the car-select menu held still for ~3 s on each car, scrolled through the whole list in both
   directions, so every UI state and every menu sound is on tape at least twice;
3. the select / confirm action and whatever plays after it.
Ask for the **menu music turned to 0 in the game's audio options** (SFX left on): menu sounds
recorded over a music bed cannot be cleanly separated, and licensed music gets reels muted.
Highest resolution available; a widescreen PC capture beats an upscaled 4:3 one.

## Running a browser game here (`tools/game_driver.js`)
`nfsu2.xyz` needs only its own host allowed. It runs in the pre-installed headless Chromium on
WebGPU through SwiftShader (software):

```bash
node tools/game_driver.js --url https://nfsu2.xyz/ --size 1280x720 --port 8765 \
     --profile /home/user/media/work/<p>/game/profile --init tools/game_audio_tap.js &
curl -s 'localhost:8765/click?x=271&y=292'          # the site's Play button at 1280x720
curl -s 'localhost:8765/key?k=Enter'                # menus: arrows, Enter, Escape
curl -s 'localhost:8765/shot?path=/abs/s.jpg&q=70'  # look at it
curl -s 'localhost:8765/rec?start=/abs/out.webm&fps=60&mbps=40' ; curl -s 'localhost:8765/rec?stop=1'
```
What was learned on the first run:
- The page logs every game screen (`[fng] … screen UI_StartCareer.fng`); `/log` shows them, which
  tells you where you are without a screenshot.
- Boot → Enter ×3 skips the logos → "create profile" defaults to **No** (ArrowLeft, Enter for Yes)
  → main menu → ArrowLeft = Career → Start New Career → Enter skips the intro movie → ~40 s load.
- Pressing Play joins a public free-roam world: other players' cars and chat (including offensive
  names) appear on screen. `window.__nfsu2.session.net.offline()` (via `/eval`) removes them.
  Do this before recording anything.
- Speed: menus and the garage 40–75 fps at 1280x720. Open world 2 fps at 1280x720 with players
  nearby, 5.5 fps at 480x270 offline. Page screenshots take ~1 s at 480x270 and ~10 s at 1280x720
  while the world is running.
- At 5 fps a key tap shorter than a frame is never seen. Hold keys (`/down`, `/up`, or `ms=`), and
  release everything before a new sequence: a key left down gives throttle + brake = a burnout.
- The audio tap works: the page has one 44.1 kHz AudioContext and `--init tools/game_audio_tap.js`
  mirrors it into the recorder. The recorder itself (`/rec`) is written but **not yet tested**.
- The NFSU2 prologue cannot be skipped: the car lot is across the whole city from the airport
  (about 5 km), and the page exposes no position, speed or teleport (`session.status` has 60
  values, none of them the car's). `tools/gps_autopilot.py` follows the blue GPS arrow and frees
  itself when wedged (it reads "under 10 mph" from the speed readout; frame differencing fails
  because rain and the day/night cycle keep the picture changing). In about 25 minutes of runs it
  reached the highway junction outside the terminal several times and then circled the airport
  loop; the world map showed no progress toward the lot. Unsolved: choosing the right exit at that
  junction, and the GPS dropping to "Searching connection" off the road network. Stepping the car
  by hand gains only a few metres per step. Treat this as not working; use route 1.
- How to read the arrow (it took five tries): it is a flat block arrow above the car, a wide
  triangular head on a short stub. Width on screen gives how far to turn (widest = sideways).
  Sideways, the thicker half is the head. When it is compact, the thin end is the tip, and
  because it floats above eye level, **tip low = straight ahead, tip high = behind you**.

## 2. Cars: kit state from the site, never by hand
All showroom GLBs (`Epsilon-Site/showroom/models/eps-*.glb`) share one frame: metres, Z up, nose
at −Y, tyres on z = 0, one node per body zone and per kit part (`part_*`), materials named by role
(`paint`, `glass_tint`, `rim_dark`, …).

```bash
python -m ive kit acura-integra-de --without fender_flares     # -> fitted[], hide[], notes[]
python -m ive kit honda-civic-sedan-fe --prefer sport_wing_duckbill
python -m ive kit honda-civic-ep3 --glb /home/user/media/<p>/glbs_final/eps-honda-civic-ep3-v17.glb
```
`ive kit` applies the showroom's own rules: a fitted part hides the stock nodes it replaces
(repo manifest `replaces`, plus `body_<part>_stock` / `trim_<part>_stock` by name); parts in one
slot group (two wings, lip vs splitter) are alternatives, so only one is fitted (`--prefer`).
Put the result in `projects/<p>/cars.yaml`.

**Use the newest exports.** The repo's `showroom/models` lags the real ones. Drive has
`Epsilon-final-GLBs-2026-10-15.zip` (file id `12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7`, 203 MB, 31 cars,
fetch with `ive fetch-drive`): e.g. Integra v29 against the repo's v8, NC v19 against v2, and cars
the repo does not have at all (EP3 v17, 350Z v24). They are 10–20× heavier (millions of
triangles, photo textures on lamps) and render fine in Cycles. Pass them with `--glb`.

A car is only usable if it has a kit GLB. `wing-configurator/data/models/*.glb` are
30k-triangle untextured body scans with no kit parts; they look wrong next to kit cars. If a
requested car has neither, show the user a render of what exists and ask.

## 3. Line-up check (do this while waiting for anything else)
```bash
python -m ive kit-render -- --glb <glb> --hide <hide,list> --paint "#848586" --finish metallic \
    --az 38 --el 7 --res 1280x720 --samples 32 --bg 0.01,0.011,0.016 --ground gloss --out lineup/<car>.png
```
~20 s per 720p still for the repo GLBs on CPU, longer for the final exports. Tile the stills with
labels and send the sheet to the user so the kit state and colours are approved before any
matched rendering. `--part-paint raw` shows kit parts in satin black if the kit needs to read
against the body colour.
- Light energies in `kit_render.py` rigs are tuned for the Standard view transform; the first
  attempt (thousands of watts) blew out to white. Start from the `carlot` rig and adjust with
  `--exposure` or a `--rig-json` copy.
- Do not render while the game is running in Chromium: both want all four cores.

## 4. Break down the capture
The first project's capture was two phone screen recordings of YouTube playthroughs (portrait
1206x2622 with a 90° rotation flag, variable frame rate ~59 fps; the game picture is a 2144x1206
strip in the middle). Make one constant-rate working copy and index everything by its frame number:

```bash
ffmpeg -i capture.mp4 -vf "fps=60,crop=2144:1206:239:0" -c:v libx264 -crf 12 -g 1 -an a60.mp4   # all-intra: exact seeks
ffmpeg -i capture.mp4 -vn -ac 2 -ar 48000 a.wav
```
Then tile it: every 1 s for the story, every 0.25 s through the menu, every frame through one
scroll. That is how the three things that make the rest possible were found:
- **the clean plate**: the frame where the menu is drawn but the first car has not slid in yet
  (empty turntable, same grade as every later hold);
- **how the game changes cars**: the menu and the room stay put; the turntable with the car on
  it slides out to the left and the next slides in from the right, 14 frames, as if both sat on one
  conveyor about 2980 px apart (the menu's first appearance does the same at half speed);
- **the rhythm**: players flick back and forth about once a second, so most holds are too short.
Write the timecodes in `clips.md`.

**Check the capture's speed before anything else.** The first project's 1440p capture was a YouTube
playthrough whose garage section the uploader had sped up 2x (v1 went out with it; the user caught it).
Measure one scroll in every capture you have (`tools/track.py` on the picture): the real game takes
0.47 s. If a section is sped up, write it out at the fraction that makes it real time (2x at 60 fps
becomes every frame at 30 fps) and take the sound from a real-time capture.

## 5. Track the slide (`projects/nfs-carlot/tools/track.py`)
Template-match the turntable's right and left rim tips (taken from the clean plate) along x in every
frame. Both at ~0 with score > 0.9 = at rest. The outgoing turntable is followed by its right tip,
the incoming one by its left tip; the few frames in the middle where neither is reliable are a
straight line. Holds sit a few pixels apart from each other (−3.5 … +3.5 px here): measure the rest
offset per hold and apply it, or the repainted turntable tiles will not line up with the real ones.

## 6. Match the menu camera and light
- Outline boxes of the game's cars (difference against the clean plate) plus the turntable's rim
  ellipse, least-squares against boxes of the cars' published length/width/height
  (`editlog.jsonl` has the numbers). Focal length is **not observable** from that (same error from
  1300 to 3400 px); pin it where the fitted heading agrees with how much of the car's front vs side
  you can see. Confirm with an onion overlay of a kit car on a game car of similar size.
- Result for the NFSU2 car lot: `projects/nfs-carlot/cam_carlot.json` (reuse it for any capture of
  that menu at 2144x1206), light rig `projects/nfs-carlot/rig_showroom.json`.
- `python -m ive lookat` needs `--loc=-4.3,-6.1,1.2` (with `=`) when a coordinate is negative.
- Render each car once, full frame, transparent, `--ground shadow`. The cars are static in this
  menu; the slide is 2D.

What went wrong in v1 and how v2 fixed it (user: "the car needs to be angled to match the game",
"match the lighting"):
- **Fit on wheels, not outlines.** Outline boxes gave a heading 7° too frontal and a camera too
  high. The near-side wheel centres of five game cars (read off gridded crops), with their
  wheelbases and tracks, pin heading and height; `tools/camfit.py` writes the camera.
- **Choose the focal length by overlaying a kit car on a game car of the same size** at three
  focal lengths (NC Miata on the game's NB Miata): only one matches how the far end of the car
  shrinks. The NFSU2 car lot on a widescreen-patched PC build is very wide: 1300 px on 2144.
- **One camera per car**: the game parks every car by its wheelbase midpoint (0.28 m behind the
  turntable centre here), so shift the camera by each GLB's own wheelbase midpoint.
- **Light it like the game, not like a studio.** Compare luminance percentiles inside the car
  silhouette with a game car of the same colour. The game's cars are dark (median 50/255) with a
  soft highlight on top and windows that reflect white. `rig_showroom.json` gets there with a dim
  ceiling key, near-black ambient and two reflection-only panels (`glossy_only`), one of them
  linked to the glass node only (`only_nodes`) so it does not wash out the paint.

- **Steer the front wheels.** The game parks every car with its front wheels turned toward the
  camera (`kit-render --steer 25` for the NFSU2 car lot; compare two angles against a game car).
- **Badges come from real artwork.** For a make the game lacks, render the emblem front-on from
  the car's own GLB (`tools/badge_from_glb.py`) and clean it to a mask. A hand-drawn badge was
  rejected. Wikimedia's API answers 429 from this environment.
- **Music the user asks for needs a file.** Captures only have the game's songs buried under
  engine and menu sounds. Ask for the track in Dropbox in the same message as the capture.

## 7. Swap the cars (`projects/nfs-carlot/tools/composite.py`)
Start from the **real capture frame** and change as little as possible:
1. repaint a soft zone where any game car and its shadow can be (union of the differences, grown)
   with the clean plate: turntable pixels take the plate shifted by the slide, room pixels take it
   unshifted;
2. lay the kit car render on top, shifted by the same amount, cut off at the top of the stat band
   so the menu stays above it;
3. paste the name plate; 4. put the mouse cursor back wherever it crossed something repainted
   (difference against the median of that hold).
Mistakes made on the way: the car's shadow was darkening the stat labels (clip it at the band);
shifting the plate under the semi-transparent stat band doubled a label (at rest use the plate
unshifted there, mid-slide leave the band alone).

## 8. Name plates and stat bars
The plates are per-car artwork, not a font. Lift real plates from holds of the capture whenever the
game has a car of the same name (Toyota Corolla, Honda Civic, Mazda Miata were pixel-true). For a
make the game does not have, the bare plate is a high percentile across many plates (a median left
ghost lettering), the logo box is another plate's box with its badge inpainted out, and the wordmark
is drawn in the capture's own greys. Leave the stat bars as the game drew them: they are not data
about our cars, and redrawing them would mean inventing numbers.

Drawn wordmarks (user asked twice for fixes on the Integra plate): look at how the game sets its
plates before choosing type - maker name small in a condensed grotesque, model name as that car's
own badge lettering - and render two or three options *under the game's real plates* to pick.
Fonts: `tools/fetch_fonts.sh` (npm `@fontsource/*`, converted with fontTools; Google Fonts hosts are
not reachable here).

## 9. Timeline and sound
Cut the picture to the sound, not the other way round. Take one continuous real-time stretch of menu
audio, find where each car starts to move in *that capture's picture* (those are its scroll times),
and make each picture range (starting on the first frame of a scroll in the picture capture) exactly
as long as the gap to the next scroll in the audio. The scroll sound then sits on every car change
with the music unbroken. If the last car needs a longer hold, jump the audio to a later scroll there:
the jump hides under the scroll sound. Verify in the output: sound level and picture motion around
every change (`review.md` v2). v1 instead cut the sped-up capture's own audio on its scrolls, which
synced but was double speed. Both captures here had the game's licensed menu song under everything.

**Buying the car (user request on v4).** End the menu on the purchase, not on a scroll: Continue,
the game's "Do you want this stock <car>?" prompt, Yes, then the end card. Use one unbroken audio
take from the last scrolls through the Yes click so the purchase sounds are the game's own, and cut
the picture to it (scroll times, when the prompt starts to fade in, when Yes is clicked). If that
take has more scrolls before the purchase than you have cars left, wrap the list back to car 1 and
buy that one — it is what a real list does. The prompt is a translucent panel over a dimmed room, so
do not repaint the car zone under it. Keep the capture's prompt frames and add
`T * (our last menu frame - the capture's last menu frame)` inside the car zone, where T is how much
of the scene shows through each part of the prompt. Measure T by fitting `prompt = T * scene + c`
per region against a frame of the bare scene (NFSU2 shows one for a frame or two right after Yes:
room 0.361, dark band 0.125, panel 0.067, button 0.055, button under the cursor 0.031). Pick the
highlighted button per frame. Fitting T per pixel with a sliding window does not work: it comes out
blotchy and the car glows in patches. Inpaint the game's car name out of the question and reset the
whole line in the matching face (NFSU2: Roboto Condensed Italic, 49 px on a 2144-wide frame); for
the fade-in, mix our last menu frame with our first steady prompt frame by the capture's own fade
amount. Use the model name the name plate shows.

**The mouse cursor (user on v6: "the cursor arrow freaks out").** A menu cut from several ranges of
a capture has the player's cursor in a different place in each, so it teleports at every cut. Deal
with it before the first delivery: track it (`projects/nfs-carlot/tools/cursor.py`), take it out of
the menu frames, and draw one cursor on a continuous path that makes sense for what happens (to the
"next" arrow, stays there for the scrolls, to Continue). Check the clean plate for a baked-in
cursor too: it shows up as a second arrow that blinks around slides. Removal: paste static UI (name
plate, arrow buttons) from frames where the cursor is elsewhere; over anything that changes with
the car, blend clean pixels in by gradient (`cv2.seamlessClone`) with a hole wider than the cursor.
Sprite: measure the white arrow over a flat dark background and rebuild the outline as the shape
grown 3 px; do not try to solve alpha from the capture. Where the capture's cursor path is already
continuous (here: from Continue through the purchase prompt) keep it, and choose frames so that it
stays continuous: drop frames where it sits still, never frames where it moves.

**Ending.** For Epsilon reels end on the EPSILON+ wordmark (white on black,
`Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png`, 800 px wide): cut to it on a menu
sound (with a purchase: on the Yes click), let the music run about 3 s under it and fade over the
last 1.8 s (user request on v3).

## 10. Layout, assemble, review (`projects/nfs-carlot/tools/assemble.py`)
The game draws its menu in a centred 4:3 box on a 16:9 picture. Crop to that box (x 300–1842),
scale to the reel's full width (1080x846) and set it on a blurred, darkened copy of the frame; a
full-height crop would cut the name plate and bars. The crop also loses uploader watermarks at the
edges. Open on something recognisable within a second (here the "Would you like to enter the
Shop?" prompt), not on the drive. Look at frames around the cut into the menu and through the
first scroll, then `ive feedback`, `ive archive`.
House rules that do **not** apply to this format: the 1:1 real-to-scan cut, the silver scan look,
the logo end card unless the user asks. Rules that still apply: no invented numbers on screen,
look at your own output.
