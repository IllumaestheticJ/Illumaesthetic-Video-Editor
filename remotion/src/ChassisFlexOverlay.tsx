import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import side from "./nbSideOutline.json";
import rear from "./nbRearOutline.json";

/**
 * Corner "reference" overlay for IRL footage: a small panel showing how the chassis flexes
 *   mode "bumps"     - side view, bumps pass under the front then rear wheel, body bends between the axles
 *   mode "cornering" - rear view, front and rear of the car roll by different amounts (= twist)
 * Outlines are traced from the real NB exterior scan. Movement is exaggerated and labelled so; no numbers.
 * Rendered as transparent ProRes 4444 at the footage size; the panel sits in one corner.
 */

export type ChassisFlexOverlayProps = {
  mode: "bumps" | "cornering";
  corner: "br" | "bl" | "tr" | "tl";
  plate: number; // 0..1 opacity of the dark backing plate
  background: "transparent" | "black";
};

export const chassisFlexOverlayDefaults: ChassisFlexOverlayProps = {
  mode: "bumps",
  corner: "br",
  plate: 0.72,
  background: "transparent",
};

export const CFO_FPS = 24000 / 1001;
export const CFO_SECONDS = 5;

const INK = "#e8ecf2";
const HOT: number[] = [255, 106, 44];
const SIDE = side.pts as [number, number][];
const REAR = rear.pts as [number, number][];

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const heat = (t: number) => `rgb(${[232, 236, 242].map((v, i) => Math.round(lerp(v, HOT[i], t))).join(",")})`;
const toPath = (pts: [number, number][]) =>
  pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join(" ") + " Z";
const ease = { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) } as const;

// Panel design space
const PW = 1000;
const PH = 560;

const Arrow: React.FC<{ x: number; y: number; dx: number; dy: number; k: number }> = ({ x, y, dx, dy, k }) => {
  // arrow from (x,y) along (dx,dy) scaled by k (0..1); hidden when tiny
  if (k < 0.04) return null;
  const x2 = x + dx * k;
  const y2 = y + dy * k;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  const h = 13;
  return (
    <g stroke={heat(1)} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" fill="none" opacity={0.35 + 0.65 * k}>
      <line x1={x} y1={y} x2={x2} y2={y2} />
      <path d={`M${x2 - ux * h - uy * h} ${y2 - uy * h + ux * h} L${x2} ${y2} L${x2 - ux * h + uy * h} ${y2 - uy * h - ux * h}`} />
    </g>
  );
};

const Bumps: React.FC<{ t: number }> = ({ t }) => {
  const L = 760; // car length in panel units
  const ox = 120;
  const oy = 190;
  const wr = { x: 0.222, y: 0.222 };
  const wf = { x: 0.8, y: 0.222 };
  const R = 0.071 * L;
  const groundY = oy + wr.y * L + R + 3;
  const H = 46; // bump height

  // Bumps travel right -> left (car is driving to the right).
  const speed = 380;
  const starts = [0.3, 2.1];
  const bumpXs = starts.map((s) => PW + 80 - (t - s) * speed);
  const profile = (x: number) => bumpXs.reduce((a, bx) => a + Math.exp(-(((x - bx) / 58) ** 2)), 0);
  const hf = H * Math.min(1, profile(ox + wf.x * L));
  const hr = H * Math.min(1, profile(ox + wr.x * L));

  // Rigid part: body follows the axles. Flex part: the middle lags behind, the overhangs whip.
  const flexAmt = (hf + hr) * 1.15;
  const strain = Math.min(1, (hf + hr) / H);
  const off = (x: number) => {
    const s = (x - wr.x) / (wf.x - wr.x);
    return -(hr + (hf - hr) * s) + flexAmt * 4 * s * (1 - s) * 0.8;
  };
  const body = toPath(SIDE.map(([x, y]) => [ox + x * L, oy + y * L + off(x)]));
  const ghost = toPath(SIDE.map(([x, y]) => [ox + x * L, oy + y * L]));

  const groundPts: string[] = [];
  for (let x = 40; x <= PW - 40; x += 8) groundPts.push(`${x} ${(groundY - H * Math.min(1, profile(x))).toFixed(1)}`);

  return (
    <>
      <defs>
        <linearGradient id="sg" gradientUnits="userSpaceOnUse" x1={ox} y1={0} x2={ox + L} y2={0}>
          <stop offset="0.25" stopColor={INK} />
          <stop offset="0.5" stopColor={heat(strain)} />
          <stop offset="0.75" stopColor={INK} />
        </linearGradient>
      </defs>
      <polyline points={groundPts.join(" ")} fill="none" stroke={INK} strokeOpacity={0.7} strokeWidth={3} strokeLinejoin="round" />
      <path d={ghost} fill="none" stroke={INK} strokeOpacity={0.3} strokeWidth={2} strokeDasharray="8 8" />
      {[
        { w: wr, h: hr },
        { w: wf, h: hf },
      ].map(({ w, h }, i) => (
        <g key={i} fill="none" stroke={INK}>
          <circle cx={ox + w.x * L} cy={oy + w.y * L - h} r={R} strokeWidth={5} />
          <circle cx={ox + w.x * L} cy={oy + w.y * L - h} r={R * 0.55} strokeWidth={2} strokeOpacity={0.6} />
          <Arrow x={ox + w.x * L} y={groundY + 78} dx={0} dy={-58} k={h / H} />
        </g>
      ))}
      <path d={body} fill="none" stroke="url(#sg)" strokeWidth={14} opacity={0.5 * strain} filter="url(#cfoGlow)" />
      <path d={body} fill="none" stroke="url(#sg)" strokeWidth={5} strokeLinejoin="round" />
    </>
  );
};

const Cornering: React.FC<{ t: number }> = ({ t }) => {
  const W = 430; // car width in panel units
  const cx = PW / 2;
  const top = 120;
  const bodyH = rear.aspect * W;
  const groundY = top + bodyH + 34;
  const pivot: [number, number] = [cx, groundY - 40]; // roll centre, near the ground

  // Lateral load: builds, holds with a little life, releases.
  const g =
    interpolate(t, [0.5, 1.4], [0, 1], ease) * interpolate(t, [3.7, 4.4], [1, 0], ease) * (0.9 + 0.1 * Math.sin(t * 5.2));
  const rearDeg = 3 * g; // rear of the car rolls a little...
  const frontDeg = 10 * g; // ...the front rolls more: the difference is chassis twist
  const strain = Math.min(1, g);

  const rot = (deg: number) =>
    toPath(
      REAR.map(([x, y]) => {
        const px = cx - W / 2 + x * W - pivot[0];
        const py = top + y * W - pivot[1];
        const a = (deg * Math.PI) / 180;
        return [pivot[0] + px * Math.cos(a) - py * Math.sin(a), pivot[1] + px * Math.sin(a) + py * Math.cos(a)];
      }),
    );
  const tyreW = 62;
  const tyreH = 74;
  const tx = [cx - W * 0.4 - tyreW / 2, cx + W * 0.4 - tyreW / 2];

  return (
    <>
      <line x1={90} x2={PW - 90} y1={groundY} y2={groundY} stroke={INK} strokeOpacity={0.7} strokeWidth={3} />
      {tx.map((x, i) => (
        <rect key={i} x={x} y={groundY - tyreH} width={tyreW} height={tyreH} rx={14} fill="none" stroke={INK} strokeWidth={4} strokeOpacity={0.85} />
      ))}
      <path d={rot(0)} fill="none" stroke={INK} strokeOpacity={0.25} strokeWidth={2} strokeDasharray="8 8" />
      {/* front of the car */}
      <path d={rot(frontDeg)} fill="none" stroke={heat(strain)} strokeWidth={3.5} strokeDasharray="14 9" strokeOpacity={0.95} />
      {/* rear of the car */}
      <path d={rot(rearDeg)} fill="none" stroke={INK} strokeWidth={14} opacity={0.35 * strain} filter="url(#cfoGlow)" />
      <path d={rot(rearDeg)} fill="none" stroke={INK} strokeWidth={5} strokeLinejoin="round" />

      {/* cornering force at the tyres, extra load on the outside tyre */}
      <Arrow x={tx[0] + tyreW + 26} y={groundY + 30} dx={-120} dy={0} k={g} />
      <Arrow x={tx[1] + tyreW + 26} y={groundY + 30} dx={-120} dy={0} k={g} />
      <Arrow x={tx[1] + tyreW / 2 + 70} y={groundY - 6} dx={0} dy={-80} k={g} />

      <g fontFamily="JetBrains Mono, monospace" fontSize={22} letterSpacing="0.12em" opacity={g}>
        <text x={cx + W / 2 + 46} y={top + 26} fill={heat(1)}>
          FRONT
        </text>
        <text x={cx + W / 2 + 46} y={top + 60} fill={INK}>
          REAR
        </text>
      </g>
    </>
  );
};

export const ChassisFlexOverlay: React.FC<ChassisFlexOverlayProps> = ({ mode, corner, plate, background }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const u = width / 3840;

  const scale = 1.32 * u; // panel is ~34% of frame width
  const margin = 150 * u;
  const w = PW * scale;
  const h = PH * scale;
  const left = corner.endsWith("l") ? margin : width - margin - w;
  const topPx = corner.startsWith("t") ? margin : height - 290 * u - h; // bottom corners clear the caption line

  const appear = interpolate(t, [0, 0.4], [0, 1], ease) * interpolate(t, [CFO_SECONDS - 0.45, CFO_SECONDS - 0.05], [1, 0], ease);

  return (
    <AbsoluteFill style={{ backgroundColor: background === "black" ? "#000" : "transparent" }}>
      <div
        style={{
          position: "absolute",
          left,
          top: topPx + (1 - appear) * 30 * u,
          width: w,
          height: h,
          opacity: appear,
          borderRadius: 28 * u,
          backgroundColor: `rgba(8,10,14,${plate})`,
          border: `${2 * u}px solid rgba(232,236,242,0.28)`,
          overflow: "hidden",
        }}
      >
        <svg width={w} height={h} viewBox={`0 0 ${PW} ${PH}`}>
          <defs>
            <filter id="cfoGlow" x="-20%" y="-40%" width="140%" height="180%">
              <feGaussianBlur stdDeviation={7} />
            </filter>
          </defs>
          <g fontFamily="Inter Display, Inter, sans-serif" fill={INK}>
            <text x={44} y={70} fontSize={40} fontWeight={700} letterSpacing="0.06em">
              CHASSIS FLEX
            </text>
          </g>
          <g fontFamily="JetBrains Mono, monospace" letterSpacing="0.12em">
            <text x={PW - 44} y={68} fontSize={26} textAnchor="end" fill={heat(1)}>
              {mode === "bumps" ? "OVER BUMPS" : "CORNERING"}
            </text>
            <text x={44} y={PH - 30} fontSize={17} fill={INK} fillOpacity={0.55}>
              MOVEMENT EXAGGERATED
            </text>
          </g>
          {mode === "bumps" ? <Bumps t={t} /> : <Cornering t={t} />}
        </svg>
      </div>
    </AbsoluteFill>
  );
};
