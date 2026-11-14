# Director report - projects/toyota-sera/project.yaml

Total 39.27 s. Sections (s): whole 4.8, front 12.0, side 3.6, rear 6.0, explode 4.8, reassembly 4.8, cta 3.27

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v3_s1_whole | 0.0 | 4.8 | whole | the whole Sera | 0.38 | 0.0 | 8.9->9.7 |  |
| v3_front | 4.8 | 9.6 | front | front - engine bay, front bumper inner face, structure behind the bumper | 6.31 | 0.0 | 16.9->22.6 |  |
| v5_lights | 14.4 | 2.4 | front | fog light / corner marker units (the 'light' scan), front bumper openings | 0.65 | 0.0 | 4.0->4.7 | subject small on first frame (4% of frame) |
| v3_s4_doors | 16.8 | 3.6 | side | butterfly doors + cabin | 3.43 | 0.0 | 22.9->26.4 |  |
| v5_wing | 20.4 | 2.4 | rear | rear wing / deck under it ('Spoiler removed') | 4.87 | 0.0 | 10.8->18.5 |  |
| v5_rear | 22.8 | 3.6 | rear | rear - bumper inner face, structure behind the bumper | 9.63 | 0.0 | 16.9->22.2 |  |
| v5_explode | 26.4 | 4.8 | explode | every scanned panel, whole car in frame | 2.03 | 0.0 | 8.7->11.3 |  |
| v5_g3a_home | 31.2 | 2.4 | reassembly | reassembly | 4.66 | 0.0 | 13.4->11.0 |  |
| v5_g3b_clean | 33.6 | 2.4 | reassembly | the reassembled car | 0.74 | 0.0 | 9.0->10.0 |  |
| cta | 36.0 | 3.27 | cta | mobile listing: 1:1 scan -> listing 360 viewer, SCAN DATA AVAILABLE NOW / ILLUMAESTHETIC.COM | 2.85 | 0.0 | 9.5->11.1 |  |

## Repeated views
- v3_s1_whole ~ v5_g3b_clean (IoU 0.65, corr 0.8): same view shown twice
- v3_s1_whole ~ cta (IoU 0.66, corr 0.82): same view shown twice
- v5_wing ~ v5_rear (IoU 0.65, corr 0.78): same view shown twice in the same section - merge or cut one
- v5_wing ~ v5_g3a_home (IoU 0.68, corr 0.83): same view shown twice
- v5_wing ~ v5_g3b_clean (IoU 0.63, corr 0.79): same view shown twice
- v5_explode ~ v5_g3a_home (IoU 0.66, corr 0.79): same view shown twice
- v5_explode ~ v5_g3b_clean (IoU 0.69, corr 0.8): same view shown twice
- v5_g3a_home ~ v5_g3b_clean (IoU 0.89, corr 0.97): same view shown twice in the same section - merge or cut one
- v5_g3b_clean ~ cta (IoU 0.78, corr 0.9): same view shown twice
