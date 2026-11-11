# Director report - projects/mazda-miata-nc/project.yaml

Total 37.97 s. Sections (s): whole 8.76, wheel 1.77, front 9.29, engine 9.34, rear 4.63, logo 4.17

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| v3_open | 0.0 | 2.93 | whole | whole car, front-left 3/4, push-in from frame 1 | 0.37 | 1.47 | 10.4->11.9 | dead frames 1.5s (nothing moves) - trim or give the hold a reason |
| v3_wheel | 2.93 | 1.77 | wheel | front wheel under the fender scoop, straight then steered out | 7.57 | 0.0 | 41.5->44.2 |  |
| v3_lamp | 4.7 | 1.73 | front | headlight close-up, bumper still on | 4.84 | 0.0 | 41.5->45.7 |  |
| v3_b1 | 6.43 | 2.33 | front | front bumper leaving the car | 1.65 | 0.0 | 11.6->13.0 |  |
| v3_b2 | 8.77 | 5.23 | front | what the bumper covered: beam, intake, lamp housing | 8.16 | 0.0 | 60.5->46.1 |  |
| v3_b3a | 14.0 | 4.67 | engine | hood opening on its hinge | 3.68 | 0.0 | 34.6->38.2 |  |
| v3_b3b | 18.67 | 4.67 | engine | engine bay after the hood lifts off | 8.68 | 0.0 | 51.8->57.4 |  |
| v3_rear | 23.33 | 4.63 | rear | trunk lid opening on its hinge | 1.37 | 0.0 | 19.4->23.3 |  |
| v3_end | 27.97 | 3.5 | whole | top view, bumper/hood/lid off then flying home | 1.69 | 0.0 | 32.2->29.5 |  |
| v3_endclean | 31.47 | 2.33 | whole | clean assembled car fading out | 3.47 | 0.0 | 25.4->24.6 |  |
| logo | 33.8 | 4.17 | logo | small logo | 0.17 | 3.17 | 0.1->1.6 |  |

## Repeated views
- v3_lamp ~ v3_b2 (IoU 0.82, corr 0.88): same view shown twice in the same section - merge or cut one
- v3_lamp ~ v3_b3a (IoU 0.7, corr 0.82): same view shown twice
- v3_b2 ~ v3_b3a (IoU 0.76, corr 0.77): same view shown twice
- v3_end ~ v3_endclean (IoU 0.99, corr 1.0): same view shown twice in the same section - merge or cut one
