"""The "Purchased" pop-up, drawn clean (BGRA) -> $W/sfx/toast.png

v2-v15 used the pop-up cut out of the second capture; its mask was a filled blob, so the capture's own floor showed inside
and between the letters wherever it was laid over something else (user, v15 review: "still isn't masked correctly").
This draws it instead: white lettering with the game's dark edge, the ticked disc, nothing else. Sizes measured on the
capture's pop-up (lettering 172 px wide, capitals 30 px, disc 43 px, in a 265x75 box with the lettering starting at x 18).
"""
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path("/home/user/media/work/gta6-integra")
LEX = "/home/user/media/gta6-integra/fonts/lexend-latin-400-normal.ttf"
K = 4; BW, BH = 265, 75


def main():
    f = ImageFont.truetype(LEX, 43 * K)
    wid = f.getlength("Purchased"); sq = 172 * K / wid
    lay = Image.new("L", (int(wid) + 40 * K, BH * K), 0); ImageDraw.Draw(lay).text((20 * K, 57 * K), "Purchased", font=f, fill=255, anchor="ls")
    t = np.asarray(lay.resize((int(lay.width * sq), BH * K), Image.LANCZOS)).astype(np.float32) / 255
    text = np.zeros((BH * K, BW * K), np.float32); x0 = int(18 * K - 20 * K * sq)
    xs = max(0, x0); w = min(t.shape[1] - (xs - x0), BW * K - xs); text[:, xs:xs + w] = t[:, xs - x0:xs - x0 + w]
    disc = np.zeros_like(text); ring = np.zeros_like(text); tick = np.zeros_like(text)
    c = (int(223.5 * K), int(35.5 * K))
    cv2.circle(ring, c, int(21.5 * K), 1, -1, cv2.LINE_AA); cv2.circle(disc, c, int(19 * K), 1, -1, cv2.LINE_AA)
    pts = (np.array([[213, 36], [220.5, 43.5], [234.5, 28]]) * K).astype(np.int32)
    cv2.polylines(tick, [pts], False, 1, int(4.6 * K), cv2.LINE_AA)
    edge = cv2.dilate(text, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(4.5 * K), int(4.5 * K))))
    dark, white = np.array([30, 28, 28], np.float32), np.array([246, 246, 246], np.float32)
    rgb = np.zeros((BH * K, BW * K, 3), np.float32); a = np.zeros_like(text)
    for col, m in ((dark, edge), (white, text), (dark, ring), (white, disc), (dark, tick)):
        rgb = rgb * (1 - m[..., None]) + col * m[..., None]; a = np.maximum(a, m)
    out = cv2.resize(np.dstack([rgb, a * 255]), (BW, BH), interpolation=cv2.INTER_AREA)
    old = W / "sfx/toast.png"
    if old.exists() and not (W / "sfx/toast_capture.png").exists():
        old.rename(W / "sfx/toast_capture.png")
    cv2.imwrite(str(old), np.clip(out, 0, 255).astype(np.uint8))
    if not (W / "sfx/toast_capture.png").exists():      # no cut-out to compare against in this project
        return
    o = out.astype(np.float32); al = o[..., 3:] / 255
    cap_ = cv2.imread(str(W / "sfx/toast_capture.png"), cv2.IMREAD_UNCHANGED).astype(np.float32); ca = cap_[..., 3:] / 255
    rows = [np.hstack([cap_[..., :3] * ca + bg * (1 - ca), o[..., :3] * al + bg * (1 - al)]) for bg in (25, 120, 235)]
    cv2.imwrite(str(W / "test/toast_new.png"), cv2.resize(np.vstack(rows).astype(np.uint8), None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC))


if __name__ == "__main__":
    main()
