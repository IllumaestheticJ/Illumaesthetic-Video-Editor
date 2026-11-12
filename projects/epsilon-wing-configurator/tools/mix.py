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

if __name__ == '__main__':
    main(sys.argv[1])
