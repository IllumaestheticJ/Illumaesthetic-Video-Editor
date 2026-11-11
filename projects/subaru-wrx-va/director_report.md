# Director report - projects/subaru-wrx-va/project.yaml

Total 30.77 s. Sections (s): whole car 2.63, engine bay 2.8, front bumper 6.3, hood 1.83, side 1.8, rear 5.46, top 5.46, untagged 4.47

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| s01_front34 | 0.0 | 2.63 | whole car | whole car, front 3/4 | 1.79 | 0.0 | 15.1->16.2 |  |
| s06_hood | 2.63 | 2.8 | engine bay | engine bay under the propped hood | 1.74 | 0.0 | 18.6->18.0 |  |
| n1_bumper | 5.43 | 6.3 | front bumper | front bumper, then the front end behind it (fbumpremoved) | 6.27 | 0.0 | 10.2->13.2 |  |
| n2_scoop | 11.73 | 1.83 | hood | hood scoop and the scoop opening | 7.37 | 0.0 | 24.8->27.7 |  |
| n_side | 13.57 | 1.8 | side | whole car, left side profile -> rear 3/4 | 1.65 | 0.0 | 9.3->10.6 |  |
| n3_wing | 15.37 | 3.63 | rear | STI wing uprights and blade | 2.54 | 0.0 | 13.1->17.7 |  |
| s07_trunk | 19.0 | 1.83 | rear | open trunk lid and cavity | 0.97 | 0.0 | 12.1->13.1 |  |
| n4a_reassemble | 20.83 | 3.63 | top | whole car reassembling | 2.37 | 0.0 | 20.3->22.2 |  |
| n4b_clean | 24.47 | 1.83 | top | whole car, assembled | 0.47 | 0.0 | 22.7->23.6 |  |
| logo | 26.3 | 4.47 |  |  | 0.08 | 4.16 | 0.0->0.8 |  |

## Repeated views
- s01_front34 ~ s07_trunk (IoU 0.68, corr 0.75): same view shown twice
- n1_bumper ~ n_side (IoU 0.7, corr 0.78): same view shown twice
- n2_scoop ~ n3_wing (IoU 0.75, corr 0.81): same view shown twice
- n4a_reassemble ~ n4b_clean (IoU 0.98, corr 0.99): same view shown twice in the same section - merge or cut one
