# Director report - projects/lexus-is300/project.yaml

Total 37.37 s. Sections (s): whole 11.76, wheel 1.3, front 9.13, side 3.9, rear 5.23, logo 6.03

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| s1_wide | 0.0 | 5.23 | whole | whole car, front-right 3/4 orbit | 0.35 | 1.89 | 5.9->6.7 | dead frames 1.9s (nothing moves) - trim or give the hold a reason; subject small on first frame (6% of frame) |
| s3_wheel | 5.23 | 1.3 | wheel | front-right wheel | 17.6 | 0.0 | 48.0->50.4 |  |
| s4_nose | 6.53 | 2.6 | front | headlight and grille | 6.04 | 0.0 | 43.8->47.6 |  |
| s5_front | 9.13 | 6.53 | front | intercooler behind the removed front bumper | 2.99 | 0.0 | 13.0->19.2 |  |
| s6_side | 15.67 | 3.9 | side | bare sill with the side skirt off | 2.05 | 0.0 | 28.9->31.5 |  |
| s7_rear | 19.57 | 5.23 | rear | rear bumper inner face and open trunk | 1.61 | 0.0 | 12.8->16.6 |  |
| s8_finale | 24.8 | 6.53 | whole | explode, reassembly, then held whole car before the fade | 3.45 | 0.93 | 21.7->15.7 | dead frames 0.9s (nothing moves) - trim or give the hold a reason |
| logo | 31.33 | 6.03 | logo | ILLUMAESTHETIC logo | 0.08 | 5.16 | 0.1->1.0 |  |

## Repeated views
- s1_wide ~ s8_finale (IoU 0.65, corr 0.82): same view shown twice in the same section - merge or cut one
- s5_front ~ s7_rear (IoU 0.67, corr 0.79): same view shown twice
