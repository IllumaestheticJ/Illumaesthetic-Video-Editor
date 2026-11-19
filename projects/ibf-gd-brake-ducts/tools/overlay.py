"""Render the reel's text cards as 1080x1920 RGBA PNGs + a text-boxes JSON for scripts/safezone_check.py.

Usage: python overlay.py spec.json out_dir
spec: {"cards": [{"name", "t0", "t1", "bg": null | "#000000" (full-frame backdrop),
                  "logo": {"path", "w", "cy"} (optional),
                  "lines": [{"text", "font": "akira"|"unb300"|"unb400"|"unb500", "size", "cy",
                             "color", "strike": bool, "key": bool, "shadow": bool}]}]}
Every line is centred horizontally on x = 484 (middle of the 48-920 safe band) and must fit inside it.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FONTS = {
    "akira": f"{ROOT}/assets/fonts/akira/AkiraExpanded-SuperBold.otf",
    "unb300": f"{ROOT}/assets/fonts/unbounded/Unbounded-300.ttf",
    "unb400": f"{ROOT}/assets/fonts/unbounded/Unbounded-400.ttf",
    "unb500": f"{ROOT}/assets/fonts/unbounded/Unbounded-500.ttf",
    "unb700": f"{ROOT}/assets/fonts/unbounded/Unbounded-700.ttf",
}
W, H, CX, X0, X1 = 1080, 1920, 484, 48, 920


def hexrgba(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def render(card, out_dir):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if card.get("bg"):
        im = Image.new("RGBA", (W, H), hexrgba(card["bg"]))
    boxes = []
    if card.get("logo"):
        lg = card["logo"]
        logo = Image.open(lg["path"]).convert("RGBA")
        w = lg["w"]; h = round(logo.height * w / logo.width)
        logo = logo.resize((w, h), Image.LANCZOS)
        x, y = CX - w // 2, lg["cy"] - h // 2
        im.alpha_composite(logo, (x, y))
        boxes.append({"t0": card["t0"], "t1": card["t1"], "x": x, "y": y, "w": w, "h": h, "label": "logo", "key": True})
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(text_layer)
    for ln in card["lines"]:
        f = ImageFont.truetype(FONTS[ln["font"]], ln["size"])
        l, t, r, b = d.textbbox((0, 0), ln["text"], font=f)
        tw, th = r - l, b - t
        x = CX - tw / 2 - l
        y = ln["cy"] - th / 2 - t
        if CX - tw / 2 < X0 or CX + tw / 2 > X1:
            sys.exit(f"line too wide for the safe band: {ln['text']!r} ({tw}px)")
        col = hexrgba(ln.get("color", "#ffffff"))
        d.text((x, y), ln["text"], font=f, fill=col)
        if ln.get("strike"):
            sy = ln["cy"]
            d.line([(CX - tw / 2 - 6, sy), (CX + tw / 2 + 6, sy)], fill=hexrgba(ln.get("strike_color", "#e0161b")), width=max(4, ln["size"] // 9))
        boxes.append({"t0": card["t0"], "t1": card["t1"], "x": int(CX - tw / 2), "y": int(ln["cy"] - th / 2),
                      "w": int(tw), "h": int(th), "label": ln["text"], "key": bool(ln.get("key", True))})
    if card.get("halo", not card.get("bg")):
        # soft dark halo behind text so it reads over footage
        a = text_layer.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14))
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        halo.putalpha(a.point(lambda v: int(v * 0.75)))
        im.alpha_composite(halo)
    im.alpha_composite(text_layer)
    p = os.path.join(out_dir, f"{card['name']}.png")
    im.save(p)
    return p, boxes


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    allb, idx = [], []
    for c in spec["cards"]:
        p, b = render(c, out)
        allb += b
        idx.append({"png": p, "t0": c["t0"], "t1": c["t1"], "fade": c.get("fade", 0.12)})
    json.dump(allb, open(os.path.join(out, "boxes.json"), "w"), indent=1)
    json.dump(idx, open(os.path.join(out, "cards.json"), "w"), indent=1)
    print(f"{len(idx)} cards, {len(allb)} boxes -> {out}")


if __name__ == "__main__":
    main()
