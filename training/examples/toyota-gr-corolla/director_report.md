# Director report - projects/toyota-gr-corolla/project.yaml

Total 28.63 s. Sections (s): whole 4.63, front 11.65, rear 9.32, untagged 3.0

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a1_whole | 0.0 | 2.3 | whole | whole car push, song opening | 1.86 | 0.0 | 10.0->15.5 |  |
| b1_fbumper | 2.3 | 2.33 | front | front bumper off FIRST, whole (fbumper6) | 9.27 | 0.0 | 16.4->18.5 |  |
| b2_beams | 4.63 | 2.33 | front | upper + lower bumper beams | 12.1 | 0.0 | 21.8->26.9 |  |
| b3_ducts | 6.97 | 2.33 | front | bumper + radiator ducts | 5.88 | 0.0 | 20.1->23.1 |  |
| b4_ic | 9.3 | 2.33 | front | intercooler in front of the radiator | 2.62 | 0.0 | 22.4->25.0 |  |
| k1_hood | 11.63 | 2.33 | front | hood hinges open over the engine bay, then lifts off | 5.13 | 0.0 | 17.9->20.3 |  |
| h1_hatch | 13.97 | 2.33 | rear | hatch hinges open over the scanned cargo area | 2.89 | 0.0 | 14.4->16.9 |  |
| h2_hatchoff | 16.3 | 2.33 | rear | open hatch lifts off | 5.68 | 0.0 | 20.5->22.0 |  |
| c1_rbumper | 18.63 | 2.33 | rear | rear bumper + diffuser off together | 12.86 | 0.0 | 12.6->20.6 |  |
| c2_crash | 20.97 | 2.33 | rear | crash beam removed | 2.03 | 0.0 | 28.4->30.3 |  |
| d1_clean | 23.3 | 2.33 | whole | clean car | 0.44 | 1.07 | 15.7->16.6 |  |
| logo | 25.63 | 3.0 |  |  | 0.61 | 2.0 | 0.8->3.3 |  |

## Repeated views
- a1_whole ~ d1_clean (IoU 0.8, corr 0.83): same view shown twice in the same section - merge or cut one
- b1_fbumper ~ k1_hood (IoU 0.71, corr 0.78): same view shown twice in the same section - merge or cut one
- k1_hood ~ c1_rbumper (IoU 0.76, corr 0.78): same view shown twice
- h1_hatch ~ h2_hatchoff (IoU 0.98, corr 1.0): same view shown twice in the same section - merge or cut one
- c1_rbumper ~ c2_crash (IoU 0.93, corr 0.94): same view shown twice in the same section - merge or cut one
