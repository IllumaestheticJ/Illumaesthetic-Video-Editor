"""Premix the Huracan soundtrack: car-select intro (engine roar + female narrator, Hot Pursuit-style car-select
homage, original script/voice) over reel_track_a, music ducked under the voice. Output is set as project music.

  python projects/huracan-evo/tools/mix.py OUT.wav
Stems (not in git, see clips.md): music = reel_track_a.mp3; engine.mp3 (Higgsfield Mirelo SFX, generated);
narration2.wav (Higgsfield Seed Audio, preset voice 'Imogen' - NOT a clone of the game's narrator).
"""
import subprocess
import sys

MUSIC = "/home/user/media/work/music/reel_track_a.mp3"
ENGINE = "/home/user/media/huracan-evo/vo/engine.mp3"
VO = "/home/user/media/huracan-evo/vo/narration2.wav"
VO_AT = 1.8          # s: voice enters as the roar settles (picture fades up 0-1.2 s)
VO_LEN = 16.1        # measured
DUCK_DB = -9.0       # music under the voice
RAMP = 0.6
LIFT = 19.279        # music lift / explode start - voice must be done and music back to full by here


def main(out):
    d0, d1 = VO_AT - RAMP, VO_AT + VO_LEN + 0.2
    g = 10 ** (DUCK_DB / 20)
    assert d1 + RAMP < LIFT, "voice runs into the lift"
    # piecewise-linear duck envelope as an ffmpeg volume expression (eval per frame)
    env = (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
           f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    fc = (
        f"[0:a]aresample=48000,volume='{env}':eval=frame[m];"
        # engine: full at the 'select', then tucks under the first line
        f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.9,afade=t=out:st=2.6:d=2.6[e];"
        # voice: clean announcer chain - HPF, gentle comp, short room
        f"[2:a]aresample=48000,highpass=f=110,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
        f"aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled,adelay={int(VO_AT * 1000)}|{int(VO_AT * 1000)}[v];"
        f"[m][e][v]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95:level=disabled[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-i", ENGINE, "-i", VO, "-filter_complex", fc,
                    "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
