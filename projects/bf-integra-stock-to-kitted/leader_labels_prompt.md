Add tracked part callouts ("leaders") to the real-footage shots of your video. Match the style the owner approved in `projects/bf-integra-stock-to-kitted` (v0.13). The reference implementation is on branch `claude/video-editing-scan-data-8o0m8g`; pull first.

**What it looks like**
- Each kit part shown on the real car gets one label: its name in caps, e.g. FRONT LIP, SIDE SKIRTS, REAR SPATS, SPORT WING.
- Under the text is a white underline exactly as wide as the text.
- One straight white leader line runs from the end of the underline to a point on the part. The leader end follows the part as the car and camera move.
- **Do not draw a dot or arrowhead** at the end of the leader. It is just a line that ends on the part.
- **One leader per label**, even when a part comes in pairs (spats, skirts). Point at the clearer one.
- Lines and text are white, with a soft dark halo (blurred black, ~150 alpha) behind them so they read on a white car.
- Font: Unbounded 600, ~46 px, from `assets/fonts/unbounded/`. This follows the owner font rule in `knowledge/fonts.md`: Akira is for headlines and offers; labels use Unbounded.
- **Text placement:**
  - The text sits in clear space (sky, road, or the blurred fill band) and never over the part.
  - The leader must not cross its own text. Place the label so the part is beyond the underline's end.
  - Text stays inside the safe zone: x 48-920, y 285-1440, and out of the right rail (x > 920 at y 900-1440). Run `python scripts/safezone_check.py <mp4>` and look at the sheet.
- **No blur, darkening or highlight** on the footage. The owner rejected that look; the labels replace it.

**Animation (30 fps, local frame k of an n-frame shot)**
- **Leader:** grows from the part out to the underline end over frames 3-7.
- **Underline:** wipes in over frames 5-9. A left-aligned label wipes left to right, right-aligned right to left, centred from the middle.
- **Text:** fades in over frames 6-10.
- **Exit:** everything fades out over the last 5 frames of the shot, so nothing is cut while it is being read.
- **Reading time:** check the current text-timing rule in `knowledge/lessons.md`. It was last revised to 1.8 s for 1-3 words. Slow the shot (0.5x with ffmpeg `minterpolate=fps=60:mi_mode=mci,setpts=2*PTS,fps=30`) or use more of the clip if a label can't be read in time. Keep cuts on the beat.

**How the leader end tracks the part (no camera solve needed)**
- Code: `projects/bf-integra-stock-to-kitted/tools/track.py`, and `HL_PARTS` / `LABELS` / `label_tracks()` / `draw_labels()` in `projects/bf-integra-stock-to-kitted/tools/build_v0.py`. Copy them into your project's tools.
- **Step 1, place the polygon by hand.** On ONE key frame of each shot, outline the part with a polygon, using frame coordinates of the final 1080x1920 frame.
  - Read the edges from zoomed, gridded crops and from column brightness profiles; don't guess.
  - Pick a key frame where the part is large and clear. It can be the first or last frame, because tracking runs both ways.
- **Step 2, add the anchor.** Append the leader's end point (a point on the part's visible surface) as an extra vertex of that polygon.
- **Step 3, track it.** Carry the polygon to every frame with `track_poly`: LK optical flow plus RANSAC homography on features in a box around the part.
  - For a part that stands clear of the body (a wing above the trunk), use `track_anchor` instead. It fits a similarity transform to a rigid, textured region next to it (trunk with emblem, plate and lamps), so background parallax can't drag it.
  - The tracked last vertex is the leader end for that frame.
- **Step 4, check it.** Look at frames at the start, middle and end of each shot with the labels drawn. The leader end must stay on the part. If it drifts, fix the key polygon or the tracking region; don't hand-nudge frames.

**Process**
- **Log decisions:** every decision goes in with a why, via `python -m ive log projects/<p> "<what>" --why "<why>"`.
- **Before you send:** look at your own output (contact sheet and frames around each cut) before sending.
- **Text over real footage:** the owner asked for these callouts on the real footage. This is an approved exception to "no text over IRL footage" for part callouts only. No other text goes on the footage.
- **Deliver:** re-export as the next version, run the safe-zone check, send the video and sheet in chat, then commit and push. Never commit media.
