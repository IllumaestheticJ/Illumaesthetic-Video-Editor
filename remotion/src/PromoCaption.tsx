import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";

/**
 * Promo caption track (scan-data promos only: knowledge/promo-script-template.md). Not the ScanHUD look.
 * Matches the reference "3_square_meter_home_design" caption, measured at 1080x1920: a fixed-width white bar
 * (x 87-993, y 1510-1582, ~18 px corner radius) with medium black sans text (~34 px), lower case, centred.
 * One caption at a time = the narration line, word for word. Times in seconds.
 * Render transparent (ProRes 4444) and overlay on scan shots only; never over IRL footage.
 */
export type PromoCaptionProps = {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  captions: { text: string; start: number; end: number }[];
  barY?: number; // centre of the bar in px (reference 1546)
  barW?: number; // reference 906
  barH?: number; // reference 72
  fontSize?: number; // reference ~34
  fadeFrames?: number; // reference swaps text hard; 0 = hard cut
};

export const promoCaptionDefaults: PromoCaptionProps = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 150,
  captions: [{ text: "let's build a 2026 nissan sentra SR", start: 0, end: 2.5 }, { text: "using nothing but scan data", start: 2.5, end: 5 }],
  barY: 1546,
  barW: 906,
  barH: 72,
  fontSize: 31,
  fadeFrames: 0,
};

export const calculatePromoCaptionMetadata: CalculateMetadataFunction<PromoCaptionProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames,
  fps: props.fps,
  width: props.width,
  height: props.height,
});

const FONT = "PromoMontserrat";
let fontLoaded = false;
const useFont = () => {
  const [handle] = React.useState(() => (fontLoaded ? null : delayRender("promo font")));
  React.useEffect(() => {
    if (!handle) return;
    const f = new FontFace(FONT, `url(${staticFile("fonts/montserrat-latin-500-normal.woff2")})`, { weight: "500" });
    f.load().then((ff) => {
      document.fonts.add(ff);
      fontLoaded = true;
      continueRender(handle);
    });
  }, [handle]);
};

export const PromoCaption: React.FC<PromoCaptionProps> = (p) => {
  useFont();
  const frame = useCurrentFrame();
  const t = frame / p.fps;
  const c = p.captions.find((x) => t >= x.start && t < x.end);
  if (!c) return <AbsoluteFill />;
  const fade = p.fadeFrames ?? 0;
  const s = Math.round(c.start * p.fps);
  const e = Math.round(c.end * p.fps);
  const op = fade > 0 ? interpolate(frame, [s, s + fade, e - fade, e], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  const w = p.barW ?? 906;
  const h = p.barH ?? 72;
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: (p.width - w) / 2,
          top: (p.barY ?? 1546) - h / 2,
          width: w,
          height: h,
          borderRadius: 18,
          background: "rgba(255,255,255,0.96)",
          boxShadow: "0 2px 10px rgba(0,0,0,0.12)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          opacity: op,
        }}
      >
        <span style={{ fontFamily: `${FONT}, sans-serif`, fontWeight: 500, fontSize: p.fontSize ?? 31, color: "#111", letterSpacing: 0.2, whiteSpace: "nowrap" }}>
          {c.text}
        </span>
      </div>
    </AbsoluteFill>
  );
};
