"""Ep 9 graphics overlay: word-by-word captions on the cartoon only (Part A and the finale tag) + the logo card (no CTA:
owner rule, a call to action only when relevant). Same Remotion composition and style as the pilot (ExplainerGfx: Fjalla One,
Pip sage #619f73, Gus #ecefec, size 88). Nothing is drawn over Part B (real footage) - checked here.

Usage: python ep9_gfx.py OUT_DIR   -> OUT_DIR/ep9_gfx_props.json + OUT_DIR/ep9_gfx.mov (ProRes 4444 alpha, 1080x1920, 30 fps)
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
VL = json.loads((HERE.parent / "voice_lines.json").read_text())
FPS = 30
A_END = 1139 / FPS
B_LEN = 150 / FPS
TAG_LEN = 114 / FPS
LOGO0 = A_END + B_LEN + TAG_LEN
TOTAL_F = 1493
CAP = dict(PIP="#619f73", GUS="#ecefec")
BRAND = {"accent": "#619f73", "onAccent": "#0b0c0b", "ink": "#ecefec", "bg": "#0b0c0b", "sub": "#d4d9d4", "sub2": "#c8cec8",
         "label": "#a8b0a8", "dim55": "rgba(236,239,236,0.55)", "dim50": "rgba(236,239,236,0.5)", "plate": "rgba(11,12,11,0.58)",
         "cap": "rgba(11,12,11,0.55)"}
PHONE_CORNERS = Path("/home/user/media/pip-gus-ep9-glue/final/screen_corners.json")
CAP_BOX = (60, 1190, 1020, 1560)   # caption plate area + margin (x0, y0, x1, y1) at y=1330, two rows of size 88
MAXC = 16            # characters per caption row at size 88 in an 880 px box
Y = 1330


def script_tokens(text):
    return [w for w in re.sub(r"\s+", " ", text.replace("...", "…")).strip().split(" ")]


def phone_clash_t():
    """First Part A time at which the phone screen (real footage) reaches the caption box - captions must end before it."""
    if not PHONE_CORNERS.exists():
        return A_END
    cj = json.loads(PHONE_CORNERS.read_text())
    x0, y0, x1, y1 = CAP_BOX
    for f in sorted(map(int, cj)):
        xs = [p[0] for p in cj[str(f)]]; ys = [p[1] for p in cj[str(f)]]
        if min(xs) < x1 and max(xs) > x0 and min(ys) < y1 and max(ys) > y0:
            return f / FPS
    return A_END


def pages():
    out = []
    CLASH = phone_clash_t()
    print(f"phone reaches the caption box at {CLASH:.3f} s (frame {round(CLASH * FPS)})")
    for L in VL["lines"]:
        toks = script_tokens(L["text"])
        toks = [t for t in toks if re.sub(r"[^A-Za-z']", "", t)] if len(toks) != len(L["words"]) else toks
        if len(toks) != len(L["words"]):   # '...Not that.' -> attach the ellipsis to the first word
            toks = [t for t in toks if t != "…"]
            toks[0] = ("…" if L["text"].startswith("...") else "") + toks[0].lstrip("…")
        assert len(toks) == len(L["words"]), (L["n"], toks, [w["w"] for w in L["words"]])
        shift = 0.0 if L["t1"] <= A_END else B_LEN
        ws = [dict(w=tk, t0=round(w["t0"] + shift, 3), t1=round(w["t1"] + shift, 3)) for tk, w in zip(toks, L["words"])]
        # split into sentence chunks, then rows of <= MAXC chars, max 2 rows per page
        chunks, cur = [], []
        for w in ws:
            cur.append(w)
            if w["w"][-1] in ".?!" and len(" ".join(x["w"] for x in cur)) > 6:
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        pg = []
        for ch in chunks:
            # balanced rows: k = ceil(chars / MAXC) rows of about equal length (no one-word orphan rows)
            n = len(" ".join(x["w"] for x in ch))
            k = max(1, -(-n // MAXC))
            target = n / k
            rows, row = [], []
            for w in ch:
                cand = len(" ".join(x["w"] for x in row + [w]))
                if row and cand > target + 2 and len(rows) < k - 1:
                    rows.append(row); row = []
                row.append(w)
            rows.append(row)
            for i in range(0, len(rows), 2):
                pg.append(rows[i:i + 2])
        for rows in pg:
            out.append(dict(t0=rows[0][0]["t0"], t1=rows[-1][-1]["t1"] + 0.35, color=CAP[L["who"]], y=Y, cx=540,
                            lines=[[dict(w=w["w"], t0=w["t0"]) for w in r] for r in rows]))
    # a page ends when the next one starts; none may reach into Part B or the logo card
    for a, b in zip(out, out[1:]):
        a["t1"] = round(min(a["t1"], b["t0"]), 3)
    for p in out:
        if p["t0"] < A_END:
            p["t1"] = round(min(p["t1"], CLASH - 1 / FPS), 3)
        else:
            assert p["t0"] >= A_END + B_LEN
            p["t1"] = round(min(p["t1"], LOGO0 - 1 / FPS), 3)
    return out


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    props = {"fps": FPS, "durationInFrames": TOTAL_F, "pages": pages(), "palette": BRAND, "size": 88,
             "items": [{"kind": "logo", "t0": LOGO0, "t1": TOTAL_F / FPS + 1, "cta": ""}]}
    pj = out / "ep9_gfx_props.json"
    pj.write_text(json.dumps(props, indent=1))
    (HERE.parent / "gfx_props.json").write_text(json.dumps(props, indent=1))
    for p in props["pages"]:
        print(f"{p['t0']:6.2f}-{p['t1']:6.2f} {' / '.join(' '.join(w['w'] for w in r) for r in p['lines'])}")
    if "--norender" in sys.argv:
        return
    mov = out / "ep9_gfx.mov"
    subprocess.run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", str(mov), f"--props={pj}", "--codec=prores",
                    "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=1", "--log=error"],
                   cwd=REPO / "remotion", check=True)
    print(mov)


if __name__ == "__main__":
    main()
