# Lexus IS300 (first gen, XE10) - scan reel sources

Scan only (no IRL footage, no text). Engineering Drive folder `Lexus IS300` (1-trkEdLN6tjMSWdl18OpvXN8NJnQQVUZ),
fetched with `python -m ive fetch-drive <id> /home/user/media/lexus-is300/scans`.

| File | Drive id | Date | Use |
|---|---|---|---|
| IS300 Full Car.stl (930 MB, 18.6M tris) | 1-v5mBT5upzAlgA3L26viXBjJdrpRtLVc | 2026-06-22 | **base** (4 mm full shots, 2 mm close-ups) |
| IS300 Squire Edition.stl (837 MB) | 10DhRvIfolLB9POyyYFxx8JYNZgQfXy4U | 2022-07-25 | not used: same car/frame as Full Car (1.5 mm median) |
| IS300 front end bumper removed .stl | 1TIl6UsKuSqVVHg-ZguyAKSJ-9qT6OqRY | 2023-10-07 | state: FMIC, radiator, crash structure, lamps, wheel; defines the front bumper (car - state) |
| IS300 Rear Trunk Open.stl | 1TIyj5cIf2oEaFc4xtd8Bn32f5QHeDkXr | 2023-10-07 | state: rear bumper off + trunk open (bumper beam, trunk floor/interior), lid only a fragment |
| IS300 OEM Trunk.stl | 1IOwNB00cmafy6SeUWikLG4I-UNM_fNJn | 2022-10-17 | lid rear face only (ragged top); defines the lid's rear face/width |
| IS300 Rear Bumper.stl | 1WUxeKX-m89JVDEEEF4H2nokLDNz6hxre | 2023-10-30 | part: rear bumper cover (exploded view) |
| IS300 Side Skirt.stl | 1WSQ9BaF_vXFcVOmMFoBcaEvfoNjJHaZT | 2023-10-30 | part: right side skirt (exploded view) |
| IS300 sIDE sKIRT under.stl | 1WSAUHRUdlfprTaX4ix7XdnqIMuwKStLS | 2023-10-30 | state: right sill/lower doors with the skirt off |
| IS300 Headlight / dash / Interior / Sake Wave 1_1 | - | 2022-24 | not used (body reel) |

All part/state scans are in their own frames -> registered to the full car (tools/register.py; transforms in
`/home/user/media/work/is300/reg/*.json`), then one levelling transform (`level.json`) + `ive prep --like car.json`.
Checks: `/home/user/media/work/is300/chk/sheet*.jpg` (red part over silver car + part alone).

Logo: `remotion/public/illumaesthetic_logo.png` = `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com (Shopify CDN), gitignored.
Music: original track generated for this reel by the coordinating session (ElevenLabs via Higgsfield) - see project.yaml.
