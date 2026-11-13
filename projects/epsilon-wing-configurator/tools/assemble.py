"""Assemble the reel: exact-frame concat of the composed clips (cuts at round(t*30) on the kick grid), logo card,
soundtrack. Plain concat = hard cuts with no duplicated/dropped frames (honda-s2000 lesson).
  python assemble.py OUT.mp4"""
import subprocess, sys
M = '/home/user/media/epsilon-wing-configurator/'
CUTS = [0, 4.07, 8.57, 14.07, 18.07, 24.07, 26.07, 29.07, 30.57, 35.57, 38.57, 43.07, 48.57, 52.57, 55.57]  # planned grid
# v1 cut frames = round(30 * measured kick attack) on the decoded track (40-120 Hz half-rise; grid read ~20 ms early;
# 18.07 and 48.57 fall in drum fills -> nearest real hit 18.003 / 48.71)
CUT_FRAMES = [0, 123, 258, 423, 540, 722, 783, 873, 917, 1067, 1157, 1293, 1461, 1578, 1667]
SHOTS = ['hero_a', 'hero_b', 'cars', 'wing', 'mounts', 'bases', 'aoa', 'turn3d', 'side', 'rear', 'sliders',
         'price', 'more', 'outro']
END = 58.9
FPS = 30
PUSH = {'cars', 'wing', 'mounts', 'bases', 'aoa', 'side', 'rear', 'sliders', 'price', 'more', 'hero_b'}  # UI holds: slow 5 % push-in (director: dead frames)
PUSH_AMT = 0.05

# v2 (user on v1): 'more options' removed, customer photos before the card, 'try it now on epsilon.plus' card + line.
# Cut frames: price ends 1461 as v1; outro to the kick at 51.597 (1548); photos on kicks 52.598/53.598/54.579/55.597.
V2 = dict(SHOTS=['hero_a', 'hero_b', 'cars', 'wing', 'mounts', 'bases', 'aoa', 'turn3d', 'side', 'rear', 'sliders',
                 'price', 'outro', 'ph1', 'ph2', 'ph3', 'ph4'],
          CUT_FRAMES=[0, 123, 258, 423, 540, 722, 783, 873, 918, 1067, 1157, 1293, 1461, 1547, 1578, 1608, 1637, 1667],
          CARD='work/logo_card_v2.png', AUDIO='work/soundtrack_v2.wav')


def main(out, audio=M + 'work/soundtrack_v1.wav', card='work/logo_card.png'):
    fr = CUT_FRAMES + [round(END * FPS)]
    ins, parts = [], []
    for i, s in enumerate(SHOTS):
        n = fr[i + 1] - fr[i]
        ins += ['-i', M + f'clips/{s}.mp4']
        push = ''
        if s in PUSH:  # centre push-in: per-frame scale up (from 2x) + fixed centre crop
            D = n / FPS
            z = f"(1+{PUSH_AMT}*t/{D})"
            push = (f",scale=w='trunc(2160*{z}/2)*2':h='trunc(3840*{z}/2)*2':eval=frame:flags=lanczos,"
                    f"crop=2160:3840:'(iw-2160)/2':'(ih-3840)/2',scale=1080:1920:flags=lanczos")
        parts.append(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,fps={FPS}{push},format=yuv420p[v{i}]')
    k = len(SHOTS); nlogo = fr[-1] - fr[-2]
    ins += ['-loop', '1', '-framerate', str(FPS), '-i', M + card]
    parts.append(f'[{k}:v]trim=end_frame={nlogo},setpts=PTS-STARTPTS,format=yuv420p,'
                 f'fade=t=in:st=0:d=0.35,fade=t=out:st={nlogo / FPS - 0.8}:d=0.8[v{k}]')
    fc = ';'.join(parts) + ';' + ''.join(f'[v{i}]' for i in range(k + 1)) + f'concat=n={k + 1}:v=1:a=0[v]'
    ins += ['-i', audio]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[v]', '-map', f'{k + 1}:a',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', out], check=True)
    print(out, 'cut frames', fr)

if __name__ == '__main__':
    if '--v2' in sys.argv:
        SHOTS[:] = V2['SHOTS']; CUT_FRAMES[:] = V2['CUT_FRAMES']
        main(sys.argv[1], M + V2['AUDIO'], V2['CARD'])
    else:
        main(sys.argv[1])
