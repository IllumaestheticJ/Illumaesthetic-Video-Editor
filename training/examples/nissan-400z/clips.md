# Nissan 400Z scan reel - sources

Scan-only reel (no IRL footage, no text). Drive folder `Nissan 400Z` (19MtEJIiJ3mH9_t0CdsVSPTAs4N2cd5Ot), service account.

| File | Drive id | Tris (raw) | Use |
|---|---|---|---|
| 400Z Full Car.stl (2.0 GB, 2026-02) | 1a2jkoB8od3omEebQTHodQBtjIaXr-R9c | ~41.7M | base; 3 mm (5.6M) full-car shots, 2 mm crops for close-ups |
| Bomex Bumper Only | 1B80XnuGMJnKFwDMjGy7hmUiix8sxC_xH | 5.0M | front bumper part (shell + grille) |
| Bomex Bumper Grille Removed | 1wNP2vQLlc5zmnd8lpWeEdnRLh-AOr-gN | 3.5M | grille = Bumper Only minus this |
| Bomex Bumper and hood removed | 1da73mBcE6-IUvZS3tXQ7TtCl3G1hjGYg | 5.0M | front structure under the bumper (explode base) |
| Bomex Hood Open | 1VaUqAEg9YotGePG50LW6sJdRYOpQkkni | 10.0M | engine bay (hood + explode bases); open hood fits the hinge |
| Bomex Rear Wing Removed | 1Db0DszsGKoux0YuDi771WRMcU8NohXPy | 13.3M | spoiler = car minus this; trunk under it |
| Bomex Side Mirrors Removed | 1UNohTMZQ0N3N58u2y50lKp8EdnlCot8C | ~20M | mirrors = car minus this; mounts under them |
| Bomex Rear Gas Door Open | 1LbjilZmH697MLevQeScvTV0RVHjLCV_0 | 2.5M | not used (partial quarter capture) |

Not used: Side Mirrors / Air Ducting / Upper / Lower Grille part files (possible Bomex CAD, not on the allowed list),
crash-foam-removed, 400Z.blend (2023).

All in one Artec frame (registration check: check renders + nearest-surface p50 1.4-1.7 mm). Car has full wheels,
but rims are hollow spoke fragments up close.

Media: /home/user/media/nissan-400z/{scans,dec,lev,parts}, /home/user/media/work/z400/{blend,renders,check}.
Pipeline: decimate 3 mm -> tools/level.py (level.json) -> ive prep car.json (--drop-islands 3000) -> parts/states --like car.json.
