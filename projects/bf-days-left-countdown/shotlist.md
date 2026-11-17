# BF 9: "days-left-countdown" shot list (TEMPLATE PLAN, waiting for the owner's approval)

**v0.2 (2026-11-17): safe zones** (`knowledge/safe-zones.md`, owner rule). All text, logos, the numeral and the car sit inside x 48-920 / y 285-1440. The layout is centred on x 484, the centre of the safe box, not the frame. Numeral content is 562x688 px at y 330-1018; "DAYS LEFT" (118 px) is centred on y 1110; "BLACK FRIDAY SALE" on y 1235; the wordmark block is at y 790-1010. The render (including the scan beam) is clipped to the safe box. `scripts/safezone_check.py` is part of every delivery.

**v0.1 (2026-11-17): NO Del & Eps.** The owner's instruction is "tell all the black friday agents to not use del & eps, just typical branding content" (MASCOT_AND_PRICES.md, e05c325). All character shots, cameos and placeholders are removed, and no Higgsfield credits are spent. Music changed to "BREAKING NEWS" (see section 2).

Planned 2026-11-17 on branch `claude/video-editing-scan-data-8o0m8g`. **Nothing is rendered until the owner approves this plan in chat.**

**Owner request (verbatim):** "add another chat that makes a short reel that says X days left"

**One line:** a silver kitted Integra on black, then a cyan scan line builds a huge silver numeral **X** from wireframe; it lands on the music's drop, "DAYS LEFT" slams in under it, and the reel ends on the Epsilon+ wordmark. One template, re-rendered per posting day: only the numeral and the line under it change.

**Format:** 1080x1920 (9:16), 30 fps, **9.4 s** (cuts on the measured hits of the track).

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

**Used: "BREAKING NEWS" - DJ DF KIT** (TikTok CML, song_clip_id 7622371201206765569, 72.8 s), from 0 s, claimed in MUSIC.md.
It has hard stabs from 0.3 s and a sustained section from 4.62 s.
- The first claim, DJ EV "BLACK FRIDAY" (7419416839039518737), is released: it's quiet until about 27 s, so no hit is reachable in a sub-10 s reel that starts at the song's beginning.
- Backup: "Machine Protocol" - Wbsound (7671666742675539969).

Measured hits on the decoded audio: 1.96 s, 4.62 s (section start, drop), 5.13 s, 6.01 s, 6.92 s. Mix: -13.5 LUFS integrated, peak -2.6 dBFS.
**The same track is used for every day's reel**, so the series reads as one campaign.

## 3. Shot table

| # | Frames / time | Dur | Hit | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition | Render method |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | f0-58 / 0.00-1.97 | 1.97 | song start → 1.96 s hit | Low rear 3/4, 28 mm, crop-in + 6 % push | Silver Integra DE with the Epsilon kit (lip, skirts, spats, Sport Wing, trunk lip) on black | `eps-acura-integra-de-v29.glb` (website zip, Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7); flares and stock duckbill hidden. Final: swap in the BF 2/3 plate (real scan) once rendered | Slow push | none | hard cut on 1.96 s | Blender still (`tools/plate_integra.py`) + push in the edit |
| 2 | f59-138 / 1.97-4.62 | 2.67 | 1.96 s → drop 4.62 s | Front-on, static | Pure black; a cyan (#6fc3d6) scan line descends; the numeral **X** builds behind it from wireframe to house silver | `tools/numeral.py --text X` (Blender text geometry, Inter Display Black; the number comes from `days_left`, never from AI) | Silver finishes exactly on the drop, with a key-light flare | the numeral **is** the text | continuous | **Blender (per day)** |
| 2b | (LAST DAY variant) | same | same | same | Same, string `LAST\nDAY` | same rig | same | "LAST DAY" (geometry) | same | Blender (once) |
| 3 | f139-207 / 4.62-6.92 | 2.30 | drop → 6.92 s hit | Same, 4 % push | Numeral held | same render | "DAYS LEFT" / "DAY LEFT" slams in on 5.13 s; "BLACK FRIDAY SALE" fades in on 6.01 s; optional `offer_line` replaces it | "DAYS LEFT" (template); "BLACK FRIDAY SALE"; `offer_line` only from the liquidation sheet (PRICES.md) | hard cut on 6.92 s | Blender numeral + text overlay (PIL in v0; Remotion `DaysLeft` for final) |
| 4 | f208-281 / 6.92-9.40 | 2.48 | 6.92 s → end | Static | Epsilon+ wordmark, **720 px** wide, centred; "BLACK FRIDAY" above it, "WWW.EPSILON.PLUS" below | Drive `EPSILON+ Logos/Epsilon+ Logo.png` (1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W) | Lands on the hit and fades out with the music (audio fade from 8.8 s) | "BLACK FRIDAY", "WWW.EPSILON.PLUS" (owner: always www.); optional `ENDS <date> <time> PT` only if `show_end_line` | end | overlay |

**Rule checks:**
- No IRL footage, so no text-over-IRL conflict.
- Everything is silver on black.
- No characters (owner, 2026-11-17).
- No prices, stock counts or dates on screen unless confirmed (Q3, Q4). Any number comes from the liquidation sheet (PRICES.md).

## 4. Render method and per-day cost

**Built once (shared by every day):**
- the shot 1 plate (v0 uses a GLB still; final reuses the BF 2/3 scan plate);
- the music and mix;
- the wordmark card;
- the compositor (`tools/compose_v0.py`, then a Remotion `DaysLeft` composition for the final).

**Per day:**
- One Blender numeral render: 149 frames at 1080x1920, Cycles CPU, 16 samples. Measured at **about 6.5 s/frame, about 16 min** per number.
- Compositing and encoding: about 1-2 min.
- **No generation credits.**

**Batch:** once the day list is confirmed, render every numeral back-to-back, one job at a time. Each posting day then costs nothing: pick the file named `bf9_days-left_<days_left>_<post_date>.mp4` and check it against the calendar in section 1.

**Checks before any day's file ships:**
- Read the final frame of the numeral and the text: is the digit right, and is the singular/plural right?
- Is the wordmark about 720 px wide?
- Loudness: -14 LUFS, true peak below -1 dBFS.
- Contact sheet of every cut.

## 5. Asset inventory

| Asset | Status | Path / ID |
|---|---|---|
| Silver Integra kitted plate | **v0: GLB still rendered**; final: reuse BF 2/3 | `eps-acura-integra-de-v29.glb` / `Integra Type S Full Car.stl` (1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5) |
| Numeral rig | **built** | `projects/bf-days-left-countdown/tools/numeral.py` |
| Epsilon+ wordmark | **found** | Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Music | **claimed** | TikTok CML "BREAKING NEWS" - DJ DF KIT, 7622371201206765569 |
| Sale end date/time | **missing**: owner to set | – |
| Countdown days | **missing**: owner to pick | – |

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
5. **Numeral style:** I recommend **A**, a clean silver numeral built by the scan sweep (the v0.1 draft). **B** builds each digit from Integra kit parts laid out into its shape: it looks great, but every digit needs its own layout.
6. (Dropped: Del's gesture. The owner removed Del & Eps from the BF videos.)
7. **Music:** keep "BREAKING NEWS" (used in v0.1), or "Machine Protocol", or your own track?
8. **Car in shot 1:** the Integra, reused from BF 2/3. Or rotate the car per day (Civic FE from BF 1/8, GR Corolla from BF 6) so each countdown looks fresh? Each car adds one reused plate, and no new renders if those reels are made first.

---

## 7. Production steps (after approval)

1. Lock the inputs: `sale_end`, the day list and the offer line. Fill in the countdown calendar (section 1).
2. Swap the shot 1 plate for the BF 2/3 scan plate, or render its still from the scan.
3. Build the Remotion `DaysLeft` composition: the text, wordmark and end line.
4. Batch-render the numerals for the approved days, one at a time.
5. Assemble and check every reel (section 4), then deliver for review.
6. Self-score with `training/rubric.md`, record feedback and archive.

