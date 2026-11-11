"""S-Log3 / S-Gamut3.Cine -> Rec.709 display LUT (.cube) for the FX3A clips (XML: s-log3-cine).
Input is ffmpeg rgb after limited->full expansion, so code value cv10 = x*876+64.
Sony S-Log3 decode, S-Gamut3.Cine->709 matrix, exposure, Hable filmic tonemap, BT.709 OETF."""
import sys
import numpy as np
N = 33
exp = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
M = np.array([[1.6269474, -0.5401385, -0.0868089], [-0.1785155, 1.4179409, -0.2394254], [-0.0444361, -0.1959199, 1.2403560]])

def slog3_to_lin(x):
    cv = x * 876 + 64
    return np.where(cv >= 171.2102946929, (10 ** ((cv - 420) / 261.5)) * 0.19 - 0.01, (cv - 95) * 0.01125 / (171.2102946929 - 95))

def hable(x):
    A, B, C, D, E, F = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30
    return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F

def oetf(L):
    L = np.clip(L, 0, 1); return np.where(L < 0.018, 4.5 * L, 1.099 * L ** 0.45 - 0.099)

g = np.linspace(0, 1, N)
b, gg, r = np.meshgrid(g, g, g, indexing='ij')           # cube order: r fastest
rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
lin = slog3_to_lin(rgb) @ M.T
lin = np.maximum(lin, 0) * exp
W = 6.0
out = oetf(hable(lin * 2.0) / hable(W))
with open(sys.argv[1], 'w') as f:
    f.write(f'TITLE "MR2 FX3A SLog3Cine to 709"\nLUT_3D_SIZE {N}\n')
    for v in out: f.write('%.6f %.6f %.6f\n' % tuple(v))
