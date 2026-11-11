# Director report - projects/c5-corvette/project.yaml

Total 39.3 s. Sections (s): whole 7.34, front 10.67, side +X 6.47, rear 7.63, side -X 3.3, untagged 3.9

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v3_open | 0.0 | 4.07 | whole | whole clean car, front bumper starts off (front-bumper base cuts in under the bumper only) | 2.05 | 0.0 | 12.1->11.6 |  |
| v3_fb | 4.07 | 5.2 | front | FRONT BUMPER REMOVED: nose structure + the bumper's scanned inside | 4.87 | 0.0 | 10.8->16.3 |  |
| v3_hood | 9.27 | 5.47 | front | hood on its fitted hinge -> scanned underside -> bay (front bumper + hood removed state) | 8.12 | 0.0 | 18.4->29.4 |  |
| v3_sill | 14.73 | 3.2 | side +X | LEFT DOORSILL: closed door -> captured door-open state on 15.856 | 6.42 | 0.0 | 21.7->21.5 |  |
| v3_gas | 17.93 | 3.27 | side +X | GAS CAP: fuel door closed -> captured open state on 19.135, macro on the cap | 6.85 | 0.0 | 25.6->41.7 |  |
| v3_trunk | 21.2 | 3.3 | rear | TRUNK OPEN: hatch glass -> captured trunk tub on 22.404 | 5.35 | 0.0 | 19.0->35.0 |  |
| v3_rear | 24.5 | 4.33 | rear | REAR BUMPER REMOVED: rear structure + the bumper's scanned inside | 3.62 | 0.0 | 7.4->15.9 |  |
| v3_fender | 28.83 | 3.3 | side -X | FENDER REMOVED (hood on = captured state): wheelhouse / mounts | 7.45 | 0.0 | 12.6->20.6 |  |
| v3_home | 32.13 | 3.27 | whole | parts return; clean car on 34.402; fade | 1.32 | 0.0 | 12.0->9.5 |  |
| logo | 35.4 | 3.9 |  |  | 0.0 | 0.0 | 0.0->0.0 |  |

## Repeated views
- v3_open ~ v3_fb (IoU 0.68, corr 0.83): same view shown twice
- v3_open ~ v3_rear (IoU 0.66, corr 0.77): same view shown twice
- v3_open ~ v3_home (IoU 0.71, corr 0.86): same view shown twice in the same section - merge or cut one
- v3_fb ~ v3_rear (IoU 0.76, corr 0.82): same view shown twice
- v3_fb ~ v3_home (IoU 0.73, corr 0.86): same view shown twice
