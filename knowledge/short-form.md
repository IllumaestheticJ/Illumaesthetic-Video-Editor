# Short-form "build story" reels (press / customer builds)

For reels whose point is **what we built and how** (SEMA cars, customer kits), not a pure scan showcase.
Approved example: `projects/nissan-sentra-sema` v19 (47.5 s, 1080x1920, 30 fps; v6 structure approved, v12-v19 polish). Read its
`feedback.jsonl` before starting.

## Ask first (one message, before building)
1. The **hook**: which post/article/controversy opens the video.
2. The **music** and where the reveal should land (default: the first hard drop).
3. Credits: who the client is and which brands may be shown.
4. Which logos close the video: our wordmark + partner marks (get each partner's official file; white versions on black).
5. Screen recordings of social posts (Instagram cannot be captured from here) and any in-progress photos.
6. Every part that was physically REPLACED vs added (Sentra: front bumper + rear diffuser replaced; brakes upgraded), and where
   the designer's files for brakes/ducts/reprints live - they are often outside the body-kit folder.

## Structure (bars counted back from the drop)
| Beat | Length | Content | Notes |
|---|---|---|---|
| Hook | ~2 bars | one real post/article, full frame | still frame of the screen recording, 3 % push |
| Answer card | 1 bar | 2-3 words on near-black ("IT WASN'T.") | brush font (Permanent Marker) ~185 px, key word in brand green |
| Scan day | 3 bars | spray timelapse, scanner in hand, timelapse ending on the solved frame | process order only - no finished-car shots here |
| 3D scan | 1 bar | **1:1 cut** from the last timelapse frame; label `3D SCAN` + triangle count from the STL header | `match/cam.json` |
| Concepts | 2 bars | 32 design renders, chronological (CAD -> renders -> livery studies), **one per 16th note** (BAR/16), label `CONCEPTS` | drop any with app UI chrome |
| Swap + panels + livery | 4 bars | each REPLACED part comes OFF first (bumper, diffuser), then new parts on: bumper, duct corners, vents, sides; stock wheels off -> brakes (rotors, then calipers) -> wheels; diffuser, wing; paint wipe, stripes | real 30 fps; labels `OLD BUMPER OFF`, `NEW BODY PANELS`, `LIVERY` |
| Final render 360 | 3 bars | full lap, then ease into the solved camera of the reveal photo and hold through the riser | `match/cam_reveal.json` |
| **Reveal** | ~3 s | **1:1 cut to the real car on the drop**; cropped real headlines land one per **base beat** (BAR/4) from the drop, staggered left/right | car stays clear in the middle |
| Other people's clips | ~11 s | cut in on a base beat ~3 s after the drop; 4 clips, whole car in frame | they are the payoff - give them the time |
| End card | ~3 s | Illumaesthetic wordmark / partner marks stacked, centred, equal gaps between visible ink, stack centred | partners fade in after; fade music |

## How (tools in `projects/nissan-sentra-sema/tools/`)
- `kicks.py` - kick onsets of a track window; map the track with 2 s energy rows first to find the drop.
- `capture.js` - phone-width screenshots of articles (hosts must be allowed); crop headline blocks, tag the outlet in type.
- `ron2car.py`, `kit2lvl.py` - designer CAD into the scan frame via the designer .blend's stored scan matrix.
- `bumper_off.py`, `diffuser_off.py` - cut a replaced stock part out of the base scan (state-scan diff, or the new part's envelope)
  so it can be keyed OFF before the new part lands.
- `brakes_in.py` (Blender: big OBJ -> per-object triangles) + `brakes_place.py` - a part set in its own frame, seated per corner
  on the measured wheel centres, left mirrored. Split L/R so each side slides in from its own side.
- `ive fetch-drive <id> <dir>` - a folder id lists its files with ids (shared links are usually folders).
- `shot.py` - keyed camera (solved-camera keys), part visibility windows, `frames` (re-render only those), `livery` (vertex-colour
  paint + wipe + stripes; groups car/kit/black/wheel/caliper/rotor; front lip/inlet rules),
  `raycast` (photo pixel -> 3D point on car/kit/wheels through a solved camera).
- `build_v6.py` - exact-frame segments from PIL/ffmpeg, concat, music; `CUT` table = bars relative to the drop.
- `grid.py` - gridded crops for landmark picking.

## Checks before sending
- Onion overlay for BOTH 1:1 cuts (scan-day frame -> scan, final render -> reveal photo). For the photo: focal fixed from EXIF,
  a far-side landmark, and the last delivered video frame compared with the photo.
- Livery measured through the reveal camera; side/front/rear check renders next to photos.
- Every render folder: frame count and per-frame luma.
- Every borrowed clip: 6 frames across its window - whole car visible, no play button.
- Before every long render queue: 2-4 check stills of the changed areas (front, rear, a wheel through the spokes).
- Say plainly what was not measured (cut-to-beat error on the delivered file was never measured on the Sentra reel).

## Text style
Colours from the website: off-white `#f2f3f1`, one key word in green `#619f73`, `#0b0c0b` cards. Typeface (user, Sentra v10): **Helvetica Bold**
for labels, blurbs and tags (the user's Helvetica-Bold.ttf upload is in `/home/user/media/sentra-sema/fonts/` - ask for it again in a
new session; media is not committed), a brush font (Permanent Marker) for the one punch-line card.
`build_v6.py`: `FJ`, `MONO`, `BRUSH`, `label`, `section_label`, `spaced`. A blurb over footage sits on a semi-transparent panel, never a solid box.

## Livery (Sentra show car, the reference for "match the real car")
White body, black roof/pillars/mirrors, black skirts with a red line, red side stripes (raycast-measured), black front lip with a
red trim on its lower edge, black trapezoid radiator inlet, black corner-intake fins, black diffuser, copper-orange calipers. When
the concepts and the built car differ, match the built car.

## Captions (user-approved tone)
Professional, no "AI" mention: lead with the standard ("When the work is good enough that people question whether it's real,
that's the standard we build to."), one paragraph of the actual process (scan -> design -> 3D -> print/fit, named parts), credits
(@partners - verify handles), a soft call to action. Never invent specs.
