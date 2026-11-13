# IS350 speed-run reels - production brief (2026-11-13)

Owner: "make 2-3 good reels derived from this video" (the finished IS350 long-form, projects/lexus-is350-speedrun-long, final v5).
Deliverables: three 9:16 reels, 1080x1920, 30 fps, 15-30 s each, Illumaesthetic logo card on the last downbeat.

## The three reels (lead's plan; the reel editor may refine order and spans, not the concepts)
- R1 "THE CRASH" - the bet ("15 minutes"), "three, two, one, go", "It just crashed. It's never crashed on me before.", reboot,
  the result ("Time. 20 minutes. ... the other one, 32 minutes"). A story reel carried by the host's real lines.
- R2 "REAL -> SCAN" - the signature format: real scanning from one angle, hard 1:1 cut to the scan from the same camera,
  four angles (rear quarter, rear bumper, hood, front walk-out), then the full-car hero. Music-driven, cuts on beats.
- R3 "HOW LONG DOES IT TAKE?" - the question and the three guesses (2 hours / 30 min / 15 min), a fast run of the process
  (spray, scan, under the car on the floor: "Is this the most optimal scanning position?"), the answer card, the scan.

## Facts (use exactly; invent nothing)
32 minutes elapsed from "go"; 20 minutes without the crash (timer restarted after the crash); the bet was 15 minutes.
End CTA: "SCANS AVAILABLE AT ILLUMAESTHETIC.COM". No triangle counts, no reflector material, plates NOT blurred (owner's rules for this video).

## Rules
- Derived from the long-form, so its owner-approved exceptions apply here too: overlays and captions may sit over the footage
  (compact, phone-legible, safe margins for Reels/TikTok UI: keep text out of the top 220 px and bottom 420 px, and off the right 120 px).
  Every spoken line that is kept is captioned; dialogue is never clipped.
- IRL -> scan is a hard 1:1 cut on a beat, matched frame to matched frame. Hook in the first 2 s. Never reuse a shot inside a reel.
- Picture quality: the working copies in /home/user/media/lexus-is350/dropbox/ are 1080p proxies - a 9:16 crop of those is only 608 px
  wide. Source the reels from the 4K originals (Dropbox folder "IS350 scanning Speed run (completed)", 15 clips; 4K copies of FX30545,
  554, 555 are already in /home/user/media/lexus-is350/dropbox_4k/). Disk is tight (~6 GB free): fetch one original at a time,
  cut the needed spans to 9:16 intermediates, delete the original.
- Scan shots must be the vertical re-renders (ids V_PAIR_2, V_MATCH_REAR, V_PAIR_3, V_MATCH_FRONT, V_RES_FULL) - never a crop of the
  16:9 renders. The 3D agent publishes the 9:16 crop window (x0) it solved each pair for; use exactly that window on the IRL side.
- Music: one track per reel from the TikTok Commercial Music Library, not used by any earlier project; the owner disliked constant
  music changes - one track, no switching. Deliver music on its own stem. The long-form's game-music compilation is NOT cleared: do not use it.
- Log every decision: python -m ive log projects/lexus-is350-reels "<what>" --why "<why>". Look at your output before reporting.
