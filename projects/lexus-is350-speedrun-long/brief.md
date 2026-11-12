# L1 - "How fast can we 3D-scan an entire car?" (Lexus IS350 speed run) - production brief

Greenlit by the owner 2026-11-12. Pitch with section-by-section shot list: `pitches/2026-11-12-pitch-slate.md` (L1).
Deliverable: YouTube long-form, 1920x1080, 23.976 fps, 5-7 min, plus a 1280x720 thumbnail.

## Facts from the owner (use exactly; invent nothing else)
- Final time: **32 minutes elapsed; 20 minutes without the crash.** What crashed and when is not known yet -
  find it in the transcript; if the footage doesn't say, write "a crash" and flag it for the owner.
- Owner wants: burned-in captions, 2D graphics, and 3D models of the finished scan "littered in" through the video
  (not only at the end), background music, a conclusion, a thumbnail.

## Media
- Footage: `/home/user/media/lexus-is350/dropbox/FX30541..555.MP4` (15 clips, Sony 4K S-Log3 23.976p; clip-by-clip notes in
  `projects/lexus-is350-scan-process/clips.md`). Grade LUT and earlier reel tooling: `projects/lexus-is350-scan-process/`.
- Scans (Drive "Lexus 4is", folder 1RI5YIMmHU9GC1ziv7P6u5ZQJoU0Bnhsv): `Lexus 4IS IS350 Full Car.stl` (24,999,992 tris),
  `Lexus 4IS reflector.stl`, `Lexus 4IS reflector removed.stl`. Fetch with `python -m ive fetch-drive <id> <dir>`.
- Work dir: `/home/user/media/work/is350-long/` (subfolders: transcripts, renders, gfx, music, vo, thumb, out).
  Media is never committed; only small text/JSON/YAML goes in `projects/lexus-is350-speedrun-long/`.

## House rules that bind every agent (full list: CLAUDE.md, knowledge/lessons.md, knowledge/style-guide.md)
- Only true numbers on screen or in narration: triangle counts from STL headers, times the owner gave or that are legible
  on the stopwatch in frame. No scanner specs, accuracy, tolerances, prices.
- The IRL -> scan transformation is a hard 1:1 cut, never a dissolve.
- Text over IRL footage: the only exception the owner has asked for here is **captions**. Other graphics go on scan
  renders, on black/graphic cards, or in a panel beside (not on top of) the footage, unless the lead says otherwise.
- Nothing opens or comes off in the scan unless a scan of that state exists (here: only the rear reflector).
- The scan shows a legible licence plate: flatten/blur it in every render and in any IRL frame where it is readable.
- Scan look: satin silver on pure black, soft studio light, slow continuous moves, no ground.
- No cloning of a real person's voice. Narration units imperial.
- Blender renders: Cycles CPU, one render job at a time on this box (4 cores), in the background.
- Log every editorial decision: `python -m ive log projects/lexus-is350-speedrun-long "<what>" --why "<why>"`.
- Look at your own output (sheets, frames) before reporting it good. Report failures and gaps plainly.
