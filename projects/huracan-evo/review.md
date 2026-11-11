# Huracan Evo scan reel v3 - self-review (training/rubric.md)  (v2: review_v2.md, v1: review_v1.md)

Output: `/home/user/media/work/out/huracan_evo_v3.mp4` - 1080x1920, 30 fps, yuv420p, AAC 48 kHz, faststart, 71.8 s.
Format: Need for Speed Hot Pursuit Remastered car-select homage (user's Gallardo reference clip) on the 2023 COUPE scan,
then the v2-brief section explode on the 2026 SPYDER scan from the music lift, logo on the music stop.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Engine start-up at 0.3 s while the garage lights come up on the whole coupe (motion from frame 1, slow push). It's a car-select reveal, as in the reference, not a transformation. |
| 2 | Beat sync | 5 | 6 hard cuts measured on the delivered file vs the fitted kick grid t = 3.0768 + 0.60006 n: +19 -14 -15 -15 -16 -16 ms (all within ±½ frame). Dips are centred on kicks n 3/17/32/47/57. The Spyder arrives on the lift (41.48 s) with the second start-up, and the logo lands on the music stop. |
| 3 | 1:1 match | n/a | No IRL in this format. |
| 4 | Scan quality | 3 | Coupe: real rims captured, licence plate and 47 debris triangles removed. **The windscreen and side glass have scan holes** (dark patches) in h0/h2/h5; I dropped the hood and high angles that showed the most glass. Spyder: wheels not captured (dark), and the composite base edges are ragged under the removed panels. |
| 5 | Story | 4 | Select -> one continuous narration over the coupe front -> wheel -> side -> rear (one sequence per section, director: no section repeated) -> Spyder lift -> front bumper (hero hold, label) -> hood/cowls -> fender + skirt -> rear bumper (hero hold, label) -> one full explode top-down -> reassembly -> logo. |
| 6 | Grade | 4 | One silver-on-black look. The coupe sits on a dark glossy floor (HP tunnel garage); the Spyder section floats on black. The floor's spot hotspot under h0/h7 is brighter than I'd like. |
| 7 | Text | 4 | Two labels, exact STL header counts: FRONT BUMPER / 4,000,015 TRIANGLES and REAR BUMPER REMOVED / 7,999,727 TRIANGLES. The front label moved to the only area that stays black (lower left) after it read white-on-silver over the hood. Narration specs are from Lamborghini's 7 Jan 2019 release. |
| 8 | Ending | 5 | Reassembly to the clean Spyder, rear 3/4 with margins, fade, small ILLUMAESTHETIC logo (380 px) on the music stop, then the reverb tail and a 0.6 s audio fade. |
| 9 | Technical | 4 | Every rendered frame luma-scanned (no dropouts; persistent data off for animated shots), and first/mid/last frames of every shot checked for clipping. The hard-cut duplicate frame from the assembler cut-hold is still there. |

## Not verified
- I couldn't listen to the narration (no ASR here), so wording and pronunciation are unchecked. The voice is a Higgsfield preset ("Imogen"), deliberately not a clone of the game's narrator.
- The engine sounds are generated V10 start-ups, not recordings of this car.

## What the next agent should know
- A glossy floor (rough 0.16, 14 m disc) roughly doubles Cycles CPU time (~30 s/frame at 75 % / 12 spp vs ~17 s). A 6 mm proxy and a bounce cap didn't help.
- Check a label's position against an occupancy map of the frames it covers (union of `luma > 45` over the label window). The hero hold fills the frame, so a fixed top-left spot can land on silver.
- `ive director` flags floor reflections as "cropped". Confirm on the frame itself, but here both whole-car shots really did touch the edges, so they were re-rendered wider.
- Don't move or delete a render folder while `ive assemble` runs; it reads clips lazily.
