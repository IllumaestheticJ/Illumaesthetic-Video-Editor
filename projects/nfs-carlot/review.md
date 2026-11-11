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

## v6 (2026-11-11) - after the user's review of v5
User: "Can you also change the EP3 to the blue we use for the lookbook?"

Output: `/home/user/media/work/out/nfs-carlot_v6.mp4`, 21.1 s.
- EP3 re-rendered in Boost Blue Pearl (B637P, #1c4fa0, pearl): the lookbook's default paint on the 11th-gen
  Civics, taken as "the lookbook blue" because the EP3 itself has no lookbook entry. Everything else as v5.
- Open: the EP3 (blue) is now followed by the Corolla (blue #16408c) where the list wraps.

## v7 (2026-11-11) - after the user's review of v6
User: "The cursor arrow freaks out, can you fix that?"

Output: `/home/user/media/work/out/nfs-carlot_v7.mp4`, 21.1 s.
- Causes: cursor in a different place in each capture range (jump at every cut), a copy of it baked into the
  clean plate (second arrow, blinking around slides), and a skipped stretch in the prompt.
- Now one cursor: rests where the capture has it as the menu opens, goes to the "next" arrow once the Corolla
  has settled, stays there through all five scrolls, travels to Continue during the last slide, then the
  capture's own cursor goes up to the prompt, hovers at No and crosses to Yes.
- Checked: contact sheet of every 8th menu frame (one cursor everywhere), 2x crops of the start spot before,
  during and after the cursor leaves (no patch), arrow buttons, hand-over frames. Sync unchanged.
- Missed in v1-v6 self-review: I looked at cars, plates and cuts but never followed the cursor. Add it to
  the checks for this format (done in the knowledge doc).

## v8 (2026-11-11) - after the user's review of v7
User: "The Audio inside the car lot also gets cut off 'use it to set yourself up -'. There's more audio after that."

Output: `/home/user/media/work/out/nfs-carlot_v8.mp4`, 21.4 s.
- The car-lot voice message (B 35.1-44.6 s) now plays whole: one audio take from the menu opening through four
  scrolls to B 45.5 s, then one jump at the last scroll to B 53.30 for the purchase. Menu music comes in at the
  end of the message as in the game, about 0.7 s before the jump.
- Picture re-timed to it: NC holds 1.3 s, EP3 1.3 s after their slides. Sync within 0.007 s.
- Checked: output audio correlates with capture B continuously (1.00 at 6, 9, 12, 13.5 s; 0.99 at 14.8 s).
- Missed in v5-v7: cut the audio by scroll times only and never looked for speech in it.

## v9 (2026-11-11) - after the user's review of v8
User: "The music at the end oddly loops before continue to play right after the speech is over."

Output: `/home/user/media/work/out/nfs-carlot_v9.mp4`, 20.9 s.
- The two audio takes now join 7 bars of the menu song apart, crossfaded just after the song's first hit:
  the song starts once, right after the voice message, and carries on in time into the last scroll and the
  purchase. EP3 holds 1.27 s (38 frames) to make the bar count come out.
- Checked: join = 7.001 bars; hits after the onset on the half-bar grid; no level dip; sync within 0.007 s;
  voice message still whole (take 1 runs to B 44.93 s, message ends 44.6 s).
- Missed in v8: moved the jump without checking what the music does across it.
