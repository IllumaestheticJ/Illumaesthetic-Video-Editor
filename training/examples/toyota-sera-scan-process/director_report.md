# Director report - projects/toyota-sera-scan-process/project.yaml

Total 29.37 s. Sections (s): front 13.17, side 2.4, rear 7.8, finished car 2.4, end card 3.6

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| irl_open | 0.0 | 1.77 | front | the real car, front 3/4 | 7.28 | 0.0 | 99.3->98.5 | first frame crops the car at both sides (reads 'too cropped') |
| scan_open | 1.77 | 1.8 | front | nose = scan of the same car | 6.94 | 0.0 | 62.4->66.5 |  |
| irl_front_lift | 3.57 | 2.4 | front | crew lifting the front bumper off | 15.95 | 0.0 | 92.2->71.5 |  |
| scan_front_match | 5.97 | 1.2 | front | engine bay as in the footage | 11.32 | 0.0 | 70.3->71.9 |  |
| scan_front_off | 7.17 | 2.4 | front | front bumper inside + outside | 3.59 | 0.0 | 13.9->17.3 |  |
| scan_front_behind | 9.57 | 1.8 | front | structure behind the front bumper | 2.89 | 0.0 | 53.6->54.6 |  |
| scan_front_design | 11.37 | 1.8 | front | designed front bumper on the scan | 3.39 | 0.0 | 13.7->13.9 |  |
| scan_doors | 13.17 | 2.4 | side | butterfly doors open | 2.29 | 0.0 | 25.8->24.8 |  |
| irl_rear_pull | 15.57 | 1.8 | rear | crew pulling the rear bumper | 22.09 | 0.0 | 96.2->96.5 |  |
| scan_rear_off | 17.37 | 2.4 | rear | rear bumper inside + outside | 4.13 | 0.0 | 9.8->12.9 |  |
| scan_rear_behind | 19.77 | 1.8 | rear | structure behind the rear bumper | 1.51 | 0.0 | 28.6->30.2 |  |
| scan_rear_design | 21.57 | 1.8 | rear | designed rear bumper on the scan | 4.23 | 0.0 | 13.7->13.4 |  |
| irl_finished_front | 23.37 | 1.2 | finished car | the real car wearing the kit, front | 4.24 | 0.0 | 86.5->86.7 |  |
| irl_finished_rear | 24.57 | 1.2 | finished car | the real car wearing the kit, rear | 1.23 | 0.0 | 92.9->92.8 |  |
| website | 25.77 | 3.6 | end card | listing page + URL | 3.24 | 0.0 | 19.2->13.6 |  |

## Repeated views
- scan_front_off ~ scan_front_design (IoU 0.74, corr 0.81): same view shown twice in the same section - merge or cut one
