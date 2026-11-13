# Miata chassis-bracing long-form ("Does chassis bracing actually do anything?") - notes

Team took over the edit from 3:04 of `MiataScan_RoughCut_1.mp4` (4K 23.976, 7:05).
Dropbox: `/3. Epsilon Motorsports/1. Video Dumps/NA MIATA GRIMACE/MiataScan_RoughCut_1.mp4` (only source; no raw scanning clips,
no chassis-flex graphics exist on Dropbox). Local: `/home/user/media/miata-bracing/`.

## Rough cut map (seconds)
| span | content |
|---|---|
| 0-12.5 | hook to camera, title card |
| 12.5-46.3 | VO "All cars flex..." over Sonoma track footage + stock NB photos (13.98-28.78 replaced by new 2D graphics) |
| 46.3-183.6 | braces (Goodwin fender braces, strut tower brace), Miata Chop Shop, 4-scan test plan. **Voice ends at 183.3** |
| 184.27-189.19 | control: scanning on the ground (only 4.9 s) |
| 189.19-211.96 | jack, tape measure, scanning jacked, no bracing |
| 211.96-248.0 | stock data cards (width, table, how-to-read at ~225-229.3, exterior heat maps) |
| 248.0-270.94 | strut tower brace install + scan (burned title to ~4:14) |
| 270.94-298.59 | strut data cards |
| 298.59-322.28 | fender off, fender brace install (title to 306.26), scanner over the brace (bumper off) |
| 322.28-330.21 | scanning fender + strut (burned title) |
| 330.21-363.24 | fender + strut data cards |
| 363.24-372.33 | removing strut brace (burned title to 371.04) - NOT used: out of order once fender-only comes first |
| 372.33-381.01 | engine-bay scan, fender braces only |
| 381.01-425 | fender-only data cards, fade out. No conclusion in the rough cut. |

Shoot order was strut -> fender+strut -> fender only. Requested story order: control -> fender -> strut -> both.
Audio after 3:04 is clip-native shop sound, silent on cards (no music bed), so re-ordering does not break music.

## Data (engineering Drive, folders 1QEe8o-y_xDQIpmim9qll9y7_g_kBj6ko and 10kmp8vpKMAJ6jE31KHDMHvIrG0WbJ4s3)
`Strut Spread.xlsx` (engine-bay width, mm): control 960.948 | jacked no bracing 962.643 (+1.695) | fender braces only 961.185 (+0.237) |
strut brace only 961.679 (+0.731) | fender + strut 961.384 (+0.436). Reduction vs unbraced: 86 % / 57 % / 74 %.
PDFs are image-only (no text layer): 4 engine-bay reports (p2 width, p3 strut-tower heat map, scale about +-3 mm) and
4 exterior heat-map reports vs Control Ground Scan (6 pages; scale +-15 mm, **fender+strut report is +-8 mm**).
Read off the colours: unbraced rear quarter ~+10 mm one side / deep blue other side; fender-only rear ~+5-10 mm one side;
strut-only almost all within +-2.5 mm; both within ~2 mm except the door (hinged panel, likely latch position).
The tower close-ups do NOT show a clear braced-vs-unbraced difference (both within ~1 mm), so no claim is made from them.

## Scan-driven heat maps (tested 2026-11-12)
Exterior STLs (Drive folder 1RbQSJ_kRFcjJwRs7hlSPaUe7-9FEsbyO; ids in tools/../editlog) are **exported already aligned to the control**
(same frame as the reports; x = length with nose at +x, z up, floor at z = -1154, car yawed ~15 deg in XY). Do NOT re-ICP the whole
scan: the floor is in every scan and the car moves relative to it, so a global ICP gets worse (median 5.6 -> 22 mm).
`tools/heat.py control.stl state.stl out.png --asis` (6 mm decimation, signed distance along the control normal) reproduces the
report pattern for control vs jacked. Body-only stats (z > floor + 420 mm, 790k points, 92-94 % covered), |deviation| in mm:

| state | median | p90 | p99 | within 2.5 mm | within 5 mm | front third median | mid | rear third median |
|---|---|---|---|---|---|---|---|---|
| jacked, no bracing | 1.82 | 7.29 | 9.59 | 58 % | 77 % | 0.44 | 1.97 | 3.65 |
| fender braces only | 1.90 | 6.16 | 9.84 | 60 % | 84 % | 0.99 | 1.30 | 4.33 |
| strut tower brace only | 0.89 | 2.46 | 4.74 | 91 % | 99 % | 0.70 | 0.54 | 1.66 |
| fender + strut | 1.14 | 3.98 | 8.55 | 74 % | 94 % | 0.53 | 0.89 | 2.36 |

The exported alignment is anchored at the front of the car (front third within ~1 mm in every state), so the maps show how far the
rear moves relative to the front. Includes doors, soft top, glass (hinged/soft panels) - not chassis only.

## Strut-top spread cross-check (2026-11-12, tools/towerspread.py)
Engine-bay STLs are also exported in a shared frame (median 1.0-1.4 mm to control). Strut-top stud centres picked on the control
height map: A (1085, 368), B (856, -577) in XY. Local trimmed ICP of each strut-top patch (state -> control), radius 35/45/60 mm:
- no bracing, jacked: spread change +0.38 / +0.45 / +0.36 mm
- fender braces only: +0.86 / +0.97 / +0.73 mm (the Distance Measurement PDF p3 says +0.691 for the same pair at strut-top centres)
- strut brace, both: not measurable this way (brace bracket covers tower B; residuals 2-4 mm, results swing -8 to -0.2 mm)
So at the strut tops fender-only is NOT smaller than unbraced, while the xlsx "engine bay width" (other points) says 1.695 -> 0.237.
The two definitions disagree on ranking: the script must not rank the braces or recommend one. Owner/engineer question #1.

## Music (2026-11-13) - Dropbox `/3. Epsilon Motorsports/1. Video Dumps/Media for Miata Brace Vid/`
Epidemic Sound tracks + SFX + screenshots + `Miata Brace Video.prproj` one level up. Fingerprint match against the rough cut (tools: see final.py):
0-48 s Dark Summer Night from 3.8 s | ~50-180 s speech (no confident match) | 180-240 2AM from 92.3 s | 240-270 Cosmic Countdown from 87.9 s |
270-298, 330-360, 380-425 Dark Summer Night from ~84 s, ducked ~25 dB (data cards) | 298-330 Time Stand Still from 137 s | 360-380 Time Stand Still from 104 s.
The rough cut is NOT one continuous track after 3:04: v6's "un-ducked bed" was a patchwork. v7 lays the real tracks per section at one level.
