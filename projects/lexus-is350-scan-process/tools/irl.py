"""Pre-render an FX3A S-Log3 clip as a 1080x1920 30 fps Rec.709 shot whose LAST frame is a given source frame.
  python irl.py src.MP4 end_frame n_out lut.cube out.mp4 --x0 596          # fixed 9:16 window (x0 in 1920-wide px)
  python irl.py ... --x0 760:40 --pan 0.35:1.0                            # window pans x0 760 -> 40 over that span
Source 23.976p frames are mapped to 30 fps by nearest-earlier frame, anchored so output[-1] == end_frame
(the 1:1 match frame). Crop is taken from the 3840x2160 original (window 1215 px wide) -> 1080x1920."""
import argparse, subprocess, tempfile, os, glob, math, shutil
ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('end', type=int); ap.add_argument('n', type=int); ap.add_argument('lut'); ap.add_argument('out')
ap.add_argument('--x0', default='604'); ap.add_argument('--pan', default='0:1'); ap.add_argument('--fps_src', type=float, default=24000 / 1001)
ap.add_argument('--eq', default='')
a = ap.parse_args()
r = a.fps_src / 30.0
src_idx = [a.end - int(math.floor((a.n - 1 - j) * r + 1e-6)) for j in range(a.n)]
s0 = src_idx[0]; ns = a.end - s0 + 1
xs = [float(v) for v in a.x0.split(':')]; p0, p1 = (float(v) for v in a.pan.split(':'))
def x_at(k):  # k = source frame offset from s0
    if len(xs) == 1: return xs[0]
    u = (k / max(1, ns - 1) - p0) / max(1e-6, p1 - p0); u = min(1, max(0, u)); u = u * u * (3 - 2 * u)
    return xs[0] + (xs[1] - xs[0]) * u
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(a.out)))
W = 2160 * 9 / 16  # 1215 px window at 4K
# x expression per source frame (n = frame index within the trimmed stream)
if len(xs) == 1:
    xexpr = f"{xs[0] * 2:.2f}"
else:
    u = f"clip((n/{max(1, ns - 1)}-{p0})/{max(1e-6, p1 - p0)},0,1)"
    xexpr = f"2*({xs[0]}+({xs[1]}-{xs[0]})*({u})*({u})*(3-2*({u})))"
vf = (f"trim=start_frame={s0}:end_frame={a.end + 1},setpts=PTS-STARTPTS,"
      f"crop={W:.0f}:2160:'{xexpr}':0,lut3d='{a.lut}'" + (f",{a.eq}" if a.eq else "") + ",scale=1080:1920:flags=lanczos")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.src, '-vf', vf, '-vsync', '0', f'{tmp}/s_%04d.png'], check=True)
fr = sorted(glob.glob(f'{tmp}/s_*.png')); assert len(fr) == ns, (len(fr), ns)
with open(f'{tmp}/list.txt', 'w') as f:
    for i in src_idx:
        f.write(f"file '{fr[i - s0]}'\nduration {1 / 30:.6f}\n")
    f.write(f"file '{fr[src_idx[-1] - s0]}'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-frames:v', str(a.n), '-r', '30',
                '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', a.out], check=True)
shutil.copy(fr[-1], a.out.replace('.mp4', '_last.png')); shutil.rmtree(tmp)
print(a.out, 'src frames', s0, '..', a.end, 'out', a.n)
