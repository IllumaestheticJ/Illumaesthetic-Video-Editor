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
  const endScale = (width - 80) / p.imgW;
  const t = interpolate(f, [8, p.zoomFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const scale = p.startScale + (endScale - p.startScale) * t;
  // centre moves from the focus point to the image centre
  const cx = p.focusX + (p.imgW / 2 - p.focusX) * t;
  const cy = p.focusY + (p.imgH / 2 - p.focusY) * t;
  const left = width / 2 - cx * scale;
  const top = height / 2 - cy * scale;
  const frameOpacity = interpolate(t, [0.6, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const urlOpacity = interpolate(f, [p.zoomFrames - 10, p.zoomFrames + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#050506" }}>
      <div
        style={{
          position: "absolute",
          left: left - 2,
          top: top - 2,
          width: p.imgW * scale + 4,
          height: p.imgH * scale + 4,
          borderRadius: 14 * frameOpacity,
          boxShadow: `0 30px 90px rgba(0,0,0,${0.7 * frameOpacity}), 0 0 0 2px rgba(232,236,242,${0.25 * frameOpacity})`,
          overflow: "hidden",
        }}
      >
        <Img src={staticFile(p.src)} style={{ width: p.imgW * scale, height: p.imgH * scale, display: "block", margin: 2 }} />
      </div>
      <div
        style={{
          position: "absolute",
          top: height / 2 + (p.imgH * endScale) / 2 + 70,
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
    </AbsoluteFill>
  );
};
