# Explainer brief (Grimace build video)

You are building short animated 2D explainers that play under one narration line each. Use the shared kit and copy the
structure of the reference exactly so every explainer looks like one family.

- Kit: `tools/gfx.py` (read its docstring and the Canvas methods). Coordinates are 1280x720. `render(line, fn)` writes
  `/home/user/media/grimace-build/gfx/L<line>.mp4` with the right duration for that narration line on its own.
- Reference: `tools/gfx_coilovers.py` (lines 13-17). Look at its check frames in `/home/user/media/grimace-build/gfx/chk/coil.jpg`.
- One function per script line, named `L<line>(c, u, t)`; `u` = 0..1 progress, `t` = seconds. Start each with
  `c.header('HOW IT WORKS', '<short title>', GROUP, u)` and end with `c.chip('<chip text given below>', GROUP, u=u)`.
- Put a `FN = {line: fn}` dict and the same `__main__` block as the reference (`still` mode writes check frames to
  `gfx/chk/L<line>.png`; no argument renders the mp4s).

Rules
- The picture must show the mechanism the line describes, moving, so that it reads with the sound off. Elements appear as the
  line gets to them (use `seg(u, a, b)` windows); keep motion slow and continuous; nothing should pop or flash.
- No numbers, units, part numbers, temperatures, sizes or percentages anywhere. No brand names except the chip text given.
- Short labels in capitals, at most about four words; nothing smaller than size 15; keep text inside x 60..1220, y 130..620
  (the header is above, the chip below). Do not overlap labels with shapes.
- Colours: use `COL[GROUP]` as the accent, `COL['bad']` / `COL['good']` only for a worse/better comparison, WHITE and DIM for text.
- Schematic, not realistic: simple side or top views built from rects, lines, circles, springs and arrows.
- These are general illustrations of how that kind of part works. Do not draw anything that claims a measured result.

Check your work: run the script with `still`, open every check frame with the Read tool, and fix overlaps, clipped text,
empty frames and anything that does not match the line. Also render two more stills per line at u = 0.15 and u = 0.95 (use
`still(lambda c, u, t: fn(c, u, <t>), <u>, path)`) and look at them, so the start and end states are right. Then render the mp4s.
Do not touch git, the script, or any other file than the one you are asked to write.
Final message: the file you wrote, the mp4s rendered, and one sentence per line on what the picture shows.
