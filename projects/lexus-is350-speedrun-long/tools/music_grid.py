"""Measure the real beat grid of a stretch of mix_full.wav (lessons [pacing]: kick attacks, not `ive beats`).

    python music_grid.py <mix_in> <mix_out> <bpm_guess> [--json out.json]

Kick band 35-110 Hz (zero-phase sosfiltfilt), 1 ms RMS envelope, attack = last sample below 30 % of the local
peak inside 80 ms before it. Fits t = t0 + n*period by iterative least squares on attacks within +-period/4 of the
grid, prints residual, on-grid ratio and the per-phase (beat mod 4) accent strength, so beat 1 is the strongest
phase rather than an assumption. Used by assemble_long.py (import measure()).
"""
from __future__ import annotations

import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, find_peaks, sosfiltfilt

MIX = "/home/user/media/work/is350-long/music/mix_full.wav"
_cache: dict = {}


def _mix():
    if "a" not in _cache:
        sr, a = wavfile.read(MIX, mmap=True)
        _cache["a"], _cache["sr"] = a, sr
    return _cache["a"], _cache["sr"]


def envelope(t0: float, t1: float, lo=35.0, hi=110.0):
    a, sr = _mix()
    i0, i1 = max(0, int((t0 - 0.5) * sr)), min(len(a), int((t1 + 0.5) * sr))
    x = a[i0:i1].astype(np.float32).mean(axis=1) / 32768.0
    if lo is not None:
        x = sosfiltfilt(butter(4, [lo, hi], btype="band", fs=sr, output="sos"), x)
    n = sr // 1000
    env = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, "same"))
    return env, sr, i0 / sr


def attacks(t0, t1, period, band=(35.0, 110.0)):
    env, sr, off = envelope(t0, t1, *band)
    pk, pr = find_peaks(env, distance=int(0.55 * period * sr), prominence=env.max() * 0.05)
    out = []
    for p in pk:
        a0 = max(0, p - int(0.08 * sr))
        seg = env[a0:p + 1]
        below = np.where(seg < 0.3 * env[p])[0]
        i = a0 + (below[-1] + 1 if len(below) else 0)
        t = off + i / sr
        if t0 <= t <= t1:
            out.append((t, float(env[p])))
    return out


def measure(t0: float, t1: float, bpm: float, band=(35.0, 110.0)) -> dict:
    period = 60.0 / bpm
    at = attacks(t0, t1, period, band)
    ts = np.array([a[0] for a in at]); st = np.array([a[1] for a in at])
    if len(ts) < 4:
        return {"ok": False, "n": len(ts)}
    # initial phase: circular mean of attacks modulo period, weighted by strength
    ph = np.angle(np.sum(st * np.exp(2j * np.pi * (ts - t0) / period))) / (2 * np.pi) * period
    g0 = t0 + (ph % period)
    for _ in range(6):
        n = np.round((ts - g0) / period)
        r = ts - (g0 + n * period)
        m = np.abs(r) < period / 4
        if m.sum() < 4:
            break
        A = np.c_[np.ones(m.sum()), n[m]]
        sol, *_ = np.linalg.lstsq(A, ts[m], rcond=None)
        g0, period = float(sol[0]), float(sol[1])
    n = np.round((ts - g0) / period); r = ts - (g0 + n * period); m = np.abs(r) < period / 4
    # accent per phase (beat index mod 4), strength of on-grid attacks
    acc = [float(st[m & (n % 4 == k)].sum()) for k in range(4)]
    k1 = int(np.argmax(acc))
    return {"ok": True, "t_first": g0, "period": period, "bpm": 60 / period, "n_attacks": int(len(ts)),
            "on_grid": float(m.mean()), "resid_ms": float(np.sqrt(np.mean(r[m] ** 2)) * 1000),
            "accent_by_phase": [round(x / max(acc), 3) for x in acc], "downbeat_phase": k1,
            "attacks": [round(float(x), 4) for x in ts[m]], "strength": [round(float(x), 5) for x in st[m]]}


def nearest_attack(t: float, measured: dict, win: float) -> float | None:
    ts = np.array(measured.get("attacks", []))
    if not len(ts):
        return None
    i = int(np.argmin(np.abs(ts - t)))
    return float(ts[i]) if abs(ts[i] - t) <= win else None


if __name__ == "__main__":
    t0, t1, bpm = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    r = measure(t0, t1, bpm)
    show = {k: v for k, v in r.items() if k not in ("attacks", "strength")}
    print(json.dumps(show, indent=1))
    if "--json" in sys.argv:
        json.dump(r, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
