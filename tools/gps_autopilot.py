"""Stop-and-check autopilot for a racing game running under tools/game_driver.js: follows the neon-blue
3D GPS arrow that NFS Underground 2 draws above the car.

    python tools/gps_autopilot.py --seconds 25 [--port 8765] [--debug out_dir]

Each tick (as fast as screenshots come back, about 1 Hz on software graphics): screenshot -> mask the arrow's blue in the upper-middle of the frame -> the arrow's
on-screen width gives how far to turn and the side its bulk sits on gives which way -> hold left/right in proportion, keep the throttle on a duty cycle, back out if the
picture stops changing. It stops early when the game logs a new screen (a prompt, a cutscene), and it
always releases every key on exit. It is a helper for a supervising agent, not a self-driving car: run
it in short bursts and look at the last frame after each one.
"""
import argparse, json, math, sys, time, urllib.request
import cv2, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--seconds", type=float, default=20)
ap.add_argument("--port", type=int, default=8765)
ap.add_argument("--cruise", type=float, default=24, help="throttle is held while the frame-to-frame change is below this (24 is about 35 mph at 480x270)")
ap.add_argument("--stuck", type=float, default=9, help="ticks under 10 mph before backing out (0 = never)")
ap.add_argument("--reverse", type=float, default=4.0, help="seconds to reverse when stuck")
ap.add_argument("--debug", default="")
ap.add_argument("--shot", default="/home/user/media/work/ap_frame.jpg")
a = ap.parse_args()
B = f"http://127.0.0.1:{a.port}"


def get(path):
    return json.loads(urllib.request.urlopen(B + path, timeout=20).read())


held = set()
def hold(k, on):
    if on and k not in held:
        get(f"/down?k={k}"); held.add(k)
    elif not on and k in held:
        get(f"/up?k={k}"); held.discard(k)


def screens():
    return [l for l in get("/log?n=40")["log"] if "[fng]" in l or "nis=1" in l]


def arrow(im):
    h, w = im.shape[:2]
    x0, x1, y0, y1 = int(w * .28), int(w * .72), int(h * .08), int(h * .50)
    hsv = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (85, 90, 130), (128, 255, 255))      # blue fill and cyan rim
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[i, cv2.CC_STAT_AREA] < 0.0006 * w * h:
        return None
    blob = (lab == i).astype(np.uint8)
    blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # The arrow is a flat block arrow above the car: a wide triangular head on a short narrow stub.
    #  - |turn| from the blob's width: widest when it points sideways, narrowest ahead/behind.
    #  - which way, sideways: seen side-on the head is a thick slab and the stub a thin bar, so the
    #    thicker half is the head.
    #  - ahead or behind, when compact: the head is a triangle, so the thin end is its tip. The arrow
    #    floats above eye level, so its far end projects LOWER on screen: tip low = straight ahead,
    #    tip high = it points back at the camera.
    # Tried and dropped: PCA long axis, distance-transform peak, centroid offset (a triangle's centroid
    # sits near its base), and "the thin end is the tip" for sideways views (there the stub is the thin end).
    cols = blob.sum(0); rows = blob.sum(1)
    xs = np.nonzero(cols)[0]; ys = np.nonzero(rows)[0]
    bx0, bx1, by0, by1 = xs[0], xs[-1], ys[0], ys[-1]
    bw, bh = bx1 - bx0 + 1, by1 - by0 + 1
    c = cols[bx0:bx1 + 1].astype(np.float64)
    a_, b_ = int(bw * 0.10), int(bw * 0.45)
    left, right = c[a_:b_].mean(), c[bw - b_:bw - a_].mean()        # thickness of each half, ends trimmed
    k = max(2, int(bh * 0.3))
    top, bottom = rows[by0:by0 + k].mean(), rows[by1 - k + 1:by1 + 1].mean()
    mag = float(np.clip((bw / w - 0.105) / (0.165 - 0.105), 0, 1))
    sign = 1.0 if right > left else -1.0
    back = mag < 0.45 and top < bottom * 0.8
    return sign * mag, bool(back), int(st[i, cv2.CC_STAT_AREA]), (x0 + bx0, y0 + by0, x0 + bx1, y0 + by1), (float(left), float(right))


base = screens()
t_end = time.time() + a.seconds
prev = None; still = 0; k = 0; backs = 0; reason = "time"
try:
    while time.time() < t_end:
        get(f"/shot?path={a.shot}&q=60")
        im = cv2.imread(a.shot)
        small = cv2.cvtColor(cv2.resize(im, (160, 90)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        moved = 99 if prev is None else float(np.abs(small - prev)[20:60].mean())
        prev = small
        ar = arrow(im)
        if screens() != base:
            reason = "screen changed"; break
        steer = ar[0] if ar else 0.0
        if ar and ar[1]:
            steer = 1.0                                # destination is behind: turn round to the right
        # Stopped or crawling = the speed readout has no tens digit (HUD box measured at 480x270: the
        # units digit sits at x 454-460, y 224-232, the tens digit just left of it). Frame differencing
        # cannot tell: rain and the day/night cycle keep the picture changing while the car is wedged.
        hh, ww = im.shape[:2]
        tens = cv2.cvtColor(im[int(hh * 224 / 270):int(hh * 233 / 270), int(ww * 444 / 480):int(ww * 453 / 480)], cv2.COLOR_BGR2GRAY)
        slow = int((tens > 140).sum()) < 3
        still = still + 1 if (slow and a.stuck > 0) else 0
        if still >= int(a.stuck):                     # stuck: back out turning away, then drive toward the arrow
            hold("ArrowUp", False); hold("ArrowLeft", False); hold("ArrowRight", False)
            want = "ArrowLeft" if steer < 0 else "ArrowRight"
            away = "ArrowRight" if steer < 0 else "ArrowLeft"
            hold(away, True); hold("ArrowDown", True); time.sleep(a.reverse); hold("ArrowDown", False); hold(away, False)
            hold(want, True); hold("ArrowUp", True); time.sleep(a.reverse * 0.7); hold(want, False)
            still = 0; prev = None; backs += 1
            print("  backed out"); continue
        # The game runs at a few frames a second on software graphics: a key must stay down for a few
        # hundred ms or the game never samples it, so keys are held states, not taps.
        hard = abs(steer) > 0.75
        hold("ArrowUp", slow or moved < (12 if hard else a.cruise))   # frame-to-frame change stands in for speed above 10 mph
        hold("ArrowLeft", steer < -0.3); hold("ArrowRight", steer > 0.3)
        if 0.3 < abs(steer) <= 0.75:                  # gentle correction: a short pulse, then straighten
            time.sleep(0.45); hold("ArrowLeft", False); hold("ArrowRight", False)
        if a.debug and k % 4 == 0:
            cv2.imwrite(f"{a.debug}/ap_{k:04d}.jpg", cv2.resize(im, (480, 270)))
        print(f"  t={a.seconds - (t_end - time.time()):5.1f} arrow={'none' if not ar else f'{ar[0]:+.2f} back={int(ar[1])} a={ar[2]}'} steer={steer:+.2f} moved={moved:.1f} slow={int(slow)}")
        k += 1
finally:
    for key in list(held):
        hold(key, False)
print("STOP:", reason)
