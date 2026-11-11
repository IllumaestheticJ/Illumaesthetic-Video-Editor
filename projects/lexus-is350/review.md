# Lexus IS350 2026 facelift scan reel: self-review (v2, first delivery)

Output: `/home/user/media/lexus-is350/out/lexus_is350_v2.mp4`. 1080x1920, 30 fps, 33.53 s, 1006 frames. Music: lexus-is350_track.mp3, an original track generated for this reel.

## Before scoring: two things that changed the reel

**Two cars, not one.** The Drive folder holds two different cars.
- The root "Full Car" STL is an older IS350, plate 9JTY488.
- The "2026 IS350 Facelift" scans are a different car: different grille and wheels, an empty dealer plate frame. The grille mesh sits 8-12 mm off the full car, the headlamps 0.8 mm.
- Mixing them would have exploded facelift parts off another car. The reel therefore uses the facelift scans only.
- The facelift set is a front clip: bumper to A-pillar base. So there are no full-car, side or rear shots.

**v1 was never delivered.** The user's v2 notes for all reels (relayed by the parent session) were built in first:
- scene order set by a scene-director agent;
- section-by-section explode;
- whole-clip opener;
- no repeats;
- bumper-removed beat as the hero, with labels;
- fade and a small logo;
- luma check;
- cuts timed against the decoded audio.

## Scores

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Orbit moves from frame 1 on the whole facelift front clip. A bolder opener would show the signature (badge bar) first. Here it comes at 5.5 s |
| 2 | Beat sync | 5 | All 9 cuts are within 0.26 frames of the broadband kick onset in the delivered file's own audio (tools/cutcheck.py). The bumper separates on the 16.03 s drop and locks on 28.56 s |
| 3 | 1:1 match | n/a | Scan-only brief, no IRL footage |
| 4 | Scan quality | 3 | Silver on black. No ground, no debris (islands dropped, floor cut). Points off for real data limits: the hood top is speckled (dusty glossy capture), so it is kept out of close-ups. The deep bay behind the radiator is unscanned, a dark void in the bay shots. The bumper shell needed ICP (7.3 to 3.3 mm). The fast pull-off ghosts slightly in the 15 to 30 fps minterpolate |
| 5 | Story | 4 | The order follows the scan data. The hood opens to the real Hood Open capture. The bumper comes off on the drop, then a long hold on the crash beam and mounts behind it, then the bumper's scanned inner face (mounting points, radar unit), then reassembly. Every state shown has a registered scan of this car |
| 6 | Grade | n/a | No IRL footage. Scan renders AgX, no colour |
| 7 | Text | 4 | 5 labels, at most 2 at once, in black space under the subject, each named from the renders: ENGINE BAY, FRONT BUMPER REMOVED, CRASH BEAM, MOUNTING POINTS, RADAR UNIT. No numbers. Labels are fairly small (52 px) |
| 8 | Ending | 4 | Reassembly locks on a kick, a 0.5 s fade, then a small logo (380 px) from the 30.03 s kick through the track's decay. The audio fades with the card |
| 9 | Technical | 5 | h264 yuv420p + AAC, 1080x1920 30 fps. Luma scan of every render folder: no dark frames, max frame-to-frame step 4.0. Persistent data off. `ive director` reports no repeated views and no flags |

## Known gaps

- **No full facelift car exists**, so the opener is a front clip, not a whole car. The older full car could carry a separate reel with only its own data (and its plate blanked).
- **Hood shown closed:** the facelift "Front End Hood Closed" scan has no hood skin. The closed hood is the Hood Open panel rotated shut on the fitted hinge (2.4 mm fit). It appears closed only briefly, in the opener and close-ups.
- **Assumed removal order:** the parts come off the floated bumper, not the car. That assumes they were removed on the bench, which is not confirmed (direction.md, open question 1).
- **IRL footage:** the Dropbox footage (FX30541-55) dates from 2025-07-12. Check it shows the facelift car before planning a 1:1-cut version.
