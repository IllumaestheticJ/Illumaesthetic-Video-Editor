import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, FPS, MONO, SANS } from "./theme";

/** Props for both GfxCard (opaque black full-frame cards) and ScanLabel (transparent overlays). */
export type GfxProps = {
  cue: string;
  frames: number;
  text: string | string[];
  sub?: string;
  /** G08: delay (frames) before row 2 lands */
  row2At?: number;
  /** G15 optional CTA once the owner confirms */
  cta?: string;
  /** ScanLabel placement: bl = bottom-left, top = top centre, lower3 = lower third (title) */
  pos?: "bl" | "top" | "lower3";
  plate?: boolean;
};
export const gfxDefaults: GfxProps = { cue: "G03", frames: 72, text: "THE BET: 15 MINUTES", sub: "" };
export const calculateGfxMetadata: CalculateMetadataFunction<GfxProps> = ({ props }) => ({
  durationInFrames: props.frames, fps: FPS, width: 1920, height: 1080,
});

const ease = Easing.out(Easing.cubic);
const inA = (f: number, at = 0, d = 8) => interpolate(f, [at, at + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
const Bar: React.FC<{ w?: number; f: number; color?: string }> = ({ w = 120, f, color = C.accent }) => (
  <div style={{ width: w * inA(f, 0, 12), height: 6, background: color, marginBottom: 36 }} />
);
const Title: React.FC<{ children: React.ReactNode; size?: number; f: number; at?: number }> = ({ children, size = 116, f, at = 0 }) => (
  <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: size, letterSpacing: 6, lineHeight: 1.08, color: C.ink, textAlign: "center", opacity: inA(f, at), transform: `translateY(${(1 - inA(f, at)) * 10}px)` }}>{children}</div>
);
const Sub: React.FC<{ children: React.ReactNode; f: number; at?: number; size?: number }> = ({ children, f, at = 6, size = 46 }) => (
  <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: size, letterSpacing: 2, lineHeight: 1.35, color: "#b4bbc6", textAlign: "center", marginTop: 40, maxWidth: 1500, opacity: inA(f, at), transform: `translateY(${(1 - inA(f, at)) * 8}px)` }}>{children}</div>
);

/** centre of the 1920x920 picture area; the 160 px rail sits below */
const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: C.black }}>
    <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 920, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>{children}</div>
  </AbsoluteFill>
);

export const GfxCard: React.FC<GfxProps> = (p) => {
  const f = useCurrentFrame();
  const txt = Array.isArray(p.text) ? p.text : [p.text];
  switch (p.cue) {
    case "G05":
      return (
        <Stage>
          <div style={{ display: "flex", alignItems: "center", gap: 24, marginBottom: 36, opacity: inA(f), fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: 4, color: C.accent }}>
            <div style={{ width: 22, height: 22, background: C.accent, opacity: Math.floor(f / 6) % 2 === 0 || f > 36 ? 1 : 0.3 }} />CRASH
          </div>
          <Title f={f}>{txt[0]}</Title>
          <Sub f={f}>{p.sub}</Sub>
        </Stage>
      );
    case "G08": {
      const rows = txt.map((r) => {
        const i = r.lastIndexOf(" · ");
        return { label: r.slice(0, i), value: r.slice(i + 3), full: r };
      });
      const at = [4, p.row2At ?? 80];
      return (
        <Stage>
          <div style={{ display: "flex", flexDirection: "column", gap: 56 }}>
            {rows.map((r, i) => (
              <div key={i} style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", width: 1560, borderBottom: `2px solid ${C.dim}`, paddingBottom: 22, opacity: inA(f, at[i]), transform: `translateY(${(1 - inA(f, at[i])) * 10}px)` }}>
                <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 40, letterSpacing: 4, color: C.ink, whiteSpace: "nowrap" }}>{r.label}</span>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 120, color: C.ink, whiteSpace: "nowrap", marginLeft: 24 }}>{r.value}</span>
              </div>
            ))}
          </div>
        </Stage>
      );
    }
    case "G09": {
      const [a, b] = txt[0].split(": ");
      const sc = interpolate(f, [10, 20], [1.06, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
      return (
        <Stage>
          <Title f={f} size={92}>{a}:</Title>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 150, letterSpacing: 8, color: C.accent, marginTop: 16, opacity: inA(f, 10, 6), transform: `scale(${sc})` }}>{b}</div>
          <Sub f={f} at={20}>{p.sub}</Sub>
        </Stage>
      );
    }
    case "G15":
      return (
        <AbsoluteFill style={{ background: C.black, alignItems: "center", justifyContent: "center" }}>
          <Img src={staticFile("illumaesthetic_logo.png")} style={{ width: 900, opacity: inA(f, 0, 12) }} />
          {p.cta ? <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 40, letterSpacing: 3, color: C.grey, marginTop: 56, opacity: inA(f, 14) }}>{p.cta}</div> : null}
        </AbsoluteFill>
      );
    case "CON_G1": {
      const rows = txt.slice(1).map((r) => {
        const i = r.indexOf(" · ");
        return { value: r.slice(0, i), label: r.slice(i + 3) };
      });
      const at = [28, 56]; // successive beats (frames); editor re-times after beat snap
      return (
        <Stage>
          <Title f={f} size={130}>{txt[0]}</Title>
          <div style={{ display: "flex", flexDirection: "column", gap: 34, marginTop: 64 }}>
            {rows.map((r, i) => (
              <div key={i} style={{ display: "flex", alignItems: "baseline", width: 1300, borderBottom: `2px solid ${C.dim}`, paddingBottom: 14, opacity: inA(f, at[i]), transform: `translateY(${(1 - inA(f, at[i])) * 10}px)` }}>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 92, color: C.ink, whiteSpace: "nowrap", width: 440 }}>{r.value}</span>
                <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 44, letterSpacing: 4, color: C.ink, whiteSpace: "nowrap" }}>{r.label}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 48, fontFamily: MONO, fontWeight: 600, fontSize: 40, letterSpacing: 3, color: "#b4bbc6", opacity: inA(f, 88) }}>{p.sub}</div>
        </Stage>
      );
    }
    case "CON_G2":
      return (
        <Stage>
          <Bar f={f} />
          <div style={{ maxWidth: 1500 }}><Title f={f} size={116}>{txt[0]}</Title></div>
          <Sub f={f} at={30} size={40}>{p.sub}</Sub>
        </Stage>
      );
    default: // G03, G04 and any title+sub card
      return (
        <Stage>
          <Bar f={f} />
          <Title f={f} size={p.cue === "G04" ? 128 : 116}>{txt[0]}</Title>
          {p.sub ? <Sub f={f}>{p.cue === "G03" ? p.sub : p.sub}</Sub> : null}
        </Stage>
      );
  }
};

/** Reusable lower-third / label for scan shots. Transparent. Dark halo (and optional plate) for bright silver. */
export const ScanLabel: React.FC<GfxProps> = (p) => {
  const f = useCurrentFrame();
  const out = interpolate(f, [p.frames - 6, p.frames - 1], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const a = inA(f) * out;
  const title = Array.isArray(p.text) ? p.text[0] : p.text;
  const pos = p.pos ?? "bl";
  const big = pos === "lower3";
  const halo = "0 0 14px #000, 0 0 4px #000, 0 2px 18px #000";
  const block = (
    <div style={{ display: "flex", alignItems: "stretch", opacity: a, transform: `translateY(${(1 - inA(f)) * 8}px)`, padding: p.plate ? "22px 34px 22px 26px" : 0, background: p.plate ? "rgba(0,0,0,0.62)" : "transparent" }}>
      <div style={{ width: 6, background: C.accent, marginRight: 24, transform: `scaleY(${inA(f, 0, 10)})`, transformOrigin: "top" }} />
      <div>
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: big ? 76 : 48, letterSpacing: 6, lineHeight: 1.08, color: C.ink, textShadow: halo, whiteSpace: "pre-line" }}>{title}</div>
        {p.sub ? <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: big ? 36 : 32, letterSpacing: 2, color: C.ink, marginTop: 14, textShadow: halo, opacity: inA(f, 5) }}>{p.sub}</div> : null}
      </div>
    </div>
  );
  const style: React.CSSProperties =
    pos === "top" ? { position: "absolute", top: 90, left: 0, right: 0, display: "flex", justifyContent: "center" }
    : { position: "absolute", left: 96, bottom: 96 };
  return <AbsoluteFill>{<div style={style}>{block}</div>}</AbsoluteFill>;
};
