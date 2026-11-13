# Self-review - Sentra SEMA 30 s v1 (2026-11-12)
Looked at: 1 fps sheet of the whole cut, frames 268-382 around the 1:1 cut, per-segment check sheet, per-frame luma of the scan render (26.5-35, no dropout).
- 1:1 cut (frame 270): car position/size match on the sheet; solve was 4.4 px RMSE ("rough"), onion checked by eye. OK for v1, refine points for v2.
- NOT measured: cut-to-kick error on the delivered file (cuts were placed on onsets measured from the source track only).
- Headline cards are typographic stand-ins (hosts blocked); wall repeats the same 12 headlines.
- Scan car is small in frame (matched to an ultra-wide source frame); kit parts are white on silver, stock grille visible in the bumper opening.
- Print step = two low-res WhatsApp stills on blurred fill; g1 reveal is a still, not a 1:1 from the CAD render.
- SEMA clips are handheld with passers-by (g4_side has a person crossing).
- minterpolate on the part fly-ins not inspected frame by frame.

# Self-review - 30 s v2 (2026-11-13)
Looked at: 1 fps sheet, frames 269-485 (1:1 cut, panels, paint wipe, stripes), per-segment sheets, luma of s2_livery (26.5-33.4, no dropout).
- Not measured: cut-to-kick error on the delivered file; minterpolate on the part fly-ins not checked frame by frame.
- First frames of the panel shot: the front bumper flies in from 0.7 m ahead and is clipped by the left frame edge for a few frames.
- 3D stripes are placed by eye (position rules), not from the stripe DXF; no red splitter line, wing or intercooler in the 3D livery.
- topgear_ph screenshot shows broken image placeholders under the headline (image CDN blocked).
- Stock grille still visible inside the kit bumper opening before the paint wipe.

# Self-review - 30 s v4 (2026-11-13)
Looked at: 1 fps sheet, 9 frames across the 3D shot (384-494), side/front/rear livery check renders against the Nov 12 photos, segment sheets.
- Not measured: cut-to-kick error on the delivered file; interpolated part fly-ins not checked frame by frame (first frames of the 3D shot show
  the bumper entering at the left edge).
- Headline stack fills the full height: the first outlet tag sits close to the top edge (platform UI may cover it).
- 3D livery is rule-based: no intercooler, orange calipers, badges or number plate; wheels are the stock scanned wheels, not the Nismo wheels.
- Photo stills are 1080x810 bands on blurred fill (whole photo, static) - small in a 9:16 frame by request.
- Closing reels keep the Instagram UI (account names visible); three clips, 38/30/45 frames.

# Self-review - 30 s v5 (2026-11-13)
Looked at: 9 frames across the 3D shot (386-494), reel and end-card frames.
- 3D shot is 15 fps renders blended to 30 fps: in-between frames show ghosted doubles of the wheels/bumper while they fly in
  (mci interpolation smeared them instead). True 30 fps render queued as renders/s6_livery30.
- Black paint now renders dark charcoal (specular cut for dark colours); wheels are Ron's models in flat dark gunmetal, no orange calipers.
- End card: website logo + typed slogan; official slogan lockup not found.
- Not measured: cut-to-kick error on the delivered file.
