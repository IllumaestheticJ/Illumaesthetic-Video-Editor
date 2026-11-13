import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, interpolate, useCurrentFrame } from "remotion";
import { C, FPS, MONO, SANS } from "./theme";

/**
 * HUD rail strip (1920x160), one transparent ProRes 4444 for the whole timeline.
 * Props come from scripts/gen_gfx_props.py (edl.json). Left: CLOCK 1 / TIMER 2 (+ bet tally).
 * Centre 410..1510 is the empty caption zone. Right: chapter label.
 * Time values are linear in the frame index (no easing), except the symbolic crash fast-forward.
 */
export type ClockState =
  | { k: "hidden" }
  | { k: "notstarted" }
  | { k: "unknown" }
  | { k: "time" | "paused" | "ff"; a: number; b: number }
  | { k: "final"; label: string };
export type Seg = { id: string; t0: number; t1: number; mode: "plate" | "overlay" | "hidden"; chapter: string; c1: ClockState; t2: ClockState };
export type HudRailProps = {
  fps: number; width: number; height: number; durationInFrames: number;
  segments: Seg[]; chips: { text: string; t0: number; hl: boolean }[]; chipsOut: number;
  crash: [number, number]; ffCard: [number, number]; timer2Appear: number;
};
export const hudRailDefaults: HudRailProps = {
  fps: FPS, width: 1920, height: 160, durationInFrames: 48, segments: [], chips: [], chipsOut: 0, crash: [0, 0], ffCard: [0, 0], timer2Appear: 0,
};
export const calculateHudRailMetadata: CalculateMetadataFunction<HudRailProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: props.width, height: props.height,
});

const ROLL = 8;
const mmss = (s: number) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
const fr = (t: number, fps: number) => Math.round(t * fps);

/** text shown by a clock state at local frame lf of a segment of n frames; null = running/unreadable */
function textOf(st: ClockState, lf: number, n: number): string | null {
  const p = n > 1 ? Math.min(1, Math.max(0, lf / (n - 1))) : 1;
  switch (st.k) {
    case "notstarted": return "00:00";
    case "final": return st.label;
    case "time": case "paused": return mmss(Math.floor(st.a + (st.b - st.a) * p));
    case "ff": return mmss(Math.floor(st.a + (st.b - st.a) * Easing.inOut(Easing.cubic)(p) + 1e-9));
    default: return null;
  }
}

const Face: React.FC<{ cur: string | null; prev: string | null; rf: number; size: number; color: string; frame: number }> = ({ cur, prev, rf, size, color, frame }) => {
  const h = Math.round(size * 1.1);
  const w = Math.round(size * 0.6);
  const rolling = rf < ROLL;
  if (cur === null) {
    // running, value not legible: sweeping segment on a track the width of "00:00"
    const tw = w * 5, ph = (frame % 36) / 36;
    const sw = tw * 0.28, x = ph * (tw + sw) - sw;
    const o = rolling && prev !== null ? rf / ROLL : 1;
    return (
      <div style={{ height: h, width: tw, display: "flex", alignItems: "center", opacity: o }}>
        <div style={{ position: "relative", width: tw, height: Math.max(5, size * 0.1), background: C.dim, overflow: "hidden", borderRadius: 3 }}>
          <div style={{ position: "absolute", left: x, width: sw, top: 0, bottom: 0, background: C.ink, opacity: 0.85, borderRadius: 3 }} />
        </div>
      </div>
    );
  }
  const e = Easing.out(Easing.cubic)(Math.min(1, rf / ROLL));
  const chars = cur.split("");
  const pc = prev ? prev.split("") : null;
  const crossfade = rolling && (prev === null || (pc && pc.length !== chars.length));
  return (
    <div style={{ display: "flex", height: h, fontFamily: MONO, fontWeight: 700, fontSize: size, lineHeight: `${h}px`, color, fontVariantNumeric: "tabular-nums", opacity: crossfade ? e : 1 }}>
      {chars.map((ch, i) => {
        const pch = pc && pc.length === chars.length ? pc[i] : ch;
        const roll = rolling && !crossfade && pch !== ch;
        return (
          <div key={i} style={{ width: w, height: h, overflow: "hidden", position: "relative", textAlign: "center" }}>
            {roll ? (
              <>
                <div style={{ position: "absolute", left: 0, right: 0, transform: `translateY(${-h * e}px)`, opacity: 1 - e }}>{pch}</div>
                <div style={{ position: "absolute", left: 0, right: 0, transform: `translateY(${h * (1 - e)}px)`, opacity: e }}>{ch}</div>
              </>
            ) : <div style={{ position: "absolute", left: 0, right: 0 }}>{ch}</div>}
          </div>
        );
      })}
    </div>
  );
};

const Label: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 3, color: C.grey, height: 30, display: "flex", alignItems: "center", gap: 14, whiteSpace: "nowrap" }}>{children}</div>
);

const PauseGlyph = () => (
  <div style={{ display: "flex", gap: 5 }}>
    <div style={{ width: 6, height: 18, background: C.ink }} /><div style={{ width: 6, height: 18, background: C.ink }} />
  </div>
);
const FFGlyph: React.FC<{ frame: number }> = ({ frame }) => (
  <div style={{ display: "flex", gap: 2, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: C.accent, opacity: 0.5 + 0.5 * Math.abs(Math.sin(frame / 4)) }}>{">>"}</div>
);

function splitChapter(s: string): string[] {
  const w = s.split(" ");
  if (s.length <= 11 || w.length < 2) return [s];
  let best: string[] = [s], bm = 1e9;
  for (let i = 1; i < w.length; i++) {
    const a = w.slice(0, i).join(" "), b = w.slice(i).join(" ");
    const m = Math.max(a.length, b.length);
    if (m < bm) { bm = m; best = [a, b]; }
  }
  return best;
}

export const HudRail: React.FC<HudRailProps> = (props) => {
  const f = useCurrentFrame();
  const { segments: segs, fps } = props;
  const t = f / fps;
  const bounds = segs.map((s) => [fr(s.t0, fps), fr(s.t1, fps)] as const);
  let si = bounds.findIndex(([a, b]) => f >= a && f < b);
  if (si < 0) si = segs.length - 1;
  const seg = segs[si];
  const [f0, f1] = bounds[si];
  const lf = f - f0, n = f1 - f0;
  if (seg.mode === "hidden") return <AbsoluteFill />;

  // fade-in after a hidden stretch
  const prevSeg = si > 0 ? segs[si - 1] : null;
  const wasHidden = !prevSeg || prevSeg.mode === "hidden";
  const railOpacity = wasHidden ? interpolate(lf, [0, 6], [0, 1], { extrapolateRight: "clamp" }) : 1;

  const prevText = (key: "c1" | "t2"): string | null => {
    if (!prevSeg || prevSeg[key].k === "hidden") return null;
    const [pa, pb] = bounds[si - 1];
    return textOf(prevSeg[key], pb - pa - 1, pb - pa);
  };
  const rollStart = (key: "c1" | "t2") => {
    // roll only at a cut where the displayed text changes (not after a hidden stretch)
    if (wasHidden) return { cur: textOf(seg[key], lf, n), prev: null, rf: 99 };
    const cur = textOf(seg[key], lf, n);
    const pv = prevText(key);
    // continuity inside a split segment (same values): no roll
    return { cur, prev: pv, rf: pv === textOf(seg[key], 0, n) ? 99 : lf };
  };

  // layout phase
  const bet = t >= 12.6 && t < props.chipsOut;
  const post = seg.t2.k !== "hidden";
  const finalState = seg.c1.k === "final";
  const shrink = interpolate(t, [props.timer2Appear, props.timer2Appear + 10 / fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pre = t < props.chipsOut ? (bet ? 56 : 84) : 84;
  const c1Size = post ? (finalState ? 38 : 38) : (t >= props.timer2Appear - 0.01 ? 38 : pre);
  const c1SizeA = post ? 38 : interpolate(shrink, [0, 1], [pre, 38]);
  void c1Size;
  const t2Size = finalState ? 52 : 64;
  const c1 = rollStart("c1"), t2 = rollStart("t2");
  const c1Color = seg.c1.k === "notstarted" ? C.grey : C.ink;
  const crashOn = t >= props.crash[0] && t < props.crash[1];
  const ffOn = seg.c1.k === "ff";
  const c1X = 48;
  const t2X = finalState ? 212 : 196;

  // chapter
  const chap = seg.chapter;
  const prevChap = prevSeg && prevSeg.mode !== "hidden" ? prevSeg.chapter : null;
  const chapChanged = prevChap !== null && prevChap !== chap;
  const cIn = chapChanged || wasHidden ? interpolate(lf, [0, 8], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 1;
  const lines = splitChapter(chap);

  return (
    <AbsoluteFill style={{ background: seg.mode === "plate" ? C.black : "transparent", opacity: railOpacity }}>
      {seg.mode === "plate" && <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 1, background: "rgba(232,236,242,0.14)" }} />}

      {/* CLOCK 1 */}
      <div style={{ position: "absolute", left: c1X, bottom: 34 }}>
        <Label>
          <span>CLOCK 1</span>
          {crashOn && (
            <span style={{ background: C.accent, color: "#fff", padding: "0 10px", height: 26, lineHeight: "26px", fontSize: 20, letterSpacing: 2, opacity: t - props.crash[0] < 1.5 ? (Math.floor((t - props.crash[0]) * 4) % 2 === 0 ? 1 : 0.35) : 1 }}>CRASH</span>
          )}
          {ffOn && <FFGlyph frame={f} />}
        </Label>
        <Face cur={c1.cur} prev={c1.prev} rf={c1.rf} size={c1SizeA} color={c1Color} frame={f} />
      </div>

      {/* TIMER 2 */}
      {post && (
        <div style={{ position: "absolute", left: t2X, bottom: 34 }}>
          <Label>
            <span>TIMER 2</span>
            {seg.t2.k === "paused" && <PauseGlyph />}
          </Label>
          <Face cur={t2.cur} prev={t2.prev} rf={t2.rf} size={t2Size} color={C.ink} frame={f} />
        </div>
      )}

      {/* bet tally */}
      {props.chips.map((c, i) => {
        const cf = f - fr(c.t0, fps);
        const outF = f - (fr(props.chipsOut, fps) - 6);
        if (cf < 0 || t >= props.chipsOut) return null;
        const a = interpolate(cf, [0, 6], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) * (outF > 0 ? 1 - outF / 6 : 1);
        return (
          <div key={c.text} style={{ position: "absolute", left: 236 + (1 - a) * -12, top: 18 + i * 42, width: 150, height: 36, opacity: a, boxSizing: "border-box", display: "flex", alignItems: "center", justifyContent: "center", gap: 0,
            fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: 1, color: c.hl ? C.ink : C.grey, border: `2px solid ${c.hl ? C.ink : C.dim}`, borderLeft: `6px solid ${c.hl ? C.accent : C.dim}`, background: c.hl ? "rgba(232,236,242,0.08)" : "transparent" }}>
            {c.text}
          </div>
        );
      })}

      {/* chapter label, right-aligned */}
      {chap !== "" && (
        <div style={{ position: "absolute", right: 48, top: 0, bottom: 0, display: "flex", alignItems: "center", justifyContent: "flex-end", opacity: cIn, transform: `translateY(${(1 - cIn) * 8}px)` }}>
          <div style={{ width: 5, height: lines.length * 40, background: C.accent, marginRight: 18 }} />
          <div style={{ textAlign: "right", fontFamily: SANS, fontWeight: 600, fontSize: 38, letterSpacing: 6, lineHeight: "40px", color: C.ink, whiteSpace: "nowrap" }}>
            {lines.map((l) => <div key={l}>{l}</div>)}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
