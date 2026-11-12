# S3 - "Scanning a Smart car down to its skeleton" - production brief

Greenlit by the owner 2026-11-12. Pitch with shot list: `pitches/2026-11-12-pitch-slate.md` (S3).
Deliverable: 9:16 reel, 1080x1920, 30 fps, about 25 s. Illumaesthetic logo card on the last downbeat.

## Media
- Footage: `/home/user/media/smart-hellkitten/dropbox/v_HHMM_SS.mov` (15 clips shot 2026-07-26; the name is the clock time
  of the Dropbox file "Video Jul 26 2026, H MM SS PM.mov"). Mix of iPhone 1080p HEVC HLG and glasses-POV 3:4 SDR clips.
  Survey notes: `/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/82ade9fc-974d-5f22-af68-15eda8fddd9b/scratchpad/survey/C_epsilon_plus.md` section 6.
- Scans, Drive folder "Smart Car (450 Series)" (1WjFb82zLPNRn4e8pLVxsSQBe4uLDprWE; STLs in 1_HE3Fj-vxAUVxAirIT3GfU3-C_X2Md_J):
  `450 Smart Car Full Car Assembled.stl` (13SMMSlz0UkwN2_uWukWAtbu7rBOgFeGZ, 1.5 GB),
  `450 Smart Car Fully Stripped.stl` (1P3BwCfYSTm8DjaaG3PYsc9Oqeh96Nj2J, 1.5 GB),
  `450 Smart Car Clam and Trunk Mounting.stl` (1sBc9cAZFVX_mrSraO87yVN-tbDJ8RKDl, 1.0 GB),
  `450 Smart Car Door Card Top Edge.stl` (1OfND8I1IPCTqp2Q58oD3jOQ1DDKUIZR6, 0.75 GB).
- Design model, Drive folder "Smart Hellcat" (1wDvirPDOZtlTEvG0f31H7VdnKhCd-L9g): `SmartHellkitten.blend`
  (1Q8wICrdHPKAFr3LCjF_1UR-VfaV7Y8Wp, 73 MB), `SmartHellkitten.fbx`, reference images `hellkitten1.png`, `hellkitten2.png`,
  `Hellkitten2.3.png` (folder 1knPBj7cXK4sSD05HR5n_sCKf6m3Hp2MO). Look at these to learn what "Hellkitten" is before using the name.
- Work dir: `/home/user/media/work/smart-450/`. Media is never committed.

## House rules that bind every agent (full list: CLAUDE.md, knowledge/lessons.md, knowledge/style-guide.md)
- No text over IRL footage. Text only on scan shots; max two items; only numbers read from the data (STL header counts).
- IRL -> scan is a hard 1:1 cut on a beat. Hook in the first 2 s. Cut on the music's accents.
- Panels come off in the scan only via the real state scans (Assembled -> Stripped); never fake a removal.
- Each section of the car appears in one continuous sequence; no camera rotations that show nothing new; never reuse a shot.
- Scan look: satin silver on pure black, no ground, plates flattened. HLG footage tonemapped to SDR.
- Music must not repeat a track used by any earlier project (check projects/*/project.yaml and editlogs).
- Blender renders: Cycles CPU, one render job at a time on this box, in the background.
- Log every decision with its reason: `python -m ive log projects/smart-450-hellkitten "<what>" --why "<why>"`.
- Look at your own output before reporting it good. Report failures and gaps plainly.
