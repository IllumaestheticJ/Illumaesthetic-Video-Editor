# Director report - projects/c5-corvette/project.yaml

Total 39.37 s. Sections (s): whole 9.27, front 12.83, side 5.2, rear 8.17, untagged 3.9

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v2_a2_open | 0.0 | 4.07 | whole | whole car, then the front bumper starting off | 1.5 | 0.0 | 6.9->8.7 |  |
| v2_b_fb_inside | 4.07 | 5.2 | front | front bumper removed: nose structure + the bumper's scanned inside | 4.8 | 0.0 | 10.9->16.5 |  |
| v2_f2_hood | 9.27 | 7.63 | front | hood on its fitted hinge -> scanned underside -> engine bay (hood removed) | 6.46 | 0.0 | 18.6->30.9 |  |
| v2_c2_fender | 16.9 | 5.2 | side | -X fender removed: wheelhouse and mounts | 5.93 | 0.0 | 12.3->20.5 |  |
| v2_g2_rear | 22.1 | 8.17 | rear | rear bumper removed: rear structure + the bumper's scanned inside | 2.36 | 0.0 | 8.9->15.3 |  |
| v2_i2_home | 30.27 | 5.2 | whole | parts return, clean car on 34.402; 1.1 s settle into the fade (hold = the ending, no new content) | 0.5 | 2.12 | 9.2->8.5 | dead frames 2.1s (nothing moves) - trim or give the hold a reason |
| logo | 35.47 | 3.9 |  |  | 0.0 | 0.0 | 0.0->0.0 |  |

## Repeated views
- v2_a2_open ~ v2_b_fb_inside (IoU 0.69, corr 0.86): same view shown twice
- v2_a2_open ~ v2_g2_rear (IoU 0.71, corr 0.75): same view shown twice
- v2_b_fb_inside ~ v2_i2_home (IoU 0.64, corr 0.75): same view shown twice
- v2_f2_hood ~ v2_g2_rear (IoU 0.63, corr 0.77): same view shown twice
