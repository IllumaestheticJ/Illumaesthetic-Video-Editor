"""Per-frame global motion (px at 1080-wide portrait) via cv2.phaseCorrelate on downscaled frames.
usage: motion.py clip.mov"""
import sys, subprocess, numpy as np, cv2
clip = sys.argv[1]; w, h = 270, 480
raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', clip, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
win = cv2.createHanningWindow((w, h), cv2.CV_32F); fps = 29.988
for i in range(1, len(fr)):
    (dx, dy), r = cv2.phaseCorrelate(fr[i - 1], fr[i], win)
    print(f"{i/fps:6.3f} f{i:3d} dx {dx*4:6.1f} dy {dy*4:6.1f} |{np.hypot(dx,dy)*4:5.1f}| r {r:.2f}")
