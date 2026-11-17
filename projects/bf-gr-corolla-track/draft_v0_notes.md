# BF 6/8 gr-corolla-track: draft v0 notes (2026-11-17)

The owner's instruction, relayed by the parent session: "have all the agents make a quick short first draft". The shot list's open questions are not answered yet, so this v0 uses my recommended default for each. Every assumption is listed below.

**Output:** `/home/user/media/work/out/bf-gr-corolla-track_v0.mp4` (1080x1920, 30 fps, about 17.6 s). Media is not in git.

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
5. **Del & Eps:**
   - Two Higgsfield GPT Image 2.6 stills with `del-eps-model-sheet.jpg` as the reference (jobs 1d0476d2 and dbee80da), background removed (jobs aca49c87 and 06c08bb5), 0.5 credits for both stills plus the two background removals.
   - Eps stands on the V2 lip (card 1) pointing his scanner; Del stands on a V1 rear spat (card 2) with arms folded. A cyan sweep brings each in; no voices.
   - They are drawn larger than true 1:10 so they read on a phone.
   - **Model check:** Del matches the sheet (boxed beard, teal/orange, tape roll). Eps matches (backwards violet cap, visor with yellow eyes, scanner), but the still shows an open smiling mouth under the visor. The README implies no visible mouth, so this is flagged for the owner.
6. **No 10 mm end sting** in v0.
7. **End card:** Epsilon+ wordmark (Drive `EPSILON+ Logos/Epsilon+ Logo.png`) 720 px wide, with "EPSILON.PLUS" under it.
8. **Music:** "Electric Youth" by Chris_record (TikTok CML, song_clip_id 7421090393491785729; claimed in MUSIC.md), from the song's beginning.
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
- Character motion beyond the sweep and breathing hold.
- Was/now prices if the owner wants them.
- Engineering-CAD kit on the scan if the owner prefers it to the lookbook parts.
