# Direction - Toyota MR2 Spyder scan-process reel (v1 -> v2)

Scene director, 2026-11-11. Inputs read: CLAUDE.md, knowledge/lessons.md (all, incl. the v2 brief rules relayed by the
coordinator), style-guide.md, clips.md, project.yaml, editlog.jsonl, overlay.json, webzoom.json, match/check*.jpg,
match/*.png scan stills, STL headers, and contact sheets of every render in /home/user/media/work/mr2/renders
(sA2, sA3 [36/51 frames done at time of review], sB, sC, sX) and the three IRL clips. No feedback.jsonl exists for this
project yet; the sibling `toyota-mr2-spyder` note (opening too cropped, explode too wide, last scenes held too long) applies.

## 1. Feature inventory

Signature features of THIS car (from footage + scans): roll hoop / top-down roadster profile; louvred engine lid behind
the seats; the 3D-printed hardtop (the project's product, only in IRL FX30636); duct-scooped hood and black rear wing
(both only in the footage - **no scan has them**).

| scan (STL header tris) | frame / registration | what it shows (looked at) | use |
|---|---|---|---|
| Full Car Top Down (14,999,997) | base frame (align.json) | whole car, top off, roll hoop, closed louvred lid, **stock hood**, no wing; dark holes in front intake/grille slit and rear lower grille | cut A, cut B, x-ray base |
| Rear End trunk open (7,000,064) | FPFH+ICP 3.2 mm rms, 31 % overlap (lid + bay differ), bumper/lamps/wheel coincide | engine lid propped open; split into `lid_open` (part) + `rear_open_nolid` | lid-open state + exploded lid |
| `lid_open` part | from the registered scan | underside ribs + insulation AND louvred top both scanned (match/lidbot.png, lidtop.png) | the one part we may spin |
| `lid_closed` | carved from Top Down | closed lid skin | x-ray reassembly |
| Hardtop Mounting Full Car (18,547,676) | same Artec frame (89 % voxel overlap) | top-down + hoop, visually ~ Top Down (match/front_htm.png) | not needed (adds no new view) |
| Full Car (19,540,297) | same `--like` frame per clips.md; **body residual vs Top Down not measured** | car WITH a roof fitted (match/front_fullcar.png) | candidate hardtop part - see open question 1 |
| Kouki+Undertray, Rear Interior Trim Removed, Trunk Open Cover On, Rear QuarterPanel, Hood Duct Data | other frames, not registered (st_*.blend are prepped/aligned only) | - | **unavailable** - no states implied from them |

Region richness (states + parts + signature + quality):

| region | states | parts | signature in scan | data quality | score |
|---|---|---|---|---|---|
| rear / engine lid | closed + open (registered) | lid (inside+outside verified) | louvres | good; lower grille holes, wing missing | **richest** |
| top / cabin | top-off (base); top-on only if Full Car verified | hardtop (unverified) | roll hoop | good | medium |
| front | closed only | none | stock hood != scooped real hood | intake slit holes | weak |
| side | closed only | none | - | good | weak (no dedicated shot) |
| wheels / bay | none | none | - | - | none |

## 2. Scene order (v2)

Two plans. **Plan F** (preferred) applies if the editor's registration of the 2024 front scans succeeds (see section 6);
**Plan base** below is the fallback and stays valid as written.

### Plan base

Travel is front -> top/side -> rear, no ping-pong; the rear (richest) gets the longest block and the explode.
Brief fixes the IRL -> 1:1 structure: cut A (front) must be on the drop, cut B (rear) follows the hardtop action.

| # | scene | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | irl_scan_front | - (DJI_0030 1700-1775) | crew scanning, scooped front | brief: open on real scanning; ends on solved frame | 6 (n23-29) | native portrait full frame - cannot widen |
| 2 | scan_front (cut A on the drop) | Top Down | whole car revealed, hoop | front is weak data -> the shot pulls OFF the hood to the whole car (the reel's only full-exterior view) | 6 (n29-35) | camA, pull 0.35 ease_out (sA3) |
| 3 | irl_hardtop | - (FX30636) | hardtop coming off | top/cabin region, physical removal of the product | 6 (n35-41) | FX 9:16 crop x=1300 |
| 4 | irl_scan_rear | - (DJI_0030 1293-1343) | deck scanning | travel to the rear; ends on solved frame | 4 (n41-45) | native portrait |
| 5 | scan_rear (cut B on n45) | Top Down | louvred lid closed, tail | n45 is the 2nd-strongest low-band kick; rear block starts | 4 (n45-49) | camB, push 6 % (sB) |
| 6 | scan_lid | rear_open_nolid + lid_open | lid open state; lid lifts, shows ribbed underside then louvred top | richest region, only verified part | 8 (n49-57) | **v2: re-render tighter on the deck (sC2)** |
| 7 | scan_xray | topdown_nolid + lid_closed | lid translates home; ends on listing hero angle, morph to grey | reassembly of the part we exploded; strong final cut into listing | 6 (n57-63) | sX reused |
| 8 | website (dissolve) | listing still | listing, title, logo, URL | end card on n63 (last full hit before the decay) | **5 (n62.x-67), was 7** | WebZoom, shortened |

No side / wheel / engine-bay / front-detail scenes: no states, parts or quality data there to show.

## 3. Music map (track s; video s = track - 12.8276; grid t = 0.5145 + 0.53535 n)

Measured per-beat strength this session (40-120 Hz low band / broadband flux):
odd beats carry the loud kick body, even beats the hi-hat flux. Strong lows: n29 drop (0.89 peak at 16.138),
n45 (0.61-0.76, double hit 24.59/24.71), n62 (0.75 @ 33.69), n63 (0.82 @ 34.34). After n63 the highs fall
(hi-band 2.6 -> 2.0 -> 1.6 -> 1.2) and the music is a decay tail; n67 (36.38 s) is where it is effectively gone.

| scene starts | n | track s | video s | frame |
|---|---|---|---|---|
| irl_scan_front | 23 | 12.828 | 0.000 | 0 |
| cut A scan_front | 29 (drop) | 16.040 | 3.212 | 96 |
| irl_hardtop | 35 | 19.252 | 6.424 | 193 |
| irl_scan_rear | 41 | 22.464 | 9.636 | 289 |
| cut B scan_rear | 45 | 24.605 | 11.778 | 353 |
| scan_lid | 49 | 26.747 | 13.919 | 418 |
| scan_xray | 57 | 31.029 | 18.202 | 546 |
| dissolve start -> web | 62.07 -> 63 | 33.73 -> 34.242 | 20.914 -> 21.414 | 627 -> 642 |
| end (fade) | 67 | 36.383 | 23.555 | 707 |

Timing check (lesson FG2/Miata): low-band peaks sit +0..+100 ms after some grid times (n29: grid 16.040, flux
onset 16.080, low peak 16.138). Verify cut-to-kick on the decoded delivered file; if cut A reads early, move the music
start 1 frame earlier, do not move the cut.

## 4. Diff vs v1

| change | what | why |
|---|---|---|
| kept | order of scenes 1-7, all cut points n29/35/41/45/49/57/63 | travel already front -> top -> rear; richest region gets the longest block (n45-63, 18 beats); cut A on the drop |
| re-render | scan_lid sC -> **sC2** (tighter, lid moved toward camera into clear black, orbit 22 deg -> 10 deg) | v1 explodes "too wide, don't zoom in on the part" (sibling + v2 brief); spin kept only because the lid's inside AND outside are scanned |
| shortened | website 3.60 s -> 2.67 s, video 24.50 -> 23.56 s (ends n67) | "last scenes held too long"; music is decay after n63 |
| HUD | `counter` 14,999,997 -> `label` "FULL CAR SCAN / 14,999,997 TRIANGLES" | ScanHUD counter stops at 99.9 % (lesson Sera/C5): v1 would show ~14,985,351 = a wrong number |
| reused | sA3, sB, sX unchanged; IRL clips unchanged | content right, only HUD/end changes |
| not added | any front/side detail, hood open, trim-removed, quarter, kouki | no registered scan of those states (honda-s2000 lesson) |

## 5. Open questions for the editor (don't guess)

0. **Front scans (Plan F gate).** Report in clips.md: residual + overlap of `front fully removed.stl`, `hood open no bumper.stl`,
   `FrontEnd.stl` vs Top Down on rigid panels (median < ~3 mm AND real overlap), what FrontEnd.stl actually is (render it alone),
   and the STL header triangle count of the scan used for the label. No registration = Plan base, no bumper beat at all.
1. **Hardtop as a part (optional upgrade, not in the plan).** Full Car.stl carries a roof; Top Down doesn't; the listing
   hero wears a hardtop. If (a) Full Car vs Top Down body residual is < 3 mm on rigid panels (regcheck, red-over-silver) and
   (b) its roof is the same hardtop the crew lifts in FX30636 (grey printed piece with foil tape - compare), then a hardtop
   part = Full Car tris > 12 mm from Top Down above the belt line, and the x-ray could end with the hardtop translating
   home -> the end frame would match the listing roof too (today "only the roof differs"). Needs the user's/your confirmation;
   until then the hardtop is IRL-only.
2. **Cut B wing.** The real car wears a black rear wing at 56.0 s (checkB.jpg); no scan has it, so it vanishes across cut B
   (same class as the hood scoop at cut A). Accept, or confirm with the user.
3. **FX30636 18.6-21.8 direction.** In this excerpt the hardtop goes from upright-in-hand to lying over the windscreen
   frame - it can read as being put ON. The full clip shows it carried away and set on the floor at ~22-31 s. If it reads as
   "on", take the in-point ~20.5 s so the lift-away (21-24 s) plays out. Never reverse footage.
4. **Plate in sB.** Check the rear plate recess in sB at full res for legible characters (lessons Miata/STI) before delivery.
5. sA3 was 36/51 frames at review time; contact-sheet the finished shot and check the last frame still fills the width
   with the hoop visible (editor's own sA2 complaint).

## Review 2026-11-11 (renders as found)
- sA2/sA3: 1:1 start fine; car sits in the lower ~55 % of frame (inherited from the portrait IRL framing). Bumper intake slit
  is a dark scan hole - the pull-back moves us off it quickly; good.
- sB: rear 1:1, car cropped at the right like the IRL; lower grille mesh partly holed; push is barely visible (fine for 4 beats).
- sC: lid lift + Z-spin reads (ribs, then louvres) and the lid ends over black; but the car is still the subject of most of
  the frame and the orbit adds little -> sC2.
- sX: rear-high start with the lid floating continues sC's end pose; orbit has a purpose (to the listing angle); grey morph works.
- Per-frame luma scan: no dark dropouts in sB, sC, sX, sA3 (so far).

## 6. Plan F - front bumper removed section (CONDITIONAL on registration, user feedback 2026-11-11)

User: bumper-removed data is a hero beat; each section in ONE continuous sequence; deliberate 9:16 framing; no open
hood/trunk/door without its registered state scan. The 2024 front scans of this car (front fully removed / hood open no
bumper / FrontEnd) prove the bumper was physically off when scanned. The footage has no bumper removal, so the section is
scan-only and sits inside the front sequence right after cut A (no IRL -> scan cut is involved).

Inventory change if registered: front goes from "weak" to **second-richest** (removed state + bumper part + exposed
crash beam / mounts / brackets / ducts). Hood open: do NOT animate it in this pass - only with a registered hood-open scan
AND a hinge fit (lessons Huracan/QX80/Sera), and the real car's hood is the scooped one, so it would show a different hood.

Music: one 8-beat splice repeats track bars n33-n40 (18.181-22.464 s) at 22.464 s (n41), 12 ms crossfade (lesson 240SX
audio); check `ive beats` shows an unbroken grid across it. All later accents move 8 beats: cut B stays on the n45 kick, web on
n63. Video grows 23.56 -> 27.84 s (inside 15-30 s). Video beat m (from video 0): v = 0.53535 m, frame = round(16.0605 m).

| # | shot | section | scans | m | video s | frames | beats | music under it (track n) |
|---|---|---|---|---|---|---|---|---|
| 1 | irl_scan_front | front | - | 0-6 | 0.000-3.212 | 0-96 | 6 | n23-29 |
| 2 | scan_front (cut A) | front | Top Down | 6-10 | 3.212-5.353 | 96-161 | **4** | n29 drop - n33 |
| 3 | sF1 bumper off | front | front-removed composite + bumper part | 10-16 | 5.353-8.566 | 161-257 | 6 | n33-39 |
| 4 | sF2 move in on structure + label | front | same | 16-20 | 8.566-10.707 | 257-321 | 4 | n39-40, splice, n33-34 |
| 5 | irl_hardtop | top | - | 20-26 | 10.707-13.919 | 321-418 | 6 | n35-40 (repeat), n41 |
| 6 | irl_scan_rear | rear | - | 26-30 | 13.919-16.060 | 418-482 | 4 | n41-45 |
| 7 | scan_rear (cut B) | rear | Top Down | 30-34 | 16.060-18.202 | 482-546 | 4 | n45 kick |
| 8 | scan_lid sC2 | rear | rear_open_nolid + lid_open | 34-42 | 18.202-22.484 | 546-675 | 8 | n49-57 |
| 9 | scan_xray | whole | topdown_nolid + lid_closed | 42-48 | 22.484-25.697 | 675-771 | 6 | n57-63 |
| 10 | website (dissolve 756-771) | end | listing | 47.07-52 | 25.197-27.838 | 756-835 | dur 2.6333 | n62-67 |

Section coverage (rule B - each section once, one continuous run): **front** = shots 1-4 (frames 0-321);
**top/cabin** = 5; **rear** = 6-8 (418-675); **whole car** = 9-10. Plan base: front = 1-2, top = 3, rear = 4-6, whole = 7-8.
No section returns. (sX's orbit passes the side on its way to the listing hero; that is the whole-car beat, not a side section.)

Why the front block may be 14 beats: with the removed state + part it carries real new geometry (crash beam, brackets,
ducts) - the reveal ladder rung the reel was missing; the drop lands on the 1:1 and the bumper comes off on the next kick (n33).
scan_front shrinks 6 -> 4 beats: it now plays sA3 frames 1-32 only (close hood -> whole front end in width), dropping the
tail of the pull where the car shrinks into the lower half of the frame (rule A).

## 7. Framing audit (rule A: first / middle / last frame of every scan shot, looked at 2026-11-11)

| shot | first | middle | last | verdict |
|---|---|---|---|---|
| sA3 (36-47/51 frames seen) | 1:1 hood close-up, car fills width, top ~50 % black (inherited from the portrait IRL frame) | f20-28: whole front end in width, bumper fully in | f44: front 3/4, tail cropped at left, top ~50 % black | Plan F: use f1-32 only. Plan base: full shot acceptable as the 1:1 payoff; the top black is fixed by the 1:1 |
| sB | 1:1 rear, car cut at the right edge like the IRL, top ~40 % black | same, 6 % push | same | keep: the crop is the match, 4 beats only |
| sC (v1) | rear 3/4, whole car in width in the lower half, lid open | lid above the car, ribs facing camera | lid top (louvres) above the car, over black | car is the subject, lid ~50 % width -> sC2 tightens on the deck/lid |
| sX | x-ray rear, whole car small (~45 % width) in centre, lid floating above | orbiting 3/4 | listing hero angle (WebZoom x1.3), whole car | keep: wide = whole car fully in frame; end pose fixed by the listing |
| sF1 / sF2 / sC2 | - | - | - | new; editor checks first/mid/last before the full render |
