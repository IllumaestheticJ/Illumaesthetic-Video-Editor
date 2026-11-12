"""Assemble the reel: exact-frame concat of the composed clips (cuts at round(t*30) on the kick grid), logo card,
soundtrack. Plain concat = hard cuts with no duplicated/dropped frames (honda-s2000 lesson).
  python assemble.py OUT.mp4"""
import subprocess, sys
M = '/home/user/media/epsilon-wing-configurator/'
CUTS = [0, 4.07, 8.57, 14.07, 18.07, 24.07, 26.07, 29.07, 30.57, 35.57, 38.57, 43.07, 48.57, 52.57, 55.57]
SHOTS = ['hero_a', 'hero_b', 'cars', 'wing', 'mounts', 'bases', 'aoa', 'turn3d', 'side', 'rear', 'sliders',
         'price', 'more', 'outro']
END = 58.9
FPS = 30

def main(out, audio=M + 'work/soundtrack_v1.wav'):
    fr = [round(t * FPS) for t in CUTS] + [round(END * FPS)]
    ins, parts = [], []
    for i, s in enumerate(SHOTS):
        n = fr[i + 1] - fr[i]
        ins += ['-i', M + f'clips/{s}.mp4']
        parts.append(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v{i}]')
    k = len(SHOTS); nlogo = fr[-1] - fr[-2]
    ins += ['-loop', '1', '-framerate', str(FPS), '-i', M + 'work/logo_card.png']
    parts.append(f'[{k}:v]trim=end_frame={nlogo},setpts=PTS-STARTPTS,format=yuv420p,'
                 f'fade=t=in:st=0:d=0.35,fade=t=out:st={nlogo / FPS - 0.8}:d=0.8[v{k}]')
    fc = ';'.join(parts) + ';' + ''.join(f'[v{i}]' for i in range(k + 1)) + f'concat=n={k + 1}:v=1:a=0[v]'
    ins += ['-i', audio]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[v]', '-map', f'{k + 1}:a',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', out], check=True)
    print(out, 'cut frames', fr)

if __name__ == '__main__':
    main(sys.argv[1])
