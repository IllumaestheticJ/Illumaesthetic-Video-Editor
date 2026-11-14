# Mazda RX-7 FC3S scan reel v5 — self-review (training/rubric.md)

Output: `/home/user/media/work/rx7/out/mazda_rx7_fc_v5.mp4` — 1080x1920, 30 fps, 34.6 s (1039 frames, 13 bars). v4: review_v4.md.
User on v4: "the two shots at 17 seconds are pointless" -> the wheel close-up (16.0-18.7) and mirror glide (18.7-20.0) are cut.
The rear bumper removal now follows the radiator support directly on the 16.0 downbeat; reassembly 21.333, CTA 26.667,
logo 30.0 (4.7 s, fades with the music on the 13th bar). Stock car only, no kit (v4 feedback).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car turning from frame 1; first change ON the drop. |
| 2 | Beat sync | 4 | Every cut's first new frame = planned frame, no duplicates; strong-hit cuts -11..+10 ms; 21.333 (-45) and 30.0 (+40) are soft beats (rise x2.5-2.9). |
| 3 | 1:1 match | 4 | CTA listing scan -> phone; s6->s9 hood swap invisible. |
| 4 | Scan quality | 4 | Registered states only; plate flattened. |
| 5 | Story | 5 | Every shot now shows a part coming off, what is behind it, or the car going back together - no detail filler. |
| 6 | Grade | 4 | Silver on the render black. |
| 7 | Text | 5 | 7 plain labels; CTA text from the listing. |
| 8 | Ending | 4 | CTA kept at its natural 3.33 s (the card ends fading toward the logo; a 4 s hold showed a dim logo for 0.7 s); logo 4.7 s. |
| 9 | Technical | 4 | Specs met; no new renders. |

## For the next agent
- cta_card.py ends with its own fade toward the logo: do not stretch it with `dur` (tpad clones a dim-logo frame); lengthen the logo instead.
- "Pointless" detail shots (wheel, mirror) in a teardown reel: every shot should show a part moving, what's behind it, or the reassembly.
