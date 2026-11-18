# Pip & Gus Ep 6 (SeamForged): v1 self-review

Output: `/home/user/media/work/ep6/out/pip_gus_ep6_v1.mp4`. 1080×1920, 30 fps, 39.63 s (1189 frames), -14 LUFS, true peak -1.5 dBTP.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Opens on the whole bumper on the printer lid, with Pip's "It's bigger than the printer...". There is motion in the first second, but no transformation yet. |
| 2 | Beat sync | 4 | Part B cuts sit on the 18-frame grid of the 100 BPM bed. The cartoon cuts follow the dialogue, as in the pilot. |
| 3 | 1:1 match | n/a | No real-to-scan cut in this episode. The phone push-in cuts 1:1 into full-screen SeamForged at frame 577. |
| 4 | Scan quality | 4 | Bomex GR86 rear bumper STL, sliced live in the app. |
| 5 | Story | 4 | Problem (too big, slow to cut by hand), then the app: slice, number, plates. Then the card and the hand-off to Ep 7. |
| 6 | Grade | n/a | Real footage only appears on the laptop screen. |
| 7 | Text | 4 | Captions on the cartoon only. The card says "SEAMFORGED / COMING SOON". No numbers anywhere; nothing over app or real footage (overlay alpha on footage is 0.0). |
| 8 | Ending | 4 | Logo card under Pip's "It's cut! Which printer do we use?", on the final chord. |
| 9 | Technical | 5 | No magenta key pixels in the cartoon and no app gizmo in Part B (both checked frame by frame). |

## Fixed before delivery
- The laptop key screen showed magenta in S3–S5. Its corners are now exported for every shot, and the laptop clip is pinned throughout.
- The app's transform gizmo was visible in Part B. Inpainting left smears, so I re-recorded (run5) with the gizmo locked hidden.

## Known open items
- B4 (Pip: "Whoa. There's the number!") is a stand-in: exploded pieces held. It needs the owner's printed GR86 piece clip, saved to `/home/user/media/pip-gus-ep6-seamforge/printed_piece.mp4`; `ep6_build.py` picks it up automatically.
- The recording numbered 24 of 32 pieces. The owner said to treat that as a SeamForge glitch (task filed).
