# NFS-style car lot reel - source media

Media is never committed. Sources: `/home/user/media/nfs-carlot/`. Work dir: `/home/user/media/work/nfs-carlot/`.

## Game capture - NOT YET CAPTURED (blocker, 2026-11-11)
User: use of the game's assets is fine; get the capture from `nfsu2.xyz`.
`nfsu2.xyz` is a browser port of the PC game (no licensed songs on the site, so menu sounds are clean). It runs
here in headless Chromium through `tools/game_driver.js`: menus and garage at 40+ fps, open world at ~5 fps.

Reached so far (profile EPSILON, new career): boot, main menu, intro movie, the airport start in Rachel's 350Z.
Not reached: the car lot. It is ~5 km away across the city and the prologue cannot be skipped. `tools/gps_autopilot.py`
got from the terminal to the first highway junction and then sat wedged on a barrier; stepping by hand gains a few
metres per step. Details and open problems: `knowledge/game-menu-reel.md` > "Running a browser game here".

Not recorded yet: the 350Z arriving at the lot, the car-select menu, its sounds. `/rec` in the driver is untested.

Earlier dead end: YouTube (`tt4LXox7vb4`, PC no-commentary longplay, 1080p60) - metadata readable, download blocked.

## Cars (Drive `Epsilon-final-GLBs-2026-10-15.zip`, file id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7)
See `cars.yaml`. Line-up check: `/home/user/media/work/nfs-carlot/lineup2/lineup_sheet.jpg` (sent to the user).
The first line-up (`lineup/`) used the older repo GLBs and had no EP3.

| Slot | Car | Model | Kit fitted |
|---|---|---|---|
| 1 | Toyota Corolla Hatchback E210 (Zenki) | `eps-toyota-corolla-hatch-e210-v18.glb` | lip, skirts, spats, WRC wing |
| 2 | Honda Civic Si sedan FE (11th gen) | `eps-honda-civic-sedan-fe-v10.glb` | lip, skirts, rear lip, sport wing on the Si duckbill |
| 3 | Acura Integra DE4 | `eps-acura-integra-de-v29.glb` | lip, skirts, spats, trunk lip, wing; flares hidden |
| 4 | Honda Civic Si EP3 | `eps-honda-civic-ep3-v17.glb` | lip, skirts, rear lip, rear wing |
| 5 | Mazda MX-5 NC | `eps-mazda-mx5-nc-v19.glb` | bumper, lip, canards, brake ducts, fender cuts, tyre spats, skirts, spats, GT wing |
