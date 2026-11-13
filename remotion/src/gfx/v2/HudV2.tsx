import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, interpolate, random, useCurrentFrame } from "remotion";
import { C, FPS, MONO, SANS } from "../theme";
import { ClockState, Face, fr, textOf } from "../HudRail";

/**
 * HUD_v2: compact overlay cluster on full-frame footage. Rendered as ONE transparent ProRes 4444 strip
 * covering the top 270 px of the frame (crop x=0,y=0,w=1920,h=270) for the whole v2 timeline.
 * Time values are linear in the frame index (no easing). Props from scripts/gen_gfx_v2.py.
 */
export type SegV2 = {
  id: string; t0: number; t1: number; visible: boolean; corner: "TR" | "TL"; chapter: string;
  c1: ClockState; t2: ClockState;
  red?: boolean; pill?: string; glyph?: string; sub?: string; glitch?: boolean; hideClock?: boolean;
};
export type HudV2Props = {
  fps: number; width: number; height: number; durationInFrames: number;
  segments: SegV2[]; chips: { text: string; t0: number; hl: boolean }[]; chipsOut: number; t2Appear: number;
  plateAlpha: number;
};
export const hudV2Defaults: HudV2Props = {
  fps: FPS, width: 1920, height: 270, durationInFrames: 48, segments: [], chips: [], chipsOut: 0, t2Appear: 1e9, plateAlpha: 0.55,
};
export const calculateHudV2Metadata: CalculateMetadataFunction<HudV2Props> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: props.width, height: props.height,
});

const SH = "0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.6)";

export const HudV2: React.FC<HudV2Props> = (props) => {
  const f = useCurrentFrame();
  const { segments: segs, fps } = props;
  const t = f / fps;
  const bounds = segs.map((s) => [fr(s.t0, fps), fr(s.t1, fps)] as const);
  let si = bounds.findIndex(([a, b]) => f >= a && f < b);
  if (si < 0) si = segs.length - 1;
  const seg = segs[si];
  if (!seg || !seg.visible) return <AbsoluteFill />;
  const [f0, f1] = bounds[si];
  const lf = f - f0, n = f1 - f0;
  const prev = si > 0 ? segs[si - 1] : null;
  const wasHidden = !prev || !prev.visible;
  const fade = wasHidden ? interpolate(lf, [0, 6], [0, 1], { extrapolateRight: "clamp" }) : 1;

  const prevText = (key: "c1" | "t2"): string | null => {
    if (!prev || !prev.visible || prev[key].k === "hidden") return null;
    const [pa, pb] = bounds[si - 1];
    return textOf(prev[key], pb - pa - 1, pb - pa);
  };
  const face = (key: "c1" | "t2") => {
    const cur = textOf(seg[key], lf, n);
    if (wasHidden) return { cur, prev: null as string | null, rf: 99 };
    const pv = prevText(key);
    return { cur, prev: pv, rf: pv === textOf(seg[key], 0, n) ? 99 : lf };
  };

  const post = seg.t2.k !== "hidden";
  const appear = post ? interpolate(f - fr(props.t2Appear, fps), [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 0;
  const finalState = seg.c1.k === "final";
  const left = seg.corner === "TR" ? 1480 : 40;
  const PW = 400;
  const plateBg = `rgba(0,0,0,${props.plateAlpha})`;
  const red = !!seg.red;
  const digitColor = red ? C.accent : seg.c1.k === "notstarted" ? C.grey : C.ink;
  const stillPulse = 0.65 + 0.35 * Math.abs(Math.sin(f / 5));

  // glitch: RGB split + jitter + scanlines on the whole cluster
  const g = !!seg.glitch;
  const jx = g ? Math.round((random(`gx${f}`) - 0.5) * 18) : 0;
  const jy = g ? Math.round((random(`gy${f}`) - 0.5) * 6) : 0;
  const stutter = g && Math.floor(lf / 2) % 3 === 1;

  const Plate: React.FC<{ top: number; h: number; border?: boolean; children: React.ReactNode }> = ({ top, h, border, children }) => (
    <div style={{ position: "absolute", left, top, width: PW, height: h, background: plateBg, borderRadius: 12, boxSizing: "border-box", border: border ? `3px solid ${C.accent}` : "3px solid transparent" }}>{children}</div>
  );
  const Lbl: React.FC<{ children: React.ReactNode; top: number; size?: number }> = ({ children, top, size = 24 }) => (
    <div style={{ position: "absolute", left: 20, top, display: "flex", alignItems: "center", gap: 12, fontFamily: MONO, fontWeight: 700, fontSize: size, letterSpacing: 3, color: "#c3c9d3", textShadow: SH, whiteSpace: "nowrap" }}>{children}</div>
  );
  const Digits: React.FC<{ fc: ReturnType<typeof face>; size: number; top: number; right?: number }> = ({ fc, size, top, right = 20 }) => (
    <div style={{ position: "absolute", right, top, textShadow: SH }}>
      <Face cur={fc.cur} prev={fc.prev} rf={fc.rf} size={size} color={digitColor} frame={f} />
    </div>
  );

  const c1f = face("c1"), t2f = face("t2");
  const mainKey = post ? "t2" : "c1";
  const mainFace = post ? t2f : c1f;
  const mainSize = finalState ? 56 : 62;
  const rowAh = 96;
  const subTop = 40 + rowAh + 8;
  let y = 40;
  const els: React.ReactNode[] = [];
  if (!seg.hideClock) {
    els.push(
      <Plate key="a" top={y} h={rowAh} border={red}>
        <Lbl top={rowAh / 2 - (seg.glyph || seg.sub ? 26 : 15)}>
          <span>{post ? "TIMER 2" : "CLOCK 1"}</span>
          {mainKey === "t2" && seg.t2.k === "paused" && (
            <span style={{ display: "flex", gap: 5 }}><span style={{ width: 6, height: 20, background: C.ink }} /><span style={{ width: 6, height: 20, background: C.ink }} /></span>
          )}
        </Lbl>
        {seg.glyph && (
          <div style={{ position: "absolute", left: 20, top: rowAh / 2 + 6, fontFamily: MONO, fontWeight: 800, fontSize: 26, letterSpacing: 1, color: C.accent, textShadow: SH, opacity: 0.6 + 0.4 * Math.abs(Math.sin(f / 3)) }}>{seg.glyph}</div>
        )}
        {!seg.glyph && seg.sub && (
          <div style={{ position: "absolute", left: 20, top: rowAh / 2 + 8, fontFamily: MONO, fontWeight: 700, fontSize: 18, letterSpacing: 2, color: "#c3c9d3", textShadow: SH, whiteSpace: "nowrap" }}>{seg.sub}</div>
        )}
        <Digits fc={mainFace} size={mainSize} top={(rowAh - Math.round(mainSize * 1.1)) / 2 - 3} />
      </Plate>
    );
    y += rowAh + 8;
    if (post) {
      els.push(
        <div key="b" style={{ opacity: appear }}>
          <Plate top={y} h={52} border={red}>
            <Lbl top={9} size={22}>CLOCK 1</Lbl>
            <Digits fc={c1f} size={36} top={(52 - 40) / 2 - 3} />
          </Plate>
        </div>
      );
      y += 52 + 8;
    }
    if (seg.pill) {
      els.push(
        <Plate key="pill" top={y} h={40} border>
          <div style={{ position: "absolute", left: 20, right: 20, top: 0, bottom: 0, display: "flex", alignItems: "center", gap: 12, fontFamily: MONO, fontWeight: 800, fontSize: 24, letterSpacing: 2, color: C.accent, opacity: stillPulse, textShadow: SH }}>{seg.pill}</div>
        </Plate>
      );
      y += 40 + 8;
    }
  }
  if (seg.chapter) {
    const chapChanged = !!prev && prev.visible && prev.chapter !== seg.chapter;
    const cIn = chapChanged || wasHidden ? interpolate(lf, [0, 8], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 1;
    const fs = Math.min(26, 372 / (seg.chapter.length * 0.66));
    els.push(
      <div key="tag" style={{ opacity: cIn }}>
        <Plate top={y} h={40}>
          <div style={{ position: "absolute", left: 14, right: 14, top: 0, bottom: 0, display: "flex", alignItems: "center", justifyContent: seg.corner === "TR" ? "flex-end" : "flex-start", fontFamily: SANS, fontWeight: 600, fontSize: fs, letterSpacing: 1.5, color: C.ink, textShadow: SH, whiteSpace: "nowrap" }}>
            <span style={{ width: 4, height: 20, background: C.accent, marginRight: 10, flex: "none" }} />{seg.chapter}
          </div>
        </Plate>
      </div>
    );
  }
  void subTop;

  // bet tally (top-left pills), only while the HUD is visible
  const chips = props.chips.map((c, i) => {
    const cf = f - fr(c.t0, fps);
    const outF = f - (fr(props.chipsOut, fps) - 6);
    if (cf < 0 || t >= props.chipsOut) return null;
    const a = interpolate(cf, [0, 6], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) * (outF > 0 ? 1 - outF / 6 : 1);
    const wds = [104, 136, 136];
    const xs = [40, 40 + 104 + 12, 40 + 104 + 12 + 136 + 12];
    return (
      <div key={c.text} style={{ position: "absolute", left: xs[i] - (1 - a) * 14, top: 40, width: wds[i], height: 46, opacity: a, boxSizing: "border-box", display: "flex", alignItems: "center", justifyContent: "center",
        background: plateBg, borderRadius: 23, fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: 1, color: c.hl ? C.ink : "#b4bbc6", textShadow: SH,
        border: `2px solid ${c.hl ? C.ink : "rgba(232,236,242,0.35)"}`, borderLeft: c.hl ? `8px solid ${C.accent}` : undefined }}>{c.text}</div>
    );
  });

  const cluster = <AbsoluteFill>{els}</AbsoluteFill>;
  return (
    <AbsoluteFill style={{ opacity: fade * (stutter ? 0.4 : 1) }}>
      {g && (
        <>
          <AbsoluteFill style={{ transform: `translate(${jx + 7}px, ${jy}px)`, opacity: 0.85, mixBlendMode: "screen" }}>
            <AbsoluteFill style={{ filter: "grayscale(1) brightness(0.1) sepia(1) hue-rotate(-50deg) saturate(8)" }}>{cluster}</AbsoluteFill>
          </AbsoluteFill>
          <AbsoluteFill style={{ transform: `translate(${jx - 7}px, ${-jy}px)`, opacity: 0.85 }}>
            <AbsoluteFill style={{ filter: "grayscale(1) brightness(0.1) sepia(1) hue-rotate(130deg) saturate(8)" }}>{cluster}</AbsoluteFill>
          </AbsoluteFill>
        </>
      )}
      <AbsoluteFill style={{ transform: `translate(${jx}px, ${jy}px)` }}>{cluster}</AbsoluteFill>
      {g && <div style={{ position: "absolute", left, top: 40, width: PW, height: 150, borderRadius: 12, backgroundImage: "repeating-linear-gradient(0deg, rgba(0,0,0,0.35) 0 2px, transparent 2px 5px)" }} />}
      {chips}
    </AbsoluteFill>
  );
};
