# Director plan - Toyota MR2 Spyder scan-process v2

Stage 2 after direction.md (scene order kept exactly; no re-ordering). Scan frame: +Y = car front, +X = car right
(viewer's left from behind), Z up, metres, car centred at origin on Z=0; tail at y = -1.94, nose at y = +1.94.
Video 30 fps, 1080x1920; renders 15 fps at 75 %, minterpolated.

`python -m ive director projects/toyota-mr2-spyder-scan-process/project.yaml` exists but **fails** on the real project:
the website clip `/home/user/media/work/out/webzoom_mr2_v1.mp4` is not rendered yet (ffmpeg exit 254). I ran it on a
scratch copy of the yaml without the website clip. Result: 21.37 s analysed, no dead frames, **no repeated views**, every clip
flagged "no focus: tag"; `irl_scan_front` first frame "crops the car at both sides". Coverage %: sA3 45->41, sB 31->34,
sC 21->24, sX 12->13 (the explode and x-ray are the small-in-frame shots).

**Two plans** (see direction.md sections 2 and 6). The table below is **Plan base** (no new front data). If the 2024 front
scans register, use **Plan F** (section at the end): same shots plus a front-bumper-removed section after cut A, an 8-beat
music splice, and every later shot shifted by 8 beats (shot lengths unchanged except scan_front 6 -> 4).

## Shot table (Plan base)

Every clip gets `section:` and `focus:` tags in project.yaml (fixes the report's missing-focus flags).

| section | shot | start-end (video s / frame) | focus | camera | part action (beat times) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| front | irl_scan_front | 0.000-3.212 / 0-96 (6 beats, n23-29) | crew scanning the scooped front | DJI_0030 1700-1775, native portrait; ends ON frame 1775 (74.0 s) | scanner sweep; camera settles on the solved frame | hook: real scanning, then the transformation on the drop | reuse |
| front | scan_front (1:1 cut A, n29 drop) | 3.212-6.424 / 96-193 (6) | whole scanned car - hoop + body - pulling off the hood | camA (loc 0.77, 2.63, 1.22, f 22 mm/20.25 sensor), pull 0.35 ease_out | none (front has no parts/states) | the 1:1 cut is the signature; the pull is the reel's only full-exterior view; leaves the hood (stock in scan) and the intake hole fast | **reuse sA3** (when its 51 frames are done; sA2 is superseded) |
| top | irl_hardtop | 6.424-9.636 / 193-289 (6) | the hardtop coming off the car | FX30636, LUT graded, 9:16 crop x=1300 | crew lifts the hardtop (see direction.md Q3 for in-point) | the only physical removal in the footage; the hardtop is the product | reuse |
| rear | irl_scan_rear | 9.636-11.778 / 289-353 (4, n41-45) | scanner on the rear deck | DJI_0030 1293-1343, ends ON frame 1343 (56.0 s) | scanner sweep, camera pulls back to the full rear | travel to the rear; sets up cut B | reuse |
| rear | scan_rear (1:1 cut B, n45 kick) | 11.778-13.919 / 353-418 (4) | louvred engine lid, closed, from behind | camB (loc -0.31, -3.09, 1.34, f 22), push 6 % | none | second 1:1; shows the closed lid that opens next | **reuse sB** |
| rear | scan_lid | 13.919-18.202 / 418-546 (8, n49-57) | engine lid: open state, then the lid's ribbed underside and louvred top | **sC2, new** - see spec below | lift + move toward camera 0.05-0.35 (n49.1-n51.5); Z-spin 180 0.40-0.90 (n52-n56) | richest region: registered open-state scan + the only verified part; inside+outside both scanned so the spin shows something new | **re-render sC2** (fallback: reuse sC) |
| rear -> whole | scan_xray | 18.202-21.414 / 546-642 (6, n57-63) | lid translating home, then the whole car at the listing angle | cam_xray_start (loc 0.55, -7.85, 3.00, f 70.8/36) orbit +50 deg about (0,0,0.55) to cam_listing_v (6.37, -4.62, 3.00) | lid from +0.7 m Z back home 0.08-0.55; morph to listing grey 0.62-1.0; holds 0.45 s | reassembly of the exploded part and the exact listing hero angle -> the strongest final cut | **reuse sX** |
| end | website (dissolve 0.5 s, n62.07-63) | 20.914-23.555 / 627-707 (dur 2.6667) | listing hero -> title, logo, URL | WebZoom, focus 983,838, startScale 1.3 | zoom-out, then text | close on the product; music decays to n67 | re-render WebZoom with durationInFrames 80 (Remotion, ~1 min) |

Total 23.555 s (707 frames), was 24.50 s. Cut frames: 96, 193, 289, 353, 418, 546, 642 (dissolve 627-642), end 707.
project.yaml: website `dur: 2.6667`; music `fade_out: 0.8` stays (fade runs 22.76-23.56 over the decay tail).
WebZoom: `durationInFrames: 80`; title/logo/URL must be fully in by card frame ~50 and hold >= 0.9 s - read the final
frame; if the text arrives later than that, shorten `zoomFrames` 45 -> 36 rather than lengthening the card.

### sC2 spec (the one new Blender render, ~25-30 min, 68 frames)
```
python -m ive render -- --scene /home/user/media/work/mr2/scan/rear_open_nolid.blend \
  --camera <cam_C2.json from `ive lookat`: location (0.80, -3.20, 1.85), look-at (0, -1.40, 1.20), focal 24 mm, sensor 20.25 mm> \
  --seconds 4.5 --move orbit --move-amount -10 --ease ease_in_out --look-at=0,-1.4,1.2 \
  --explode "/home/user/media/work/mr2/scan/lid_open.blend:0,-0.35,0.45:0.05:0.35:z180:0.40:0.90" \
  --res 1080x1920 --res-pct 75 --samples 12 --fps 15 --out /home/user/media/work/mr2/renders/sC2/
```
- Camera in words: rear 3/4 from the car's right-rear, ~2.1 m from the lid, ~35 deg down, framed on the deck/lid; the tail
  lamps and rear wheel arches crop at the frame sides (focus on the section, not the whole car). 24 mm on the 20.25 mm sensor
  gives ~1.65 m of width at the lid, so the 1.4 m lid fills ~85 % of the width at its widest.
- Part: same verified lid motion as sC, but it travels 0.35 m toward the camera (-Y) as well as up 0.45 m, so it sits above
  the tail against black, not over the roll hoop/body (reviewer: move parts into clear background, often toward camera).
  Spin starts at 0.40 (after the lift completes) and ends at 0.90 - underside ribs/insulation first, louvred top last; the
  last 10 % holds the top view, which matches sX's first frame (lid floating above the rear).
- Clearance: lid centre ends ~(0, -1.47, 1.65); the spin sweeps y -2.2..-0.75 at z >= 1.4, above the tail (z <= 1.0) and
  the roll hoop (z ~1.15) - no intersection. Check frames 1, 25, 40, 55, 68 before the full run (`kill -STOP` trick if
  another job runs) and confirm the lid never leaves the frame top.
- Persistent data OFF (animated part, lessons G35/Ferrari/Cappuccino); scan per-frame luma after the render.
- Orbit cut from -22 to -10 deg: the spin is the move; the orbit only adds parallax (rule: no wasted rotations).
- HUD on sC2 unchanged: brackets 421-543, "REAR END SCAN / 7,000,064 TRIANGLES" 424-480, "ENGINE LID / INSIDE + OUTSIDE
  SCANNED" 484-543 (claim verified on lidbot/lidtop renders). Keep text out of the lid's path: top-left at y 0.10 is where the
  lid now rises - move both labels to y 0.80 (lower-left, above the 20 % caption zone) if the lid overlaps them in sC2.
- Fallback if the render budget is not there: reuse sC unchanged (content verified, just wider).

## HUD (overlay.json, Remotion re-render)
| item | frames | change |
|---|---|---|
| brackets scan_front | 99-190 | keep |
| counter 14,999,997 | 102-188 | **replace with `label`** title "FULL CAR SCAN", sub "14,999,997 TRIANGLES" (counter stops at 99.9 %, would show a false number) |
| brackets + 2 labels on scan_lid | 421-543 | keep (numbers from STL headers, verified this session: 14,999,997 / 7,000,064) |
| durationInFrames | 735 | -> 707 |
No HUD on IRL, sB, sX or the end card.

## Cut list (removed from v1)
- Website card frames 707-735 (0.93 s) - held after the music is gone ("last scenes held too long").
- sC's wide framing and 22 deg orbit - replaced by sC2 (same lid action, tighter, part into clear black).
- HUD counter animation - false final number.
Nothing else is redundant: the director report found no repeated views, and each shot has a different subject
(scanning front / whole car / hardtop / scanning rear / closed lid / open lid + part / reassembly / listing).

## Hold list (> 0.75 s with little motion)
- sB 2.14 s, push only 6 %: it is the 1:1 payoff of cut B; the eye is still matching the real tail to the scan. Keep.
- sX last 0.45 s (frames ~628-642): intentional hold on the listing angle under the dissolve so it reads as one object.
- sC2 last ~0.4 s: lid top view held so the cut into sX's floating-lid start reads as continuous.
- Website: zoom then ~1 s static text - needed for the URL to be read; ends with the music.

## Render budget
- New Blender: sC2 only, 68 frames at 15 fps, 75 %, 12 spp (~25-30 min). Run after sA3 finishes (one Blender at a time).
- Remotion: HUD overlay (707 frames) and WebZoom (80 frames) re-renders.
- Reused unchanged: sA3 (in progress), sB, sX, irlA, irlB, irlH (in-point per direction.md Q3 only if it reads as "on").
- Not used: sA, sA2 (superseded), match/test renders.

## Checks before delivery
- Frame diffs at every cut (96, 193, 289, 353, 418, 546) and cut-to-kick error on the decoded file (target <= 1/2 frame).
- Per-frame luma on sC2.
- Plate recess in sB at full res.
- Final frames of the HUD labels and the WebZoom text.

## Plan F - front bumper removed (CONDITIONAL: only if the editor's registration of the 2024 front scans passes)

Timing (frames at 30 fps, m = video beat): irl_scan_front 0-96 | scan_front 96-161 | **sF1 161-257** | **sF2 257-321** |
irl_hardtop 321-418 | irl_scan_rear 418-482 | sB 482-546 | sC2 546-675 | sX 675-771 | web 756-835 (dissolve 756-771,
dur 2.6333). Music: start 12.8276, splice = repeat 18.181-22.464 s at 22.464 s (12 ms crossfade); end 27.838 s with fade 0.8.

| section | shot | frames | focus | camera | part action | why | render |
|---|---|---|---|---|---|---|---|
| front | scan_front (cut A) | 96-161 (4) | the matched front end | camA, sA3 frames 1-32 only, src_fps 15 | none | 1:1 payoff on the drop; cut before the pull shrinks the car | reuse sA3 (trim) |
| front | sF1 | 161-257 (6) | front bumper coming off, its inner face (mount tabs, brackets) | front 3/4 from the car's right-front, matching camA's side: loc (1.90, 4.20, 1.35), look-at (0.10, 1.50, 0.45), 30 mm / 20.25 mm sensor, push 8 % ease_in_out | bumper 0.10-0.55: translate (0, +0.55, +0.75) - forward toward the lens and UP into the black above the nose (9:16: stack above); tip x-80 deg 0.30-0.70 so its scanned inner face turns to the lens (pick the sign so the bottom edge swings forward; verify on 3 test frames); hold 0.70-1.0 | hero beat (user): the removed state + part; moves into clear black, not across the body | **new** ~52 frames |
| front | sF2 | 257-321 (4) | exposed crash beam / bumper mounts / brackets / ducts | continuous move-in: from (1.20, 3.30, 0.95) to (0.70, 2.75, 0.75), look-at (0.0, 1.75, 0.45), 35 mm; the bumper stays parked at its sF1 end offset (out of frame top) | none - hold to read | lets the viewer read the structure; label lands here | **new** ~36 frames |

sF1/sF2 scene (editor builds, lessons Ferrari/C5/Frontier/STI): base = Top Down minus triangles within ~9 mm of the bumper
part, plus `front fully removed` triangles > 7 mm from the trimmed car inside the bumper opening box only (no ground < 100 mm,
nothing above the hood line). Bumper part = carved from Top Down (car tris > 12 mm from `front fully removed`, y > ~1.4,
largest island) so it seats exactly; use FrontEnd.stl instead only if rendering it alone shows it IS the bumper and it lands
< 3 mm on the car. Before claiming anything: render the exposed area and the bumper's back - if the crash beam/brackets are
scan holes, frame what IS captured (240SX: crash beam only existed on the chassis scan). Persistent data off; luma-scan frames.
Framing (rule A): sF1 = whole front end (both headlights, both front wheels) in width the whole time with the bumper fully in
frame at the top; sF2 = structure fills >= 70 % of the width. Check first/mid/last before the full run.

HUD (Plan F): scan_front label "FULL CAR SCAN / 14,999,997 TRIANGLES" frames 99-158; sF2 brackets 260-318 + label
"FRONT BUMPER REMOVED" with sub = "<N> TRIANGLES" where N = the STL header of the front-removed scan actually used (read it;
do not round or invent); rear labels shift +128 frames (brackets 549-672, "REAR END SCAN" 552-608, "ENGINE LID" 612-672);
durationInFrames 835. Max two items on screen; nothing over IRL.

Not in Plan F: hood opening (no registered hood-open scan + hinge yet, and the scan hood is stock vs the real scooped hood).

Render budget Plan F: sF1 (~52 frames) + sF2 (~36) + sC2 (68) = ~156 frames, ~70-80 min serial on this CPU box;
order: sC2 (needed in both plans) first, then sF1, sF2 once registration passes. Reused unchanged: sA3 (trimmed), sB, sX, all IRL.
