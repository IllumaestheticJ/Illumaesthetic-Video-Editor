---
name: game-menu-reel
description: Make a reel that plays a real video game's car-select sequence (intro cutscene, menu, scrolling through cars, picking one) with the game's own UI and sound effects, but with Epsilon kit cars rendered from the Epsilon-Site showroom GLBs in place of the game's cars. Use for any "pick your starter car", "car lot", "garage menu", "NFS / Gran Turismo / Forza style car select" reel, or any request to put Epsilon site GLB kit cars into game footage or a game menu.
---

# Game-menu reel

Read `CLAUDE.md` (mandatory list) and then `knowledge/game-menu-reel.md`, which is the procedure.
Worked project: `projects/nfs-carlot/`.

1. **Capture first.** Search Dropbox and Drive for the game capture. If it is not there, ask the
   user for it in your first reply (what it must contain is in the knowledge doc § Capture) and
   carry on with steps 2–3 meanwhile. YouTube and archive.org are not reachable from this
   environment.
2. **Cars.** For each requested car: `python -m ive kit <car-id> [--without …] [--prefer …]`,
   write `projects/<p>/cars.yaml`. A car without a showroom GLB is a question for the user, with
   a render of what exists.
3. **Line-up sheet.** `python -m ive kit-render -- …` one still per car, tile, look at it, send
   it to the user for kit and colour sign-off.
4. **Capture breakdown.** Constant-rate all-intra working copy, tile it, find the clean plate (menu up,
   no car yet), how the game swaps cars, and the longest pauses. `clips.md`.
5. **Track + camera.** `projects/nfs-carlot/tools/track.py` for the turntable slide; fit the menu camera
   to the game cars' outlines (for the NFSU2 car lot reuse `projects/nfs-carlot/cam_carlot.json` and
   `rig_showroom.json`); render each car once with `ive kit-render --camera … --ground shadow`.
6. **Swap + assemble.** `tools/composite.py` (real frames, only the car zone repainted; the purchase prompt at the end) then
   `tools/assemble.py` (9:16 on a blurred copy, the capture's own audio, cuts on scrolls). Copy both
   into the new project and change the constants at the top.
7. **Deliver + learn.** Look at the join frames, send it, `ive feedback` (`--rule` for anything
   general), `ive archive`, commit, push.

Never invent numbers for on-screen stats, and tell the user once that the game's footage, UI and
audio are the publisher's.
