"""Paint a rough HDR panorama of the mod shop to light and reflect the car (Blender equirectangular mapping).

    python projects/gta6-customs/tools/make_env.py out.hdr

Car frame: Z up, nose at -Y, left = +X. What the capture shows of the room, by direction from the car:
  +Y (behind the car)  the open roll-up door: sky, trees, sunlit concrete. The tailgate of the game's car
                       mirrors exactly that in the rear view, and the floor's sun line runs behind its tail.
  -X/+Y (right rear)   teal block wall, white above a red stripe, grey lockers and door (menu view background).
  -Y (ahead)           workbench, red tool chests, dark (rear view background).
  -X (right)           yellow spray-booth doors (rear view, right side).
  above                dark ceiling with a few shop lights; below, grey concrete, sunlit near the door.
Colours are taken from the capture; the brightness of what is clipped white there (sky, sunlit ground) is a guess.
"""
import sys
import numpy as np, cv2

W, H = 2048, 1024
u = (np.arange(W) + 0.5) / W; v = 1 - (np.arange(H) + 0.5) / H          # v up
az = (u - 0.5) * 2 * np.pi                                                # Blender: u = atan2(dy, -dx) / 2pi + 0.5
el = (v - 0.5) * np.pi
AZ, EL = np.meshgrid(az, el)
dx, dy, dz = -np.cos(AZ) * np.cos(EL), np.sin(AZ) * np.cos(EL), np.sin(EL)
yaw = np.degrees(np.arctan2(dx, dy))        # 0 = +Y (door, behind the car), +90 = +X (car's left), -90 = car's right, 180 = ahead
eld = np.degrees(EL)
img = np.zeros((H, W, 3), np.float32)       # RGB, linear


def put(mask, rgb):
    img[mask] = rgb


srgb = lambda r, g, b, k=1.0: tuple(k * ((np.array([r, g, b]) / 255.0) ** 2.2))
put(np.ones_like(yaw, bool), srgb(70, 75, 80))                              # default: grey block wall
put(eld > 24, srgb(38, 40, 42))                                             # ceiling
put(eld < -9, srgb(62, 66, 76))                                             # concrete floor (bluish from the sky light)
wall = (eld >= -9) & (eld <= 24)
put(wall & (eld < 7), srgb(96, 138, 138))                                   # teal lower wall
put(wall & (eld >= 7) & (eld < 9), srgb(170, 60, 55))                       # red stripe
put(wall & (eld >= 9), srgb(196, 200, 196))                                 # white upper wall
ahead = np.abs(np.abs(yaw) - 180) < 55
put(ahead & wall, srgb(60, 44, 40))                                         # workbench wall, tool chests: dark, warm
put(ahead & (eld > -6) & (eld < 3), srgb(150, 40, 36))                      # red tool chests
right = (yaw < -55) & (yaw > -125)
put(right & wall, srgb(150, 140, 60))                                       # yellow booth doors
door = (np.abs(yaw) < 42) & (eld > -9) & (eld < 30)                         # the opening behind the car
put(door, srgb(245, 248, 252, 9.0))                                         # sky, clipped white in the capture
put(door & (eld < 13) & (eld > 1.5), srgb(120, 150, 95, 2.2))               # trees
put(door & (eld <= 1.5), srgb(215, 212, 205, 4.5))                          # sunlit concrete outside
put((np.abs(yaw) < 48) & (eld <= -9) & (eld > -30), srgb(170, 175, 185, 1.6))   # floor near the door catches the daylight
for y0, y1 in ((-150, -120), (-60, -30), (40, 70), (130, 160)):             # shop lights
    put((yaw > y0) & (yaw < y1) & (eld > 52) & (eld < 58), srgb(255, 250, 240, 14.0))
img = cv2.GaussianBlur(img, (0, 0), 3)
cv2.imwrite(sys.argv[1], cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
cv2.imwrite(sys.argv[1].replace(".hdr", "_preview.jpg"), cv2.cvtColor((np.clip(img, 0, 1) ** (1 / 2.2) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
print("wrote", sys.argv[1])
