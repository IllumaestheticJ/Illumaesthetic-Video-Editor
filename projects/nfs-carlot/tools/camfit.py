"""Camera JSON for the car-lot menu from fitted parameters, and an onion overlay to check it.

    python projects/nfs-carlot/tools/camfit.py <name> <f_px> <az> <el> <d> <up> <yaw> <o> [glb hide paint frame car_mid_y]

Parameters are those of the wheel fit (see editlog): az/el/d = where the camera sits around the turntable
centre, up/yaw = how far its axis is tilted off that centre, o = how far forward of the centre the game
parks a car's wheelbase midpoint. `car_mid_y` is the wheelbase midpoint of the GLB in its own frame.
"""
import json, math, subprocess, sys
import cv2, numpy as np
W = '/home/user/media/work/nfs-carlot'
REPO = '/home/user/Illumaesthetic-Video-Editor'


def write_cam(name, f, az, el, d, up, yaw, o, car_mid_y=0.0, size=(2144, 1206)):
    a = math.radians(az); e = math.radians(el); h = d * math.cos(e)
    loc = np.array([h * math.sin(a), -h * math.cos(a), d * math.sin(e)])
    tgt = np.array([0, 0, loc[2] + h * math.tan(math.radians(up))])
    fwd = tgt - loc; fwd /= np.linalg.norm(fwd); right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
    y = math.radians(yaw); fwd = fwd * math.cos(y) + right * math.sin(y); fwd /= np.linalg.norm(fwd)
    shift = np.array([0, car_mid_y - o, 0])          # the car stays at its GLB origin; move the camera instead
    loc = loc + shift; T = loc + fwd * 8
    focal = 36 * f / size[0]
    out = f'{W}/match/{name}.json'
    subprocess.run(['python', '-m', 'ive', 'lookat', out, '--loc=' + ','.join(f'{v:.4f}' for v in loc), '--target=' + ','.join(f'{v:.4f}' for v in T),
                    '--focal', f'{focal:.3f}', '--sensor', '36', '--size', f'{size[0]}x{size[1]}'], check=True, capture_output=True, cwd=REPO)
    return out


def onion(name, glb, hide, paint, frame, alpha=0.5):
    r = subprocess.run(['python', '-m', 'ive', 'kit-render', '--', '--glb', glb, '--hide', hide, '--paint', paint, '--camera', f'{W}/match/{name}.json',
                        '--res-pct', '50', '--samples', '8', '--ground', 'none', '--out', f'{W}/match/{name}.png'], capture_output=True, text=True, cwd=REPO)
    cap = cv2.VideoCapture(W + '/a60.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES, frame); ok, F = cap.read()
    bg = cv2.resize(F, (1072, 603)).astype(np.float32)
    im = cv2.imread(f'{W}/match/{name}.png', cv2.IMREAD_UNCHANGED).astype(np.float32)
    a = im[:, :, 3:] / 255
    edge = cv2.Canny((a[:, :, 0] * 255).astype(np.uint8), 50, 150)
    mix = bg * (1 - a * alpha) + im[:, :, :3] * a * alpha
    mix[edge > 0] = (0, 255, 255)
    return mix.astype(np.uint8)


if __name__ == '__main__':
    name = sys.argv[1]; f, az, el, d, up, yaw, o = [float(v) for v in sys.argv[2:9]]
    write_cam(name, f, az, el, d, up, yaw, o, float(sys.argv[13]) if len(sys.argv) > 13 else 0.0)
    if len(sys.argv) > 12:
        cv2.imwrite(f'{W}/match/{name}_onion.jpg', onion(name, sys.argv[9], sys.argv[10], sys.argv[11], int(sys.argv[12])))
