# Director report - projects/toyota-sera-scan-process/project.yaml

Total 27.57 s. Sections (s): front 11.37, side 2.4, rear 6.0, whole car 4.2, end card 3.6

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| irl_open | 0.0 | 1.77 | front | the real car, front 3/4 | 7.28 | 0.0 | 99.3->98.5 | first frame crops the car at both sides (reads 'too cropped') |
| scan_open | 1.77 | 1.8 | front | nose = scan of the same car | 6.94 | 0.0 | 62.4->66.5 |  |
| irl_front_lift | 3.57 | 2.4 | front | crew lifting the front bumper off | 15.95 | 0.0 | 92.2->71.5 |  |
| scan_front_match | 5.97 | 1.2 | front | engine bay as in the footage | 11.32 | 0.0 | 70.3->71.9 |  |
| scan_front_off | 7.17 | 2.4 | front | front bumper inside + outside | 3.59 | 0.0 | 13.9->17.3 |  |
| scan_front_behind | 9.57 | 1.8 | front | structure behind the front bumper | 2.89 | 0.0 | 53.6->54.6 |  |
| scan_doors | 11.37 | 2.4 | side | butterfly doors open | 2.29 | 0.0 | 25.8->24.8 |  |
| irl_rear_pull | 13.77 | 1.8 | rear | crew pulling the rear bumper | 22.09 | 0.0 | 96.2->96.5 |  |
| scan_rear_off | 15.57 | 2.4 | rear | rear bumper inside + outside | 4.13 | 0.0 | 9.8->12.9 |  |
| scan_rear_behind | 17.97 | 1.8 | rear | structure behind the rear bumper | 1.51 | 0.0 | 28.6->30.2 |  |
| scan_xray | 19.77 | 4.2 | whole car | bumpers seat home, listing angle | 2.07 | 0.0 | 13.9->13.7 |  |
| website | 23.97 | 3.6 | end card | listing page + URL | 3.24 | 0.0 | 19.2->13.6 |  |

## Repeated views
- scan_xray ~ website (IoU 0.72, corr 0.89): same view shown twice
