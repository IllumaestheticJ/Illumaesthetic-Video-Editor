import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * End card: a website screenshot that starts tight on one region (e.g. the "SCAN DATA" heading)
 * and zooms out to show the page, framed like a browser window with the URL underneath.
 * Screenshot: capture with Playwright (see knowledge/sources.md), put it in remotion/public/.
 */
export type WebZoomProps = {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  src: string; // file in remotion/public
  imgW: number;
  imgH: number;
  focusX: number; // px in the screenshot to start centred on
  focusY: number;
  startScale: number; // screenshot px -> video px at frame 0
  zoomFrames: number; // frames to reach the full-width view
  url: string;
  title?: string; // shown above the page once zoomed out, e.g. "SCAN DATA NOW AVAILABLE"
  logo?: string; // file in remotion/public, shown under the URL
  logoWidth?: number;
  // optional layout for tall (mobile) screenshots; defaults keep the landscape layout
  endWidth?: number; // page width in video px once zoomed out (default width - 80)
  pageCenterY?: number; // vertical centre of the page in video px (default height / 2)
  titleTop?: number; // absolute title top in video px (default: 330 px above the page)
  radius?: number; // page corner radius once zoomed out (default 14)
  titleFrom?: number; // frame the title starts fading in (default zoomFrames - 18)
};

export const webZoomDefaults: WebZoomProps = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 174,
  src: "web_scan_data.png",
  imgW: 2880,
  imgH: 1640,
  focusX: 1440,
  focusY: 680,
  startScale: 1.25,
  zoomFrames: 95,
  url: "ILLUMAESTHETIC.COM",
};

export const calculateWebZoomMetadata: CalculateMetadataFunction<WebZoomProps> = ({ props }) => ({
  width: props.width,
  height: props.height,
  fps: props.fps,
  durationInFrames: props.durationInFrames,
});

export const WebZoom: React.FC<WebZoomProps> = (p) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const endScale = (p.endWidth ?? width - 80) / p.imgW;
  const midY = p.pageCenterY ?? height / 2;
  const t = interpolate(f, [8, p.zoomFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const scale = p.startScale + (endScale - p.startScale) * t;
  // centre moves from the focus point to the image centre
  const cx = p.focusX + (p.imgW / 2 - p.focusX) * t;
  const cy = p.focusY + (p.imgH / 2 - p.focusY) * t;
  const left = width / 2 - cx * scale;
  const top = midY - cy * scale;
  const frameOpacity = interpolate(t, [0.6, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  // order: page settles -> title -> logo -> URL (last)
  const logoIn = interpolate(f, [p.zoomFrames + 6, p.zoomFrames + 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const urlStart = p.logo ? p.zoomFrames + 26 : p.zoomFrames - 10;
  const urlOpacity = interpolate(f, [urlStart, urlStart + 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const titleStart = p.titleFrom ?? p.zoomFrames - 18;
  const titleIn = interpolate(f, [titleStart, titleStart + 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const pageTop = midY - (p.imgH * endScale) / 2;
  const pageBottom = midY + (p.imgH * endScale) / 2;
  return (
    <AbsoluteFill style={{ backgroundColor: "#050506" }}>
      <div
        style={{
          position: "absolute",
          left: left - 2,
          top: top - 2,
          width: p.imgW * scale + 4,
          height: p.imgH * scale + 4,
          borderRadius: (p.radius ?? 14) * frameOpacity,
          boxShadow: `0 30px 90px rgba(0,0,0,${0.7 * frameOpacity}), 0 0 0 2px rgba(232,236,242,${0.25 * frameOpacity})`,
          overflow: "hidden",
        }}
      >
        <Img src={staticFile(p.src)} style={{ width: p.imgW * scale, height: p.imgH * scale, display: "block", margin: 2 }} />
      </div>
      {p.title ? (
        <div
          style={{
            position: "absolute",
            top: (p.titleTop ?? pageTop - 330) + (1 - titleIn) * 24,
            width: "100%",
            textAlign: "center",
            opacity: titleIn,
            color: "#e8ecf2",
            fontFamily: "'Inter Display', 'Inter', sans-serif",
            fontWeight: 700,
            fontSize: 88,
            letterSpacing: 10,
            lineHeight: 1.08,
            padding: "0 70px",
            boxSizing: "border-box",
          }}
        >
          {p.title}
        </div>
      ) : null}
      <div
        style={{
          position: "absolute",
          top: pageBottom + (p.logo ? 90 + ((p.logoWidth ?? 640) * 345) / 2000 + 60 : 70),
          width: "100%",
          textAlign: "center",
          opacity: urlOpacity,
          color: "#e8ecf2",
          fontFamily: "'Inter Display', 'Inter', sans-serif",
          fontWeight: 700,
          fontSize: 64,
          letterSpacing: 8,
        }}
      >
        {p.url}
      </div>
      {p.logo ? (
        <Img
          src={staticFile(p.logo)}
          style={{
            position: "absolute",
            top: pageBottom + 90,
            left: (width - (p.logoWidth ?? 640)) / 2,
            width: p.logoWidth ?? 640,
            opacity: logoIn,
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};
