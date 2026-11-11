"""Build a 3D .cube LUT: Sony S-Log3 / S-Gamut3.Cine (FX30, legal-range video) -> Rec.709 display.

ffmpeg's lut3d receives RGB decoded from tv-range YUV (code 64 -> 0.0, 940 -> 1.0), so we first
recover the 10-bit code value, then apply Sony's S-Log3 inverse, the S-Gamut3.Cine->Rec709
matrix, an exposure gain, a Hable filmic shoulder and the Rec.709 OETF.

    python tools/slog3_lut.py out.cube [--exposure 1.0] [--sat 1.0]
"""
import argparse
import numpy as np

M = np.array([[1.6269474, -0.5401385, -0.0868089],
              [-0.1785155, 1.4179409, -0.2394254],
              [0.0444361, -0.1959116, 1.1514755]])


def slog3_to_lin(code):  # code = 10-bit code value / 1023
    cv = code * 1023.0
    hi = (10 ** ((cv - 420.0) / 261.5)) * (0.18 + 0.01) - 0.01
    lo = (cv - 95.0) * 0.01125 / (171.2102946929 - 95.0)
    return np.where(cv >= 171.2102946929, hi, lo)


def hable(x):
    A, B, C, D, E, F = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30
    return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F


def rec709_oetf(l):
    l = np.clip(l, 0, 1)
    return np.where(l < 0.018, 4.5 * l, 1.099 * l ** 0.45 - 0.099)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=33)
    ap.add_argument("--exposure", type=float, default=1.0)
    ap.add_argument("--sat", type=float, default=1.0)
    a = ap.parse_args()
    n = a.size
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # cube order: r fastest
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    code = (rgb * 876.0 + 64.0) / 1023.0
    lin = slog3_to_lin(code) @ M.T
    lin = np.maximum(lin, 0) * a.exposure
    W = 6.0
    disp = hable(lin * 2.0) / hable(W)  # 2.0 = exposure bias so mid grey lands ~0.42 after OETF
    out = rec709_oetf(disp)
    if a.sat != 1.0:
        y = out @ np.array([0.2126, 0.7152, 0.0722])
        out = y[:, None] + (out - y[:, None]) * a.sat
    out = np.clip(out, 0, 1)
    with open(a.out, "w") as f:
        f.write(f"TITLE \"slog3_to_709\"\nLUT_3D_SIZE {n}\n")
        for v in out:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    mid = rec709_oetf(hable(np.array([0.18 * a.exposure * 2.0])) / hable(W))
    print(a.out, "mid grey ->", float(mid[0]))


if __name__ == "__main__":
    main()
