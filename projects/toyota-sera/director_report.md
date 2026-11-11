# Director report - projects/toyota-sera/project.yaml

Total 39.27 s. Sections (s): whole 4.8, front 12.0, side 3.6, rear 6.0, explode 4.8, reassembly 4.8, logo 3.27

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v3_s1_whole | 0.0 | 4.8 | whole | the whole Sera | 0.38 | 0.0 | 8.9->9.7 |  |
| s3_wheel | 4.8 | 2.4 | front | front-right wheel | 8.02 | 0.0 | 49.1->55.7 |  |
| v3_front | 7.2 | 9.6 | front | front - engine bay, front bumper inner face, structure behind the bumper | 6.19 | 0.0 | 16.9->23.0 |  |
| v3_s4_doors | 16.8 | 3.6 | side | butterfly doors + cabin | 3.43 | 0.0 | 22.9->26.4 |  |
| v3_rear | 20.4 | 6.0 | rear | rear - bumper inner face, structure behind the bumper | 5.97 | 0.0 | 16.9->21.6 |  |
| v3_e1_explode | 26.4 | 4.8 | explode | every scanned panel, whole car in frame | 2.0 | 0.0 | 8.8->11.3 |  |
| v3_g3a_home | 31.2 | 2.4 | reassembly | reassembly | 3.37 | 0.0 | 15.2->14.7 |  |
| v3_g3b_clean | 33.6 | 2.4 | reassembly | the reassembled car | 1.48 | 0.0 | 11.7->10.8 |  |
| logo | 36.0 | 3.27 | logo | logo | 0.24 | 2.34 | 0.2->1.7 |  |

## Repeated views
- v3_s1_whole ~ v3_g3a_home (IoU 0.66, corr 0.83): same view shown twice
- v3_s1_whole ~ v3_g3b_clean (IoU 0.7, corr 0.83): same view shown twice
- v3_g3a_home ~ v3_g3b_clean (IoU 0.93, corr 0.98): same view shown twice in the same section - merge or cut one
