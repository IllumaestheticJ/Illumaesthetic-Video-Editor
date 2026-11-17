# Self-review - Toyota GR Corolla v12b (`toyota_gr_corolla_v12.mp4`, 44.5 s, 1080x1920)

v12b (user: "missing the canards, and the full lip kit and wing are improperly placed"): engineering's parts are in
engineering's car frame, offset from ours by 0.79 deg and (4, 59, 30) mm - found by ICP of engineering's own full-car
scan (V2 reference blend) to our car (99 % within 12 mm, 2.5 mm rmse). Re-placed the V2 lip, skirts, spats and the wing
(wing now within 7 mm of engineering's Wing_V2.2 CAD). Canards added (user's Drive folder: Projects_/Corolla GR/3d
Printed Parts/Cannard), rising in with the lip; label EPSILON AERO V2 LIP + CANARDS.


v12 = teardown (unchanged through the crash beam) + reassembly + finale (user on v11: "The epsilon aero wing needs to
go on as the car reassembles... the small side pieces on the trunk need to come off... mounted and aligned properly";
"After the car is fully assembled, I want a full 360 of the car while the epsilon V2 lip kit and canards also gets
installed"). Reassembly front first so the car is consistent when the wing goes on: hood + ducts + beams + bumper,
crash beam + rear bumper/diffuser, hatch, factory side covers off + WRC wing on, then a 2-bar 360 where the V2 lip,
skirts and spats rise into place as the camera passes each. End card with the contact line. 18 bars. v11: review_v11.md.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Unchanged opening. |
| 2 | Beat sync | 4 | Every shot cuts on a 70-frame downbeat; 360 holds 2 bars; dip into the end card on downbeat 18. Same music grid as v9-v11. |
| 3 | 1:1 match | n/a | No IRL. |
| 4 | Scan quality | 4 | Wing re-registered to the CMM scans of its own endplates on this car (mirror-symmetric to 2 mm; matches engineering's Wing_V2.2 CAD bbox). Side covers traced on shut lines, recessed backing under them. V2 kit is engineering's car-frame data. Missing front-left/right-rear wheels mirrored from the complete ones so the 360 has four wheels. |
| 5 | Story | 5 | Teardown -> JR intercooler -> rear teardown -> everything flies home -> covers off, wing on -> 360 with the V2 kit -> end card. |
| 6 | Grade | 5 | One silver look throughout. |
| 7 | Text | 5 | EPSILON AERO WRC WING after it seats; EPSILON AERO V2 LIP KIT after the lip seats, gone before the dip; end card contact line. No invented numbers. |
| 8 | Ending | 5 | Complete car with wing + V2 kit in a full orbit, end card. |
| 9 | Technical | 5 | 1080x1920, 30 fps, 1334 frames, all frames verified; -16.5 LUFS, true peak -1.6 dBFS. |

Risk: 44.5 s is long for short form; the crash beam returns by state swap, not as a moving part.
