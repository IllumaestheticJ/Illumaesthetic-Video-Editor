---
name: temerario-scan-reel
description: Build an Illumaesthetic / Epsilon "Temerario-style" scan-only reel - a 9:16 video made only from a car's 3D scan data (no shop footage), silver on black, where the car is taken apart section by section (hood, bumpers, lights, wing, skirts, exhaust, underbody), removed parts are shown alone with their sub-parts exploded, everything flies home on the music and the logo or store CTA closes. Use this whenever the user asks for a Temerario-style video, a scan-only reel, a teardown / exploded-view / "parts coming off" video of a scanned car, an Epsilon kit install on a scan, names a car plus "scan reel", or gives feedback on one of these reels (parts clipping, parts off screen, wrong cut lines, leftover or missing scan, hallucinated parts, wheels cut flat, music too loud, wrong part of the song, logo too small, add a section) - even if they do not say "Temerario".
---

# Temerario-style scan reel

Updated 2026-11-17 from all 754 reviewer notes across the scan reels, plus `knowledge/lessons.md`.
`knowledge/lessons.md` and the car's own `feedback.jsonl` override this file. `CLAUDE.md`'s mandatory reading still
applies. Before planning, query the knowledge graph from the repo root:
`graphify query "<car> <section> lessons"`. Read the car's digest in `knowledge/feedback/<project>.md`.

**References in this skill:**
- `references/reviewer-rules.md`: every rule, with the user's words. Read it once in full.
- `references/scan-cutting.md`: how to cut, nest and register scans so the cuts pass.
- `references/music-and-timing.md`: choosing the track, finding the grid, checking the cuts.
- `references/endings.md`: logo size, the mobile store CTA, Epsilon and partner endings.
- `references/comparison.md`: Revuelto v5 against the other reels.

**Approved examples to imitate:**
- `projects/lamborghini-revuelto/` v5 ("this is perfect for the temerario style videos"): `shots_v4.py`, `project.yaml`, `overlay.json`.
- For short revisions, `projects/subaru-gd-trio/` v2 and `projects/mazda-miata-na/` v5 (about 20 s).
- For kit installs, `projects/toyota-gr-corolla/` v12 and `projects/honda-civic-11/` v5.

## The five things the user rejects most

1. **Hallucinated or wrongly cut scan.** Parts that weren't scanned are moved anyway, panels are cut along made-up lines,
   cuts take the neighbours with them, leftovers stay on the car, or a moving part is missing a chunk.
   Fix: every part comes from a part scan or a state scan, and every cut follows the real shut line (`scan-cutting.md`).
2. **Wrong order.** Children leave before their parent, or a panel comes off without hinging open first. Hood first,
   then bumper; doors and lids only open unless they were really removed.
3. **Bad motion.** Parts clip through each other, go off screen, or park in front of the next subject. The camera cuts
   away before the exposed data is seen.
4. **Slow.** Long holds, filler cutaways, turntables, a slow intro. Revised reels settle at about 20-25 s. Length follows
   content.
5. **Weak ending and audio.** A small logo, a text-only CTA, generated music, a loud master, a song started mid-way.

## Workflow

1. **Inventory every scan.**
   - List the car's whole Drive folder, including sub-folders such as "Underbody" and "Scan Analysis".
   - Search the engineering drive by name and spelling variants, and check the 3D artist's `Projects_` folder.
   - Write `clips.md` with one row per file: full car (which version), state scans ("Bumper Removed", "Hood Open",
     "Trunk Open", "Rear Wing Removed", "No Exhaust"...), part scans and sub-part scans.
   - Mark duplicates (the same part scanned twice) and wrong versions (facelift vs pre-facelift, V1 vs V2 kit).
   - Render every state scan alone, and drop the ragged ones.
   - The file and state names are the only source for label text.
2. **Register.** Level once, prep with `--like <full car>.json`, and solve one shared offset per second scanning session
   (`scripts/xform.py`). Tint-check every part over the car.
3. **Cut.** Cut each removable panel on its traced shut line, with no leftovers and nothing taken from the neighbours.
   Make each moving part complete, and limit each state fill to its own opening. Check three stills side by side before
   any render (`scan-cutting.md`).
4. **Music.** Get the user's track or a real one (`music-and-timing.md`). Find the true grid, and lay sections on whole bars
   or kicks.
5. **Direct.** Run the `scene-director` agent (`.claude/agents/scene-director.md`): it sets the scene order from this car's
   scan features. Then run `python -m ive director` to remove repeated views. Write the shot list as code, copying
   `projects/lamborghini-revuelto/shots_v4.py`: cut frames per shot, parked poses, keys in bars, and `parents` for nested
   parts.
6. **Preview** every shot at 30 % (`scripts/preview5.sh`). Render one final-quality still per new lighting setup; small
   lone parts and cabins need exposure around -1.8. Then queue the finals one at a time (`scripts/render_queue2.sh`,
   resumable, at most about 2 h per job).
   - Render at 75 % resolution, 12 spp, 15 fps, then minterpolate to 30.
   - Shots with a state swap or a fast part move render at native 30 fps.
   - "60 fps" means true 60 fps renders.
   - Check free disk before queueing. After any disk-full event, PIL-load every frame.
7. **Check** (below), then render the HUD. Assemble with exact frame counts (`projects/honda-s2000/tools/concat_assemble.py`)
   and run `scripts/verify_delivery.py`.
8. **Deliver.** Self-score into `review.md`, record feedback with `ive feedback` (`--rule` when general), archive, commit,
   push and send the mp4. The project's knowledge goes in `knowledge/lessons.md`; then run `/graphify --update`.

## Story template (adapt it to what was scanned; never fill gaps with fakes)

1. **Whole car**, fully in frame and moving from frame 1. About one bar, with the hook early.
2. **Front:** hood hinges open (and comes off if asked), then the bumper comes off. The camera moves in on what the bumper hid
   (crash beam, mounts) with a label. Then the bumper alone: inner face, outer face, and its scanned sub-parts separate
   along their mounting direction.
3. **Side:** mirrors, skirts, flares and fender, each with a beat, a label, and a hold on the removed-state scan.
4. **Rear:** trunk hinges open; lights come out sideways; the bumper goes straight back, then up; the exhaust follows as 1:1
   state swaps with the surround kept; then the wing and diffuser. Finish with the rear bumper alone and its sub-parts.
5. **Underbody, interior, suspension or wheel houses** when they exist. Shoot the underbody from below with an under-light,
   and move removed parts fully out of the way first.
6. **Short exploded view** with everything out at once, from 2-3 angles. This closes the inventory.
7. **Reassembly,** with kit or aftermarket parts going on here after the parts they replace come off. Everything locks on a
   strong downbeat.
8. **Ending** per `references/endings.md`: the store CTA 1:1 on the listing cover photo, or the Epsilon or partner end card.
   The logo is about 720 px.

## Hard rules (short form; reasons and sources are in `reviewer-rules.md`)

- Only real scan data. Use no carved stand-ins, triangle counts or invented numbers, and add no section the user didn't ask for.
- Cut on the traced shut lines. A removed part takes only its own skin and all of it; it comes off whole, and what was
  under it stays.
- Children wait for their parent. Hinged panels open first. Two files of one part make one part.
- No clipping, which you check numerically (`pathcheck.py`, `projects/porsche-gt3rs-992/tools/clipcheck.py`). Nothing goes
  off screen, and parts move into clear background.
- Hold on every exposed state, side included. Use no filler cutaways and no turntables, except a requested 360.
- No jump cuts: change the angle a lot, or continue the previous camera key exactly.
- **Slow down wherever there is text (owner rule):** slow-mo, speed-ramp or hold the shot under any label so slow readers can finish it. Text stays fully readable for at least 2.5 s (1-3 words), plus 0.4 s per extra word, and 3 s or more for prices. See `knowledge/lessons.md`.
- Every scanned part gets a beat and a short factual label, placed over scan shots only and in clear black (or on a plate).
- Use real music, started from its beginning, at -14 LUFS with true peak below -1 dBFS. Every cut lands on a measured hit,
  verified on the decoded mp4.
- Plates stay, except on the IS300 or when asked in that reel's chat.

## Checks before sending (on the real files)

```
python scripts/lumacheck.py <renders>/<shot>*            # dropouts / dark frames
python scripts/edge_margins.py <renders>/<shot> ...      # nothing reaches the frame edge (every frame, parked parts too)
python scripts/pathcheck.py <shots>/<shot>.json          # parts do not pass through each other
python scripts/verify_delivery.py out.mp4 --cuts 103,206,... --lock <frame>   # cut sync, loudness, frames
```

Then look at the delivered file:
- a contact sheet at every label and every cut;
- the first, middle and last frame of every shot;
- full-size frames of each parked pose;
- a close-up of every cut seam and every tyre;
- frame diffs at the cuts, to catch jump cuts.

Write each new check image to a new timestamped filename, because the image viewer caches by path. After any re-time,
re-check the whole reel.

## Working habits that saved time

- Keep `project_vN.yaml`, `overlay_vN.json` and `review_vN.md` for every version. A music swap on the same grid reuses the
  renders.
- If a note is ambiguous, take the reading that is cheapest to reverse, say which one you took, and offer the other.
  If a request names scans ambiguously, list the candidates and ask.
- Save user-supplied files (logos, tracks) to Drive, Dropbox or the repo's asset notes: another session's container is gone.
- Background waiters count their time limit from launch. Launch each batch when the previous one reports.
- `training/examples/INDEX.md` and `knowledge/lessons.md` conflict on almost every rebase: keep both sides, then dedupe.
