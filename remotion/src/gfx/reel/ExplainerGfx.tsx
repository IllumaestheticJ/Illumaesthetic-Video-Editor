import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, cancelRender, continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ReelGfx, ReelItem, Palette } from "./ReelGfx";

/**
 * Scan-tedium explainer reel (full): word-by-word dialogue captions over the cartoon half + the R3-style ReelGfx items
 * (the FULL VIDEO tease card). One transparent overlay, 1080x1920, 30 fps.
 * Captions: Fjalla One (OFL, public/fonts), speaker colour, dark ring outline + soft shadow. A word appears on its spoken
 * start (layout reserved, so nothing shifts); a page holds 1-2 lines. Each page has its own centre y (placed by eye
 * to keep faces and the phone screen clear); a 50 % near-black plate sits behind each page (Pip's sage on his sage hoodie
 * did not read with the outline alone). Props from projects/scan-tedium-explainer-reel/tools/full_build.py.
 */
const FONT = "Fjalla One";
const fontHandle = delayRender("Fjalla One");
const face = new FontFace(FONT, `url(${staticFile("fonts/fjalla-one-latin-400-normal.woff2")}) format('woff2')`);
face.load().then((f) => { document.fonts.add(f); continueRender(fontHandle); }).catch((e) => cancelRender(e));

type Word = { w: string; t0: number };
export type CapPage = { t0: number; t1: number; color: string; y: number; cx?: number; lines: Word[][] };
export type ExplainerGfxProps = { fps: number; durationInFrames: number; items: ReelItem[]; pages: CapPage[]; palette?: Partial<Palette>; size?: number };
export const explainerGfxDefaults: ExplainerGfxProps = { fps: 30, durationInFrames: 60, items: [], pages: [] };
export const calculateExplainerGfxMetadata: CalculateMetadataFunction<ExplainerGfxProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: 1080, height: 1920,
});

const OUT = "#0b0c0b";
const ring = (r: number) => {
  const s: string[] = [];
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    s.push(`${(Math.cos(a) * r).toFixed(2)}px ${(Math.sin(a) * r).toFixed(2)}px 0 ${OUT}`);
  }
  return s.join(", ");
};
const SHADOW = `${ring(5)}, ${ring(3)}, 0 4px 10px rgba(0,0,0,0.5)`;

const Page: React.FC<{ p: CapPage; f: number; fps: number; size: number }> = ({ p, f, fps, size }) => (
  <div style={{ position: "absolute", left: (p.cx ?? 500) - 440, width: 880, top: p.y - 200, height: 400, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
   <div style={{ background: "rgba(11,12,11,0.5)", borderRadius: 18, padding: "10px 26px 12px", display: "flex", flexDirection: "column", alignItems: "center" }}>
    {p.lines.map((ln, i) => (
      <div key={i} style={{ display: "flex", gap: size * 0.26, justifyContent: "center", whiteSpace: "nowrap", lineHeight: 1.12 }}>
        {ln.map((w, j) => {
          const lf = f - Math.round(w.t0 * fps);
          const on = lf >= 0;
          const sc = interpolate(lf, [0, 3], [0.82, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
          return (
            <span key={j} style={{ fontFamily: `'${FONT}'`, fontSize: size, color: p.color, textShadow: SHADOW, opacity: on ? 1 : 0,
              transform: `scale(${on ? sc : 1})`, display: "inline-block", letterSpacing: 1 }}>{w.w}</span>
          );
        })}
      </div>
    ))}
   </div>
  </div>
);

export const ExplainerGfx: React.FC<ExplainerGfxProps> = (props) => {
  const f = useCurrentFrame();
  const { fps, pages, size = 88 } = props;
  const live = pages.filter((p) => f >= Math.round(p.t0 * fps) && f < Math.round(p.t1 * fps));
  return (
    <AbsoluteFill style={{ background: "transparent" }}>
      <ReelGfx fps={fps} durationInFrames={props.durationInFrames} items={props.items} palette={props.palette} />
      {live.map((p, i) => <Page key={i} p={p} f={f} fps={fps} size={size} />)}
    </AbsoluteFill>
  );
};
