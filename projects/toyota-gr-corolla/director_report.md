# Director report - projects/toyota-gr-corolla/project.yaml

Total 38.67 s. Sections (s): whole 6.9, front 15.42, side 1.73, rear 10.26, untagged 4.33

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| s1_whole | 0.0 | 3.47 | whole | whole car, front-right 3/4 | 0.14 | 3.33 | 9.5->9.8 | dead frames 3.3s (nothing moves) - trim or give the hold a reason |
| s2_wheel | 3.47 | 3.43 | front | front-right wheel and arch | 7.28 | 0.0 | 39.9->38.0 |  |
| s3_hood | 6.9 | 3.43 | front | hood vents | 9.67 | 0.0 | 60.2->58.7 |  |
| s4_nose | 10.33 | 3.43 | front | headlight and grille | 9.21 | 0.0 | 48.7->49.4 |  |
| s5_fbumper | 13.77 | 5.13 | front | front bumper inner face + structure behind it | 2.65 | 0.0 | 14.4->13.6 |  |
| s6_side | 18.9 | 1.73 | side | left flank with front bumper off | 0.24 | 1.6 | 11.1->10.9 |  |
| s7_diffuser | 20.63 | 3.43 | rear | diffuser removed | 4.08 | 0.0 | 9.7->18.6 |  |
| s8_rbumper | 24.07 | 3.4 | rear | rear bumper inner face + crash beam | 11.36 | 0.0 | 10.8->21.5 |  |
| s9_mounts | 27.47 | 3.43 | rear | mounting points (crash bar removed) | 2.5 | 0.0 | 29.8->34.1 |  |
| s10_reassemble | 30.9 | 1.73 | whole | parts returning home | 1.29 | 0.0 | 10.6->10.4 |  |
| s11_clean | 32.63 | 1.7 | whole | clean car lock before fade | 0.2 | 1.6 | 9.3->9.6 |  |
| logo | 34.33 | 4.33 |  |  | 0.23 | 3.33 | 0.2->1.9 |  |

## Repeated views
- s1_whole ~ s6_side (IoU 0.81, corr 0.87): same view shown twice
- s4_nose ~ s9_mounts (IoU 0.73, corr 0.76): same view shown twice
- s8_rbumper ~ s9_mounts (IoU 0.95, corr 0.98): same view shown twice in the same section - merge or cut one
- s10_reassemble ~ s11_clean (IoU 0.93, corr 0.98): same view shown twice in the same section - merge or cut one
