# Huracan Evo scan reel v9 - self-review (training/rubric.md)  (older: review_v8 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v9.mp4` - 1080x1920, 30 fps, AAC, 29.97 s.
Changes from the user's notes on v8: deeper narration ("ball knowledge"), faster scan pacing, Spyder scans back in with a stealth
transition between the two cars.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 2 | Beat sync | 5 | 10 scan cuts vs kicks on the delivered file: +22 (drop) then -11..-12 ms each. |
| 3 | 1:1 match | 4 | Coupe -> Spyder on the drop: same camera, silhouette IoU 0.89 after a 29 px registration shift; frame difference at the cut 3.3 (other cuts 31-60). Tells: the Spyder's wheels are dark (not captured) and its windscreen has no scan holes. |
| 4 | Scan quality | 4 | As v8. |
| 5 | Story | 4 | Coupe select, wheel, side, push to the nose -> drop -> Spyder front opens, bumper, hood, side -> coupe rear bumper, deck, exhaust, wheel well -> Spyder full explode -> coupe reassembly -> logo. Ten scan shots in 16.8 s (1.2-1.8 s each; v8 had six). The parts move at 1.3-2.7x, so individual moves are brisk. |
| 7 | Text | 5 | Two title-only labels (REAR END, NO BUMPER 1.0 s; EVO EXHAUST 1.3 s). They're short at this pace. |
| 8 | Ending | 5 | The speech ends ~26.7 s on its conclusion, the music stops at 27.08 s, and the 720 px logo follows. |
| 9 | Technical | 4 | Every frame lit. Speech -13.4 LUFS, peak -1.0 dBFS. |

## Narration (one take, untrimmed, speech_rate 8, no tempo/pitch change)
"Lamborghini Huracan EVO. Its V10 fires at uneven intervals, fifty-four then ninety degrees, and that is the howl you hear.
Titanium intake valves help it make six hundred thirty-one horsepower, while LDVI steers all four wheels before you ask. Its
successor went twin-turbo hybrid, so this is one of the last great naturally aspirated Lamborghinis."
Sources: 5.2 V10 odd firing 90/54 deg (Lamborghini V10 references; evo.co.uk 'anatomy of a V10'); titanium intake valves (EVO
release, 7 Jan 2019); LDVI + rear-wheel steering + four-wheel torque vectoring (same); Temerario twin-turbo V8 hybrid (Lamborghini,
Aug 2024).

## Not verified
- I can't listen here, so the delivery is unheard. "That is the howl you hear" attributes the sound to the firing intervals; they're one contributor, not the only one.

## What the next agent should know
- Stealth swap between two scans of the same model: render car A at car B's first camera key (no floor), register by silhouette (IoU search for dx/dy), and hard-cut on a beat while B is still closed. Then start B's parts moving within a few frames.
- This custom voice reads number-heavy scripts slowly (70 words with decimals ran 32-34 s). Budget about 50-55 words for 24 s and cut words, never tempo.
- Faster pacing from existing renders: play frame ranges at 1.3-2.7x (`src_fps` >= 30 needs no interpolation), choosing the range where the part actually moves.
