# L1 transcript - Lexus IS350 speed run (15 clips)

Model: faster-whisper **large-v3** (int8, CPU, VAD threshold 0.3, word timestamps) as primary, with a **medium.en** pass kept as a cross-check (`medium_en_segments` inside each JSON). Where only medium.en heard a line it is marked `(m)`. Per-clip word-timed JSON: `/home/user/media/work/is350-long/transcripts/FX305xx.json`. Times are seconds into that clip, `[mm:ss.s]`.

Detected speech is sparse: about 4.9 min of spoken words in ~28 min of footage (the rest is spray gun, scanner fan, shop noise, or silence). Whisper timestamps inside long noisy stretches can drift by a second or two; re-check any line before cutting to it. Speakers: **A** = host (grey "Berkeley" tee, runs scanner and spray gun), **B** = man in black polo with lanyard, **C** = camera operator (wears an Apple Watch, holds the phone stopwatch; never seen speaking on camera). Labels are inferred from frames and content, not certain.

## Findings

### 1. Rules / goal / prediction for the speed run
No rules are stated beyond the question and the stopwatch. The goal is "how long to scan this car"; there is no stated rule list (e.g. what counts as done).
- FX30541 [00:12.2] A or C coaching: "explain the whole thing so that way the viewer knows. ... How long do you think it'll take to scan this car?" The question is then asked four times (00:12, 00:15, 00:19.7, 00:23.9), one answer per take.
- Predictions (FX30541): [00:17.5] "I'll say two hours." (also [00:02.4] "Two hours."), [00:22.1] "Maybe 30 minutes.", [00:26.3] "I think I can do it in less than the length of a YouTube video. 15 minutes." (large-v3 appended "of course"; medium.en has no "of course"). Who says which is not certain; the 15-minute line is most likely the host (it matches his later confidence).
- FX30541 [00:32.2] (m) "Then you want to like film with like a stopwatch in your hand or something?" / "Yeah" - the stopwatch is the proof device.
- FX30541 [01:46.7] "then when I'm done spraying the car, show the watch ... I'm gonna show the watch periodically" (large-v3: "show the watch"; medium.en misheard it as "lock"). Rule-ish: spray time is counted ("Is that with the 2 minutes of spraying?" FX30545 [01:03]).

### 2. Elapsed time / stopwatch mentions
Two timers exist: the **primary** timer (phone stopwatch, started at the "go") and a **secondary** timer started after the reboot (FX30542 [00:12.6]).
- FX30541 [00:57.8] (m [01:00]) "That's like 40 days worth of time. I'm gonna stop it." - this is a phone timer/alarm joke before the run, not run time.
- FX30541 [01:11.6]-[01:14] "Three, two, one, go." Frame check: phone stopwatch reads **00:00.43** at 75.0 s, so the run clock = clip time - 74.6 s.
- FX30541 [03:00]-[03:21] "Checkpoint. Just two minutes." (medium: "Check point. Just two minutes.") Phone frame at 300 s reads **03:45.43** (so at 03:21 the watch is about 02:47; "two minutes" is the checkpoint chatter, not a reading).
- FX30541 [06:09.2] "Time check." [06:11.5] "What? Oh, it's switched. Five minutes on the dot." Analog stopwatch face at 372 s reads **04:57.46**; phone at 405 s reads **05:30.48**.
- FX30542 [00:04.8] "after like a five minute delay" (the reboot) and [00:12.6] "start a secondary timer. Now." [00:13] "Yup. So starting in two minutes." (m) - unsure what the "two minutes" refers to.
- FX30545 [00:03.0] "7 minutes and 41 seconds." (the context is lost: audio only; frame shows spraying, no readable watch.)
- FX30545 [00:53]-[01:12] Camera on the Apple Watch (out of focus, not legible; green start button visible, i.e. stopped): "What's the time?" "The cheating time is 8 minutes and 32 seconds." "Is that with the 2 minutes of spraying?" "No, it's 10 minutes." "So yeah, 10 minutes with spraying and 20 minutes with the crash. 20 minutes. Full car."
- FX30548 [00:07] Apple Watch stopwatch face is legible in frame: **13:05.01** (running; the face also shows clock 6:35). Nobody says it. Which timer it is (primary or secondary) is not stated. It is most likely the 32-minute primary clock reading 13:05, which fits a time after the interior/jacking start, but that is an inference; do not caption it as anything.
- FX30553 [00:09.7] "Time. 20 minutes. Done. And the other one, 32 minutes. Yep." (no watch in frame at that moment; frames at 3/10/20/40 s show car and host back only.)
- FX30553 [00:26.9] "that 20 minute span right here, most of the spray is already off the hood".
- FX30555 [00:08.5] "30 minutes on the... 30 minutes actual, but if we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car, 10 minutes if I just did the exterior..."
- Number conflicts to flag: owner says 32 min / 20 min. On camera: 32 (FX30553) vs "30 minutes actual" (FX30555, rounding); and FX30545 [01:07] says "20 minutes **with** the crash" while everything else says 20 minutes **without** it. Treat the FX30545 line as a slip (or whisper-correct but misspoken); do not use it. "Exterior only: 10 minutes" appears in FX30545 and FX30555 but is "with spray gun" in 555 and "with spraying" in 545 - ambiguous whether spray time is included.

### 3. The crash
It IS mentioned, and clearly: the **scanner** (Artec Leo, host's own scanner) crashed during the scan.
- FX30541 [06:16.9]-[06:22] Speaker (likely C or B) "How you feeling halfway through it?" Speaker A: "It just crashed. It's never crashed on me before." [06:34.6] "we have to pause this" ... [06:40.6]/[06:42] "We're still rolling" (medium.en: "this timer's still rolling" - the primary timer was left running). [06:50.8] "once this is sorted out, I'm just gonna start a new scan".
- When: about **5 minutes into the run** - "five minutes on the dot" at [06:11.5], crash called at ~[06:17], and the stopwatch reads ~04:57 at 372 s, so ~5:02 on the run clock (clip time - 74.6 s).
- What: the scanner software/device ("the scanner crashed" FX30542 [00:01.7]). Whether data was lost is **not stated**; "start a new scan" suggests the in-progress scan was abandoned but that is not said outright. No mention of "freeze", "lost data" or "restart" beyond "rebooting it".
- Cost: FX30542 [00:00]-[00:11] A: "So what happened? So the scanner crashed. So after like a five minute delay, we're rebooting it. And now we're gonna try again. All right, let's start the... start a secondary timer. Now." -> **~5 minutes delay** as stated. FX30555 [00:11.6] "if we ignore the scanner crashing on me ... 20 minutes". 32 - 20 = 12 minutes of crash overhead on the owner's numbers, which does not equal the stated "five minute delay": the 12 min presumably includes the lost scan time and the pause; not stated, flag for the owner.
- Crash not mentioned in any other clip (543, 544, 546-552, 554).

### 4. Names said on camera (exact words)
- Scanner: "Artec Leo" - FX30541 [03:58]-[04:08] "But with the Artec Leo, that's a thing of the past." and FX30555 [00:20.7] "the Artec Leo". FX30541 [01:27.9] "This is an Artec ad and an AESUB ad all in one" - large-v3 heard "arctic ad and a sub ad", medium.en "Artec ad and an AE Sub ad"; treat spelling as inferred from audio.
- Spray: "AESUB Violet" - FX30555 [00:19.8]; FX30553 [00:23.8] "AESUB Violet and Orange". (Spelled "AESUB" by the model; only audio evidence.)
- People: "Lorenzo" - FX30541 [04:50] "Hey, Lorenzo ... can you grab the scanner or the spray gun" (medium.en [04:21]), FX30553 [00:35.7] "our boy Lorenzo here", FX30548 [00:04.5] "Lorenzo, do you know how to drop a jack?" (medium.en heard "Lauren"). "Caleb" - FX30555 [00:07.3] "So in the span of how long, Caleb?" (speaker B answers). "Clayton" - FX30547 [01:26.7] "Clayton says hi." "Oslick"/"Osik" - FX30541 [03:23.9]/[03:32] "I've seen [Oslick/Osik] here in a film just like this" - unintelligible, model disagrees: **[inaudible name]**. FX30553 [00:37.7] "Haro" after "backs the car" is probably "and" garble: [inaudible]. Note "Tom Cruise" (FX30551 [01:21.9], a joke comparison, not a name of anyone present).
- Product/brand "Berkeley" etc. appear only on shirts, not said. No full names said.

### 5. Ten strongest to-camera/quotable lines
Mark: all clips have little true to-camera delivery; only FX30541 0-30 s and FX30555 are clearly to camera (frames checked). Others are off-camera narration.
1. FX30541 [00:12.2] "How long do you think it'll take to scan this car?" (hook, 4 takes, to camera)
2. FX30541 [00:26.3] "I think I can do it in less than the length of a YouTube video. 15 minutes." (prediction)
3. FX30541 [01:17.6] "I'm so confident in my ability, I'm not gonna rush. I gotta take my time." (setup for the crash)
4. FX30541 [01:11.6] "Three, two, one, go." (start; run clock zero = clip 74.6 s)
5. FX30541 [06:16.9] "How you feeling halfway through it?" ... "It just crashed. It's never crashed on me before." (turn)
6. FX30542 [00:00.0] "So the scanner crashed. So after like a five minute delay, we're rebooting it. And now we're gonna try again."
7. FX30545 [00:56] "So that's the exterior. That's done. Check mark." (off-camera, reviewing)
8. FX30553 [00:09.7] "Time. 20 minutes. Done. And the other one, 32 minutes." (result; off-camera)
9. FX30553 [00:22] "one thing to note is also cleanup time ... most of the spray is already off the hood and it's already starting to evaporate." (why a step matters)
10. FX30555 [00:11.2] "If we ignore the scanner crashing on me... 20 minutes for the whole car, 10 minutes if I just did the exterior." (to camera, final result line); runner-up [00:21.7] "I don't know if there's any other scanner out there that can do it faster, but yeah, this thing's fast." (see flags)
Honourable: FX30541 [03:58.8] "The sunlight sometimes makes scanning a pain. But with the Artec Leo, that's a thing of the past." (brand claim, see 6). FX30545 [01:55] "if you wanna make a lip kit, let's jack the car up, do the fronts and sides, wheel wells inside. So let's also time that."

### 6. Do NOT put in the video
- Profanity: FX30551 [00:04.3] "What the fuck? Where's the can?" (also bleep/cut the rest of the stumble).
- Phone screen with contacts, phone number and messages legible: FX30541 frame ~40-55 s (the phone shows a contact/number and apps). Do not show; blur or cut.
- FX30547 [02:09] "I can't wait to blur that. Put a smiley face there." - crew intends something to be blurred (person or plate) in the 2:00-2:12 area; check the frame and blur before use. Also the plate **9JTY488** is legible in FX30541 (~100 s, ~205 s), FX30545 (~30 s) and FX30553 (40 s): blur.
- Third parties: FX30547 [01:26.7] "Clayton says hi. Tell me who." (private chatter, unknown person); FX30541 [03:23]-[03:40] chatter about a person ("I've seen [?] here in a film just like this ... I paid for the last time I had to watch this"): unintelligible and about a third party.
- Sponsorship/claim issues: FX30541 [01:27.9] "This is an Artec ad and an AESUB ad all in one" (joke, but reads as a paid-ad admission; owner must decide). FX30541 [03:58] "with the Artec Leo, that's a thing of the past" and FX30555 [00:21.7] "I don't know if there's any other scanner out there that can do it faster" are unverified competitive/performance claims; no numbers should be added.
- Wrong/conflicting numbers: FX30545 [01:07] "20 minutes with the crash" (contradicts 32/20); FX30555 "30 minutes actual" vs 32; FX30545 "7 minutes and 41 seconds" and "8 minutes and 32 seconds" (a timer that is not identified; use only if the timer is shown).
- FX30553 [00:23] "AESUB Violet and Orange ... starting to evaporate": product behaviour claim, cosmetic; avoid stating as a spec.
- Off-topic chatter and meowing: FX30551 [01:25]-[01:36] "Na-na-nyow" (large-v3 had it; medium.en hallucinated "meow meow").
- Private-ish: FX30541 [00:57.8] "40 days worth of time" (phone alarm/timer joke), pointless.

## Audio quality (ffmpeg volumedetect, mono 16 kHz extract)
Mean volume is low everywhere (-25.8 to -37 dB) - normalise before burning captions timing checks; peaks clip at 0 dB in 547/551/552/553 (spray gun/scanner noise).

| clip | mean dB | max dB | usable speech sync |
|---|---|---|---|
| FX30541 | -25.8 | -0.4 | Good: 00:00-01:50 and 03:20-07:04 intelligible; spray noise 01:50-03:20 |
| FX30542 | -31.4 | -2.9 | Speech only 00:00-00:15 (clear); 03:00 chatter |
| FX30543 | -35.0 | -14.8 | No speech detected |
| FX30544 | -31.2 | -1.4 | No speech detected (scanner noise) |
| FX30545 | -27.3 | -2.7 | Good 00:50-02:05; 00:03 line sits in spray noise |
| FX30546 | -37.0 | -9.6 | Very quiet; one word at 00:02 |
| FX30547 | -35.9 | 0.0 | Quiet, clipped peaks; 00:00-00:04 and 01:20-02:12 usable but low |
| FX30548 | -33.1 | -12.2 | Quiet but clear (jack calls) |
| FX30549 | -27.6 | -4.0 | Short direction line only |
| FX30550 | -32.3 | -0.8 | "Where's the can?" at 00:28 only |
| FX30551 | -28.8 | -0.0 | Banter only; profanity at 00:04 |
| FX30552 | -32.5 | 0.0 | Mostly silence, a few words |
| FX30553 | -28.3 | -0.0 | Good (00:00-00:40) |
| FX30554 | -29.3 | -6.1 | 00:22-00:30 only usable |
| FX30555 | -27.5 | -2.8 | Best: clear to-camera, wind slight |

Transcribed with the stock ffmpeg 16 kHz WAV; `av.open(... metadata_errors)` in faster-whisper failed against the installed PyAV, so audio was passed as a numpy array.

---

## Transcripts (large-v3 primary; `(m)` = medium.en only)

### FX30541 (7:04) - mix of to-camera (00:00-00:30) and off-camera (camera on phone/car)
Frame notes: 00:02 host A looks into lens (to camera); 00:12 A and B in frame (interview takes); 00:45 phone with contacts on screen (private); 01:17+ camera POV from C with stopwatch; 01:40-03:20 spraying.
- [00:00.0] C?: Camera. Alright.
- [00:00.9] A: How long do you think it's gonna take?
- [00:02.4] B?: Two hours.
- [00:03.5] A: Elaborate. Elaborate. Like, actually...
- [00:06.0] C: No, no. When you ask the question, explain the whole thing so that way the viewer knows.
- [00:11.1] A: What's the whole thing? How long do you think it'll take to scan this car?
- [00:14.2] Okay.
- [00:15.0] (take 2) How long do you think it'll take to scan this car? [00:17.5] I'll say two hours.
- [00:19.7] (take 3) How long do you think it'll take to scan this car? [00:22.1] Maybe 30 minutes.
- [00:23.9] (take 4) How long do you think it'll take to scan this car? [00:26.3] I think I can do it in less than the length of a YouTube video. 15 minutes of course. (large-v3; medium.en: "15 minutes.")
- [00:32.2] (m) Then you want to like film with like a stopwatch in your hand or something?
- [00:35.5] (m) Yeah, I'll [inaudible] this.
- [00:49.5] (m) Alarms.
- [00:51.8] (m) Oh, I forgot, remember? / What? / You still have it on? / Of course. That's like 40 days worth of time.
- [01:01.9] (m) I'm gonna stop it. I'm just gonna jack up both sides. Alright, stop it.
- [01:07.1] Alright, ready to start? Huh? Yeah.
- [01:11.6] Three, two, one, go.
- [01:17.6] A: I'm so confident in my ability, I'm not gonna rush. I gotta take my time.
- [01:21.2] Oh no, oh no, that's not the right one. (large-v3: "not the way this...")
- [01:27.9] A: This is an Artec ad and an AESUB ad all in one. (spelling inferred; large-v3: "arctic ad and a sub ad")
- [01:46.7] A: Then when I'm done spraying the car, show the watch. Okay, I'm gonna show the watch periodically. C: Yeah, yeah.
- [01:50]-[03:20] spray noise, no intelligible speech.
- [03:21.0] Checkpoint. Just two minutes.
- [03:23.9] [inaudible name] here in a film just like this.
- [03:29.2] Did you hear what he said? No. So repeat what you just said. I've seen [inaudible name] here in a film just like this. Oh, wow.
- [03:37.9] This looks familiar. [03:40.0] I paid for the last time I had to watch this. (low confidence)
- [03:51.1] Down, down, down, down.
- [03:53.6] Oh, uh, [inaudible]. I was worried about the sunlight, so it's okay.
- [03:58.8] For you? Huh? For you? A: No, no. The sunlight sometimes makes scanning a pain. But with the Artec Leo, that's a thing of the past.
- [04:11.1] Did you cut?
- [04:13.3] I'm just gonna continuously roll and cut afterwards.
- [04:17.9] Oh, I didn't get the bottom side of the tail light. Hey, [04:50.7] Lorenzo. Yes? Can you grab the scanner or the spray gun, spray the dark spots of your rear view mirror, and then also aim up and spray the bottom of the tail lights?
- [05:04.0] Basically anything that isn't covered. Like right here.
- [05:31.2] And then the inside. The doors I don't care about. Mostly just the black and the clear colored things. Okay.
- [05:44.4] We're good, we're good.
- [05:47.6] The corner of the left headlight. You see how it's like not fully covered? Got you.
- [05:57.3] Because this also evaporates. Oh, okay. So sometimes.
- [06:06.8] Actually.
- [06:09.2] Time check.
- [06:11.5] What? Oh, it's switched. Five minutes on the dot.
- [06:16.9] How you feeling halfway through it? A: It just crashed. It's never crashed on me before. Okay,
- [06:34.6] we have to pause this ((m) "this timer's still rolling")
- [06:40.6] We're still rolling.
- [06:50.8] Yeah, once this is sorted out, I'm just gonna start a new scan. Yeah, I know.

### FX30542 (4:49) - off-camera (A talking to camera operator while scanner prep)
Frame notes: 00:05 A adjusting, scanner on table; 02:30 A scanning left side.
- [00:00.0] A: So, uh, what happened? So the scanner crashed. So
- [00:04.8] after like a five minute delay, uh, we're rebooting it. And now we're gonna try again. All right, let's start the... start a secondary timer. Now. Yep.
- [00:19.4] Did you...
- [03:00.6] (say) a kimbo? Yeah. Dual wielding. (low confidence: "akimbo"; likely the host holding scanner and spray gun)

### FX30543 (0:11): no speech detected.
### FX30544 (2:28): no speech detected (scanner noise only).

### FX30545 (2:04) - camera rotated 90 deg, off-camera voices; watch and scanner screens
- [00:03.0] 7 minutes and 41 seconds.
- [00:36.6] Thank you. (m: low confidence)
- [00:47.3] Done. Go over there.
- [00:51.3] Finished.
- [00:53.4] C: So, are you still recording? Yep. A: So that's the exterior. That's done. Check mark. What's the time? [01:00.2] The cheating time is 8 minutes and 32 seconds. Is that with the 2 minutes of spraying? No, it's 10 minutes. So yeah, 10 minutes with spraying and 20 minutes with the crash. [01:11.4] 20 minutes. Full car. Let's review it.
- [01:16.6] IS350.
- [01:26.5] A (over scanner screen): Okay, so that's the whole back of the car. Missing a little bit right there.
- [01:34.8] This is the full walk around of the car. Front, hood, roof, right side. Rear quarter panel's a little messed up. Roof's messed up. So I came back here, did the whole roof, did the right quarter panel, fixed the trunk.
- [01:55.2] That's the full interior. So now, if you wanna make a lip kit, let's jack the car up, do the fronts and sides, wheel wells inside. So let's also time that.

### FX30546 (1:13)
- [00:02.3] Go ahead. (very quiet)

### FX30547 (2:41) - A off-camera, scanner screen and floor scanning
- [00:00.1] For harder-to-reach areas, I'll use the can. Your position. (m: "Your" unclear)
- [01:20.6] position. Can I get the can?
- [01:26.7] Clayton says hi. Tell me who. Oh, yeah.
- [01:38.3] Can I get the spray can? Uh, [01:50.1] yeah. My bad. I didn't know it was over here. I got it.
- [02:00.6] It's a crazy position. Is this the most optimal scanning position? Yeah.
- [02:09.2] I can't wait to blur that. Put a smiley face there.

### FX30548 (0:14)
- [00:04.5] Lorenzo, do you know how to drop a jack?
- [00:08.9] Drop the right side, drop the right side jack for me.
(Frame 00:07: Apple Watch stopwatch face reads 13:05.01.)

### FX30549 (0:08)
- [00:03.3] Uh, go to the rear jacking point. [00:05.8] Take it, take it to the rear, no no, take it to the left side.

### FX30550 (0:40)
- [00:27.9] Where's the can? ... [00:39.4] Where's the can?
(large-v3 heard "cat"; medium.en "can".)

### FX30551 (1:49)
- [00:00.0] Oh, under the car! It disappeared!
- [00:04.3] What the fuck? Where's the can?
- [00:13.7] Oh, it's right here. Right? Oh yeah, it is. It blended in. I do the same thing all the time. I feel like Tom Cruise. (large-v3 timestamps the last words at 01:21.9, which is probably drift; medium.en puts the line at 00:13-00:18 - check by ear)
- [01:25.7] Down here.
- [01:29.9] Na-na-nyow. Na-na-nyow. Na-na-nyow. Nyow-nyow. (cat noises)

### FX30552 (1:59)
- [00:19.4] Okay. [00:21.2] Done? Nope. Oh yeah, almost done.
- [01:26.8] Can?

### FX30553 (0:43) - off-camera, host back in frame at 20 s
- [00:01.2] Car coming down.
- [00:07.3] Time. 20 minutes. Done. And the other one, 32 minutes. Yep.
- [00:18.8] So one thing to note is also cleanup time. So with AESUB Violet and Orange, you can already see in that 20 minute span right here, most of the spray is already off the hood and it's already starting to evaporate.
- [00:33.7] So if our boy Lorenzo here backs the car [inaudible] puts it in the sun, go ahead and do that.

### FX30554 (0:35)
- [00:22.5] So, just leave it in the sun, we're gonna import the scan, and I'll show you how to process it. (medium.en also has [00:03]: "All the way, just leave it outside. Good.")

### FX30555 (0:31) - TO CAMERA, A and B in frame outdoors
- [00:02.2] Come here.
- [00:05.4] A: So in the span of how long, Caleb?
- [00:08.5] B: 30 minutes on the... 30 minutes actual,
- [00:11.2] A: but if we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car, 10 minutes if I just did the exterior, with the power of a spray gun, AESUB Violet, and the Artec Leo. I don't know if there's any other scanner out there that can do it faster, but yeah, this thing's fast.

## Blockers for captions
- No burnable caption timing exists yet (stage 2). Only ~5 minutes of intelligible speech exist, mostly short off-camera lines; the edit will need to use captions sparingly or rely on VO.
- Open items for the owner: what exactly crashed and whether data was lost; the 32 vs "30 actual" and "20 with the crash" slip; who "Lorenzo", "Caleb", "Clayton" are and whether naming them is OK; the sponsorship wording "Artec ad / AESUB ad".
