# Game-menu reel: "pick your car" with Epsilon kit cars

A reel that plays a real game's car-select sequence (cutscene → menu → scrolling cars → select)
with the game's own UI and sound, but the cars on the showroom floor are Epsilon kit cars rendered
from the site's GLBs. First project: `projects/nfs-carlot/`.

**Status (2026-11-11): steps 1–3 are built and proven. Steps 4–9 are the plan; they have not been
run yet because the first project is waiting on its game capture. Rewrite them from what actually
worked once the first reel is delivered, and delete this line.**

## 1. Inputs to collect before anything else
- **The game capture.** The exact UI and SFX only exist in a real capture, so nothing past step 3
  can start without it. Check Dropbox and Drive first; if it is not there, ask the user for it in
  the *first* message, not after an hour of prep.
  - `www.youtube.com` and `archive.org` are refused by the environment's network policy, and
    YouTube media comes from random `*.googlevideo.com` hosts an exact-host allowlist cannot
    cover. Do not plan on downloading the capture yourself; ask for a file in Dropbox.
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

## 2. Cars: kit state from the site, never by hand
All showroom GLBs (`Epsilon-Site/showroom/models/eps-*.glb`) share one frame: metres, Z up, nose
at −Y, tyres on z = 0, one node per body zone and per kit part (`part_*`), materials named by role
(`paint`, `glass_tint`, `rim_dark`, …), no textures.

```bash
python -m ive kit acura-integra-de --without fender_flares     # -> fitted[], hide[], notes[]
python -m ive kit honda-civic-sedan-fe --prefer sport_wing_duckbill
```
`ive kit` reads the showroom manifests and applies the showroom's own rules: a fitted part hides
the stock nodes it `replaces`; parts in one slot group (two wings, lip vs splitter) are
alternatives, so only one is fitted (`--prefer` picks which). Put the result in
`projects/<p>/cars.yaml`.

A car is only usable if it has a **showroom** GLB. `wing-configurator/data/models/*.glb` are
30k-triangle untextured body scans with no kit parts (EP3: `kitPending: true`); they look wrong
next to kit cars. If a requested car has no showroom model, show the user a render of what exists
and ask, don't substitute silently.

## 3. Line-up check (do this while waiting for anything else)
```bash
python -m ive kit-render -- --glb <glb> --hide <hide,list> --paint "#848586" --finish metallic \
    --az 38 --el 7 --res 1280x720 --samples 32 --bg 0.01,0.011,0.016 --ground gloss --out lineup/<car>.png
```
~20 s per 720p still on CPU. Tile the stills with labels and send the sheet to the user so the
kit state and colours are approved before any matched rendering. `--part-paint raw` shows kit
parts in satin black if the kit needs to read against the body colour.
- Light energies in `kit_render.py` rigs are tuned for the Standard view transform; the first
  attempt (thousands of watts) blew out to white. Start from the `carlot` rig and adjust with
  `--exposure` or a `--rig-json` copy.

## 4. Break down the capture (plan)
`ive probe`, `ive sheet`, then write `clips.md` with the timecodes of: cutscene, menu settle,
each car's idle hold, each scroll transition, the confirm. Note the capture's aspect ratio and
decide the 9:16 layout with the user's first draft (full-height crop on the car vs letterboxed
menu with the UI intact; the UI must stay readable, so expect a crop that keeps the name plate).

## 5. Separate UI, car and background (plan)
While the menu scrolls, the UI and the lot stay still and only the car, its name and its stat
bars change. A per-pixel temporal variance over the idle holds of all cars gives the mask of
what changes; everything else is a locked plate. Inside the car region the lot floor is never
fully visible: cover it with the new car plus a rebuilt floor patch, and check the join.

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
Cut each menu sound (scroll, confirm, back) from the capture at its onset and re-trigger it on
every scroll in the edit. Keep the cutscene's own audio under the cutscene.

## 9. Assemble, review, archive
`ive assemble`, frames ±2 around every scroll and cut, rubric, `ive feedback`, `ive archive`.
House rules that do **not** apply to this format: the 1:1 real-to-scan cut and the silver scan
look. Rules that still apply: no invented numbers in on-screen text, look at your own output.
