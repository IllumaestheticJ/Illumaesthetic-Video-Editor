# Toyota MR2 SW20 scan-process reel — clip notes
Footage: Dropbox `/1. Epsilon Plus Videos/1. Video dumps/MR2 SW20 scanning/` -> `/home/user/media/mr2/dropbox/`.
iPhone, HEVC HLG, 1920x1080 rotated -90 (portrait), 30 fps, Jul 20 2026. Local name = v_HHMM_SS (24 h).
Not used: `/2. Illumaesthetic Videos/1. Video dumps/MR2 Kalvin footage` (Sony FX30, 2025-06, MR2 Spyder per knowledge/car-inventory.md).

| local | Dropbox name | len | content | car state |
|---|---|---|---|---|
| v_1432_22 | Video Jul 20 2026, 2 32 22 PM.mov | 1.1 s | crew back, door opening, powdered cabin | doors off |
| v_1433_07 | Video Jul 20 2026, 2 33 07 PM.mov | 2.5 s | **rear-left 3/4, crew leaning into empty left door opening with scanner; car on lift, wheel off** -> 1:1 at 2.300 s | doors off, T-tops ON, frunk + engine lid open |
| v_1433_19 | Video Jul 20 2026, 2 33 19 PM.mov | 4.3 s | scanner in cabin close-up | |
| v_1434_17 | 2 34 17 PM | 0.7 s | inside looking up at roof/T-bar | |
| v_1434_18 | 2 34 18 PM | 2.2 s | whip pan, low angle, lift | unusable (motion) |
| v_1434_23 | 2 34 23 PM | 3.0 s | crew scanning cabin through door opening, T-bar | |
| v_1434_34 | 2 34 34 PM | 3.4 s | scanner over floor pan (hands) | |
| v_1434_39 | 2 34 39 PM | 3.8 s | scanner across cabin, blue lift | |
| v_1438_02 | 2 38 02 PM | 3.5 s | crew scanning door inner panel (door on) | |
| v_1447_56 | 2 47 56 PM | 4.3 s | from driver side, looking across: windshield, passenger T-top, passenger door inner panel being scanned | passenger door ON, T-tops ON |
| v_1448_05 | 2 48 05 PM | 4.2 s | across cabin through empty door opening | one door off |
| v_1448_15 | 2 48 15 PM | 3.6 s | crew scanning door inner panel, standing in opening | |
| v_1456_05 / v_1456_11 | 2 56 05 / 2 56 11 PM | 4.2 / 4.6 s | across cabin, crew scanning rear bulkhead | |
| v_1500_26 | 3 00 26 PM | 3.0 s | **crew leaning into door opening; scanner screen shows the live scan** | |
| v_1529_27 | 3 29 27 PM | 5.4 s | over the roof into cabin (rear quarter foreground, frunk lid up) | doors off (far door on?), T-tops off |
| v_1529_40 | 3 29 40 PM | 3.6 s | front fender / A-pillar, crew scanning roof | |
| v_1602_36 | 4 02 36 PM | 7.3 s | rear-left 3/4 then rear, crew scanning trunk lid overhead | trunk open |
| v_1602_50 | 4 02 50 PM | 4.6 s | **straight rear: trunk open on prop rod, MR2 garnish, plate; crew scanning the trunk lid** -> 1:1 at 4.400 s | trunk open (Interior scan) |
| v_1603_04 | 4 03 04 PM | 3.9 s | scanner screen in hand (Artec Leo UI), car behind | |
| screen_0729_0318 | 2026-07-29 03-18-50.mp4 | 97 s | Artec Studio screen recording (over remote desktop in a browser) of the textured SW20 scan; crop only inside the viewport (x 990-1384, y 118-818) - the rest shows personal browser tabs | |

Scans (engineering Drive, `Toyota MR2 (SW20) > SW20 > Cage`, Artec, mm, one shared frame):
| file | id | tris (STL header) | state |
|---|---|---|---|
| Toyota MR2 SW20 Full Chassis Interior.stl (2026-07-26) | 1WA7Rd8Z89rax3HImfaaFhhQBFUM_qk8I | 34,993,395 | doors + T-tops ON (glass sprayed), trunk + engine lid + frunk open, interior stripped, on stands |
| Toyota MR2 SW20 Full Chassis T-Top Off.stl (2026-07-26) | 1Q-MPfO994hTUE7wQS_iqJiJNGuTlOzX6 | 34,998,108 | doors + both T-tops removed, engine lid + frunk open, trunk shut |
| Toyota MR2 SW20 Chassis Simplified.stl (2026-11-10) | 1-5uoI8T6bNIPGu0B1CLZ21n1l3RpuTOw | 9,989,226 | cabin-only cut for cage design - not used (later derivative) |
| MR2 sw20 full car.stl (2025-02) | 1IUSJML7dmNRuQrv1EI5hK26dVIQY_R96 | - | assembled car (listing hero) - not used |
Doors in the Interior scan: inner face only (outer skin not scanned) - verified by rendering from outside.

Pipeline (all in /home/user/media/work/mr2): decimate 4 mm -> tools/level.py fit (huracan) + tools/relevel.py (true ground)
-> level.py apply -> ive crop -> tools/islands.py -> ive prep (ttop.blend; interior/simpl/parts with --like ttop.json).
Parts: tools/diffparts.py interior vs ttop (12 mm) -> part02/part03 = door+T-top per side -> tools/split_door_ttop.py.
Composites: comp_ttopsOn = T-Top Off + both T-tops (side 1:1 state).

Music: parent-session SW20 track (ElevenLabs via Higgsfield), `/home/user/media/work/music/toyota-mr2-sw20-scan-process_track.mp3`
(not committed). 112 BPM, drop 8.643 s, ends ~34.7 s. Reel uses 5.428 s onward.
Listing: https://www.illumaesthetic.com/products/toyota-mr2-sw20-3d-scan-1989-1999
