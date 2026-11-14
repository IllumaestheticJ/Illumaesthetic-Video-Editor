# Clip logging brief (Grimace parts-build long-form)

You are logging raw footage so an editor can build a sponsor-supported YouTube long-form about the parts installed on
"Grimace", a purple NA Miata race car (#558, Epsilon Motorsports). You only log; you do not edit or plan.

Read first: `projects/grimace-build-longform/clips.md` (sources, the host's parts walkthrough, parts by supplier).

Per clip you have, under `/home/user/media/grimace-build/`:
- `sheets/<stem>.jpg`: contact sheet, up to 24 frames in time order, 6 per row (frame spacing = `sheet_step` seconds in `ingest.jsonl`).
  Look at every sheet with the Read tool.
- `tx/<stem>.json`: speech transcript (may be empty; small.en model, so brand names are often misheard, e.g. "Mud-i-Q" = MotoIQ,
  "white line" = Whiteline, "good one" = Good-Win). `transcripts.txt` has all of them.
- `proxy/<stem>.mp4`: 960x540 proxy. When a sheet is not enough to tell which part or what step it is, pull full frames:
  `ffmpeg -v error -y -ss <t> -i proxy/<stem>.mp4 -frames:v 1 /tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/a4d5891b-ecef-5048-9c6e-5f4d234ca56f/scratchpad/<stem>_<t>.jpg` and Read it.
  Do this for any clip where a brand, box label or part is visible but unreadable on the sheet.

Write ONE markdown file (path given in your task) with one table row per clip, in file-name order:

| clip | dur s | what happens (specific: which part, which corner of the car, which step) | part / brand visible | speech (short quote or summary; "none") | shot type | quality | best span s |

- shot type: one of `talking head`, `install action`, `part beauty`, `car beauty`, `b-roll shop`, `track`, `on-board`, `blooper`, `other`.
- quality: `good`, `ok`, or `poor` plus the reason if not good (soft focus, shaky, dark, blocked, too short, profanity in audio).
- Never guess a brand or part name. If you cannot read it, write what it looks like and "unidentified".
- Note anything that shows before/after (old part next to new part), a finished install, or torque/measurement steps.

After the table add three short lists:
1. **Install coverage**: for each part family (coilovers, big brake kit, pads/fluid, bushings, sway bars, strut tower brace,
   fender braces, tie rods, steering rack bushings, steering wheel, other), which clips show it and how complete the
   coverage is (unboxing / removal of old part / fitting / finished).
2. **Usable host lines**: clip + time + exact words for anything the host says to camera that explains a part.
3. **Problems**: clips that are unusable and why.

Be accurate over fast: a wrong part name in this log becomes a wrong line in a sponsor video. Final message: path of the
file you wrote and a five-line summary.
