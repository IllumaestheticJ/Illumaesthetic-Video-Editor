# NFS car lot reel v1 - self-review (2026-11-11)

Output: `/home/user/media/work/out/nfs-carlot_v1.mp4`, 1080x1920, 30 fps, 16.8 s, H.264 + AAC.
The scan-video rubric only partly applies (no scan, no 1:1 cut, no logo card); scored where it does.

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | opens on the game's own "Would you like to enter the Shop?" prompt; the first Epsilon car arrives at 6.4 s |
| 2 | Cut timing | 4 | every menu cut is the first frame of a scroll, so the game's scroll sound lands on each car change; not beat-synced (no added music) |
| 3 | Car match | 4 | size, heading and wheel contact agree with the game's cars in an onion overlay; lighting is close, not identical (our cars are cleaner and glossier than the game's) |
| 5 | Story | 4 | prompt, 350Z pulls in, pick a car: reads without text |
| 7 | Text | 4 | no added text; three name plates are the game's own, the Integra plate is drawn and its badge is simplified |
| 9 | Technical | 4 | 1080x1920/30/yuv420p/AAC/faststart; join frames and first slide checked |

Known weak points to raise with the user:
- The game frame fills the middle 44 % of the screen; above and below is a blurred copy.
- Two cars share the "Honda Civic" plate (11th-gen Si and EP3).
- The stat bars are the game's, for the game's cars.
- The menu music is the game's licensed song and jumps slightly at each scroll.
- Ends on the last car; the game's confirm dialog names a 240SX and was left out.
- Holds are 3.0, 1.2, 1.4, 2.1, 1.8 s: the second and third cars go by fast.
- Windscreens catch a broad white reflection of the ceiling light.

## v2 (2026-11-11) - after the user's review of v1
User: "Works, but match the lighting and use the fixed audio when in the garage - it's sped up way too fast.
The car also needs to be angled to match the game."

Output: `/home/user/media/work/out/nfs-carlot_v2.mp4`, 1080x1920, 30 fps, 16.5 s.
- Angle: camera refit from wheel centres; the NC now overlays the game's Miata outline-for-outline.
- Lighting: rig matched to the game's Miata (numbers in the edit log); colours deeper, windows reflect white.
- Garage: real-time (half speed of the capture) with the second capture's audio; scroll sounds verified on
  all five car changes. Holds now 2.0, 1.9, 1.2, 1.3, 1.3 s after each 0.5 s slide.
Still open: 0.3 s of silence where the cutscene audio ends and the second capture's menu audio starts;
frame fills the middle 44 % of the screen; two "Honda Civic" plates; game's own stat bars; no confirm dialog.

## v3 (2026-11-11) - after the user's review of v2
User: "The Acura badge is also wrong. Please also add some of the NFSUG2 soundtrack in there. The wheels are turned."

Output: `/home/user/media/work/out/nfs-carlot_v3.mp4`, 16.5 s.
- Badge: real emblem lifted from the Integra GLB's grille (`tools/badge_from_glb.py`).
- Wheels: front wheels steered 25 deg, checked against the game's cars.
- Audio: cutscene tail bridges the silent start of capture B; garage bed +2 dB.
- NOT done: a proper NFSU2 soundtrack bed. No clean track is available in this environment; waiting on the user.

## v4 (2026-11-11) - after the user's review of v3
User: "This is great. Fix the Acura Integra type face, let the ending music play out a little longer, then end with the epsilon logo."

Output: `/home/user/media/work/out/nfs-carlot_v4.mp4`, 19.6 s.
- Plate lettering reset to match the game's plates (Roboto Condensed + stroked Michroma).
- Last car holds 1.5 s after its slide; cut to the EPSILON+ card on the next scroll sound; music runs 3 s under it and fades.
- Still open: no separate NFSU2 soundtrack bed (needs a file from the user).

## v5 (2026-11-11) - after the user's review of v4
User: "Are you able to add the section where you select and purchase the car, THEN it cuts to the epsilon logo?"

Output: `/home/user/media/work/out/nfs-carlot_v5.mp4`, 21.1 s.
- Order now: Corolla, Civic Si, Integra, NC, EP3, back to the Corolla (list wraps), Continue, "Do you want
  this stock Corolla?", Yes, EPSILON+ card. The wrap is there because the real-time capture has two more
  scrolls right before its purchase and that take is used unbroken (B 50.03 s to the end).
- Checked in the output: Continue highlights under the cursor, prompt fades in with the Corolla dim and blue
  behind the panel (first pass was blotchy and too bright: per-pixel transparency; fixed with per-region
  values), question lettering overlays the game's, No is the default, cursor travels to Yes, card cuts in
  on the click. Picture/sound offsets printed by `assemble.py`: all within 0.007 s.
- Changes from v4 the user did not ask for: the NC and EP3 swapped places (NC is now 4th), and the last
  holds are shorter (NC 1.5 s, EP3 0.8 s, Corolla 0.3 s before Continue) because they follow the capture.
- Still open: no separate NFSU2 soundtrack bed (needs a file from the user). The Corolla's stat bars are
  the game's 240SX bars on its second appearance (different from its first).
