# Nissan Frontier Pro-4X - sources

Scan-only Temerario-style reel (no IRL footage, no text). Sibling of ferrari-296 / huracan-evo / a90-supra.

## Scans (engineering Drive folder 1Lwbqt8eQBSSABL0n9VCCJPhjfLdm3xst "Nissan Frontier Pro-4X/Scans")
Downloaded to /home/user/media/nissan-frontier/scans, decimated to 4/2 mm (dec/), levelled (lev/, tools/level.py),
lift/ground cleaned (tools/clean.py), prepped --like prep/car4.json (prep/).

| key | Drive name | id | what it is (looked at it) | use |
|---|---|---|---|---|
| full | Frontier Pro-4X Full Car.stl | 1zpIGLKQp1qtSG91bk8cq_xKg7c-WP7Aq | whole truck on a lift, no wheels, 25M tris | base for every shot (4 mm), close-ups (2 mm nose crop) |
| fbr | Frontier Pro-4X Front Bumper Removed.stl | 1Hg0N4NLbECd4H06axEicbJSZ9hXw0kZa | the removed bumper itself (fascia, grille, fogs), in the car frame | bumper part (minus grille) |
| fbrhc | Frontier Pro-4X Front bumper Removed (Hood closed).stl | 1ynHTSxWeSY0ay5qz2Y2UmRmT3Ug103_I | front end, bumper off, hood shut | registration check |
| bhr | Frontier Pro-4X Bumper and Hood Removed.stl | 1dExmtFOFF-NItzHUHmlkpCTH1G99YmGH | front clip with bumper + hood off: radiator support, core, lamps | structure under the opened front |
| flares | Frontier Pro-4X Fender Flares Removed.stl | 1wWhMrmp7cr4V-g7Fa7E9oWU0Em-2CxOz | lower body + arches without the flares (2 GB) | flares part (difference) + arch fill |
| mount | Frontier Pro-4X Bumper Grille Mounting.stl | 1GQa6LW_u7nnYY9aFZjogJUC4nA1Kb6C6 | lower front bar only | not used (covered by the bumper scan) |
| grille | Frontier Pro-4X Frontier Grille.stl | 15gLCXGBt194TiolPmiFrmxDZWZbcUrGL | stock grille part | grille part |

Not used: `Frontier Accessories *` (badge, grille, fogs, side markers) and `Senta SR Frontier Fog` - aftermarket parts,
brief says our scan of the truck only.

Registration (tools/regcheck.py, median distance to the full car where they overlap): hood-closed 1.3 mm, flares 1.3,
grille 2.1, mount 2.6, bumper+hood removed 3.7, bumper 6.3 mm. All used at identity.

## Logo
remotion/public/illumaesthetic_logo.png (gitignored) = illumaesthetic.com header logo
`cdn/shop/files/IllumaestheticLogo_V2COMPLETE_1.png` (6135x1059, white/red on transparent).

## Music
Original track generated for this reel by the coordinating session (pending at the time of writing).
