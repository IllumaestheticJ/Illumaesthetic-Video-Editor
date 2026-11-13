"""Premix the Huracan soundtrack: car-select intro (engine roar + female narrator, Hot Pursuit-style car-select
homage, original script/voice) over reel_track_a, music ducked under the voice. Output is set as project music.

  python projects/huracan-evo/tools/mix.py OUT.wav
Stems (not in git, see clips.md): music = reel_track_a.mp3; engine.mp3 (Higgsfield Mirelo SFX, generated);
narration4.wav (Higgsfield Seed Audio, preset voice 'Imogen' - NOT a clone of the game's narrator), car-only script.
"""
import subprocess
import sys

# v3 (user's Hot Pursuit Remastered car-select clip, NOT the NFSU2 one first used): engine start-up on the select, ~3 s
# hush, then one continuous descriptive narration about the COUPE over the track's pads (extended 8 bars); the Spyder
# arrives on the music lift with a second start-up. Music = track_a_hp.wav (3 s lead-in + pads +32 beats + groove +16).
MUSIC = "/home/user/media/huracan-evo/music/track_a_hp.wav"
ENGINE = "/home/user/media/huracan-evo/vo/engine_start1.mp3"      # coupe selected
ENGINE_AT = 0.3
ENGINE2 = "/home/user/media/huracan-evo/vo/engine_start2.mp3"     # Spyder arrives: catch lands on the lift
ENGINE2_AT = 41.48 - 0.25
VO_RAW = "/home/user/media/huracan-evo/vo/narration6.wav"   # HP-style descriptive script about the coupe
VO = "/home/user/media/huracan-evo/vo/narration6_tight.wav"
VO_AT = 3.9          # file has 0.42 s lead-in -> speech from ~4.3 s, after the start-up settles (ref: 5-8 s hush)
GAP_KEEP = 0.32      # s: pauses trimmed to this
TEMPO = 1.04         # ref narrator is quicker (4.1 vs 2.9 voiced onsets/s) but still measured
DUCK_DB = -9.0       # music under the voice
RAMP = 0.6
LIFT = 41.48         # music lift (Spyder arrives) - voice must be done and music back to full by here


def tighten(src, dst):
    """Trim pauses longer than GAP_KEEP to GAP_KEEP (cut in the middle of the silence, 10 ms crossfade), then atempo."""
    import numpy as np
    sr = 48000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    m = x.mean(1); w = int(0.03 * sr)
    e = np.sqrt(np.convolve(m ** 2, np.ones(w) / w, "same")); on = e > 0.06 * e.max()
    idx = np.flatnonzero(np.diff(on.astype(int)))  # transitions
    keep, last = [], 0
    starts = [i for i in idx if not on[i]]          # silence -> speech
    ends = [i for i in idx if on[i]]                # speech -> silence
    for a in ends:
        b = next((s_ for s_ in starts if s_ > a), None)
        if b is None or (b - a) / sr <= GAP_KEEP:
            continue
        h = int(GAP_KEEP / 2 * sr)
        keep.append((last, a + h)); last = b - h
    keep.append((last, len(x)))
    xf = int(0.01 * sr); out = x[keep[0][0]:keep[0][1]].copy()
    for a, b in keep[1:]:
        seg = x[a:b].copy(); r = np.linspace(0, 1, xf)[:, None]
        out[-xf:] = out[-xf:] * (1 - r) + seg[:xf] * r; out = np.concatenate([out, seg[xf:]])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                    "-af", f"atempo={TEMPO}", dst], input=out.astype(np.float32).tobytes(), check=True)
    n = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                             capture_output=True, text=True).stdout)
    return n


def main(out):
    VO_LEN = tighten(VO_RAW, VO)
    print("voice", round(VO_LEN, 2), "s, ends at", round(VO_AT + VO_LEN, 2))
    d0, d1 = VO_AT - RAMP, VO_AT + VO_LEN + 0.2
    g = 10 ** (DUCK_DB / 20)
    assert d1 + RAMP < LIFT, "voice runs into the lift"
    # piecewise-linear duck envelope as an ffmpeg volume expression (eval per frame)
    env = (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
           f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    fc = (
        f"[0:a]aresample=48000,volume='{env}':eval=frame[m];"
        # engine: full at the 'select', then tucks under the first line
        f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.9,afade=t=out:st=2.4:d=3.0,"
        f"adelay={int(ENGINE_AT * 1000)}|{int(ENGINE_AT * 1000)}[e1];"
        f"[3:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.75,afade=t=out:st=1.6:d=2.4,"
        f"adelay={int(ENGINE2_AT * 1000)}|{int(ENGINE2_AT * 1000)}[e2];"
        f"[e1][e2]amix=inputs=2:normalize=0:duration=longest[e];"
        # voice: clean announcer chain - HPF, gentle comp, short room
        f"[2:a]aresample=48000,highpass=f=110,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
        f"aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled,adelay={int(VO_AT * 1000)}|{int(VO_AT * 1000)}[v];"
        f"[m][e][v]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95:level=disabled[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-i", ENGINE, "-i", VO, "-i", ENGINE2, "-filter_complex", fc,
                    "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


# v4 (user on v3: opening pans too long; voice closer to the reference; Spyder shown -> talk about the Spyder; imperial;
# faster; quirks not just specs). Music = track_a_v4.wav (tools/music_v4.py): lift n40 = 27.079 s, stop n84 = 53.48 s.
# Voice = preset 'Vesper' (c3204739-...), speech_rate 45, pitch_rate +2: closest preset to the reference narrator by
# tools/voicematch.py (timbre 1.7 dB LTAS distance, F0 -0.4 st, pace 4.14 vs 4.12 onsets/s). Still NOT a clone.
V4 = dict(MUSIC="/home/user/media/huracan-evo/music/track_a_v4.wav", LIFT=27.079,
          VOS=[("/home/user/media/huracan-evo/vo/narration7_coupe.wav", 3.6),     # coupe, ends before the lift
               ("/home/user/media/huracan-evo/vo/narration7_spyder.wav", 28.6)],  # Spyder, after the 2nd start-up catches
          TEMPO=1.05)   # take already matched the ref pace; +5 % so the coupe block ends before the lift (user: "speak faster")


def main_v4(out):
    global TEMPO
    TEMPO = V4["TEMPO"]; g = 10 ** (DUCK_DB / 20)
    vos, wins = [], []
    for i, (raw, at) in enumerate(V4["VOS"]):
        tight = raw.replace(".wav", "_tight.wav"); n = tighten(raw, tight); vos.append((tight, at))
        wins.append((at - RAMP, at + n + 0.2)); print("voice", i, round(n, 2), "s:", at, "->", round(at + n, 2))
    assert wins[0][1] + RAMP < V4["LIFT"], "coupe voice runs into the lift"
    # duck envelope: product of per-window trapezoids
    def trap(d0, d1):
        return (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
                f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    env = "*".join(f"({trap(a, b)})" for a, b in wins)
    e2 = V4["LIFT"] - 0.25
    vchain = ("aresample=48000,highpass=f=110,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
              "aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled")
    fc = (f"[0:a]aresample=48000,volume='{env}':eval=frame[m];"
          f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.9,afade=t=out:st=2.4:d=3.0,"
          f"adelay={int(ENGINE_AT * 1000)}|{int(ENGINE_AT * 1000)}[e1];"
          f"[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.75,afade=t=out:st=1.6:d=2.4,"
          f"adelay={int(e2 * 1000)}|{int(e2 * 1000)}[e2];"
          f"[3:a]{vchain},adelay={int(vos[0][1] * 1000)}|{int(vos[0][1] * 1000)}[v1];"
          f"[4:a]{vchain},adelay={int(vos[1][1] * 1000)}|{int(vos[1][1] * 1000)}[v2];"
          f"[m][e1][e2][v1][v2]amix=inputs=5:normalize=0:duration=first,alimiter=limit=0.95:level=disabled[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V4["MUSIC"], "-i", ENGINE, "-i", ENGINE2, "-i", vos[0][0], "-i", vos[1][0],
                    "-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


# v5 (user on v4: 30 s total, scan data sooner; engine start = the reference clip's exactly; voice still too high; "why is
# there a fighter jet sound" = the generated engine_start2 at the lift (energy 57 % 200-1k Hz, 26 % 1-4 kHz: a whine) -> removed).
# Engine: hp_1138.mp4 1.70-6.60 s (the game's Gallardo start-up on the select screen), unprocessed, at 0.3 s.
# NOTE: that is game audio from the user's own screen recording - flagged to the user (rights), used as asked.
# Voice: Vesper pitch_rate -3 (F0 ~136 Hz, ~5 st under the ref narrator; same intonation spread), speech_rate 60.
V5 = dict(MUSIC="/home/user/media/huracan-evo/music/track_a_v5.wav", LIFT=10.278,
          ENGINE="/home/user/media/huracan-evo/vo/engine_ref.wav", ENGINE_AT=0.3,
          VOS=[("/home/user/media/huracan-evo/vo/narration8_coupe.wav", 3.0, 1.15),
               ("/home/user/media/huracan-evo/vo/narration8_spyder.wav", 10.6, 1.0)])


def main_v5(out):
    global TEMPO
    g = 10 ** (DUCK_DB / 20); vos, wins = [], []
    for raw, at, tempo in V5["VOS"]:
        TEMPO = tempo; tight = raw.replace(".wav", "_tight.wav"); n = tighten(raw, tight); vos.append((tight, at))
        wins.append((at - RAMP, at + n + 0.2)); print("voice", raw.split("/")[-1], round(n, 2), "s:", at, "->", round(at + n, 2))
    assert wins[0][1] - 0.2 <= V5["LIFT"] + 0.05, "coupe voice runs past the lift"
    assert wins[1][1] < 27.0, "Spyder voice runs into the music stop"
    def trap(d0, d1):
        return (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
                f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    env = f"({trap(wins[0][0], wins[1][1])})"          # one continuous duck: voice blocks are 0.5 s apart
    vchain = ("aresample=48000,highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
              "aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled")
    ea = int(V5["ENGINE_AT"] * 1000)
    fc = (f"[0:a]aresample=48000,volume='{env}':eval=frame[m];"
          f"[1:a]aresample=48000,adelay={ea}|{ea}[e];"           # reference start-up exactly (no EQ/fade beyond its own tail)
          f"[2:a]{vchain},adelay={int(vos[0][1] * 1000)}|{int(vos[0][1] * 1000)}[v1];"
          f"[3:a]{vchain},adelay={int(vos[1][1] * 1000)}|{int(vos[1][1] * 1000)}[v2];"
          f"[m][e][v1][v2]amix=inputs=4:normalize=0:duration=first,alimiter=limit=0.89:level=disabled[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V5["MUSIC"], "-i", V5["ENGINE"], "-i", vos[0][0], "-i", vos[1][0],
                    "-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


# v6: ONE speech about the EVO (user), in the consented custom voice (clips.md "v6 voice"), natural pitch and pace: no
# pitch_rate, no atempo; only pauses > GAP_KEEP trimmed. Same music/engine as v5.
V6 = dict(VO="/home/user/media/huracan-evo/vo/narration9.wav", AT=3.0, LAST=26.9)


def main_v6(out):
    global TEMPO
    TEMPO = 1.0; g = 10 ** (DUCK_DB / 20)
    tight = V6["VO"].replace(".wav", "_tight.wav"); n = tighten(V6["VO"], tight)
    d0, d1 = V6["AT"] - RAMP, V6["AT"] + n + 0.2
    print("voice", round(n, 2), "s:", V6["AT"], "->", round(V6["AT"] + n, 2))
    assert V6["AT"] + n <= V6["LAST"], "speech runs into the logo"
    env = (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
           f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    vchain = ("aresample=48000,highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
              "aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled")
    ea = int(V5["ENGINE_AT"] * 1000); va = int(V6["AT"] * 1000)
    fc = (f"[0:a]aresample=48000,volume='{env}':eval=frame[m];[1:a]aresample=48000,adelay={ea}|{ea}[e];"
          f"[2:a]{vchain},adelay={va}|{va}[v];[m][e][v]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=disabled[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V5["MUSIC"], "-i", V5["ENGINE"], "-i", tight, "-filter_complex", fc,
                    "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


# v7: same voice/settings; script ends on a conclusion (user: "it needs a conclusion for the end of the video"):
# "...Named after a fighting bull, and built like one. This is the Huracan EVO." - last line lands on the logo (27.08 s).
def main_v7(out):
    V6.update(VO="/home/user/media/huracan-evo/vo/narration11.wav", LAST=29.2)
    main_v6(out)


# v8 (user on v7: "the voice at the end feels patched on - needs to be re-flowed"): the script was rewritten as flowing sentences
# with the conclusion as its last sentence, generated as ONE take and used UNTRIMMED (no pause cuts, no tempo); it ends at
# ~26.6 s, before the music stop, instead of running over the logo after the music had gone.
def main_v8(out):
    global GAP_KEEP
    GAP_KEEP = 9.0
    V6.update(VO="/home/user/media/huracan-evo/vo/narration12_r5.wav", LAST=26.95)
    main_v6(out)


# v9 (user on v8: "the narration is shallow at best, include some ball knowledge"): enthusiast script - odd-firing V10 (54/90
# degree intervals), titanium intake valves, LDVI + four-wheel steering, successor went twin-turbo hybrid. One take
# (speech_rate 8), untrimmed, no tempo/pitch change. Longer drafts ran 32-34 s -> script shortened, voice not sped up.
def main_v9(out):
    global GAP_KEEP
    GAP_KEEP = 9.0
    V6.update(VO="/home/user/media/huracan-evo/vo/narration14_short_r8.wav", LAST=27.0)
    main_v6(out)


# v10 (user: may run longer than 30 s for pacing): music = track_a_v10.wav (stop n56 = 36.68 s); with the extra room the
# fuller enthusiast script is used (the 31.8 s one-take draft that did not fit v9): adds the 5.2 l, port + direct injection
# and the 8,000 rpm peak. Untrimmed, no tempo/pitch change; speech 3.2 -> 34.6 s.
def main_v10(out):
    global GAP_KEEP
    GAP_KEEP = 9.0
    V5["MUSIC"] = "/home/user/media/huracan-evo/music/track_a_v10.wav"
    V6.update(VO="/home/user/media/huracan-evo/vo/narration13_r12.wav", LAST=36.2)
    main_v6(out)


# v11 (user: the car must be named "LP640-4 Evo, representing the 640 metric horsepower it produces, mated to a 4-wheel drive
# system"): new one-take script opening with that line; the separate 631 hp figure is dropped (640 metric hp = 631 hp, said once).
def main_v11(out):
    global GAP_KEEP
    GAP_KEEP = 9.0
    V5["MUSIC"] = "/home/user/media/huracan-evo/music/track_a_v10.wav"
    V6.update(VO="/home/user/media/huracan-evo/vo/narration15_r12.wav", LAST=36.2)
    main_v6(out)


# v12 (user: "don't drop the huracan"; replace the successor/last-NA ending with how the EVO improves on the previous
# generation): one take - "Lamborghini Huracan LP640-4 EVO ..." ending on +30 hp, rear-wheel steering, >5x downforce, 0-62 3.2 -> 2.9 s.
def main_v12(out):
    global GAP_KEEP
    GAP_KEEP = 9.0
    V5["MUSIC"] = "/home/user/media/huracan-evo/music/track_a_v10.wav"
    V6.update(VO="/home/user/media/huracan-evo/vo/narration16_r12.wav", LAST=36.2)
    main_v6(out)


if __name__ == "__main__":
    {"--v12": main_v12, "--v11": main_v11, "--v4": main_v4, "--v5": main_v5, "--v6": main_v6, "--v7": main_v7, "--v8": main_v8, "--v9": main_v9, "--v10": main_v10}.get(next((a for a in sys.argv if a.startswith("--v")), ""), main)(sys.argv[1])
