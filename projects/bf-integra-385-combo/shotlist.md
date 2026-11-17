# BF 3/8 - "What $385 gets you" (Integra Sport Wing + Rear Trunk Lip combo) - SHOT LIST (draft v2, awaiting approval)

Planned 2026-11-17. Nothing is rendered until the user approves this plan in chat.
v2: the owner's BF doc fixes the prices (gloss-black combo $600 -> $385, no dates on screen), and the owner chose the
Epsilon mascots **Del & Eps** (projects/_blackfriday/MASCOT_AND_PRICES.md), not Pip & Gus.
v3: the characters follow the owner's LOCKED look, `knowledge/characters/del-and-eps/README.md` + `del-eps-model-sheet.jpg`
(branch claude/clever-shannon-u8rv5l). That look is a matte arcade-racing-game 3D style: Del has a boxed beard, a teal cap
with an orange brim and a headset; Eps wears a violet cap backwards and a visor with yellow eye marks, and carries the
scanner. The parts and scans stay silver/black product; the characters are the only colour.

**Concept (one line):** Eps opens the combo box with his scanner, and the Sport Wing and Rear Trunk Lip rise out on its beam. Del taps the receipt, and $600 is struck to
$385, so the combo costs less than the wing alone at full price ($500). The parts fly onto the Integra, and a hard 1:1 cut takes us
from the CGI car to the scan and on to the real car.

**Target length:** about 17 s (one 4-beat bar per shot at about 120 BPM; re-timed to the chosen track's measured hits).
9:16, 1080x1920, 30 fps. Ends on the Epsilon+ wordmark, not Illumaesthetic.

## Prices (source of truth: the owner's BF liquidation sheet; projects/_blackfriday/PRICES.md)
Owner's decision (2026-11-17): use the sheet "Black Friday 2026 Liquidation Pricing" (Pricing tab; snapshot
`projects/_blackfriday/bf_liquidation_pricing.csv`, rev 25) **even where store stock is negative**. The crossed-out price is the
sheet's "Current Price" and the sale price is its "BF 2026 Price". No stock counts on screen, and no dates (the window isn't set).

| Item (sheet row) | Was | BF | Used on screen |
|---|---|---|---|
| Sport Wing + Rear Trunk Lip - Integra, Gloss Black | $600 | **$385** | shot 4 strike + stamp, shot 1 title, end card |
| Sport Wing - Acura Integra, Gloss Black | $500 | $350 | shot 2 receipt line ($500, the wing's current price) and "less than the wing alone ($500)" |
| Rear Trunk Lip - Acura Integra, ABS Gloss Black | $100 | $40 | shot 3 receipt line ($100) |
| Combo, Paint Matched | $1,050 | $835 | not shown (the ad is the gloss offer) |

The sheet's own note on the combo: "$385 so the combo beats wing ($350) + trunk lip ($40) bought separately" ($390), so
the combo is also the cheapest way to buy both during the sale. Re-read the live sheet (PRICES.md) before final render.
Shopify product refs: wing gid://shopify/Product/7386931298348 `epsilon-wing-acura-integra-de-2023` (combo gloss variant
45259291000876, SKU EPS-DE4-SWG-ABS-27); lip gid://shopify/Product/7386985332780.

## Music candidates (real tracks from Dropbox /Moosic, not used by any reel in projects/*)
1. **Claimed in projects/_blackfriday/MUSIC.md:** Lil Jon ft. The Eastside Boyz, "Get Low" (NFSU OST), Dropbox id:ihAynaYnO_4AAAAAAACRvA (mp4; extract the audio). Punchy and recognisable, with a big hit for the drop at the 1:1 cut.
2. Backup: Juiced OST 23, Way Out West, "Killa", id:ihAynaYnO_4AAAAAAACRvw.
(GT2 "Arcade Mode Theme" went to BF 4.)
Start at the song's beginning. Mix at -14 LUFS with true peak below -1 dBFS. The 8 BF sessions draw from the same folder,
so the parent should confirm no other BF video takes the same track.

## Shot table (times assume 120 BPM; snapped to measured kicks after `ive beats`)
Recommended version **A (CGI unboxing on black, with Eps and Del)**: the concept's "hand" becomes Eps's scanner, and every
text item sits on black or CGI, so the no-text-over-IRL rule holds. The characters appear only in shots 1-4 (and the
optional sting), never in the car, scan or IRL shots, so they cost about five short character clips.
**Character method (owner's locked path):** Higgsfield image/video with `del-eps-model-sheet.jpg` as the reference image.
The clips go on a flat key background, are keyed, and are composited over our Blender renders of the box, parts and car;
the products are always our own renders, never AI-drawn. No 3D rig is built for this ad.

| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-2.00 | 2.0 | bar 1, b1-b4 | high 3/4 over the box, 50 mm, 5 % push-in | **Eps** (locked look) beside the closed Epsilon+ box on pure black | box modelled in Blender from the real packaging photos on the lip listing (`integra-rear-trunk-lip-carbon-and-painted-packed.heic`, `...-carbon-packaging.heic`, cdn.shopify.com/s/files/1/0036/2250/2435/files/) | Eps walks in from frame right on b1-b2, aims the scanner at the box; a cyan (#6fc3d6) sweep crosses it and the flaps pop open on b4 | "WHAT $385 GETS YOU" title on black above (owner's line; BF liquidation sheet) | hard cut on bar 2 b1 | Blender (Cycles) + Remotion title |
| 2 | 2.00-4.00 | 2.0 | bar 2 | same side, lower, box in lower third | **The Sport Wing rises out on Eps's scanner beam**; Eps tracks it, then gives a visor ^ ^ | `eps-acura-integra-type-s-de5-v19.glb` node `part_sport_wing` (lookbook sha 4eb01375eebf623b), gloss-black material | wing lifts out (Blender) and turns a quarter to show its profile; Eps is a composited clip. **His hands never touch the part**, because AI video can't hold our real geometry. The part stays true gloss black | receipt panel slides in on the black space on the right: "SPORT WING ..... $500" (live store, wing alone, gloss) | hard cut, bar 3 b1 | Blender + Remotion `Receipt` (new component) |
| 3 | 4.00-6.00 | 2.0 | bar 3 | wing parked high, frame out | **the Rear Trunk Lip rises** on a second sweep | same GLB, node `part_duckbill` (= Rear Trunk Lip) | lip comes out under the wing; Eps swings the scanner down to follow it | receipt adds "REAR TRUNK LIP ..... $100" (live store) | hard cut, bar 4 b1 | Blender + Remotion |
| 4 | 6.00-8.00 | 2.0 | bar 4 | both parts floating side by side, front-on; **Del steps in** at frame left | Del next to the receipt, Eps beside the parts | as 2+3 | slow 15 deg orbit | Del taps the receipt (point action); "COMBO $600" is struck through on b2, then "$385" stamps in on b3 (BF liquidation sheet). Line under it: "less than the wing alone ($500)" (store list price) | hard cut, bar 5 b1 | Blender + Remotion |
| 5 | 8.00-10.00 | 2.0 | bar 5 | rear 3/4 of the car, low, 35 mm | CGI Integra Type S, no kit | `eps-acura-integra-type-s-de5-v19.glb` (body/shell/glass/wheels; paint from the lookbook list, e.g. Platinum White, to match the end photo) | wing drops onto the deck, lip slides onto the trunk edge, both seat on b3 / b4 | none | **hard 1:1 cut on the drop** (same camera) | Blender |
| 6 | 10.00-12.00 | 2.0 | bar 6 | same camera, orbiting 25 deg toward the solved photo camera | the scan of the car with the kit on | scan `Integra Type S Full Car.stl` Drive 1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5 (decimated, <=4 mm); wing = `Integra Sport Wing Scan .stl` 1s5ggkKLZPmIdofrnGhpy-upbbcNw6rTq; lip = CAD `Integra Rear Wing + Duckbill Final.stp` 1hpc2giqPqY6-4S23JUBxqXjTzuZ1DAes, placed by ICP from engineering's frame | house silver on black; orbit eases to rest exactly on the photo's solved camera | optional HUD, max 1 item, only if true (Q6), e.g. a triangle count from the STL header | **hard 1:1 cut** scan -> photo on a kick | Blender + Remotion HUD |
| 7 | 12.00-14.00 | 2.0 | bar 7 | the photo's own framing; shared Ken Burns zoom-out (fg2 kenburns.py) | the real Integra with the wing and lip fitted | Shopify wing listing photo `white-rear-quarter` (or a black-kit photo if one exists, Q3) | slow zoom out | **none (IRL)** | hard cut, bar 8 b1 | footage edit |
| 8 | 14.00-15.00 | 1.0 | bar 8 b1-b2 | real pan along the wing | finished Sport Wing on the white Integra | Dropbox `/1. Epsilon Plus Videos/1. Video dumps/*Posted Videos (Finished Legacy Raw)/Integra Sport Wing Install Tutorial/C0222` | short real-motion beat | **none (IRL)** | hard cut, bar 8 b3 | footage edit (tonemap if HLG) |
| 9 | 15.00-17.00 | 2.0 | bar 8 b3 - bar 9 | static, 3 % push-in | end card on black | Epsilon+ wordmark Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W, 720 px wide | wordmark lands on the downbeat; music fades with it | "SPORT WING + TRUNK LIP  $385" / "BLACK FRIDAY" / "epsilon.plus" (BF liquidation sheet; **no dates**). Optional 0.5 s sting: Eps pats his pockets, Del holds up the 10 mm socket (the running gag; reference `del-eps-10mm-socket-gag.jpg`) (Q4) | end | Remotion |

**Version B (if the owner films a real unboxing, Q1):** shots 1-4 become real hand footage (iPhone, 9:16, top-down on a
bench, box -> wing -> lip). The receipt can't sit over the footage unless the owner OKs it (Q2). Without the OK, the
receipt goes on a black panel in the lower 40 % and the footage stays in the top 60 %, with no text on the footage
itself. Shot 5 becomes a 1:1 cut from the last unboxing frame (the wing in the hands) to the GLB wing at the same pose
(the fg2 rule: start the CG part where the real hands hold it). Shots 6-9 stay the same.

## Asset inventory
| Asset | Status | Path / ID |
|---|---|---|
| Lookbook GLB, Type S | **found**, downloaded | `eps-acura-integra-type-s-de5-v19.glb` (19.07 MB) -> /home/user/media/bf-integra-385-combo/glb/. Nodes: body, glass, interior, part_duckbill, part_sport_wing, shell, trim, underbody, wheel_*, exhaust_*. It has no body_*_stock pieces (check how the bare trunk edge looks with part_duckbill hidden) |
| Lookbook GLB, base DE4 | found (backup) | `eps-acura-integra-de-v29.glb` (16.08 MB, has body_duckbill_stock); same folder |
| Full-car scan | found | Engineering Design/Acura Integra Type S/Integra Type S Full Car.stl, 1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5 (1.24 GB); rescan 10eR0dVkan3A_2iPDbvO1AzjFXvjK_77I |
| Sport Wing part scan | found | Engineering Design/Acura Integra 2021+/Integra Sport Wing Scan .stl, 1s5ggkKLZPmIdofrnGhpy-upbbcNw6rTq (250 MB) |
| Wing + trunk lip CAD | found | .../Acura Integra 2021+/CAD/Integra Rear Wing + Duckbill Final.stp, 1hpc2giqPqY6-4S23JUBxqXjTzuZ1DAes |
| Trunk lip print STL | found | Projects_/Integra 2023/A Spec Printing Files/Duckbill/Integra_duckbill_v2_fixed_2.stl, 125yWp0-im3kd86nV8enEmgwt50tg3Ao0 |
| Trunk lip part scan | **missing** | use the CAD instead |
| Real unboxing footage of this combo | **missing** | closest: `/Footage Library/Videos/Shoot Sessions/2026-11-04 Body kit parts unboxing/` (3 phone clips, parts unknown, not yet viewed), the install raws C0188-C0241 (no unboxing confirmed). **To request** (Q1) |
| Packaging photos | found | lip listing: integra-rear-trunk-lip-carbon-packaging.heic, ...-carbon-and-painted-packed.heic |
| Finished-car photos | found | wing listing: white-rear-quarter, blue-side-profile, champagne, gray-rear, ...; lip listing: rear-three-quarter, rear-on, ... (finish of each to be checked against gloss black, Q3) |
| IRL wing footage | found | Install Tutorial C0222 (finished wing pan); posted `3. Short form/Posted/integra sport wing.mp4` (not reused as an edit) |
| Epsilon+ wordmark | found | Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Characters: **Del & Eps** (Epsilon+) | **found (locked look)** | `knowledge/characters/del-and-eps/README.md` and `del-eps-model-sheet.jpg` (the reference; front/3-4/side/back of both), `del-eps-10mm-socket-gag.jpg`, `del-eps-install-drill-template.jpg`. On this branch (commit 46e523b). Original Higgsfield jobs: bdb1a2e8, 069f42d6, e3315b11, 85f40a22. No 3D model or rig, and none is needed for this plan. Pip & Gus are **not used** |
| Music | found | see candidates above |

## Open questions for the user
1. **Unboxing:** CGI unboxing by Eps (version A, recommended), or will you film a real one (version B)? In version B the
   characters drop out of shots 1-4.
2. **Text over real footage:** only matters in version B. Version A puts all text on black.
3. **Finish:** should the CGI parts be gloss black (the $385 variant)? And is there a real photo of an Integra with the
   *gloss-black* wing and lip fitted for shot 7? The white car in the listing photos may have painted parts.
4. **Del & Eps extras:** the locked look is now settled. The plan has no dialogue, music only, since no voices are cast yet:
   should one line be added (e.g. Eps: "Customer asks... what does $385 get me?" Del: "Both.")? And keep the 10 mm end sting?
5. **Character approval gate:** before any video, I'll make one Higgsfield still of shot 4 (Del + Eps with our rendered
   parts) from the model sheet for your OK, keeping credits minimal. OK?
6. **Claim text** on the scan shot (e.g. "designed on a 3D scan of the Integra")? Default: none.
7. **Music:** "Get Low" (claimed) is the default; say if you want "Killa" or your own track.

## Production steps (after approval)
1. `ive log` each approved decision. `ive fetch-drive` the scan, wing scan and CAD into /home/user/media/bf-integra-385-combo/.
2. Scan prep: decimate the full car out of core to <=4 mm, ground cleanup, pin with `--like`.
   Register the wing scan and CAD to the car by ICP from engineering's frame (GR Corolla v12 rule), and check close-ups at the mounting edges.
3. GLB: import the Type S v19, check part_sport_wing/part_duckbill against the CAD (they must match the real parts), set
   gloss-black parts, and set the car paint to match the end photo.
4. Box model from the packaging photos (plain, no invented logos or labels), studio-on-black lighting.
4b. Del & Eps: Higgsfield with `del-eps-model-sheet.jpg` as the reference image. First a single still for the owner's OK
   (Q5), then about five short image-to-video clips (walk-in + scanner aim, track the wing, track the lip, Del's tap, the
   optional sting) on a flat key background. Key them and composite them over the Blender plates, with scale and light
   matched to the black stage. Check every clip against the sheet: Del's beard short and boxed, Eps's cap backwards. No
   AI-drawn products and no on-screen text from the AI.
5. Music: download, `ive beats`, kick-anchored grid, lay the cuts in frames.
6. Solve the end-photo camera against the scan (ferrari-296 photo_search), end shot 6's orbit on it, 1:1 cut.
   Align the CGI with the scan (align_game.py) so cut 5->6 is 1:1.
7. Framing previews at 30 %, then finals one at a time in the background. Persistent data off; per-frame luma check.
8. Remotion: a new `Receipt` component (Inter Display / JetBrains Mono, #e8ecf2, strike + stamp on beats), title, end card.
9. `ive director` pass, assemble, contact sheet + frames +/-2 around every cut, check the cuts against the decoded audio, loudness check.
10. Self-score with the rubric, deliver, record feedback, archive, commit and push.
