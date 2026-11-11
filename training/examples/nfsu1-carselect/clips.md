# NFS Underground 1 car-select reel - source media

Media is never committed. Sources: `/home/user/media/nfsu1-carselect/`. Work dir: `/home/user/media/work/nfsu1-carselect/`.

## Game capture (Dropbox `/5. Claude Training/Good Reels (Epsilon)/`)
| File | What | Used |
|---|---|---|
| `Video Nov 11 2026, 12 25 40 AM.mp4` (94 MB, 53.6 s; `(1)` is a duplicate upload) | phone screen recording of the YouTube video "NFS Underground - All Cars (+Bonus Cars) 1080p60"; 1206x2622 rotated, ~56 fps VFR; game picture 2144x1206 at x 239 | picture and sound |
| `Video Nov 10 2026, 11 38 44 PM.mp4` (59 MB) | NFS Hot Pursuit Remastered car select: a different game, not for this reel | no |

Working copies: `a60.mp4` (60 fps, cropped 2144x1206, all-intra), `a.wav`. Frame numbers below are `a60.mp4` frames.

## How this menu works (it is NOT the Underground 2 turntable)
- The car sits still **on screen** during a hold while the garage streams past behind it (the car is "driving", wheels turning).
- "Next" starts a fixed 3.7 s animation: the menu (logo strip, name plate) switches to the next car at once, the old car
  drives away for 133 frames with the camera swinging after it, hard cut, the new car drives in towards the camera for
  about 90 frames (headlights, close sweep along its side) and settles into the hold pose.
- The animation's timing is identical every time; the garage behind it is not (different stretch of the garage each time).
- The menu is drawn over the scene, partly see-through: the car passes *under* the top band, the name plate and the stat panel.

| Frames | Seconds | What |
|---|---|---|
| 0-640 | 0-10.7 | YouTube player chrome / black |
| 656-832 | 10.9-13.9 | VW Golf hold (YouTube title overlay still fading: not usable for statistics) |
| 833, 1181, 1520, 1840, 2139, 2488, 2850 | 13.88, 19.68, 25.33, 30.67, 35.65, 41.47, 47.5 | car starts to pull away (the menu flips to the next car about 8 frames earlier) |
| 966, 1314, 1653, 1973, 2272, 2621 | +2.22 s | hard cut to the incoming car |
| 1653-1743 | 27.55-29.05 | **Miata drives in** (tracked) |
| 1743-1838 | 29.05-30.63 | **Miata hold** (car-relative camera static) |
| 1838-1972 | 30.63-32.87 | **Miata drives away** (tracked) |
| 2668-2860 | 44.5-47.7 | YouTube pause overlay, then the phone's control centre |

Cars in the capture, in order: VW Golf GTI, Honda Civic, Peugeot 206, Mazda Miata (NB, blue), Dodge Neon, Mitsubishi Eclipse,
Toyota Celica, Mazda RX-7 (cut off).

## Cars
See `cars.yaml`. Models: Drive `Epsilon-final-GLBs-2026-10-15.zip` (id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) and, for the FR-S,
Ron's `GT2 Animation FRS-green.blend` (Drive id 1q8-BnHUn-hvb6Tzi1Cy_OsfSdG_QCBVv, found through Epsilon-Site `showroom/models/FRS.md`).
Line-up sheet sent to the user: `lineup_sheet.jpg`.
