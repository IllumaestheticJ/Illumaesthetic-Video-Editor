# Suzuki Cappuccino - scan-only Temerario-style reel

No IRL footage, no text (brief). Reference: `training/references/README.md` -> `v_jul22_1047_58` (Temerario).

## Scans (engineering Drive)
Folder `Suzuki Cappucino/Scan Data` (1cBbPLMHVcJ32NoTsjRmxnnzcZJrYnU4L), Artec exports 2026-07-19, all in one frame.
The near-duplicate `Cappuccino/Cappuccino scans` (19KYLrtuvoFRRdXCGpJukAm516UUzh3e6) holds byte-identical copies
(md5 match) minus Rear End Trunk Open; that folder's FBX/.blend/renders/inspo/car photos are not raw scan data - not used.

| File | Drive id | tris | what it is |
|---|---|---|---|
| Full Car.stl | 1DPxH_AwA5PJxDq9BaNyZ6BR4qa-hMNRQ | 24,996,349 | hardtop on, closed; tyres/rims captured |
| Front Bumper.stl | 1NErzIA5KGP4CNEss3mQZdrzkA6ZQ7-sI | 14.7M | bumper skin, off the car, inside+outside |
| Front Bumper Lights.stl | 1y3SqM85OwA16FWNc5QgkosEUJhAvMHYc | 0.8M | the two bumper lamps |
| Front Bumper Off, Hood Open.stl | 1GprbIXD0mjO-Qi5_fgat3kTZuH0osXBT | 10.0M | front clip: engine bay, radiator, one fender + lamp; propped hood only a sliver |
| Rear Bumper.stl | 1lSVfbwinMyuiErzuHKgXgntDFoMmBTqp | 15.5M | bumper skin |
| Rear End Trunk Open.stl | 1bio3xb8Gstb8BTACnFbRbYxBykLfFL2E | 10.0M | rear end, bumper on, lid propped (partial) |
| Rear Bumper Trunk Open.stl | 1KOGZEXp1YIyWR4tKEPaUWWU1Z6tgxR4_ | 10.0M | same capture as Rear End Trunk Open (identical regcheck) - unused |
| Rear End All Removed.stl | 1HU1aGgnNrnEAX4HgQ76NS5yqOQq--0T9 | 10.0M | rear end, bumper off: rear panel, exhaust, boot |
| Suzuki Cappuccino New Turn Signal.stl | 1ADYeF80x4rQEv03siYG7-sPczI3CfmK3 | - | Oct design part, not a capture state - unused |

Measured: footprint 3,277 x 1,504 mm (incl. mirrors), wheelbase 2,060 mm (wheel centres in the levelled scan).

## Pipeline (media in /home/user/media/suzuki-cappuccino, blends in /home/user/media/work/cappuccino/blend)
decimate (2 mm parts, 2/3/4 mm car) -> tools/level.py (one rigid transform, level.json) -> ive crop (--footprint-from car)
-> tools/regcheck.py -> tools/lids.py (hood/trunk lid cut from the car) -> tools/hinge.py (hinge_hood.json, hinge_trunk.json)
-> tools/composite.py (base.stl, fb_nolights.stl) -> ive prep (car3.json master, everything else --like car3.json)
-> shots.py -> tools/shot.py (Blender) / tools/framing.sh.

## Logo
`remotion/public/illumaesthetic_logo.png` = illumaesthetic.com/cdn/shop/files/IllumaestheticLogo_V2COMPLETE_1.png (needs a browser UA).
