---
name: scan-video-edit
description: Edit an Illumaesthetic "240sx-style" scan-process video from Dropbox shop footage and engineering-drive 3D scan data - real footage of the car being scanned and taken apart, a 1:1 perspective cut from the real car to its scan on a beat, Blender scan renders in the house silver look, beat-synced assembly, Remotion HUD, the mobile store CTA, and recording feedback so future edits improve. Use for any request to edit/cut a reel or video that involves scanning footage, scan data, STL/OBJ car scans, Blender renders of a scan, "IRL to scan" transitions, or a "240sx style" video. For scan-only teardown reels with no shop footage use the temerario-scan-reel skill.
---

# Scan video edit ("240sx style")

Updated 2026-11-17. First follow `CLAUDE.md` (the mandatory reading list), then query the graph
(`graphify query "<car> scan process"`) and read `knowledge/feedback/<project>.md`. Every scan-side rule in the
`temerario-scan-reel` skill applies here too: its `references/reviewer-rules.md` (only real scan data, shut-line cuts,
nesting order, no clipping, labels, music, logo) and its `references/scan-cutting.md`. This file adds what is specific
to footage plus scan.

Approved examples:
- `projects/240sx-scan/`, the original;
- `projects/c5-corvette-scan-process/` ("C5 reel is great");
- `projects/honda-civic-11-scan-process/` v5 ("nice");
- `projects/toyota-mr2-sw20-scan-process/` v2/v3, with Riders on the Storm.

## Story

1. **Open on the 1:1 cut.** The transformation is the hook, not something 8 s in (240SX). Real footage of the car being
   scanned comes first; the scanner clip is the action (MR2 Spyder: "more of the scanner clip").
2. **Real crew removing a part plays out**, then cuts 1:1 into the scan of that state on a beat (240SX front bumper). Let the
   real action run a little longer before the cut.
3. **The scan data in detail.** Use the scan reel rules: move in on the removed areas, show bumper inside and outside, then
   the crash beams. Include sections that have no footage when the scan exists ("Add a section showing the rear bumper
   removed data, even without IRL footage", C5). Show more scans: under-hood, Z06 engine bay and the rest (C5).
4. **Reassembly.** An x-ray reassembly works: the bumper translates onto the bumper-removed scan with no un-rotating (240SX).
5. **Store CTA:** the last scan frame lands 1:1 on the listing's cover photo, then zooms out to the mobile product page
   ("needs a better final cut into the product listing", MR2 SW20). The logo goes below, then the URL fades in last.
   See `temerario-scan-reel/references/endings.md`.

## Footage rules

- **Slow down wherever there is text (owner rule):** slow-mo, speed-ramp or hold the shot under any label so slow readers can finish it. Text stays fully readable for at least 1.8 s (1-3 words), plus 0.3 s per extra word, and 2.2 s or more for prices. Apply it to new work only; never re-cut a finished video just for this. See `knowledge/lessons.md`.
- Never put text over IRL footage.
- **Widen the IRL crops at the match cuts.** "IRL to CGI 1:1 crops are awfully close" (Sera). Zoom the real shots out so
  they're less cropped.
- **The 1:1 solve must match the interior, not only the outline.** A silhouette solve on a car cropped by the frame can be
  about 12° rolled. Onion the full-res frame with the render's interior edges, and fix it with landmark PnP
  (`projects/toyota-mr2-spyder-scan-process/tools/pnp_landmarks.py`). The scan camera angle must match too: "the scan
  camera angle is too low" (240SX). Method: `knowledge/match-cut.md`.
- **The IRL to scan transformation is a hard cut on a beat. The scan to finished-car reveal may crossfade** (Sera).
- **Use the right footage.**
  - Check the Dropbox video dumps, Camera Uploads and phone backups.
  - A team long-form edit may supply only the IRL shot that cuts 1:1 into the scan (NA Miata Grimace).
  - Don't keep reusing the IS350 footage.
  - Import clips that "look like colored blobs" read badly (Lola).
- **Don't show a part coming off unless it was physically removed on the car AND scanned in that state.** "we never pulled
  the EK bumper" (Civic scan process).
- **Film or partner reels:**
  - Clear them before posting (Lola: "production is fine with it").
  - Trailer shots can supply the 1:1 cut.
  - Drop the website URL and festival captions when asked.
- **Plates:** blur only on the IS300, or where the user asks in that reel's chat.

## Music

Use a real, trending or user-supplied track, never library or generated music. Don't reuse another reel's track. Start from
the song's beginning, or from the line the user names ("'my life be like' starts the song", Lola). Aim for -14 LUFS with
true peak below -1 dBFS. Let the final set's cuts breathe with the music instead of a rigid grid (240SX). Details:
`temerario-scan-reel/references/music-and-timing.md`.

## Steps

1. **Inputs.**
   - Footage: Dropbox `/2. Illumaesthetic Videos/1. Video dumps/<car>` and Camera Uploads.
   - Scans: the engineering Drive, per car, one STL per state. List every file.
   - Download per `knowledge/sources.md`.
2. **Understand.** Run `ive probe` and `ive sheet` on every clip, and `ive analyze` on every reference or approved edit.
   Find the music grid. Write `projects/<p>/clips.md`.
3. **Plan.** Run the `scene-director` agent, then lay a beat-gridded timeline in `projects/<p>/project.yaml` (copy
   `projects/_template`). Log each story decision with its reason.
4. **Scan.** Decimate, crop, then prep (`knowledge/scan-pipeline.md`). Cut panels per `temerario-scan-reel/references/scan-cutting.md`.
5. **Match cut.** Follow `knowledge/match-cut.md`: frame, reference render, landmarks, raycast, solve (PnP), check the interior
   onion.
6. **Shots.** Check framing at 30 % resolution, then queue finals in the background, one at a time (15 fps plus
   interpolation; native frame rate for swaps; true 60 fps only when asked).
7. **HUD.** `projects/<p>/overlay.json`, then `ive hud`. Labels are factual, from file names, with no counts.
8. **Assemble and review.** Run `ive assemble`. Inspect frames around every cut, and check cut sync and loudness on the
   decoded file. Score with `training/rubric.md`.
9. **Deliver and learn.** Share the file, record feedback with `ive feedback` (`--rule` for general rules), add lessons, run
   `ive archive`, refresh the graph (`/graphify --update`), commit and push.
