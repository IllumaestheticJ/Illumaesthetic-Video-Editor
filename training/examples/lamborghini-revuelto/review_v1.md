# Lamborghini Revuelto scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/lamborghini_revuelto_v1.mp4` — 1080x1920, 30 fps, 34.57 s (1037 frames), h264 yuv420p + AAC.
Temerario-style, scan only, no IRL, no text. Music: original track generated for this reel (parent session).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Opens on a slow low side track fading up from black, matching the ref and the track's quiet 9 s intro; nothing *transforms* until 11.6 s. Moves from frame 0 but no 1.5 s "event" - the music has none to cut on. |
| 2 | Beat sync | 5 | Grid 102.52 BPM fitted to 20 onsets (resid <=3 ms). All 10 cuts measured by frame diff on the delivered file land on the planned frames (139..912 = round(t*30)). Parts stop moving at 27.93-27.97 s = the climax taiko attack (27.93); logo on the loudest hit (attack 30.40, frame 912). |
| 3 | 1:1 match | n/a | Scan-only format, no IRL->scan cut. |
| 4 | Scan quality | 4 | Silver on black, flat-shaded 3 mm car + 2 mm parts/close-up zone. Registration verified numerically (1.5-2.6 mm medians) and visually (chk/reg_overlay.jpg). Fixed after looking: lid pinholes + door crack (mirror scan carried door skin). Remaining: raw-scan marks at the windscreen base and black speckle in the dark intake grilles (not captured by the scanner - left as is); exploded base shows the real state-scan structure, some ragged edges. |
| 5 | Story | 4 | Ref order: side track -> front/rear 3/4 turntables -> headlight + wheel ECUs -> front opens (bumper, headlights, lid on its fitted hinge) -> top-down spin -> 12-panel explode -> float -> slam-home on the climax -> logo. Only the car's left-side panels were scanned, so the side panels come off one side. |
| 6 | Grade | 4 | AgX, -0.5 EV (Huracan sibling's luma match to the ref). Top-down frames run a little hot on the roof. |
| 7 | Text | 5 | None, per brief. |
| 8 | Ending | 5 | Logo (illumaesthetic.com V2, 760 px) cuts in on the last big taiko hit, holds through the measured decay, fades with the music at 34.6 s (-45 dB). |
| 9 | Technical | 5 | Spec met; no black/dup frames at cuts (only the 3 fade-in frames). |

## Known weaknesses / what I'd change with feedback
- Exploded/float shots are wide (camera 10-11.6 m) to keep the 12-panel stack inside 9:16; the car reads ~75 % of
  frame width there. Could tighten by dropping the skirts/fin to a smaller lateral offset and pushing to ~9 m.
- s10 hero after the lock is a slow linear push; the camera decelerates into the lock, then starts again at constant speed.
- Render budget: ~3.6 h of Blender (15-35 s/frame at 75 %/12 spp); 2 mm close-ups are the slowest.
