---
name: game-modshop-reel
description: Make a reel set in a real video game's car customisation shop (GTA 6 mod shop, or any photoreal game garage / tuning menu with several camera views) where an Epsilon car from the site GLBs replaces the game's car and the client's parts are bought one by one through the game's own menus, with the game's UI, sounds, radio and voice lines. Use for "GTA style mod shop reel", "customisation menu", "buy the parts in game", "install the kit in the game garage", for feedback on such a reel (navigation skips steps, purchased pop-up, screen tear, prices, stats bar, radio, voice line, end card), or any request to put an Epsilon car and parts list into a game's upgrade menus. For a car-select / car-lot menu use game-menu-reel instead.
---

# Game mod-shop reel

Read `CLAUDE.md` (mandatory list), then `knowledge/game-modshop-reel.md` (the procedure, written from 19 review
rounds), then `projects/gta6-customs/review.md` and `editlog.jsonl`. Tools: `projects/gta6-customs/tools/`.

1. **Ask first** (knowledge doc §0): the story screen by screen, part names, exact reference pictures, voice
   lines, watermark, ending. Search Dropbox ("Claude Training") and Drive for captures while waiting.
2. **Capture breakdown** into `clips.md`: held views, lists and titles as the game has them, purchases, sound events.
3. **Cameras**: `vps.py` for focal and pitch, `camfit.py` / `mancam.py` for position, then move in until the car
   covers the game's car and the part is in frame. `whipcams.py` for every view change.
4. **Renders**: one Blender at a time, in the background; states are hide-lists (`cars.yaml`).
5. **Menus**: `ui4.py` builds every state; `toast.py` draws the pop-up. Game titles stay, client items use the
   client's wording, prices are the catalogue's for the variant shown.
6. **Timeline**: `compose4.py`. Every screen entered and left as the game does it. Partial re-render with
   `START` / `END` / `OUTNAME`.
7. **Sound**: `assemble4.py`. Check any reused clip for a hidden voice. Radio as one unbroken bed.
8. **Check at delivery size** (knowledge doc §10), send, `ive feedback`, `ive log`, `review.md`, commit, push.

Never: ping-pong capture frames, hold a sharp rectangle through a whip, cut inside music or speech, repeat a voice
line, put an orbit on black, rename the game's own screens without saying so, invent prices or stats.
