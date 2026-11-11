# Game-menu reel: "pick your car" with Epsilon kit cars

A reel that plays a real game's car-select sequence (cutscene → menu → scrolling cars → select)
with the game's own UI and sound, but the cars on the showroom floor are Epsilon kit cars rendered
from the site's GLBs. First project: `projects/nfs-carlot/`.

**Status (2026-11-11): steps 1–3 and the browser game driver are built and proven. Steps 4–9 are
the plan; they have not been run yet because the first project still has no capture of the car
lot. Rewrite them from what actually worked once the first reel is delivered, and delete this line.**

## 1. Inputs to collect before anything else
- **The game capture.** The exact UI and SFX only exist in a real capture, so nothing past step 3
  can start without it. Check Dropbox and Drive first; if it is not there, ask the user for it in
  the *first* message, not after an hour of prep. Routes, best first:
  1. **The user records it** and drops the file in Dropbox. For NFS Underground 2 they can play
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
     safety check. `archive.org` is not reachable either.
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

## 4. Break down the capture (plan)
`ive probe`, `ive sheet`, then write `clips.md` with the timecodes of: cutscene, menu settle,
each car's idle hold, each scroll transition, the confirm. Note the capture's aspect ratio and
decide the 9:16 layout with the user's first draft (full-height crop on the car vs letterboxed
menu with the UI intact; the UI must stay readable, so expect a crop that keeps the name plate).
The game's menus draw their UI in a centred 4:3 box over a widescreen 3D scene.

## 5. Separate UI, car and background (plan)
While the menu scrolls, the UI and the lot stay still and only the car, its name and its stat
bars change. A per-pixel temporal variance over the idle holds of all cars gives the mask of
what changes; everything else is a locked plate. Inside the car region the lot floor is never
fully visible: cover it with the new car plus a rebuilt floor patch, and check the join.
(In the browser port the main-menu garage shows an empty turntable when no car is selected: a
free clean plate for that scene. Look for the same in the car lot.)

## 6. Match the menu camera and light (plan)
Solve the menu camera once from the game car (wheel hubs, bumper corners, roof corners against
the real car's published dimensions; `ive solve`), then reuse it for every Epsilon car via
`kit-render --camera`. Copy the lot's light directions into a `--rig-json`. If the game idles
with a slow camera move or car spin, measure it and reproduce it (`--spin` / `--orbit`).
Verify with an onion overlay on the game car, never from the solve score alone.

## 7. Replace what the UI says (plan)
Car name, maker badge and stat bars are redrawn in the game's own type and colours, sampled from
the capture. Stat bars are numbers on screen: don't invent performance figures. Either keep the
bars as a visual gag the user signs off on, or drive them from something real.

## 8. Sound (plan)
Keep the capture's own timeline where possible: the scroll and confirm sounds are already in
sync with the UI animation, so swapping the car under an untouched menu needs no sound editing.
Only re-trigger cut-out sounds if the edit reorders or repeats scrolls.

## 9. Assemble, review, archive
`ive assemble`, frames ±2 around every scroll and cut, rubric, `ive feedback`, `ive archive`.
House rules that do **not** apply to this format: the 1:1 real-to-scan cut and the silver scan
look. Rules that still apply: no invented numbers in on-screen text, look at your own output.
