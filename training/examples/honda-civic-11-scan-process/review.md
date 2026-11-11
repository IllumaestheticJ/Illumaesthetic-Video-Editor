# Honda Civic EK scan-process reel v4 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/civic_ek_scan_process_v4.mp4` — 1080×1920, 30 fps, 27.53 s, H.264 + AAC. Earlier: review_v1/v2/v3.md.
v4 = parent "v2 brief for all reels" (user approved "make v4"): travel order front -> left side -> rear -> top/hero, each section once,
wide IRL frame at cut B, short end card, exact HUD numbers, cuts measured on decoded-audio kicks. Plan: direction.md.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | powdering the front + build/snare fill -> 1:1 cut to the scan on the drop kick (3.20 s, +1 ms) |
| 2 | Beat sync | 5 | cutcheck: +1, -10, -15, +6, +1, +1 ms vs kicks; 16.33 s cut sits on the break downbeat (no kick by design) |
| 3 | 1:1 match | 5 | cut A cam_A 18.3 mm; cut B now WIDE rear (cam_B2 24 mm, median silhouette 2.9 px) - onion of f320/f321 shows no ghosting |
| 4 | Scan quality | 4 | intact full-car scan; rear lenses clean on the push-in; right mirror touches the frame edge at the push-in peak (~13.3 s, detail beat) |
| 5 | Story | 5 | front IRL -> front scan -> scanner on the left side -> powder on the hatch -> rear wide -> 1:1 rear scan push/crane -> software in the break -> top-down sweep on the re-entry -> listing hero -> listing. No section twice, one orbit-type move per section |
| 6 | Grade | 4 | HLG tonemapped; software beat is an upscaled viewport crop |
| 7 | Text | 5 | 24,997,508 TRIANGLES CAPTURED (STL header) on the front scan only; EXTERIOR SCAN (listing "Dataset: Exterior Only") on the rear scan; nothing over IRL |
| 8 | Ending | 5 | sweep lands on the listing angle, morph done before the dissolve, end card 4.67 s (v3 had a 2.7 s dead hold); URL last, ~1.8 s hold; ends on a downbeat with a 0.4 s fade |
| 9 | Technical | 5 | lumacheck: no dropouts in S2'/S3'; frame-accurate holds |

## Learned this round
- Keyframed camera moves between very different poses need aim-point interpolation (slerp the view direction about a lerped
  target), not loc-lerp + rotation-slerp: the latter swung the car half out of frame mid-move (tools/campath.py `aim`).
- Blender 5 actions are layered: reach fcurves through layers -> strips -> channelbags.
- The widest IRL frame for a 1:1 is often at the start of a "detail" clip (v_1958_06 0-1.4 s) - scan every clip's first second.
