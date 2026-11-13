# Mazda Miata ND scan reel - self-review (v8, delivered)

v8 = the user's note on v7: "the drop is right when the music ends". File `/home/user/media/work/miata/out/miata_nd_v8.mp4`
(34.9 s, 1046 frames). Music 21.052-55.9 s of Megalomaniac: the 1-bar riser (43.1 s) plays under the trunk opening and the
explode separates on the drop (45.488 s), reassembly + CTA + logo ride the new section, music fades over the logo.
Re-time of v7 (no new renders). Beat sync 5 (drop cut within 3 ms of the riser cut-off / sub kick).

## Earlier reviews (v7 and before) kept below
# Mazda Miata ND scan reel - self-review (v7, delivered)

v7 = the user's notes on v6: music started too early and missed the drop; the trunk lid took a chunk of the tail light.
File: `/home/user/media/work/miata/out/miata_nd_v7.mp4` (33.9 s, 1018 frames, 1080x1920).
- Beat sync 5: music from 2 bars before the drop; hard cut ON the drop (frame 114) into the bumper popping off on the hit;
  hood lands on the k20 bar accent; reassembly locks on k52.
- Scan quality 4: trunk lid no longer carries tail-light pieces (open-state scan decides what stays on the body); lamp housings
  stay whole when the lid opens and in the explode.
- Story: whole car over the build -> DROP: front bumper off -> crash beam -> hood -> side (skirt holds on the sill) -> rear bumper ->
  trunk -> explode -> reassembly -> mobile CTA -> logo. Headlight detail cut to reach the drop in 3.8 s.

## Earlier reviews (v6 and before) kept below
# Mazda Miata ND scan reel - self-review (v6, delivered)

v6 = the user's notes on v5: edit from the beginning of Megalomaniac, drop the wheel close-up, hold on the side skirt.
File: `/home/user/media/work/miata/out/miata_nd_v6.mp4` (35.8 s, 1074 frames, 1080x1920).
- Beat sync 4: music from 0.432 s; intro verified to be on the same 128.05 BPM grid as the kick (phase within 4 ms), cuts on
  k = -24 -20 -12 -4 2 12 18 22 26 30; kick entry lands on the hood reaching its captured open pose. Onset checks in the intro
  read +24..+95 ms because the arpeggio has notes between beats - the grid itself is right.
- Story 4: whole car -> lamp -> front bumper off (inner face) -> crash beam / front structure pass -> hood opens on the kick entry
  -> side (mirror, then skirt off and HOLD on the exposed sill) -> rear bumper off -> trunk -> explode -> reassembly -> CTA -> logo.
  No wheel close-up; each section appears once; nothing cuts away mid-action.
- Length: 35.8 s (v5 30.1 s) - the song's intro is 15.5 s and carries five shots. Longer than the 15-30 s house default.

## Earlier reviews (v5/v4/v3) kept below
# Mazda Miata ND scan reel - self-review (v5, delivered)

v5 = the user's notes on v4 (feedback.jsonl): edit to the uploaded Megalomaniac track, hood cut line corrected, 1:1 match into
the mobile listing. File: `/home/user/media/work/miata/out/miata_nd_v5.mp4` (30.1 s, 903 frames, 1080x1920).
- Beat sync 4: 128.05 BPM onset grid; cuts -21..+20 ms on clear onsets; the hood-shot cut sits on the off-grid stutter-fill hit
  (238.96 s, +10 ms); the hood lands on the drop. One weak-onset cut (21.6 s) reads +120 ms in a dense passage (measurement noise).
- Scan quality 4: hood cut on the real shut lines (cowl arc, fender-top seams, headlight tops, badge line) from a high-pass height map.
- 1:1 into the CTA 5: reassembly ends on the listing camera solved from the screenshot (IoU 0.975); onion check shows wheels,
  glass line, door and lamps coinciding; scan toned to the listing grey, then dissolves into the page's own image.
- Ending 5: CTA phone (title, ILLUMAESTHETIC.COM) -> 760 px logo; music fades out over the logo (the track continues past the reel).

## Earlier reviews (v4/v3) kept below
# Mazda Miata ND scan reel - self-review (v4, delivered)

v4 = v3 + the user's notes on v3 (feedback.jsonl): rear-wing residue on the trunk deleted, mobile call-to-action
transition into the final shot, logo 760 px. File: `/home/user/media/work/miata/out/miata_nd_v4.mp4` (32.1 s, 963 frames).
- Scan quality 4 -> 4: wing fragments gone from the closed and open lid (fills cleaned, 6 shots re-rendered); thin seam lines
  at the lid gap remain (trunk-opening edge visible through the panel gap).
- Ending 5: reassembly locks on the last hit -> car shrinks into a phone showing the real ND listing (CTA) -> 760 px logo.
- Technical: luma scan clean on every re-render (incl. the s_side frames resumed after a worker restart); cuts unchanged.

## v3 review (kept for the record)


File: `/home/user/media/work/miata/out/miata_nd_v3.mp4` - 1080x1920, 30 fps, 29.5 s (885 frames), h264 yuv420p + AAC, faststart.
v3 = the user's v2 brief + addendum (relayed by the parent session). Scene order from the scene-director agent
(`direction.md`, `director.md`). v1 review: `review_v1.md` (file miata_nd_v2.mp4 was v1 with an s7 fix).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, front 3/4, moving from frame 1 (car 10-91 % of the width); first cut on the first kick at 2.07 s |
| 2 | Beat sync | 4 | Cuts on even kicks, measured against the decoded audio's broadband onset: -11..+13 ms on clear onsets (one -23 ms); later cuts sit in a dense section where the onset rise is only x1.5-2 (measurement noise -36..-62 ms). Parts lock on the last hit (frame 807) |
| 3 | 1:1 match | n/a | Scan-only reel |
| 4 | Scan quality | 4 | Plate flattened; jack stands dropped; hood/trunk panels are single skin (cameras keep away from their undersides); mirror cap shows small dark patches; hood speckle visible in the engine-bay shot |
| 5 | Story | 4 | Front (lamp -> bumper off + crash beam -> hood to captured open pose -> wheel) -> side (mirror mount, skirt) -> rear (bumper off + exhaust/structure -> trunk to captured pose) -> progressive explode (front angle, rear angle) -> reassembly on the last hit -> fade -> small logo. Each section once; no repeated view |
| 6 | Grade | 5 | House silver; no lighting dropouts (per-frame mean luma scanned for every render folder) |
| 7 | Text | 4 | 4 factual labels, bumper-removed sections only, 80 px inside the edges, above the car. 'ENGINE BAY' dropped: no clear area off the car. 'REAR CRASH BAR' not used: not clearly readable behind the exhaust |
| 8 | Ending | 5 | Reassembly locks on the last hit, fades to black, 300 px logo over the decay |
| 9 | Technical | 5 | Exact frame counts (concat assembler), no frozen frames at cuts (only eased-start frames and a planned 0.27 s pause on the bumper's inner face) |

## Changed from v1 (why)
- Opener re-framed to the whole car (v1 cropped). s1/s2 duplicate turntables, s7 top-down rotation and the all-at-once s8 explode cut.
- Bumper-off sections are the hero beats: the part turns its scanned inner face to the lens in clear black, then the camera pushes in on what's behind it.
- Hood and trunk open only to their registered captured poses ('Bumper Off Hood Open', 'Rear End Trunk Open Bumper Removed'). No door.
- Explode is progressive over two tight angles, then reassembly. Parts translate; only the bumpers (scanned inside) and the right mirror (scanned mount plate) turn.
- Cut grid moved 31.8 ms earlier onto the broadband kick onset.

## Open for the reviewer
- The bumpers exit through the bottom of frame while the camera pushes in (moving, not parked) - say if you'd rather they leave sideways.
- Right side only for the mirror/skirt (the skirt state scan exists for the right side only).
