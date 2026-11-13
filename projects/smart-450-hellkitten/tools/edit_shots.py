"""Shot table for the Smart 450 'Hellkitten' reel: transcribed from direction.md section 3 / 5.

Frame numbers are timeline frames at 30 fps (= round(T*30)). `n` is the exact frame count of the shot. Crop windows are
source pixels on the UPRIGHT frame: (w, h) and keyed top-left corners [(fraction of the shot 0..1, x0, y0), ...] (linear).
Changes against direction.md are marked CHANGED with the reason (also logged with `ive log`).
"""
DB = "/home/user/media/smart-hellkitten/dropbox"
DESIGN = "/home/user/media/smart-hellkitten/design"
SM = "/home/user/media/work/smart-450"
FPS = 30

# kind: irl | still | scan | logo.  audio: None | 'under' | 'up'
SHOTS = [
    dict(id="S1", start=0, n=22, kind="irl", src="v_1852_56", ss=20.800, win=(504, 896),
         keys=[(0, 736, 184), (0.5, 900, 184), (1, 1100, 184)], audio="under",
         section="parts_off", focus="panels on the floor: this car is in pieces"),
    dict(id="S2", start=22, n=23, kind="irl", src="v_1852_56", ss=25.267, win=(608, 1080),
         keys=[(0, 760, 0)], audio="under", section="stripped_side", focus="bare shell and its door frame (ends on the solved 26.0 s frame)"),
    dict(id="S3", start=45, n=45, kind="scan", scan="a1_match_str", t0=0.0, sections=None, section="stripped_side",
         focus="the same frame as a 3D scan (1:1 cut on drop 1)"),
    dict(id="S4", start=90, n=45, kind="irl", src="v_1857_58", ss=1.200, win=(608, 1080),
         keys=[(0, 520, 0), (1, 600, 0)], audio="under", section="stripped_side", focus="hand on the real door braces"),
    dict(id="S5", start=135, n=23, kind="irl", src="v_1632_12", ss=0.000, win=(608, 1080),
         keys=[(0, 370, 0)], audio="under", section="whole_assembled", focus="the car before: black and intact"),
    dict(id="S6", start=158, n=22, kind="irl", src="v_1634_19", ss=14.500, win=(608, 1080),
         keys=[(0, 560, 0), (1, 450, 0)], audio="up", section="assembled_front", focus="powder turns black paint matte grey"),
    dict(id="S7", start=180, n=23, kind="irl", src="v_1634_19", ss=6.900, win=(608, 1080),
         keys=[(0, 500, 0)], audio="up", section="assembled_side", focus="the powder mist on the door"),
    dict(id="S8", start=203, n=22, kind="irl", src="v_1634_51", ss=0.150, win=None,
         keys=None, audio="up", section="assembled_rear", focus="tail lamp goes matte"),
    dict(id="S9", start=225, n=45, kind="irl", src="v_1724_26", ss=11.000, win=(990, 1760),
         keys=[(0, 85, 0)], audio="under", section="scanner", focus="the scanner: green = captured"),
    dict(id="S10", start=270, n=113, kind="scan", scan="a2_body_on_off", t0=0.0667, swap_t=1.6, post_speed=0.537, section="whole_scan",
         focus="scan body on, then body off on drop 2"),
    dict(id="S11", start=383, n=23, kind="irl", src="v_1659_53", ss=1.900, win=(608, 1080), rot180=True,
         keys=[(0, 540, 0)], audio="under", section="parts_off", focus="what came off: inside of a body panel"),
    dict(id="S12", start=406, n=22, kind="irl", src="v_1712_33", ss=19.050, win=(608, 1080),
         keys=[(0, 540, 0)], audio="under", section="stripped_rear", focus="the bare rear"),
    dict(id="S13", start=428, n=23, kind="irl", src="v_1852_56", ss=6.000, win=(608, 1080),
         keys=[(0, 600, 0), (1, 630, 0)], audio="under", section="stripped_front", focus="front end off, nose on the jack"),
    dict(id="S14", start=451, n=22, kind="irl", src="v_1722_25", ss=24.600, win=(978, 1739),
         keys=[(0, 526, 261)], audio="up", section="stripped_front", focus="the bare structure gets powdered"),
    dict(id="S15", start=473, n=23, kind="irl", src="v_1722_25", ss=35.000, win=(1125, 2000),
         keys=[(0, 190, 0)], audio="up", section="stripped_front", focus="glass turns matte so the scanner can see it"),
    dict(id="S16", start=496, n=45, kind="irl", src="v_1724_26", ss=107.300, win=(849, 1510),
         keys=[(0, 240, 250)], audio="under", section="stripped_front", focus="scanning the bare front"),
    dict(id="S17", start=541, n=23, kind="irl", src="v_1729_10", ss=0.480, win=(608, 1080),
         keys=[(0, 590, 0)], audio="under", section="scanner_result", focus="the scan is on the device"),
    dict(id="S18", start=564, n=67, kind="scan", scan="a3_detail", t0=0.0, speed=0.75, section="stripped_front_scan",
         focus="front structure in detail (scan)"),
    dict(id="S19", start=631, n=45, kind="still", img="Blueprint.jpeg", section="payoff_design",
         focus="the new body drawn over this Smart"),
    dict(id="S20", start=676, n=91, kind="still", img="RenderDay1.jpeg", section="payoff_render",
         focus="what the scan is for"),
    dict(id="S21", start=767, n=31, kind="logo", section="logo", focus="logo card"),
]
END = 798

# frames of each scan shot's PNG sequence that must exist for the shot to count as finished (see direction.md section 4)
# CHANGED a2: 46 (not 60) because S10 plays the post-swap part at 0.537x speed, shot time 1.60-2.80 (R1 not re-keyed: the car touches the frame edge from shot time 3.6 s)
SCAN_NEED = {"a1_match_str": 26, "a2_body_on_off": 46, "a3_detail": 29}   # a3: S18 plays at 0.75x (shot time 0-1.68 s): the car reaches the left frame edge from render frame 30

