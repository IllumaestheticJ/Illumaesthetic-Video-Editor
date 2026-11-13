import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, random, staticFile, useCurrentFrame } from "remotion";
import { C, FPS, MONO, SANS } from "../theme";
import { mmss } from "../HudRail";

export type CueV2Props = {
  cue: string; frames: number; text: string | string[]; sub?: string;
  x?: number; y?: number; w?: number; align?: "left" | "right";
  beats?: number[]; // frame offsets for staged lines (G08 rows, CON_G1 lines)
  from?: number; to?: number; // card clock ff range in seconds (G05b)
  cta?: string;
};
export const cueV2Defaults: CueV2Props = { cue: "G03_v2", frames: 48, text: "THE BET: 15 MINUTES", x: 80, y: 640 };
export const calculateCueV2Metadata: CalculateMetadataFunction<CueV2Props> = ({ props }) => ({
  durationInFrames: props.frames, fps: FPS, width: 1920, height: 1080,
});

const ease = Easing.out(Easing.cubic);
const inA = (f: number, at = 0, d = 7) => interpolate(f, [at, at + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
const SH = "0 1px 3px rgba(0,0,0,0.9), 0 0 10px rgba(0,0,0,0.6)";
const PLATE = "rgba(0,0,0,0.58)";

const Box: React.FC<{ x: number; y: number; w: number; align?: "left" | "right"; a: number; dx: number; children: React.ReactNode }> = ({ x, y, w, align = "left", a, dx, children }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, opacity: a, transform: `translateX(${dx}px)`, background: PLATE, borderRadius: 14, padding: "22px 28px", boxSizing: "border-box", textAlign: align, borderLeft: align === "left" ? `8px solid ${C.accent}` : undefined, borderRight: align === "right" ? `8px solid ${C.accent}` : undefined }}>{children}</div>
);

/** Plated overlays on footage: G03, STING1/2, G_SPRAY, G08, G09, CON_G1. Transparent. */
export const CueV2: React.FC<CueV2Props> = (p) => {
  const f = useCurrentFrame();
  const txt = Array.isArray(p.text) ? p.text : [p.text];
  const x = p.x ?? 80, y = p.y ?? 640, w = p.w ?? 820, align = p.align ?? "left";
  const dir = align === "left" ? -1 : 1;
  const sting = p.cue.startsWith("STING");
  // slide in, and for stings slide out on the last 8 frames; others cut with the shot
  const slide = (1 - inA(f, 0, sting ? 10 : 6)) * 60 * dir;
  const outF = sting ? interpolate(f, [p.frames - 8, p.frames - 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const a = inA(f, 0, 6) * (1 - outF);
  const dx = slide + outF * 60 * dir;
  const big = (s: string, size: number, color = C.ink) => (
    <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: size, letterSpacing: 5, lineHeight: 1.05, color, textShadow: SH, whiteSpace: "nowrap" }}>{s}</div>
  );
  const mono = (s: string, size: number, color = C.ink) => (
    <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: size, letterSpacing: 2, lineHeight: 1.15, color, textShadow: SH, whiteSpace: "nowrap" }}>{s}</div>
  );

  switch (p.cue) {
    case "G03_v2": {
      const [a1, b1] = txt[0].split(": ");
      return (
        <AbsoluteFill>
          <Box x={x} y={y} w={w} a={a} dx={dx}>
            {big(a1 + ":", 44, "#c3c9d3")}
            <div style={{ height: 6 }} />
            {big(b1, 96)}
          </Box>
        </AbsoluteFill>
      );
    }
    case "G01_v2": {
      const lines = txt[0].split("\n");
      return (
        <AbsoluteFill>
          <Box x={x} y={y} w={w} a={a} dx={dx}>
            {lines.map((l, i) => <div key={i}>{big(l, 58)}</div>)}
            <div style={{ marginTop: 16, fontFamily: MONO, fontWeight: 700, fontSize: 27, letterSpacing: 2, lineHeight: 1.3, color: "#d5dae2", textShadow: SH }}>{p.sub}</div>
          </Box>
        </AbsoluteFill>
      );
    }
    case "STING1_v2":
    case "STING2_v2": {
      const [pt, nm] = txt[0].split(" · ");
      return (
        <AbsoluteFill>
          <Box x={x} y={y} w={w} a={a} dx={dx}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 22 }}>
              {big(pt, 84, C.accent)}
              {big("·", 84, "#c3c9d3")}
              {big(nm, 84)}
            </div>
          </Box>
        </AbsoluteFill>
      );
    }
    case "G_SPRAY_v2": {
      const sc = interpolate(f, [0, 8], [1.06, 1], { extrapolateRight: "clamp", easing: ease });
      const [l1, l2] = txt[0].split(" · ");
      return (
        <AbsoluteFill>
          <div style={{ transform: `scale(${sc})`, transformOrigin: "right center" }}>
            <Box x={x} y={y} w={w} align="right" a={a} dx={dx}>
              {big(l1, 80)}
              <div style={{ height: 10 }} />
              {mono(l2, 46, "#e8ecf2")}
            </Box>
          </div>
        </AbsoluteFill>
      );
    }
    case "G08_v2": {
      const at = p.beats ?? [0, 60];
      return (
        <AbsoluteFill>
          <div style={{ position: "absolute", left: x, top: y, width: w, display: "flex", flexDirection: "column", gap: 14 }}>
            {txt.map((r, i) => {
              const k = r.lastIndexOf(" · ");
              const label = r.slice(0, k), value = r.slice(k + 3);
              const aa = inA(f, at[i]);
              return (
                <div key={i} style={{ opacity: aa, transform: `translateX(${(1 - aa) * -40}px)`, background: PLATE, borderRadius: 14, borderLeft: `8px solid ${C.accent}`, padding: "14px 24px", boxSizing: "border-box" }}>
                  <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 27, letterSpacing: 2.5, lineHeight: 1.2, color: "#d5dae2", textShadow: SH }}>{label}</div>
                  <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 78, lineHeight: 1.0, color: C.ink, textShadow: SH }}>{value}</div>
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      );
    }
    case "G09_v2": {
      const [l1, l2] = txt[0].split(": ");
      return (
        <AbsoluteFill>
          <Box x={x} y={y} w={w} a={a} dx={dx}>
            {big(l1 + ":", 40, "#d5dae2")}
            <div style={{ height: 4 }} />
            <div style={{ transform: `scale(${interpolate(f, [8, 16], [1.06, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })})`, transformOrigin: "left center", opacity: inA(f, 8, 5) }}>{big(l2, 104, C.accent)}</div>
            <div style={{ height: 14 }} />
            {mono(p.sub ?? "", 34, "#e8ecf2")}
          </Box>
        </AbsoluteFill>
      );
    }
    case "CON_G1_v2": {
      const at = p.beats ?? [0, 32, 66];
      return (
        <AbsoluteFill>
          <div style={{ position: "absolute", left: x, top: y, width: w, display: "flex", flexDirection: "column", gap: 12 }}>
            {txt.map((r, i) => {
              const aa = inA(f, at[i]);
              const last = i === txt.length - 1;
              const k = r.indexOf(" MIN ");
              return (
                <div key={i} style={{ opacity: aa, transform: `translateX(${(1 - aa) * -40}px)`, background: PLATE, borderRadius: 14, borderLeft: `8px solid ${last ? "rgba(232,236,242,0.5)" : C.accent}`, padding: last ? "10px 24px" : "12px 24px", boxSizing: "border-box" }}>
                  {last ? (
                    <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 34, letterSpacing: 4, color: "#d5dae2", textShadow: SH }}>{r}</div>
                  ) : (
                    <div style={{ display: "flex", alignItems: "baseline", gap: 18, whiteSpace: "nowrap" }}>
                      <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 64, color: C.ink, textShadow: SH }}>{r.slice(0, k + 4)}</span>
                      <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 32, letterSpacing: 3, color: "#d5dae2", textShadow: SH }}>{r.slice(k + 5)}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      );
    }
    default:
      return <AbsoluteFill />;
  }
};

/** Opaque black cards: G05a (glitched), G05b (reboot with fast-forward clock), G15 (end). */
export const CardV2: React.FC<CueV2Props> = (p) => {
  const f = useCurrentFrame();
  const txt = Array.isArray(p.text) ? p.text[0] : p.text;
  if (p.cue === "G15_v2") {
    return (
      <AbsoluteFill style={{ background: C.black, alignItems: "center", justifyContent: "center" }}>
        <Img src={staticFile("illumaesthetic_logo.png")} style={{ width: 900, opacity: inA(f, 0, 12) }} />
        {p.cta ? <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 40, letterSpacing: 3, color: "#b4bbc6", marginTop: 56, opacity: inA(f, 14) }}>{p.cta}</div> : null}
      </AbsoluteFill>
    );
  }
  const glitchy = (txtStr: string, size: number, g: number) => {
    const jx = (random(`a${f}`) - 0.5) * 24 * g, jy = (random(`b${f}`) - 0.5) * 8 * g;
    const base: React.CSSProperties = { position: "absolute", left: 0, right: 0, top: 0, bottom: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: SANS, fontWeight: 700, fontSize: size, letterSpacing: 8 };
    const slice = (k: number) => ({ clipPath: `inset(${k * 11}% 0 ${100 - k * 11 - 9}% 0)`, transform: `translateX(${(random(`s${f}${k}`) - 0.5) * 120 * g}px)` });
    return (
      <>
        <div style={{ ...base, color: "#ff2a2a", transform: `translate(${jx + 9 * g}px,${jy}px)`, mixBlendMode: "screen", opacity: 0.9 }}>{txtStr}</div>
        <div style={{ ...base, color: "#19e6ff", transform: `translate(${jx - 9 * g}px,${-jy}px)`, mixBlendMode: "screen", opacity: 0.9 }}>{txtStr}</div>
        <div style={{ ...base, color: C.ink, transform: `translate(${jx}px,${jy}px)` }}>{txtStr}</div>
        {g > 0.2 && [1, 3, 6].map((k) => <div key={k} style={{ ...base, color: C.ink, ...slice(k) }}>{txtStr}</div>)}
      </>
    );
  };
  if (p.cue === "G05a_v2") {
    const g = f < 6 ? 1 : f < 10 ? 0.4 : Math.floor(f / 3) % 4 === 0 ? 0.35 : 0.08; // hard hit, settles, small twitches
    const flash = f < 2 ? 0.25 : 0;
    return (
      <AbsoluteFill style={{ background: "#000" }}>
        <AbsoluteFill style={{ background: `rgba(255,1,0,${flash})` }} />
        {glitchy(txt, 132, g)}
        <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(0deg, rgba(255,255,255,0.05) 0 2px, transparent 2px 5px)" }} />
      </AbsoluteFill>
    );
  }
  // G05b: REBOOTING... with CLOCK 1 fast-forward (linear in frame index, no easing; lands exactly and holds)
  const a = p.from ?? 340, b = p.to ?? 716;
  const land = Math.max(1, p.frames - 10);
  const pr = Math.min(1, f / land);
  const v = Math.floor(a + (b - a) * pr + 1e-9);
  const chev = Math.floor(f / 3) % 4;
  const holding = f >= land;
  return (
    <AbsoluteFill style={{ background: "#000", alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "absolute", top: 250, fontFamily: SANS, fontWeight: 700, fontSize: 96, letterSpacing: 8, color: C.ink, opacity: 0.55 + 0.45 * Math.abs(Math.sin(f / 7)) }}>{txt}</div>
      <div style={{ position: "absolute", top: 480, display: "flex", alignItems: "center", gap: 36 }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: 6, color: "#9aa2ae", writingMode: "horizontal-tb" }}>CLOCK 1</div>
      </div>
      <div style={{ position: "absolute", top: 530, display: "flex", alignItems: "center", gap: 44 }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 250, color: holding ? C.ink : C.accent, fontVariantNumeric: "tabular-nums", letterSpacing: 2 }}>{mmss(v)}</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 120, color: C.accent, opacity: holding ? 0 : 1, width: 160 }}>{">".repeat(chev + 1)}</div>
      </div>
    </AbsoluteFill>
  );
};

/** Dramatic glitch treatment overlay for C_02 (freeze): scanlines, red edge, tear bands. 1080p alpha. */
export const FxGlitch: React.FC<CueV2Props> = (p) => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 2) % 3;
  const bands = [0, 1, 2, 3].map((i) => ({ y: random(`fy${f}${i}`) * 1000, h: 10 + random(`fh${f}${i}`) * 50, o: (random(`fo${f}${i}`) - 0.5) * 80 }));
  const hit = interpolate(f, [0, 3, p.frames - 1], [1, 0.6, 0.25], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: k === 1 ? 0.55 : 1 }}>
      <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(0deg, rgba(0,0,0,0.28) 0 2px, transparent 2px 5px)" }} />
      <AbsoluteFill style={{ boxShadow: `inset 0 0 220px 40px rgba(255,1,0,${0.55 * hit})` }} />
      {bands.map((b, i) => (
        <div key={i} style={{ position: "absolute", left: 0, right: 0, top: b.y, height: b.h, background: i % 2 ? "rgba(25,230,255,0.16)" : "rgba(255,42,42,0.18)", transform: `translateX(${b.o}px)`, mixBlendMode: "screen" }} />
      ))}
    </AbsoluteFill>
  );
};
