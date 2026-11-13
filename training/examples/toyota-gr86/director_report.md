# Director report - projects/toyota-gr86/project.yaml

Total 39.83 s. Sections (s): whole 11.77, front 11.81, side 1.97, rear 11.8, end 2.5

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a_open | 0.0 | 1.93 | whole | whole car, front-right 3/4 arc + push (v2 render at 2x) - build bar 0 | 1.46 | 0.0 | 12.2->12.2 |  |
| b_headlight | 1.93 | 1.93 | front | headlight + slat grille + intake - build bar 1 | 1.53 | 0.0 | 46.2->47.4 |  |
| c1_hood_hinge | 3.87 | 2.0 | front | DROP: hood hinges open -50 deg (label HOOD) | 8.73 | 0.0 | 34.2->40.5 |  |
| c2_hood_off | 5.87 | 1.97 | front | hood lifts off -> engine bay (Hood Open) | 21.14 | 0.0 | 42.0->49.4 |  |
| m1_side_marker | 7.83 | 1.97 | front | side markers (part scan) pop out of the bumper corners - hats enter | 8.55 | 0.0 | 37.1->42.6 |  |
| c3b_front_bumper_off | 9.8 | 1.97 | front | front bumper (part scan, markers out) pulls, tips, drops | 15.41 | 0.0 | 26.3->32.8 |  |
| c4_front_structure | 11.77 | 1.97 | front | front structure push-in (Bumper Hood Removed) | 8.79 | 0.0 | 25.6->34.9 |  |
| d_mirror4 | 13.73 | 1.97 | side | right mirror off -> mirror mount (Side Mirrors Removed) | 11.64 | 0.0 | 44.9->57.6 |  |
| e1_lid_hinge | 15.7 | 1.93 | rear | trunk lid (shut-line cut) hinges open +65 deg | 1.64 | 0.0 | 23.3->25.1 |  |
| e2_lid_off_cargo | 17.63 | 1.97 | rear | lid lifts off -> cargo (Trunk Open) | 8.79 | 0.0 | 33.7->34.0 |  |
| e3_rear_bumper_off | 19.6 | 2.0 | rear | rear bumper (part scan) pulls, tips, drops | 12.49 | 0.0 | 19.7->33.2 |  |
| e4_rear_beam | 21.6 | 2.0 | rear | rear crash beam push-in (Rear Bumper Removed) - loudest bar | 16.03 | 0.0 | 48.2->49.5 |  |
| f1_reverse_light | 23.6 | 1.93 | rear | reverse light (part scan) lifts into the black band | 10.88 | 0.0 | 41.4->45.7 |  |
| f2_plate_light | 25.53 | 1.97 | rear | licence plate light (part scan) lifts, turns upright, lands | 14.59 | 0.0 | 64.6->63.7 |  |
| x1_explode_fr | 27.5 | 1.93 | whole | every part flies out to the exploded view - front-right | 3.72 | 0.0 | 13.8->17.1 |  |
| x2_explode_rr | 29.43 | 1.97 | whole | exploded view, rear-right (rear bumper + lights) | 1.11 | 0.0 | 18.0->18.8 |  |
| x3_explode_high | 31.4 | 1.97 | whole | exploded view, high (every part) | 2.25 | 0.0 | 25.5->27.2 |  |
| h1_reassemble_v5 | 33.37 | 2.0 | whole | every part flies home, hood lands on the cut | 4.17 | 0.0 | 10.7->14.2 |  |
| h2_hero | 35.37 | 1.97 | whole | clean complete car (car4), fade | 0.23 | 1.86 | 18.0->17.7 | dead frames 1.9s (nothing moves) - trim or give the hold a reason |
| logo | 37.33 | 2.5 | end | ILLUMAESTHETIC logo (860 px) over the section's decay | 1.05 | 0.84 | 1.5->4.5 |  |

## Repeated views
- b_headlight ~ m1_side_marker (IoU 0.9, corr 0.87): same view shown twice in the same section - merge or cut one
- c1_hood_hinge ~ c2_hood_off (IoU 0.83, corr 0.79): same view shown twice in the same section - merge or cut one
- m1_side_marker ~ c3b_front_bumper_off (IoU 0.84, corr 0.82): same view shown twice in the same section - merge or cut one
- c3b_front_bumper_off ~ c4_front_structure (IoU 0.78, corr 0.78): same view shown twice in the same section - merge or cut one
- h1_reassemble_v5 ~ h2_hero (IoU 0.93, corr 0.95): same view shown twice in the same section - merge or cut one
