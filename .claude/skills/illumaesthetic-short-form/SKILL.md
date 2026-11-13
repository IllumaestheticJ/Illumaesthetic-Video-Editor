---
name: illumaesthetic-short-form
description: Build an Illumaesthetic short-form "build story" reel (9:16, 30-60 s) for a customer or show car - press/controversy hook, scan day, 1:1 cut to the 3D scan, concepts flipbook, new panels and livery in 3D, a 360 of the final render that cuts 1:1 to the real car on the music drop with real headlines, other people's clips, official logo end card. Use for requests like "make a short form video of the <car> build", "show the process and the media attention", "SEMA build reel", or any reel that mixes shop footage, WhatsApp/in-progress photos, designer files, 3D scans and press coverage. For pure scan showcase reels use scan-video-edit instead.
---

# Illumaesthetic short-form build reel

Follow `CLAUDE.md` (mandatory reading), then `knowledge/short-form.md` - it holds the approved structure, the questions to ask
up front, the tool list and the pre-send checks. Worked example: `projects/nissan-sentra-sema/` (v6 approved).

1. **Ask once, up front** - hook post, music + reveal moment, client/credits, the official "Customize everything" logo file,
   social screen recordings. Carry on with everything that does not depend on the answers.
2. **Gather** - Dropbox dump (footage, WhatsApp export, screen recordings, in-progress photos), engineering Drive scans, the
   designer's folder (.blend with kit, wheels, wing; print STLs). Sheet everything; write `projects/<p>/clips.md`.
3. **Map the music** - find the drop, count bars back, write the cut table (see `tools/build_v6.py` `CUT`).
4. **Scan + design in one frame** - level/crop/prep the scan; bring the kit, wheels and wing in with `ron2car.py` / `kit2lvl.py`;
   fit-check in red over silver.
5. **Two camera solves** - scan-day frame -> scan, and a sharp photo of the finished car -> finished 3D car. Onion-check both.
6. **Livery by measurement** - raycast the photo's livery corners through the reveal camera; never eyeball.
7. **Render** - scan shot, panels + livery (parts pop on), 360 ending on the reveal camera. One queue script; check counts + luma.
8. **Coverage** - `capture.js` for articles (allow the hosts), cropped headlines one per beat; reels held ~2 s with the whole car.
9. **Assemble, look, send** - exact-frame segments, contact sheet, both cut frames; list what was not measured.
10. **Learn** - `ive feedback` every note (`--rule` when general), update `knowledge/short-form.md` when the user changes the
    structure, `ive archive`, commit, push.

Standing preferences from the Sentra reel: photos whole and static; section labels on; no finished-car shots before the reveal;
keep any controversy angle to the hook unless told otherwise; warn once if the music is a commercial track.
