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
4. **Capture breakdown → plate/UI separation → camera + light match → UI text → SFX → assemble.**
   Follow the knowledge doc; update it with what actually worked.
5. **Deliver + learn.** Rubric, `ive feedback` (`--rule` for anything general), `ive archive`,
   commit, push.

Never invent numbers for on-screen stats, and tell the user once that the game's footage, UI and
audio are the publisher's.
