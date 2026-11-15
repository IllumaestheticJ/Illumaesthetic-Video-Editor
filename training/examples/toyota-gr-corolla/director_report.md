# Director report - projects/toyota-gr-corolla/project.yaml

Total 26.3 s. Sections (s): whole 4.63, front 9.32, rear 9.32, untagged 3.0

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a1_whole | 0.0 | 2.3 | whole | whole car push, song opening | 1.73 | 0.0 | 9.5->14.6 |  |
| b1_fbumper | 2.3 | 2.33 | front | front bumper off FIRST, whole (fbumper6) | 8.45 | 0.0 | 16.4->18.1 |  |
| b2_beams | 4.63 | 2.33 | front | upper + lower bumper beams | 12.1 | 0.0 | 21.8->26.9 |  |
| b3_ducts | 6.97 | 2.33 | front | bumper + radiator ducts | 5.88 | 0.0 | 20.1->23.1 |  |
| b4_ic | 9.3 | 2.33 | front | intercooler in front of the radiator | 2.62 | 0.0 | 22.4->25.0 |  |
| h1_hatch | 11.63 | 2.33 | rear | hatch hinges open over the scanned cargo area | 2.82 | 0.0 | 14.3->16.7 |  |
| h2_hatchoff | 13.97 | 2.33 | rear | open hatch lifts off | 5.36 | 0.0 | 20.1->21.4 |  |
| c1_rbumper | 16.3 | 2.33 | rear | rear bumper + diffuser off together | 12.86 | 0.0 | 12.6->20.6 |  |
| c2_crash | 18.63 | 2.33 | rear | crash beam removed | 2.04 | 0.0 | 28.4->30.4 |  |
| d1_clean | 20.97 | 2.33 | whole | clean car | 0.44 | 1.06 | 15.7->16.5 |  |
| logo | 23.3 | 3.0 |  |  | 0.61 | 2.0 | 0.8->3.3 |  |

## Repeated views
- a1_whole ~ d1_clean (IoU 0.77, corr 0.83): same view shown twice in the same section - merge or cut one
- h1_hatch ~ h2_hatchoff (IoU 0.98, corr 1.0): same view shown twice in the same section - merge or cut one
- c1_rbumper ~ c2_crash (IoU 0.93, corr 0.94): same view shown twice in the same section - merge or cut one
