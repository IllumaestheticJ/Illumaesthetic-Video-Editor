# bf-paint-match-roulette: draft v0 notes (2026-11-17)

The owner said "have all the agents make a quick short first draft" (relayed by the parent session). v0 is a **preview-quality**
draft of `shotlist.md`. Output: `/home/user/media/work/out/bf-paint-match-roulette_v0.mp4` (1080x1920, 30 fps, about 23.3 s; media is not committed).
Tools: `tools/render_v0.py` (Blender stills), `tools/compose_v0.py` (assembly + text), `tools/probe.py`.

## Assumptions (my defaults for the open questions; please correct any of them)

1. **Wings:** all three wings are in the video (FL hatch + FE sedan + Integra), with every store colour for each wing.
2. **Hook car is the FE sedan, not the FL hatch.** This is a change from the shot list. The silver scan is the wing configurator's
   decimated FE scan (`ewc-honda-civic-sedan-fe-r3.glb`, a real scan at 30k faces). The engineering full-car scans weren't downloaded
   for a quick draft. The only hatch scan on the configurator is an FL5 Type R wearing its factory wing, so it can't carry the Sport Wing.
   The lookbook Sport Wing sits on the scan in silver. For the 1:1 cut, the scan is aligned to the lookbook body by plan-view PCA
   heading (0.7°) and bbox centre, not by ICP. The cut is approximate, and the onion overlay is close but not exact.
3. **Prices on screen** come from the BF liquidation sheet (PRICES.md, rev 25 snapshot), with the old price struck through:
   Civic base ~~$450~~ $315, Civic paint-matched ~~$850~~ $715, Integra base ~~$500~~ $350, Integra paint-matched ~~$950~~ $800
   (shown only on Double Apex Blue, a $950 colour). The end card says "FROM $315". No stock counts, no dates.
4. **"Each on its car":** Boost Blue, Championship White and Rallye Red FL are the real FL5 Type R listing photos. The other FL colours are
   rendered on the lookbook FL2 hatch. FE and Integra colours are on their own lookbook cars. FE ends on the real red FE photo
   (DILL7196). Sonic Gray Pearl appears twice (once for the FE wash, once in the FL run), because it's on both store lists.
5. **Del & Eps:** these are **placeholders cut from the committed model sheet** (`knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`),
   not new Higgsfield generations. I kept spend at zero, so the frames are labelled "DRAFT v0 - placeholder". They stand static on the
   silver scan in shots 1 and 37 only (house rule: characters are the only colour in frame; the roulette has no characters).
   The "hand on the wing", the scanner sweep and the 10 mm gag are not animated in v0.
6. **Paint wash** (shot 3): a 0.6 s wipe from gloss black to Sonic Gray Pearl across the wing, travelling right to left from where Eps stands.
7. **Pace:** the FE and Integra spins use half-beat cuts (about 6-7 frames). The measured flux grid has a transient on every 8th note.
8. **No text over photos:** the photo shots carry no colour names (the band option, Q9, isn't used in v0).
9. **Music:** GT2 "Arcade Mode Theme" (Dropbox /Moosic, assigned in MUSIC.md), from 0 s, with a 0.6 s fade at the end. Grid:
   140 BPM, first beat 0.0703 s (flux autocorrelation + phase fit). Loudness: -14.0 LUFS, peak -3.5 dBFS.
10. **Logo:** the epsilon.plus site header wordmark (`Epsilon_banner_black...png`, inverted to white, 720 px), standing in for the Drive
    `EPSILON+ Logos/Epsilon+ Logo.png`.
11. **Integra body:** the DE5 Type S lookbook model (v19), with its duckbill part hidden.
12. **Kit parts hidden:** the lookbook front lip, skirts and rear lip are hidden on the Civics, so the wing is the only Epsilon part in frame.

## Preview-quality shortcuts (to fix for v1)
- 540x960 Cycles stills (16 samples, denoised), upscaled 2x. Motion is a 2-6 % digital push-in, not a camera move.
- Lighting/paint is a quick studio rig. Pearl/metallic is approximated with Principled metallic + coat.
- No Remotion: text is drawn with PIL in Inter Display.
- The scan is the configurator's decimated scan, not the engineering full-car scan.
