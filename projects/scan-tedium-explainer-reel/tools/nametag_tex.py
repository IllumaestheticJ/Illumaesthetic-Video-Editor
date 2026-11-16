"""Name-badge textures for Gus and Pip (owner: "small illumaesthetic nametags").

Near-white #ecefec card, thin sage #619f73 top stripe, the Illumaesthetic logo (remotion/public/illumaesthetic_logo.png, the
end-card logo, as is) on top and the name below in Fjalla One (remotion/public/fonts). Writes OUT/nametag_GUS.png, nametag_PIP.png.

Usage: python nametag_tex.py OUT_DIR
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
LOGO = REPO / "remotion/public/illumaesthetic_logo.png"
FONT = REPO / "remotion/public/fonts/fjalla-one-latin-400-normal.woff2"
W, H = 800, 500            # 1.6:1, same as the badge face


def font(size):
    for f in (FONT, "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"):
        try:
            return ImageFont.truetype(str(f), size)
        except OSError:
            continue
    raise SystemExit("no font")


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    lw = int(W * 0.86)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    for name in ("GUS", "PIP"):
        im = Image.new("RGB", (W, H), (0xEC, 0xEF, 0xEC))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, int(H * 0.09)), fill=(0x61, 0x9F, 0x73))        # sage top stripe
        im.paste(logo, ((W - lw) // 2, int(H * 0.15)), logo)
        f = font(int(H * 0.46))
        bb = d.textbbox((0, 0), name, font=f)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        y = int(H * 0.47) - bb[1] + (int(H * 0.47) - (bb[3] - bb[1])) // 2
        d.text((x, y), name, font=f, fill=(0x0B, 0x0C, 0x0B))
        im.save(out / f"nametag_{name}.png")
        print(out / f"nametag_{name}.png", "font", getattr(f, "path", f))


if __name__ == "__main__":
    main()
