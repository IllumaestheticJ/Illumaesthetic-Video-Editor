# Pip & Gus episode sessions: shared brief

You are producing ONE episode of the Illumaesthetic "Pip & Gus" explainer series (your episode is named in your session prompt).

This session belongs to that episode only.

**Repo:** IllumaestheticJ/Illumaesthetic-Video-Editor. Work from branch `claude/laughing-albattani-bav6u7` and develop on your own branch the branch named in your session prompt.

## Read first
- `CLAUDE.md` and everything it lists as mandatory: `knowledge/lessons.md`, `style-guide.md` and `workflow.md`. The lessons are standing owner rules and override everything.
- `projects/pip-gus-series/scripts.md`: the series format, the rules, YOUR episode's draft script, and the owner questions for it.
- The pilot that established the series: `projects/scan-tedium-explainer-reel/`.
  - `characters/design.md`: the locked character spec, which now includes no eyebrows (eye-shape expressions only) and Illumaesthetic nametags.
  - `feedback.jsonl` and `editlog.jsonl`: every owner note so far.
  - `tools/`: the Blender cel-shaded scene and rig (`partA_scene.py`, `partA_anim.py`, `nametag_tex.py`), the voice splitting tool (`el_split.py`), and the full-reel build (`full_build_v2.py --v3`).
  - `review.md`.

## Owner decisions that apply to every episode
- **Voices:** Higgsfield `elevenlabs_v4` in dialogue mode.
  - Pip: Kiki, preset voice_id `2d51d9d0-b2a4-5e8b-9c63-f310adafd5f7`.
  - Gus: Harrison, preset voice_id `573e5163-59b3-4926-aab1-951ef2985f81`.
  - Generate the whole dialogue in one call with emotion tags, and never speed it up.
  - Gus is matter-of-fact and only slightly annoyed (never angry or sad); Pip is curious, impatient, then excited.
  - Send the owner the voice take to approve BEFORE animating.
- **Look:** cel-shaded EEVEE world (Blender 5.3; run `scripts/setup.sh`; EEVEE needs `libegl1 libegl-mesa0 libgbm1`).
  - Dot eyes, no eyebrows, no arms, nametags, half marker-dot density.
  - Real footage stays photographic.
- **Structure:**
  - Cartoon part with word-by-word captions (Fjalla One; Pip in sage #619f73, Gus in #ecefec, dark plate).
  - Then real footage: aim for 4-5 s, longer only if it genuinely needs it.
  - Then the "HOW LONG / FULL VIDEO ON OUR CHANNEL"-style teaser card with a framed clip, then the Illumaesthetic logo card.
  - Adapt the teaser text to the episode, and ask the owner if unsure.
- **Music:** a curious, inquisitive generated bed, NOT game or battle music (ElevenLabs Music v2.5 via Higgsfield; the pilot's track is at the Higgsfield job referenced in the editlog).
- **Never:**
  - text over IRL footage;
  - invented numbers (anything marked [VERIFY] in the script needs the owner's confirmation);
  - a dissolve for a real-to-scan cut;
  - naming or mocking competitor brands.
- **Credits:** keep Higgsfield credit use minimal and say the cost before spending more than about 5 credits.
- **Media:** never commit media. Work in `/home/user/media/<project>/`; footage is in the owner's Dropbox (connector).

## Your first steps
1. Create the project folder `projects/pip-gus-ep<N>-<slug>/` from `projects/_template`.
2. Put the episode script in `script.md`, tightened to about 30-40 s.
3. Ask the owner the open [VERIFY] questions for your episode, all in one message.
4. Get the script approved before generating voices or rendering.

Log every decision with `python -m ive log`, and record feedback with `python -m ive feedback`. Commit and push to your branch. No pull request unless asked.

## Per-episode notes
- **Pip & Gus Ep 0 - Intro "Meet Pip & Gus" (official Illumaesthetic mascots)** (branch `claude/pip-gus-ep0-intro`): This is the series intro the owner asked for: Pip and Gus introduce themselves as the official Illumaesthetic mascots who will explain the ins and outs of 3D scanning/printing and what Illumaesthetic does. Owner questions pending: the line describing what Illumaesthetic does, and the end call-to-action. Ends on the logo card (no teaser card).
- **Pip & Gus Ep 1 - Why we spray windows/black cars (how white-light scanners work)** (branch `claude/pip-gus-ep1-spray-white-light`): Owner asked specifically to explain how white/structured-light scanners work (projected pattern, camera, triangulation) and why glass, chrome and black paint fail. Do not name the owner's scanner. Pairs with Ep 9 (AESUB).
- **Pip & Gus Ep 2 - "Can't you just 3D print the scan?"** (branch `claude/pip-gus-ep2-print-the-scan`): Owner approved this concept. Best scan-sales CTA (SCANS AVAILABLE AT ILLUMAESTHETIC.COM).
- **Pip & Gus Ep 3 - "Why can't I just print the bumper I want?" (custom design + print still costs more than buying)** (branch `claude/pip-gus-ep3-whole-bumper`): Owner approved, and asked that it explain why just printing a bumper is not cheap or worth it. Real "before" footage: Dropbox /2. Illumaesthetic Videos/1. Video dumps/Seamforged/Seamforged V1/ (bumper cut into many pieces across many plates in a slicer).
- **Pip & Gus Ep 4 - SeamForge (our app) and why it is useful** (branch `claude/pip-gus-ep4-seamforge`): SeamForge is the owner's own desktop app: repo IllumaestheticJ/SeamForge (add it with add_repo and read its README - the feature list in scripts.md comes from it; Print Layout/costing is currently hidden in the UI, do not promise it). Owner wrote "Seamforged" - ask which name goes on screen, availability/price, and for a screen capture.
- **Pip & Gus Ep 5 - Different ways to glue 3D prints together** (branch `claude/pip-gus-ep5-glue`): Owner topic. Keep claims general and qualitative; ask the owner which methods they actually use and recommend.
- **Pip & Gus Ep 6 - Big vs small printers: pros and cons** (branch `claude/pip-gus-ep6-printer-size`): Owner topic. No brands, no build volumes/prices/speeds unless the owner supplies them.
- **Pip & Gus Ep 7 - Which materials to use for car parts** (branch `claude/pip-gus-ep7-materials`): Owner topic. No temperatures on screen; ask the owner for the materials they stand behind.
- **Pip & Gus Ep 8 - NURBS vs mesh (STEP vs STL) and when to use them** (branch `claude/pip-gus-ep8-stl-vs-step`): Owner topic. Real footage idea: the mirror-package workflow (STL scan -> Class-A STEP -> deviation map); ask the owner which project may be shown.
- **Pip & Gus Ep 9 - AESUB vs AESUB alternatives (pros and cons)** (branch `claude/pip-gus-ep9-aesub`): Owner topic; AESUB may be named (owner asked), alternatives stay generic. Sourced facts are in scripts.md (AESUB datasheets/reviews); keep hours off screen unless the owner OKs. Pairs with Ep 1.
