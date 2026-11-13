# Huracan Evo scan reel v11 - self-review (training/rubric.md)  (older: review_v10 ... review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v11.mp4` - 1080x1920, 30 fps, AAC, 39.6 s.
Picture identical to v10 (video stream copied). Only the narration changed: the user asked for the car to be named
"LP640-4 Evo, representing the 640 metric horsepower it produces, mated to a 4-wheel drive system".

All rubric rows as v10 (review_v10.md). Audio re-checked on the delivered file: music is sample-aligned with v10 (0.0 ms offset),
speech 3.2-34.9 s (ends 1.8 s before the last kick and the logo), speech section -13.6 LUFS, peak -1.0 dBFS.

## Narration (one take, untrimmed, speech_rate 12, no tempo/pitch change)
"Lamborghini LP six-forty four EVO, representing the six hundred forty metric horsepower it produces, mated to a four-wheel drive
system. Its V10 fires at uneven intervals, fifty-four and ninety degrees apart, which gives it that jagged, howling note. Titanium
intake valves carry it to eight thousand RPM, while LDVI steers all four wheels before you ask. Its successor went to a twin-turbo
hybrid V8, which makes this one of the last great naturally aspirated Lamborghinis."
- "Huracan" is no longer spoken (the user's line replaces "Huracan Evo"). The separate 631 hp figure was dropped so the power is
  stated once (640 metric hp). The 5.2 l and injection details were cut to fit the same slot.

## Not verified
- I can't listen here: how the voice reads "L P six-forty four" is unheard.

## What the next agent should know
- An audio-only revision does not need a re-assembly: copy the video stream and mux the new mix with the assembler's audio
  settings (aac 320k, 0.6 s fade-out), then confirm the music offset against the previous file by cross-correlation.
