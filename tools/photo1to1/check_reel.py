"""check_reel.py VIDEO OUT.jpg : cut times vs kicks in the file's own audio + a sheet of each cut (blend) and shot."""
import sys, subprocess, numpy as np, librosa
from PIL import Image, ImageDraw
O, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', O, '-vf', 'scale=180:320', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 320, 180, 3)
cuts = [i + 1 for i in np.nonzero(np.abs(np.diff(f.mean(3), axis=0)).mean((1, 2)) > 12)[0]]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', O, '-vn', '-ac', '1', '-ar', '22050', '/tmp/_chk.wav'])
y, sr = librosa.load('/tmp/_chk.wav', sr=22050); S = np.abs(librosa.stft(y, n_fft=2048, hop_length=128)); fr = librosa.fft_frequencies(sr=sr, n_fft=2048)
k = S[(fr > 40) & (fr < 120)].sum(0); k /= k.max(); t = librosa.times_like(k, sr=sr, hop_length=128)
kt = t[librosa.util.peak_pick(k, pre_max=20, post_max=20, pre_avg=40, post_avg=40, delta=0.08, wait=40)]
errs = [1000 * (c / 30 - kt[np.argmin(abs(kt - c / 30))]) for c in cuts]
print('frames', len(f), 'cuts', len(cuts), 'cut-kick ms', [round(e) for e in errs])
sh = Image.new('RGB', (180 * len(cuts), 640))
for i, c in enumerate(cuts):
    sh.paste(Image.blend(Image.fromarray(f[c - 1]), Image.fromarray(f[c]), 0.5), (i * 180, 0)); sh.paste(Image.fromarray(f[min(len(f) - 1, c + 20)]), (i * 180, 320))
    ImageDraw.Draw(sh).text((i * 180 + 3, 3), f'{c / 30:.2f}s', fill='yellow')
sh.save(out)
