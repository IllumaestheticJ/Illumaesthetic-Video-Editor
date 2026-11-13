import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * Split-screen end card: two website screenshots, each starting 1:1 on a region that fills its own
 * half of the frame (the listing's scan view, matched by the last scan shot of that panel) and zooming
 * out to two page cards, with the title above, then the logo and the URL below.
 * The visible region of each screenshot is interpolated (never leaves the image), so nothing distorts.
 */
export type SplitPage = {
  src: string; // file in remotion/public
  imgW: number;
  imgH: number;
  // region of the screenshot shown at frame 0 (fills the panel exactly): x, y, w, h in screenshot px
  region: [number, number, number, number];
};

export type WebZoomSplitProps = {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  pages: [SplitPage, SplitPage];
  holdFrames: number; // frames to hold the 1:1 start before zooming
  zoomFrames: number; // frame the zoom-out ends
  cardWidth: number; // page width in video px once zoomed out
  cardCenters: [number, number]; // vertical centres of the two cards
  title: string;
  titleTop: number;
  url: string;
  logo: string;
  logoWidth: number;
  logoTop: number;
  urlTop: number;
};

export const webZoomSplitDefaults: WebZoomSplitProps = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 200,
  pages: [
    { src: "web_a.png", imgW: 2880, imgH: 1800, region: [435, 368, 1060, 942] },
    { src: "web_b.png", imgW: 2880, imgH: 1800, region: [435, 368, 1060, 942] },
  ],
  holdFrames: 20,
  zoomFrames: 85,
  cardWidth: 940,
  cardCenters: [620, 1240],
  title: "SCAN DATA NOW AVAILABLE",
  titleTop: 70,
  url: "ILLUMAESTHETIC.COM",
  logo: "illumaesthetic_logo.png",
  logoWidth: 560,
  logoTop: 1590,
  urlTop: 1740,
};

export const calculateWebZoomSplitMetadata: CalculateMetadataFunction<WebZoomSplitProps> = ({ props }) => ({
  width: props.width,
  height: props.height,
  fps: props.fps,
  durationInFrames: props.durationInFrames,
});

export const WebZoomSplit: React.FC<WebZoomSplitProps> = (p) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const t = interpolate(f, [p.holdFrames, p.zoomFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const fade = (a: number, b: number) => interpolate(f, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const frameOpacity = interpolate(t, [0.5, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const titleIn = fade(p.zoomFrames - 22, p.zoomFrames);
  const logoIn = fade(p.zoomFrames + 4, p.zoomFrames + 20);
  const urlIn = fade(p.zoomFrames + 22, p.zoomFrames + 40);
  const panelH = height / 2;
  return (
    <AbsoluteFill style={{ backgroundColor: "#050506" }}>
      {p.pages.map((pg, i) => {
        const [rx, ry, rw, rh] = pg.region;
        // visible region in screenshot px
        const u0 = rx * (1 - t);
        const v0 = ry * (1 - t);
        const uw = rw + (pg.imgW - rw) * t;
        const vh = rh + (pg.imgH - rh) * t;
        const s0 = width / rw;
        const s1 = p.cardWidth / pg.imgW;
        const scale = s0 * Math.pow(s1 / s0, t);
        const w = uw * scale;
        const h = vh * scale;
        const cx = width / 2;
        const cy = panelH * (i + 0.5) + (p.cardCenters[i] - panelH * (i + 0.5)) * t;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: cx - w / 2,
              top: cy - h / 2,
              width: w,
              height: h,
              overflow: "hidden",
              borderRadius: 14 * frameOpacity,
              boxShadow: `0 24px 70px rgba(0,0,0,${0.7 * frameOpacity}), 0 0 0 2px rgba(232,236,242,${0.25 * frameOpacity})`,
              zIndex: 2 - i,
            }}
          >
            <Img
              src={staticFile(pg.src)}
              style={{ position: "absolute", left: -u0 * scale, top: -v0 * scale, width: pg.imgW * scale, height: pg.imgH * scale, maxWidth: "none" }}
            />
          </div>
        );
      })}
      <div
        style={{
          position: "absolute",
          top: p.titleTop + (1 - titleIn) * 20,
          width: "100%",
          textAlign: "center",
          opacity: titleIn,
          color: "#e8ecf2",
          fontFamily: "'Inter Display', 'Inter', sans-serif",
          fontWeight: 700,
          fontSize: 80,
          letterSpacing: 9,
          lineHeight: 1.1,
          padding: "0 70px",
          boxSizing: "border-box",
          zIndex: 5,
        }}
      >
        {p.title}
      </div>
      <Img src={staticFile(p.logo)} style={{ position: "absolute", top: p.logoTop, left: (width - p.logoWidth) / 2, width: p.logoWidth, opacity: logoIn, zIndex: 5 }} />
      <div
        style={{
          position: "absolute",
          top: p.urlTop,
          width: "100%",
          textAlign: "center",
          opacity: urlIn,
          color: "#e8ecf2",
          fontFamily: "'Inter Display', 'Inter', sans-serif",
          fontWeight: 700,
          fontSize: 60,
          letterSpacing: 8,
          zIndex: 5,
        }}
      >
        {p.url}
      </div>
    </AbsoluteFill>
  );
};
