# Director report - projects/toyota-gr86/project.yaml

Total 39.23 s. Sections (s): whole 7.33, front 12.27, side 2.43, rear 14.7, end 2.5

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| a_open | 0.0 | 2.43 | whole | whole car, front-right 3/4 arc + push from frame 1 (v2 render played 2x: 15 fps frames at 30) | 1.43 | 0.0 | 12.2->12.0 |  |
| b_headlight | 2.43 | 2.47 | front | right headlight + slat grille + intake detail | 1.72 | 0.0 | 46.2->47.9 |  |
| c1_hood_hinge | 4.9 | 2.43 | front | hood hinges open -50 deg about its rear corners (user: hinge open THEN off) | 7.69 | 0.0 | 34.2->41.1 |  |
| c2_hood_off | 7.33 | 2.47 | front | hood lifts off the open pose, push into the engine bay (Hood Open scan) | 21.7 | 0.0 | 42.0->53.0 |  |
| c3_front_bumper_off | 9.8 | 2.43 | front | front_bumper_v4 (car skin + scan inner) pulls out, tips, drops into black - no leftovers | 13.19 | 0.0 | 26.3->31.7 |  |
| c4_front_structure | 12.23 | 2.47 | front | push-in on the structure behind the bumper (Bumper Hood Removed scan) | 7.75 | 0.0 | 25.6->37.1 |  |
| d_mirror4 | 14.7 | 2.43 | side | right mirror flies off -> scanned mirror mount (Side Mirrors Removed) | 10.98 | 0.0 | 44.9->61.8 |  |
| e1_lid_hinge | 17.13 | 2.47 | rear | lid_v4 (cut on its shut lines) hinges open +65 deg | 1.45 | 0.0 | 23.3->25.3 |  |
| e2_lid_off_cargo | 19.6 | 2.43 | rear | lid lifts off -> cargo opening (Trunk Open scan) | 7.83 | 0.0 | 33.7->33.5 |  |
| e3_rear_bumper_off | 22.03 | 2.47 | rear | rear_bumper_v4 pulls back, tips, drops into black | 11.45 | 0.0 | 19.7->36.2 |  |
| e4_rear_beam | 24.5 | 2.43 | rear | push-in on the rear crash beam (Rear Bumper Removed scan) | 14.33 | 0.0 | 48.2->49.5 |  |
| f1_reverse_light | 26.93 | 2.47 | rear | reverse light lifts off the parked bumper into the black band | 10.47 | 0.0 | 41.4->46.9 |  |
| f2_plate_light | 29.4 | 2.43 | rear | licence plate lamp lifts out, turns upright, lands below the beam | 13.59 | 0.0 | 64.6->64.4 |  |
| h1_reassemble | 31.83 | 2.47 | whole | every part flies home rear -> front; hood swings shut on the 34.32 cut | 9.24 | 0.0 | 29.8->26.3 |  |
| h2_hero | 34.3 | 2.43 | whole | clean complete car (car4) from high on the right, fade | 0.22 | 2.27 | 18.0->17.6 | dead frames 2.3s (nothing moves) - trim or give the hold a reason |
| logo | 36.73 | 2.5 | end | ILLUMAESTHETIC logo (860 px, v3 size) | 1.05 | 0.84 | 1.5->4.5 |  |

## Repeated views
- b_headlight ~ d_mirror4 (IoU 0.76, corr 0.76): same view shown twice
- c1_hood_hinge ~ c2_hood_off (IoU 0.83, corr 0.79): same view shown twice in the same section - merge or cut one
- c3_front_bumper_off ~ c4_front_structure (IoU 0.78, corr 0.78): same view shown twice in the same section - merge or cut one
