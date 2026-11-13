# Audio review: speech audible in the CUT (smart450_v1.mp4)

**Machine transcription.** faster-whisper `medium.en` (CPU, int8) run on the shop-sound stem (`/home/user/media/work/smart-450/out/stem_shopsound.wav`) span by span, each span normalised so quiet speech is not missed, plus the source clip over the same span for context. Quote marks are what it *sounds like*, not what was said; names are guesses. The flag column is a keyword scan of both transcripts. It can miss quiet or overlapped words, so listen to every row. Nothing was censored, cut or muted (owner's note in `feedback.jsonl`).

Level in the cut: `under` = shop sound about 14 dB below the music, `up` = about 6 dB below (RMS per shot, see `audio_levels.json`). Scan shots (S3, S10, S18), the two design stills and the logo carry music only. Timeline times are seconds in the delivered file.

## Rows with speech

| timeline (s) | shot | source clip, time (s) | level | sounds like (stem span) | wider source context | profanity / slur / scanner price |
|---|---|---|---|---|---|---|
| 0.00-0.73 | S1 | v_1852_56 20.80-21.53 | under (+8 dB gain) | "Snack" | ...questions, but I guess we'll keep going because this is all for a car that's not even a US... | none detected |
| 0.73-1.50 | S2 | v_1852_56 25.27-26.03 | under (-12 dB gain) | "Huh?" | ...U .S. market car. sigh... | none detected |
| 3.00-4.50 | S4 | v_1857_58 1.20-2.70 | under (+5 dB gain) | "This is a GNK car, cause they -" | ...I just realized that this is a G and K car because they added, these bars are like.... | none detected |
| 4.50-5.27 | S5 | v_1632_12 0.00-0.77 | under (+8 dB gain) | "Of course." | ...Is she Canadores? Is she Canadores? So.... | none detected |
| 7.50-9.00 | S9 | v_1724_26 11.00-12.50 | under (+24 dB gain) | "You" | ...Thank you very much.... | none detected |
| 12.77-13.53 | S11 | v_1659_53 1.90-2.67 | under (-2 dB gain) | "out of." | ...For those who are curious, it is made out of...... | none detected |
| 13.53-14.27 | S12 | v_1712_33 19.05-19.78 | under (+9 dB gain) | "Set." | ...Okay, and it's gonna be a cabriolet. Sick.... | none detected |
| 14.27-15.03 | S13 | v_1852_56 6.00-6.77 | under (+6 dB gain) | "This is" | ...This is actually a first gen smart car. So now I'm developing a body kit for.... | none detected |
| 16.53-18.03 | S16 | v_1724_26 107.30-108.80 | under (-1 dB gain) | "Yeah, you're probably not mad at him. Kwon?" | ...Um, Guan, I don't know if you remember, you probably not met him, Guan, Guan, one of the associate producers.... | none detected |
| 18.03-18.80 | S17 | v_1729_10 0.48-1.25 | under (-2 dB gain) | "of the" | ...So I have the full car scanned in its current state.... | none detected |

## Spans where no speech was detected (spray hiss, shop noise, handling)

| timeline (s) | shot | source clip, time (s) | what the machine heard |
|---|---|---|---|
| 5.27-6.00 | S6 | v_1634_19 14.50-15.23 | nothing (repeated letters = ASR reading noise) |
| 6.00-6.77 | S7 | v_1634_19 6.90-7.67 | N[hiss/noise] (repeated letters = ASR reading noise) |
| 6.77-7.50 | S8 | v_1634_51 0.15-0.88 | [hiss/noise] (repeated letters = ASR reading noise) |
| 15.03-15.77 | S14 | v_1722_25 24.60-25.33 | [hiss/noise] (repeated letters = ASR reading noise) |
| 15.77-16.53 | S15 | v_1722_25 35.00-35.77 | [hiss/noise] (repeated letters = ASR reading noise) |

## Notes for the owner

- No profanity, slur or price was detected by the keyword scan inside the used spans. That is a statement about this machine pass only: S9, S14, S15 and S16 come from the bystander-heavy glasses clips (`clips.md` marks them 'do not use' for talk), and words heard at 14 dB under music are easy to miss. Please listen to S9 (7.50-9.00) and S16 (16.53-18.03) first.
- S16 contains a bystander talking to a named person (sounds like 'Guan' / 'Kwon').
- S1, S2, S4, S5, S11, S12, S13, S17 carry the filmmaker's own narration fragments (a few words each, cut mid-sentence).
- To remove or replace any of it, edit the span in `tools/edit_shots.py` (`audio: None` mutes a shot) and run `python projects/smart-450-hellkitten/tools/build.py`; the separate shop stem is delivered so it can also be edited in an audio editor.
