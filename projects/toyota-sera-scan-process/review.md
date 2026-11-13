# Toyota Sera scan-process reel v7 - self review (training/rubric.md)
Output: /home/user/media/work/out/sera_scan_process_v7.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 29.97 s.
Plan: direction.md (scene director). v1/v2 reviews: review_v1.md .. review_v6.md.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Real car 1.77 s, 1:1 cut to the scan on the 1.8 s phrase change. |
| 2 | Beat sync | 5 | Cuts measured on the DECODED audio of the delivered file: 1.800 3.600 6.000 7.200 9.600 11.400 13.800 15.600 18.000 19.800 - all within +/-7 ms of kick peaks (< 1/2 frame). |
| 3 | 1:1 match | 3 | Opening: wider crop (zoom 1.0), aligns within a few px. Front lift: wider, hand-placed camera on a blurred frame, ~20 px. Rear: hard cut (bumper never fully off on camera). |
| 4 | Scan quality | 4 | No lighting dropouts (per-frame luma checked on every render). Rear close-up shows the tail-light holes of the Rear Bumper Removed capture (real scan holes, kept short). |
| 5 | Story | 4 | One sequence per section: front (real car, 1:1, real bumper lift, 1:1 bay, bumper inside+outside, what's behind it) -> side (butterfly doors from the Door Open scan) -> rear (real pull, bumper inside+outside, behind it) -> x-ray reassembly -> listing. Still no handheld-scanner footage (none exists). |
| 6 | Grade | 4 | S-Log3 LUT; daylight vs shop warmth differ (real). |
| 7 | Text | 5 | Static labels only over scans; numbers = STL header counts (14,999,999 / 1,800,000 / 4,999,998 / 10,500,000); "removed"/"behind the bumper" labels name what is visible. |
| 8 | Ending | 4 | X-ray lands on the listing hero angle (clay, listing grey) and dissolves; end card 3.6 s, no dead frames; rear-wheel ghost in the dissolve remains. |
| 9 | Technical | 5 | Spec met; director report: no dead frames, every shot tagged with section + focus; only flagged repeat is the intended x-ray -> listing dissolve. |

## v3 changes (all-reels brief + addendum)
- Order front -> side -> rear, no ping-pong; v2's rear-first block and the wide spinning explodes (s3_rear, s6_frontx) cut.
- Bumper-removed hero beats: each bumper drops below the car into black and turns to show its scanned inside, then a
  close 3/4 on the exposed structure from the bumper-removed state, with labels.
- New side beat: butterfly doors from the 'Door Open' capture as captured (no faked opening), composited on the full car.
- Frames: first/middle/last of every shot checked; parts stacked vertically so nothing leaves the 9:16 frame.
- End card trimmed 6.6 -> 3.6 s; x-ray re-timed (front bumper home 20.4, rear on the 21.0 phrase change).

## Gap to learn from
v1/v2 laid scan shots out by template (rear, front, x-ray) and framed explodes wide; the feature-driven order and
stacked part paths fixed both without new footage.

## v4 (user: "include shots of the bumper we designed and put them into the scan data, then cut to the finished car")
- Found: designed kit CAD on Drive (Ron's Folder/Toyota Sera/Print) and the finished car in the posted short
  'Toyota Sera at home'. Kit registered to the scan (yaw + ICP translation, then 2.70 deg pitch from tyre contacts);
  fit checked from front, rear and side.
- New shots: designed front bumper rises onto the bumper-less scan (11.4-13.2), designed rear bumper (21.6-23.4),
  labelled NEW FRONT/REAR BUMPER - DESIGNED ON THE SCAN DATA; then finished car front (23.4) and rear (24.6), hard cuts
  on kicks; listing card 25.8-29.4. X-ray reassembly removed (stock bumpers returning contradicts the story).
- Cuts on decoded audio: all within +/-7 ms of kicks. Director: no dead frames; one flagged repeat (stock bumper off
  vs designed bumper on share the camera on purpose - same view, different part).
- Scores changed vs v3: Story 4 -> 5 (scan -> design -> finished car), Ending 4 -> 3 (hard cut into the listing instead
  of the position-locked dissolve; finished-car clips are a 1.43x upscale of a captioned short, caption cropped out).
- Open: raw (uncaptioned) finished-car clips would look better; ducktail and side skirts exist as CAD but are not shown.

## v5 (user: "missing side skirts and the rear wing, and missing the final transition from the modified car in SG to the finished 3D printed car")
- Ducktail (Print/Ducktail.stl) and both side skirts registered with the same kit->scan transform as the bumpers
  (match/kit_to_scan.json); seating checked in clay renders.
- Rear design shot: rear bumper rises on, then the ducktail drops onto the hatch (label NEW REAR BUMPER + DUCKTAIL), on the 21.0 phrase change.
- New scan_kit_final (22.8-24.6): doors-up scan wearing all five parts, side skirts slide on, camera pushes in and ends on
  match/cam_fin.json -> hard 1:1 cut on the 24.6 beat to the real finished car, then the rear, then the listing.
- Timing: doors 2.4 -> 1.8 s, end card 3.6 -> 3.0 s, total 30.0 s (inside the music).
- Checked: frames around every changed cut, end-frame onion (qa/v5_onion), per-frame luma (min 28.6, no dropouts).

Scores vs v4: 1:1 match stays 3 - the new scan -> finished-car cut lines up on bumper, bonnet, windshield and wheels within
~15 px at 540 w, but the real doors are opened to a different angle than the Door Open scan, so the door tips jump.
Story 4 -> 5 (kit complete, ends scan -> real). Only the car-left skirt is visible in the final shot; the finished-car clips
are still an upscaled crop of the captioned posted short (raw clips would fix both sharpness and framing).

## v6 (user: "zoom out more of the irl photos so its not as cropped")
- Finished-car clips now use the full 1080x1920 frame of the posted short: the burned-in caption sat entirely on clear sky,
  so tools/uncaption.py replaces it with a per-column sky ramp + grain (checked first/last frame of both clips: no trace).
  No crop, no 1.43x upscale -> sharper, and the whole car with road and horizon is in frame.
- match/cam_fin_full.json = same solved pose on the full sensor; scan_kit_final re-rendered; end-frame onion (qa/v6_onion)
  holds the same alignment as v5. SIDE SKIRTS label moved to the top (car now sits in the lower half).
- The FX30 shop shots were not changed: they already use the full frame height (crop zoom 1.0); going wider would need bars.
- Checked: frames around the 24.6 / 25.8 / 27.0 cuts, luma min 28.6 (no dropouts), 29.97 s.

## v7 (user: "crossfade the 1:1 shot")
- Kitted scan -> finished car is now a 0.4 s crossfade (24.4-24.8) centred on the 24.6 beat, both sides frozen on the
  matched frame; the real clip then plays 24.8-25.8. Later cuts unchanged (25.8, 27.0). Frames 24.3-24.8 checked: body
  stays registered through the fade; the door-angle difference now reads as a soft ghost instead of a jump.
- The IRL -> scan cuts at 1.8 s and 6.0 s remain hard cuts (standing rule).
