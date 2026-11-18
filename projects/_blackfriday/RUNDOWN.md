# Epsilon+ Black Friday 2026: rundown (as of 2026-11-18)

Nine short 9:16 promo reels for **Epsilon+** (epsilon.plus, Illumaesthetic's aero-parts sister brand). Each reel is built in its own Claude Code cloud session, coordinated by a parent session. All work is on the branch `claude/video-editing-scan-data-8o0m8g` of `IllumaestheticJ/Illumaesthetic-Video-Editor`. There are no PRs. Each project lives in `projects/bf-<slug>/`, and the shared files are in `projects/_blackfriday/`.

## The 9 videos

| # | Slug | Concept | Latest | Status |
|---|---|---|---|---|
| 1 | civic-parts-rain | Civic 11 kit parts rain down and land on the car on the beat: "Black Friday: 30% off the full kit" | v0.5 | In review |
| 2 | integra-stock-to-kitted | Integra goes from stock to kitted. Full-bleed scrolling BLACK FRIDAY wall intro; kit parts highlighted on the real footage | v0.9 | In review |
| 3 | integra-385-combo | "What $385 gets you": Sport Wing + trunk lip combo, RETAIL $600 crossed out, BF $385 | v0.9 | In review |
| 4 | paint-match-roulette | Wing / lip colour roulette across a car lineup (Civic, Integra Type S, DE4 widebody...) in a racing-game-menu style | v0.9 | In review |
| 5 | clearance-shelf-drop | Clearance parts drop onto a shelf, with glossy carbon | v0.6 | **Approved**; final pending the Akira font swap |
| 6 | gr-corolla-track | GR Corolla on track: "V2 kit 30% off, V1 up to 45% off" | v0.6 | In review |
| 7 | miata-mr2-night-meet | NC Miata + MR2 Spyder night meet: "Fiberglass 20% off", with TC wings and an MR2 diffuser | v1.6 (50.7 s) | In review; length decision pending |
| 8 | scan-teardown-prices | Scan teardown with a price on every part; ends 1:1 on Ron's render | v0.8 | **Approved**; final pending the Akira font swap |
| 9 | days-left-countdown | Car drives or drifts over "BLACK FRIDAY SALE" on the floor, which swaps to "X DAYS LEFT" | v0.5 (drive + drift, 9.4 s each) | Waiting on sale dates |

The rendered mp4s are at `/home/user/media/work/out/bf-<slug>_v<N>.mp4` inside each video's own session (media is never committed).

## Owner rules for this campaign (newest first)

1. **Fonts:**
   - **Akira Expanded** (commercial licence confirmed 2026-11-18) for headlines, offers, big prices and countdown numbers.
   - Text **right next to the logo** uses a different, matching font: **Unbounded** 300-400. Small labels use Unbounded 500.
   - Akira is on Drive at `EPSILON+ Logos/AkiraExpanded-SuperBold.otf` (ID `1nrF80enolDd9HAu5807kv5XIx0cUSDya`). Install it to the gitignored `assets/fonts/akira/`; **never commit it.** Unbounded (OFL) is in `assets/fonts/unbounded/`.
   - Akira is ASCII only, with no → arrow, so show was/now prices with a crossed-out old price.
   - Details: `knowledge/fonts.md`.
2. **URL** is always **WWW.EPSILON.PLUS**.
3. **Safe zones** (Reels / TikTok / Shorts), for 1080x1920:
   - All text, prices and logos sit inside **x 48-920, y 285-1440**.
   - Nothing important goes in the bottom 480 px, the right rail (x>920, y 900-1440) or the top 220 px.
   - Key offers stay inside the 4:5 feed crop.
   - Check with `python scripts/safezone_check.py out.mp4 [--text-boxes boxes.json]` and **look at** the sheet. Spec: `knowledge/safe-zones.md`.
4. **No Del & Eps / mascots** in BF videos: just typical Epsilon+ branding content.
5. **Prices come only from the BF liquidation sheet**, even where the store's stock disagrees. The sheet is Claude Sheets "Black Friday 2026 Liquidation Pricing", mirrored in `projects/_blackfriday/bf_liquidation_pricing.csv` and `PRICES.md`.
   - Was = Current Price; BF = BF 2026 Price.
   - Never derive or invent a number, and show no stock counts unless the owner asks.
   - Parts not on the sheet show their regular price only and are left off the % card.
6. **Only show colours each car was really sold in** (e.g. Tiger Eye Pearl is Integra Type S only, not DE4).
7. **Quick, short first drafts**, then iterate on the owner's notes in each chat.
8. **Music:** one real track per video, no repeats and never generated. Mix at -14 LUFS with true peak below -1 dBFS, with cuts on measured hits. Registry: `projects/_blackfriday/MUSIC.md`.
9. Standing house rules still apply (`CLAUDE.md`, `knowledge/lessons.md`):
   - only real scan data;
   - no text over IRL footage unless OK'd in that video's chat;
   - Epsilon wordmark at about 720 px;
   - plates blurred only on the IS300.

## Key prices (BF sheet)

| Item | Was | BF |
|---|---|---|
| Integra Sport Wing + trunk lip combo, gloss | $600 | $385 |
| Integra Sport Wing, gloss | $450 / $500 | $315 / $350 |
| Integra trunk lip, ABS | $100 | $40 |
| Integra trunk lip, CF | $240 | $96 |
| GR Corolla V1 carbon lip | $600 | $330 |
| FG2 front lip | $150 | $79.99 |

The MR2 front bumper has no BF deal. The full table is in `PRICES.md`.

## Open questions for the owner

1. **BF9:** sale end date and time, and which days get an "X days left" reel.
2. **BF7:** it runs 50.7 s against the 10-25 s target. Keep it, or cut it (e.g. one car per reel)?
3. **BF4:** prices for the paint-matched lip and flares are missing from the sheet. The FE Platinum White wing price was derived and needs confirming.
4. **BF5:** keep the "ONLY 14 LEFT IN CARBON" line?
5. **BF6:** the canards "BACK IN STOCK" caption conflicts with the store, which shows them on backorder.
6. **BF8:** Ron's end render has gold wheels while the scan wheels are now silver.
7. **All:** should car parts also stay clear of the right-side button rail (BF1, BF7 and BF8 briefly pass under it)? Should every video carry part-name + was/now labels like BF7?

## Sessions (for send_message)

| Role | Session ID |
|---|---|
| Parent | session_01KS3BnjipTLCB8uZBRBnwzW |
| BF1 | session_01KS3BnjQvC5Jwt8werdkQBu |
| BF2 | session_01KS3BnmM54rXYGMV1RvcvZf |
| BF3 | session_01KS3BnnazWMpySj8txWHeua |
| BF4 | session_01KS3Bnkpa1e8EVisa1cNNaR |
| BF5 | session_01KS3Bnmz82He8An7T2ENwZy |
| BF6 | session_01KS3Bnka9bHh81UskP8hSEK |
| BF7 | session_01KS3BnkgfkzP1tsykcS3KiF |
| BF8 | session_01KS3Bnn3GHL1sQkZRAiLmRx |
| BF9 | session_01KS3BnkWMe1ARdePp9ffKPm |

## Files to read first

- `projects/_blackfriday/`:
  - `BRIEF.md`
  - `PRICES.md`
  - `MUSIC.md`
  - `ASSETS.md` (Drive / Dropbox IDs for GLBs, scans and logos)
  - `MASCOT_AND_PRICES.md` (decision log, newest first)
- `knowledge/fonts.md`
- `knowledge/safe-zones.md`
- `knowledge/lessons.md`
- Each video's `projects/bf-<slug>/shotlist.md` and its feedback log
