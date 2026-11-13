# Toyota Sera scan reel - self-review (training/rubric.md)

Deliverable: `/home/user/media/work/sera/out/toyota_sera_v4.mp4`: 1080x1920, 30 fps, 39.27 s. Scan only, with 4 factual labels.
Order (front -> side -> rear, each section once):
- whole car, pushing in
- front wheel
- FRONT: hood opens; front bumper comes off and shows its inner face (label); camera in on the structure behind it (label)
- SIDE: both butterfly doors
- REAR: same pattern as the front (2 labels)
- progressive explode -> reassembly orbiting to the listing's view -> 1:1 into the mobile listing CTA

Previous cut (v2, turntables and an all-at-once explode) is in `project_v2.yaml` / `training/examples/toyota-sera/`.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car on frame 1 and already pushing in (front-right 3/4, 73-75 % of width). There's no transformation in the first 1.5 s; the brief asks to open on the whole car |
| 2 | Beat sync | 5 | Measured on the decoded audio of the delivered file: all 8 cuts land 3.3-5.6 ms after the kick attack (limit ±16.7 ms). Big moments land on phrase downbeats: front 7.235, side 16.835, explode 26.435, lock 33.635, logo 36.035 |
| 3 | 1:1 match | n/a | Scan-only reel. IRL footage is listed in clips.md |
| 4 | Scan quality | 4 | Every state is registered, with one rigid levelling transform and every prep pinned with `--like`. Hood and doors open only because real Hood-open and Door-Open scans exist; there is no trunk shot because there is no hatch-open scan. Weak spots: dark scan holes in the grille, and the hood is the most constructed panel (closed skin + inner side from the open capture) |
| 5 | Story | 5 | One section at a time, front to back. The bumper-removed data is the hero: the part comes off, turns to show its inner face, clears frame, and the camera moves in and holds on what was behind it. The explode is progressive, then the car reassembles |
| 6 | Grade | 5 | House satin silver on black, AgX, -0.35 EV, consistent across shots. Per-frame luma check: no dropouts. The one step (rear frame 58) is the bumper leaving frame |
| 7 | Text | 4 | 4 labels, over scan only, clear of the car and above the bottom 20 %. Each label pairs its part name with a triangle count read from the STL headers; no specs. The sub-line is small mono text, readable but not large on a phone |
| 8 | Ending | 5 | v4: the reassembly locks on b56 while orbiting to the mobile listing's camera (solved, IoU 0.972); on b60 that exact frame shrinks 1:1 onto the car in the phone (handoff diff 0.01, ~1 px landing), then logo, SCAN DATA AVAILABLE NOW and ILLUMAESTHETIC.COM settle with a slow push-in |
| 9 | Technical | 4 | h264 yuv420p, 1080x1920, 30 fps, AAC, no black frames, no reused shot. 1178 frames, one fewer than planned (the music ends at 38.435 s, so the end hold is unaffected) |

## Changes in v4 vs v3 (user: "add the scan data call to action to the end, where it aligned to the website mobile listing")
- Fade + logo card replaced by the mobile listing CTA; reassembly camera re-rendered to end on the listing's view.
- The phone shows the real page (title, $800.00, Dataset dropdown are the site's); no text of ours beyond the offer line and URL.
- The URL's baseline sits right at the bottom-20 % line at the end of the push-in.

## Changes in v3 vs v2
- Removed turntables, the rear orbit, the nose slide and the rotating top-down: wasted rotations / not in the brief's order.
- Front and rear are each one held shot built around the bumper-removed states (addendum C), with 4 labels.
- Exploded view is progressive (hood -> front bumper -> doors -> rear bumper on successive beats); reassembly locks on the beat; then fade and a small logo.
- Persistent data is off for every animated shot; luma check is clean.

## What I'd want the reviewer to check
- Label wording: triangle counts are exact header values. Are they wanted, or should labels be part names only?
- The rear bumper's exit is fast (frames 56-58 of the render), so the bumper reads as clearing the frame quickly.

## Process notes for the next agent
- cutcheck.py's broadband half-peak reads ~110 ms early when a bass note sustains under each kick. Measure the kick click on a >2 kHz high-band envelope instead.
- Typewriter label subs need about 0.9 frames per character plus the title in-animation. Check the last frames of each label in the delivered file, not only the first ones.
- `ive director` matches whole-car views by silhouette: a front 3/4 and a rear 3/4 at the same scale are flagged as a repeat. Look before cutting.
