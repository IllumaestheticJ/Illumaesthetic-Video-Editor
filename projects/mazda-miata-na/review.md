# Mazda Miata NA scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_na_v2.mp4` — 1080x1920, 30 fps, 35.57 s, H.264 yuv420p + AAC, faststart.
v1: review_v1.md / project_v1.yaml. v2 answers the reviewer ("car is cropped in beginning, repetitive steps; talk about front
bumper data first, show it, move to back") and the parent's v2 brief + addendum.

Order (one continuous sequence per section, front → side → rear):
whole car (s1) → FRONT: bumper lifts out and turns to show its scanned inside (s2) → bumper-removed front end, crash beam,
mounts, radiator, labelled (s3, hero) → hood opens on its fitted hinge (s3_hood) → SIDE dolly (s4b) → REAR: trunk
closed → half → open, the three captures (s5) → trunk well (s6) → TOP: everything goes home (s7) → hold, dip, small logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, fully in frame with margins, moving from frame 1 (linear push, no ease-out stall). First transformation (bumper lifts) at 5.0 s on the phrase kick; the intro is the track's calm 8 bars. |
| 2 | Beat sync | 5 | Measured on the decoded audio of the delivered file: all 8 cuts −12..+16 ms from the kick (≤ ½ frame). 152/685 moved one frame after measuring +24/+22 ms. |
| 3 | 1:1 match | n/a | No IRL footage. |
| 4 | Scan quality | 4 | Real bumper-off capture is the hero (old-bumper remnants removed from the base); open lids are fitted to the real open-state scans (no faked openings). Plate blanked. Hood underside capture partial (camera kept on the scanned side). |
| 5 | Story | 4 | Front bumper data first (part, then what's behind it), then side, then rear, then the whole car re-assembled. Each section appears once. Only the bumper has a removed-state scan, so only the bumper comes off. |
| 6 | Grade | 5 | Silver on pure black, AgX. |
| 7 | Text | 4 | Three sequential label cards, one at a time, on black (never over the car): FRONT BUMPER / INSIDE + OUTSIDE SCANNED; FRONT BUMPER REMOVED / WHAT'S BEHIND IT, SCANNED; CRASH BEAM / MOUNTING POINTS · RADIATOR. No numbers. Small subtitle line is thin on a phone. |
| 8 | Ending | 5 | Top-down hold, dip to black, then the 'now available' CTA on the b56 phrase change (31.7 s): the mobile listing (MAZDA MIATA (NA) 3D SCAN, $500) pulls back into a phone frame, MIATA NA SCAN NOW AVAILABLE, logo, ILLUMAESTHETIC.COM holds ~1.3 s while the audio fades. |
| 9 | Technical | 5 | Specs met; every rendered frame luma-checked (no black/dark frames; persistent data off); first/mid/last of every shot checked for clipping; only the planned dip/fade frames are dark. |

## v2 fix (reviewer: "the old bumper still shows when you take the new bumper off the main scan")
- The full-car scan carries a different bumper (round fog-lamp holes, deeper chin) than 'Front Bumper Only'. The explode
  base only cut car skin within 9 mm of the removed part, so the old bumper's chin/corners stayed. New base
  (comp_explode2): ahead of the front tyres and below the hood line, keep only what the 'Front End Bumper Off' capture
  confirms (−136,823 tris). s1 now shows that base + the removable bumper, so the same bumper is on the car before it
  comes off. Re-rendered s1, s2, s3_front_removed, s3_hood, s4b_side, s7; re-checked luma, framing and cut timing.

## CTA (user: "add the Miata scan 'now available' CTA - using the mobile version of the site")
- Live listing captured on an iPhone 13 viewport (Playwright); only edits: hid a third-party pin icon that can't load in
  this sandbox, and one swipe on the 360 viewer to clear its 'Drag to rotate' hint. cta.json -> WebZoom (new optional
  mobile layout props). Note: the listing's only dataset is 'Exterior Only'; the bumper-off / engine bay / trunk state
  scans shown in the reel are not a listed dataset.

## ive director (v2)
- Sections: whole 5.0, front 11.1, side 2.2, rear 8.9, top 4.4, end 4.5 s — one continuous block each.
- Flags "s3_hood ~ s4b_side" and "s4b_side ~ s5_trunk": checked the best-matching frames (front-¾ hood open vs driver door;
  rear wheel vs rear-¾ trunk) — different subjects, IoU inflated by the car filling a mid-frame band. Kept, logged.
- s1 0.9 s "dead" tail (ease-out) fixed with a linear push.

## Known weaknesses / for the next pass
- s4b_side and s6_trunk_well are deliberate close-ups: the body runs off the frame edges (subject itself is inside).
- Only the bumper exists as a removed-state scan; hood/trunk come off nowhere — they only open (registered open captures).
