# Director report - projects/epsilon-wing-configurator/project.yaml

Total 58.9 s. Sections (s): app 11.57, vehicle 5.5, wing 3.9, setup 15.63, views 9.47, price 5.6, more 3.9, ending 3.33

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| hero_a | 0.0 | 4.1 | app | GR86 scan + recommended TC wing (3D orbit) | 0.37 | 0.0 | 99.1->99.1 | first frame crops the car at both sides (reads 'too cropped') |
| hero_b | 4.1 | 4.5 | app | phone layout: Configure sheet, steps 1-4 | 8.06 | 0.0 | 99.1->98.9 |  |
| cars | 8.6 | 5.5 | vehicle | make/model picker swaps the 3D car (3D Scan labels) | 1.21 | 2.32 | 99.7->99.7 | dead frames 2.3s (nothing moves) - trim or give the hold a reason |
| wing | 14.1 | 3.9 | wing | wing element: TC 47.5 / TC 66.5 / GT / custom width (rear view) | 4.1 | 1.67 | 95.7->96.8 | dead frames 1.7s (nothing moves) - trim or give the hold a reason |
| mounts | 18.0 | 6.07 | setup | tested setups + mount: bottom, swan neck, fender (NA Miata) | 2.71 | 3.66 | 95.9->97.5 | dead frames 3.7s (nothing moves) - trim or give the hold a reason |
| bases | 24.07 | 2.03 | setup | base style: 5-axis CNC vs sheet metal | 7.32 | 0.0 | 97.8->97.8 |  |
| aoa | 26.1 | 3.0 | setup | AoA hole 0-15, wing pitch in 3D | 0.2 | 2.16 | 98.5->98.3 | dead frames 2.2s (nothing moves) - trim or give the hold a reason |
| turn3d | 29.1 | 1.47 | views | 3D view: drag to turn, scroll to zoom | 2.79 | 0.0 | 99.1->99.2 |  |
| side | 30.57 | 5.0 | views | side view: drag wing (overhang/height), tilt handle | 0.73 | 3.5 | 98.2->98.2 | dead frames 3.5s (nothing moves) - trim or give the hold a reason |
| rear | 35.57 | 3.0 | views | rear view: drag endplate -> width | 0.28 | 2.16 | 99.2->99.2 | dead frames 2.2s (nothing moves) - trim or give the hold a reason |
| sliders | 38.57 | 4.53 | setup | number controls, locks, inches -> mm | 2.56 | 1.67 | 98.8->99.1 | dead frames 1.7s (nothing moves) - trim or give the hold a reason |
| price | 43.1 | 5.6 | price | live estimate, Save spec, Request a quote (locked, not sent) | 5.5 | 3.33 | 98.3->98.1 | dead frames 3.3s (nothing moves) - trim or give the hold a reason |
| more | 48.7 | 3.9 | more | More options: blueprint / own photos | 7.41 | 0.0 | 98.6->98.5 |  |
| outro | 52.6 | 2.97 | app | finished build, rear 3/4 right, push-in | 0.55 | 0.0 | 99.0->98.9 |  |
| logo | 55.57 | 3.33 | ending | Epsilon+ wordmark (Drive EPSILON+ Logos, 720 px) | 0.0 | 0.0 | 0.0->0.0 |  |

## Repeated views
- hero_a ~ hero_b (IoU 1.0, corr 1.0): same view shown twice in the same section - merge or cut one
- hero_a ~ turn3d (IoU 1.0, corr 0.8): same view shown twice
- hero_b ~ turn3d (IoU 1.0, corr 0.77): same view shown twice
