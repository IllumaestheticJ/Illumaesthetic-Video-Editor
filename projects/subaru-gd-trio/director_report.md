# Director report - projects/subaru-gd-trio/project.yaml

Total 18.9 s. Sections (s): front 8.54, rear 5.14, top 3.44, untagged 1.8

| clip | start | dur | section | focus | motion | dead s | cover % | flags |
|---|---|---|---|---|---|---|---|---|
| F1_bug | 0.0 | 1.67 | front | face, whole car | 0.98 | 0.0 | 13.9->14.6 |  |
| F1_blob | 1.67 | 1.73 | front | face, whole car | 1.17 | 0.0 | 15.6->16.5 |  |
| F1_hawk | 3.4 | 1.7 | front | face, whole car | 0.98 | 0.0 | 17.9->18.6 |  |
| F2_bug | 5.1 | 0.87 | front | lamps, grille, scoop | 3.35 | 0.0 | 27.2->28.3 |  |
| F2_blob | 5.97 | 0.87 | front | lamps, grille, scoop | 3.64 | 0.0 | 29.9->31.3 |  |
| F2_hawk | 6.83 | 1.7 | front | lamps, grille, scoop | 2.84 | 0.0 | 34.0->36.8 |  |
| R1_bug | 8.53 | 0.87 | rear | wing / tail, whole car | 1.35 | 0.0 | 14.6->14.9 |  |
| R1_blob | 9.4 | 0.87 | rear | wing / tail, whole car | 1.61 | 0.0 | 15.8->16.1 |  |
| R1_hawk | 10.27 | 0.83 | rear | wing / tail, whole car | 1.69 | 0.0 | 16.1->16.2 |  |
| R2_bug | 11.1 | 0.87 | rear | tail lamps, wing, roof vane | 2.89 | 0.0 | 25.5->26.6 |  |
| R2_blob | 11.97 | 0.87 | rear | tail lamps, wing, roof vane | 3.78 | 0.0 | 28.8->30.1 |  |
| R2_hawk | 12.83 | 0.83 | rear | tail lamps, wing, roof vane | 3.88 | 0.0 | 31.4->32.6 |  |
| T1_bug | 13.67 | 0.87 | top | scoop, wing, vane from above | 1.14 | 0.0 | 35.8->36.4 |  |
| T1_blob | 14.53 | 0.87 | top | scoop, wing, vane from above | 1.14 | 0.0 | 37.1->37.8 |  |
| T1_hawk | 15.4 | 1.7 | top | scoop, wing, vane from above | 0.88 | 0.0 | 38.6->40.2 |  |
| logo | 17.1 | 1.8 |  |  | 0.69 | 1.16 | 3.5->3.2 |  |

## Repeated views
- F1_bug ~ F1_blob (IoU 0.9, corr 0.96): same view shown twice in the same section - merge or cut one
- F1_bug ~ F1_hawk (IoU 0.81, corr 0.9): same view shown twice in the same section - merge or cut one
- F1_bug ~ R1_bug (IoU 0.75, corr 0.79): same view shown twice
- F1_bug ~ R1_blob (IoU 0.73, corr 0.78): same view shown twice
- F1_bug ~ R1_hawk (IoU 0.72, corr 0.77): same view shown twice
- F1_blob ~ F1_hawk (IoU 0.93, corr 0.97): same view shown twice in the same section - merge or cut one
- F1_blob ~ F2_bug (IoU 0.61, corr 0.78): same view shown twice in the same section - merge or cut one
- F1_blob ~ R1_bug (IoU 0.71, corr 0.77): same view shown twice
- F1_blob ~ R1_blob (IoU 0.72, corr 0.77): same view shown twice
- F1_blob ~ R1_hawk (IoU 0.71, corr 0.77): same view shown twice
- F1_hawk ~ F2_bug (IoU 0.69, corr 0.8): same view shown twice in the same section - merge or cut one
- F1_hawk ~ F2_blob (IoU 0.6, corr 0.76): same view shown twice in the same section - merge or cut one
- F1_hawk ~ R1_bug (IoU 0.66, corr 0.75): same view shown twice
- F1_hawk ~ R1_hawk (IoU 0.69, corr 0.76): same view shown twice
- F2_bug ~ F2_blob (IoU 0.9, corr 0.96): same view shown twice in the same section - merge or cut one
- F2_bug ~ F2_hawk (IoU 0.8, corr 0.87): same view shown twice in the same section - merge or cut one
- F2_bug ~ R2_bug (IoU 0.72, corr 0.78): same view shown twice
- F2_bug ~ R2_blob (IoU 0.76, corr 0.79): same view shown twice
- F2_bug ~ R2_hawk (IoU 0.77, corr 0.79): same view shown twice
- F2_blob ~ F2_hawk (IoU 0.93, corr 0.96): same view shown twice in the same section - merge or cut one
- F2_blob ~ R2_bug (IoU 0.68, corr 0.77): same view shown twice
- F2_blob ~ R2_blob (IoU 0.75, corr 0.79): same view shown twice
- F2_blob ~ R2_hawk (IoU 0.78, corr 0.82): same view shown twice
- F2_hawk ~ R2_blob (IoU 0.72, corr 0.77): same view shown twice
- F2_hawk ~ R2_hawk (IoU 0.78, corr 0.8): same view shown twice
- R1_bug ~ R1_blob (IoU 0.92, corr 0.96): same view shown twice in the same section - merge or cut one
- R1_bug ~ R1_hawk (IoU 0.85, corr 0.93): same view shown twice in the same section - merge or cut one
- R1_blob ~ R1_hawk (IoU 0.98, corr 1.0): same view shown twice in the same section - merge or cut one
- R2_bug ~ R2_blob (IoU 0.95, corr 0.97): same view shown twice in the same section - merge or cut one
- R2_bug ~ R2_hawk (IoU 0.86, corr 0.91): same view shown twice in the same section - merge or cut one
- R2_blob ~ R2_hawk (IoU 0.99, corr 1.0): same view shown twice in the same section - merge or cut one
- T1_bug ~ T1_blob (IoU 0.99, corr 0.99): same view shown twice in the same section - merge or cut one
- T1_bug ~ T1_hawk (IoU 0.96, corr 0.98): same view shown twice in the same section - merge or cut one
- T1_blob ~ T1_hawk (IoU 0.99, corr 1.0): same view shown twice in the same section - merge or cut one
- F1_bug ~ F1_blob: same focus 'face, whole car' twice - merge into one held shot
- F1_bug ~ F1_hawk: same focus 'face, whole car' twice - merge into one held shot
- F2_bug ~ F2_blob: same focus 'lamps, grille, scoop' twice - merge into one held shot
- F2_bug ~ F2_hawk: same focus 'lamps, grille, scoop' twice - merge into one held shot
- R1_bug ~ R1_blob: same focus 'wing / tail, whole car' twice - merge into one held shot
- R1_bug ~ R1_hawk: same focus 'wing / tail, whole car' twice - merge into one held shot
- R2_bug ~ R2_blob: same focus 'tail lamps, wing, roof vane' twice - merge into one held shot
- R2_bug ~ R2_hawk: same focus 'tail lamps, wing, roof vane' twice - merge into one held shot
- T1_bug ~ T1_blob: same focus 'scoop, wing, vane from above' twice - merge into one held shot
- T1_bug ~ T1_hawk: same focus 'scoop, wing, vane from above' twice - merge into one held shot
