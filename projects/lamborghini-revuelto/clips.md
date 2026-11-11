# Lamborghini Revuelto - sources

Scan-only Temerario-style reel (no IRL footage, no text). Reference: `training/references/README.md`
(`v_jul22_1047_58` Temerario section).

## Scans (engineering Drive "Lamborghini Revuelto" 14GtNl467QXsTocssFNsSOpahDMLP4V5p / "Full Scans")
All from the 2026-07-26 capture session (same Artec frame). Raw STLs were decimated to 2 mm out of core
(`ive decimate`), levelled with one rigid transform (`/home/user/media/lamborghini-revuelto/level.json`), then deleted.
Media lives in `/home/user/media/lamborghini-revuelto/` (`dec2/`, `lev/`, `clean/`, `comp/`, `blend/`).

| Scan (Drive id) | Raw tris | Role |
|---|---|---|
| Full Car (1eEahwd9dZ6vTDjDM_MY8Yp5WEk-Ein6K, 1.75 GB) | 34,994,797 | base of everything; 3 mm (`car_3mm`), 2 mm close-up zones (`car_zone`) |
| Front Bumper (Huren Scans, 1Nc-mocVS6l1...) | 14,996,520 | part (fb) |
| Head Lights (Huren Scans, 14luKU_ExdhF...) | 6,986,365 | part (hl) |
| Rear Bumper (Forced) (1Lf0UYx6bkP7...) | 14,993,289 | part (rb) - the "forced" capture overlaps the car 82 % |
| Rear Wing (17j8kR8Z3yOO...) | 7,235,817 | part (wing) |
| Fender (1xrp6Jz_awj9...) | 4,096,099 | part (fe), car's left front, upper fender |
| Side Skirt Front / Rear (1l65GDDey8LH... / 1R1MYAC5UBHT...) | 2,461,576 / 2,565,228 | parts (ssf, ssr), left |
| Side Fin (1E0e72DwweDj...) | 2,036,794 | part (fin), left |
| Side Mirrors (1Ib1FRq372Ne...) | 5,641,869 | part (mir), left mirror only |
| Left / Right Tail Light (1XanQglS... / 1ciNB9ut...) | ~3.1 M each | parts (tll, tlr) |
| Hood Open (Huren Scans, 1sY2pSRbmdeX...) | - | state: frunk exposed; open lid used to fit the hood hinge |
| Front End Bumper & Headlights Removed (Huren Scans, 1Jg13BQSWF2G...) | - | state, front structure for the base |
| Rear End Bumper Off (Tail Lights Off) (1LAFScbb-0Xe...) | - | state, rear structure |
| Rear End Wing Removed (1bSvd8xVhVtL...) | - | state |
| Fender Removed (Mounting) (1duC8KTZu1kT...) | - | state |
| Side Skirts & Fin Removed (1GaJ5mCRN6k1...) | - | state |
| Wheels (1RMYz9LhOVWm...) | - | fetched, not used (full car captured the wheels fully) |

Not used: 2024 "Lamborghini Revuelto Full Scan.stl" (other session), "VF Scans" exhaust/engine-bay set (other
session, exhaust product work), cats/catback/airducts, top bumper halves, diffusers (overlap the rear bumper).

Derived: `hood` = the front lid cut from the full car (tools/hood.py), `base` = exploded-view base (tools/composite.py).

## Music
Original track generated for this reel by the parent session (ElevenLabs via Higgsfield) - see project.yaml.

## Logo
`remotion/public/illumaesthetic_logo.png` = illumaesthetic.com `IllumaestheticLogo_V2COMPLETE_1.png` (gitignored).
