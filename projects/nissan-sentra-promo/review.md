# Nissan Sentra SR promo v1 - self review (training/rubric.md)
Output: `nissan_sentra_promo_v1.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC 192k, faststart, 47.00 s (1410 frames).
Voice only (owner: no music), -14.9 LUFS integrated, -1.5 dBTP. White PromoCaption bubble from the cut on.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Real finished SEMA car (IMG_3229) with the voice from 0.25 s; it moves (handheld push) but nothing transforms until the 4.33 s cut - the voice line is the hook. |
| 2 | Beat sync | n/a (4) | No music by owner decision. Cuts sit on line starts instead: scan 4.333 (line 2 at 4.53), brake 37.10, final 41.23, logo 43.43 - each a gap between voice lines. |
| 3 | 1:1 match | 3 | Cut camera hand-matched by onion overlay of the CAD bumper/ducts on the real frame (~30 px at 540 wide). Per the approved script the scan side opens on empty black and the bumper drops in ~4 frames later, so the match is felt in perspective more than seen in a shared silhouette. |
| 4 | Scan quality | 4 | Quadric-simplified hero mesh, ground/debris islands removed; per-frame luma check on every render (no black frames, no dropouts). Engine-bay scan shows sprayed-matte speckle on the cowl; hub close-up shows scan fringes around the strut (real capture). |
| 5 | Story | 5 | Real car -> scan void -> whole car scanned (body lines, panel gap, bay, fog lamps) -> every SEMA part placed on the scan in one front->rear move -> brake adapters revised -> finished build -> CTA. One part group per line. |
| 6 | Grade | 4 | One IRL clip only (tonemapped); scan in house silver on black. |
| 7 | Text | 5 | Captions = the narration verbatim, one line at a time, never over IRL, phone-legible white bubble. No numbers on screen. |
| 8 | Ending | 4 | Logo card 43.43-47.0 under "get it on illumaesthetic.com"; voice ends 45.58, card holds and fades. |
| 9 | Technical | 5 | Spec met; frames around all four cuts checked (no dup/black); exact frame counts asserted per segment. |

## Fixed during review
- Fog-lamp beat ("and the fog lights"): v1 render parked the two lamps 0.9 m apart from a 3/4 camera - the 9:16 frame only
  spans ~0.6 m there, so one lamp was a speck at the edge and the other off-frame. Re-framed (lamps side by side in
  front of the nose, camera dead ahead) and re-rendered frames 257-352.

## Known weaknesses / for the reviewer
- Fog lamps now read against the engine bay (silver on silver) rather than black - recognisable, but busy.
- Wing beat shows the wing **adapter** only: it is the only file in the SEMA Wing folder (narration "and a wing" is owner-approved).
- Brake adapters: test-fit vs V3 differ 6-15 mm, V3 vs V4 ~2 mm - the V3->V4 step is barely visible on screen.
- Engine-bay scan and the bumper-removed state were captured hood-off; the hub was captured drooped on the lift, so the
  brake beat is its own close-up rather than placed in the car.
- Final orbit frames the whole car small in 9:16 (whole car + wheels in frame).
- Render cost: ~10-60 s/frame at 75 % / 12 spp on 4 CPUs (engine-bay frames slowest); ~5.5 h total for 598 frames.

## v2 (reviewer feedback 2026-11-14) - `nissan_sentra_promo_v2.mp4`, same spec, -14.9 LUFS / -1.5 dBTP
| Note | Fix |
|---|---|
| the new wheels aren't on | Wheels FL/FR/RL/RR from Ron's `Sentra Review 2.blend` (collection *Wheels & Wing*, already in the design frame). Stock wheels+tyres cut out of the scan (`tools/rearcut.py`, centred on the new wheel, liner kept above the axle); they pull outboard and the new wheels slide in under "wider fenders and a new hood" (30.2-30.95 s). In the finished-car orbit. |
| the rear wing isn't actually installed | The wing (`nissan_gtr_nismo.001`, same collection) lands on the adapter under "and a wing" (36.15-36.6 s) and stays for the orbit. `Plane.002` in that collection lies on the scanned trunk lid (median 3 mm) - a mounting reference, not used. |
| old diffuser is not removed | Stock lower valance (scan tris within 45 mm of the CAD diffuser, below its top edge) drops away 34.45-34.8 s, then the diffuser comes up into its place. |

Re-rendered main frames 386-495 and the final orbit; seam at 385/386 measured at the median frame difference (invisible).
Scores changed: Story 5 (unchanged, now true to the finished build), Scan quality 4.

## Gap to learn from
v1 used only the SEMA `STL/` folder. The wheels and wing lived in Ron's review .blend (`Sentra Review 2.zip`), and the
stock parts the kit *replaces* (valance, wheels) must come off the scan, not just have the new part laid over them.
Inventory the review files and list replaced stock parts before planning shots.
