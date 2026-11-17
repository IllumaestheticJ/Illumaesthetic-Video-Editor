# BF 3/8 - "What $385 gets you" (Integra Sport Wing + Rear Trunk Lip combo) - SHOT LIST (draft, awaiting approval)

Planned 2026-11-17. Nothing is rendered until the user approves this plan in chat.

**Concept (one line):** the combo box opens and the Sport Wing and Rear Trunk Lip come out. A receipt shows the
combo costs less than the wing alone at full price. The parts fly onto the Integra, and a hard 1:1 cut takes us
from the CGI car to the scan and on to the real car.

**Target length:** about 17 s (one 4-beat bar per shot at about 120 BPM; re-timed to the chosen track's measured hits).
9:16, 1080x1920, 30 fps. Ends on the Epsilon+ wordmark, not Illumaesthetic.

## Prices (live Shopify, re-checked by this session on 2026-11-17)
| Item | Variant ID | List | Stock |
|---|---|---|---|
| Sport Wing, gloss black (wing only) | 42916569415724 | $500 | -10 (backorder) |
| Combo Sport Wing + Rear Trunk Lip, gloss black (SKU EPS-DE4-SWG-ABS-27) | 45259291000876 | $600 | -4 (backorder) |
| Combo, painted (9 colours) / Platinum White | 44810179051564 ... / 44810179084332 | $1,050 / $1,100 | 0 or below |
| Rear Trunk Lip ABS gloss black (alone) | 42916797153324 | $100 | -18 |
Product: gid://shopify/Product/7386931298348 `epsilon-wing-acura-integra-de-2023`; lip gid://shopify/Product/7386985332780
`epsilon-rear-trunk-lip-acura-integra-de4-de5-2023`.
**No listing is $750.** $385 is below the $500 wing-alone price, so the pitch holds. Every price on screen is
`[WAS]` / `[BF]` until the user gives them (Q1).

## Music candidates (real tracks from Dropbox /Moosic, not used by any reel in projects/*)
1. Lil Jon ft. The Eastside Boyz, "Get Low" (NFSU OST), Dropbox id:ihAynaYnO_4AAAAAAACRvA (mp4; extract the audio). Punchy and recognisable, with a big hit for the drop at the 1:1 cut.
2. Juiced OST 23, Way Out West, "Killa", id:ihAynaYnO_4AAAAAAACRvw.
3. Gran Turismo 2, "Arcade Mode Theme", id:ihAynaYnO_4AAAAAAACRvg.
Start at the song's beginning. Mix at -14 LUFS with true peak below -1 dBFS. The 8 BF sessions draw from the same folder,
so the parent should confirm no other BF video takes the same track.

## Shot table (times assume 120 BPM; snapped to measured kicks after `ive beats`)
Recommended version **A (CGI unboxing on black)**: every text item sits on black or CGI, so the no-text-over-IRL rule holds.

| # | Time | Dur | Beat | Camera | Subject | Source asset (exact) | Action | On-screen text (source) | Transition out | Render |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00-2.00 | 2.0 | bar 1, b1-b4 | high 3/4 over the box, 50 mm, 5 % push-in | closed Epsilon+ shipping box on pure black | box modelled in Blender from the real packaging photos on the lip listing (`integra-rear-trunk-lip-carbon-and-painted-packed.heic`, `...-carbon-packaging.heic`, cdn.shopify.com/s/files/1/0036/2250/2435/files/) | box sits still; flaps pop open on b4 | "WHAT [BF] GETS YOU" title on black above the box (owner's line; price = Q1) | hard cut on bar 2 b1 | Blender (Cycles) + Remotion title |
| 2 | 2.00-4.00 | 2.0 | bar 2 | same side, lower, box in lower third | Sport Wing rises out of the box | `eps-acura-integra-type-s-de5-v19.glb` node `part_sport_wing` (lookbook sha 4eb01375eebf623b), gloss-black material | wing lifts out and turns a quarter to show its profile | receipt panel slides in on the black space on the right: "SPORT WING ..... $500" (live store, wing alone, gloss) | hard cut, bar 3 b1 | Blender + Remotion `Receipt` (new component) |
| 3 | 4.00-6.00 | 2.0 | bar 3 | wing parked high, frame out | Rear Trunk Lip rises out | same GLB, node `part_duckbill` (= Rear Trunk Lip) | lip lifts out under the wing | receipt adds "REAR TRUNK LIP ..... $100" (live store) | hard cut, bar 4 b1 | Blender + Remotion |
| 4 | 6.00-8.00 | 2.0 | bar 4 | both parts side by side, front-on | the two parts together | as 2+3 | slow 15 deg orbit | receipt: "COMBO [WAS]" struck through on b2, then "[BF]" stamps in on b3 (user-supplied prices, Q1). Optional line under it: "less than the wing alone" | hard cut, bar 5 b1 | Blender + Remotion |
| 5 | 8.00-10.00 | 2.0 | bar 5 | rear 3/4 of the car, low, 35 mm | CGI Integra Type S, no kit | `eps-acura-integra-type-s-de5-v19.glb` (body/shell/glass/wheels; paint from the lookbook list, e.g. Platinum White, to match the end photo) | wing drops onto the deck, lip slides onto the trunk edge, both seat on b3 / b4 | none | **hard 1:1 cut on the drop** (same camera) | Blender |
| 6 | 10.00-12.00 | 2.0 | bar 6 | same camera, orbiting 25 deg toward the solved photo camera | the scan of the car with the kit on | scan `Integra Type S Full Car.stl` Drive 1SzdWjN092P5lqGnmAnTjxNqEBSWbs2d5 (decimated, <=4 mm); wing = `Integra Sport Wing Scan .stl` 1s5ggkKLZPmIdofrnGhpy-upbbcNw6rTq; lip = CAD `Integra Rear Wing + Duckbill Final.stp` 1hpc2giqPqY6-4S23JUBxqXjTzuZ1DAes, placed by ICP from engineering's frame | house silver on black; orbit eases to rest exactly on the photo's solved camera | optional HUD, max 1 item, only if true (Q6), e.g. a triangle count from the STL header | **hard 1:1 cut** scan -> photo on a kick | Blender + Remotion HUD |
| 7 | 12.00-14.00 | 2.0 | bar 7 | the photo's own framing; shared Ken Burns zoom-out (fg2 kenburns.py) | the real Integra with the wing and lip fitted | Shopify wing listing photo `white-rear-quarter` (or a black-kit photo if one exists, Q4) | slow zoom out | **none (IRL)** | hard cut, bar 8 b1 | footage edit |
| 8 | 14.00-15.00 | 1.0 | bar 8 b1-b2 | real pan along the wing | finished Sport Wing on the white Integra | Dropbox `/1. Epsilon Plus Videos/1. Video dumps/*Posted Videos (Finished Legacy Raw)/Integra Sport Wing Install Tutorial/C0222` | short real-motion beat | **none (IRL)** | hard cut, bar 8 b3 | footage edit (tonemap if HLG) |
| 9 | 15.00-17.00 | 2.0 | bar 8 b3 - bar 9 | static, 3 % push-in | end card on black | Epsilon+ wordmark Drive `EPSILON+ Logos/Epsilon+ Logo.png` 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W, 720 px wide | wordmark lands on the downbeat; music fades with it | "SPORT WING + TRUNK LIP  [BF]" / "BLACK FRIDAY" / "epsilon.plus" (prices Q1, dates Q7) | end | Remotion |

**Version B (if the owner films a real unboxing, Q2):** shots 1-4 become real hand footage (iPhone, 9:16, top-down on a
bench, box -> wing -> lip). The receipt can't sit over the footage unless the owner OKs it (Q3). Without the OK, the
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
| Real unboxing footage of this combo | **missing** | closest: `/Footage Library/Videos/Shoot Sessions/2026-11-04 Body kit parts unboxing/` (3 phone clips, parts unknown, not yet viewed), the install raws C0188-C0241 (no unboxing confirmed). **To request** (Q2) |
| Packaging photos | found | lip listing: integra-rear-trunk-lip-carbon-packaging.heic, ...-carbon-and-painted-packed.heic |
| Finished-car photos | found | wing listing: white-rear-quarter, blue-side-profile, champagne, gray-rear, ...; lip listing: rear-three-quarter, rear-on, ... (finish of each to be checked against gloss black, Q4) |
| IRL wing footage | found | Install Tutorial C0222 (finished wing pan); posted `3. Short form/Posted/integra sport wing.mp4` (not reused as an edit) |
| Epsilon+ wordmark | found | Drive 1ITcVMoXW7Rs580760cSbFBAmn9zkkt0W |
| Characters | **found, but they are Illumaesthetic mascots** | Pip and Gus, branches `claude/pip-gus-ep0-intro`..`ep9-aesub`; procedural build `projects/scan-tedium-explainer-reel/tools/partA_scene.py`; no Epsilon character exists. **Not used in version A** (Q5) |
| Music | found | see candidates above |

## Open questions for the user
1. **Prices:** what is the crossed-out price, and what is the Black Friday price? The store has the gloss-black combo
   at $600 and the wing alone at $500. Nothing is $750. Is $385 for gloss black only? (Painted is $1,050-$1,100.)
   Plan: strike $600 (or the $500 + $100 parts sum, which is the same), stamp the BF price.
2. **Unboxing:** there is no real unboxing footage of this combo. Use the CGI unboxing (version A, recommended), or will you
   film one (version B: top-down, 9:16, box -> wing -> lip, 10-15 s raw)?
3. **Text over real footage:** do you want the receipt over real footage for this ad? Version A avoids the question; in
   version B the receipt sits on a black panel unless you say it can go over the footage.
4. **Finish:** the $385 offer is presumably gloss black. Should the CGI parts be gloss black? And is there a real photo of
   an Integra with the *gloss-black* wing and lip fitted? The white car in the listing photos may be painted, and photos
   must show the part in its finished state.
5. **Characters:** Pip and Gus are Illumaesthetic mascots, and there is no Epsilon character. Should they stay out of
   this ad (recommended; their cel style clashes with the silver scan look), or should Pip's mitten hands open the box in
   shot 1?
6. **Claims:** may the scan shot say anything (e.g. "designed on a 3D scan of the Integra")? Default: no claim text.
7. **Dates/fine print:** BF start and end dates, and whether a code is needed, for the end card. Note that the combo
   variant is backordered (stock -4), so no "only X left". Also, the trunk lip carries a `laborday-exclude` tag, and its
   Tiger Eye variant is $230 against $300 for the other colours, which looks like a store entry error.
8. **Music:** pick one of the three candidates, or supply a track.

## Production steps (after approval)
1. `ive log` each approved decision. `ive fetch-drive` the scan, wing scan and CAD into /home/user/media/bf-integra-385-combo/.
2. Scan prep: decimate the full car out of core to <=4 mm, ground cleanup, pin with `--like`.
   Register the wing scan and CAD to the car by ICP from engineering's frame (GR Corolla v12 rule), and check close-ups at the mounting edges.
3. GLB: import the Type S v19, check part_sport_wing/part_duckbill against the CAD (they must match the real parts), set
   gloss-black parts, and set the car paint to match the end photo.
4. Box model from the packaging photos (plain, no invented logos or labels), studio-on-black lighting.
5. Music: download, `ive beats`, kick-anchored grid, lay the cuts in frames.
6. Solve the end-photo camera against the scan (ferrari-296 photo_search), end shot 6's orbit on it, 1:1 cut.
   Align the CGI with the scan (align_game.py) so cut 5->6 is 1:1.
7. Framing previews at 30 %, then finals one at a time in the background. Persistent data off; per-frame luma check.
8. Remotion: a new `Receipt` component (Inter Display / JetBrains Mono, #e8ecf2, strike + stamp on beats), title, end card.
9. `ive director` pass, assemble, contact sheet + frames +/-2 around every cut, check the cuts against the decoded audio, loudness check.
10. Self-score with the rubric, deliver, record feedback, archive, commit and push.
