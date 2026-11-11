# Director report - projects/lexus-is350-scan-process/project.yaml

Total 28.07 s. Sections (s): whole 12.07, front 5.0, side 1.5, rear 9.5

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| irl_walkout | 0.0 | 2.97 | whole | the powdered car the camera walks onto | 12.17 | 0.0 | 50.4->63.1 | first frame crops the car at both sides (reads 'too cropped') |
| scan_front | 2.97 | 4.0 | front | grille + headlights as the camera pushes in | 1.61 | 0.0 | 22.8->28.5 |  |
| irl_spray | 6.97 | 1.0 | front | scan powder going on | 16.24 | 0.0 | 100.0->100.0 |  |
| irl_scanner | 7.97 | 1.5 | side | live scan on the scanner screen | 40.97 | 0.0 | 81.0->87.1 |  |
| irl_rear_scan | 9.47 | 3.5 | rear | crew scanning the rear corner | 17.74 | 0.0 | 100.0->98.7 |  |
| scan_rear | 12.97 | 6.0 | rear | the rear reflector dropping out and turning | 9.59 | 0.0 | 38.0->47.1 |  |
| scan_xray | 18.97 | 4.5 | whole | reflector returning home, then the full car in x-ray | 8.86 | 0.0 | 53.6->32.2 | first frame crops the car at both sides (reads 'too cropped') |
| website | 23.47 | 4.6 | whole | listing with the 2026 bumper selected, then logo + URL | 2.85 | 1.17 | 18.1->14.9 | dead frames 1.2s (nothing moves) - trim or give the hold a reason; first frame crops the car at both sides (reads 'too cropped') |

## Repeated views
- scan_rear ~ scan_xray (IoU 0.89, corr 0.8): same view shown twice
- scan_xray ~ website (IoU 0.72, corr 0.91): same view shown twice in the same section - merge or cut one
