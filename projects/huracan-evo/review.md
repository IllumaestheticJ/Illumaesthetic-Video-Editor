# Huracan Evo scan reel v15 - self-review (training/rubric.md)  (older: review_v14 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v15.mp4` - 1080x1920, 30 fps, AAC, 46.8 s.
Picture and music identical to v13/v14 (video stream copied). Change from the user's note on v14: the slowed name was "too slow
now, it needs to read more natural".

All rubric rows as v13 (review_v13.md). Speech 3.4-37.2 s, -13.3 LUFS, peak -1.0 dBFS; ~6.7 s of music only before the logo.

## Narration (new one-take recording, untrimmed, speech_rate 8, no tempo/pitch change)
"The Lamborghini Huracan L P six-forty dash four EVO, representing the six hundred forty metric horsepower it produces, mated to
a four-wheel drive system. Its V10 fires at uneven intervals, fifty-four and ninety degrees apart, for that jagged, howling note.
Titanium intake valves carry it to eight thousand RPM, and LDVI predicts your next move. Over the original Huracan it gained
thirty horsepower, rear-wheel steering, and more than five times the downforce, cutting zero to sixty-two from three-point-two
seconds to two-point-nine."
- Name timing by take: v13 2.6 s (user: rushed) -> v14 5.7 s with four written pauses (user: too slow, unnatural) -> v15 3.7 s as
  one unbroken phrase.

## Not verified
- I can't listen here: timing is measured, naturalness is unheard.

## What the next agent should know
- Slowing a phrase with written pauses (ellipsis + commas between every part) over-corrects and sounds unnatural. Write the phrase
  plainly and lower `speech_rate` a few points instead, then measure the phrase length and check that it has no internal pauses.
