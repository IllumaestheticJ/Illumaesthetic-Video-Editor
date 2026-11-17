# Black Friday 2026 - brief for the 8 shot-list sessions

Written by the parent session on 2026-11-17. Each session's own concept is in its first message.

You are one of 8 sessions. Each one plans a single Epsilon+ (epsilon.plus, sister brand of Illumaesthetic) Black Friday promo video.

YOUR JOB IN THIS CHAT: plan the full shot list for your video. The owner's request was: "please plan out the shotlist for these videos, using a combination of the website GLB files and our scan data, and our epsilon characters". Do not render or produce the video until the user approves the shot list in this chat.

Repo: branch claude/video-editing-scan-data-8o0m8g. Pull first. Commit and push your plan there; never open a PR.

Read first:
- CLAUDE.md, then knowledge/lessons.md (standing rules, they override everything).
- The skills: .claude/skills/temerario-scan-reel/ (SKILL.md and references/reviewer-rules.md, endings.md, music-and-timing.md) and .claude/skills/scan-video-edit/ (240sx-style).
- Query the knowledge graph from the repo root: graphify query "<topic>". The interpreter path is in graphify-out/.graphify_python.

ASSETS TO COMBINE (find and verify each yourself; list exact paths and IDs in the plan):
- Website GLB files: the Epsilon lookbook/configurator GLBs. They ship part_<part> and body_<part>_stock pieces plus paint materials.
  Repo precedents: projects/toyota-mr2-spyder (kit_nest2.py nests lookbook parts into a scan), projects/honda-civic-11 (Epsilon kit from Ron's files and the lookbook), projects/epsilon-wing-configurator, and the branches for de5-configurator (Integra) and nc-configurator.
- Scan data: the engineering Google Drive, plus knowledge/car-inventory.md and each project's clips.md.
- Epsilon characters / mascots: the Pip and Gus series is on the pip-gus-ep* branches (read with git show <branch>:<path>). Find how they were made, their voices, and their rules, e.g. "Don't make Gus sad", AESUB pronounced AY-EEE-Sub. Confirm whether there are Epsilon-specific characters, and use them where they fit the concept. If you can't find character files, say so in the plan.
- Real footage and photos: Dropbox "/2. Illumaesthetic Videos/1. Video dumps/", Camera Uploads, and "Claude Training/Good Reels". Product photos are on the Shopify listings.
- Prices and stock come ONLY from the live Shopify store (Shopify MCP tools, store "Epsilon+ Aerodynamics"). Re-check them before you finalise; never invent numbers on screen.

STORE FACTS CHECKED BY THE PARENT ON 2026-11-17 (USD, list price):
- Acura Integra DE4/DE5 (2023+):
  - Front Lip $285 PU (stock 26), Side Skirts $400 PU (stock 61), Rear Spats $175 PU (stock 68, OEM Stock and OEM Aero diffuser versions).
  - Rear Trunk Lip $100 gloss black / $300 paint-matched (stock negative = backordered).
  - Sport Wing $500 gloss black / $950-$1,000 paint-matched (11 Acura colours: Majestic Black, Platinum White, Lunar Silver, Urban Gray, Liquid Carbon, Performance Red, Apex Blue, Double Apex Blue, Solar Silver, Tiger Eye).
  - Sport Wing + Rear Trunk Lip combo variant $600 gloss black / $1,050-$1,100 painted.
  - Fender flare widebody $800. GT Wing $1,900-$2,200.
- Honda Civic 11th gen:
  - FE/FL Front Lip $285 (zenki and kouki versions), FE/FL Side Skirts $400, FE Rear Lip $285, FL Rear Lip $285 (pre-order). Paint-matched lip/skirt variants $485 / $800.
  - Sport Wing FL2/FL5 $450 black / $850 painted (13 Honda colours: Championship White NH0, Boost Blue Pearl B637P, Sonic Gray NH877P, Rallye Red R513, Crystal Black, Lunar Silver, Platinum White, Solar Silver, Urban Gray, Meteorite Gray, Sand Dune, Smokey Mauve).
  - Sport Wing FE sedan $450 / $850-$900.
- GR Corolla:
  - V1 Front Lip $215 PU (stock 69) / $600 CF (stock 14), V1 Side Skirts $275 (stock 27), V1 Rear Spats $125 (stock 20).
  - V2 Front Lip $285 (stock 64), V2 Side Skirts $400 (stock 67), V2 Rear Spats $175 (stock 35).
- FG2 Civic Front Lip $150 (stock 64). WRX VB front lip already [CLEARANCE] at $99.99 (stock negative).
- MR2 Spyder (fiberglass, made to order): front bumper $900, side skirt/fender combo $700, rear spats $350, headlight eyelids $100. Rear duckbill $220 (ABS, stock 10). Hood vents $400 / $470 with brackets (fiberglass, backordered). The parent's first search missed this listing.
- NC Miata (fiberglass): front bumper $800-$1,100, fender cuts $300-$350.

KNOWN PROBLEMS WITH THE OWNER'S CONCEPTS (raise the ones that touch your video with the user in this chat; don't silently change the concept):
- The "$750 crossed out -> $385" combo price matches no listing. The combo is $600 (gloss) or $1,050+ (painted), and 30% off $600 is $420. Ask the user for the real Black Friday price.
- Boost Blue / Championship White / Sonic Gray are Civic FL wing colours; the Integra wing uses Acura colours.
- "Only X left": the stocked parts have healthy counts, and backordered ones show negative stock. Don't show a low count unless the store really shows one.
- Discount wording (30% / 45% / 20%) is the owner's. Confirm which products each discount covers before it goes on a card.

HOUSE RULES THAT APPLY:
- 9:16 vertical.
- Real music only, never generated, and not a track another reel already used. Start from the song's beginning. Mix at -14 LUFS with true peak below -1 dBFS.
- Every cut on a measured hit.
- No text over IRL footage unless the user explicitly asks for it for this ad. Raise that conflict if the concept needs on-screen prices over real footage.
- Logo about 720 px wide. For product reels, use the Epsilon wordmark, not Illumaesthetic.
- Scan data only as captured. Kit parts placed accurately from the design files. No clipping, nothing off screen.
- Plates stay, except on the IS300.

DELIVERABLE: projects/bf-<your slug>/shotlist.md containing:
- the concept in one line;
- the target length (short-form, 10-25 s unless the concept needs more);
- the music candidates;
- a numbered shot table: time, duration, beat, camera, subject, the source asset with its exact path/ID (GLB / scan / character / footage / photo), action, on-screen text with its source, transition, and render method (Blender, Remotion, footage edit);
- the asset inventory, marked found / missing / to-request;
- open questions for the user;
- production steps.

Log your decisions with "python -m ive log". Commit, push, then reply in this chat with a short summary and the open questions. Finally, send the parent session a one-paragraph status with send_message: session_id @parent if available, otherwise session_01KS3BnjipTLCB8uZBRBnwzW.
