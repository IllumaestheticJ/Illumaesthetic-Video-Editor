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
