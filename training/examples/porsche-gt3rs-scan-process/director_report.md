# Director report - projects/porsche-gt3rs-scan-process/project.yaml

Total 38.37 s. Sections (s): untagged 38.38

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| irl_headon | 0.0 | 3.77 |  |  | 12.06 | 0.0 | 79.3->90.8 | first frame crops the car at both sides (reads 'too cropped'); no focus: tag - what should the viewer look at? |
| scan_headon | 3.77 | 3.83 |  |  | 0.94 | 0.8 | 18.6->14.7 | dead frames 0.8s (nothing moves) - trim or give the hold a reason; no focus: tag - what should the viewer look at? |
| xray_front | 7.6 | 3.8 |  |  | 3.57 | 0.0 | 13.2->13.8 | no focus: tag - what should the viewer look at? |
| irl_crew_scan | 11.4 | 2.7 |  |  | 21.54 | 0.0 | 94.4->93.0 | no focus: tag - what should the viewer look at? |
| scan_side | 14.1 | 1.0 |  |  | 0.0 | 0.93 | 18.3->18.3 | dead frames 0.9s (nothing moves) - trim or give the hold a reason; no focus: tag - what should the viewer look at? |
| xray_side | 15.1 | 3.67 |  |  | 1.89 | 0.0 | 22.0->19.4 | no focus: tag - what should the viewer look at? |
| irl_scanner | 18.77 | 3.77 |  |  | 16.39 | 0.0 | 91.1->86.1 | no focus: tag - what should the viewer look at? |
| xray_rear | 22.53 | 3.8 |  |  | 2.33 | 0.0 | 15.4->18.7 | no focus: tag - what should the viewer look at? |
| xray_reassembly | 26.33 | 6.07 |  |  | 1.18 | 0.0 | 12.2->11.4 | no focus: tag - what should the viewer look at? |
| website | 32.4 | 5.97 |  |  | 2.67 | 1.5 | 18.2->13.0 | dead frames 1.5s (nothing moves) - trim or give the hold a reason; no focus: tag - what should the viewer look at? |

## Repeated views
- scan_headon ~ xray_front (IoU 0.96, corr 0.93): same view shown twice
- scan_side ~ xray_side (IoU 0.82, corr 0.86): same view shown twice
- xray_reassembly ~ website (IoU 0.6, corr 0.84): same view shown twice
