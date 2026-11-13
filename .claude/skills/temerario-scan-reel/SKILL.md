---
name: temerario-scan-reel
description: Build an Illumaesthetic / Epsilon "Temerario-style" scan-only reel - a 9:16 video made only from a car's 3D scan data (no shop footage), silver on black, where the car is taken apart section by section (bumpers, lights, wing, skirts, exhaust), removed parts are shown alone with their sub-parts exploded, everything flies home on the music and the logo closes. Use this whenever the user asks for a Temerario-style video, a scan-only reel, a teardown / exploded-view / "parts coming off" video of a scanned car, names a car plus "scan reel", or gives feedback on one of these reels (parts clipping, parts off screen, wheels cut flat, music too loud, wrong part of the song, add a section) - even if they do not say "Temerario".
---

# Temerario-style scan reel

The approved reference is `projects/lamborghini-revuelto/` v5 ("this is perfect for the temerario style videos").
Imitate its files before inventing anything: `project.yaml`, `shots_v4.py` (shot list as code), `overlay.json`,
`direction.md`, `review.md`, `feedback.jsonl`. How it compares with the A90 Supra and the other reels, and what the
reviewer has asked for across all of them, is in `references/comparison.md` - read it before planning.

This skill adds to `CLAUDE.md` and the `scan-video-edit` skill; it does not replace the mandatory reading list
(`knowledge/lessons.md` first - reviewer rules there override this file).

## What the format is

One car, only its own scan data, rendered in Blender in the house silver on black. The story is the real job, in the
order a technician would do it:

1. **Whole car** under the song's opening (two bars), slow push.
2. **Front**: bumper and headlights come off, lid opens -> close shot of the structure they exposed.
3. **Front bumper alone**: inner face, outer face, then its scanned sub-parts separate (fog lights, radar, trims).
4. **Side**: skirts, fin, fender.
5. **Rear wing**: wide shot of it lifting off -> close shot of the wing-removed state scan.
6. **Rear**: tail lights out sideways, bumper straight back then up.
7. **Exhaust** (when scanned): tips -> catback -> cats -> bare bay, as 1:1 state swaps, inside the car.
8. **Rear bumper alone** + its sub-parts.
9. **Reassembly**: everything flies home and locks on a strong downbeat; hero push; fade.
10. **Logo** (about 720 px wide) on a downbeat, audio fades with it.

Only show an opening or removal that has scan data behind it. A section with no scan is left out, not faked.
About 35-45 s; every shot is a whole number of bars.

## Workflow

1. **Inventory the scans** (Drive folder for the car): full car, state scans ("Front Bumper Removed", "Rear Wing
   Removed", "Engine Bay Exhaust On / Cats On / No Exhaust" ...), part scans, sub-part scans. Write `clips.md`.
   The state and part names in the file names are the only source for label text.
2. **Register everything to the full car.** Level once, clean, prep every scan with
   `--like <full car>.json` so parts stay registered. Scans from a second scanning session (typically the exhaust
   set) share ONE offset: solve it once by ICP of one state against the nearest first-session state and apply the
   same transform to all (`scripts/xform.py`). Per-part ICP of pipes against a car is unreliable.
   Tint-check every part over the car before animating it.
3. **Music first.** Use the track the user supplied, **from its beginning** unless told otherwise. Find the bar
   grid (kick attacks in the 40-120 Hz band), then lay the sections above onto whole bars. If a splice is needed,
   cut on a downbeat with a ~20 ms crossfade. Turn the music down, never up: target about **-14 LUFS, true peak
   below -1 dBFS** (a hot master passed straight through clipped at +2.8 dBFS after the AAC encode and the
   reviewer heard it as "way too loud and blown out").
4. **Direct** with the `scene-director` agent, then write the shot list as code (copy `shots_v4.py`): one table of
   cut frames per shot, one table of parked poses, cameras and keys expressed in bars so a re-time is one edit.
5. **Preview every shot** at 30 % (`scripts/preview5.sh`), fix, then queue finals one at a time
   (`scripts/render_queue2.sh`, resumable). 75 % res, 12 spp, 15 fps + minterpolate to 30; shots that contain a
   state swap render at native 30 fps because interpolation ghosts the swap frame.
6. **Check the renders** (next section), render the HUD, assemble with exact frame counts
   (`projects/honda-s2000/tools/concat_assemble.py`), then run `scripts/verify_delivery.py` on the mp4.
7. Review, feedback, archive, commit, push, send the mp4 - as in `CLAUDE.md`.

## Rules that came from reviewer notes

Each of these was a correction on a delivered version; the reason matters more than the wording.

- **Parts leave the way they unbolt, and never pass through a neighbour.** ("the bumper clips with the tail lights
  and rear wing") Give each mover a via key that clears its neighbours first: bumpers slide along the car's axis,
  then rise; lights go out sideways before the bumper moves. Run `scripts/pathcheck.py <shot.json>`; ignore
  contact within 10 cm of home (parts touch where they seat).
- **Every part stays on screen while it comes off.** ("some parts are going off the screen") A removal is a WIDE
  shot whose parked poses are all inside the frame, then a hard cut to a CLOSE shot of what was exposed, where
  the removed parts are not loaded at all. Parked parts are fully in frame or fully absent, never half out.
  Measure with `scripts/edge_margins.py` over all frames - a 6-frame sheet passed a shot that touched the edge.
- **Never crop a state scan's sides to tidy ragged edges.** ("the exhaust scans need the surround scan to be more
  present, too much of it is cut off") Keep the scan's full width and seat it inside the car, with the car carved
  around it: `scripts/carve.py base.stl out.stl --ref state1.stl state2.stl ... --d 15 --box <leftover parts>`.
  The viewer needs the surrounding body to know where they are looking.
- **Removed assemblies get their own shot with sub-parts exploded.** ("exploded views of the individual parts
  removed from the front and rear bumpers") Show the bumper alone, turn it, then separate its scanned pieces along
  their mounting direction with a label below the pieces.
- **Wheels must be round.** ("the wheels are oddly cut flat") Ground removal that uses a plane fitted to the
  lowest geometry can pick the undertray. Cut by footprint + a fixed height below the tyre contact, and look at a
  tyre close-up before rendering.
- **State scans are shown as captured, swapped 1:1 on a beat** - no dissolve, no blending two states.
- **Labels**: short, one at a time, only over scan shots, in clear black away from moving parts, text only from
  file names and STL headers (triangle counts). Never invent a number.
- **Hold on what a removal exposed, for every section including the side.** (Miata ND: "the side skirt comes off
  and then immediately cuts away, its just a bad practice") The Revuelto's side shot is its weakest for this reason.
- **Every scanned part gets a beat and a name.** (GR86: "make sure all parts are highlighted") Where it helps, say
  what the scan is used for (Miata NC), not only what it is.
- **Sub-parts move only after their parent is off; hinged panels open before they come off.** (400Z, GR86)
- **No leftover skin or scan specks.** (A90: "scan artifacts must be cut out, and no parts may be left behind")
- **No turntables, no wheel close-ups, nothing shown twice.** (Miata NC, ND)
- **Length follows content.** 35-45 s was accepted when each second was a requested section; the older guidance is
  15-30 s and "move faster", so do not stretch holds to fill bars.
- **Look for underbody and interior scans** in the car's Drive folder; the A90 reviewer wants them in when they exist.
- **Number plate**: leave the scanned plate alone unless the lessons file names that car.

## Checks before sending (do all, on the real files)

```
python scripts/lumacheck.py <renders>/<shot>*            # dropouts / dark frames
python scripts/edge_margins.py <renders>/<shot> ...      # nothing reaches the frame edge
python scripts/pathcheck.py <shots>/<shot>.json          # parts do not pass through each other
python scripts/verify_delivery.py out.mp4 --cuts 103,206,... --lock <frame>
```

Then look: a contact sheet of the delivered file at every label and every cut, and full-size frames of each
parked pose. Numbers do not replace looking - and write every re-made check image to a new timestamped
filename, because the image viewer caches by path and will show you the old one.

Re-check the whole reel after any re-time: labels that cleared the parts at one length can collide at another.

## Working habits that saved time

- Keep every version's `project_vN.yaml`, `overlay_vN.json`, `review_vN.md`; a music swap on the same bar grid
  re-uses all renders.
- When the reviewer's note is ambiguous ("exhaust after the bumper"), pick the reading that needs no re-render to
  reverse, say which reading you took, and offer the swap.
- A background waiter that greps a log for a completion string must match what the tool really prints; otherwise
  it waits forever and the queue never starts.
- `training/examples/INDEX.md` and `knowledge/lessons.md` conflict on almost every rebase: keep both sides, then
  dedupe the project's INDEX line.
