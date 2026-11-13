"""Soundtrack for the wing-configurator reel: generated track (from MUSIC_IN) + the consented custom-voice narration.
Voice processing = huracan-evo tools/mix.py main_v6 (user-approved): pauses > 0.32 s trimmed (tighten, TEMPO 1.0, no
atempo, no pitch), HPF 90 Hz, comp -20 dB 3:1 8/120 ms +3, aecho 0.85:0.5:38|71:0.18|0.10, volume 2.4, alimiter 0.8;
music ducked -9 dB under the voice (0.6 s ramps); final alimiter 0.89 (level=disabled).
  python mix.py OUT.wav"""
import subprocess, sys
sys.path.insert(0, '/home/user/illumaesthetic-video-editor/projects/huracan-evo/tools')
import mix as hmix

M = '/home/user/media/epsilon-wing-configurator/'
MUSIC = M + 'music/ewc_track.mp3'
MUSIC_IN = 13.5          # track time at video 0: drop (16.07) -> 2.57 s, last hit (71.95) -> 58.45 s
VO_RAW = M + 'vo/narration1.wav'
VO_AT = 0.5
LENGTH = 58.9
FADE = 0.8
DUCK_DB, RAMP = -9.0, 0.6

def main(out):
    hmix.TEMPO = 1.0
    tight = VO_RAW.replace('.wav', '_tight.wav'); n = hmix.tighten(VO_RAW, tight)
    g = 10 ** (DUCK_DB / 20); d0, d1 = VO_AT - RAMP, VO_AT + n + 0.2
    print('voice', round(n, 2), 's:', VO_AT, '->', round(VO_AT + n, 2))
    d0 = max(d0, 0.0)
    env = (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
           f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    vchain = ("aresample=48000,highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
              "aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled")
    va = int(VO_AT * 1000)
    fc = (f"[0:a]atrim=start={MUSIC_IN},asetpts=PTS-STARTPTS,aresample=48000,volume='{env}':eval=frame[m];"
          f"[1:a]{vchain},adelay={va}|{va}[v];"
          f"[m][v]amix=inputs=2:normalize=0:duration=first,atrim=end={LENGTH},afade=t=out:st={LENGTH - FADE}:d={FADE},"
          f"alimiter=limit=0.89:level=disabled[out]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', MUSIC, '-i', tight, '-filter_complex', fc, '-map', '[out]',
                    '-c:a', 'pcm_s24le', out], check=True)
    print(out)



# ---- v2 (user on v1): drop "Car not listed? Add it from a blueprint, or your own photos." (tight take 48.07-52.12, inside
# the pauses either side), add "Try it now, on epsilon dot plus." (same voice/settings, line_try.wav) on the logo card.
V2 = dict(CUT=(48.07, 52.12), LINE=M + 'vo/line_try.wav', LINE_AT=55.45, LENGTH=58.9,
          # v4 (user): car line replaced, same start (tight 8.14 = video 8.64), padded to the old length (region 8.00-13.29
          # lies inside the pauses either side), so nothing after it moves
          CARS=dict(file=M + 'vo/line_cars.wav', region=(8.00, 13.29), at=8.14))

def main_v2(out):
    import numpy as np
    hmix.TEMPO = 1.0
    tight = VO_RAW.replace('.wav', '_tight.wav'); hmix.tighten(VO_RAW, tight)
    lt = V2['LINE'].replace('.wav', '_tight.wav'); nl = hmix.tighten(V2['LINE'], lt)
    sr = 48000
    rd = lambda f: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'],
                                                capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    x = rd(tight)
    if V2.get('CARS') and '--v4' in sys.argv:
        cr = V2['CARS']; ct = cr['file'].replace('.wav', '_tight.wav'); hmix.tighten(cr['file'], ct); y = rd(ct)
        e = np.sqrt(np.convolve(y.mean(1) ** 2, np.ones(1440) / 1440, 'same')); on = np.flatnonzero(e > 0.06 * e.max())
        y = y[max(0, on[0] - int(0.02 * sr)):on[-1] + int(0.1 * sr)]
        r0, r1 = (int(t * sr) for t in cr['region']); at = int(cr['at'] * sr)
        assert at + len(y) < r1, 'new car line longer than the old one'
        x = x.copy(); x[r0:r1] = 0; x[at:at + len(y)] = y
        print('car line', round(len(y) / sr, 2), 's at tight', cr['at'])
    a, b = (int(t * sr) for t in V2['CUT']); xf = int(0.01 * sr)
    seg = x[b:].copy(); r = np.linspace(0, 1, xf)[:, None]
    head = x[:a].copy(); head[-xf:] = head[-xf:] * (1 - r) + seg[:xf] * r
    vo = np.concatenate([head, seg[xf:]])
    n1 = len(vo) / sr
    line = rd(lt); at = int((V2['LINE_AT'] - VO_AT) * sr)
    full = np.zeros((max(at + len(line), len(vo)), 2), np.float32); full[:len(vo)] = vo; full[at:at + len(line)] += line
    vo_path = M + 'vo/narration_v2.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '2', '-i', '-', vo_path], input=full.tobytes(), check=True)
    w1 = (VO_AT, VO_AT + n1); w2 = (V2['LINE_AT'], V2['LINE_AT'] + nl)
    print('voice block 1', [round(t, 2) for t in w1], 'line', [round(t, 2) for t in w2])
    g = 10 ** (DUCK_DB / 20)
    def trap(d0, d1):
        d0 = max(d0, 0.0)
        return (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
                f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    env = f"({trap(w1[0] - RAMP, w1[1] + 0.2)})*({trap(w2[0] - RAMP, w2[1] + 0.2)})"
    vchain = ("aresample=48000,highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
              "aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled")
    va = int(VO_AT * 1000); L = V2['LENGTH']
    fc = (f"[0:a]atrim=start={MUSIC_IN},asetpts=PTS-STARTPTS,aresample=48000,volume='{env}':eval=frame[m];"
          f"[1:a]{vchain},adelay={va}|{va}[v];"
          f"[m][v]amix=inputs=2:normalize=0:duration=first,atrim=end={L},afade=t=out:st={L - FADE}:d={FADE},"
          f"alimiter=limit=0.89:level=disabled[out]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', MUSIC, '-i', vo_path, '-filter_complex', fc, '-map', '[out]',
                    '-c:a', 'pcm_s24le', out], check=True)
    print(out)


if __name__ == '__main__':
    (main_v2 if ('--v2' in sys.argv or '--v4' in sys.argv) else main)(sys.argv[1])
