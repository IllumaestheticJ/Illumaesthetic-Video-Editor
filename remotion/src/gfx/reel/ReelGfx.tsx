import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "../theme";

/**
 * IS350 reels: ALL graphics of one 9:16 reel as one transparent overlay (1080x1920, 30 fps, ProRes 4444 alpha), except `logo`,
 * which is an opaque black card. Same system as the long-form v2 graphics (theme, 58 % black content-sized plates with EQUAL
 * padding and the red bar, Inter Display titles, JetBrains Mono numbers, caption plate), sized for a phone.
 * Safe area for Reels/TikTok UI (brief): text only inside x 60-960, y 220-1500.
 * Props from projects/lexus-is350-reels/tools/gfx_props.py. Times in seconds on the reel timeline.
 */
type Row = { label: string; v0: number; v1?: number; text?: string; big?: boolean };
export type ReelItem =
  | { kind: "title"; t0: number; t1: number; lines: string[]; y?: number }
  | { kind: "pills"; t0: number; t1: number; y?: number; pills: { text: string; at: number; hl?: boolean }[] }
  | { kind: "clock"; t0: number; t1: number; rows: Row[]; red?: boolean; pill?: string; pillAt?: number; fadeIn?: boolean; y?: number }
  | { kind: "result"; t0: number; t1: number; y?: number; rows: { value: string; label: string; at: number }[]; footer?: { text: string; at: number } }
  | { kind: "tag"; t0: number; t1: number; text: string; y?: number }
  | { kind: "label"; t0: number; t1: number; text: string; sub?: string; y?: number }
  | { kind: "cap"; t0: number; t1: number; lines: string[] }
  | { kind: "logo"; t0: number; t1: number; cta: string }
  | { kind: "tease"; t0: number; t1: number; lines: string[]; sub: string };
export type ReelGfxProps = { fps: number; durationInFrames: number; items: ReelItem[] };
export const reelGfxDefaults: ReelGfxProps = { fps: 30, durationInFrames: 60, items: [] };
export const calculateReelGfxMetadata: CalculateMetadataFunction<ReelGfxProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: 1080, height: 1920,
});

const X0 = 60, X1 = 960; // safe text column (right 120 px kept clear)
const SH = "0 1px 3px rgba(0,0,0,0.9), 0 0 10px rgba(0,0,0,0.6)";
const PLATE = "rgba(0,0,0,0.58)";
const PAD = 28;
const ease = Easing.out(Easing.cubic);
const inA = (f: number, at = 0, d = 7) => interpolate(f, [at, at + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
const mmss = (s: number) => { const v = Math.max(0, Math.floor(s + 1e-6)); return `${String(Math.floor(v / 60)).padStart(2, "0")}:${String(v % 60).padStart(2, "0")}`; };

/** Content-sized plate: equal padding on all four sides (cap-height compensated at the bottom like CueV2's Box). */
const Plate: React.FC<{ children: React.ReactNode; bar?: boolean; barColor?: string; pad?: number; style?: React.CSSProperties }> = ({ children, bar = true, barColor = C.accent, pad = PAD, style }) => (
  <div style={{ width: "fit-content", background: PLATE, borderRadius: 16, padding: `${pad}px ${pad}px ${pad - 6}px`, boxSizing: "border-box", display: "flex", gap: 20, alignItems: "stretch", ...style }}>
    {bar ? <div style={{ width: 8, borderRadius: 4, background: barColor, flex: "none" }} /> : null}
    <div>{children}</div>
  </div>
);
const Col: React.FC<{ y: number; children: React.ReactNode; align?: "flex-start" | "center" }> = ({ y, children, align = "center" }) => (
  <div style={{ position: "absolute", left: X0, width: X1 - X0, top: y, display: "flex", flexDirection: "column", alignItems: align, gap: 14 }}>{children}</div>
);

const Item: React.FC<{ it: ReelItem; f: number; fps: number }> = ({ it, f, fps }) => {
  const lf = f - Math.round(it.t0 * fps);
  const n = Math.round(it.t1 * fps) - Math.round(it.t0 * fps);
  const a = it.t0 <= 0 ? 1 : inA(lf, 0, 6); // the hook text is fully on from frame 0
  switch (it.kind) {
    case "title":
      return (
        <Col y={it.y ?? 250}>
          <div style={{ opacity: a, transform: `translateY(${(1 - a) * -16}px)` }}>
            <Plate>
              {it.lines.map((l, i) => (
                <div key={i} style={{ fontFamily: SANS, fontWeight: 700, fontSize: 60, letterSpacing: 3, lineHeight: 1.1, color: C.ink, textShadow: SH, whiteSpace: "nowrap" }}>{l}</div>
              ))}
            </Plate>
          </div>
        </Col>
      );
    case "pills":
      return (
        <div style={{ position: "absolute", left: X0, width: X1 - X0, top: it.y ?? 560, display: "flex", gap: 16, justifyContent: "center" }}>
          {it.pills.map((p, i) => {
            const pa = inA(f - Math.round(p.at * fps), 0, 5);
            const sc = interpolate(f - Math.round(p.at * fps), [0, 6], [1.15, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
            return (
              <div key={i} style={{ opacity: pa, transform: `scale(${sc})`, background: p.hl ? C.accent : PLATE, borderRadius: 40, padding: "16px 28px 12px",
                fontFamily: MONO, fontWeight: 800, fontSize: 50, letterSpacing: 1, color: C.ink, textShadow: p.hl ? "none" : SH, whiteSpace: "nowrap" }}>{p.text}</div>
            );
          })}
        </div>
      );
    case "clock": {
      const u = n > 1 ? Math.min(1, Math.max(0, lf / n)) : 0;
      const fa = it.fadeIn ? a : 1;
      const red = !!it.red && (it.pillAt === undefined || f >= Math.round(it.pillAt * fps));
      const pillA = it.pill ? inA(f - Math.round((it.pillAt ?? it.t0) * fps), 0, 4) : 0;
      return (
        <div style={{ position: "absolute", left: X0, top: it.y ?? 240, opacity: fa, display: "flex", alignItems: "flex-start", gap: 16 }}>
          <Plate barColor={red ? C.accent : "rgba(232,236,242,0.55)"} pad={22} style={{ border: red ? `3px solid ${C.accent}` : "3px solid transparent" }}>
            {it.rows.map((r, i) => {
              const v = r.v1 === undefined ? r.v0 : r.v0 + (r.v1 - r.v0) * u;
              const big = r.big ?? i === 0;
              return (
                <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 16, marginTop: i ? 6 : 0 }}>
                  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: big ? 28 : 24, letterSpacing: 2, color: "#aab1bc", width: 160 }}>{r.label}</div>
                  <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: big ? 76 : 44, lineHeight: 1.0, color: red && i === 0 ? C.accent : C.ink, fontVariantNumeric: "tabular-nums", textShadow: SH }}>{r.text ?? mmss(v)}</div>
                </div>
              );
            })}
          </Plate>
          {it.pill ? (
            <div style={{ opacity: pillA, marginTop: 18, background: C.accent, borderRadius: 30, padding: "12px 22px 9px", fontFamily: MONO, fontWeight: 800, fontSize: 36, letterSpacing: 2, color: C.ink, whiteSpace: "nowrap" }}>{it.pill}</div>
          ) : null}
        </div>
      );
    }
    case "result":
      return (
        <Col y={it.y ?? 250} align="flex-start">
          {it.rows.map((r, i) => {
            const ra = inA(f - Math.round(r.at * fps), 0, 6);
            return (
              <div key={i} style={{ opacity: ra, transform: `translateX(${(1 - ra) * 40}px)` }}>
                <Plate pad={24}>
                  <div style={{ display: "flex", alignItems: "baseline", gap: 18, whiteSpace: "nowrap" }}>
                    <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 84, lineHeight: 1.0, color: C.ink, textShadow: SH }}>{r.value}</span>
                    <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 38, letterSpacing: 3, color: "#d5dae2", textShadow: SH }}>{r.label}</span>
                  </div>
                </Plate>
              </div>
            );
          })}
          {it.footer ? (
            <div style={{ opacity: inA(f - Math.round(it.footer.at * fps), 0, 6) }}>
              <Plate pad={20} barColor="rgba(232,236,242,0.5)">
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 44, letterSpacing: 4, color: C.ink, textShadow: SH, whiteSpace: "nowrap" }}>{it.footer.text}</div>
              </Plate>
            </div>
          ) : null}
        </Col>
      );
    case "tag":
      return (
        <div style={{ position: "absolute", left: X0, top: it.y ?? 560, opacity: a, transform: `translateX(${(1 - a) * 40}px)` }}>
          <Plate pad={20}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, letterSpacing: 2, color: C.ink, textShadow: SH, whiteSpace: "nowrap" }}>{it.text}</div>
          </Plate>
        </div>
      );
    case "label":
      return (
        <Col y={it.y ?? 1290}>
          <div style={{ opacity: a, transform: `translateY(${(1 - a) * 16}px)` }}>
            <Plate>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 50, letterSpacing: 4, lineHeight: 1.05, color: C.ink, textShadow: SH, whiteSpace: "nowrap" }}>{it.text}</div>
              {it.sub ? <div style={{ marginTop: 12, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 1, color: "#d5dae2", textShadow: SH, whiteSpace: "nowrap" }}>{it.sub}</div> : null}
            </Plate>
          </div>
        </Col>
      );
    case "cap":
      // hard in/out on exact frames (a caption never precedes its first word); bottom edge at y 1480
      return (
        <div style={{ position: "absolute", left: X0, width: X1 - X0, top: 0, height: 1480, display: "flex", flexDirection: "column", justifyContent: "flex-end", alignItems: "center" }}>
          <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 56, lineHeight: "64px", color: C.ink, textAlign: "center", background: "rgba(0,0,0,0.55)", borderRadius: 14, padding: "18px 26px 16px", textShadow: "0 2px 5px rgba(0,0,0,0.9)", maxWidth: X1 - X0 }}>
            {it.lines.map((l, i) => (<div key={i} style={{ whiteSpace: "nowrap" }}>{l}</div>))}
          </div>
        </div>
      );
    case "tease":
      // opaque black card; text block centred in the safe column (x 60-960), vertically at ~45 %
      return (
        <AbsoluteFill style={{ background: C.black }}>
          <div style={{ position: "absolute", left: X0, width: X1 - X0, top: 220, height: 1280, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            {it.lines.map((l, i) => (
              <div key={i} style={{ opacity: inA(lf, i * 4, 7), transform: `translateY(${(1 - inA(lf, i * 4, 7)) * 14}px)`, fontFamily: SANS, fontWeight: 700, fontSize: 104, letterSpacing: 5, lineHeight: 1.08, color: C.ink, whiteSpace: "nowrap", textAlign: "center" }}>{l}</div>
            ))}
            <div style={{ width: 140 * inA(lf, 8, 10), height: 8, borderRadius: 4, background: C.accent, margin: "44px 0 40px" }} />
            <div style={{ opacity: inA(lf, 12, 8), fontFamily: MONO, fontWeight: 700, fontSize: 44, letterSpacing: 3, color: "#d5dae2", whiteSpace: "nowrap" }}>{it.sub}</div>
          </div>
        </AbsoluteFill>
      );
    case "logo":
      return (
        <AbsoluteFill style={{ background: C.black }}>
          <div style={{ position: "absolute", left: 0, width: 1080, top: 0, height: 1920, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", paddingBottom: 140, boxSizing: "border-box" }}>
            <Img src={staticFile("illumaesthetic_logo.png")} style={{ width: 780, opacity: inA(lf, 0, 6) }} />
            <div style={{ marginTop: 64, opacity: inA(lf, 6, 8), textAlign: "center", fontFamily: MONO, fontWeight: 600, fontSize: 44, letterSpacing: 3, lineHeight: 1.3, color: "#c9ced6" }}>
              {it.cta.split("\n").map((l, i) => (<div key={i}>{l}</div>))}
            </div>
          </div>
        </AbsoluteFill>
      );
  }
};

export const ReelGfx: React.FC<ReelGfxProps> = ({ items, fps }) => {
  const f = useCurrentFrame();
  const live = items.filter((it) => f >= Math.round(it.t0 * fps) && f < Math.round(it.t1 * fps));
  // logo card first (opaque), everything else above it
  const opaque = (k: string) => (k === "logo" || k === "tease" ? -1 : 0);
  live.sort((p, q) => opaque(p.kind) - opaque(q.kind));
  return (
    <AbsoluteFill style={{ background: "transparent" }}>
      {live.map((it, i) => <Item key={i} it={it} f={f} fps={fps} />)}
    </AbsoluteFill>
  );
};
