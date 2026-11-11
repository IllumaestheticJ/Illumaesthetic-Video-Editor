# Toyota MR2 Spyder scan reel v2 - self-review (training/rubric.md)

Output: `/home/user/media/work/mr2/out/mr2_spyder_v2.mp4` - 1080x1920, 30 fps, yuv420p, AAC, faststart, 1009 frames, 33.63 s.
v2 answers the first-revision notes (lessons.md V2 brief + addendum A-D): one continuous sequence per section, nose -> roof -> tail; bumper-removed hero beat with labels; open states only where a registered scan exists; ive director reports **no repeated views**.

Timeline: s1_wide (whole car, push-in) -> s4_wheel -> s12_front (bumper slides out, camera moves in on the crash structure and holds, hood opens) -> s13_top (hardtop lifts off, crane into the roll-bar cabin) -> s14_rear (rear lid opens on the strong hit, crane over the engine bay) -> s15_reassemble (parts return, clean-car swap, fade) -> small logo.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 3 | Whole car from frame 0 with a push-in (1.12x->1.28x) plus orbit; fade-up 1 s. Still nothing *transforms* in the first 1.5 s - the first transformation is the bumper at ~6.6 s. |
| 2 | Beat sync | 4 | Six cuts measured against the decoded audio's transients (10 ms RMS envelope): 129, 193, 389, 579 within ~20 ms; 771 ~30 ms early; 916 on the final hit. Cut 3 was moved 386->389 because the grid beat had no transient (real hit +100 ms). Not all strictly within the brief's +-1/2 frame - 10 ms resolution. |
| 3 | 1:1 match | n/a | No IRL. Panel-state continuity carried across s12->s13->s14 (bumper off, hood + lid open). |
| 4 | Scan quality | 3 | Every frame lit (per-frame luma scan, persistent data off on all moving shots). Diff-made front bumper still has ragged open edges (visible as it slides out); front base ragged where the bumper was differenced - which is honestly what's behind the scanned bumper. Clean-car swap hides it at the end. |
| 5 | Story | 4 | Whole -> wheel -> front (bumper off = hero) -> roof -> rear -> reassembly -> logo. Each section once, no ping-pong. No explode stack this time (the director plan dropped it as a repeat of s12-s14); the progressive per-section reveal stands in for it. |
| 6 | Grade | 4 | One satin-silver look; close-ups read brighter because the car fills the frame. |
| 7 | Text | 4 | 7 short labels over scan only, factual (states that exist as scans: bumper on/off, hood closed/open, hardtop on/off, lid closed/open; STRUT TOWER / ROLL BAR / ENGINE BAY name visible parts), no numbers. More than the rubric's 2 items because the addendum asked for labelled bumper-removed detail. Each label on black; FRONT BUMPER REMOVED moved to the top so the sliding bumper doesn't pass under it. |
| 8 | Ending | 4 | Clean car fades out (0.45 s), small logo card (380 px) on the final hit, music fade 1.2 s. |
| 9 | Technical | 5 | Specs correct; plain concat (no cloned hold frames at cuts); freezedetect only fires on the static logo card. |

## Fixes found by looking (not by score)
- Labels rendered twice: concat_assemble already burns `overlays:` in, so the extra label_pass composited a second copy. Removed label_pass.
- s14 opened small and low with ~450 px dead black above -> post zoom-crop 1.2x->1.0 instead of a 37-min re-render.
- Director flagged s13 ~ s14 (both opened on a whole-car 3/4 silhouette, corr 0.78) -> s13 starts 12 source frames in (corr 0.72).

## Not verified
- Phone-speaker listen; label legibility on an actual phone.

## What the next agent should know
- `concat_assemble.py` composites `overlays:` itself - don't add a second label pass.
- ScanHUD label with an empty `sub` crashes (interpolate range [6,6]); always give a sub.
- Kick grid != transients everywhere: verify each cut on the decoded audio, the 112 BPM grid was 100 ms early at 12.86 s.
- Post zoom-crops (PIL crop + LANCZOS back to 810x1440) are a cheap fix for framing on 75% renders; keep >=5% margin.

---
# Toyota MR2 Spyder scan reel v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/mr2/out/mr2_spyder_v1.mp4` - 1080x1920, 30 fps, yuv420p, AAC, faststart (moov first), 1163 frames, 38.77 s.
Format: Temerario-style scan-only reel (no IRL, no text) on the generated track from the parent session (112 BPM, kick-anchored grid).

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 3 | Fade-up from black over 1 s into a low side-profile track along the hardtop car; first cut on the first kick accent (3.16 s). Moves from frame 0, but nothing *transforms* in the first 1.5 s (format has no IRL to cut from). |
| 2 | Beat sync | 5 | 11 hard cuts measured on the delivered file (frame-diff peak vs the beat grid): +12 -8 +16 +7 -2 +12 -7 -16 -2 -12 +10 ms, all within half a frame. Big hits 13 (s6 hardtop) and 45 (s9 explode) carry the two transformations. |
| 3 | 1:1 match | n/a | No IRL in this format. Panel-state continuity across s6 -> s7 -> s8 -> s9 checked (top off, bumper off / hood + lid open carried through). |
| 4 | Scan quality | 3 | Silver on black, levelled (tyre contact spread 2.7 mm), every frame lit (max luma 255 on all 550 renders after the persistent-data fix). Gaps: the composite base is ragged at the front where the bumper/hood were differenced out and the 2023-06 Hood Duct state scan fills in (visible in s7/s9/s11 mid); diff-made parts (esp. front bumper) have open edges. End hero swaps to the clean 2 mm full car to hide this. |
| 5 | Story | 4 | Turntables -> wheel / tail close-ups -> hardtop lifts off (roof-down scan) -> front + rear open on fitted hinges -> top-down -> exploded stack -> float -> reassembly into the hardtop car -> logo. Follows the Temerario order. |
| 6 | Grade | 4 | One look, -0.5 EV AgX satin silver; close-ups (s4/s5) read brighter (mean luma 63-74 vs 20-38) because the car fills the frame - same material. n/a for IRL. |
| 7 | Text | 5 | No on-screen text. |
| 8 | Ending | 5 | Clean car hero -> ILLUMAESTHETIC logo (official PNG) hard-cut on the final hit (33.70 s, err +10 ms), track's ring-out under it, 0.8 s audio fade to -54 dB at the end. |
| 9 | Technical | 4 | Specs correct, no black frames. One assembler cut-hold (cloned) frame before each cut, as in the 240SX/Huracan reels. 4-6 near-still frames at the eased starts of s6 and s7. 15 fps renders minterpolated to 30 fps: some interpolation smear on the fast panel moves in s9/s11. |

## Not verified
- Not listened to on a phone speaker; audio checked by level only.
- 2023-05 `MR2 Spyder Hood Open.stl` / `front End.stl` were downloaded but never registered or used - a cleaner front-end state may be in there.

## What the next agent should know
- Cycles persistent data dropped all lights mid-shot on every hinge-animated shot here (s7 from f34, s9 from f46: mean luma 26 -> 4). Set `"persistent": False` on any shot with hinge/part animation and scan per-frame luma before assembling.
- The 2022 Front Bumper Data scans don't register to the 2023 car (fit 8-10 %, inconsistent poses); the 2023-06 Hood Duct Data scan does (2.0 mm median) and is the one to use for the front states.
- Parts by differencing same-frame state scans work for the hardtop and rear lid; the front bumper diff is thin and ragged - for a hero reassembly, cut to the clean full car the frame the last panel lands (shots.py s11 `visible` windows).
- open3d has no wheel for Python 3.13 in this box: `tools/globalreg.py` is a numpy/scipy replacement.
