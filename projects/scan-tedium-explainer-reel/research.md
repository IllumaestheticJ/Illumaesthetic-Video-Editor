# Research: how a full car is usually 3D-scanned, and why it is tedious

Researcher/scriptwriter, 2026-11-14. Sources are scanner makers' own docs and tutorials first (Creality, SHINING 3D / Einstar,
Revopoint, Creaform, Artec, ZEISS), then universities' lab guides, then reseller case studies. Each claim is marked
**SOURCED** (link + quote/paraphrase + where on the page) or **UNSOURCED** (not verified, so it must not go on screen).
Brand names are for this research file only: the reel never names or mocks a scanner brand ("the usual way", "a lot of scanners").

Access notes: support.artec3d.com and docs.artec3d.com/as/20/en/align.html returned HTTP 403 to the fetcher; www.capture3d.com is
not reachable from this session (DNS blocked). Claims that rested only on those pages are marked UNSOURCED or cited via another page.

---

## 1. Marker (target) based scanning: why markers are needed

| # | Claim | Status | Source and quote |
|---|---|---|---|
| M1 | Markers (reference points) are how the scanner works out where it is: it finds the circular reflective dots and positions itself from them. | SOURCED | Creality Wiki, "Guidelines for Using Markers", section *Why Use Markers*: "When the scanner operates, it determines the coordinate information by identifying the circular reflective area of the markers, thereby achieving precise spatial positioning." https://wiki.creality.com/en/3d-scanner/tutorials/general/marker |
| M2 | On a small object the dots can go on the mat or table; on a large object such as a car they must go on the object itself. | SOURCED | Same page, *Sticking Position*: "when the object is large (e.g. the car in the picture below), the markers need to be attached to the surface of the object. Please note that the markers should be randomly placed." |
| M3 | In blue-laser mode markers are mandatory; for featureless objects they are recommended in other modes too. | SOURCED | Same page, *When to Use Markers*: "When scanning in Blue Laser Mode, you must use markers to assist tracking." |
| M4 | Large, smooth vehicle panels are exactly where markers are needed. | SOURCED | SHINING 3D, "Practical automotive 3D scanning tips": "Markers are essential when scanning large vehicles or components with limited geometric features." https://www.shining3d.com/practical-automotive-3d-scanning-tips-for-better-results |
| M5 | Laser handheld scanners position themselves from reflective targets stuck on the part. | SOURCED (via search summary of Digital Engineering, not fetched in full) | Digital Engineering 24/7, "Scan by hand" (HandySCAN): "uses reflective targets applied to the surface of the part to be scanned to position itself." https://www.digitalengineering247.com/article/scan-by-hand/additive-manufacturing |
| M6 | A scanner maker says more than a third of its own users call targets a significant limitation. | SOURCED | Creaform blog, "New 3D scanner revolutionizing extensive surface damage assessment": "Indeed, more than a third of our users have identified the use of targets as a significant limitation of 3D scanning." https://www.creaform3d.com/en/resources/blog/new-3d-scanner-revolutionizing-extensive-surface-damage-assessment (Not used in the script: it would mean quoting a competitor's data.) |

## 2. How many markers, spacing rules

| # | Claim | Status | Source and quote |
|---|---|---|---|
| S1 | Every frame must see at least 4 markers in common with the previous one. | SOURCED | Creality Wiki (marker guide), *Marker Placement Spacing*: "each adjacent frame of data must share at least four common points during continuous alignment." Also: "Ensure at least four markers are visible in the CrealityScan software's view". |
| S2 | Spacing depends on the scanner; one maker gives 60-100 mm (cross-line mode) and 20-50 mm (parallel-line mode) for one series, 80-150 mm / 30-70 mm for another. | SOURCED | Creality Wiki, *Reference spacing*: "For Raptor series scanners, when using cross-line mode, the spacing should be 60mm-100mm, and in parallel-line mode, it should be 20mm-50mm. The Sermoon S1 requires fewer markers, and the spacing should be 80mm-150mm…" |
| S3 | On a car's rear body panel: about 8 cm between points and 8-15 points per frame with one scanner; about 4 cm and more than 5 per frame with a smaller one. | SOURCED | Revopoint blog, "How to 3D Scan a Car's Rear Body Panel" (2023-06-26), *Maker Points*: "If using the RANGE, you can have around an 8cm spacing between the points and around 8 to 15 points per frame. If you're using POP 2, the spacing will need to be smaller, around 4cm, and more than 5 markers per frame". https://www.revopoint3d.com/blogs/blog/how-to-3d-scan-a-car-s-rear-body-panel |
| S4 | A wide-field scanner can space targets "as far as 30 cm" in some cases (i.e. normal spacing is tighter). | SOURCED | Creaform blog (as M6): "In some cases, the targets can even be spaced as far as 30 cm apart." |
| S5 | Markers must be random: no rows, triangles or circles, or the software mis-stitches. | SOURCED | Creality Wiki, *Irregular Distribution*: "Avoid arranging them in regular formations such as straight lines, triangles, or circles. Regularly arranged points can lead to splicing errors". SHINING 3D (as M4): "Distribute markers randomly instead of placing them in straight rows or regular patterns." |
| S6 | Not on edges, holes or engraved features; spray goes on before the markers. | SOURCED | Creality Wiki, *Avoid Special Position* and *Pay attention to the order*: "markers should not be applied at right angles or on edges"; "always apply the spray/powder before attaching markers." |
| S7 | If the software says "Not enough markers", you pause and add more. | SOURCED | Creality Wiki, *Marker Recognition Preview*: "If the software always prompts "Not enough markers", you can pause the scan and add markers to the area where there are insufficient markers." |
| S8 | A whole car needs "hundreds" of markers. | UNSOURCED | A search summary attributed this to SHINING 3D; the fetched page gives no count. Rough arithmetic (car skin area / 8 cm grid) would suggest that order, but that is my estimate, not a source. Not used on screen. |
| S9 | Total number of markers for a full car. | UNSOURCED | No maker gives one. Not used. |

## 3. Time to apply and remove markers

| # | Claim | Status | Source and quote |
|---|---|---|---|
| T1 | Applying and removing adhesive markers on vehicles is time-consuming and labour-intensive. | SOURCED | SHINING 3D (as M4): "repeatedly applying and removing adhesive markers can be both time-consuming and labor-intensive." |
| T2 | People resort to tricks to avoid "scrapping them off one by one" (markers on strips of clear tape; magnetic marker blocks). | SOURCED | Revopoint blog, "3D Scanning Tracking Aids" (2023-06-20), *Sticky Tape*: "you might not want to place tons of markers on an object individually and then spend a long time scrapping them off one by one." Warns the tape "may pull chunks" of paint. https://www.revopoint3d.com/blogs/blog/3d-scanning-tracking-aids |
| T3 | Makers sell faster-to-remove alternatives (marker pyramids, magnetic targets) because stickers are slow. | SOURCED | SHINING 3D (as M4): "Marker pyramids provide an efficient alternative…". Creaform (as M6): magnetic targets "can be positioned and removed more quickly than traditional markers." |
| T4 | Markers can be avoided on show cars to protect paint. | SOURCED | SCANTECH case study: "Marker-based positioning was not an option for the vehicle's exterior". https://www.3d-scantech.com/3d-scanning-solutions-for-automotive-inspection-and-vehicle-digitization/ |
| T5 | Minutes/hours it takes to apply or remove markers on a whole car. | UNSOURCED | No maker or tutorial gives a figure. Do not put a marker-time number on screen. |

## 4. Scanning in sections and aligning / registering / merging in software

| # | Claim | Status | Source and quote |
|---|---|---|---|
| A1 | A whole vehicle is scanned as overlapping sections. | SOURCED | SHINING 3D (as M4): "When scanning an entire vehicle, divide the project into overlapping sections to simplify data alignment." |
| A2 | With too little computer memory, a car panel scan "will need to be split into sections and merged once finished". | SOURCED | Revopoint (as S3), *Device*. |
| A3 | Standard software workflow: Scanning, Cleaning, Alignment, (Global) Registration, Fusion, Postprocessing. Alignment = "Aligning multiple scans of the same object"; fusion makes "a single surface, as opposed to the multiple surfaces that constitute the source scan". | SOURCED | Artec Studio 20 docs, "3D Scanning at a Glance": https://docs.artec3d.com/as/20/en/qsg.html (note: this applies to the scanner family Illumaesthetic itself appears to use, so it is not an "only the old way" claim). |
| A4 | Auto-alignment exists; manual alignment is used when it fails "owing to a lack of texture or lack of overlapping areas". | SOURCED | Same page, *Alignment*. Einstar/EinScan docs call manual alignment a fallback when auto alignment fails (search summary). |
| A5 | Manual alignment = click matching points on two scans, at least 3 pairs, then repeat scan by scan. | SOURCED | University of Melbourne NExT Lab, Artec guide "Manual Alignment": "Select [New Pair] and click a matching point on each model. Repeat step 3 until you have at least 3 pairs of matching points… Repeat steps as necessary to align more scans (layers) one by one". https://ms-kb.msd.unimelb.edu.au/next-lab/3d-scanning/guides/artec-eva-3d-scanner/manual-alignment |
| A6 | Merging separate projects by markers needs markers that both projects saw. | SOURCED | Einstar Support, "Detailed introduction of Manual Alignments": "Make sure you are using the common markers between projects to do the manual alignment." https://support.einstar.com/support/solutions/articles/60001106931-detailed-introduction-of-manual-alignments |
| A7 | A real full-car job (reseller case study): scanned "in sections and stitch them together later"; halves aligned in one program, stitched in another; "captured the car's body in about three hours". | SOURCED (one case, reseller blog) | Top3DShop, "We 3D Scanned a Rolls-Royce Wraith". https://top3dshop.com/blog/case-study-how-we-3d-scanned-a-rolls-royce-wraith-for-customization . One case, one scanner; not a general rule, so not on screen. |
| A8 | Very large projects are registered in chunks (e.g. ~100 scans at a time) when the software cannot show all at once. | UNSOURCED | From a search summary of an Artec support article and a third-party blog; the support page returned 403. Not used. |

## 5. Photogrammetry-target workflows for large objects

| # | Claim | Status | Source and quote |
|---|---|---|---|
| P1 | For large parts a photogrammetry camera first builds a "positioning model": place coded targets, take several blocks of convergent photos, run bundle adjustment; scale bars give the scale; the scanner then uses that model. | SOURCED (maker brochure via search summary) | Creaform MaxSHOT 3D brochure: "place a few coded targets either on the object to be measured or in its environment, take several blocks of convergent photos and launch the bundle adjustment process"; "The scale bars provided in the measurement volume allow for model scaling." https://hitech.netlify.app/uploadedFiles/MaxSHOT3D_Brochure_EN_EMEA_08072014.pdf |
| P2 | ZEISS/GOM TRITOP: regular markers on the object plus coded markers and a scale bar; photographed; the structured-light scanner then uses these reference points to transform each measurement into one frame. | SOURCED (paper, via search summary) | IMEKO 2000 paper on TRITOP: "The markers are applied onto the object to be digitized and some coded markers and a scale bar are placed in addition onto the object." https://imeko.org/publications/wc-2000/IMEKO-WC-2000-TC14-P399.pdf |
| P3 | A full-vehicle tutorial covers "placing the reference points for scanning and the coded markers and scale bars for photogrammetry" then capturing "the vehicle from many different angles". | SOURCED | Hands-on Metrology video page "How to scan a complete vehicle": https://www.handsonmetrology.com/es/video/how-to-scan-a-complete-vehicle/ |

## 6. Post-processing time

| # | Claim | Status | Source and quote |
|---|---|---|---|
| X1 | After scanning: noise/outlier removal, fusion, hole filling, simplification, texturing are separate steps. | SOURCED | Artec Studio 20 docs (as A3). |
| X2 | Turning a car scan into surfaces (NURBS) "takes hours". | SOURCED (one case, reseller blog) | Top3DShop (as A7). Scan-to-CAD is beyond what the reel shows; not used. |
| X3 | Typical hours for aligning + fusing a full-car scan. | UNSOURCED | No maker gives a number. Not on screen. |

## 7. Sources that disagree / caveats
- Marker spacing ranges from ~2 cm to 30 cm depending on scanner and mode (S2, S3, S4). The script therefore says "every few inches"
  (≈ 8 cm, S3, the only car-specific figure) and the on-screen number is "~8 CM", attributed to a car-panel tutorial in this file.
- Markers per frame: "at least four" (Creality, S1) vs "8 to 15" / "more than 5" (Revopoint, S3). The script uses the floor: "4+".
- Whole-car times in vendor case studies range from "1.5 hours" (marker-free, SCANTECH) to "about three hours" (Top3DShop) to
  "overnight" with two scanners (Digital Engineering). None is a neutral benchmark; **no time figure for the usual way goes on screen.**
  The spinning wall clock carries "it takes a long time" without a number.
- Auto-alignment exists in all modern software (A4); manual point-pair alignment (A5) is the fallback, not every scan pair.
  The cartoon exaggerates by showing the manual case; the on-screen text only states the sourced rule ("3+ matching points").

## 8. What Illumaesthetic's own data supports (for Part B)
- Scanned handheld after spraying, no markers: from the production brief; consistent with the R2 contact sheet (no marker dots visible on the
  powdered IS350 in any R2 frame, `/home/user/media/work/is350-reels/out/is350_reel_R2_real_to_scan_contact.jpg`). Owner to confirm "NO MARKERS" before it goes on screen.
- Scanner model: the host says "Artec Leo" on camera (projects/lexus-is350-speedrun-long/transcript.md, FX30541 [03:58], FX30555 [00:20.7]),
  but the long-form treats brands as owner-only, so the script does not name it.
- Time: 32 min from go / 20 min without the crash / bet 15 min (lexus-is350-reels/brief.md). The owner asked that R3 not give the real time away;
  this reel does not show 32 or 20. "Minutes, not hours" is supportable from the 32-minute run and is offered as an owner option only.
- Whether the IS350 data needed alignment/merging of several scans is **not documented** in the project notes. The script therefore does not
  claim "no stitching" or "one pass".
