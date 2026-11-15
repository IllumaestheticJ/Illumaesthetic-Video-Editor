"""Continuous music bed for a review cut. usage: music.py <media_dir> <in.mp4> <timeline.md> <out.mp4> [single <track file>]
With `single`, one track carries the whole video (owner, v4: several tracks "jumps around and is massively confusing"):
it starts at SINGLE_OFF, and loops with a 4 s crossfade before its fade-out tail.
One track per section (plan below), 4 s crossfades centred on the section change, every track levelled to the same
loudness, bed about 14 dB under the voice, lifted 8 dB with 3 s ramps where the picture runs without any voice
(the track montage). Prints the bed level second by second around each change and the quietest second overall."""
import sys, re, subprocess, numpy as np
M, IN, TLM, OUT = sys.argv[1:5]; SR = 48000
PLAN = [('0.', 'private_wins', 6), ('2.', '2am', 10), ('3.', 'dark_summer_night', 8), ('4.', 'time_stand_still', 10), ('5.', 'cosmic_countdown', 12),
        ('6.', '2am', 30), ('7.', 'private_wins', 60), ('9.', 'dark_summer_night', 60)]       # section prefix -> track, start offset (s)
BED_DB, LIFT_DB, XF = -15.0, 8.0, 4.0        # bed gain applied to a track levelled to -18 LUFS  ->  about -33 LUFS, voice is -19


def load(path, extra=()):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, *extra, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


SINGLE = sys.argv[6] if len(sys.argv) > 6 and sys.argv[5] == 'single' else None
rows = []
for l in open(TLM):
    c = [x.strip() for x in l.split('|')]
    if len(c) > 6 and ':' in c[1] and c[1][0].isdigit():
        m, s = c[1].split(':'); rows.append((int(m) * 60 + float(s), float(c[2]), c[3], c[4]))
total = rows[-1][0] + rows[-1][1]; N = int(total * SR)
starts = []
for pre, trk, off in PLAN:
    t0 = next(r[0] for r in rows if r[2].startswith(pre)); starts.append((0.0 if pre == '0.' else t0, trk, off))
bed = np.zeros(N, np.float32)
if SINGLE:
    x = load(SINGLE, ['-af', 'loudnorm=I=-18:TP=-2:LRA=7']); k = int(XF * SR)
    body = x[int(1.0 * SR):len(x) - int(9 * SR)]                      # drop the fade-out tail
    pos = 0
    while pos < N:
        seg = body[:N - pos + k].copy(); n = len(seg)
        if pos > 0: seg[:k] *= np.sin(np.linspace(0, np.pi / 2, k)) ** 2
        if pos + n < N + k and n == len(body): seg[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2
        m_ = min(n, N - pos); bed[pos:pos + m_] += seg[:m_]; pos += len(body) - k
    starts = []
for i, (t0, trk, off) in enumerate(starts):
    t1 = starts[i + 1][0] if i + 1 < len(starts) else total
    a, b = max(0, t0 - XF / 2), min(total, t1 + XF / 2); n = int((b - a) * SR)
    x = load(f'{M}/music/{trk}.mp3', ['-af', 'loudnorm=I=-18:TP=-2:LRA=7,acompressor=threshold=-24dB:ratio=3:attack=200:release=1500:makeup=2'])
    seg = np.resize(x[int(off * SR):], n)                       # loops if the section outlasts the track
    env = np.ones(n, np.float32); k = int(XF * SR)
    if i > 0: env[:k] = np.sin(np.linspace(0, np.pi / 2, k)) ** 2
    if i + 1 < len(starts): env[-k:] = np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    s0 = int(a * SR); bed[s0:s0 + n] += (seg * env)[:N - s0]
gain = np.full(N, 10 ** (BED_DB / 20), np.float32)
spans = [(r[0], r[0] + r[1]) for r in rows if r[3] == 'PICTURE' and r[2].startswith('8.')]
if spans:
    a, b = min(s[0] for s in spans), max(s[1] for s in spans); t = np.arange(N) / SR
    up = np.clip((t - (a - 1.5)) / 3, 0, 1) * np.clip(((b + 1.5) - t) / 3, 0, 1)
    gain *= 10 ** (LIFT_DB * up / 20)
bed *= gain; bed[:int(1.0 * SR)] *= np.linspace(0, 1, int(1.0 * SR)); bed[-int(3 * SR):] *= np.linspace(1, 0, int(3 * SR))
mix = load(IN); n = min(len(mix), N); out = mix[:n] + bed[:n]
pk = np.abs(out).max(); out = out / pk * 0.97 if pk > 0.97 else out
out.tofile(f'{M}/out/_mix.f32')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', IN, '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', f'{M}/out/_mix.f32', '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', OUT], check=True)
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
sec = np.array([db(bed[i * SR:(i + 1) * SR]) for i in range(int(total) - 3)])
print('bed per second: median %.1f dB, quietest %.1f dB at %d s, loudest %.1f dB at %d s' % (np.median(sec), sec[2:].min(), 2 + sec[2:].argmin(), sec.max(), sec.argmax()))
for t0, trk, off in starts[1:]:
    i = int(t0); print(f'change at {i // 60}:{i % 60:02d} -> {trk}: ' + ' '.join('%.0f' % v for v in sec[i - 4:i + 5]))
print('seconds under -42 dB:', [int(i) for i in np.nonzero(sec[2:] < -42)[0] + 2]); print('wrote', OUT)
