"""Numeric inspection of a delivered DITL cut. python inspect_cut.py <cut.mp4> -> JSON on stdout.
Layout (picture 1080x1080 at y=420..1499, black bands, title inside 80 px margins), cuts (frame diffs at the expected
cut frames, flashes, duplicates, dark frames), container facts."""
import sys, json, subprocess, numpy as np

NF = [66, 48, 47, 95, 48, 48, 47, 72, 48, 48, 162, 48, 48, 81, 180]
CUTS = [sum(NF[:i]) for i in range(1, len(NF))]          # index of the first frame of shots 2..15
W, H = 1080, 1920
path = sys.argv[1]
probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True).stdout)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
n = 0; prev = None; diffs = []; means = []; band_max = 0; title_box = [W, H, 0, 0]; edge = []
while True:
    b = p.stdout.read(W * H)
    if len(b) < W * H: break
    y = np.frombuffer(b, np.uint8).reshape(H, W).astype(np.int16)
    pic = y[420:1500]; top = y[:420]; bot = y[1500:]
    tm = top > 40; ys, xs = np.where(tm)
    if len(xs): title_box = [min(title_box[0], xs.min()), min(title_box[1], ys.min()), max(title_box[2], xs.max()), max(title_box[3], ys.max())]
    outside = top.copy(); outside[150:360, 60:1020] = 0          # band outside the title area
    band_max = max(band_max, int(outside.max()), int(bot.max()))
    edge.append((float(y[419].mean()), float(y[1500].mean())))
    means.append(float(pic.mean()))
    if prev is not None: diffs.append(float(np.abs(pic - prev).mean()))
    prev = pic; n += 1
d = np.array(diffs)                                           # d[i] = diff between frame i and i+1
cut_d = {c: round(float(d[c - 1]), 1) for c in CUTS}          # diff entering the first frame of each shot
inner = np.array([v for i, v in enumerate(d) if (i + 1) not in CUTS])
flashes = [i for i in range(1, len(d)) if d[i - 1] > 25 and d[i] > 25 and (i not in CUTS and (i + 1) not in CUTS)]
dups_at_cuts = [c for c in CUTS if d[c - 1] < 0.05 or (c < len(d) and d[c] < 0.05) or d[c - 2] < 0.05]
dark = [i for i, m in enumerate(means) if m < 12]
v = [s for s in probe["streams"] if s["codec_type"] == "video"][0]; a = [s for s in probe["streams"] if s["codec_type"] == "audio"]
out = dict(frames=n, expected=sum(NF), size=f'{v["width"]}x{v["height"]}', fps=v["r_frame_rate"], pix_fmt=v["pix_fmt"], audio=a[0]["codec_name"] if a else None,
           band_max_luma=band_max, title_bbox=[int(t) for t in title_box], title_in_80px_margins=bool(title_box[0] >= 80 and title_box[2] <= W - 80),
           row419_mean_max=round(max(e[0] for e in edge), 1), row1500_mean_max=round(max(e[1] for e in edge), 1),
           cut_diffs=cut_d, min_cut_diff=round(min(cut_d.values()), 1), inner_diff_p99=round(float(np.percentile(inner, 99)), 1), inner_diff_max=round(float(inner.max()), 1),
           flashes=flashes, dups_at_cuts=dups_at_cuts, dark_frames=dark, min_mean_luma=round(min(means), 1),
           last_frame_mean=round(means[-1], 1))
print(json.dumps(out, indent=1))
