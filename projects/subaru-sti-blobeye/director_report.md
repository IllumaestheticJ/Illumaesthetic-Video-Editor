# Director report - projects/subaru-sti-blobeye/project.yaml

Total 39.23 s. Sections (s): whole 8.0, rear 4.8, wheel 1.6, front 12.8, engine 7.6, untagged 4.43

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| O1_open | 0.0 | 3.2 | whole | whole car, wing | 1.92 | 0.0 | 13.0->17.4 |  |
| R_wing | 3.2 | 3.2 | rear | wing | 5.14 | 0.0 | 27.3->48.7 |  |
| wing | 6.4 | 1.6 | rear | wing end plate + tail light | 2.26 | 0.0 | 67.2->66.6 |  |
| wheel | 8.0 | 1.6 | wheel | front-right wheel + caliper | 17.07 | 0.0 | 54.1->58.3 |  |
| light | 9.6 | 1.6 | front | headlight -> hood scoop | 19.83 | 0.0 | 49.3->63.9 |  |
| H_a | 11.2 | 2.0 | engine | hood + scoop | 15.26 | 0.0 | 40.1->62.3 |  |
| E_bay | 13.2 | 5.6 | engine | engine bay | 11.42 | 0.0 | 74.7->88.3 |  |
| B_a | 18.8 | 1.6 | front | front bumper | 7.51 | 0.0 | 20.0->25.9 |  |
| B_b | 20.4 | 4.8 | front | intercooler core | 2.69 | 0.0 | 31.9->41.5 |  |
| B_c | 25.2 | 4.8 | front | intercooler piping | 7.78 | 0.0 | 41.0->41.1 |  |
| close | 30.0 | 4.8 | whole | whole car, front | 1.2 | 0.0 | 11.3->15.6 |  |
| logo | 34.8 | 4.43 |  |  | 0.05 | 4.33 | 0.0->0.5 |  |

## Repeated views
- O1_open ~ close (IoU 0.76, corr 0.83): same view shown twice in the same section - merge or cut one
- R_wing ~ light (IoU 0.82, corr 0.86): same view shown twice
- R_wing ~ H_a (IoU 0.87, corr 0.84): same view shown twice
- wing ~ light (IoU 0.87, corr 0.77): same view shown twice
- light ~ H_a (IoU 0.75, corr 0.82): same view shown twice
- B_b ~ B_c (IoU 0.91, corr 0.78): same view shown twice in the same section - merge or cut one
