"""Stabilise C0240 on the CAR (not the background): track features on the car body with LK optical flow, estimate
per-frame similarity (scale+rot+translation), replace the measured path with a cubic fit over the clip, warp each
frame by (smooth path) o (measured path)^-1. Writes footage/c0240_carstab.mp4 (same timing as c0240_seg.mp4)."""
import cv2, numpy as np, subprocess
F = '/home/user/media/bf-integra-385-combo/footage'
cap = cv2.VideoCapture(f'{F}/c0240_seg.mp4'); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
H, W = frames[0].shape[:2]; n = len(frames); print('frames', n, W, H)
def carmask(shape):
    m = np.zeros(shape[:2], np.uint8); m[int(H * 0.22):int(H * 0.92), int(W * 0.15):int(W * 0.85)] = 255; return m
A = [np.eye(3)]
prev = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
for k in range(1, n):
    cur = cv2.cvtColor(frames[k], cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(prev, 600, 0.01, 8, mask=carmask(prev.shape))
    p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, p0, None, winSize=(31, 31), maxLevel=4)
    g = st.ravel() == 1
    M, inl = cv2.estimateAffinePartial2D(p0[g], p1[g], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    T = np.vstack([M, [0, 0, 1]]); A.append(T @ A[-1]); prev = cur
# decompose cumulative transforms -> (dx, dy, angle, log scale), fit cubic, rebuild
P = np.array([[a[0, 2], a[1, 2], np.arctan2(a[1, 0], a[0, 0]), np.log(np.hypot(a[0, 0], a[1, 0]))] for a in A])
t = np.arange(n); S = np.stack([np.polyval(np.polyfit(t, P[:, j], 3), t) for j in range(4)], 1)
print('raw vs smooth residual px (std):', (P[:, :2] - S[:, :2]).std(0).round(2))
out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '23.976',
                        '-i', '-', '-c:v', 'libx264', '-crf', '12', f'{F}/c0240_carstab.mp4'], stdin=subprocess.PIPE)
def mat(p):
    c, s_ = np.cos(p[2]) * np.exp(p[3]), np.sin(p[2]) * np.exp(p[3]); return np.array([[c, -s_, p[0]], [s_, c, p[1]], [0, 0, 1]])
zoom = 1.06  # hide warped borders
Z = np.array([[zoom, 0, W / 2 * (1 - zoom)], [0, zoom, H / 2 * (1 - zoom)], [0, 0, 1]])
for k in range(n):
    Wk = Z @ mat(S[k]) @ np.linalg.inv(A[k])
    out.stdin.write(cv2.warpAffine(frames[k], Wk[:2], (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
out.stdin.close(); out.wait(); print('wrote c0240_carstab.mp4')
