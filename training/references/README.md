# Reference edits

Numbers in `*.json` come from `python -m ive analyze`. Notes below are the human/agent read of each.
Add a section for every new reference the team says is good.

## `edited_oct31_1330_46` — 240SX scanning, IRL-only reel (approved, Oct 31 2026)
Dropbox `/2. Illumaesthetic Videos/1. Video dumps/240SX scanning/Video Oct 31 2026, 1 30 46 PM.mp4`
- 1440×2560 HLG, 22.8 s, 6 shots, avg 3.8 s; music 95.7 BPM, all cuts on beats.
- Story: crew walks to car → scanning powder / handheld scanner → bumper removal → logo card at 20.1 s.
- What it lacks (and the v1 scan reel adds): the scan data itself. The audience never sees the result.

## `v_jul22_1047_58` — Lamborghini Temerario scan reel (website reference)
Same Dropbox folder, `Video Jul 22 2026, 10 47 58 AM.mov`. 1440×1920, 39.8 s, one continuous move.
- Silver metallic scan on pure black, soft top light; dense scan detail visible.
- Beats: slow 3/4 turntables → extreme close-up (wheel) → hood/doors open → top-down flip →
  **exploded view** (body panels separate, then reassemble) → logo.
- No text at all. The scan *is* the content.

## `reel_0144_48` — Corolla "Good Reel" (Epsilon)
Dropbox `/5. Claude Training/Good Reels (Epsilon)/Video Nov 10 2026, 1 44 48 AM.mp4`. 7.8 s, 3 shots of ~2.6 s.
- **Every cut is a 1:1 perspective cut**: stock car on a street → same framing, rendered modified car
  in a different location → same framing, real modified car. Car size/position constant; world changes.

## `reel_0149_10` — Civic "Good Reel" (Epsilon)
Same folder, `Video Nov 10 2026, 1 49 10 AM.mp4`. 13.6 s, 14 shots.
- 4.5 s CG hook on black with a quoted caption ("This car has NO lip options, it's so ugly") →
  **1:1 cut at 4.47 s** from the CG car to the real car in the same pose → rapid detail montage
  (0.3–0.8 s shots) on the beat → wing hero.
- Integra training photos (`Integra training/`) show the finished-product angles the team likes:
  low front 3/4, rear 3/4 at wheel height, straight-on rear with wing.

## `FG2 Lip CGI-Real.mp4` — Ecky's CGI→real cut (FG2 #806)
Drive `74 - Civic FG2 Race Lip` (1itRtubjAyFciRvZC0IKNiRUqHEoOTuET). 1080x1920 60 fps, 52 s, no audio.
- Red CGI car on a dark ground with black background → same pose, real #806 car; front, lip close-ups, rear wing.
- CGI look: glossy red paint, black lip/wing, black sky. `projects/fg2-race-car` reuses this look from `FG2 Race Lip.blend`.

### `v_jul22_1047_58` Temerario - measured timeline (added by the huracan-evo agent, 2026-11-11)
From 1 s contact sheets of the 24 fps 1440x1920 file (no audio track). Two hard shot boundaries detected (`ive analyze`
threshold 0.3); the rest are whip-smears / continuous moves.
| t (s) | beat |
|---|---|
| 0-3 | fade up from black, low side profile, nose right, slow track |
| 4-7 | front 3/4 low, slow turntable |
| 8-11 | rear 3/4, turntable; whip-smear out at ~11 |
| 12-15 | front-fender/wheel close-up; front bumper comes off, hood opens, front structure exposed |
| 16-20 | fast flip to top-down, spinning, front parts (bumper, liners) spread around the nose |
| 21-23 | high rear 3/4, engine cover / panels lifting off |
| 24 | dark flash |
| 25-31 | side view, panels floating in layers ABOVE the car (portrait-friendly stacking) |
| 32-35 | panels return, assembled car rear 3/4, fades to black |
| 36-39 | ILLUMAESTHETIC logo (~50 % frame width) on black |
Look: near-white satin silver, AgX-ish, mid-grey median luma ~200 on car pixels; raw scan speckle visible (dusty capture).

### `v_jul22_1047_58` Temerario - watched frame by frame (2026-11-11, Ferrari 296 session)
Downloaded and sheeted at 1 fps plus 8 frames/s around each jump. 1440x1920, 24 fps, 39.83 s, **no audio track**.
- **Timeline:** 0-1 s fade up from black on a side profile → 1-4 side slide → 4-8 low front 3/4 → 8-11 rear 3/4 →
  ~11.5 fast fly-in to an extreme wheel/arch close-up that fills the frame → 12-16 front-wheel close-up while the front
  end **progressively comes apart** (bumper slides off, frunk lid opens, inner panels peel) → hard jump at 16.2 to a
  high top-down 3/4, rotating, front parts *and wheels* floating off → 21-24 rear-high 3/4, engine cover/rear panels
  lifting → hard jump at 24.2 → 25-27 close side tracking with panels stacked above → 28-31 wide side **fully exploded:
  panels lifted vertically in layers** above the chassis, wheels off → 32-33 parts fly back → 34-35 assembled rear 3/4
  → 36 fade to black → 37-38.5 small logo (~35 % of frame width) on black → black.
- The exploded section is ~20 s of the 40 s (half the reel); disassembly is progressive, not one burst.
- Only 2-3 visible camera jumps; everything else is one continuous, slow move with occasional fast fly-ins.
- **Look:** NOT smooth chrome. Warm, slightly mauve satin silver with cool blue-grey shadows (warm key, cool fill),
  and the **raw scan grain is visible everywhere** (sandblasted/stone texture: full-resolution mesh, no decimation
  smoothing). Undersides/backfaces of lifted panels read darker mauve-red. Background pure black, no floor.
- Car is smaller in frame than our reels in the wide shots (~60-70 % of width); close-ups are extreme.
