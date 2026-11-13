# Infiniti QX80 R-Spec reel v4 - "how it was made" - self-review (training/rubric.md)

Output: `/home/user/media/infiniti-qx80/out/infiniti_qx80_v4.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.83 s, 1165 frames.
Built by `tools/build_v4.py` (exact-frame segments + concat, Sentra pattern); scene list `direction.md` "## v4" (scene-director).
Earlier versions (scan-only Temerario style): review_v1.md, review_v2.md, review_v3.md.

Sources used: WhatsApp export (Dropbox, 540 photos + chat), Ecky's Drive folder `100 - Nismo QX80` (16 kit STL groups placed on
our scan with his own scan matrix; Render/ + Presentation Render/ originals in the concepts), press screenshots (Carscoops x2,
Motor Illustrated - the only outlets this environment could reach), our QX80 full-car scan.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Finished car (studio photo 1701) from frame 1, three real headlines stack on the beats at 1.4/2.7/4.0 s. Only 3 outlets (network allow-list). |
| 2 | Beat sync | 4 | All 14 section cuts on their planned frames (frame diff = plan). Decoded-audio check (cutcheck.py): section cuts -5..+44 ms of the nearest onset except 15.70 s (+107) and 28.70 s (+96), both in sustained string passages with no hit (flat RMS). Kit parts land on beats; the wrap sweep starts on the lift. |
| 3 | 1:1 match | n/a | No IRL->scan match cut in this cut (optional: photo 46 -> scan solve, not done). |
| 4 | Scan quality | 4 | Clean full-car scan; kit seated with Ecky's matrix (1.6 mm scan agreement). Wrap is an approximation of a colour-shift film (checked against 1702, copper/blue flips added); wheels/glass/grille masked by position. Stock wheels shown (the real car runs aftermarket wheels). |
| 5 | Story | 5 | Stock -> scan -> concepts -> kit on the scan -> wrap -> engineering -> print -> test fit -> finished, all from real project data. |
| 6 | Grade | 4 | Photos untouched (phone shots of varying light) on darkened blurred fills; renders AgX. |
| 7 | Text | 4 | Short section labels in the band above photos / clear black above renders; no triangle counts, no hp claims of our own, no staff names. |
| 8 | Ending | 4 | Finished car on the strongest accent (31.96 music), logo 720 px + "Customize everything" over the fade. |
| 9 | Technical | 5 | Spec met; luma scan clean on D/E; edge-touch test on scan segments (E re-rendered wider after it failed). |

Open items for the user: allow motor1/thedrive/gearjunkie/drifted/infinitinews in the environment for more headlines; OK to credit
Ecky by name?; the 3D wrap is an approximation; music is the generated QX80 track (another user rejected a generated track on MR2).
