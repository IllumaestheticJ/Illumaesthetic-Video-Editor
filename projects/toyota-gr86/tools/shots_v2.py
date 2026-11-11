"""v2 shot specs (projects/toyota-gr86/director.md): whole-car opener, front section (hood off -> bay -> front bumper off
-> front structure), rear section (rear bumper off -> beam), top stack that hands over to s7's reassembly tail.
Part rot = degrees XYZ about the part's bbox centre (no pivot). Times are local shot time; seconds = slot + 0.2.
  python projects/toyota-gr86/tools/shots_v2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import spec, B  # noqa: E402  (re-writes the v1 specs too; harmless)

Z = [0, 0, 0]


def k(t, loc, rot=Z, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def cam(t, loc, target, focal):
    return {"t": t, "loc": loc, "target": target, "focal": focal, "ease": "inout"}


FB_OFF, FB_ROT = [0.30, -0.90, -0.42], [110, 0, 0]
RB_OFF, RB_ROT = [0.30, 0.90, -0.42], [-110, 0, 0]
HOOD_UP = [0, -0.10, 1.20]
HOOD_AWAY = [0, -0.10, 2.40]   # rises out of the top of frame while the camera reads the bay
FB_AWAY = [1.70, -1.30, -0.42]  # after its inside is shown the bumper slides out of frame (clear view of the structure)
RB_AWAY = [1.70, 1.30, -0.42]

# A: whole car, front-right 3/4, dolly-in + small arc (motion from frame 1, nothing clipped)
spec("a_open", ["car4.blend"], [
    cam(0, [4.60, -4.70, 1.40], [0, -0.25, 0.70], 30),
    cam(5.162, [2.10, -5.90, 1.10], [0, -0.50, 0.66], 30)], 5.162)  # ~20 deg arc + push: v1's 0.8 m dolly read as static (ive director)

# C: front section. hood lifts off (lands 2.449 = 9.860 abs), bay read, front bumper out + tipped (lands 7.347 = 14.758 abs)
spec("d_front", ["comp_explode.blend"], [
    cam(0, [2.20, -4.90, 2.00], [0.10, -1.40, 0.80], 30),
    cam(2.449, [1.60, -4.00, 2.70], [0.05, -1.20, 0.75], 30),
    cam(4.898, [0.90, -3.30, 2.50], [0.00, -1.10, 0.70], 32),
    cam(7.347, [2.40, -5.30, 1.65], [0.25, -1.95, 0.55], 30),
    cam(9.996, [1.00, -3.60, 1.20], [0.00, -1.85, 0.55], 30)], 9.996,
    parts=[{"blend": B + "hood_m.blend", "keys": [k(0, Z), k(0.612, Z), k(2.449, HOOD_UP, ease="out"), k(4.898, HOOD_AWAY, ease="in")]},
           {"blend": B + "front_bumper.blend", "keys": [k(0, Z), k(5.510, Z), k(7.347, FB_OFF, FB_ROT),
                                                        k(9.996, FB_AWAY, FB_ROT)]},
           {"blend": B + "rear_bumper.blend", "keys": [k(0, Z)]}])

# D: rear section. rear bumper out + tipped (lands 2.449 = 19.656 abs), push in on the beam, slide to the left tip
spec("g_rear", ["comp_explode.blend"], [
    cam(0, [1.70, 4.50, 1.60], [0.05, 1.75, 0.75], 30),
    cam(2.449, [2.10, 4.80, 1.70], [0.10, 2.10, 0.60], 30),
    cam(4.898, [1.10, 3.80, 1.15], [0.05, 1.95, 0.72], 30),
    cam(7.547, [-0.65, 3.70, 1.05], [-0.15, 1.95, 0.70], 32)], 7.547,
    parts=[{"blend": B + "rear_bumper.blend", "keys": [k(0, Z), k(0.612, Z), k(2.449, RB_OFF, RB_ROT),
                                                       k(4.898, RB_AWAY, RB_ROT)]},
           {"blend": B + "hood_m.blend", "keys": [k(0, [0, -0.10, 8.0])]},  # parked far out of frame
           {"blend": B + "front_bumper.blend", "keys": [k(0, FB_AWAY, FB_ROT)]}])

# E: top-down stack -> high rear-right 3/4; end poses = s7 f111 (hood z 1.253, bumpers z 0.803)
spec("s_stack", ["comp_explode.blend"], [
    cam(0, [0.30, 1.40, 8.00], [0, -0.10, 0.80], 34),
    cam(2.449, [0.50, 1.60, 7.00], [0, -0.10, 0.85], 36),
    cam(7.547, [2.40, 6.20, 5.60], [0, -0.20, 0.95], 34)], 7.547,
    parts=[{"blend": B + "front_bumper.blend", "keys": [k(0, FB_OFF, FB_ROT), k(2.449, [0, -0.50, 0.78]),
                                                        k(7.547, [0, -0.50, 0.803], ease="lin")]},
           {"blend": B + "rear_bumper.blend", "keys": [k(0, RB_OFF, RB_ROT), k(0.612, RB_OFF, RB_ROT),
                                                       k(2.449, [0, 0.50, 0.78]), k(7.547, [0, 0.50, 0.803], ease="lin")]},
           {"blend": B + "hood_m.blend", "keys": [k(0, HOOD_UP), k(2.449, [0, -0.10, 1.22]),
                                                  k(7.547, [0, -0.10, 1.253], ease="lin")]}])
