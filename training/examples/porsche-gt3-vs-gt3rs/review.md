# Review - GT3 vs GT3 RS (992) split-screen, v3

Output: /home/user/media/work/gt3vs/out/gt3_vs_gt3rs_v3.mp4 (1080x1920, 42.5 s). Previous: review_v2.md.

## What changed (user feedback on v2)
1. "When the GT3 rear bumper comes off, show the bumper-removed scan underneath" - rear base rebuilt (comp_gt3b: the
   2023 stripped-state scans + the 2026 GT3-992-ExhaustOn-UWT scan, ICP-registered); g_rear restaged so the camera
   pushes in low under the lifted bumper and holds on the exposed rear for 4 beats (label "UNDER THE REAR BUMPER").
2. "CTA is wrong - like the 240SX videos" - text CTA and logo card removed. After the lock both cars sweep round the
   tail and land on the angle of their product listing's scan view (silhouette IoU 0.977 GT3 / 0.962 RS), dissolve into
   screenshots of the two real listing pages, zoom out to two page cards with SCAN DATA NOW AVAILABLE, logo, URL.

## Self-score (training/rubric.md, 1-5)
- Story / one focus per shot: 4 - the rear reveal now has its own held beat.
- Match / transition: 4 - landing frames overlay the listing views within a few px (match_end.jpg, check_v3.jpg);
  the look still changes silver-on-black -> viewer grey through the dissolve (no grade morph).
- Scan look: 3 - the under-bumper structure is real scan data but still fragmented.
- Sync: 4 - cuts unchanged on the kick grid; sweep lands b77, zoom-out b78-b82.
- Text: 4 - no on-screen numbers; all end-card text is the real page.

## Known limits / open
- No dedicated GT3 REAR bumper-off capture was found in the Drive folder: "Nikitas GT3 Full Underbody + Bumper Off" has the
  FRONT bumper off, the 2026 Exhaust scans are taken from below. If a cleaner rear capture exists, it needs pointing out.
- The listing pages open on the 360 viewer, so the 1:1 match targets that frame, not the grey "Photos" cover render.
- g_side / g_wide were not re-rendered on the new base (difference is on the underside, not visible from those angles).
- The sweep shots were not beat-checked with a cutcheck run; verified by frames only.
