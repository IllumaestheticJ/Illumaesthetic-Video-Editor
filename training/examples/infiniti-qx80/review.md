# Infiniti QX80 v6 - self-review (training/rubric.md)

Output: /home/user/media/infiniti-qx80/out/infiniti_qx80_v6.mp4 (not in git), built by tools/build_v6.py.
1080x1920, 30 fps, yuv420p, AAC, 1462 frames = 48.73 s. Earlier reviews: review_v1..v4.md.

Structure (Sentra v6 short-form, knowledge/short-form.md): Carscoops article hook -> "HERE'S HOW." answer card ->
scan day (3 WhatsApp stills) -> 3D scan -> concepts -> new body panels (designer CAD kit flying onto the scan) ->
final render 360 (Midnight Purple wrap sweeping rear->front, bronze CE28 wheels) easing into the solved photo camera ->
1:1 hard cut to the real car on the drop (video 30.000 s, frame 900) with three headlines landing one per beat ->
finished photos (credit "INFINITI QX80 R-SPEC / for Nissan / Nismo · SEMA 2025") -> logo wordmark only.
Music: deadmau5 "Ghosts 'n' Stuff (Original Instrumental Mix)", TikTok CML 6739936808198473729, 128 BPM, track 15.019 = video 0.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Article headline readable from frame 0, slight push; the answer card follows on beat 8 |
| 2 | Beat sync | 4 | Cuts vs decoded audio onsets (broadband half-rise): -23..+19 ms, one at 43.133 s +39 ms (just over half a frame); breakdown cuts on the grid |
| 3 | 1:1 match | 4 | Silhouette solve IoU 0.870 (cam1702_grid2.json); 50/50 blend of frames 899/900: wheels, grille, body line up; real car sits lower on its wheels |
| 4 | Scan quality | 4 | Stock wheels removed, designer wheels/grille/lights placed from the review blend; luma clean through the 360 (no steps > 2) |
| 5 | Story | 5 | Article question -> how: scan day, scan, concepts, panels, render, real car, finished photos |
| 6 | Grade | 3 | Photos used as delivered; shop stills warmer than the studio reveal photo |
| 7 | Text | 4 | Only headlines from real articles, section labels and credit; no numbers invented, no triangle counts, no text over photos (text sits above/below) |
| 8 | Ending | 4 | Wordmark only (user: no slogan); music fades over the last 2.2 s |
| 9 | Technical | 5 | ffprobe as above; no black/dup frames at cuts; edge touches only on panels flying in (intended) |

Known limits: no video of other people / no scan-day video exists, so scan day and the finish are stills; the article
sites beyond Carscoops/Motor Illustrated stayed blocked (environment edit rejected); the track is a commercial CML track
and may be claimed outside TikTok.
