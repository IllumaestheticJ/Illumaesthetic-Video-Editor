# Infiniti G35 coupe - Temerario-style scan reel (scan only: no IRL footage, no text)

Engineering Drive folder `Infiniti G35` (1_UIcJgsI3etggSWNFAxa-2ncM8TC8O_X), listed recursively with the service account,
fetched with `ive fetch-drive` to `/home/user/media/infiniti-g35/scans/`.

| Scan | Tris | What it is (looked at) | Used? |
|---|---|---|---|
| Coupe / Infiniti G35 Full Car (1aEYKsbX...) | 24,999,998 | whole coupe incl. ground; front jacked up (2 jack stands), aftermarket spoiler, mesh front / 5-spoke rear wheels | **yes** - car4 (4 mm) wide shots, car25 (2.5 mm) close-ups |
| Coupe / G35 Trunk (10Bfd9r8...) | 5,000,000 | trunk lid outer skin, scanned without the spoiler | **yes** - opening lid + exploded part |
| Coupe / SFP Aero G35 (1ajNhn2X...) | 9,807,277 | partial re-scan of the same coupe (roof/hood/trunk missing, other wheels), same Artec frame (median 3.1 mm) | no - adds no panel |
| Sedan / G35FrontBumper1.obj, FrontBumper2.stl, RearBumper1.obj, RearBumper2.stl | 291k / 291k / 241k / 241k | sedan bumper covers | no - other body (global reg. on coupe fitness 0.04-0.11) |
| Sedan / SFP Front End, Rear End, Left Skirt Removed, Right Skirt Door Open, Right Skirt Mounted, Rear Bumper Removed | 2-4M each | partial sedan states, each in its own frame, no sedan full car | no |

## Frame / processing (all in tools/)
1. `ive decimate` raw full car at 4 / 2.5 mm, trunk at 2 mm.
2. `level.py` (from huracan-evo): RANSAC ground plane -> Z up, long axis -> Y, nose -Y. Ground normal was (0.150,0.040,0.988).
3. `ive crop` + `clean_car.py` (drop z < 4 mm: a pit / jack scraps down to -167 mm).
4. `rake.py`: pitch 3.7 deg nose-down + roll 0.65 deg - the body was nose-up on the jack (wheel centres / arch tops in an
   orthographic side render), applied identically to car + trunk.
5. `stands.py`: two jack stands under the right sill / behind the right front wheel removed.
6. `deplate.py`: licence plate characters flattened (plate-plane projection).
7. `segment.py`: panels cut from the car along seams (hood, front/rear bumper covers, doors+mirrors, spoiler) + lid skin
   removal for the trunk-open base. Checked with colour-coded renders.
8. Every .blend: `ive prep ... --like prep/frame.json` (one transform, pinned).

Registration: trunk part vs car median 4.3 mm as captured; the only large deviation (30-50 mm) is the band under the
car's spoiler (absent from the part scan). ICP's 40 mm "correction" barely changed fitness (0.42 -> 0.43): rejected.

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com (site sits behind a bot check; fetched with Playwright)
-> `remotion/public/illumaesthetic_logo.png` (gitignored).
