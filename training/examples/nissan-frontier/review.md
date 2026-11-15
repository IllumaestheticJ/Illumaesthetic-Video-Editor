# Nissan Frontier Pro-4X -> RONIN v11 - self-review (training/rubric.md). Earlier: review_v10.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v11.mp4 - 1080x1920, 30 fps, 52.87 s, 1586 frames.
v11 (user on v10): badge centred 14 mm higher and back near its scanned size (1:1 grid comparison: overlaps the real badge);
flares-removed state scan highlighted + labelled from when the stock flares leave until the wide fenders cover it; the 360 lands on
the solved camera on the cut frame (no hold) and the real reveal clip is 1.8 s at 0.82x; end card MotoIQ lockup rebuilt to the Sentra
description (white moto, red iq box) - the Sentra PNG itself was an upload in that session and is not reachable here.
Measured on the delivered file: bass drop = cut 434 (+0 ms). m4/m5 kept from v10 (badge 14 mm lower there, ~2 px in those wide shots).

--- v10 review follows ---
# Nissan Frontier Pro-4X -> RONIN v10 - self-review (training/rubric.md). Earlier: review_v9.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v10.mp4 - 1080x1920, 30 fps, 53.47 s, 1604 frames.
v10 (user on v9): full-car-scan bumper once the trimmed bumper lands (tools/fullbumper.py); badge centred on the CAD ring and scaled
1.26 to fill it like the real one; grille lights 2 mm under the measured brow windows (tools/lights_v2.py); MotoIQ wordmark under the
Illumaesthetic logo; music M.O.O.N. 'Paris' from 115.337 s, drop on the first mod (frame 434), every cut on 434 + 18k (100 BPM).
Looked at: front check renders (v10_chk.png), zoomed 1:1 comparison of lights and badge against IMG_3223, m1 frames around the
bumper swap, 20-frame sheet of the delivered file, onion match/check_3223_v10.jpg, luma of all six shots (clean).
Measured on the delivered file: bass drop at 14.467 s = cut 434 (0 ms). Other cuts are on the drop's beat grid by arithmetic only.
Open: badge scaled 1.26 from the stock-badge scan (the Ronin's lit badge was not scanned); MotoIQ logo is white, made from the 3D logo STL.

--- v9 review follows ---
# Nissan Frontier Pro-4X -> RONIN "how we modified this truck" v9 - self-review (training/rubric.md). Earlier: review_v8.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v9.mp4 - 1080x1920, 30 fps, 53.6 s, 1608 frames. Same cut as v8.
v9 (user on v8): every scanned triangle inside or in front of the Ronin grille removed (170,771 body + 25,785 hood, tools/grille_clip.py;
before/after stills chk/gc_check.png); the SCANNED NISSAN badge goes onto the new grille after the lights; labels carry no MOD/STEP numbers.
Looked at: before/after clip stills (front 3/4 + top), full-res grille close-up f_0176, 20-frame sheet of the assembled file, onion
match/check_3223_v9.jpg, luma of all six re-rendered shots (clean). Scores as v8 except Scan quality: the grille close-up is now clean.
Left as is: thin dark seam where the hood lip was trimmed; the stock plate recess below the lower grille (stock bumper, not clipping);
badge is scan-silver in the build shots and black in the livery shots (the real one is black with a red outline).

--- v8 review follows ---
# Nissan Frontier Pro-4X -> RONIN "how we modified this truck" v8 - self-review (training/rubric.md). Earlier: review_v7.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v8.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 53.6 s, 1608 frames.
v8 (user on v7): no longer a "what we scanned" reel. Built on the Sentra short-form playbook (knowledge/short-form.md, other branch):
real article hook -> "HERE'S HOW." -> build in order with the SCANNED grille lights and fender lights -> livery + 360 of the
finished render -> 1:1 cut to the real truck on the crash -> real clips -> photo + logo (no slogan).

Looked at: 19 + 15 frame sheets of the assembled file, frames 1268-1271 around the reveal, onion match/check_3223_v8.jpg,
CAD sections with the seated grille lights, close-ups of the grille and fender lights, per-frame luma of all six new shots.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real Motor Illustrated headline full frame (4.9 s) then a 2.4 s answer card; 7.2 s before the first 3D frame is long |
| 2 | Beat sync | 4 | every cut frame is a measured beat onset (146 217 290 361 434 614 689 868 977 1051 1270 1341 1414 1488); NOT re-measured on the delivered file |
| 3 | 1:1 match | 4 | 360 holds the solved camera 0.4 s before the cut; onion still overlaps cab, grille, grille lights, mirror, wheels; real truck has roof rack/lights/bumper the scan lacks |
| 4 | Scan quality | 4 | grille + fenders = team CAD, grille and fender lights = real scans seated in the CAD pockets/slots; wheels still a stand-in; turbo = label only; livery breaks up on the lower bumper |
| 5 | Story | 5 | question -> answer -> steps in build order -> finished render -> the real truck |
| 6 | Grade | 4 | livery teal brighter than the real wrap; black CAD grille reads mid-grey in the close-up |
| 7 | Text | 4 | step/mod labels on scan shots only; none over real footage; RONIN GRILLE label is faint for its first frames |
| 8 | Ending | 5 | reveal on the crash, three real clips ~2.4 s each, photo + logo |
| 9 | Technical | 4 | new shots true 30 fps; the three reused opening shots are still 15 fps interpolated; reveal clip is 0.62x motion-interpolated |

Not done / assumptions: grille light seating angle is fitted to the pocket section by eye (54 deg), not from a mounted scan;
'Sidemarker 1' is used on both right fenders and 'Sidemarker 2' on both left; no headlines over the real truck; no credits card.
