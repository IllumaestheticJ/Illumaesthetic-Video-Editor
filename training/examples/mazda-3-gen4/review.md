# Mazda 3 (gen 4) hatch scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/m3/out/mazda_3_gen4_v1.mp4` — 1080x1920, 30 fps, 38.2 s (1146 frames), h264 yuv420p + AAC.
Scan only (no IRL, no text). Music: mazda-3-gen4_track.mp3 (generated for this reel), 110 BPM, kick drop 19.68 s, ends ~38 s.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable moving from frame 0, but the track is near-silent for the first ~1 s (ambient intro), so the first 2 s are calm by design. |
| 2 | Beat sync | 5 | Grid from kick peaks (110.02 BPM). Frame-diff cuts in the delivered file: 132, 263, 329, 394, 460, 590, 689, 1049 = −15..+16 ms from the beat (≤ ½ frame). Wing lift b30→b34, explode separates b44, locks b60 32.77, top-down lands on the drop. |
| 3 | 1:1 match | n/a | No IRL footage in this brief. |
| 4 | Scan quality | 4 | 4 mm full car / 2 mm close-ups, levelled, jack + floor removed, debris stick removed from the 2 mm crops. Remaining: tyres are rings without contact patch (car scanned on jacks), front-left wheel partly a hub, small jack-pad remnant on the right sill, small gaps at the headlamp top edge. Grille (holey) kept out of frame; right rear quarter (scan ribbing) never shown. |
| 5 | Story | 4 | Turntables → headlamp/flank/tail-lamp Kodo close-ups → wing comes off onto its real mounts (Wing Removed state) → top-down on the drop → exploded stack → logo. The explode is light (2 parts) because only the wing registers; the aero-kit spoiler floats but is never seated (not registered). |
| 6 | Grade | 5 | House silver on render black (bg RGB 7,7,9), AgX, consistent across shots; car median luma ~161 (Temerario ~200, ours slightly more contrast). |
| 7 | Text | 5 | None (brief). |
| 8 | Ending | 5 | ILLUMAESTHETIC logo (site V2 logo) cuts in on b64 34.95 s, holds through the last kicks (36.59) and fades with the track's decay; video ends 38.2 s where the music has died (−46 dB). |
| 9 | Technical | 4 | Specs met. The assembler repeats one frame before each cut (hold frame); s7 ends on a fast yaw spin as the camera passes over the top (smooth, no jump). |

## Things a reviewer may ask about
- Hatch Upper Trim Panel is the rear wing itself (registered to the Rear Wing scan, 93 % coverage) — shown once.
- OEM Aero Kit Spoiler is a different design in its own (inch) frame and does not fit this car's scan; it floats above the wing in the explode and leaves — never placed on the car.
- No door-open shot: Side Skirt Door Open only covers the sill; no door part or cabin scan.
