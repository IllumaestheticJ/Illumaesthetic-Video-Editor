# Director report - projects/mazda-3-gen4/project.yaml

Total 38.2 s. Sections (s): front 4.37, side 4.37, rear 6.57, rear-hatch-top 9.8, wing-part 3.27, top 6.53, end 3.3

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| m1_open | 0.0 | 4.37 | front | whole car, front-left 3/4 | 0.33 | 3.35 | 8.7->9.8 | dead frames 3.4s (nothing moves) - trim or give the hold a reason |
| m2_flank | 4.37 | 4.37 | side | left flank surfacing | 0.14 | 4.26 | 9.9->10.1 | dead frames 4.3s (nothing moves) - trim or give the hold a reason |
| m3_rear | 8.73 | 6.57 | rear | tail lamps + hatch | 1.2 | 0.0 | 9.8->14.2 |  |
| m4_wingoff | 15.3 | 9.8 | rear-hatch-top | rear wing -> exposed mounting points (Wing Removed scan) | 4.97 | 1.0 | 40.3->58.3 | dead frames 1.0s (nothing moves) - trim or give the hold a reason |
| m5_part | 25.1 | 3.27 | wing-part | wing underside / mounting face | 8.59 | 0.0 | 26.5->27.3 |  |
| m6_reassemble | 28.37 | 6.53 | top | wing returning to its mounts, whole car from above | 0.78 | 0.79 | 9.6->13.6 | dead frames 0.8s (nothing moves) - trim or give the hold a reason |
| logo | 34.9 | 3.3 | end | small logo | 0.1 | 2.84 | 0.0->0.8 |  |

## Repeated views
- m1_open ~ m2_flank (IoU 0.73, corr 0.8): same view shown twice
- m1_open ~ m3_rear (IoU 0.8, corr 0.86): same view shown twice
- m2_flank ~ m3_rear (IoU 0.82, corr 0.89): same view shown twice
- m3_rear ~ m6_reassemble (IoU 0.62, corr 0.76): same view shown twice
