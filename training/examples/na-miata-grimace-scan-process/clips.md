# NA Miata "Grimace" / NB chassis-scan reel — clip notes

Dropbox: `/3. Epsilon Motorsports/1. Video Dumps/NA MIATA GRIMACE/` (downloaded to /home/user/media/miata/dropbox).

**Important:** the car that was scanned is NOT Grimace. The team's rough cut ("Does chassis bracing actually do anything?")
explains Grimace's cage rules it out of a flex test, so they scanned a silver stock **NB Miata** ("Miata chop shop" reference car).
All heatmap PDFs and Drive scans are that NB. Grimace (purple NA, #558) appears only in the Jun 7 Sonoma track-day clips.

## Footage used
| local | source | content |
|---|---|---|
| v0607_113440 | Video Jun 07 2026, 11 34 40 AM.mov (iPhone HLG, portrait, 3.9 s) | Grimace sweeps past close on the paddock exit — hook |
| irl_front.mp4 | MiataScan_RoughCut_1.mp4 185.90–187.75 (45 frames @23.976), crop x0=1520 (right of the burned-in title) | scanner close-up → silver NB front 3/4 in the shop, car on the ground; last frame = match frame (187.70) |
| irl_side.mp4 | rough cut 201.97–204.74, crop x0=660 | tech walks in with the Artec scanner → right side door/rear arch, front corner on the jack; last frame = match frame (204.70) |

Rough cut (4K 23.976, 7:05) spans with burned-in subtitles/section titles were not usable (no text over IRL footage).
Text-free scanning spans found: 140.5–141.7 (outdoor low push-in, too wide-angle to solve), 186.83–187.75, 201.95–204.75,
372.5–377.5 (engine-bay scanning).

## Other footage (not used)
- 38 more iPhone clips Jun 5–7: Sonoma track day (paddock, fuelling, driver changes, on track, pit board), GoPro GX010102.
- Fuji Dump (Thered): track footage, skipped per brief. GX010100.MP4 (7 GB) skipped.
- Chassis Scan Video/: 10 PDF reports only (no video).

## Scans (engineering Drive, service account; folder 1RbQSJ_kRFcjJwRs7hlSPaUe7-9FEsbyO)
| file | tris (STL header) | use |
|---|---|---|
| NB Miata Scan Control Ground Scan.stl | 24,997,127 | match cut 1, end orbit (= listing render) |
| NB Miata Scan Strut Tower Jacked Exterior.stl | 24,993,431 | match cut 2 (front corner jacked) |
| NB Miata Scan Engine Bay Control.stl | 4,997,392 | bay base (no brace) |
| NB Miata Scan Strut Brace Jacked Up.stl | 4,998,154 | strut bar extracted by ICP diff vs control |
Also on Drive: Jacked Exterior, Fender and Strut Jacked Up Exterior, Fender Brace Only Jacked (1.25 GB each), Jacked Up / Fender Brace / Fender+Strut engine-bay states.

## Data (distance PDFs, page 2 — engine-bay width)
control 960.948 mm · jacked, no bracing 962.643 (+1.695) · strut brace 961.679 (+0.731) · fender + strut 961.384 (+0.436) · fender brace only 961.185 (+0.237).

## Listing
illumaesthetic.com/products/mazda-mx-5-miata-nb-3d-scan-1998-2005 — "Mazda Miata (NB) 3D Scan (1998-2005)"; its
"stock front left" photo is a grey render of this same Control Ground scan (same hood blotches / wheels).
