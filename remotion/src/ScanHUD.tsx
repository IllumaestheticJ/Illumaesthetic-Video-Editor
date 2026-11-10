import React from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Easing,
  interpolate,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * Transparent HUD layer composited over the scan beats by `ive assemble`.
 * Everything is driven by props (projects/<name>/overlay.json) so agents never touch TSX
 * to make a new video - they only write the item list.
 *
 * House rules (knowledge/style-guide.md): text only on scan shots, never on IRL footage;
 * max two items on screen; enter on the beat; nothing inside the car silhouette.
 */

export type HudItem =
  | {
      kind: "label";
      from: number; // frame
      duration: number;
      title: string; // e.g. "FRONT BUMPER"
      sub?: string; // e.g. "REMOVED · 471,838 TRIS"
      x: number; // 0..1 of width
      y: number; // 0..1 of height
      align?: "left" | "right";
    }
  | {
      kind: "counter";
      from: number;
      duration: number;
      label: string; // "POINTS CAPTURED"
      value: number;
      x: number;
      y: number;
      align?: "left" | "right";
    }
  | {
      kind: "brackets"; // scan-frame corner brackets
      from: number;
      duration: number;
      inset?: number; // px
    }
  | {
      kind: "title";
      from: number;
      duration: number;
      text: string;
      sub?: string;
      y: number;
    };

export type ScanHUDProps = {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  accent: string;
  items: HudItem[];
};

export const scanHudDefaults: ScanHUDProps = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 90,
  accent: "#e8ecf2",
  items: [
    { kind: "brackets", from: 0, duration: 90 },
    { kind: "counter", from: 6, duration: 80, label: "TRIANGLES CAPTURED", value: 24991097, x: 0.08, y: 0.18 },
    { kind: "label", from: 20, duration: 60, title: "NISSAN 240SX", sub: "S13 HATCH · FULL BODY SCAN", x: 0.92, y: 0.8, align: "right" },
  ],
};

export const calculateScanHudMetadata: CalculateMetadataFunction<ScanHUDProps> = ({ props }) => ({
  width: props.width,
  height: props.height,
  fps: props.fps,
  durationInFrames: props.durationInFrames,
  defaultCodec: "prores",
  defaultVideoImageFormat: "png",
  defaultPixelFormat: "yuva444p10le",
  defaultProResProfile: "4444",
});

const MONO = "'JetBrains Mono', 'DejaVu Sans Mono', monospace";
const SANS = "'Inter Display', 'Inter', sans-serif";

/** Fade/slide in over 8 frames, out over 6. */
const useInOut = (duration: number) => {
  const f = useCurrentFrame();
  const fin = interpolate(f, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const fout = interpolate(f, [duration - 6, duration], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return { f, k: Math.min(fin, fout), slide: (1 - fin) * 18 };
};

const Label: React.FC<{ item: Extract<HudItem, { kind: "label" }>; accent: string }> = ({ item, accent }) => {
  const { width, height } = useVideoConfig();
  const { f, k, slide } = useInOut(item.duration);
  const right = item.align === "right";
  const rule = interpolate(f, [2, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  // typewriter on the sub line
  const sub = item.sub ?? "";
  const chars = Math.floor(interpolate(f, [6, 6 + sub.length * 0.9], [0, sub.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <div
      style={{
        position: "absolute",
        top: item.y * height,
        [right ? "right" : "left"]: (right ? 1 - item.x : item.x) * width,
        textAlign: right ? "right" : "left",
        opacity: k,
        transform: `translateX(${right ? slide : -slide}px)`,
        color: accent,
      }}
    >
      <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 52, letterSpacing: 6, lineHeight: 1 }}>{item.title}</div>
      <div
        style={{
          height: 2,
          width: 260 * rule,
          background: accent,
          opacity: 0.7,
          margin: "16px 0 14px",
          marginLeft: right ? "auto" : 0,
        }}
      />
      <div style={{ fontFamily: MONO, fontSize: 30, letterSpacing: 3, opacity: 0.75 }}>{sub.slice(0, chars)}</div>
    </div>
  );
};

const Counter: React.FC<{ item: Extract<HudItem, { kind: "counter" }>; accent: string }> = ({ item, accent }) => {
  const { width, height } = useVideoConfig();
  const { f, k, slide } = useInOut(item.duration);
  const v = Math.round(
    interpolate(f, [0, Math.min(item.duration * 0.7, 45)], [0, item.value], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.exp),
    }),
  );
  const right = item.align === "right";
  return (
    <div
      style={{
        position: "absolute",
        top: item.y * height,
        [right ? "right" : "left"]: (right ? 1 - item.x : item.x) * width,
        textAlign: right ? "right" : "left",
        opacity: k,
        transform: `translateY(${slide}px)`,
        color: accent,
      }}
    >
      <div style={{ fontFamily: MONO, fontSize: 28, letterSpacing: 4, opacity: 0.7 }}>{item.label}</div>
      <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 64, letterSpacing: 2, marginTop: 8 }}>
        {v.toLocaleString("en-US")}
      </div>
    </div>
  );
};

const Brackets: React.FC<{ item: Extract<HudItem, { kind: "brackets" }>; accent: string }> = ({ item, accent }) => {
  const { width, height } = useVideoConfig();
  const { f, k } = useInOut(item.duration);
  const inset = item.inset ?? 80;
  const grow = interpolate(f, [0, 10], [0, 70], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const corners: [number, number, number, number][] = [
    [inset, inset, 1, 1],
    [width - inset, inset, -1, 1],
    [inset, height - inset, 1, -1],
    [width - inset, height - inset, -1, -1],
  ];
  return (
    <AbsoluteFill style={{ opacity: k * 0.8 }}>
      <svg width={width} height={height}>
        {corners.map(([x, y, sx, sy], i) => (
          <path key={i} d={`M ${x} ${y + sy * grow} L ${x} ${y} L ${x + sx * grow} ${y}`} stroke={accent} strokeWidth={3} fill="none" />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

const Title: React.FC<{ item: Extract<HudItem, { kind: "title" }>; accent: string }> = ({ item, accent }) => {
  const { height } = useVideoConfig();
  const { k, slide } = useInOut(item.duration);
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div style={{ position: "absolute", top: item.y * height, textAlign: "center", opacity: k, transform: `translateY(${slide}px)`, color: accent }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 92, letterSpacing: 10 }}>{item.text}</div>
        {item.sub ? <div style={{ fontFamily: MONO, fontSize: 32, letterSpacing: 6, opacity: 0.7, marginTop: 18 }}>{item.sub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

export const ScanHUD: React.FC<ScanHUDProps> = ({ items, accent }) => {
  return (
    <AbsoluteFill>
      {items.map((item, i) => (
        <Sequence key={i} from={item.from} durationInFrames={item.duration} layout="none">
          {item.kind === "label" ? <Label item={item} accent={accent} /> : null}
          {item.kind === "counter" ? <Counter item={item} accent={accent} /> : null}
          {item.kind === "brackets" ? <Brackets item={item} accent={accent} /> : null}
          {item.kind === "title" ? <Title item={item} accent={accent} /> : null}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
