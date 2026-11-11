# Infiniti QX80 - sources

Scan only (no IRL footage). Engineering Drive folder `Infiniti QX80` (1iQtSiptYOOJv9XN7nj5j4c6eOkeXXW0W), listed
recursively with the service account. Media in `/home/user/media/infiniti-qx80/` (not in git).

## Used
| Scan | Drive id | Use | Registration (tools/regcheck.py) |
|---|---|---|---|
| Scans/Infiniti QX80 QX80 Full Car.stl (1.75 GB, 35M tris) | 1in6egTiGMJ4TVQoAksGnQjM2YNRh-6em | every shot, 4 mm (5.9M tris) | reference frame |
| Scans/Infiniti QX80 Hood Underside.stl | 1F_ZbmUETtbb1-QWqbM-Obint3UoPZtQL | hood-open state: hinge fit + hood panel + under-hood capture | 2.0 mm |
| Scans/Infiniti QX80 Fender Inner.stl | 1PnmaYH0HieltZw51ddaAfbSBvyiwz1yD | clean right-front fender panel (explode) | 2.4 mm |
| Scans/Infiniti QX80 Wing Only.stl | 1X2buWQWwADa-oIRrsgeiy-0b0zHLNTAP | roof spoiler (explode) | 2.6 mm |
| Scans/Infiniti QX80 Side Vents.stl | 1BR9e1dGzEnicu9r6j3cWJM7vWFAZDMXI | both fender vents (explode) | 3.1 mm |
| Scans/Infiniti QX80 Front Bumper Duct.stl | 1HFpY572q82YtdrP2VkKCSvWcR0RBbRmv | RF bumper corner + left duct (explode) | 7.2 mm |
| Scans/Infiniti QX80 Exhaust cover.stl | 1RaKHdzOOHfZdnFW3Egfw3gR8Yz7QSYNU | two exhaust trims (explode) | 2.4 mm |

Fetched and registered but not used: Right Fender No Vent (1.9 mm; a partial corner capture, the clean fender is
"Fender Inner"), Right Side Skirt Door Open (2.2 mm; fragments, no clean door to hinge).

Not registered to the car (bench scans in their own frames, 0 % overlap): Door Mirror, Front Caliper, Rear Caliper,
T-spec Bumper, NACA Ducts, Badge. Rear Bumper Inner floats mid-car (1 % overlap) - excluded.
Engine / transmission / adaptor-plate / brake CAD folders are GT-R swap engineering, not used (scan reel of the car).

## Frames
Raw Artec frame -> `tools/level.py` (RANSAC ground plane, long axis -> Y, nose +Y): `/home/user/media/infiniti-qx80/level.json`,
then `ive prep --like car6.json` for every mesh (car4, hood, base, parts). Car: 5.36 m x 2.17 m (with mirrors) x 1.94 m.

## Logo
Team Drive `IllumaestheticLogoColor-01.png` (1cZJj521P88T_vC2YZDJVVUCctGyNoukR) -> `remotion/public/illumaesthetic_logo.png`
(gitignored); the website returned a bot-verification page.

## Music
`/home/user/media/work/music/infiniti-qx80_track.mp3` - generated for this reel by the parent session (not in git).
