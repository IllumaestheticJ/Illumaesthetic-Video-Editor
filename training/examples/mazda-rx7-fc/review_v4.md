# Mazda RX-7 FC3S scan reel v4 — self-review (training/rubric.md)

Output: `/home/user/media/work/rx7/out/mazda_rx7_fc_v4.mp4` — 1080x1920, 30 fps, 37.3 s (1119 frames, 14 bars).
User on v3: "just do the car, no kit". v4 = stock S5 scan only, same T-Pain track/excerpt (drop at 5.333), same mobile CTA
(the listing's 2025 FC3S scan into the phone) and 760 px logo. Built entirely from existing stock renders - no new Blender work.

Order: whole stock car (2-bar lead-in) -> ON the drop the hood opens (Hood Up) -> captured hood lifts off over the bay ->
front bumper (Front Face part) off -> radiator support / crash beam -> wheel -> mirror -> rear bumper off -> rear crash beam
+ mounting points -> rear bumper, front bumper and hood fly home, clean car -> CTA -> logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car turning from frame 1; first change ON the drop. |
| 2 | Beat sync | 4 | Every cut's first new frame = planned frame, no duplicate frames. Strong-hit cuts -22..+10 ms of the kick; 4 cuts sit on soft grid beats (rise x1.8-2.7) where the detector picks neighbouring events (-51..+58 ms). |
| 3 | 1:1 match | 4 | CTA listing scan on the solved viewer camera -> phone; s6->s9 hood swap invisible. |
| 4 | Scan quality | 4 | Only registered state scans; plate flattened; hub-speckle and cowl-hole frames skipped. |
| 5 | Story | 4 | Stock teardown of the three panels that have removal scans, reassembly, CTA. No kit (user). |
| 6 | Grade | 4 | Silver on the render black throughout. |
| 7 | Text | 5 | 7 plain labels on scan shots, none on moving parts; CTA text from the listing. |
| 8 | Ending | 5 | Clean car on 25.333-30.667, CTA on the 30.667 downbeat, logo on 34.0, music fades on the 14th bar. |
| 9 | Technical | 4 | Specs met; reused v2 renders edge-checked (reassembly starts at frame 17 so the parked bumper is never half-cut at rest). |
