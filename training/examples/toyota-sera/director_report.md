# Director report - projects/toyota-sera/project.yaml

Total 39.27 s. Sections (s): whole 4.8, front 12.0, side 3.6, rear 6.0, explode 4.8, reassembly 4.8, cta 3.27

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v3_s1_whole | 0.0 | 4.8 | whole | the whole Sera | 0.38 | 0.0 | 8.9->9.7 |  |
| s3_wheel | 4.8 | 2.4 | front | front-right wheel | 8.02 | 0.0 | 49.1->55.7 |  |
| v3_front | 7.2 | 9.6 | front | front - engine bay, front bumper inner face, structure behind the bumper | 6.19 | 0.0 | 16.9->23.0 |  |
| v3_s4_doors | 16.8 | 3.6 | side | butterfly doors + cabin | 3.43 | 0.0 | 22.9->26.4 |  |
| v3_rear | 20.4 | 6.0 | rear | rear - bumper inner face, structure behind the bumper | 5.97 | 0.0 | 16.9->21.6 |  |
| v3_e1_explode | 26.4 | 4.8 | explode | every scanned panel, whole car in frame | 2.0 | 0.0 | 8.8->11.3 |  |
| v4_g3a_home | 31.2 | 2.4 | reassembly | reassembly | 4.94 | 0.0 | 14.9->11.7 |  |
| v4_g3b_clean | 33.6 | 2.4 | reassembly | the reassembled car | 0.73 | 0.0 | 9.2->10.1 |  |
| cta | 36.0 | 3.27 | cta | mobile listing: 1:1 scan -> listing 360 viewer, SCAN DATA AVAILABLE NOW / ILLUMAESTHETIC.COM | 2.85 | 0.0 | 9.5->11.1 |  |

## Repeated views
- v3_s1_whole ~ v4_g3b_clean (IoU 0.65, corr 0.8): same view shown twice
- v3_s1_whole ~ cta (IoU 0.66, corr 0.82): same view shown twice
- v3_e1_explode ~ v4_g3a_home (IoU 0.67, corr 0.79): same view shown twice
- v3_e1_explode ~ v4_g3b_clean (IoU 0.7, corr 0.8): same view shown twice
- v4_g3a_home ~ v4_g3b_clean (IoU 0.88, corr 0.97): same view shown twice in the same section - merge or cut one
- v4_g3b_clean ~ cta (IoU 0.78, corr 0.9): same view shown twice
