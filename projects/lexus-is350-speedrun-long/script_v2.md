# L1 script v2: "How fast can we 3D-scan an entire car?" (Lexus IS350 speed run)

Script v2, 2026-11-13. It implements the owner's 11 notes on the v1 rough cut (brief.md, "v2"); where they conflict with v1 rules, they win.
The edit as data is `edl_v2.json`: same schema as v1, plus `protect_dialogue`, `dialogue`, `speed`, `decode` and `replaces_v1`, and overlay positions instead of the rail.
v1 files (`script.md`, `edl.json`) are untouched.
Every number on screen still comes from **the owner** (32 / 20), **a time said aloud** (transcript timestamp) or **a stopwatch legible in frame** (clip @ s),
or it is marked **derived** (camera clock) or **interpolated** (one card).

## Titles (5)

1. **We Bet 15 Minutes to 3D-Scan an Entire Car. Then the Scanner Crashed.** (chosen, unchanged)
2. How Fast Can We 3D-Scan an Entire Car? (32 Minutes, 1 Crash)
3. Can We 3D-Scan a Whole Car in 15 Minutes?
4. 3D-Scanning a Lexus IS350 Against the Clock: 32 Minutes, 2 Timers
5. We Tried to Scan a Whole Car Faster Than a YouTube Video (replaces v1's triangle-count title, rule 10)

**Logline:** the host bets he can 3D-scan a whole Lexus IS350 in 15 minutes, "less than the length of a YouTube video". The spraying alone takes 1:55.
Five minutes in, the scanner crashes. After a reboot, a second timer and a lot of lying on the floor, he gets 32 minutes from "go" and 20 without the crash.
Then the real car turns into its scan, angle by angle.

## Run order v2

| # | section | time | dur | what it does |
|---|---|---|---|---|
| 1 | Cold open | 0:00.00-0:10.80 | 10.8 s | A guess ("two hours"), then a tease of the strongest real-to-scan cut (front), title over the scan |
| 2 | The bet | 0:10.80-0:21.47 | 10.7 s | 30 minutes; the host's 15 |
| 3 | PART 1 · SPRAY | 0:21.47-0:55.42 | 34.0 s | Go; confident line; 3 distinct spray shots (front, side, time-lapse of the rest); phone 01:55 "SPRAY DONE"; "Just two minutes" |
| 4 | PART 2 · SCAN | 0:55.42-1:14.33 | 18.9 s | First passes; coverage check |
| 5 | The crash (set-piece) | 1:14.33-2:00.14 | 45.8 s | "Five minutes on the dot" -> "It just crashed" -> freeze/glitch -> clock still running -> reboot fast-forward -> "start a secondary timer. Now." |
| 6 | Try again | 2:00.14-2:59.80 | 59.7 s | Restart passes; exterior done (TIMER 2 08:32); review on the scanner screen; "let's also time that" |
| 7 | The hard parts | 2:59.80-4:00.77 | 61.0 s | Jacks, arches, the floor, the lost can; "almost done" |
| 8 | Time | 4:00.77-4:15.02 | 14.3 s | "Time. 20 minutes. Done. And the other one, 32 minutes." scoreboard overlay; bet result |
| 9 | The scan: end montage | 4:15.02-4:48.52 | 33.5 s | 5 real -> scan pairs building in pace, then the full-car hero |
| 10 | Conclusion (CON_*) | 4:48.52-5:06.67 | 18.2 s | The host's answer, in one full sentence; final scan + CTA |
| 11 | End card | 5:06.67-5:11.67 | 5.0 s | Logo |
| | **Total** | | **5:11.7** | target 5:00-6:00. Beat snap can only lengthen protected lines, so expect +1-3 s |

Seconds by kind: sync dialogue **164.9 s**, IRL music-only / time-lapse / freeze **104.1 s**, scan **33.5 s** (all at the end plus the 5 s cold-open tease),
black cards **9.2 s in 3 cards** (crash, reboot, end).

## What changed from v1 (owner notes -> events)

| # | owner note (brief v2) | implemented in | how |
|---|---|---|---|
| 1 | Cuts clipped the dialogue | every event with `protect_dialogue: true` (CO_01, B_01, B_02, P_01, P_02, P_04, P_08, Q_05, C_01, C_04, C_06, C_08, T_07, T_08, H_03, H_07, H_10, H_11, H_14, TM_01, CON_01) | src_in/out from word times + audio energy: ≥0.25 s before the first word and ≥0.4 s after the last word of the complete sentence. Beat snap may only lengthen. Exceptions are listed below |
| 2 | Scan presentation only at the end, IRL -> same-angle scan, several angles, then the hero | M1_A-M6 (end montage); CO_02/CO_03 (tease) | SC_INS_ROOF/WHEEL/SILL/CABIN, SC_TITLE, the mid-body SC_MATCH_REAR (v1 E33) and SC_MATCH_FRONT (v1 E67) are out of the body |
| 3 | FX30545 looked wrong (pillarbox) | T_07, T_08 | 4K original `/home/user/media/lexus-is350/dropbox_4k/FX30545.MP4`. **Decode with `-noautorotate`**: the file carries a -90° rotation flag, but the raw 3840x2160 frame is already upright 16:9 (checked at 56, 104 and 117 s). Full frame, no crop needed |
| 4 | Do not blur plates | all events | `blur: null` everywhere; v1's 8 tracked blurs and the CON_03 blur are removed |
| 5 | Fewer, non-repetitive spray clips | P_03 (front), P_04 (side, with sync), P_05 (time-lapse of the rest) | v1 E12/E13/E14/E15/E19 (5 spray shots incl. a roof re-spray) -> 3 distinct shots + the phone + the result |
| 6 | Subsection break spray / scan | STING1_v2 on P_03, STING2_v2 on Q_01; chapter tags | Overlay stings "PART 1 · SPRAY" / "PART 2 · SCAN", not black cards |
| 7 | Show how long the spraying took | P_05 time-lapse + P_06 phone + G_SPRAY_v2 + P_08 | Real clock runs 00:39 -> 01:55 at 20x and lands on the phone at 01:55.47 (see evidence below) |
| 8 | Dramatize the crash, with fitting music | C_01-C_08 | Set-piece with music stop, freeze/glitch, card, still-running clock, fast-forward, release (spec below) |
| 9 | Graphics as overlays on full-frame footage | HUD_v2, CAP_v2, all G*_v2 | No rail, no bars; IRL full 1920x1080; timer cluster top-right (flips to top-left per event), captions bottom-centre, lower-left/right overlays; 3 black cards |
| 10 | No triangle count / mesh shot | removed G11, SC_RES_MESH, CON_G2, title #5 | No triangle text anywhere (thumbnail agent: same) |
| 11 | No reflector section | removed E70, G12, G13, SC_RES_REFLECTOR | - |

## Clipped dialogue in v1 (`timeline.json` vs word times, checked against the audio energy)

Whisper word ends drift across pauses, so each suspect out-point was checked on the 20 ms energy envelope of the clip's WAV and against medium.en.

| v1 event | built src in-out | what was cut | v2 fix |
|---|---|---|---|
| E02 (cold open) | 541 380.63-382.84 | tail of "before" (speech to ~382.95) | merged into C_01, out 383.35 |
| E06 | 541 21.90-22.98 | started on the tail of the question ("car?" 21.74-21.92) | B_01 takes the whole take: 19.45-23.20 |
| E07 | 541 26.15-30.03 | "minutes" (speech to ~30.15); no breath | B_02 out 30.55 (there is no "of course": large-v3 artefact) |
| E09 | 541 71.28-76.54 | started inside "Huh? Yeah." | P_01 in 70.75 |
| E10 | 541 77.24-81.00 | "time" cut mid-word (80.84-81.24) | P_02 runs to the end of "Oh no, oh no, that's not the right one." (83.78) |
| E13 | 541 106.61-111.49 | stopped mid-sentence: "I'm gonna show the [watch periodically]" (to 112.9) + "Yeah, checkpoint" | P_04 out 114.24 |
| E21 | 541 347.31-353.35 | "Got you." (352.98-353.38) | Q_05 out 353.78 |
| E28/E29 | 542 0-2.50 / 4.71-14.60 | jump cut through "So" at 2.42; lost the closing "Yup." (energy 16.9-17.5) | C_08 one take 0.00-17.95 |
| E45 | 547 0-3.05 | "can." (speech to ~3.3) | H_03 out 3.70 |
| E54 | 551 0-2.42 | the rest of the line (speech 2.3-3.0; medium.en "it's just over here") | H_10 out 3.45 (profanity starts ~4.3) |
| E62 (card audio) | 553 13.70-18.08 | "Yep." (speech to ~18.1), no breath | TM_01 one take 7.30-18.55 |
| CON_01 | 555 11.64-15.77 | "car," (to ~16.05) and the rest of the sentence | CON_01 11.50-21.65, whole sentence |
| CON_03 | 555 25.61-27.24 | "fast" (to ~27.25); also starts mid-sentence after an excluded claim | removed |

Tight but not clipped in v1 (tail < 0.4 s or lead < 0.25 s): E01, E05, E22 (0.24), E26, E38 (0.13), E39 (0.11), E40 (0.16), E42 (0.14), E50 (0.04) and E58 (0.11). All are fixed in v2.

**Exceptions in v2** (the rule cannot be met without excluded words; each has `max src_out` in the EDL):
- **Clip starts on the first word:** C_08 (542 @0.00), H_10 (551 @0.00) and H_03 (547, lead 0.08). Pre-roll 0.25 s of room tone from the same clip, as named in the notes.
- **T_07 tail 0.20 s.** The next sentence ("Is that with the 2 minutes of spraying? ... 20 minutes with the crash") contradicts the owner's numbers. Hard limit 63.22, with a 3-frame audio fade.
- **CON_01 lead 0.14 s / tail 0.35 s.** Before it, the other speaker's "30 minutes actual, but" runs straight in. After it comes the excluded "any other scanner ... faster". Both edges sit in measured silence, so no word is touched.

## Overlay layout (replaces the v1 HUD rail)

- **IRL is full frame 1920x1080.** No rail, no bars.
- **HUD_v2 cluster, top-right** (x 1480-1880, y 40-200). CLOCK 1 is the large MM:SS on a 45 % black plate with 12 px radius. From "Now." (C_08) TIMER 2 becomes the large number and CLOCK 1 the small row. A chapter tag sits under the timers.
  Each event carries `hud.corner`. The editor flips it to the top-left mirror (x 40-440) when a face or the in-shot stopwatch enters x > 1440, y < 240, checked on a frame sheet of every event.
  The HUD is hidden on all scan shots, the cold-open walk-out and the end card.
- **Captions (CAP_v2):** bottom-centre, y 900-1010, at most 2 lines of 42 characters, white on a 55 % black rounded backing. Shown only on sync.
- **Stings and overlays:** lower-left x 80-900, y 640-860, or lower-right x 1020-1840, y 640-860. Always above the caption band and clear of faces.
- **Black cards (3):** C_03 "SCANNER CRASHED", C_07 "REBOOTING..." with the clock fast-forward, END.

## Clock model v2

| clock | legible in frame | said | between readings |
|---|---|---|---|
| CLOCK 1 (phone, from "go") | 541@72 00:00.00 · 541@75 00:00.43 · **541@190 01:55.47** · **541@192 01:57.46** · 541@298 03:43.44 · 541@300 03:45.43 · 541@374 04:59.52 · 541@404 05:29.46 · 542@24 12:20.75 · 544@45 17:53.38 · 546@0 "21:--" · **553@16.14 32:53.18** | "Five minutes on the dot" 541 [06:11.5]; "Just two minutes" 541 [03:21]; "32 minutes" 553 [00:14.5] | 541/542/544: real time from the faces. **545: unknown** (CLOCK 1 lost ~75 s in the review), so it shows "running" with no digits. **546-553: DERIVED** = camera clock − 18:10:00.9. This is anchored on 32:53.18 and agrees with 546@0 "21:--" (21:02). Frozen at 32:53, then "32 MIN" |
| TIMER 2 (watch, after the reboot) | 542@16 00:03.00 · 544@30 05:28.64 · 545@56 08:32.23 (stopped) · 546@5 08:46.40 · 547@66 11:17.36 · 548@7 13:05.01 · 551@30 15:31.30 · 553@9 20:24.95 | "8 minutes and 32 seconds" 545 [01:01.5]; "20 minutes" 553 [00:09.7] | Real time from the faces. 550/552: derived from the camera clock. Paused at 08:32 (G07_v2). Frozen at 20:24, then "20 MIN" |

The one interpolated value is C_07 (CLOCK 1 05:49 >> 11:56 on the reboot card, between 541@404 and 542@24).

## How long the spraying took: the evidence

- **Start:** "go" at 541 src 74.6. The phone reads 00:00.43 at 541@75.0 (legible). The first spray hits the front bumper at 541 ≈96.5 s, i.e. about 00:22 on the clock (derived, not legible). 82-94 s is filling and showing the spray gun.
- **End:** in P_04 the host says he will "show the watch" when he is done spraying (541 [01:46.7]). The spray gun is last in use at ≈186 s.
  The phone is then shown at **01:55.47 (541@190)** and **01:57.46 (541@192)**, both legible. At 200-202 s the gun goes back on the bench, and someone says "Checkpoint. Just two minutes." (541 [03:21]).
  Later, FX30545 [01:03] refers to "the 2 minutes of spraying".
- **On screen:** **SPRAY DONE · 01:55 ON THE CLOCK** (G_SPRAY_v2). The number is the legible 01:55.47, and the stamp claims no more than it shows (it includes ~22 s of set-up from "go").
  The time-lapse P_05 runs the real clock 00:39 -> 01:55 at 20x over 541 114.24-189.80, so the duration is visible, not just stated.
  We do **not** claim a spray-only time (1:33 would rest on a derived start).

## The crash set-piece (C_01-C_08, 1:14.33-2:00.14)

| beat | event | picture | sound / music |
|---|---|---|---|
| Confidence | (P_02 earlier) "I'm so confident in my ability, I'm not gonna rush" | | callback: the crash plays against it |
| Tension | C_01 1:14.33-1:25.10 | "Time check" ... watch 04:57 / phone 04:59 in shot; "Five minutes on the dot"; "How you feeling halfway through it?" | **TENSE PIECE starts at 1:14.33 and builds 10.8 s** to a peak exactly on "crashed" |
| It dies | C_01 1:25.10-1:28.85 | "It just crashed." The host lifts the scanner and laughs: "It's never crashed on me before." Ends on the scanner screen in his hand | **MUSIC HARD STOP on "crashed" (1:25.10)**; room tone only under "never crashed on me before" |
| Freeze | C_02 1:28.85-1:29.85 | Freeze on the dead scanner screen; 2-frame stutter, RGB split, scanlines, desaturate. CLOCK 1 keeps counting, turns red: "● STILL RUNNING" | power-down SFX + digital crackle, then **0.4 s of dead silence** |
| Card | C_03 1:29.85-1:31.05 | BLACK CARD 1: glitched "SCANNER CRASHED"; the clock overlay still counts | sub drone enters (low, ~40 Hz) |
| Still running | C_04-C_06 1:31.05-1:39.19 | "We're still rolling."; phone 05:29.46; "once this is sorted out, I'm just gonna start a new scan" | drone + a tick layer synced to the phone's seconds, ducked under speech |
| Reboot wait | C_07 1:39.19-1:42.19 | BLACK CARD 2: "REBOOTING..." with the big clock fast-forwarding 05:49 >> 11:56 | accelerating ticks + 3.0 s riser |
| Comeback | C_08 1:42.19-2:00.14 | "So, what happened? So the scanner crashed..." facepalm, "start a secondary timer. Now." Watch 00:03 | drone under the speech; **RELEASE on "Now." (1:55.79)**: the upbeat game music returns. TIMER 2 appears |

**Music needed for the crash:**
- **(a) Tense cue, ≥ 11 s.** It must rise to a hard, cuttable peak, or end on a button, at 1:25.10.
- **(b) Drone / pulse bed, ~30.7 s** (1:25.1-1:55.8). It must be loopable and sit under speech, with a tick at ~1 Hz that can be doubled for C_07.
- **(c) Release.** The main game-music piece re-enters on a downbeat or drop at 1:55.79 ("Now."). Pick a bar that lands within ±0.15 s; dialogue may not move.

## The end montage (M1-M6, 4:15.02-4:48.52)

Five pairs. Each pair is real scanning from one angle, then a HARD 1:1 cut on a kick to the scan from the same camera, then on to the next real shot on the following kick.
Pace builds: IRL/scan 3.0/3.0 -> 2.75/2.75 -> 2.5/2.5 -> 2.25/2.25 -> 2.5/3.0. Then **SC_RES_FULL** as the 7 s hero, then the conclusion. No HUD and no text except G10_v2 on the hero.
IRL->scan cuts land at **4:18.02, 4:23.77, 4:29.02, 4:33.77, 4:38.52**. The hero starts at 4:41.52 (music lift there).

| slot | IRL | scan | status |
|---|---|---|---|
| PAIR_1 | FX30542 44.381-47.381 (ends on the solved f1135) | SC_MATCH_REAR 0-3.0 | solved |
| PAIR_2 | 2.75 s ending on a solved frame | SC_PAIR_2 2.75 s | **slot** |
| PAIR_3 | 2.50 s | SC_PAIR_3 2.50 s | **slot** |
| PAIR_4 | 2.25 s | SC_PAIR_4 2.25 s | **slot** |
| PAIR_5 | FX30554 8.553-11.053 (ends on f264) | SC_MATCH_FRONT 0-3.0 | solved; also teased in the cold open (deliberate bookend) |

**Rule for filling PAIR_2-4** (`scan_shots.md` does not list the new pairs yet):
1. Three different parts. None may be the rear bumper or the front fascia (already taken), and no part twice.
2. The IRL frame must come from **un-jacked** footage: 541, 542, 543, 544, 545, or 553 from 6 s on. Jacking starts in 546 and the ride height changes, so 546-552 cannot match the scan.
3. The 2-3 s before the solved frame must show real scanning (scanner or host in action) on a steady camera, with no whip.
4. No range the body uses. Body ranges: 541 14-30, 70-114, 189-202, 247-250, 285-299, 321-325, 347-424; 542 0-25, 64-68, 110-114, 168-172; 544 4-8, 29-31, 44-46; 545 53-63, 94-124.
5. **Candidates kept free for the 3D agent:**
   - 541 212-221 (rear right quarter and taillight)
   - 541 227-242 (trunk lid / rear deck, side view)
   - 542 216-232 (hood and windshield)
   - 544 120-135 (lower door / sill line)
   - 545 8-16 (rear-left quarter and wheel; 4K raw, upright)
6. Order PAIR_2-4 by solve quality, worst first, so the strongest cuts come last. Alternate sides and heights.
7. If only 2 new pairs arrive: drop PAIR_4 and give PAIR_3 2.5/2.5. If only 1 arrives: montage = REAR, PAIR_2, FRONT, with the hero at 8 s. Runtime stays above 5:00 either way.

## What I need from the 3D agent

- **SC_MATCH_FRONT, 5.0 s.** It is used twice: frames 0-5.0 in CO_03, with the title from +2.0 s and the lower third clean, and frames 0-3.0 in M5_B.
- **SC_MATCH_REAR:** 0-3.0 s (the 4.5 s render is fine).
- **SC_PAIR_2/3/4:** 2.75 / 2.5 / 2.25 s each, plus 0.5 s handle. Frame 1 must equal the solved IRL frame.
- **SC_RES_FULL:** 7.0 s, one continuous move, not a turntable.
- **SC_CON_HERO:** 8.0 s of the planned 11.76 s, lower-left kept clear for the CTA.
- **No longer needed:** SC_TITLE, SC_RES_MESH, SC_RES_REFLECTOR, SC_INS_ROOF, SC_INS_WHEEL, SC_INS_SILL.
- **Plates:** the owner says do not blur IRL plates. Renders stay "as delivered by the 3D agent" (currently flattened).

## Music map v2 (timeline times; hit points are fixed, everything else snaps)

| span | need |
|---|---|
| 0:00-0:05.8 | light, curious; **hit on the 1:1 cut at 0:05.80** (CO_02 -> CO_03) |
| 0:05.8-0:21.5 | title swell, then playful under the three answers (ducked) |
| **0:24.95** | **DROP on "go."** |
| 0:32.38 | small hit for STING1 "PART 1 · SPRAY" |
| 0:43.93-0:47.71 | **3.8 s riser / fast-forward fill** under the time-lapse, **landing hit at 0:47.71** on the phone (01:55) |
| 0:55.42 | small hit for STING2 "PART 2 · SCAN" |
| 1:14.33-1:55.79 | crash cues (a), (b), (c) above |
| 1:55.79-4:01 | main game music; highest energy in the hard parts (2:59.8-4:00.8) |
| **4:01.07** | **stop / sting on "Time."** |
| 4:15.02-4:41.52 | montage: kicks on each IRL->scan cut (4:18.02, 4:23.77, 4:29.02, 4:33.77, 4:38.52); intensity builds |
| **4:41.52** | **lift** for the hero |
| 4:48.5-5:11.7 | resolve under the conclusion, out on the end card |

## Sections (shot tables)

### 1 COLD OPEN (0:00.00-0:10.80, 10.8 s)

Hook: the first guess, then the strongest real-to-scan cut as a 2 s tease, with the title over the scan.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| CO_01 | 0:00.00-0:03.80 | FX30541 14.750-18.550 | Crew member in a dark tee, to camera (take 2 of the question) | "How long do you think it'll take to scan this car?" / "I'll say two hours." [541 [00:15.0]-[00:18.1]] **PROTECTED** lead 0.25 / tail 0.41 | C1 00:00-00:00; -; TR | CAP_v2, G02_v2 | Take 2 replaces take 1: take 1 has no clean out (next speaker starts ~3.0 s). Rail-free: clock overlay shows 00:00 dimmed. Prev word "Okay." ends 14.40; next "How" 19.70. |
| CO_02 | 0:03.80-0:05.80 | FX30554 9.053-11.053 | Walk out of the shop door to the powdered car in the sun; ENDS on solved frame 264 (11.011 s) | music only | hidden | - | TEASE of the strongest pair (front, RMSE 0.4 px). Bookend: the same pair closes the end montage (M5) - deliberate. out = 11.011 + 1/23.976 (fixed). |
| CO_03 | 0:05.80-0:10.80 | SC_MATCH_FRONT (5.00 s) | HARD 1:1 CUT on a hit to the scan from the same camera; slow push. Title lands at +2.0 s | music only | hidden | G01_v2 | Replaces SC_TITLE (no body scans in v2). Uses render frames 0-5.0 s. |

### 2 THE BET (0:10.80-0:21.47, 10.7 s)

Two more takes of the same question: "30 minutes", then the host's bet of 15. Chips build top-left.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| B_01 | 0:10.80-0:14.55 | FX30541 19.450-23.200 | Question (take 3), crew member in black polo + lanyard answers | "How long do you think it'll take to scan this car?" / "Maybe 30 minutes." [541 [00:19.7]-[00:22.7]] **PROTECTED** lead 0.25 / tail 0.40 | C1 00:00-00:00; THE BET; TR | CAP_v2, G02_v2 | v1 E06 started on the tail of "car?". Next word "How" 23.88. |
| B_02 | 0:14.55-0:21.47 | FX30541 23.630-30.550 | Question (take 4); the host (Berkeley tee) answers to camera, grinning | "How long do you think it'll take to scan this car?" / "I think I can do it in less than the length of a YouTube video. 15 minutes." [541 [00:23.9]-[00:30.2]] **PROTECTED** lead 0.25 / tail 0.40 | C1 00:00-00:00; THE BET; TR | CAP_v2, G02_v2, G03_v2 | Energy shows speech ends ~30.15; there is no "of course" (large-v3 artefact). v1 out 30.03 clipped "minutes". Next words 32.23. |

### 3 PART 1 - SPRAY (0:21.47-0:55.42, 34.0 s)

The clock starts. Three distinct spray shots: front (P_03), side with the "show the watch" line (P_04), and a time-lapse of the rest (P_05) that lands on the phone at 01:55. Then the powdered car and "Just two minutes".

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| P_01 | 0:21.47-0:25.69 | FX30541 70.750-74.970 | Phone stopwatch 00:00.00 in hand, start pressed | "Huh?" "Yeah." "Three, two, one, go." [541 [01:11.0]-[01:14.6]] **PROTECTED** lead 0.26 / tail 0.40 | C1 00:00-00:00; PART 1 · SPRAY; TR | CAP_v2 | MUSIC DROP on "go." (src 74.23). CLOCK 1 starts at src 74.6. v1 started inside "Yeah". |
| P_02 | 0:25.69-0:32.38 | FX30541 77.090-83.780 | Bench: scanner on its stand, powder bottle, spray gun being filled | "I'm so confident in my ability, I'm not gonna rush. I gotta take my time." / "Oh no, oh no, that's not the right one." [541 [01:17.3]-[01:23.4]] **PROTECTED** lead 0.25 / tail 0.40 | C1 00:02-00:09; PART 1 · SPRAY; TR | CAP_v2 | v1 cut "time" mid-word (81.0). The "Oh no" is kept: it completes the moment and foreshadows. Next words 88.26 ("Artec ad" line, excluded). |
| P_03 | 0:32.38-0:36.18 | FX30541 96.800-100.600 | First spray: the front bumper and grille (host crouched at the plate) | music only | C1 00:22-00:26; PART 1 · SPRAY; TR | STING1_v2 | Spray shot 1 of 3 (front). Source audio muted; spray gun hiss may be mixed in at -18 dB. |
| P_04 | 0:36.18-0:43.93 | FX30541 106.490-114.240 | Spray shot 2 of 3 (side): spraying along the side panels | "Then when I'm done spraying the car, show the watch. Okay, I'm gonna show the watch periodically." / "Yeah, checkpoint." [541 [01:46.7]-[01:53.8]] **PROTECTED** lead 0.25 / tail 0.40 | C1 00:31-00:39; PART 1 · SPRAY; TR | CAP_v2 | v1 out 111.49 cut "...show the [watch periodically]". medium.en heard "lock"; large-v3 "watch" (use "watch"). |
| P_05 | 0:43.93-0:47.71 | FX30541 114.240-189.800 @20x | TIME-LAPSE (spray shot 3 of 3): the rest of the car goes matte, roof, rear, wheels, at 20x | music only | C1 00:39-01:55; clock runs at 20x showing the true value for each source frame; ">> 20x" glyph; PART 1 · SPRAY; TR | TL_v2 | 75.56 s of source at 20x = 3.78 s. Frame-blend or optical-flow ramp; keep it one continuous take (no cuts). CLOCK 1 runs at the true value for each source frame (00:39 -> 01:55), with a ">> 20x" glyph. |
| P_06 | 0:47.71-0:50.71 | FX30541 189.800-192.800 | Phone stopwatch: 01:55.47 (src 190) -> 01:57.46 (src 192), as promised in P_04 | music only | C1 01:55-01:58; PART 1 · SPRAY; TR | G_SPRAY_v2 | Real speed. Lands the time-lapse on the hit. Phone sits centre-left; G_SPRAY_v2 goes lower-right. |
| P_07 | 0:50.71-0:53.71 | FX30541 194.000-197.000 | The fully powdered car, front, static | music only | C1 01:59-02:02; PART 1 · SPRAY; TR | - | Spray result held 3 s. No plate blur (owner). |
| P_08 | 0:53.71-0:55.42 | FX30541 200.760-202.470 | Host puts the spray gun down at the bench | "Checkpoint. Just two minutes." [541 [03:21.0]-[03:22.1]] **PROTECTED** lead 0.25 / tail 0.40 | C1 02:06-02:07; PART 1 · SPRAY; TR | CAP_v2 | NEW. The spoken corroboration of the spray time. large-v3 heard "He's two minutes"; medium.en (transcript) "Check point. Just two minutes." Caption check by ear. Next words 203.88 (third-party chatter, excluded). |

### 4 PART 2 - SCAN (0:55.42-1:14.33, 18.9 s)

The subsection sting, then the first passes and a coverage check. Q_01 is muted (brand line underneath).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| Q_01 | 0:55.42-0:58.42 | FX30541 247.000-250.000 | Host with the scanner for the first time, grinning; live view on its screen | music only | C1 02:52-02:55; PART 2 · SCAN; TR | STING2_v2 | NEW. Source audio MUTED: it carries the excluded "with the Artec Leo, that's a thing of the past" (244.2-248.1). |
| Q_02 | 0:58.42-1:02.42 | FX30541 285.500-289.500 | Scanner close-up passing along the car | music only | C1 03:30-03:34; PART 2 · SCAN; TR | - | - |
| Q_03 | 1:02.42-1:03.92 | FX30541 297.500-299.000 | Phone stopwatch 03:43.44 (src 298) | music only | C1 03:42-03:44; PART 2 · SCAN; TR | - | - |
| Q_04 | 1:03.92-1:07.92 | FX30541 321.000-325.000 | Host bent low, scanning the side of the car | music only | C1 04:06-04:10; PART 2 · SCAN; TR | - | NEW (replaces the roof re-spray E19, a spray repeat). |
| Q_05 | 1:07.92-1:14.33 | FX30541 347.370-353.780 | Host with scanner points out a spot; crew member with spray gun | "The corner of the left headlight. You see how it's like not fully covered?" / "Got you." [541 [05:47.6]-[05:53.4]] **PROTECTED** lead 0.25 / tail 0.40 | C1 04:32-04:39; PART 2 · SCAN; TR | CAP_v2 | v1 out 353.35 clipped "Got you." Next words 357.27. |

### 5 THE CRASH (1:14.33-2:00.14, 45.8 s)

The set-piece (spec above).

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| C_01 | 1:14.33-1:28.85 | FX30541 368.830-383.350 | Crew around the host; analog watch 04:57.46 (src 372) and phone 04:59.52 (src 374) in shot; host lifts the scanner and laughs; ends on the scanner screen in his hand | "Time check." / "What? Oh, it's switched. Five minutes on the dot." / "How you feeling halfway through it?" / "It just crashed. It's never crashed on me before." [541 [06:09.1]-[06:22.9]] **PROTECTED** lead 0.25 / tail 0.40 | C1 04:54-05:08; PART 2 · SCAN — THE CRASH; TR | CAP_v2 | One continuous take. Tense music builds from the first frame; MUSIC HARD STOP on "crashed" (src 379.60). From there: room tone only. Speech ends ~382.95 (energy); whisper's "Okay" at 382.7 is a mis-time (medium.en: 388.6). |
| C_02 | 1:28.85-1:29.85 | FX30541 383.350-384.350 (freeze 1.0 s) | FREEZE on the last frame of C_01 (the dead scanner screen in hand) + glitch: 2-frame stutter, RGB split, scanlines, desaturate to 30 % | music only | C1 05:08-05:09; picture frozen; CLOCK 1 keeps counting in red ("● STILL RUNNING"); PART 2 · SCAN — THE CRASH; TR | G_FREEZE_v2 | Picture frozen 1.0 s; the CLOCK 1 overlay keeps counting (05:08 -> 05:09) and turns red. SFX: power-down + digital crackle, then 0.4 s of dead silence. |
| C_03 | 1:29.85-1:31.05 | gfx:G05a_v2 (1.20 s) | BLACK CARD 1 of 3: glitched text "SCANNER CRASHED" | music only | clock overlay stays on the card and keeps counting; PART 2 · SCAN — THE CRASH; TR | G05a_v2 | Clock overlay stays on the card, still counting (05:09 -> 05:10). Sound: low sub drone enters. |
| C_04 | 1:31.05-1:33.22 | FX30541 400.330-402.500 | Host walking with scanner and spray gun | "We're still rolling." [541 [06:40.6]-[06:42.1]] **PROTECTED** lead 0.25 / tail 0.40 | C1 05:25-05:27; PART 2 · SCAN — THE CRASH; TR | CAP_v2 | medium.en: "timer's still rolling". Drone continues under. |
| C_05 | 1:33.22-1:35.02 | FX30541 403.800-405.600 | Phone stopwatch 05:29.46 (src 404): the clock is still running | music only | C1 05:29-05:31; PART 2 · SCAN — THE CRASH; TR | G_FREEZE_v2 | Room tone + drone + a ticking layer synced to the phone. |
| C_06 | 1:35.02-1:39.19 | FX30541 410.550-414.720 | Host with the spray gun | "Yeah, once this is sorted out, I'm just gonna start a new scan." / "Yeah, I know." [541 [06:50.8]-[06:54.3]] **PROTECTED** lead 0.25 / tail 0.40 | C1 05:35-05:40; PART 2 · SCAN — THE CRASH; TR | CAP_v2 | medium.en hears "cuz" from 414.2; if audible, end at 414.72 still clean (check by ear). |
| C_07 | 1:39.19-1:42.19 | gfx:G05b_v2 (3.00 s) | BLACK CARD 2 of 3: big centred CLOCK 1 fast-forwarding 05:49 -> 11:56 under "REBOOTING..." | music only | CLOCK 1 fast-forwards 05:49 -> 11:56 big and centred (INTERPOLATED, ">>"); PART 2 · SCAN — THE CRASH; TR | G05b_v2 | INTERPOLATED clock between legible 05:29.46 (541@404) and 12:20.75 (542@24). Sound: drone + accelerating tick, riser into C_08. |
| C_08 | 1:42.19-2:00.14 | FX30542 0.000-17.950 | Host at the bench, facepalm (3-5 s), scanner and spray gun, then the watch: TIMER 2 at 00:03.00 (src 16) | "So, what happened? So the scanner crashed. So after like a five minute delay, we're rebooting it. And now we're gonna try again. All right, let's start the... start a secondary timer. Now." / "Yup." [542 [00:00]-[00:17.5]] **PROTECTED** lead 0.00 / tail 0.45 | C1 11:56-12:14; T2 00:00-00:04; PART 2 · SCAN — THE CRASH; TR | CAP_v2, G06_v2 | One continuous take (v1 jump-cut through "So" at 2.5 and lost "Yup" at ~17). Clip starts on the first word: pre-roll 0.25 s of room tone from 542 14.70-14.95. MUSIC RELEASE on "Now." (energy ~13.6): the upbeat game music returns. TIMER 2 appears at src 13.0. Next words 18.22 (medium only). |

### 6 TRY AGAIN (2:00.14-2:59.80, 59.7 s)

Clean restart passes with both clocks; exterior done (TIMER 2 stopped at 08:32); the review on the scanner screen (4K original, full frame); "let's also time that".

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| T_01 | 2:00.14-2:01.54 | FX30542 23.600-25.000 | Phone stopwatch 12:20.75 (src 24) | music only | C1 12:20-12:21; T2 00:10-00:12; PART 2 · SCAN — TRY AGAIN; TR | - | - |
| T_02 | 2:01.54-2:05.54 | FX30542 64.000-68.000 | Host scanning the side glass and roof edge, arm raised | music only | C1 13:00-13:04; T2 00:51-00:55; PART 2 · SCAN — TRY AGAIN; TR | - | NEW (replaces the rear pass, which moved to the montage). |
| T_03 | 2:05.54-2:09.54 | FX30542 110.000-114.000 | Scanner screen close: the live scan filling in | music only | C1 13:46-13:50; T2 01:37-01:41; PART 2 · SCAN — TRY AGAIN; TR | - | NEW. |
| T_02b | 2:09.54-2:13.54 | FX30542 168.000-172.000 | Host "dual wielding": scanner in one hand, spray gun in the other | music only | C1 14:44-14:48; T2 02:35-02:39; PART 2 · SCAN — TRY AGAIN; TR | - | NEW. Source audio muted. |
| T_04 | 2:13.54-2:17.54 | FX30544 4.000-8.000 | Host kneeling, scanning the lower front fender in the doorway light | music only | C1 17:12-17:16; T2 05:02-05:06; PART 2 · SCAN — TRY AGAIN; TR | - | - |
| T_05 | 2:17.54-2:18.94 | FX30544 29.600-31.000 | Watch: TIMER 2 05:28.64 (src 30) | music only | C1 17:37-17:39; T2 05:28-05:29; PART 2 · SCAN — TRY AGAIN; TR | - | - |
| T_06 | 2:18.94-2:20.34 | FX30544 44.600-46.000 | Phone lock screen: CLOCK 1 17:53.38 (src 45) | music only | C1 17:52-17:54; T2 05:43-05:44; PART 2 · SCAN — TRY AGAIN; TR | - | - |
| T_07 | 2:20.34-2:30.42 | FX30545 53.140-63.220 | 4K original, upright, full frame: the watch stopped at 08:32.23 (src 56), the host | "So, are you still recording?" "Yep." "So that's the exterior. That's done. Check mark. What's the time?" "The cheating time is 8 minutes and 32 seconds." [545 [00:53.4]-[01:03.0]] **PROTECTED** lead 0.25 / tail 0.20 | C1 running, no digits; T2 08:29-08:32; PART 2 · SCAN — TRY AGAIN; TR | CAP_v2, G07_v2 | EXCEPTION: tail 0.20 s only. The next sentence ("Is that with the 2 minutes of spraying? ... 20 minutes with the crash") is excluded and starts at ~63.3 (energy). Beat-snap may NOT lengthen past 63.22; use a 3-frame audio fade-out. |
| T_08 | 2:30.42-2:59.80 | FX30545 94.600-123.980 | 4K original, upright, full frame: the scan of the car turning on the scanner screen under his thumb (95-113), then the host (115-124) | "This is the full walk around of the car. Front, hood, roof, right side. Rear quarter panel's a little messed up. Roof's messed up. So I came back here, did the whole roof, did the right quarter panel, fixed the trunk." / "That's the full interior. So now, if you wanna make a lip kit, let's jack the car up, do the fronts and sides, wheel wells inside. So let's also time that." [545 [01:34.9]-[02:03.6]] **PROTECTED** lead 0.25 / tail 0.40 | C1 running, no digits; T2 08:32-08:32; PART 2 · SCAN — TRY AGAIN; TR | CAP_v2, G07_v2 | One take (the cabin insert E41 is gone). Clip ends 124.62. |

### 7 THE HARD PARTS (2:59.80-4:00.77, 61.0 s)

Jacks, arches, the floor; the lost-and-found can; "almost done". Watch faces punctuate it. No scan inserts.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| H_01 | 2:59.80-3:01.80 | FX30546 4.600-6.600 | Watch: TIMER 2 08:46.40 -> 08:47.40, running again | music only | C1 21:06-21:08 (derived); T2 08:46-08:48; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_02 | 3:01.80-3:05.30 | FX30546 59.500-63.000 | Host working the floor jack | music only | C1 22:01-22:05 (derived); T2 09:40-09:44; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_03 | 3:05.30-3:09.00 | FX30547 0.000-3.700 | Host holds up the spray can | "For harder-to-reach areas, I'll use the can." [547 [00:00.1]-[00:03.3]] **PROTECTED** lead 0.08 / tail 0.40 | C1 22:32-22:35 (derived); T2 10:11-10:15; PART 2 · SCAN — THE HARD PARTS; TR | CAP_v2 | v1 out 3.045 clipped "can." Clip starts 0.08 s before the first word: pre-roll room tone 0.2 s from 547 3.75-3.95. |
| H_04 | 3:09.00-3:12.50 | FX30547 36.000-39.500 | Spray can into the front wheel arch | music only | C1 23:08-23:11 (derived); T2 10:47-10:50; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_05 | 3:12.50-3:17.00 | FX30547 53.500-58.000 | Live scan on the scanner screen beside the wheel | music only | C1 23:25-23:30 (derived); T2 11:04-11:09; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_06 | 3:17.00-3:18.40 | FX30547 65.600-67.000 | Watch: TIMER 2 11:17.36 (src 66) | music only | C1 23:37-23:39 (derived); T2 11:16-11:18; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_07 | 3:18.40-3:24.25 | FX30547 120.250-126.100 | Host lying on the floor scanning under the front | "It's a crazy position." "Is this the most optimal scanning position?" "Yeah." [547 [02:00.5]-[02:05.6]] **PROTECTED** lead 0.25 / tail 0.47 | C1 24:32-24:38 (derived); T2 12:11-12:17; PART 2 · SCAN — THE HARD PARTS; TR | CAP_v2 | Speech starts ~120.5 (energy; whisper's "It's" at 113.4 is a drift). Never past 126.8: 127-133 is the "can't wait to blur that" span. |
| H_08 | 3:24.25-3:26.25 | FX30548 6.200-8.200 | Watch: TIMER 2 13:05.01 (src 7) | music only | C1 25:25-25:27 (derived); T2 13:04-13:06; PART 2 · SCAN — THE HARD PARTS; TR | - | Source audio muted (the jack call names a crew member). |
| H_09 | 3:26.25-3:30.25 | FX30550 12.000-16.000 | Jacking the rear up | music only | C1 26:51-26:55 (derived); T2 14:30-14:34 (derived); PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_10 | 3:30.25-3:33.70 | FX30551 0.000-3.450 | Floor / under the car: the spray can went missing | "Oh, under the car! It disappeared!" [551 [00:00]-[00:03.0]] **PROTECTED** lead 0.00 / tail 0.40 | C1 27:22-27:25 (derived); T2 15:01-15:04; PART 2 · SCAN — THE HARD PARTS; TR | CAP_v2 | Clip starts on the first word (pre-roll room tone 0.25 s from 551 3.4-3.65). medium.en hears "Under the car, it's just over here" (2.3-3.0 is speech): caption check by ear. HARD LIMIT 3.90: profanity from ~4.3. |
| H_11 | 3:33.70-3:40.21 | FX30551 13.450-19.960 | The can found, white on the powdered floor | "Oh, it's right here. Right?" "Oh yeah, it is. It blended in." "I do the same thing all the time." [551 [00:13.7]-[00:19.6]] **PROTECTED** lead 0.25 / tail 0.40 | C1 27:35-27:42 (derived); T2 15:14-15:21; PART 2 · SCAN — THE HARD PARTS; TR | CAP_v2 | NEW (payoff of H_10). Caption check by ear; large-v3 puts "I feel like Tom Cruise" at 81.9 (drift) - if it is audible right after 19.6, end at 19.96 anyway. |
| H_12 | 3:40.21-3:41.61 | FX30551 29.600-31.000 | Watch: TIMER 2 15:31.30 (src 30) | music only | C1 27:51-27:53 (derived); T2 15:30-15:32; PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_13 | 3:41.61-3:47.31 | FX30551 84.000-89.700 | Host lying under the car scanning the sill | music only | C1 28:46-28:51 (derived); T2 16:25-16:31; PART 2 · SCAN — THE HARD PARTS; TR | - | Out before the cat noises (89.9). |
| H_14 | 3:47.31-3:51.77 | FX30552 19.160-23.620 | Host scanning low by the car | "Okay." "Done?" "Nope." "Oh yeah, almost done." [552 [00:19.4]-[00:23.2]] **PROTECTED** lead 0.25 / tail 0.41 | C1 30:33-30:37 (derived); T2 18:12-18:16 (derived); PART 2 · SCAN — THE HARD PARTS; TR | CAP_v2 | - |
| H_15 | 3:51.77-3:55.77 | FX30552 48.000-52.000 | Under the rear wheel arch beside the jack | music only | C1 31:02-31:06 (derived); T2 18:41-18:45 (derived); PART 2 · SCAN — THE HARD PARTS; TR | - | - |
| H_16 | 3:55.77-4:00.77 | FX30552 100.000-105.000 | Host flat on his back scanning upward | music only | C1 31:54-31:59 (derived); T2 19:33-19:38 (derived); PART 2 · SCAN — THE HARD PARTS; TR | - | Biggest energy; cut to TM_01 on a bar line. |

### 8 TIME (4:00.77-4:15.02, 14.2 s)

The answer in one take, with legible faces for both clocks; the scoreboard overlay, then the bet result over the hood.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| TM_01 | 4:00.77-4:12.02 | FX30553 7.300-18.550 | Watch: TIMER 2 20:24.95 (src 9) fills the frame; host; phone CLOCK 1 32:53.18 (src 16.14) | "Time. 20 minutes. Done. And the other one, 32 minutes. Yep." [553 [00:07.6]-[00:18.1]] **PROTECTED** lead 0.30 / tail 0.45 | C1 32:44-32:53; T2 20:23-20:24; TIMER 2 runs to 20:24 at src 9.0 and freezes; CLOCK 1 runs to 32:53 at src 16.14 and freezes; at src 17.6 both flip to "32 MIN" / "20 MIN" (owner) and stay frozen to the end; TIME; TR | CAP_v2, G08_v2 | One continuous take (v1 split it into E61 + card E62 and clipped "Yep" at 18.08). Music stops / stings on "Time." (src ~7.6). TIMER 2 freezes at 20:24 at src 9.0; CLOCK 1 freezes at 32:53 at src 16.14 (legible); both then flip to the owner numbers. |
| TM_02 | 4:12.02-4:15.02 | FX30553 39.500-42.500 | The hood up close: the powder already clearing in X-shaped marks | music only | C1 32 MIN-32 MIN; T2 20 MIN-20 MIN; TIME; TR | G09_v2 | Source audio muted (names a crew member at 35.7). Replaces the black bet card. |

### 9 THE SCAN (END MONTAGE) (4:15.02-4:48.52, 33.5 s)

Spec above. The HUD is hidden.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| M1_A | 4:15.02-4:18.02 | FX30542 44.381-47.381 | Host crouched scanning the rear bumper (solved frame 1135 = 47.339 s) | music only | hidden | - | Ends on the solved frame (fixed src_out; beat snap moves src_in only). v1 E32. |
| M1_B | 4:18.02-4:21.02 | SC_MATCH_REAR (3.00 s) | Rear bumper scan, slow push | music only | hidden | - | HARD 1:1 cut on a kick; first frame = the IRL frame. |
| M2_A | 4:21.02-4:23.77 | PAIR_2_IRL (3D agent: clip + solved frame) (2.75 s) | PAIR_2: real scanning of part 2 from the solved angle | music only | hidden | - | SLOT: fill per the pair rule in script_v2.md.  |
| M2_B | 4:23.77-4:26.52 | SC_PAIR_2 (2.75 s) | Scan of part 2 from the same camera | music only | hidden | - | HARD 1:1 cut on a kick; first frame = the IRL frame. |
| M3_A | 4:26.52-4:29.02 | PAIR_3_IRL (3D agent: clip + solved frame) (2.50 s) | PAIR_3: real scanning of part 3 | music only | hidden | - | SLOT: fill per the pair rule in script_v2.md.  |
| M3_B | 4:29.02-4:31.52 | SC_PAIR_3 (2.50 s) | Scan of part 3 from the same camera | music only | hidden | - | HARD 1:1 cut on a kick; first frame = the IRL frame. |
| M4_A | 4:31.52-4:33.77 | PAIR_4_IRL (3D agent: clip + solved frame) (2.25 s) | PAIR_4: real scanning of part 4 | music only | hidden | - | SLOT: fill per the pair rule in script_v2.md.  |
| M4_B | 4:33.77-4:36.02 | SC_PAIR_4 (2.25 s) | Scan of part 4 from the same camera | music only | hidden | - | HARD 1:1 cut on a kick; first frame = the IRL frame. |
| M5_A | 4:36.02-4:38.52 | FX30554 8.553-11.053 | Walk-out into the sun (solved frame 264 = 11.011 s) | music only | hidden | - | Ends on the solved frame (fixed src_out; beat snap moves src_in only). v1 E66. |
| M5_B | 4:38.52-4:41.52 | SC_MATCH_FRONT (3.00 s) | Front scan, slow push (bookend of the cold-open tease) | music only | hidden | - | HARD 1:1 cut on a kick; first frame = the IRL frame. |
| M6 | 4:41.52-4:48.52 | SC_RES_FULL (7.00 s) | HERO: whole car, one continuous dolly side -> front-left 3/4 (not a turntable) | music only | hidden | G10_v2 | Music lift on the first frame. |

### 10 CONCLUSION (4:48.52-5:06.67, 18.1 s)

See "Conclusion v2" below.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| CON_01 | 4:48.52-4:58.67 | FX30555 11.500-21.650 | Host to camera outdoors with scanner + spray gun, crew member behind, the powdered car | "If we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car, 10 minutes if I just did the exterior, with the power of a spray gun, AESUB Violet, and the Artec Leo." [555 [00:11.6]-[00:21.3]] **PROTECTED** lead 0.14 / tail 0.35 | C1 32 MIN-32 MIN; T2 20 MIN-20 MIN; THE ANSWER; TR | CAP_v2, CON_G1_v2 | Whole sentence (v1 cut it at "car," 15.77 mid-sentence). Starts at "If": "but" (11.18) runs into the other speaker's "30 minutes actual" with no gap; 11.50 sits in the 0.1 s silence before "If". EXCEPTION: tail 0.35 s (next sentence "I don't know if there's any other scanner ... faster" is excluded, starts 21.70). OWNER: the sentence says "10 minutes" and two product names (captions as spoken). Fallback if refused: 11.50-16.35 (ends on the 0.3 s pause after "whole car,"; no word cut) and lengthen CON_02 by 5.3 s. |
| CON_02 | 4:58.67-5:06.67 | SC_CON_HERO (8.00 s) | Whole car, front-left 3/4, one slow pull-back; lower-left clear | music only | hidden | CON_G3_v2 | v1 CON_02 (answer card), CON_03 ("this thing's fast": same sentence as the excluded claim) and CON_04 (triangle card) are removed. |

### 11 END CARD (5:06.67-5:11.67, 5.0 s)

Black card 3 of 3.

| id | time in-out | source (clip in-out s) | what we see | what we hear | HUD overlay (C1; T2; chapter; corner) | gfx | notes |
|---|---|---|---|---|---|---|---|
| END | 5:06.67-5:11.67 | gfx:G15_v2 (5.00 s) | BLACK CARD 3 of 3: logo + CTA | music only | hidden | G15_v2 | - |

## Graphic cues v2 (exact text, timeline, overlay position)

| id | type | text / sub | timeline | position | source |
|---|---|---|---|---|---|
| HUD_v2 | overlay cluster (replaces the v1 black rail) | CLOCK 1 MM:SS (large); TIMER 2 MM:SS (from C_08); chapter tag | 0:00.00-4:15.02 | top-right cluster x1480-1880 y40-200 (timer plate 400x96, 45 % black, 12 px radius; TIMER 2 row below; chapter tag 400x34 under it). Flip to TL when a face or the in-shot stopwatch enters x>1440,y<240 (editor checks every event on a frame sheet). Hidden on scan shots and the end card. | edl events hud.* |
| CAP_v2 | burned-in captions | verbatim sync words (events audio.hear), word-timed | 0:00.00-5:11.67 | bottom-centre, max 2 lines x 42 chars, y 900-1010, white, 55 % black rounded backing | large-v3 word JSON; medium.en where noted |
| G01_v2 | title overlay on SC_MATCH_FRONT | HOW FAST CAN WE 3D-SCAN AN ENTIRE CAR? — sub: LEXUS IS350 · ONE CAR · ONE STOPWATCH | 0:07.80-0:10.80 | lower third over the black below the car, white, halo | question; no numbers |
| G02_v2 | overlay chips (prediction tally) | 2 HR / 30 MIN / 15 MIN | 0:03.25-0:21.47 | top-left x40-600 y40-100, small pills; "2 HR" pops on "hours" (CO_01 src 18.0), "30 MIN" on B_01 src 22.4, "15 MIN" on B_02 src 29.7 (highlighted) | 541 [00:17.5], [00:22.1], [00:26.3]-[00:30.2] |
| G03_v2 | overlay | THE BET: 15 MINUTES | 0:20.62-0:21.47 | lower-left x80-900 y640-860 (above the caption band) (host is centre-right in B_02) | 541 [00:26.3] |
| STING1_v2 | subsection sting overlay | PART 1 · SPRAY | 0:32.38-0:33.98 | lower-left x80-900 y700-860, big, slides in on a hit and out | - |
| TL_v2 | overlay glyph on the time-lapse | >> 20x | 0:43.93-0:47.71 | beside CLOCK 1 in the HUD cluster | playback speed |
| G_SPRAY_v2 | overlay stamp | SPRAY DONE · 01:55 ON THE CLOCK | 0:48.01-0:53.71 | lower-right x1020-1840 y640-860 (phone is centre-left) | phone 01:55.47 legible at 541@190; corroborated by "Just two minutes" 541 [03:21] (P_08) and "the 2 minutes of spraying" 545 [01:03] |
| STING2_v2 | subsection sting overlay | PART 2 · SCAN | 0:55.42-0:57.02 | same as STING1_v2 | - |
| G_FREEZE_v2 | overlay treatment | ● STILL RUNNING | 1:28.85-1:35.02 | under CLOCK 1 in the HUD cluster, red; the clock digits turn red for the same span | 541 [06:40.6] "We're still rolling"; phone 05:29.46 at 541@404 |
| G05a_v2 | BLACK CARD 1/3 | SCANNER CRASHED | 1:29.85-1:31.05 | centre, glitched (RGB split, jitter) | 541 [06:19.5], 542 [00:01.7] |
| G05b_v2 | BLACK CARD 2/3 | REBOOTING... — sub: CLOCK 1 05:49 >> 11:56 (big, fast-forwarding) | 1:39.19-1:42.19 | centre | 542 [00:08] "we're rebooting it"; clock interpolated between 541@404 05:29.46 and 542@24 12:20.75 |
| G06_v2 | HUD element | TIMER 2 — sub: AFTER REBOOT | 1:55.19-4:15.02 | second row of the HUD cluster; from here TIMER 2 is the large number and CLOCK 1 the small one | 542 [00:12.6] "start a secondary timer. Now." |
| G07_v2 | HUD state | TIMER 2 08:32 ❚❚ | 2:23.20-2:59.80 | HUD cluster; CLOCK 1 row shows "running" without digits (no legible value in 545) | watch stopped at 08:32.23, 545@56; said 545 [01:01.5] |
| G08_v2 | scoreboard overlay on footage | CLOCK 1 · FROM "GO" · 32 MIN / TIMER 2 · WITHOUT THE CRASH · 20 MIN | 4:06.67-4:12.02 | lower-left x80-900 y640-860 (above the caption band); row 2 lands on the beat after "32 minutes"; keep clear of the phone at src 16 | owner (32 elapsed / 20 without the crash); said 553 [00:09.7] and [00:14.5]; legible 20:24.95 (553@9) and 32:53.18 (553@16.14) |
| G09_v2 | overlay | THE 15-MINUTE BET: MISSED — sub: CLOSEST GUESS: 30 MINUTES | 4:12.02-4:15.02 | lower-left x80-900 y640-860 (above the caption band) | 541 [00:26.3], [00:22.1]; owner 32/20 |
| G10_v2 | label on scan | LEXUS IS350 — sub: FULL CAR SCAN | 4:42.52-4:48.22 | bottom-left over black, halo | clips.md |
| CON_G1_v2 | answer overlay on CON_01 | 32 MIN FROM "GO" / 20 MIN WITHOUT THE CRASH / THE BET WAS 15 | 4:50.77-4:57.02 | top-left x60-760 y60-300, one line per beat (host is centre) | owner 32/20; 541 [00:26.3] 15 |
| CON_G3_v2 | CTA label on scan | LINK IN THE DESCRIPTION | 5:02.17-5:06.67 | bottom-left over black, halo | owner to choose the CTA (conclusion.md options) |
| G15_v2 | BLACK CARD 3/3 (end card) | ILLUMAESTHETIC — sub: [CTA sub line per owner choice] | 5:06.67-5:11.67 | logo 700+ px wide, centre | - |

Removed from v1: G04 (spray card -> STING1_v2 + time-lapse); G11 + SC_RES_MESH (triangles); G12/G13 + SC_RES_REFLECTOR (reflector); CON_G2 (triangle line; the "coffee break" line had no source); RAIL_CAP/G14/black HUD rail (-> CAP_v2 + HUD_v2 overlays); all plate blurs; SC_TITLE, SC_INS_ROOF, SC_INS_WHEEL, SC_INS_SILL, SC_INS_CABIN (no scans in the body); G03/G08/G09 black cards (-> overlays).

## Conclusion v2 (CON_*, revised in place; replaces conclusion.md Version A for v2)

- **CON_01** (FX30555 11.50-21.65, 10.15 s, protected) is the host's whole sentence: "If we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car, 10 minutes if I just did the exterior, with the power of a spray gun, AESUB Violet, and the Artec Leo."
  The HUD is frozen at 32 MIN / 20 MIN. CON_G1_v2 builds top-left, one line per beat, from "20 minutes": **32 MIN FROM "GO"** / **20 MIN WITHOUT THE CRASH** / **THE BET WAS 15**.
- **CON_02** is SC_CON_HERO for 8.0 s, with CON_G3_v2 **LINK IN THE DESCRIPTION** from +3.5 s. It hands off to the END card.
- **Removed:**
  - CON_02 v1 (black answer card): it is now the overlay on CON_01.
  - CON_03 "Yeah, this thing's fast": it is the end of the excluded sentence "I don't know if there's any other scanner out there that can do it faster, but yeah, this thing's fast", so it cannot play complete.
  - CON_04 (triangle card): rule 10. Its "coffee break" line had no source either.
- **Fallback** if the owner refuses the brand names or the "10 minutes" in CON_01: play 11.50-16.35 ("...20 minutes for the whole car,") and stop in the 0.3 s pause before "10". No word is cut, but it is mid-sentence. CON_02 then grows to 13.3 s.
- Only the owner's numbers go on screen: 32, 20, and the bet of 15. The "10 minutes" exists only as spoken words in the caption.

## Optional pickup lines (host records later; the video works without them)

| id | where | line |
|---|---|---|
| PU1 | B_02 end, 0:19.9 | "One car, one stopwatch. It starts on 'go'." |
| PU2 | P_05 time-lapse, 0:43.9 | "Step one is powder. Shiny paint and glass are hard for a scanner to read, so the whole car gets a thin matte coat. That alone took about two minutes." (2 min = said + legible 01:55) |
| PU3 | C_07 reboot card, 1:39.2 | "The first clock kept running. Once it rebooted, we started a second one." |
| PU4 | H_01-H_02, 2:59.8 | "The outside is the easy part. If you want to design a lip kit, you need the arches, the sills and the wheels, and that means jack stands and lying on the floor." |
| PU6 | CON_01 replacement if the brand sentence is refused | "So how fast can we 3D-scan an entire car? Thirty-two minutes from 'go'. Twenty without the crash. Fifteen next time?" |

(PU5, the triangle line, is withdrawn under rule 10.)

## For the owner

1. **CON_01 brands and "10 minutes".** Keeping the host's last line whole means captions show "10 minutes if I just did the exterior ... AESUB Violet, and the Artec Leo". OK? If not, the fallback (above) or PU6.
2. **Clock 1 digits in the hard parts are derived, not read.** They come from the camera's recording clock, anchored on the legible 32:53.18 at the end and checked against "21:--" at 546. Show them, or show "running" with no digits (as in 545)?
3. **Spray stamp wording.** "SPRAY DONE · 01:55 ON THE CLOCK" includes ~22 s of set-up between "go" and the first spray. Prefer "ABOUT 2 MIN OF SPRAYING" (said twice on camera)?
4. **Front pair twice.** The cold open teases the walk-out -> scan cut, and the montage ends on it. OK as a bookend, or tease the rear pair instead?
5. **Scoreboard wording** now uses your phrase "20 MIN WITHOUT THE CRASH". The footage shows TIMER 2 started about 12:10 after "go", so it leaves out the ~5 min before the crash as well as the reboot. Keep the phrase?
6. **"The cheating time is 8 minutes and 32 seconds"** stays as spoken in T_07. OK?
7. **"Checkpoint. Just two minutes."** (P_08). The speaker is off-camera and the models disagree ("He's two minutes" vs "Just two minutes"). The caption agent should confirm by ear.
8. **CTA:** scan listing or scanning service (conclusion.md options)? CON_G3_v2 and G15_v2 carry the placeholder.

Assumed:
- The owner's "do not blur plates" covers the background car in 541 344-384 too.
- The IRL clips other than 545 come from the 1080p conversions in `dropbox/`.
- FX30543 is unused.
- The crash and comeback music can be cut from the owner's game-music mix. If no tense passage exists in it, the music agent should say so before the editor builds the set-piece.
