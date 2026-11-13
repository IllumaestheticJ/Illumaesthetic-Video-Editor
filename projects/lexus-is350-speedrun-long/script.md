# L1 script: "How fast can we 3D-scan an entire car?" (Lexus IS350 speed run)

Script v1, 2026-11-13. Written by the script agent. The edit as data is in `edl.json` (same ids, same times, generated from the same source).
Every number on screen in this video comes from one of four sources, cited where it is used: **the owner** (32 min elapsed, 20 min without the crash),
**the STL header** (24,999,992 triangles), **a time said aloud** (transcript timestamp), or **a stopwatch legible in frame** (clip @ seconds).

## Titles (5)

1. **We Bet 15 Minutes to 3D-Scan an Entire Car. Then the Scanner Crashed.** (chosen)
2. How Fast Can We 3D-Scan an Entire Car? (32 Minutes, 1 Crash)
3. Can We 3D-Scan a Whole Car in 15 Minutes?
4. 3D-Scanning a Lexus IS350 Against the Clock: 32 Minutes, 2 Timers
5. One Car, One Stopwatch, 24,999,992 Triangles

Why 1: the story is the bet and the crash, and the 15 is said by the host on camera (541 [00:26.3]). The on-screen title card (G01) keeps the
approved question, "How fast can we 3D-scan an entire car?". Numbers used in the titles: 15 (said), 32 (owner), 2 timers (both on camera),
24,999,992 (STL header).

## Logline

The host bets he can 3D-scan a whole Lexus IS350 in 15 minutes, "less than the length of a YouTube video". Five minutes in, the scanner crashes.
After a reboot, a second timer, and a lot of lying on the floor, the result is 32 minutes from "go" and 20 minutes on the timer restarted after
the crash. The proof is a 24,999,992-triangle scan.

## How this video works without narration

- About 4.9 min of words exist in 28 min of footage. The story runs on four things: **the host's real lines** (captioned), **the stopwatch**
  in the HUD rail (always on), **short black cards** (one idea each, 1.5-4.4 s), and **music** that follows the game logic: start, crash, continue, finish.
- **Layout (lead's decision):** IRL plays in the top 1920x920. A 160 px black **HUD rail** along the bottom holds CLOCK 1 (left), TIMER 2 (right of it, from the reboot on),
  captions (centre) and the chapter name (right). No text ever sits on IRL picture. Cards are full frame on black, and the rail stays on them.
  Scan renders are full frame 1920x1080. On scan inserts the rail stays as an overlay with a transparent background, so the 3D agent frames the car above y = 900.
  The rail is hidden on the title (E04), on the result sequence (E68-E70) and on the end card.
- **Two clocks, both real.** Reading the footage frame by frame turned up 19 legible stopwatch faces plus one minutes-only reading (list below). CLOCK 1 is the phone stopwatch started on "go".
  TIMER 2 is the watch stopwatch restarted after the reboot. In every IRL shot the rail shows the true value for that shot's own frames.
  Because the edit compresses the run, the clock jumps forward at cuts. Animate each jump as an 8-frame digit roll, and never let the clock run backwards.
  Format MM:SS (truncated like a stopwatch, no hundredths).
- **Captions** are verbatim from the large-v3 word times (`/home/user/media/work/is350-long/transcripts/FX305xx.json`), shown only during sync,
  in the rail, at most 2 lines of 42 characters. A spoken product name stays in a caption only if it is in a used span. None of the spans in the body contains one.

### Clock model (for the graphics agent)

| clock | legible readings in frame (clip @ s = value) | said aloud | rule |
|---|---|---|---|
| CLOCK 1 (phone, from "go") | 541@72 00:00.00 · 541@75.0 00:00.43 · 541@192 01:57.46 · 541@298 03:43.44 · 541@300 03:45.43 · 541@372 04:57.46 (analog face) · 541@374 04:59.52 · 541@404 05:29.46 · 542@24 12:20.75 · 544@45 17:53.38 (lock screen) · 546@0 "21:--" (minutes only) | "Five minutes on the dot" 541 [06:11.5]; "32 minutes" 553 [00:14.5] | 541: clip t − 74.6 s. 542: t + 716.75. 544: t + 1028.38. **After 544 nothing is legible**, so CLOCK 1 shows "running" with no digits until it freezes at "32 MIN" (owner). |
| TIMER 2 (watch, after reboot) | 542@16 00:03.00 · 544@30 05:28.64 · 545@56 08:32.23 (stopped) · 546@5 08:46.40 · 546@6 08:47.40 · 547@66 11:17.36 · 548@7 13:05.01 · 551@30 15:31.30 · 553@9 20:24.95 | "8 minutes and 32 seconds" 545 [01:01.5]; "20 minutes" 553 [00:09.7] | Starts at 542 t = 13.0 ("Now." 13.53). Paused at 08:32 during the 545 review (show a pause glyph, G07). From 546 on, value = camera wall-clock − 18:22:21.7. This agrees with all five faces from 546 to 553 to within 0.4 s. 549, 550 and 552 have no face, so their values are **derived** from that clock (marked in the EDL). Frozen at 20:24 after "Time.", then "20 MIN" (owner). |

The one interpolated span is the reboot card E27: CLOCK 1 fast-forwards from 05:49 to 11:56. That lies between legible 05:29.46 (541@404) and 12:20.75 (542@24),
and the card shows a ">>" glyph. The cards and scan inserts in between hold the last value.
Owner's official numbers on screen: **CLOCK 1 · FROM "GO" · 32 MIN** and **TIMER 2 · RESTARTED AFTER THE CRASH · 20 MIN**. We do not explain the 12-minute gap between them (see "For the owner").

## Run order at a glance

| # | section | time | dur | purpose |
|---|---|---|---|---|
| 1 | Cold open | 0:00-0:06.6 | 6.6 s | Hook: a guess, the crash, a facepalm |
| 2 | Title | 0:06.6-0:12.6 | 6.0 s | Scan hero + the question |
| 3 | The bet | 0:12.6-0:22.0 | 9.4 s | Predictions; the host bets 15 |
| 4 | Go: spray + first pass | 0:22.0-1:07.7 | 45.7 s | Clock starts; powder; first scanning; roof insert |
| 5 | The crash | 1:07.7-1:31.2 | 23.5 s | The turn: "It just crashed"; clock 1 keeps running |
| 6 | Try again | 1:31.2-2:43.6 | 72.4 s | Reboot, TIMER 2, rear 1:1 cut, exterior done, review |
| 7 | The hard parts | 2:43.6-3:43.4 | 59.8 s | Jacking, arches, wheels, lying on the floor; wheel + sill inserts |
| 8 | Time | 3:43.4-4:17.8 | 34.4 s | "Time. 20 minutes. Done." Scoreboard, bet result, walk-out, front 1:1 cut |
| 9 | The scan | 4:17.8-4:36.8 | 19.0 s | Full car, 24,999,992 triangles, reflector in/out |
| 10 | CONCLUSION (conclusion agent) | 4:36.8-5:04.8 | 28 s | Answer the question on camera |
| 11 | End card | 5:04.8-5:09.8 | 5 s | Logo + CTA |
| | **Total** | | **5:09.8** | target 5:00-6:30, kept tight |

Seconds by kind: IRL with sync speech 124.0 s, plus 4.4 s of sync audio under a card (E62), so **128.4 s of sync**. IRL music-only or room tone: **92.7 s**.
Scan renders: **46.5 s** (8-9 shots). Black cards: **18.6 s** (4.4 s of it carries sync audio). Conclusion slot: 28 s (mostly sync, content set by the conclusion agent).

## Music map (for the music agent; times are this script's timeline)

| span | feel | hard points |
|---|---|---|
| 0:00-0:06.6 | cold-open sting, punchy | cut to title on a downbeat |
| 0:06.6-0:12.6 | title hit | first frame of E04 on a hit |
| 0:12.6-0:22.0 | playful "character select" groove, light | ducked under the three answers |
| 0:22.0-1:07.7 | **drop on "go"** (E09, src 73.78 = timeline ~0:24.5), driving | cuts on accents |
| 1:07.7-1:18.6 | same groove continues under "Time check" | **music cuts dead on "crashed"** (E22 src 379.5 = ~1:18.2) |
| 1:18.2-1:43.3 | room tone; E27 a low "loading" pad | silence makes the crash land |
| 1:43.3 | **music back in on "Now."** (E29 src 13.53 = ~1:42.5) | a "continue?" restart |
| 1:43-3:43 | build; highest energy in the hard parts | E60 to E61 cut on a bar line |
| 3:43.4 | **stop / sting on "Time."** (E61 src 7.33 = ~3:43.9) | |
| 3:50-4:37 | victory / resolve, calmer under the result | 1:1 cuts E66 to E67 on a kick |
| 4:37-5:10 | under the conclusion, out on the end card | |

Editor: timeline times are pre-beat-snap. Snap each cut to the nearest accent within ±0.15 s. Move music-only shots first, and never cut inside a sync word.
The two match-cut `src_out` values are fixed (move `src_in`).

## Scan shots needed (3D agent; `scan_shots.md` did not exist when this was written, so the ids are placeholders)

| id | event | dur | tied to | note |
|---|---|---|---|---|
| SC_TITLE | E04 | 6.0 | title | whole car hero; leave the lower third clean for G01 |
| SC_INS_ROOF | E20 | 3.0 | roof sprayed in E19 (541 307-311 s) | roof + rear glass, raking light |
| SC_MATCH_REAR | E33 | 4.5 | FX30542 @47.339 s 1:1 | existing solve |
| SC_INS_CABIN | E41 | 3.0 | "That's the full interior" 545 [01:55.2] | **conditional**: only if the STL holds cabin geometry |
| SC_INS_WHEEL | E48 | 3.0 | front arch sprayed/scanned, 547 36-58 s | front wheel only (rear well is ragged) |
| SC_INS_SILL | E57 | 3.0 | lying under the car, 551 84-90 s | sill from low; no underside claim without data |
| SC_MATCH_FRONT | E67 | 5.0 | FX30554 @11.011 s 1:1 | existing solve |
| SC_RES_FULL | E68 | 7.0 | result | slow continuous move, not a turntable (lessons: rotations wasted) |
| SC_RES_MESH | E69 | 5.0 | result | triangles visible; clean black lower-left for G11 |
| SC_RES_REFLECTOR | E70 | 7.0 | result | reflector in place, then removed; pocket small, no push-in |
| (stills) | thumbnail / end card | - | - | not in the timeline |

Not used: SC_INS_FRONT and SC_INS_REAR. The front is reserved for the walk-out 1:1 cut and the rear for the FX30542 1:1 cut, and the house rule says each part of the car
appears in one continuous sequence only. If the 3D agent has already rendered them, they are spares. Rear appears twice by design (the 1:1 cut at 1:53 and the reflector result at 4:30).
Run `python -m ive director` on the cut and say in `direction.md` why the rear appears twice.

## Sections

### 1. Cold open (0:00-0:06.6, 6.6 s)

**Purpose:** hook within 15 s: a guess, the disaster, a facepalm, then the title. Nothing gets explained yet.
The crash appears here as a flash-forward. E02 is the line *after* "It just crashed", and the body (E22) stops on "It just crashed", so no frame plays twice.
The facepalm (E03) comes from the reboot clip, and the body jumps over it (E28 to E29).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E01 | 0:00.00-0:02.15 | FX30541 0.80-2.950 | Host off-camera asks; crew member (dark tee) answers to camera, smiling | "How long do you think it's gonna take?" / "Two hours." [541 [00:00.9]-[00:02.8]] | C1 00:00-00:00; (none) | RAIL_CAP | - |
| E02 | 0:02.15-0:04.45 | FX30541 380.55-382.850 | Host laughing, scanner held up over his head (crash moment) | "It's never crashed on me before." [541 [06:20.8]-[06:22.7]] | C1 05:05-05:08; (none) | RAIL_CAP | background red car plate behind the host (541 ~344-384 s) - blur if legible at 1080p |
| E03 | 0:04.45-0:06.60 | FX30542 2.55-4.700 | Host, hands over his face (after the reboot decision) | music only | C1 11:59-12:01; (none) | - | - |


### 2. Title (0:06.6-0:12.6, 6.0 s)

**Purpose:** the question, over the finished scan, so the payoff is visible from the start.
G01 on the scan render: **HOW FAST CAN WE 3D-SCAN AN ENTIRE CAR?** / sub **LEXUS IS350 · ONE CAR · ONE STOPWATCH**.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E04 | 0:06.60-0:12.60 | SC_TITLE (6.0 s) | Title hero: whole car, satin silver on black, slow push | music only | hidden; (none) | G01 | plate flattened in render (scan agent) |


### 3. The bet (0:12.6-0:22.0, 9.4 s)

**Purpose:** set the stakes with real predictions. A tally builds in the rail (G02: 2 HR, 30 MIN, 15 MIN). "2 HR" was heard in the cold open (541 [00:02.4]),
and the host's 15 is highlighted as THE BET.
Who says which (checked in frames): "Two hours" = crew member in a dark tee (takes 1 and 2); "Maybe 30 minutes" = crew member in a black polo with a lanyard;
"15 minutes" = the host (Berkeley tee). G03 card: **THE BET: 15 MINUTES** / **"LESS THAN THE LENGTH OF A YOUTUBE VIDEO"** (541 [00:26.3]).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E05 | 0:12.60-0:14.55 | FX30541 12.15-14.100 | Host to camera with the crew member in black polo beside him | "How long do you think it'll take to scan this car?" [541 [00:12.2]] | C1 00:00-00:00; THE BET | RAIL_CAP, G02 | - |
| E06 | 0:14.55-0:15.65 | FX30541 21.90-23.000 | Crew member in black polo + lanyard, to camera | "Maybe 30 minutes." [541 [00:22.1]] | C1 00:00-00:00; THE BET | RAIL_CAP, G02 | - |
| E07 | 0:15.65-0:19.50 | FX30541 26.15-30.000 | Host (Berkeley tee) to camera, grinning | "I think I can do it in less than the length of a YouTube video. 15 minutes." [541 [00:26.3]] | C1 00:00-00:00; THE BET | RAIL_CAP, G02 | - |
| E08 | 0:19.50-0:22.00 | gfx:G03 (2.5 s) | Card on black: the bet | music only | hold the previous event's last value; THE BET | G03 | - |


### 4. Go: spray + first pass (0:22.0-1:07.7, 45.7 s)

**Purpose:** the clock starts, and we learn the process from the pictures: powder first, then the scanner. The clock visibly runs.
Phone faces in E16 and E18 match the rail. G04 card: **STEP 1: SPRAY** / **A TEMPORARY MATTE COAT SO THE SCANNER CAN READ SHINY PAINT AND GLASS**.
Scan insert: **SC_INS_ROOF** right after the roof is sprayed (E19). E21 shows the team checking coverage ("not fully covered"), which sets up the time pressure.
Do not use: 541 40-68 s (phone with alarms and a joke timer), 87.9-92.3 s ("Artec ad and an AESUB ad"), 242-248 s ("with the Artec Leo, that's a thing of the past"),
or 203-222 s (chatter about a third party).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E09 | 0:22.00-0:27.30 | FX30541 71.30-76.600 | Phone stopwatch at 00:00.00 in hand, start pressed; car behind | "Three, two, one, go." [541 [01:11.6]-[01:14]] | C1 00:00-00:02; SPRAY + FIRST PASS | RAIL_CAP, G14 | - |
| E10 | 0:27.30-0:31.00 | FX30541 77.30-81.000 | Hands at the bench: spray bottle, scanner on its stand, spray gun | "I'm so confident in my ability, I'm not gonna rush. I gotta take my time." [541 [01:17.6]] | C1 00:02-00:06; SPRAY + FIRST PASS | RAIL_CAP | - |
| E11 | 0:31.00-0:32.50 | gfx:G04 (1.5 s) | Card on black: step 1 | music only | CLOCK 1 holds its last value (00:06); SPRAY + FIRST PASS | G04 | - |
| E12 | 0:32.50-0:36.10 | FX30541 103.00-106.600 | Host sprays the front bumper/grille | music only | C1 00:28-00:32; SPRAY + FIRST PASS | - | front plate (9JTY488) legible - track and blur |
| E13 | 0:36.10-0:40.90 | FX30541 106.70-111.500 | Spraying along the side | "Then when I'm done spraying the car, show the watch. ... I'm gonna show the watch periodically." [541 [01:46.7]] | C1 00:32-00:36; SPRAY + FIRST PASS | RAIL_CAP | - |
| E14 | 0:40.90-0:43.90 | FX30541 119.00-122.000 | Host crouched, spraying the door and wheel | music only | C1 00:44-00:47; SPRAY + FIRST PASS | - | - |
| E15 | 0:43.90-0:47.40 | FX30541 166.00-169.500 | Static front of the fully powdered car | music only | C1 01:31-01:34; SPRAY + FIRST PASS | - | front plate (9JTY488) legible - track and blur |
| E16 | 0:47.40-0:49.20 | FX30541 191.60-193.400 | Phone stopwatch close-up (01:57.46 at src 192) | music only | C1 01:57-01:58; SPRAY + FIRST PASS | - | - |
| E17 | 0:49.20-0:53.20 | FX30541 285.50-289.500 | First scan pass: scanner close-up along the car | music only | C1 03:30-03:34; SPRAY + FIRST PASS | - | - |
| E18 | 0:53.20-0:54.70 | FX30541 297.50-299.000 | Phone stopwatch 03:43.44 (src 298) | music only | C1 03:42-03:44; SPRAY + FIRST PASS | - | - |
| E19 | 0:54.70-0:58.70 | FX30541 307.00-311.000 | Crew member in black polo sprays the roof/trunk | music only | C1 03:52-03:56; SPRAY + FIRST PASS | - | - |
| E20 | 0:58.70-1:01.70 | SC_INS_ROOF (3.0 s) | Scan insert: the roof and rear glass, low raking light, slow lateral move | music only | hold the previous IRL event's last value (clock frozen during scan inserts); SPRAY + FIRST PASS | - | plate flattened in render (scan agent) |
| E21 | 1:01.70-1:07.70 | FX30541 347.40-353.400 | Host with scanner points out a spot; crew member with spray gun | "The corner of the left headlight. You see how it's like not fully covered?" / "Got you." [541 [05:47.6]-[05:53.2]] | C1 04:32-04:38; SPRAY + FIRST PASS | RAIL_CAP | background red car plate behind the host (541 ~344-384 s) - blur if legible at 1080p |


### 5. The crash (1:07.7-1:31.2, 23.5 s)

**Purpose:** the turn. "Five minutes on the dot" and two watch faces (04:57.46, 04:59.52) put the clock right there. Then "How you feeling halfway through it?" / "It just crashed."
The music cuts dead and the room goes quiet. Then come "We're still rolling" with the phone at 05:29.46, so the clock has not stopped, and the plan: "start a new scan".
G05 card: **SCANNER CRASHED** / **REBOOTING · CLOCK 1 KEEPS RUNNING**. The rail's CLOCK 1 fast-forwards 05:49 to 11:56 (interpolated, ">>" glyph).
The crash time on the run clock is ~5:05 (541 src 379.5 − 74.6).
The card gives no reason or duration for the delay. The host says "a five minute delay" himself in E29, and that stays in his words only.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E22 | 1:07.70-1:19.00 | FX30541 369.00-380.300 | Crew around the host; analog watch face 04:57.46 (src 372), phone 04:59.52 (src 374); host lifts the scanner | "Time check." / "What? Oh, it's switched. Five minutes on the dot." / "How you feeling halfway through it?" / "It just crashed." [541 [06:09.2]-[06:19.5]] | C1 04:54-05:05; THE CRASH | RAIL_CAP, G14 | background red car plate behind the host (541 ~344-384 s) - blur if legible at 1080p |
| E23 | 1:19.00-1:21.10 | FX30541 382.70-384.800 | Scanner screen in the host's hand | room tone | C1 05:08-05:10; THE CRASH | - | - |
| E24 | 1:21.10-1:22.70 | FX30541 400.40-402.000 | Host walking with scanner and spray gun | "We're still rolling." [541 [06:40.6]] | C1 05:25-05:27; THE CRASH | RAIL_CAP | - |
| E25 | 1:22.70-1:24.50 | FX30541 403.80-405.600 | Phone stopwatch 05:29.46 (src 404) | room tone | C1 05:29-05:31; THE CRASH | - | - |
| E26 | 1:24.50-1:28.20 | FX30541 410.70-414.400 | Host with the spray gun | "Yeah, once this is sorted out, I'm just gonna start a new scan." / "Yeah, I know." [541 [06:50.8]] | C1 05:36-05:39; THE CRASH | RAIL_CAP | - |
| E27 | 1:28.20-1:31.20 | gfx:G05 (3.0 s) | Card on black: crash / reboot; CLOCK 1 fast-forwards | music only | CLOCK 1 fast-forwards 05:49 -> 11:56 (INTERPOLATED between legible 05:29.46 [541@404] and 12:20.75 [542@24]; show the fast-forward glyph); THE CRASH | G05 | - |


### 6. Try again (1:31.2-2:43.6, 72.4 s)

**Purpose:** the restart, with a second timer, a first look at the payoff, and the exterior done.
E29 "start a secondary timer. Now." brings the music back, and TIMER 2 appears in the rail (G06: **TIMER 2** / **STARTED AFTER THE REBOOT**).
From here TIMER 2 is the big clock and CLOCK 1 shrinks.
The rear-bumper pass ends on the solved frame, and E33 is the **hard 1:1 cut to SC_MATCH_REAR**, the first time the real car becomes its scan.
After it: more passes, watch 05:28.64, and the last legible phone value 17:53.38. Then the exterior is called done: "That's done. Check mark."
TIMER 2 stops at 08:32.23 (stopped in frame, and "8 minutes and 32 seconds" said), and the rail shows **TIMER 2 08:32 ❚❚** (G07).
The scanner-screen review (E39) shows the scan building on the device.
Scan inserts: SC_MATCH_REAR, and **SC_INS_CABIN** after "That's the full interior" (conditional: drop it if the STL has no cabin).
E42 "So let's also time that" hands off to the hard parts.
Excluded: 545 [01:03]-[01:12] ("Is that with the 2 minutes of spraying? ... 20 minutes with the crash"), which contradicts the owner's numbers, and 545 [00:03] "7 minutes and 41 seconds" (no face in frame).
545 is filmed rotated 90°. Rotate it upright and centre-crop to 1920x920 (from 4K if the original is kept, else pillarbox on a blurred, darkened copy of the same frame, with no text on it).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E28 | 1:31.20-1:33.70 | FX30542 0.00-2.500 | Host turns to camera at the bench | "So, what happened? So the scanner crashed." [542 [00:00]-[00:02.4]] | C1 11:56-11:59; TRY AGAIN | RAIL_CAP, G14 | - |
| E29 | 1:33.70-1:43.60 | FX30542 4.70-14.600 | Bench: scanner, spray gun; host; wrist | "So after like a five minute delay, we're rebooting it. And now we're gonna try again. All right, let's start the... start a secondary timer. Now. Yep." [542 [00:04.8]-[00:14.1]] | C1 12:01-12:11, T2 00:00-00:01; TRY AGAIN | RAIL_CAP, G06 | - |
| E30 | 1:43.60-1:45.20 | FX30542 15.40-17.000 | Watch face 00:03.00 (src 16), running | music only | C1 12:12-12:13, T2 00:02-00:04; TRY AGAIN | G06 | - |
| E31 | 1:45.20-1:46.60 | FX30542 23.60-25.000 | Phone stopwatch 12:20.75 (src 24) | music only | C1 12:20-12:21, T2 00:10-00:12; TRY AGAIN | - | - |
| E32 | 1:46.60-1:53.01 | FX30542 40.97-47.381 | Host crouched scanning the rear bumper; ENDS on solved frame 1135 (47.339 s) | music only | C1 12:37-12:44, T2 00:27-00:34; TRY AGAIN | - | rear plate (9JTY488) legible - track and blur |
| E33 | 1:53.01-1:57.51 | SC_MATCH_REAR (4.5 s) | HARD 1:1 CUT to the scan from the same camera, then a slow push on the rear bumper | music only | hold the previous IRL event's last value (clock frozen during scan inserts); TRY AGAIN | - | plate flattened in render (scan agent) |
| E34 | 1:57.51-2:01.51 | FX30544 4.00-8.000 | Host kneeling, scanning the lower front fender in the doorway light | music only | C1 17:12-17:16, T2 05:02-05:06; TRY AGAIN | - | - |
| E35 | 2:01.51-2:02.91 | FX30544 29.60-31.000 | Watch 05:28.64 (src 30) | music only | C1 17:37-17:39, T2 05:28-05:29; TRY AGAIN | - | - |
| E36 | 2:02.91-2:04.31 | FX30544 44.60-46.000 | Phone lock screen stopwatch 17:53.38 (src 45) | music only | C1 17:52-17:54, T2 05:43-05:44; TRY AGAIN | - | - |
| E37 | 2:04.31-2:09.31 | FX30544 126.00-131.000 | Scanner close along the lower door | music only | C1 19:14-19:19, T2 07:04-07:09; TRY AGAIN | - | - |
| E38 | 2:09.31-2:19.01 | FX30545 53.30-63.000 | Camera rotated 90 deg: watch 08:32.23 stopped (src 56), host | "So, are you still recording?" "Yep." "So that's the exterior. That's done. Check mark. What's the time?" "The cheating time is 8 minutes and 32 seconds." [545 [00:53.4]-[01:02.9]] | C1 running, no digits, T2 08:29-08:32; TRY AGAIN | RAIL_CAP, G07 | - |
| E39 | 2:19.01-2:32.26 | FX30545 100.70-113.950 | Scanner screen: the car's scan turning under his thumb | "Front, hood, roof, right side. Rear quarter panel's a little messed up. Roof's messed up. So I came back here, did the whole roof, did the right quarter panel, fixed the trunk." [545 [01:40.8]-[01:53.8]] | C1 running, no digits, T2 08:32-08:32; TRY AGAIN | RAIL_CAP, G07 | - |
| E40 | 2:32.26-2:33.41 | FX30545 115.15-116.300 | Scanner screen / host | "That's the full interior." [545 [01:55.2]] | C1 running, no digits, T2 08:32-08:32; TRY AGAIN | RAIL_CAP, G07 | - |
| E41 | 2:33.41-2:36.41 | SC_INS_CABIN (3.0 s) | Scan insert: cabin through the side glass opening (CONDITIONAL) | music only | hold the previous IRL event's last value (clock frozen during scan inserts); TRY AGAIN | - | plate flattened in render (scan agent) |
| E42 | 2:36.41-2:43.61 | FX30545 116.35-123.550 | Host (rotated source) | "So now, if you wanna make a lip kit, let's jack the car up, do the fronts and sides, wheel wells inside. So let's also time that." [545 [01:56.4]-[02:03.3]] | C1 running, no digits, T2 08:32-08:32; TRY AGAIN | RAIL_CAP, G07 | - |


### 7. The hard parts (2:43.6-3:43.4, 59.8 s)

**Purpose:** what makes a scan useful for parts design: arches, wheels, sills, from jack height and from the floor. Highest energy, shortest shots.
The clock is TIMER 2 only (CLOCK 1 shows "running", with no digits, because nothing is legible after 544@45). Watch faces at 08:46, 11:17, 13:05 and 15:31 punctuate the montage.
Lines: "For harder-to-reach areas, I'll use the can." / "It's a crazy position. Is this the most optimal scanning position?" / "Oh, under the car! It disappeared!" /
"Done? Nope. Oh yeah, almost done." Scan inserts: **SC_INS_WHEEL** after the live scan at the wheel (E47) and **SC_INS_SILL** after lying under the car (E56).
Do not use: 547 127-133 s (the crew says "I can't wait to blur that"), 551 4.3-7 s (profanity), 551 89.9-97 s (cat noises), and the 548 jack call, which names a crew member (ducked to music).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E43 | 2:43.61-2:45.61 | FX30546 4.60-6.600 | Watch 08:46.40 -> 08:47.40, running again | music only | C1 running, no digits, T2 08:46-08:48; THE HARD PARTS | G14 | - |
| E44 | 2:45.61-2:49.11 | FX30546 59.50-63.000 | Host working the floor jack | music only | C1 running, no digits, T2 09:40-09:44; THE HARD PARTS | - | - |
| E45 | 2:49.11-2:52.16 | FX30547 0.00-3.050 | Host holds up the spray can | "For harder-to-reach areas, I'll use the can." [547 [00:00.1]] | C1 running, no digits, T2 10:11-10:14; THE HARD PARTS | RAIL_CAP | - |
| E46 | 2:52.16-2:55.66 | FX30547 36.00-39.500 | Spray can into the front wheel arch | music only | C1 running, no digits, T2 10:47-10:50; THE HARD PARTS | - | - |
| E47 | 2:55.66-3:00.16 | FX30547 53.50-58.000 | Live scan on the scanner screen beside the wheel | music only | C1 running, no digits, T2 11:04-11:09; THE HARD PARTS | - | - |
| E48 | 3:00.16-3:03.16 | SC_INS_WHEEL (3.0 s) | Scan insert: front wheel and arch (the front-left wheel is the well-captured one) | music only | hold the previous IRL event's last value (clock frozen during scan inserts); THE HARD PARTS | - | plate flattened in render (scan agent) |
| E49 | 3:03.16-3:04.56 | FX30547 65.60-67.000 | Watch 11:17.36 (src 66) | music only | C1 running, no digits, T2 11:16-11:18; THE HARD PARTS | - | - |
| E50 | 3:04.56-3:09.96 | FX30547 120.40-125.800 | Host lying on the floor scanning under the front | "It's a crazy position." "Is this the most optimal scanning position?" "Yeah." [547 [02:00.6]-[02:05.3]] | C1 running, no digits, T2 12:11-12:17; THE HARD PARTS | RAIL_CAP | - |
| E51 | 3:09.96-3:11.96 | FX30548 6.20-8.200 | Watch 13:05.01 (src 7) | music only | C1 running, no digits, T2 13:04-13:06; THE HARD PARTS | - | - |
| E52 | 3:11.96-3:13.96 | FX30549 0.50-2.500 | Low-angle powder spray close-up | music only | C1 running, no digits, T2 13:46-13:48 (derived); THE HARD PARTS | - | - |
| E53 | 3:13.96-3:17.96 | FX30550 12.00-16.000 | Jacking the rear up | music only | C1 running, no digits, T2 14:30-14:34 (derived); THE HARD PARTS | - | check rear plate at 1080p (visible at 0 s and 36 s, likely not in 12-16 s) |
| E54 | 3:17.96-3:20.36 | FX30551 0.00-2.400 | Floor / under the car (the can went missing) | "Oh, under the car! It disappeared!" [551 [00:00]-[00:02.3]] | C1 running, no digits, T2 15:01-15:03; THE HARD PARTS | RAIL_CAP | - |
| E55 | 3:20.36-3:21.76 | FX30551 29.60-31.000 | Watch 15:31.30 (src 30) | music only | C1 running, no digits, T2 15:30-15:32; THE HARD PARTS | - | - |
| E56 | 3:21.76-3:27.46 | FX30551 84.00-89.700 | Host lying under the car scanning the sill/underside | music only | C1 running, no digits, T2 16:25-16:31; THE HARD PARTS | - | - |
| E57 | 3:27.46-3:30.46 | SC_INS_SILL (3.0 s) | Scan insert: side sill from a low angle | music only | hold the previous IRL event's last value (clock frozen during scan inserts); THE HARD PARTS | - | plate flattened in render (scan agent) |
| E58 | 3:30.46-3:34.36 | FX30552 19.30-23.200 | Host scanning low by the car | "Okay." "Done?" "Nope." "Oh yeah, almost done." [552 [00:19.4]-[00:23.1]] | C1 running, no digits, T2 18:12-18:16 (derived); THE HARD PARTS | RAIL_CAP | - |
| E59 | 3:34.36-3:38.36 | FX30552 48.00-52.000 | Under the rear wheel arch beside the jack | music only | C1 running, no digits, T2 18:41-18:45 (derived); THE HARD PARTS | - | - |
| E60 | 3:38.36-3:43.36 | FX30552 100.00-105.000 | Host flat on his back scanning upward | music only | C1 running, no digits, T2 19:33-19:38 (derived); THE HARD PARTS | - | - |


### 8. Time (3:43.4-4:17.8, 34.4 s)

**Purpose:** the answer. "Time. 20 minutes. Done." over the watch at 20:24.95. Then the scoreboard card, with the host's "And the other one, 32 minutes. Yep." running under it (J-cut).
G08: **CLOCK 1 · FROM "GO" · 32 MIN** / **TIMER 2 · RESTARTED AFTER THE CRASH · 20 MIN**. G09: **THE 15-MINUTE BET: MISSED** / **CLOSEST GUESS: 30 MINUTES**.
Then a small extra: the powder is already evaporating off the hood in that span (said on camera, no number of ours).
Walk-out to the car in the sun ends on the solved frame, then the **hard 1:1 cut to SC_MATCH_FRONT**. The rail freezes at **C1 32 MIN · T2 20 MIN** from E62 to the end.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E61 | 3:43.36-3:50.26 | FX30553 6.80-13.700 | Watch 20:24.95 (src 9) fills the frame, then the host | "Time. 20 minutes. Done." [553 [00:07.3]-[00:11.8]] | C1 running, no digits, T2 20:22-20:24; TIME | RAIL_CAP, G14 | - |
| E62 | 3:50.26-3:54.66 | gfx:G08 (4.4 s) | Scoreboard card on black | "And the other one, 32 minutes. Yep." | rail clocks frozen: CLOCK 1 "32 MIN", TIMER 2 "20 MIN"; TIME | G08, RAIL_CAP | - |
| E63 | 3:54.66-3:56.86 | gfx:G09 (2.2 s) | Card on black: the bet result | music only | frozen as E62; TIME | G09 | - |
| E64 | 3:56.86-4:00.56 | FX30553 18.70-22.400 | Host walking to the front of the car | "So one thing to note is also cleanup time." [553 [00:18.8]-[00:22.3]] | FROZEN: C1 32 MIN, T2 20 MIN; TIME | RAIL_CAP | - |
| E65 | 4:00.56-4:07.76 | FX30553 25.90-33.100 | The hood: powder already clearing in X-shaped marks | "...in that 20 minute span right here, most of the spray is already off the hood and it's already starting to evaporate." [553 [00:26.0]-[00:32.9]] | FROZEN: C1 32 MIN, T2 20 MIN; TIME | RAIL_CAP | front plate if in frame |
| E66 | 4:07.76-4:12.81 | FX30554 6.00-11.053 | Walk out of the shop door onto the car in the sun; ENDS on solved frame 264 (11.011 s) | music only | FROZEN: C1 32 MIN, T2 20 MIN; TIME | - | front plate (9JTY488) legible - track and blur |
| E67 | 4:12.81-4:17.81 | SC_MATCH_FRONT (5.0 s) | HARD 1:1 CUT to the scan from the same camera, front of the car, slow push | music only | hold the previous IRL event's last value (clock frozen during scan inserts); TIME | - | plate flattened in render (scan agent) |


### 9. The scan (4:17.8-4:36.8, 19.0 s)

**Purpose:** proof, and what the customer gets. Rail hidden, music resolving.
G10 **LEXUS IS350** / **FULL CAR SCAN**. G11 **24,999,992 TRIANGLES** / **FULL CAR · STL FILE** (STL header; a static label, not the ScanHUD counter, which stops at 99.9 %).
G12 **REAR REFLECTOR** / **SCANNED IN PLACE**, then G13 **REFLECTOR REMOVED** / **THE MOUNTING POCKET BEHIND IT** (the only part state with a scan).
Labels go over pure black with a halo (lessons).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E68 | 4:17.81-4:24.81 | SC_RES_FULL (7.0 s) | Full car, satin silver on black, slow continuous move (not a turntable) | music only | hidden; THE SCAN | G10 | plate flattened in render (scan agent) |
| E69 | 4:24.81-4:29.81 | SC_RES_MESH (5.0 s) | Mesh-density close-up: triangles visible on a panel edge | music only | hidden; THE SCAN | G11 | plate flattened in render (scan agent) |
| E70 | 4:29.81-4:36.81 | SC_RES_REFLECTOR (7.0 s) | Rear lower corner: reflector in place -> reflector removed (pocket) | music only | hidden; THE SCAN | G12, G13 | plate flattened in render (scan agent) |


### 10. CONCLUSION (written by the conclusion agent) (4:36.8-5:04.8, 28 s)

**Slot: CONCLUSION (written by the conclusion agent).** Target **28 s** (25-32 s). It runs 4:36.8-5:04.8, then the end card.

- **Hand off from:** E70. The last image is the reflector-removed pocket. Music is in its resolve. The rail is hidden, and comes back frozen at **C1 32 MIN · T2 20 MIN** when IRL returns.
- **Must do:** answer the title question in the host's own words, with the owner's numbers (32 min from "go", 20 min without the crash). Say no new number.
- **Best source:** FX30555, to camera, outdoors, host + crew member. Usable sync: 11.18-15.80 "but if we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car,"
  and 25.86-27.06 "yeah, this thing's fast." (judgement call).
  Avoid or decide: 5.38-7.52 names "Caleb". 8.50-10.60 "30 minutes actual" conflicts with 32: either cut it or keep it with the rail showing 32 MIN and flag it.
  16.02-21.20 "10 minutes if I just did the exterior, with the power of a spray gun, AESUB Violet, and the Artec Leo" (the 10-minute figure is ambiguous, and brands are owner-only).
  21.70-25.10 "any other scanner out there that can do it faster" is an excluded claim.
  The front plate is legible at 555 @30 s.
- **May use:** a black recap card (the predictions vs the two clocks, from G02/G08 values only) or one of the spare scan stills. Optional pickup PU6.
- **Must not:** put text on IRL, use a dissolve between IRL and scan, or repeat any shot used above (FX30554 6-11 s and FX30553 6.8-33.1 s are taken).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E71 | 4:36.81-5:04.81 | CONCLUSION_SLOT (28.0 s) | Conclusion: hands off from E70; primary source FX30555 to-camera | see script.md slot brief | frozen final: CLOCK 1 "32 MIN", TIMER 2 "20 MIN"; RESULT | RAIL_CAP | front plate (9JTY488) legible - track and blur (555 @30 s) |


### 11. End card (5:04.8-5:09.8, 5 s)

**Purpose:** sign-off. G15: Illumaesthetic logo, large (lessons: 700+ px wide), and a CTA line the owner must confirm.
The scan listing exists at illumaesthetic.com/products/lexus-is-xe30-3d-scan-facelift-2020 (from clips.md). Whether to name it, and the exact wording, is the owner's call. Rail hidden.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD rail (clock; chapter) | gfx | blur |
|---|---|---|---|---|---|---|---|
| E72 | 5:04.81-5:09.81 | gfx:G15 (5.0 s) | End card on black | music only | hidden; (none) | G15 | - |

## Graphic cues (exact text)

| id | type | text / sub | timeline | placement | source of every word/number |
|---|---|---|---|---|---|
| G01 | title on scan render | HOW FAST CAN WE 3D-SCAN AN ENTIRE CAR? — sub: LEXUS IS350 · ONE CAR · ONE STOPWATCH | 0:07.40-0:12.60 | lower third of the scan render, white sans, black halo/plate (lessons: labels on silver need a halo) | question = video title; no numbers |
| G02 | rail chips (prediction tally) | 2 HR / 30 MIN / 15 MIN | 0:12.60-0:22.00 | HUD rail, right of the clock; "2 HR" shows from E05 (heard in E01), "30 MIN" pops on E06 "30", "15 MIN" pops on E07 "15" and is highlighted as THE BET | 541 [00:02.4] / [00:17.5] "two hours", [00:22.1] "30 minutes", [00:26.3] "15 minutes" |
| G03 | full-frame card on black | THE BET: 15 MINUTES — sub: "LESS THAN THE LENGTH OF A YOUTUBE VIDEO" | 0:19.50-0:22.00 | centre | 541 [00:26.3] |
| G04 | full-frame card on black | STEP 1: SPRAY — sub: A TEMPORARY MATTE COAT SO THE SCANNER CAN READ SHINY PAINT AND GLASS | 0:31.00-0:32.50 | centre | no numbers; "it evaporates" is said on camera (541 [05:57.3], 553 [00:32]) |
| G05 | full-frame card on black | SCANNER CRASHED — sub: REBOOTING · CLOCK 1 KEEPS RUNNING | 1:28.20-1:31.20 | centre; rail CLOCK 1 fast-forwards 05:49 -> 11:56 with a ">>" glyph (interpolated) | 541 [06:19.5] "It just crashed", 542 [00:01.7] "the scanner crashed", 542 [00:08] "we're rebooting it", 541 [06:40.6] "We're still rolling"; clock continuity checked: 542@24 reads 12:20.75 |
| G06 | rail element | TIMER 2 — sub: STARTED AFTER THE REBOOT | 1:42.00-5:09.81 | HUD rail, second clock right of CLOCK 1; from here TIMER 2 is the big clock and CLOCK 1 goes small | 542 [00:12.6] "start a secondary timer. Now."; watch 00:03.00 at 542@16 |
| G07 | rail state | TIMER 2 08:32 ❚❚ | 2:12.01-2:43.61 | HUD rail TIMER 2 frozen with a pause glyph | watch 08:32.23 stopped at 545@56; "8 minutes and 32 seconds" said at 545 [01:01.5] |
| G08 | full-frame scoreboard card on black | CLOCK 1 · FROM "GO" · 32 MIN / TIMER 2 · RESTARTED AFTER THE CRASH · 20 MIN | 3:50.26-3:54.66 | two rows, centre; row 2 lands on the beat after "32 minutes" ends | owner: 32 min elapsed / 20 min without the crash; said 553 [00:09.7] "20 minutes", [00:14.5] "32 minutes"; watch 20:24.95 at 553@9 |
| G09 | full-frame card on black | THE 15-MINUTE BET: MISSED — sub: CLOSEST GUESS: 30 MINUTES | 3:54.66-3:56.86 | centre, playful | 541 [00:26.3] 15, [00:22.1] 30; owner 32/20 |
| G10 | label on scan render | LEXUS IS350 — sub: FULL CAR SCAN | 4:18.81-4:24.31 | bottom-left, over pure black only (measure coverage under the box) | car identity from clips.md |
| G11 | label on scan render | 24,999,992 TRIANGLES — sub: FULL CAR · STL FILE | 4:25.31-4:29.81 | bottom-left, static text (NOT the ScanHUD counter: it stops at 99.9 %) | STL header of "Lexus 4IS IS350 Full Car.stl" |
| G12 | label on scan render | REAR REFLECTOR — sub: SCANNED IN PLACE | 4:30.31-4:33.11 | black band above the car | scan file "Lexus 4IS reflector.stl" |
| G13 | label on scan render | REFLECTOR REMOVED — sub: THE MOUNTING POCKET BEHIND IT | 4:33.31-4:36.81 | same position as G12 (swap on the state change) | scan file "Lexus 4IS reflector removed.stl" |
| G14 | rail chapter label | per event hud.chapter | 0:00.00-5:09.81 | HUD rail, right end; changes on the first event of each section | - |
| G15 | end card on black | ILLUMAESTHETIC — sub: [owner to confirm: scan listing CTA / URL] | 5:04.81-5:09.81 | logo large (lessons: 700+ px wide), CTA below | - |
| RAIL_CAP | burned-in captions in the HUD rail | verbatim sync words (event audio.hear) | 0:00.00-5:09.81 | HUD rail centre, max 2 lines x 42 chars, white on the black rail, never over picture | large-v3 word times in /home/user/media/work/is350-long/transcripts/ |

## Blur / privacy list (editor)

| where | what | action |
|---|---|---|
| E12, E15 (541 103-106, 166-170) | front plate 9JTY488 | track + blur |
| E32 (542 41-47.4) | rear plate 9JTY488, legible through the match frame | track + blur. The scan side is flattened in the render, so the 1:1 cut stays clean |
| E66 (554 6-11.05) | front plate 9JTY488 | track + blur up to the cut frame |
| E65 (553 25.9-33.1) | front plate, if the hood shot reaches the bumper | check at 1080p |
| E53 (550 12-16) | rear plate (visible at 550 0 s and 36 s) | check at 1080p |
| E02, E21, E22 (541 344-384) | another car's plate (red car in the background) | blur if legible at 1080p |
| conclusion (555 @30) | front plate | blur if used |
| never used | 541 40-68 s phone (alarms, joke timer), 547 127-133 s ("can't wait to blur that"), 551 4.3 s profanity | not in the cut |

Phone screens that ARE used (E09, E16, E18, E25, E31, E36) show only the stopwatch / lock-screen stopwatch. They were checked frame by frame and show no contacts or messages.

## Optional pickup lines (host records later; the video works without them)

| id | where | line | replaces |
|---|---|---|---|
| PU1 | E08, 0:19.5 (card grows 2.5 s to ~4.5 s) | "One car, one stopwatch. It starts on 'go'." | nothing (VO over the G03 card) |
| PU2 | E11, 0:31.0 (card grows 1.5 s to ~5 s) | "Step one is powder. Shiny paint and glass are hard for a scanner to read, so the whole car gets a thin matte coat that evaporates on its own." | G04's sub line (keep only STEP 1: SPRAY) |
| PU3 | E27, 1:28.2 (card stays 3 s, may grow to ~5 s) | "Five minutes in, the scanner crashed. The first clock kept running. Once it rebooted, we started a second one." | G05's sub line |
| PU4 | E43-E47, 2:43.6-3:00 (music-only shots) | "The outside is the easy part. If you want to design a lip kit or fenders, you need the arches, the sills and the wheels, and that means jack stands and lying on the floor." | nothing (VO over music-only IRL) |
| PU5 | E68-E70, 4:17.8-4:36.8 (scan, music) | "That's the whole car: 24,999,992 triangles. We also scanned it with the rear reflector out." | nothing; G11 stays as is |
| PU6 | conclusion slot | "So how fast can we 3D-scan an entire car? Thirty-two minutes from 'go'. Twenty on the clock we restarted after the crash. Fifteen next time?" | the conclusion agent's choice of a 555 line |

Rules for pickups: the host's own voice only (no cloning), imperial units, and no numbers beyond 15 / 32 / 20 / 24,999,992. PU2's "evaporates" is backed by 541 [05:57.3] and 553 [00:32].

## For the owner

Open questions:
1. **The two timers.** The frames show TIMER 2 started about 12:10 after "go" (phone 12:20.75 at 542@24, while the watch read 00:03.00 at 542@16). The crash came at ~5:05 on CLOCK 1.
   So the 20 minutes leaves out the ~5 min before the crash as well as the reboot. TIMER 2 was also stopped for ~1.5 min during the exterior review (08:32.23 stopped, 545@56).
   The camera clock suggests CLOCK 1 may also have been paused around then. We show only your numbers, labelled **CLOCK 1 · FROM "GO" · 32 MIN** and **TIMER 2 · RESTARTED AFTER THE CRASH · 20 MIN**.
   We do not explain the gap. Is that wording right, or do you want "20 MIN WITHOUT THE CRASH"?
2. **"Five minute delay".** It is said on camera (E29) and kept as speech. The card does not repeat it. OK?
3. **"The cheating time is 8 minutes and 32 seconds"** (E38): keep the word "cheating" in the caption? It matches the watch face, but the phrase is unexplained.
4. **Cabin scan (E41).** It goes in only if the full-car STL holds cabin geometry. The earlier reel's notes say the sprayed glass may be a closed shell. If it doesn't, the shot is dropped (-3 s).
5. **End card CTA.** Name the scan listing (illumaesthetic.com/products/lexus-is-xe30-3d-scan-facelift-2020) or a scanning-service line? Exact wording?
6. **People.** Two crew members appear to camera (the "two hours" and "30 minutes" guesses). Are they OK to show? No names are on screen. "Lorenzo" is ducked out (548), and "Caleb" is said in 555 if the conclusion uses 5.4-7.5 s.
7. **Brands.** "Artec Leo" and "AESUB" are said on camera (541 [04:05], 553 [00:23.8], 555 [00:19.8]-[00:21]). The body uses none of them, and no graphic names them.
   The conclusion agent will leave them out unless you want them in. The "Artec ad and an AESUB ad" joke (541 [01:28]) and "any other scanner ... faster" (555 [00:21.7]) are cut.
8. **"30 minutes actual"** (555 [00:10]) vs your 32. The conclusion should cut it. Confirm 32 is the number to show.
9. **Music.** `music.md` in this project still says "not delivered". This script assumes the owner's ~20-minute "video game" mix as the lead described, mapped by the music agent.

What I assumed:
- The 15-minute bet is the host's. Frames show him (Berkeley tee) to camera at 541 26-30 s. "Two hours" is the crew member in the dark tee; "30 minutes" the one in the black polo.
- The phone is CLOCK 1 and the watch is TIMER 2 after the reboot. Before the crash the watch tracked the same run (04:57.46 at 541@372 vs phone 04:59.52 two seconds later).
  This is checked against the camera clock: TIMER 2 = wall-clock − 18:22:21.7 for all five faces from 546 to 553.
- Clock values for 549, 550 and 552 are derived from the camera clock (no face in those clips), and the reboot fast-forward is interpolated. Both are marked `clock_known: false` in `edl.json`.
- The clips are being converted to 1080p in place. All source times here are in seconds and do not depend on resolution. The 545 rotation crop will be soft at 1080p.
- Clip order follows the camera's recording times. 543 (11 s) is not used.
- Runtime is 5:10, at the short end of the target, because only about two minutes of usable sync exists. A longer cut would mean padding.
