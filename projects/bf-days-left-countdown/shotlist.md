# BF 9: "days-left-countdown" shot list (TEMPLATE PLAN, waiting for the owner's approval)

Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`. **Nothing is rendered until the owner approves this plan in chat.**

**Owner request (verbatim):** "add another chat that makes a short reel that says X days left"

**One line:** on black, Eps raises his scanner and the cyan sweep builds a huge silver **X** out of wireframe on the beat,
"DAYS LEFT" slams in under it, Del taps the tape roll on his belt ("clock's running"), and the reel ends on the Epsilon+
wordmark. One template, re-rendered per posting day: only the numeral and the line under it change.

**Format:** 1080x1920 (9:16), 30 fps, **16 beats, about 7.5-8.5 s** (exact length is set by the measured beat grid).

---

## 1. Template inputs

| Input | Type | Example | Rules |
|---|---|---|---|
| `days_left` | integer >= 0 | `5` | **Computed, not typed:** `days_left = sale_end_date - post_date` in calendar days, both in **America/Los_Angeles**. `0` renders the "LAST DAY" variant. `1` renders "DAY LEFT" (singular). The build script refuses to render if the reel's `post_date` isn't set. |
| `sale_end` | ISO datetime, Pacific | `2026-12-01T23:59-08:00` | **Not set yet** (the owner's BF doc says the window is open). Required before any render. |
| `post_date` | date, Pacific | `2026-11-26` | The day the reel goes up. A reel rendered for one day is never posted on another. |
| `show_end_line` | bool | `false` | When true, adds "ENDS <Mon> <D>, <h:mm> PT" under the wordmark. Default **off** until the owner confirms the window. |
| `offer_line` | string or empty | `""` | Optional one-liner under "DAYS LEFT". Numbers only from the BF liquidation sheet (`projects/_blackfriday/PRICES.md`; snapshot `bf_liquidation_pricing.csv`, commit 7ec3adf; re-read the live Pricing tab before render), wording confirmed by the owner (Q4). Never a stock count. Empty by default. |

**Countdown calendar (fill in once `sale_end` is known):**

| post_date (PT) | days_left | Numeral | Line under it |
|---|---|---|---|
| end − 5 | 5 | `5` | DAYS LEFT |
| end − 3 | 3 | `3` | DAYS LEFT |
| end − 1 | 1 | `1` | DAY LEFT |
| end date | 0 | (none) | **LAST DAY** variant (see shot 2b) |

(Example set from the brief: 5 / 3 / 1 / last day. The owner picks the actual days, Q2.)

Edge case: if the sale ends at midnight PT and the reel posts in the evening of the last day, "LAST DAY" is still right.
If the sale ends at a time other than 23:59, a reel posted after that time must not go up at all.

---

## 2. Music

Every `/Moosic` track is already used by another reel (checked: the Dropbox folder listing against `projects/*/project.yaml`
and the other BF shot lists). So the pick comes from TikTok's Commercial Music Library, checked 2026-11-17 against MUSIC.md and the repo:

| # | Track | song_clip_id | Why |
|---|---|---|---|
| **1 (claimed, provisional)** | "BLACK FRIDAY" - DJ EV (144 s) | 7419416839039518737 | On-theme title. Unused anywhere in the repo or registry. |
| 2 | "BREAKING NEWS" - DJ DF KIT (72 s) | 7622371201206765569 | Urgent, news-sting feel; suits a countdown. |
| 3 | "Machine Protocol" - Wbsound (149 s) | 7671666742675539969 | Mechanical; matches the scan sweep. |

Rules: start at the song's beginning. Cuts go on measured hits (`ive beats` plus a kick-envelope check, lesson L586).
If the first hard hit in #1 lands later than about 2.5 s, the cold open can't reach it inside 8 s. In that case I fall to #2 and tell you.
Mix at -14 LUFS, true peak below -1 dBFS. **The same track is used for every day's reel** so the series reads as one campaign.

---

## 3. Shot table

Beat numbers are on the measured grid of the chosen track (B1 = first hit). Times assume about 128 BPM (0.469 s/beat) and are re-timed after measurement.

| # | Time | Dur | Beats | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition | Render method |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-1.88 | 1.88 | B1-B4 | Low rear 3/4, 35 mm, 5 % push-in | Silver Integra with the Epsilon kit on black; **Del** (1:1) beside the rear quarter, in colour | **Reused plate:** the silver Integra render from BF 2 (`bf-integra-stock-to-kitted` shot 5, `eps-acura-integra-de-v29.glb`) or BF 3 (`bf-integra-385-combo` shot 6, scan `Integra Type S Full Car.stl` Drive 1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5 + Sport Wing/trunk lip). Whichever is rendered first; if neither is ready, render a 2 s window from the same file. Del: Higgsfield clip, ref `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg` | Del taps the yellow tape roll on his belt twice, in time with B2 and B4: a "clock's running" tick | none | hard cut on B5 | Blender plate (reused) + Higgsfield character clip, composited |
| 2 | 1.88-3.75 | 1.88 | B5-B8 | Front-on, slightly low, static | Pure black. **Eps** (1:1) frame right raises his scanner; the cyan (#6fc3d6) sweep plane passes top to bottom; a huge numeral **X** builds behind it from scan wireframe to house silver | Numeral: Blender text object (bold sans, 1.2 m tall, 8 cm bevel), house silver material + a triangle-wireframe pass masked by the sweep (same sweep as the characters' "scan-in" rule). Eps: Higgsfield clip, same reference | Sweep hits the top of the numeral on B5 and finishes on B8. Eps' visor eyes go from `- -` to wide `O O` as it completes | the numeral **is** the text (Blender geometry; the number comes from `days_left`, never from AI) | continuous into 3 (same camera) | **Blender (per-day)** + Higgsfield clip (shared) |
| 2b | (LAST DAY variant) | same | B5-B8 | same | Same, but the sweep builds the words **LAST DAY** in two lines | same Blender text rig, string = `LAST\nDAY` | Eps does a double take (eyes `O O` → `! !`) | "LAST DAY" (geometry) | same | Blender (once) + 1 extra Higgsfield clip |
| 3 | 3.75-5.63 | 1.88 | B9-B12 | Same camera, 4 % push toward the numeral | Numeral held; **Del** steps in frame left | Same render continues; Del: Higgsfield clip | "DAYS LEFT" (or "DAY LEFT") slams in under the numeral on B9 in the house font, white with a soft dark halo (lesson L533). Del taps the tape roll once on B11, then a slow nod. Optional `offer_line` lands on B11 | "DAYS LEFT" / "DAY LEFT" (template); `offer_line` (owner-confirmed only) | hard cut on B13 | Blender (per-day numeral) + Remotion text + composite |
| 4 | 5.63-7.50 (+ decay) | 1.88+ | B13-B16 | Static | Epsilon+ wordmark on black, about **720 px** wide, centred; `EPSILON.PLUS` under it | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | Wordmark lands on B13 and rides the decay; music fades with it | `EPSILON.PLUS`; "BLACK FRIDAY"; optional end line `ENDS <date> <time> PT` **only if `show_end_line` and the window is confirmed** | end | Remotion (per-day only if the end line is on) |

Optional end sting (+1.5 s, off by default to stay short): the 10 mm gag from BF 5 shot 11, reused as-is, with no re-render.

**Rule checks:**
- No IRL footage in this reel, so no text-over-IRL conflict.
- The scans and numeral are silver; Del & Eps are the only colour.
- The characters never touch the geometry: Eps scans from a distance, and Del taps his own belt.
- No prices or dates on screen unless confirmed (Q3, Q4). Any number comes from the liquidation sheet (PRICES.md), never from the store's stock.

---

## 4. Render method and per-day cost

**Built once, at approval (shared by every day):**
1. **Shot 1 plate:** reused from BF 2/3 (zero new renders), or a 2 s Cycles window from the same file if neither exists yet.
2. **Character clips (Higgsfield, model sheet as reference element):** Del tape-tap, Eps scan-raise, Del step-in + nod, and Eps double take (LAST DAY).
   - That is 4 clips. No digits or text are ever in the AI prompt or frame, so an AI can't draw a wrong number.
   - Each clip is generated on a flat grey background, then cut out (`remove_background`) and composited.
   - I'll get a credit quote (`ads_studio_quote` / `generate_video` quote) before generating anything and show it to you.
3. **Blender numeral rig** `tools/numeral.py` with `--text "5"`: the sweep animation, wordmark-matched lighting and an alpha pass. The black background lets the characters sit over it.
4. **Remotion composition** `DaysLeft` with props `{days_left, offer_line, show_end_line, sale_end}`, for the text, wordmark and end line.

**Per day (what changes):**
- One Blender render of shot 2-3's numeral, about 3.75 s = 113 frames at 1080x1920. It's a single plain mesh on black, so it's light for Cycles CPU. I'll measure the real time on the first render and log it, not guess it here.
- One Remotion text pass (seconds), then `ive assemble` with the shared clips and audio.
- Character clips, the shot 1 plate, the music and the mix are **reused unchanged**: **no extra Higgsfield credits per day.**

**Cheaper still:** once you confirm the day list, render **all the numerals in one batch** (e.g. 5, 3, 1 and LAST DAY). Then each posting day costs nothing: pick the file whose `post_date` matches today.
Each output is named `bf9_days-left_<days_left>_<post_date>.mp4`. Before handing over a file, I check it against the calendar in section 1.

**Checks before any day's file ships:**
- Read the final frame of the numeral and the text: is the digit right, and is the singular/plural right?
- Is the wordmark about 720 px wide?
- Loudness: -14 LUFS, true peak below -1 dBFS.
- Contact sheet of every cut.

---

## 5. Asset inventory

| Asset | Status | Path / ID |
|---|---|---|
| Del & Eps reference | **found** | `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg` (locked look, README in the same folder) |
| Silver Integra kitted plate | **to reuse** (from BF 2 / BF 3 once rendered) | `eps-acura-integra-de-v29.glb` (website zip, Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7) / `Integra Type S Full Car.stl` (1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5) |
| Epsilon+ wordmark | **found** | Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Music | **claimed, provisional** | TikTok CML "BLACK FRIDAY" - DJ EV, 7419416839039518737 |
| Numeral rig | **to build** (after approval) | `projects/bf-days-left-countdown/tools/numeral.py` |
| Sale end date/time | **missing**: owner to set | – |
| Countdown days | **missing**: owner to pick | – |

---

## 6. Open questions for the owner

1. **Sale end date and time (Pacific)?** And the start date, if you want a "starts in X days" version too. Nothing renders without the end date.
2. **Which days get a reel?** E.g. 5 / 3 / 1 / LAST DAY, or every day of the window. Batch-render all of them, or render each morning?
3. **Show the end date on screen** ("ENDS DEC 1, 11:59 PM PT")? Default: no, until the window is final.
4. **Offer line under the number?** Options:
   - none (default);
   - "BLACK FRIDAY SALE";
   - a tier from the liquidation sheet (the price source of truth per the owner, `projects/_blackfriday/PRICES.md`), e.g. "30% OFF PU LIPS & SKIRTS".
   - "UP TO 60% OFF" is true, but the sheet's only 60% item is the Integra trunk lip, so it rests on that one product. Your call.
   - Per the owner, every item the sheet prices is on sale even when backordered; no stock counts on screen.
5. **Numeral style:** I recommend **A**, a clean silver numeral built by Eps' scan sweep. One rig works for every digit, so re-renders are cheap.
   - **B:** the digit physically **assembled from kit parts**: lips, skirts and spats from the Integra GLB laid out into the shape of a 5, 3 or 1.
   - B looks great, but each digit needs its own hand layout (more work per day), and the parts would be posed off-car, which bends the "parts move the way they unbolt" rule. Your pick.
6. **Del's gesture:** the model sheet has **no watch**, so I use his tape-roll tap as the "time's ticking" beat rather than adding a watch to the locked look. OK, or do you want a watch added?
7. **Music:** keep DJ EV "BLACK FRIDAY" (provisional), or "BREAKING NEWS" / "Machine Protocol", or your own track?
8. **Car in shot 1:** the Integra, reused from BF 2/3. Or rotate the car per day (Civic FE from BF 1/8, GR Corolla from BF 6) so each countdown looks fresh? This adds one reused plate per car and no new renders if those reels are made first.

---

## 7. Production steps (after approval)

1. Lock the inputs: `sale_end`, the day list and the offer line. Fill in the countdown calendar (section 1) and get your OK on it.
2. Download the track, then run `ive beats` and the kick-envelope check. Set B1 and re-time the shot table; confirm the reel fits in about 8 s.
3. Build `tools/numeral.py`. Render one test digit and check its contact sheet; log the render time.
4. Get a credit quote, then generate the 4 Higgsfield character clips with the model sheet as reference. Check each against the sheet (Eps' cap backwards, Del's short boxed beard), then cut them out.
5. Pull the shot 1 plate from BF 2/3 (or render its 2 s window).
6. Build the Remotion `DaysLeft` composition.
7. Batch-render the numerals for the approved days, assemble every reel and check each one (section 4). Deliver them for review.
8. Self-score with `training/rubric.md`, record feedback and archive.
