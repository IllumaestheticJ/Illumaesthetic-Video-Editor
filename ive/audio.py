"""Beat grid for cutting on the music (numpy only, no librosa)."""
from __future__ import annotations

import subprocess

import numpy as np


def beats(media: str, sr: int = 22050, hop: int = 512, z: float = 2.0) -> dict:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", media, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    win = 1024
    frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
    S = np.abs(np.fft.rfft(frames, axis=1))
    flux = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    t = np.arange(len(flux)) * hop / sr
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lags = np.arange(len(ac)) * hop / sr
    m = (lags > 0.3) & (lags < 1.0)
    period = float(lags[m][np.argmax(ac[m])])
    onsets = [round(float(t[i]), 3) for i in range(1, len(flux) - 1) if flux[i] > z and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
    return {"duration": round(len(x) / sr, 3), "beat_period_s": round(period, 3), "bpm": round(60 / period, 1),
            "strong_onsets": onsets,
            "hint": "cut on strong onsets; 4 beats ~ one shot in house style (see knowledge/style-guide.md)"}
