"""Car mask for a frame of the red MR2: GrabCut seeded by red-paint pixels (sure FG) and a rough car
region; everything above y_top is sure background. usage: carmask.py frame.png out.png y_top [x0,y0,x1,y1 extra-fg ...]"""
import sys, cv2, numpy as np
img = cv2.imread(sys.argv[1]); H, W = img.shape[:2]; s = 900 / max(H, W)
sm = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); h, w = sm.shape[:2]
hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
red = (((hsv[..., 0] < 8) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 120) & (hsv[..., 2] > 60)).astype(np.uint8)
red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((3, 3)))
n, lab, st, _ = cv2.connectedComponentsWithStats(red); keep = np.zeros_like(red)
for i in range(1, n):
    if st[i, 4] > 0.002 * h * w: keep[lab == i] = 1
gc = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
gc[: int(float(sys.argv[3]) * s)] = cv2.GC_BGD
hull = cv2.convexHull(cv2.findNonZero(keep)); hm = np.zeros_like(keep); cv2.fillPoly(hm, [hull], 1)
gc[cv2.dilate(hm, np.ones((25, 25))) > 0] = cv2.GC_PR_FGD
gc[cv2.erode(keep, np.ones((5, 5))) > 0] = cv2.GC_FGD
for b in sys.argv[4:]:
    x0, y0, x1, y1 = [int(float(v) * s) for v in b.split(',')]; gc[y0:y1, x0:x1] = cv2.GC_FGD
bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
cv2.grabCut(sm, gc, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
m = np.where((gc == 1) | (gc == 3), 255, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
if n > 1: m = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9)))
cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); m[:] = 0; cv2.drawContours(m, cs, -1, 255, -1)
m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR); m = (m > 127).astype(np.uint8) * 255
cv2.imwrite(sys.argv[2], m)
v = img.copy(); v[m > 0] = (0.5 * v[m > 0] + [0, 90, 0]).astype(np.uint8); cv2.imwrite(sys.argv[2].replace('.png', '_vis.jpg'), cv2.resize(v, None, fx=0.25, fy=0.25))
