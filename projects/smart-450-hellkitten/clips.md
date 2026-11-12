# S3 Smart 450 "Hellkitten" scan reel: clip notes

Source: Dropbox `Hellkitten Footage`, shot 2026-07-26 (local copies in `/home/user/media/smart-hellkitten/dropbox/`).
**15 files** (the pitch said 14; `v_1728_34` is a 0.9 s fragment). Contact sheets at 1 frame per second, 6x4 tiles
(HLG tonemapped, with timecodes), are in `/home/user/media/work/smart-450/sheets/<clip>_NN.jpg`, where NN counts 24-second blocks.
I looked at every sheet. Extra enlarged frames are in `/home/user/media/work/smart-450/sheets/frames/`.
(`ive sheet` only tiles evenly over the whole clip and has no density option, so the sheets were made with ffmpeg directly.)

All timecodes are seconds into the file as the clip is **displayed**. Descriptions are what I saw; guesses are marked *(guess)*.
Motion figures quoted as "steady" come from frame-difference (ffmpeg signalstats YDIF at 320 px wide); the number is only
relative, the lower the steadier.

## Read this first: three clips carry a wrong rotation tag

`v_1633_51`, `v_1645_19`, `v_1659_53` are tagged rotation -90 (the `probe` says portrait), but the picture is **not**
upright after the tag is applied: the car appears on its side (sheet check, and a `-noautorotate` frame shows the raw 1920x1080
picture is upside down). Fix: decode with `-noautorotate` and rotate 180 degrees (`hflip,vflip`); the result is an upright 1920x1080
landscape clip (verified on a frame of each, `frames/rot_check.jpg`). Anything that trusts the tag (`ive assemble`, `ive frame`)
will give a sideways car. Check how `ive assemble` handles rotation before using these three.
`v_1634_51` (-90) and `v_1634_19` / `v_1729_10` (-180) are correct as tagged.

## Format and audio table

iPhone clips: HEVC Main10, **HLG (arib-std-b67, bt2020)**, 1920x1080, ~30 fps, 4-channel audio.
Glasses-POV clips (Ray-Ban Meta style, *guess from the 3:4 portrait SDR profile; same as the Lola notes*): HEVC 8-bit **SDR bt709**, ~30 fps, 3:4, 2-channel audio.

| local | Dropbox name | len | res / rot tag | HDR | audio mean / peak (dB) | speech |
|---|---|---|---|---|---|---|
| v_1620_30 | Video Jul 26 2026, 4 20 30 PM.mov | 34.0 s | 1920x1080, 0 | HLG | -20.6 / 0.0 | narration to camera |
| v_1632_12 | Video Jul 26 2026, 4 32 12 PM.mov | 26.0 s | 1920x1080, 0 | HLG | -21.0 / 0.0 | narration to camera |
| v_1633_51 | Video Jul 26 2026, 4 33 51 PM.mov | 14.9 s | 1920x1080, -90 (**wrong, see above**) | HLG | -19.9 / -0.4 | narration, partly garbled |
| v_1634_19 | Video Jul 26 2026, 4 34 19 PM.mov | 28.7 s | 1920x1080, -180 (ok) | HLG | -22.6 / -4.8 | none detected |
| v_1634_51 | Video Jul 26 2026, 4 34 51 PM.mov | 10.8 s | 1920x1080, -90 (ok, true portrait) | HLG | -21.0 / -3.3 | none detected |
| v_1640_44 | Video Jul 26 2026, 4 40 44 PM.mov | 68.8 s | 1504x2000 (3:4), 0 | SDR | -24.6 / -1.4 | bystander conversation |
| v_1645_19 | Video Jul 26 2026, 4 45 19 PM.mov | 19.7 s | 1920x1080, -90 (**wrong**) | HLG | -20.1 / 0.0 | narration to camera |
| v_1659_53 | Video Jul 26 2026, 4 59 53 PM.mov | 22.2 s | 1920x1080, -90 (**wrong**) | HLG | -21.0 / 0.0 | narration to camera |
| v_1712_33 | Video Jul 26 2026, 5 12 33 PM.mov | 22.4 s | 1920x1080, 0 | HLG | -21.5 / 0.0 | narration to camera |
| v_1722_25 | Video Jul 26 2026, 5 22 25 PM.mov | 107.0 s | 1504x2000 (3:4), 0 | SDR | -23.5 / -0.2 | bystander banter |
| v_1724_26 | Video Jul 26 2026, 5 24 26 PM.mov | 125.3 s | 1328x1760 (3:4), 0 | SDR | -25.7 / -0.4 | bystander conversation |
| v_1728_34 | Video Jul 26 2026, 5 28 34 PM.mov | 0.9 s | 1376x1840 (3:4), 0 | SDR | -45.8 / -4.5 | none |
| v_1729_10 | Video Jul 26 2026, 5 29 10 PM.mov | 11.6 s | 1920x1080, -180 (ok) | HLG | -21.8 / 0.0 | narration to camera |
| v_1852_56 | Video Jul 26 2026, 6 52 56 PM.mov | 27.4 s | 1920x1080, 0 | HLG | -21.3 / 0.0 | narration to camera |
| v_1857_58 | Video Jul 26 2026, 6 57 58 PM.mov | 24.1 s | 1920x1080, 0 | HLG | -22.9 / 0.0 | narration to camera |

Probe: all ~29.99-30.0 fps (the iPhone clips are 29.987 fps VFR-ish; the glasses clips 29.995-30.001).

### Shop sound
Every clip has loud shop audio (means about -20 to -25 dB, peaks at 0 dBFS on the iPhone clips, so there may be clipped handling thumps).
But almost all of it is **voice**: the filmmaker narrates to camera in the iPhone clips, and the glasses clips are full of bystander
chatter. Sound that works under music as pure ambience (no speech detected by faster-whisper): **`v_1634_19` and `v_1634_51`**
(spray-gun hiss and shop noise while powdering). `v_1728_34` is near silent (-45.8 dB). Everything else needs the audio dropped
or ducked heavily.

### Speech (faster-whisper `tiny.en`, run on every clip; transcripts are rough, quotes are ASR and may be wrong)
Addressed to camera by the person filming (a possible VO source, but the brief says no VO):
- v_1620_30, 1-34 s: "This is our 2002 smart car ... we are going to turn this into the [Hellkitten?] thing, so first things first I have to scan it. It's not in very good shape. It's missing doors. It's missing the inside door cards, battery is super dead. It's dirty. We got the car for free ... first things first we're gonna put the car exterior back together as much as we can and then scan it." (The ASR heard "Helkin thing"; I read it as the project name *(guess)*.)
- v_1632_12, 0-25 s: "So with the help of my friends, the panels are back on. Kind of. But now we're gonna go ahead and spray the car up and start scanning it. We don't have windows because they kind of just fell ... Time to start scanning."
- v_1645_19, 0-20 s: "So we've got the car scanned and now we're going to pull the front end off. Unbeknownst to me, the whole front end is like actually one piece because these are fake lines. The more you know."
- v_1659_53, 0-21 s: PBT/polycarbonate joke about the plastic part, "the French did not finish ... because they never do. The car's coming back together, we're coming apart."
- v_1712_33, 0-20 s: "So this is the car, fully taken apart, sides, skirts, front clam, bumper, everything. So we're going to go ahead and scan it as is. I'm going to have to capture the front clam mounting points right here."
- v_1729_10, 0-12 s: "So I have the full car scan in its current state. Since we're going way up on the wheel size, I am afraid the fender liners are gonna get in the way, so we're gonna go ahead and just pull those off now."
- v_1852_56, 0-26 s: "So bad news, I did not know that this is actually a first gen smart car. So now I'm developing a body kit for a car that you can't even get in the US ... this is a 2002 and we didn't get this car until like '07."
- v_1857_58, 0-24 s: about extra reinforcing bars in the door opening: "you can definitely tell that these welds are like not supposed to be here ... They reinforced it." (ASR garbled the first line, something like a "federalization for the US market car".)
- v_1633_51 is partly garbled ("Like all my other scanning projects, we're going to use a ...").

**Not for use:** v_1640_44, v_1722_25, v_1724_26 contain bystander conversation (the 1640_44 one includes the scanner's price, which must not be quoted, plus profanity and a slur around 52-56 s; 1722_25 has crude jokes; 1724_26 has talk about a games company and its projects). Do not let that audio into the reel. The narration clips also contain a few swear words (not counted).

Chronology implied by the narration: 4:20 car as received (missing doors) -> 4:32 panels back on -> 4:33-4:34 powdering -> 4:40-4:45 scanned
as assembled -> 4:45 front end comes off -> 4:59 front end off -> 5:12 "fully taken apart" -> 5:22-5:24 powdering and scanning the stripped car ->
5:29 "full car scan in its current state", fender liners next -> 6:52 and 6:57 shell with removed panels on the floor.
So **"assembled" = ~4:32-4:45, "stripped" = 5:12 onwards** (the exact match of the two STL states to these clock times is for the scan agent to confirm).

---

## v_1620_30 (4 20 30 PM): the car as received, walk-around, interior  (34.0 s, HLG, landscape)
Car state: **assembled bodywork, not powdered, but doors missing / door skin leaning against the car** (the narration says it is missing doors and door cards).
Sheets: `v_1620_30_00/01.jpg`.
- 0-2 s: low front 3/4 of the car, a black door panel leaning at left of frame; steady 2.0-2.9 s.
- 3-4 s whip pan (blurred); 5-6 s front again; 7-9 s passenger-side opening, no door, seat and empty window opening visible; 9-11 whip to shop.
- 11-15 s rear: soft-top rear window, red tail lamp, rear 3/4 view (steadier 13.5-14.5 s).
- 16-24 s walk to the open door side, then interior: seats, steering wheel, dirty dash, yellow cloth on the seat (blurred 17-22 s).
- 24-28 s turn back to the car front; **26.2-27.8 s: front 3/4 of the whole car, close, steady** (windscreen with a yellow sticker, headlamps, bonnet).
- 28-33 s whip around to the open door side, black door skin standing against the car (29-33 s).
Best spans: **26.2-27.8** (front 3/4, steady, whole car); 2.0-3.0 (front, steady-ish). Rest is handheld sweeping.
Usable for the hook/before: weakly, doors are off so it is not a clean "intact" car.
Problems: none seen close to lens (no faces; no plate on the car). Narration clips talks over everything.

## v_1632_12 (4 32 12 PM): panels back on, walk-around  (26.0 s, HLG, landscape)
Car state: **assembled** (door skins on, no window glass, soft top up, black unpowdered paint look).
Sheets: `v_1632_12_00/01.jpg`.
- **0.0-1.2 s: front 3/4 of the whole car, steady** (frame-diff lowest of the clip), a man in a black T-shirt walks away at right (back view).
- 1-4 s walk to the front/passenger side (head-on front at 2 s), 4-9 s side profile, door skin and wheel, cabin visible through empty window openings; a foot enters frame ~7 s.
- 9-14 s rear: man in black tee crosses and crouches by the rear, his face visible at mid distance around 10-11 s *(guess: face partly visible)*; rear of the car with a cracked soft-top rear window and a sticker.
- 15-23 s interior and fast pans, blurred.
- **24.2-25.8 s: rear of the car, steady, straight on**, same man at the right edge.
Best spans: **0.0-1.2** (assembled front 3/4), **24.2-25.8** (assembled rear); 4.5-8.0 (side walk-by, readable).
Problems: bystander at 9-14 s and 24-26 s (not close). Whole car is small in a 9:16 centre crop; use blurred fill or accept a crop.

## v_1633_51 (4 33 51 PM): powdering the front  (14.9 s, HLG, **rotation tag wrong, rotate 180 from raw**)
Car state: **assembled, front being powdered** (matte grey patches growing).
Sheets: `v_1633_51_00.jpg` (the sheet shows the sideways, tag-applied picture).
After the fix (upright landscape): POV from the sprayer's other hand, red cordless spray gun with a white cup.
- 0-1 s car front wide from ~3 m; 1-5 s gun swings in, windscreen/bonnet; 6-9 s close on windscreen and bonnet, spray mist visible at 8-9 s (washed-out frames); 10-14 s bumper close-ups with the gun in frame.
Best spans: 2.0-4.5 and 10.0-13.0 on paper. Low priority: the other powder clips (1634_19, 1634_51) are better and need no rotation fix.

## v_1634_19 (4 34 19 PM): powder around the whole car, arm POV  (28.7 s, HLG, landscape, -180 correct)
Car state: **assembled, being powdered**; the car goes from dark black/grey to light matte grey as it progresses.
This is an iPhone clip (not glasses): first-person view with the arm and red spray gun in frame, wide lens, *(guess)* phone held at chest or head height.
Sheets: `v_1634_19_00/01.jpg`; enlarged frames `frames/s1634_19.jpg` (7.5, 15, 21.5, 26 s).
- 0-5 s rear: tail lamp and rear bumper being sprayed, rear panel texture; 4-6 s rear quarter.
- 6-9 s side panel and wheel, mist visible from the nozzle; 9-13 s door and open window, cabin seat visible; 14-16 s front quarter, headlamp and bumper sprayed (frame 15 s: headlamp, black/grey transition on the wing).
- 17-19 s front bumper/bonnet; 19-23 s door aperture, seat visible through the empty window; 24-28 s rear quarter and door, spraying (frame 26 s: grey door, gun nozzle and mist).
Best spans: **6.0-8.8** (nozzle mist on door and wheel, in focus), **14.0-16.0** (front quarter with headlamp), 21.0-23.0 (spraying into the window opening), 0.0-2.5 (tail lamp/rear bumper for the "tail lamp" close-up in the pitch).
Problems: frame-diff is high throughout (hand-held, panning); take 1.5-2 s spans, not longer. No bystanders or plates seen. Usable shop sound (spray hiss, no speech).

## v_1634_51 (4 34 51 PM): powder, rear to front, true vertical  (10.8 s, HLG, 1080x1920 after rotation)
Car state: **assembled, mostly powdered** (matte grey).
Native vertical, no crop needed.
Sheets: `v_1634_51_00.jpg`.
- 0-3 s rear: tail lamp, soft-top rear window with two stickers (a "DRIFTER" film/brand sticker, third party), gun spraying the tail panel; 3-6 s passenger door and open window; 6-8 s turn to the front quarter; **8.2-10.8 s front of the car, straight on, car centred and small in frame** (garage door open behind).
Best spans: **8.5-10.8** (front elevation, centred, powdered), 0.0-2.5 (powdered tail lamp, the pitch's "tail lamp" shot).
1:1-cut candidate (assembled, front, powdered, native vertical, steady-ish: frame-diff 28-36).
Problems: none on faces/plates. Audio is clean spray noise, usable.

## v_1640_44 (4 40 44 PM): scanner on the bench, then scanner aimed around the shop  (68.8 s, glasses 3:4, SDR)
Car state: car mostly out of view (assembled, powdered, seen briefly at 34-36 s and below the scanner at 48-66 s).
Sheets: `v_1640_44_00/01/02.jpg`.
- 0-15.5 s: at the tool-chest bench. White handheld scanner on its desk stand, the filmmaker's hands hold/tap its screen, which shows a small 3D thing (red/dark, *guess: a red part or helmet*). Behind a glass window a man is visible at distance (0-3 s). A "EPSILON+" sign and a logo sticker sit on the chest. Steady (frame-diff 3-10 s).
- 15.5-21 s: whip to the bright roller door (overexposed 16 s, 21 s), a man in a light shirt standing arms folded in the doorway (face visible, about 4 m away, 17-20 s); 19 s back to bench.
- 22-33 s: alternating bench (hand on the scanner screen 22-25 s, 28-29 s, 31 s) and the doorway; two men facing the lens at about 3 m at 33 s.
- 34-36 s: car with powdered windscreen and the roof open, panning past the front wing (steady little).
- **37-66 s: scanner held out at arm's length, pointed at the ceiling and walls (the shop is being "scanned"), live screen visible the whole time.** 38-47 s screen shows a green rectangle on a grey camera view (frame 40 s: scanner dead centre, screen about 14% of frame width); 55-66 s the screen shows a red-and-white live image, turning to colour patches while it moves (frame 58 s: red surface, roof and scanner steady). Car roof and door visible below at 47-53 s.
- 67-68.8 s: two men stand facing the lens about 3 m away.
Best spans: **38.0-45.0** (scanner in frame with live green screen, steady, frame-diff ~10), 57.0-60.0 (red live image, clearest colour), 3.0-12.0 (hands and screen on the bench, steady).
Scanner screen legibility: the colours/shapes read (green block, red scan), but not any UI text; the screen is small. The clearer scanner screens are in v_1724_26 and v_1729_10.
Problems: bystander faces (man behind glass 0-3 s and 22-25 s; man at door 17-21, 26-27, 32-33 s; two men at 33 s and 67-68 s). Bench signage reads EPSILON+ (sister brand). Audio unusable (conversation, profanity). No readable plate; a white pickup and a yellow Corvette-like car sit outside the door (16-18, 26-27 s).

## v_1645_19 (4 45 19 PM): powdered front, headlamp and vent close-ups, the front end about to come off  (19.7 s, HLG, **rotation tag wrong, rotate 180 from raw**)
Car state: **assembled, powdered, front end still on.** Narration: the car is scanned, now the front end comes off.
Sheets: `v_1645_19_00.jpg` (sideways in the sheet because of the wrong tag). After fixing it is an upright landscape clip.
- 0-2 s: pan across the shop, a person in a light top and another in dark pass by.
- 2-4 s: approach to the car front (grey-black powder, a yellow sticker with characters on the windscreen, cream headlamp lenses).
- **4.5-9.5 s: close-ups of the powdered headlamp lens, the bonnet vent grille and the panel seam** (the pitch's "vent" shot; sharp on the lamp at 6-8 s).
- 9.5-11.5 s: a hand pulls at the seam between wing and front panel (the "fake line" the narrator mentions).
- 12-14 s: wobbly tilt back; **15.5-19 s front of the car from about 3 m, steady (frame-diff ~10-12 at 17.0-18.5 s), car centred**, a person at the left edge (back/side, face not visible).
Best spans: **6.2-8.4** (headlamp + vent close-up), **17.0-18.6** (steady front of the powdered car, assembled state, 1:1-cut candidate), 9.8-11.2 (hand at the seam).
Problems: rotation tag. No tail lamp here (the pitch's "tail lamp" is in v_1634_51/v_1634_19). Bystanders only as bodies.

## v_1659_53 (4 59 53 PM): front end off, a plastic panel up close, the stripped rear  (22.2 s, HLG, **rotation tag wrong, rotate 180 from raw**)
Car state: **panels coming off / mostly stripped** (front end just removed; rear bumper already gone).
Sheets: `v_1659_53_00.jpg` (sideways in the sheet).
- 0-1 s: hand lifting a black plastic part; 1-9 s: **extreme close-up of the inner face of a black plastic panel** with embossed `smart`, a part-number block ("... made in France"), the recycling mark `>PC/PBT<`, clip tabs and a round plug (steady for 1.5-3 s, in focus; 14-16 s the same embossing again, 'smart' lettering legible).
- 9-13 s: the hand carries or turns the panel (blurred); 16-17 s: panel edge and floor.
- **17.5-22 s: the car's rear from about 3 m, straight on:** soft-top rear window with two stickers, wiring loom and rear structure exposed, both tail lamps on, rear bumper missing with the exhaust in view; a man crouches at the right edge, back to camera (cap, light shirt; face not visible). Steadiest at **19.0-19.8 s** (frame-diff 17-23).
Best spans: **19.0-19.8** (dead-on rear of the stripped rear, steady, 1:1 candidate once the rotation is fixed), 1.5-3.2 (panel macro with legible 'smart' emboss), 14.0-15.5 (the 'smart' lettering).
Problems: rotation tag; the rear stickers (third-party) and the man at the edge.

## v_1712_33 (5 12 33 PM): the car "fully taken apart", walk-around  (22.4 s, HLG, landscape upright)
Car state: **stripped**: no doors (aluminium door-frame cage visible), front end and bumper off with the radiator, hoses and a tan crash board showing, rear panels off with the rear structure showing; soft top, windscreen, wheels still on.
Sheets: `v_1712_33_00.jpg`.
- 0-0.6 s: whole car, rear 3/4 from about 4 m, steady (frame-diff ~30), a person at the far left edge.
- 1-4 s: sweep around the rear wheel arch and the door-less side; 3-5 s side cage and open cabin; 4-9 s front, engine bay and the tan board (5-7 s the clearest, windscreen sticker visible); 9-10 s whip.
- 10-14 s: hand pointing at the cage and a connector at the pillar; 13-14 s close on the cage bars.
- 14-16 s: rear quarter, red tail lamp; **16-21 s: rear of the car straight on** (rear window with a cracked soft-top panel and sticker, bare rear structure), steadiest at 19.0-19.9 s.
Best spans: **4.9-6.8** (front end off, engine bay), 10.4-12.6 (hand and cage), 19.0-19.9 (rear), 0.0-0.6 (whole stripped car).
Problems: lots of whips (frame-diff peaks at 9-10 s and 13 s). The pitch calls this "car on the jack, wheels and panels coming off": **no jack and no panel removal in this clip**; it is the finished stripped state.

## v_1722_25 (5 22 25 PM): powdering the stripped car, glasses POV  (107 s, 3:4, SDR)
Car state: **partly stripped, being powdered**: front end off, doors off with the window glass removed, rear boot panel up/open.
Sheets: `v_1722_25_00` to `_04.jpg`.
- 0-3 s: bench, red spray gun, white scanner close to lens (blurred), man behind the glass window.
- 3-8 s: **rear boot/hatch panel lifted**, a hand pulls the soft-top rear panel up (3-5 s), blue carpet boot, red third brake lamp on the underside of the lid (5-7 s), blue jack stands; a man's legs at the right edge (3 s).
- 9 s: bench with EPSILON+ sign, scanner on the stand; 10-12 s door-less side of the car, interior; 13-16 s whips to the bright door and bench; scanner on its stand shows a green screen at 14 s.
- 17-23 s: powder spraying through the open door frame into the cabin (gun with red body and white cup in lower frame, mist visible 18-21 s), then the front wing and the exposed front end (22-23 s).
- 24-29 s: **front end stripped (engine bay, tan board), powdered front wing, spraying the windscreen area**; a man in a black tee stands beside the car with his face visible at about 2 m (26-27 s); a sticker with characters on the windscreen.
- 30-31 s hands at the door frame; **32-38 s the windscreen turns from clear to matte grey-white under the spray** (clear powder-doing-its-job shot); 38 s front straight on; 39-41 s doorway and a man with long hair at the far end.
- 42-47 s: rear quarter with a window glass held in the frame; 47-57 s close on the rear quarter panel and a hand holding the door mirror from behind; **1:00-1:08 the camera is a hand-span from a flat grey panel, nothing readable** (frame-diff 4-8, dead steady but empty).
- 1:09-1:11 door-frame cage; **1:12-1:19 the open boot with the red lamp, hatch lid up, rear of the stripped car**; 1:17-1:24 spraying the rear, gun in lower left; 1:25-1:27 a man with a bun hairstyle at the bench, face clear at 1-2 m; 1:28-1:35 hand lifts the lid, soft-top rear window with a cracked panel and the 'DRIFTER' sticker, gun spraying (1:33); 1:36-1:43 side and rear 3/4 of the stripped car, gun in lower right; 1:44-1:46 bench with the lit scanner on the stand, floor and a plastic jug.
Best spans: **18.2-21.6** (powder spray into the cabin through the door opening), **24.0-26.9** (spraying the exposed front end), **32.5-37.0** (windscreen going matte), **3.2-6.8** (boot lid lifted), **1:14.0-1:19.0** (open boot, rear of stripped car), 1:36.5-1:38.0 (stripped side 3/4).
Problems: bystander faces (man in black tee 26-27 s, 1:14-1:25 s; man with bun 1:25-1:27 s; man at doorway 16, 39-41 s); jokes in the audio, do not use sound; extreme close-up block 0:47-1:11 is dead footage; bench signage (EPSILON+).

## v_1724_26 (5 24 26 PM): scanning the stripped car, scanner screen in frame throughout  (125.3 s, 3:4, SDR)
Car state: **stripped** (door cage open, front clam off, rear structure bare, rear lid with a cracked soft-top window and sticker).
Sheets: `v_1724_26_00` to `_05.jpg`.
The scanner (white handheld, its colour screen faces the camera) sits in the lower third of the frame for most of the clip, so this is the pitch's "POV scanning, green live scan visible", **confirmed**.
- 0-9 s: rear of the car with the scanner at the bottom, **green block on the screen growing, with a grey camera view and small UI text** (frames 3-5, 7 s); a man in black (hair in a bun) stands at the back looking at his phone, face visible at about 2 m (3-4, 9 s).
- 6-8 s swing to ceiling lights; 7-8 s the scanner handle/dock with a hand grabbing it.
- **10.3-13.5 s: rear of the car (cracked rear window, DRIFTER sticker, tyre rack behind), scanner screen large at lower left showing green scan plus the camera view** (frame-diff 7-16, steadiest long window in the clip; screen is about 40% of frame width: the best scanner-screen span).
- 14-19 s: hand lifts the scanner away; man in black tee at the right with his phone (face about 1.5 m at 16-17 s); a hand shows an orange-cased phone to the camera (17-19 s, screen unreadable).
- 20-23 s: rear 3/4 and then door-side of the stripped car; 24-29 s car side/rear with two bystanders (man in black tee, man in white tee with long hair; faces about 3 m).
- 30-40 s: scanner pointed at the ceiling and the roller door, screen shows green patches over grey (36-37 s, screen bottom-left, frame-diff 11); 40-47 s car side/front-left and the bench.
- 48-50 s: **rear straight on, bare structure and tape**, scanner at the bottom; 51-58 s floor: tail lamps, panels and mounting parts on the ground (53-57 s), operator's grey shoes, scanner in bottom left with green screen.
- 59-71 s: side of the stripped car (door cage, seats), scanner bottom frame, green patch on screen (1:04-1:11).
- **1:14-1:21: scanner held in the hand pointing at the floor, screen big in the lower centre with green and red regions** (frame-diff 8-18; screen legible, floor and jack stands behind, operator's feet in view).
- 1:23-1:28 car rear then ceiling; **1:28-1:35 front-left of the stripped car, windscreen, radiator and engine bay, scanner screen at bottom right (green)**; 1:34-1:35 two bystanders at the doorway (faces at 3-4 m).
- **1:36.5-1:39.5: side of the stripped car with the door cage open and the seat inside, scanner screen bottom right with green patch** (frame-diff 17-21; whole-car simple angle).
- 1:41-1:43 engine bay; 1:43-1:45 a black bumper/wing on the floor; **1:46-1:50 front of the stripped car straight on, board visible, windscreen, scanner at bottom** (frame-diff 18-23); 1:50-1:55 shelf, bystander; 1:56-1:58 front again.
- 1:57-2:05 floor: black panel on the ground, operator's grey shoes, scanner at lower right.
Best spans: **10.3-13.5** (scanner screen, large), **1:14.0-1:21.0** (screen, big, steady), **1:36.5-1:39.5** (stripped side with screen), **1:46.5-1:49.5** (stripped front with screen), 0.0-6.0 (scanner screen with rear of car).
Problems: bystander faces and phones (3, 9, 16-17, 24-29 s, 1:34-1:35 s); audio unusable (conversation about a games company, profanity); long stretches of ceiling.

## v_1728_34 (5 28 34 PM): fragment  (0.9 s, 3:4, SDR)
Bench: scanner on its stand, red spray gun, water bottle; dark, off-balance exposure and nearly silent (-45.8 dB). **Unusable** (0.9 s, no action).

## v_1729_10 (5 29 10 PM): "full car scan in its current state"  (11.6 s, HLG, landscape, -180 correct)
Car state: **stripped** (front end off with the engine bay open, door cage open, wheels and soft top on, windscreen powdered).
Sheets: `v_1729_10_00.jpg`; enlarged frames `frames/t1.jpg` (0.1, 0.9 s, and 1852_56 at 26 s).
- **0.0-0.4 s: clean front 3/4 of the whole stripped car, ~4 m, steady, simple angle** (frame 0.1 s). Window is short (the scanner then comes into frame).
- **~0.5-1.7 s: the scanner is raised into frame, screen towards camera, showing a "Projects" list with three thumbnails of the scanned car** (frame 0.9 s; UI text is small but the layout and the thumbnails read well in 1080p).
- 2-5 s: walk toward the car front (steady 1.5-2.5 s), then the sill and wheel arch; 5-8 s door cage and wheel; 8-11 s a man sits/lies on the floor at the rear (legs, back; face not visible), rear 3/4 of the car at 10.5-11.5 s.
Best spans: **0.0-0.4** (whole stripped car, 1:1 candidate), **0.6-1.6** (scanner screen with project thumbnails, a clear "result on the scanner" beat), 10.5-11.5 (rear 3/4).
Problems: the opening is short; the 1:1 window is only ~0.4 s unless the first frame is held. A white pickup is parked outside (plate tiny and not legible at 1080p in frame 0.1).

## v_1852_56 (6 52 56 PM): the stripped shell and the panels on the floor  (27.4 s, HLG, landscape upright)
Car state: **stripped shell**, with removed panels laid out on the floor (the pitch's hook, **confirmed**).
Sheets: `v_1852_56_00/01.jpg`; enlarged frames `frames/v_1852_56_0.5.jpg`, `_15.jpg`, `_21.jpg`, `_6` and `_25` (in `frames/p_*.jpg`), `_26` (in `t1.jpg`).
- **0.0-1.2 s: the black front bumper cover and a side skirt on the floor, the stripped car at the top right** (frame-diff 21-22, steady).
- 1.2-5.5 s: shaky pan (bumper again, black tool cart, the car small and straight on at 2 s; the narrator's hand points at the bumper 3.5-4.5 s, frame-diff 50-125).
- 5.5-8 s: approach to the car front: front end off, a floor jack under the front and the tan crash board *(guess: the front is supported on the jack)*, 8-9 s engine bay close.
- 9-12 s side: door cage and seat, wheel; 12-13 s rear wheel.
- **13-19 s: rear 3/4 of the whole stripped car from about 4 m, steady at 15.0-16.0 s** (frame 15 s: soft top and rear window, rear structure bare, exhaust and bumper missing, tail lamp on, tyre rack and shop behind).
- **19.6-22.4 s: panels on the floor: rear bumper cover, side sills, wing pieces, tail lamps (two red), clear headlamp lenses at the top** (frame 21 s; steady at 20.8-21.6 s, frame-diff 27-31).
- 22.5-25 s: whip back to the car; **25.3-27.4 s: close 3/4 of the stripped shell, door cage, rear quarter with the soft-top stub** (steadiest, frame-diff 10-13; the car fills the right 80% of frame).
Best spans: **20.8-21.7** (panels on the floor, the hook), **0.0-1.1** (bumper on the floor), **15.0-16.0** (whole stripped car, rear 3/4, 1:1 candidate), **25.3-27.4** (very steady close shell, 1:1 candidate), 6.0-8.0 (car on the jack).
Problems: shaky 1.2-5.5 s; white vehicles in the doorway at 20-22 s have visible plates at top right (small; blur or avoid). Narration is quotable but not needed. In 9:16, a centre crop at 21 s keeps the panels but at 0.5 s loses the stripped car at the right.

## v_1857_58 (6 57 58 PM): hand showing the structure of the bare shell  (24.1 s, HLG, landscape upright)
Car state: **stripped**; the door opening shows the aluminium cage bars.
Sheets: `v_1857_58_00.jpg`.
- **0.2-8 s: hand and forearm point to the diagonal bars and the window regulator in the door opening**, close, in focus, then a hand pulls at a bar (the pitch's "hand pointing at the structure", **confirmed**); a sticker on the cage is visible.
- 8.5-10 s: whip along the car side, seats beyond; 11-12 s cage and seat; 13-15 s front of the stripped car (engine bay, board, windscreen sticker).
- 16-21 s: close on the lattice bars from the cabin side, a hand touches a diagonal bar at 19-20 s; **22-24.1 s: pull back to a steady side profile of the stripped car** (cage rail, seats, wheel at the right).
Best spans: **0.3-4.8** (pointing at the cage, clear, hand and bars), 11.0-12.5 (cage plus seat), 22.0-24.0 (side profile of the stripped car, possible 1:1 candidate; I did not measure its steadiness).
Problems: none (no faces, no plates).

---

## Where the car is whole, steady and simple: candidate 1:1 cut points

| state | clip | time | what | notes |
|---|---|---|---|---|
| assembled (panels on, unpowdered) | v_1632_12 | 0.0-1.2 s | front 3/4, whole car, steady | man walking away at right edge (back only); landscape |
| assembled | v_1620_30 | 26.2-27.8 s | front 3/4, near, steady | doors missing, so not a perfect "intact" car |
| assembled, powdered, front end still on | v_1645_19 | 17.0-18.6 s | front of the car at ~3 m, steady | **needs the 180 degree rotation fix**; people at the left edge |
| assembled, powdered | v_1634_51 | 8.5-10.8 s | front elevation, car centred, native vertical | car is small in frame; frame-diff 28-36 |
| stripped | v_1729_10 | 0.0-0.4 s | front 3/4, whole car, clean | very short window; scanner enters after |
| stripped | v_1852_56 | 15.0-16.0 s | rear 3/4, whole car | steady, reads as a simple angle |
| stripped | v_1852_56 | 25.3-27.4 s | close 3/4 of the shell, door cage | steadiest; car cut at the left |
| stripped (rear) | v_1659_53 | 19.0-19.8 s | dead-on rear | needs the rotation fix; man crouched at the right edge |
| stripped (3:4, glasses) | v_1724_26 | 1:36.5-1:39.5 | side of the car, cage open, scanner screen in the corner | steady enough; punch-in friendly |
| stripped (3:4, glasses) | v_1724_26 | 1:46.5-1:49.5 | front of the car straight on, scanner screen in the corner | moderate motion |

**Caveat that affects every 1:1 candidate from the 1080p iPhone clips:** a centre 9:16 crop of a 1920x1080 frame is only 608 px wide (32% of the width), and the whole car (about 50-60% of the landscape width) does not fit in it without cutting the car. Those clips need blurred fill (or a letterboxed placement with the scan matched to the smaller car), or a punch-in that keeps only part of the car. Only `v_1634_51` (native vertical) and the 3:4 glasses clips keep the whole car inside a plain crop. I did not render the 16:9 options.

## Reframing the 3:4 glasses clips to 9:16 (checked on frames: `frames/cmp_all.png`)
| clip | source | 9:16 crop at full height | lost left/right | scale to 1080x1920 |
|---|---|---|---|---|
| v_1640_44, v_1722_25 | 1504x2000 | 1125x2000 | 379 px total (25.2%), ~189 px (12.6%) each side | 0.96x (slight downscale) |
| v_1724_26 | 1328x1760 | 990x1760 | 338 px total (25.5%), ~169 px (12.7%) each side | 1.09x (slight upscale) |
Blurred fill would fit the whole 3:4 frame at 1080 wide (1080x1440, 240 px of blurred bars top and bottom), so the picture shrinks to 75% of the screen height.
I compared both on frames from v_1724_26 (12 s), v_1722_25 (19 s) and v_1640_44 (5 s, 44 s). **The centre crop (punch-in) is better in every case**: the subject (scanner with its screen, the car, the gun, the bench) stays centred, the picture fills the screen with no bars, and nothing important is lost. What the crop loses: in v_1724_26 the left edge of the scanner housing and the left tyre rack (the screen stays inside the crop; shift the crop window about 5% to the left on the scanner-screen spans to keep the whole scanner); in v_1722_25 the doorframe edges and the gun on the right at some moments; in v_1640_44 the water bottle at the left and the red item at the right of the bench. Blurred fill looks cheaper and gives no extra content, so use it only if a span needs the full width.
(The 3:4 glasses footage was shot at ~67 degrees *(Lola note)*, so cropping to 75% of the width is a small step; it is not as drastic as cropping 16:9 footage.)

## Unusable material and risks
- `v_1728_34`: 0.9 s fragment, dark, silent.
- Shake: v_1620_30 (whole clip bar 2-3 s, 13.5-14.5 s, 26.2-27.8 s), v_1712_33 (9-10 s, 13 s), v_1852_56 (1.2-5.5 s, 22.5-25 s), v_1634_19 and v_1633_51 (spray POV, always moving; use 1.5-2 s spans).
- Dead footage: v_1722_25 0:47-1:11 (a flat panel at 10 cm, nothing readable), v_1724_26 ceiling and wall stretches (6-8 s, 30-40 s, 1:24-1:27).
- Bystander faces: v_1640_44 (many, incl. two men facing the lens at 33 s and 67-68 s), v_1722_25 (26-27 s, 1:14-1:27 s), v_1724_26 (3-4, 9, 16-17, 24-29 s, 1:34-1:35 s), v_1632_12 (10-11 s, mid distance). None right on the lens except the 1.5-2 m shots in v_1722_25 and v_1724_26.
- Licence plates / VIN: **no plate or VIN seen on the Smart car**. A white pickup parked outside the roller door shows a plate at small size in v_1852_56 (20-22 s, top right) and possibly v_1729_10; cut around it or blur it. The yellow sticker on the Smart's windscreen has characters on it (an import or registration sticker, *guess*), not a plate.
- Brand and third-party marks in frame: "EPSILON+" sign and a second logo sticker on the bench chest (v_1640_44, v_1722_25), a "DRIFTER" sticker on the rear window (v_1634_51, v_1722_25, v_1724_26, v_1659_53, v_1632_12, v_1712_33), DeWalt vacuum. Epsilon+ is the sister brand, not Illumaesthetic; avoid the bench shots for the Illumaesthetic reel unless that is intended.
- Pocket footage: none found. The nearest to it is the hand-span panel block in v_1722_25.
- Audio: bystander talk and profanity in v_1640_44, v_1722_25, v_1724_26 (do not use); the scanner's price is spoken in v_1640_44 (0-7 s), do not put it in the reel.
- Rotation tags on v_1633_51, v_1645_19, v_1659_53 (see top).

## Scanner screen: when it is clearly legible
1. **v_1724_26 10.3-13.5 s**: screen large (about 40% of frame width), a green patch over a grey camera view with small UI text, car rear behind it. Best.
2. **v_1724_26 1:14-1:21**: scanner in hand pointed at the floor, screen big with green and red regions; also 1:28-1:35 and 1:36.5-1:39.5 with the stripped car behind.
3. **v_1729_10 ~0.6-1.6 s**: scanner raised to camera, a "Projects" list with three car thumbnails.
4. v_1640_44 38-45 s (green block) and 57-60 s (red live image): readable as colour and shape, small (about 14% of frame width).
5. v_1722_25 14 s, v_1728_34, v_1640_44 0-15 s: the scanner sits on its desk stand, screen small.
No frame shows legible numbers or specs on the scanner screen that I would quote; do not put any text from the screen on the reel.

## Story coverage (pitch S3 shots 1-10)
| # | pitch picture | pitch source | verdict |
|---|---|---|---|
| 1 | Stripped shell, panels on the floor (hook) | 6 52 56 PM | **Confirmed**: v_1852_56 20.8-21.7 s (panels on floor, steady, fits a centre crop) and 0.0-1.1 s (bumper on floor, shell behind it at the right); 25.3-27.4 s for the shell itself. |
| 2 | Same car intact, walk-around | 4 20 30 PM | **Different clip better**: in v_1620_30 the doors are missing and a door leans on the car. Use v_1632_12 (panels back on; 0.0-1.2 front, 4.5-8.0 side, 24.2-25.8 rear) for "intact"; keep v_1620_30 26.2-27.8 s as the "before" front view. |
| 3 | POV: powder from the red spray gun | 4 34 19 PM | **Confirmed**, but it is iPhone arm-POV, not glasses; use 6.0-8.8 s, 14.0-16.0 s. v_1634_51 (native vertical, 8.5-10.8 s front, 0-2.5 s rear) is an equally good, easier-to-reframe alternative; both give usable sound. |
| 4 | POV: handheld scanner, live scan filling in on its screen | 4 40 44 PM | **Partly**: v_1640_44 38-45 s shows the scanner with a live green screen, but small and in a 69 s clip full of bystanders. A better screen: v_1724_26 10.3-13.5 s or 1:14-1:21, or v_1729_10 0.6-1.6 s ("Projects" with car thumbnails). |
| 5 | Powdered tail lamp and vent close-ups | 4 45 19 PM | **Half**: v_1645_19 has the powdered headlamp and bonnet vent (6.2-8.4 s) and the hand at the panel seam (9.8-11.2 s), **no tail lamp**; the tail lamp being powdered is in v_1634_51 0.0-2.5 s and v_1634_19 0-2.5 s. v_1645_19 needs the rotation fix. |
| 6 | Car on the jack, wheels and panels coming off | 5 12 33 PM | **Different clip needed**: v_1712_33 is the finished stripped car (no jack, no removal on camera). Panels coming off: v_1645_19 9.8-11.2 s (hand at the seam) and v_1659_53 0-1 s and 9-13 s (the removed front-end plastic in hand, panel macro 1.5-3.2 s); jack under the front: v_1852_56 6.0-8.0 s *(guess)*; v_1712_33 4.9-6.8 s for the opened front. No shot shows a large panel leaving the car in one take. |
| 7 | POV scanning with the front clam off, green live scan visible | 5 24 26 PM | **Confirmed**: v_1724_26 (front end off at 40-50 s, 1:28-1:35 s and 1:46-1:50 s with the screen in the lower corner; best screen 10.3-13.5 s). Not a single frame has "clam off" plus a fully legible screen; 1:28-1:35 and 1:46.5-1:49.5 are the best compromise. |
| 8 | Scan renders | new renders | Not footage; the 1:1 cut candidates are listed above (assembled: v_1645_19 17.0-18.6 s, v_1632_12 0.0-1.2 s, v_1634_51 8.5-10.8 s; stripped: v_1729_10 0.0-0.4 s, v_1852_56 15.0-16.0 s and 25.3-27.4 s). |
| 9 | Hand pointing at the structure on the bare shell | 6 57 58 PM | **Confirmed**: v_1857_58 0.3-4.8 s. |
| 10 | Logo card | logo card | n/a |

Better moments the pitch missed:
- **v_1729_10 0.0-1.6 s**: whole stripped car (steady), then the scanner raised with a readable "Projects" screen. A natural bridge from "the car" to "the scan".
- **v_1722_25 32.5-37.0 s**: windscreen turning matte under the powder, and **18.2-21.6 s** powder through the door opening of the stripped car: the clearest "why we powder" shots, with the gun's mist visible.
- **v_1722_25 1:14-1:19 s**: open boot with red lamp, stripped rear.
- **v_1659_53 1.5-3.2 s and 14-15.5 s**: macro of the inside of a removed panel with the embossed `smart` lettering and the recycling mark; a strong detail cutaway.
- **v_1852_56 25.3-27.4 s** and **v_1857_58 22.0-24.0 s**: steady shots of the bare shell for the "skeleton" idea (title says "down to its skeleton").
- v_1724_26 51-58 s: removed tail lamps and panels laid on the floor next to the scanner screen (frame 53-57 s), a second "panels on the floor" option with the scanner in frame.
- The narration is clean and quotable in v_1620_30, v_1729_10, v_1852_56 and v_1857_58 (for captions or VO), but the brief says no VO and the swearing makes most of it unusable as-is.

Not found anywhere in the footage: a panel physically coming off in one take, a shot of the Smart on a jack with a wheel off, the front clamshell lifted off as a unit, and any tail-lamp close-up in the pitch's named clip.
