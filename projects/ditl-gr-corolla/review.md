# DITL GR Corolla: review of first cut v2 (2026-11-20)

Cut: `/home/user/media/ditl-gr-corolla/ditl-gr-corolla_firstcut_v2.mp4` (not committed). 990 frames, 33.0 s, no music (owner: "no music is
fine for now may be added later after final render"). **Not done:** the sales-sheet numbers are agent placeholders until the owner
confirms them.

## Numeric checklist (master session's list)
| Check | Result |
|---|---|
| Container | h264, 1080x1920, 30 fps, yuv420p, AAC, faststart, 990 frames |
| Layout | Picture is the 1080x1080 square at y=420-1499 (rows 420 and 1499 carry picture, rows 418 and 1501 are black). Bands are black away from the picture edge; the title sits inside the side margins (see the full-resolution line printed by the check, recorded in the edit log) |
| Cuts | All 13 cuts land on the planned frames (65, 113, 160, 255, 302, 350, 397, 444, 539, 587, 634, 682, 777). No dark frames. No flash frames at cuts (`tools/checks.py`) |
| Held frames | Three static holds, not errors: frames 110-113 (end of shot 2), 251-255 (end of shot 4), and parts of 603-613 (shot 11 while the man talks). The hands are still there; worth animating if the owner wants more motion |
| Jumps away from cuts | Only where planned: the like slam, the stamp, whip pans, face swaps, rev shakes |
| Visibility audit | `tools/visaudit.py`: no object on any shot has its first hide key after frame 1 |
| Arm overlaps | `tools/collide.py`: `{}` on all 14 shots (step 3; shots 1, 3, 6, 12 at step 2 after fixes). Shot 14's hands did not change with the grandma edit |
| Voice | Take edges silent (first/last 30 ms RMS 0.000-0.002). "I wanted something different." starts at frame 450; "Same." ends about frame 522, 17 frames before the cut at 539; "...different." ends about frame 954, 36 frames before the end |
| Loudness | -14.1 LUFS integrated, true peak -2.5 dBFS |
| Kit parts | Every car shot uses the GLB nodes at their own transforms (`cars.grc`): `part_front_lip_v2`, `part_canards`, `part_side_skirts_v2`, `part_rear_spats_v2`, `part_wrc_wing`, `part_wing_strakes`. In shot 4 the thrown copies end at the original transform (rotation 0, scale 1). Grandma's Spoiler Extension is the GR Corolla GLB node moved 40 mm down to the hatch roofline (an approximation: the hatch has no modelled extension) |
| Store titles (live, 2026-11-20) | Active: "Front Lip V2 – Toyota GR Corolla (Zenki, E210, 2023-2024)", "[BACKORDER] Canards / Dive Planes – Toyota GR Corolla (Zenki, E210, 2023-2024)", "Side Skirts V2 – Toyota GR Corolla (E210, 2023+)", "Rear Spats V2 – Toyota GR Corolla (E210, 2023+)", "[Backorder] WRC Wing V3 – Toyota GR Corolla (E210, 2023+)", "WRC Wing Strakes V2 – TOYOTA GR COROLLA (E210, 2023+)", "Spoiler Extension – Toyota Corolla Hatchback / GR Corolla (E210, 2019-)". Also active: "[Backorder] WRC Wing V3 – Toyota Corolla Hatchback (E210, 2019-2023+)", so the wing on the hatch would have been listing-true as well |
| Sales-sheet numbers | +$20,000, 29.99% APR, $1,499/mo x 84 months. Placeholders. $1,499 x 84 = $125,916, absurd on purpose; no MSRP is shown so nothing contradicts it |

## Rubric (adapted: this is a game-look short, not a scan reel)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | Thumb swipes within the first half second; the like slam lands at 1.8 s |
| 2 | Beat sync | n/a | No music yet; cuts are on the 1.58 s grid from video #1 |
| 3 | 1:1 match | n/a | |
| 4 | Model quality | 3 | The FL5 is a painted shell with a box wing and looks lumpier than the other cars |
| 5 | Story | 4 | "different" at 2 s, "Same." at 17 s, "...different." at 31 s; every scene between says "Corolla" |
| 6 | Look | 4 | Game textures and crunch on every frame |
| 7 | Text | 3 | All sheet/sign/bubble text reads at phone size; the numbers are unconfirmed placeholders |
| 8 | Ending | 4 | Hard cut to black on the whisper, no end card |
| 9 | Technical | 5 | See the checklist |

## Known weak spots
- Shot 14: the push-in crops grandma's hatch at the mirror's left edge, so the spoiler extension is hard to see; grandma's thumbs-up reads.
- Shot 8: grandma's wave is hidden by the door; she only grins.
- Shot 11: the man at the pump has no arms; the hand on the nozzle is small.
- Shot 6: the trolley overtaking him is hard to spot behind the A-pillar.
- Audio has not been heard by the agent; the owner judges the takes and the mix.
