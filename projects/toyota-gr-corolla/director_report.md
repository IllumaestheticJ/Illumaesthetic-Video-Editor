# Director report - projects/toyota-gr-corolla/project.yaml

Total 23.97 s. Sections (s): whole 4.67, front 11.65, rear 4.63, untagged 3.0

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a1_whole | 0.0 | 2.3 | whole | whole car, front-left 3/4 push | 1.73 | 0.0 | 9.5->14.6 |  |
| a2_grille | 2.3 | 2.33 | front | lower grille, intercooler behind the mesh | 5.87 | 0.0 | 25.2->27.9 |  |
| b1_fbumper | 4.63 | 2.33 | front | front bumper off - first, before anything behind it | 8.99 | 0.0 | 16.4->18.2 |  |
| b2_beams | 6.97 | 2.33 | front | upper + lower bumper beams | 12.18 | 0.0 | 22.2->27.5 |  |
| b3_ducts | 9.3 | 2.33 | front | bumper + radiator ducts | 6.0 | 0.0 | 20.3->23.3 |  |
| b4_ic | 11.63 | 2.33 | front | intercooler; engine-bay scan behind | 2.86 | 0.0 | 23.1->25.4 |  |
| c1_rbumper | 13.97 | 2.33 | rear | rear bumper + diffuser off together | 13.29 | 0.0 | 12.7->20.5 |  |
| c2_crash | 16.3 | 2.3 | rear | crash beam removed, mounting points | 2.03 | 0.0 | 28.2->30.2 |  |
| d1_clean | 18.6 | 2.37 | whole | clean car, rear-right 3/4 | 0.44 | 1.07 | 15.7->16.5 |  |
| logo | 20.97 | 3.0 |  |  | 0.61 | 2.0 | 0.8->3.3 |  |

## Repeated views
- a1_whole ~ c1_rbumper (IoU 0.69, corr 0.79): same view shown twice
- a1_whole ~ d1_clean (IoU 0.77, corr 0.83): same view shown twice in the same section - merge or cut one
- a2_grille ~ b4_ic (IoU 0.71, corr 0.75): same view shown twice in the same section - merge or cut one
- b1_fbumper ~ c1_rbumper (IoU 0.69, corr 0.79): same view shown twice
- c1_rbumper ~ c2_crash (IoU 0.92, corr 0.94): same view shown twice in the same section - merge or cut one
