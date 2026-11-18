# BF 6/8 gr-corolla-track: draft v0 notes (2026-11-17)

The owner's instruction, relayed by the parent session: "have all the agents make a quick short first draft". The shot list's open questions are not answered yet, so this v0 uses my recommended default for each. Every assumption is listed below.

**Output:** `/home/user/media/work/out/bf-gr-corolla-track_v0.1.mp4` (v0.1 = v0 without characters) (1080x1920, 30 fps, about 17.6 s). Media is not in git.

## Assumptions (my defaults for the open questions)
1. **Footage:** the track is CGI. No real track or autocross clip of the V2 car exists in Dropbox.
   - The car is the lookbook GLB `eps-toyota-gr-corolla-v23` (V2 lip, skirts and spats on; V1, canards and wing hidden) on a simple procedural Blender circuit: asphalt, kerbs, armco, tyre walls, boards, gantries, trees, a grandstand and a gradient sky.
   - The car is static; the track moves under it at 33 m/s; the wheels spin; Cycles motion blur is on.
2. **Paint:** a plain Supersonic Red (#b21522, the earlier GR Corolla reel's colour). No Castrol livery, so there is no third-party branding. The V2 kit is matte black PU, which is how it ships unpainted.
3. **The 1:1 cuts:** CGI -> scan at 2.9 s (shot 2 -> 3) and on the lip macro at 5.7 s (shot 4 -> 5).
   - The scan is the engineering full car (`GR Corolla Full Car.stl`, Drive 17j3c0hlvYD1xm4WODOa_xH07Q_mD16WP), decimated to 3 mm and ICP-aligned into the GLB frame (tools/photo1to1 method, median 33 mm).
   - The kit on the scan is the lookbook's V2 parts in silver: the parts the configurator ships, not engineering's CAD, which is a different frame and is v12b's job.
4. **Captions:** on black cards between shots, never over driving footage.
   - Card 1: "BLACK FRIDAY / V2 KIT / 30% OFF". Card 2: "BLACK FRIDAY / V1 UP TO / 45% OFF".
   - Percentages only: no was/now prices, no stock, no dates. The sheet confirms both percentages (PRICES.md).
5. **No characters** (owner, 2026-11-17: no Del & Eps, just typical branding). v0.1 removes the Del & Eps cut-outs that v0 had tested on the cards. Two stills and two background removals had already been spent on Higgsfield (1d0476d2, dbee80da, aca49c87, 06c08bb5, 0.5 credits for the stills); nothing more will be spent.
6. **End card:** Epsilon+ wordmark (Drive `EPSILON+ Logos/Epsilon+ Logo.png`) 720 px wide, with "EPSILON.PLUS" under it.
7. **Music:** "Electric Youth" by Chris_record (TikTok CML, song_clip_id 7421090393491785729; claimed in MUSIC.md), from the song's beginning.
   - It measures as ~126.8 BPM with kicks from 0.07 s.
   - Cuts land on individually measured kick onsets (half-rise, 40-150 Hz): kicks 4, 6, 10, 12, 14, 18, 22, 26, 30.
   - The logo is on kick 30 (14.3 s) and holds to kick 36, followed by a 1 s fade.
   - The file is the TikTok CML full track (146 s). Attach the same sound in TikTok when posting.

## Preview quality (v0 only)
- Renders are 540x960 (50 %), 12 spp, denoised, then upscaled to 1080x1920.
- The circuit is deliberately simple and the sky is a flat gradient. The lesson that low-detail environments get rejected applies to v1.

## Not done in v0 (planned for v1 after notes)
- Full resolution and samples.
- A richer circuit (corners, run-off, crowd, a real sky).
- Was/now prices if the owner wants them.
- Engineering-CAD kit on the scan if the owner prefers it to the lookbook parts.

## v0.1 checks (2026-11-17)
- **File:** 1080x1920, 30 fps, 543 frames, 18.1 s.
- **Loudness:** -14.0 LUFS, true peak -2.8 dBFS (gain +2.2 dB, limiter at -1.4 dBFS).
- **Cut sync on the decoded audio:** 8 detected cuts are within -21..+7 ms of the measured kicks; 7 of 8 are within half a frame. The s1->s2 cut is a continuous move, so it isn't detected as a hard change.
- **Frames:** every render frame was checked for black or unlit frames (min mean luma per shot is fine). A 27-frame contact sheet around every cut was reviewed.
- **Known issues:**
  - The lip-macro 1:1 cut is about 5 cm off (global ICP, median 33 mm).
  - The scan has no captured rear wheels; it shows in the s3 pull-back.
  - The card kit layout sits left of centre.
  - The circuit is low detail.
  - s1 -> s2 is a same-car tracking cut and reads as a jump.

## v0.2 (user notes on v0.1: canards back in stock, highlight V2, game GLBs instead of scan)
- **File:** `/home/user/media/work/out/bf-gr-corolla-track_v0.2.mp4`, 1080x1920, 30 fps, 19.9 s. Loudness -14.0 LUFS, true peak -2.8 dBFS.
- **Cut sync:** 9 detected cuts within -21..+7 ms of the kicks (8 of 9 within half a frame). No dark frames.
- **No scan data:** the scan shots are now lookbook-GLB studio shots. The body goes graphite, the V2 parts glow in, and labels name each part.
- **Canards:** carbon canards are on the car in every CGI shot, plus a new close-up labelled "CARBON CANARDS / BACK IN STOCK".
  - The store still says "[BACKORDER]" with inventory -2; the listing needs updating before the ad runs.
  - No canard price is shown (canards are not in the BF sheet).

## v0.3 safe zones (owner rule, knowledge/safe-zones.md)
- `scripts/safezone_check.py`, v0.2 -> v0.3:
  - Labels moved out of the bottom zone (now y 1190-1320).
  - Card plates scaled to 0.79 so the spats end above y 1440; the card text is smaller and centred in the skirt gap.
  - Every 3D shot is lens-shifted 8 % left so the car clears the right rail.
  - The end-card logo and URL are centred at x 484, y 760 / 860.
- All text and logos now sit inside x 48-920 / y 285-1440.
- **Remaining:** in the wide CGI and studio frames the car's front corner still reaches the rail's left edge, and the lip macro fills the frame by design. There's no text there.
- File: `bf-gr-corolla-track_v0.3.mp4`, 19.9 s, -14.0 LUFS / -2.8 dBTP, same cut timing as v0.2.

## v0.5 (user notes + owner URL rule)
- **URL:** WWW.EPSILON.PLUS on the end card (v0.4).
- **Drive-past:** ends 2 kicks sooner.
- **Lip macro:** the camera is raised to about 0.6 m, looking down. The highlighted lip shot keeps the 1:1.
- **Offer cards (6 kicks each):**
  1. Graphite GLB car with the kit glowing in place, under a big "V2 KIT" / "V1".
  2. A red slash strikes through it.
  3. The body fades and the lip, one skirt and one spat lift into a 3/4 line-up as the camera moves in.
  4. "30% OFF" / "UP TO 45% OFF" punches in at 168 px.
  - The spat sits nearer the lens than true scale so it reads.
- **Checks:** 20.9 s, -13.9 LUFS / -2.8 dBTP; 9 cuts within -21..+7 ms of the kicks; the safe-zone sheet passes for all text and logos.

## v0.6 (user: slow readers, pairs; owner font rule)
- **Text hold times:** cards 8 kicks (the percent holds ~1.8 s); FRONT LIP held across s4+s5 (~1.8 s); SIDE SKIRTS / REAR SPATS ~1.4 s each; CARBON CANARDS / BACK IN STOCK ~2.5 s.
- **Pairs:** both skirts and both spats in the card line-up; the canards shot from the front so both show.
- **Fonts:** Unbounded 800-900 stands in for Akira (file not supplied); Unbounded 500 labels, 300 URL.
- **Checks:** 24.7 s, -13.9 LUFS / -2.8 dBTP, safe zones pass.

## v0.7 (Akira font, owner licence 2026-11-18)
- **Akira Expanded Super Bold** (Drive 1nrF80enolDd9HAu5807kv5XIx0cUSDya, SHA-256 checked, `assets/fonts/akira/` gitignored) is now used for BLACK FRIDAY, V2 KIT / V1, UP TO and 30% / 45% OFF.
  - Every string is checked against the font's cmap: no missing glyphs, no arrows.
- Labels stay Unbounded 500 / 400, and the URL beside the logo stays Unbounded 300.
- Composite-only change; no re-render.
- **Checks:** 24.7 s, -13.9 LUFS / -2.8 dBTP, safe zones pass, same cut timing as v0.6.
