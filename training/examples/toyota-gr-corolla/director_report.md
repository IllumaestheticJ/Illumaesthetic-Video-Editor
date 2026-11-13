# Director report - projects/toyota-gr-corolla/project.yaml

Total 23.97 s. Sections (s): whole 3.97, front 12.0, rear 5.0, untagged 3.0

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a1_whole | 0.0 | 1.97 | whole | whole car, front-right 3/4 push | 1.83 | 0.0 | 9.5->14.4 |  |
| a3_wheel | 1.97 | 2.0 | front | front-right wheel + arch | 9.62 | 0.0 | 39.9->38.5 |  |
| a2_grille | 3.97 | 2.0 | front | lower grille, intercooler behind the mesh | 6.35 | 0.0 | 25.2->27.7 |  |
| b1_fbumper | 5.97 | 2.0 | front | front bumper off, inner face | 11.32 | 0.0 | 16.1->18.2 |  |
| b2_beams | 7.97 | 2.0 | front | upper + lower bumper beams | 11.84 | 0.0 | 19.9->24.4 |  |
| b3_ducts | 9.97 | 2.0 | front | bumper + radiator ducts | 6.08 | 0.0 | 16.8->18.8 |  |
| b4_ic | 11.97 | 2.0 | front | intercooler | 2.65 | 0.0 | 17.3->19.2 |  |
| c1_diffuser | 13.97 | 2.0 | rear | diffuser removed | 4.29 | 0.0 | 9.7->12.6 |  |
| c2_rbumper | 15.97 | 2.0 | rear | rear bumper off -> crash beam | 13.62 | 0.0 | 12.4->20.2 |  |
| c3_mounts | 17.97 | 1.0 | rear | crash beam removed, mounting points | 2.86 | 0.0 | 28.2->29.4 |  |
| d1_clean | 18.97 | 2.0 | whole | clean car, rear-left 3/4 | 0.47 | 0.8 | 15.7->16.4 |  |
| logo | 20.97 | 3.0 |  |  | 0.61 | 2.0 | 0.8->3.3 |  |

## Repeated views
- a1_whole ~ c1_diffuser (IoU 0.62, corr 0.79): same view shown twice
- a1_whole ~ c2_rbumper (IoU 0.68, corr 0.78): same view shown twice
- a1_whole ~ d1_clean (IoU 0.77, corr 0.82): same view shown twice in the same section - merge or cut one
- a2_grille ~ b4_ic (IoU 0.62, corr 0.78): same view shown twice in the same section - merge or cut one
- c2_rbumper ~ c3_mounts (IoU 0.92, corr 0.93): same view shown twice in the same section - merge or cut one
