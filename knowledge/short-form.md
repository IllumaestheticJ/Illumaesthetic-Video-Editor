# Short-form "build story" reels (press / customer builds)

For reels whose point is **what we built and how** (SEMA cars, customer kits), not a pure scan showcase.
Approved example: `projects/nissan-sentra-sema` v6 (47.5 s, 1080x1920, 30 fps). Read its `feedback.jsonl` before starting.

## Ask first (one message, before building)
1. The **hook**: which post/article/controversy opens the video.
2. The **music** and where the reveal should land (default: the first hard drop).
3. Credits: who the client is and which brands may be shown.
4. Which logo file closes the video (default: the website wordmark alone; never type a slogan under it).
5. Screen recordings of social posts (Instagram cannot be captured from here) and any in-progress photos.

## Structure (bars counted back from the drop)
| Beat | Length | Content | Notes |
|---|---|---|---|
| Hook | ~2 bars | one real post/article, full frame | still frame of the screen recording, 3 % push |
| Answer card | 1 bar | 2-3 words on near-black ("IT WASN'T.") | Fjalla One ~250 px, key word in brand green |
| Scan day | 3 bars | spray timelapse, scanner in hand, timelapse ending on the solved frame | process order only - no finished-car shots here |
| 3D scan | 1 bar | **1:1 cut** from the last timelapse frame; label `3D SCAN` + triangle count from the STL header | `match/cam.json` |
| Concepts | 2 bars | flipbook of the designer's iteration screenshots, ~4-5 frames each, label `CONCEPTS` | chronological |
| Swap + panels + livery | 4 bars | old bumper slides OFF (scanned structure shows), new bumper ON, ducts/sides/wheels, rear diffuser + wing, paint wipe, stripes | real 30 fps; labels `OLD BUMPER OFF`, `NEW BODY PANELS`, `LIVERY` |
| Final render 360 | 3 bars | full lap, then ease into the solved camera of the reveal photo and hold through the riser | `match/cam_reveal.json` |
| **Reveal** | 4 bars | **1:1 cut to the real car on the drop**; cropped real headlines land around it, one per beat from beat 2 | car stays clear in the middle |
| Other people's clips | 4 bars | 4 clips, whole car in frame, ~2 s each | no paused reels |
| End card | ~3 s | Illumaesthetic logo only (no typed slogan) | fade music |

## How (tools in `projects/nissan-sentra-sema/tools/`)
- `kicks.py` - kick onsets of a track window; map the track with 2 s energy rows first to find the drop.
- `capture.js` - phone-width screenshots of articles (hosts must be allowed); crop headline blocks, tag the outlet in type.
- `ron2car.py`, `kit2lvl.py` - designer CAD into the scan frame via the designer .blend's stored scan matrix.
- `shot.py` - keyed camera (solved-camera keys), part visibility windows, `livery` (vertex-colour paint + wipe + stripes),
  `raycast` (photo pixel -> 3D point on car/kit/wheels through a solved camera).
- `build_v6.py` - exact-frame segments from PIL/ffmpeg, concat, music; `CUT` table = bars relative to the drop.
- `grid.py` - gridded crops for landmark picking.

## Checks before sending
- Onion overlay for BOTH 1:1 cuts (scan-day frame -> scan, final render -> reveal photo). For the photo: focal fixed from EXIF,
  a far-side landmark, and the last delivered video frame compared with the photo.
- Livery measured through the reveal camera; side/front/rear check renders next to photos.
- Every render folder: frame count and per-frame luma.
- Every borrowed clip: 6 frames across its window - whole car visible, no play button.
- Say plainly what was not measured (cut-to-beat error on the delivered file was never measured on the Sentra reel).

## Text style
Website style everywhere: Fjalla One caps, off-white `#f2f3f1`, one key word in green `#619f73`, JetBrains Mono green kickers, `#0b0c0b` cards
(`build_v6.py`: `FJ`, `MONO`, `label`, `section_label`, `spaced`). A blurb over footage sits on a semi-transparent panel, never a solid box.
