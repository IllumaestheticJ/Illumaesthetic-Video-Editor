import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import outline from "./nbSideOutline.json";

/**
 * 2D explainer overlay: "chassis flex" on the NB Miata.
 * The side outline is traced from the real exterior scan (nbSideOutline.json, nose to the right,
 * x/y normalised by car length). The bend is exaggerated and labelled as such - no numbers.
 *
 * Beats (seconds): 0-1 outline draws on (roof on) · 1-3.5 small flex · 3.5-4.2 roof drops out ·
 * 4.2-7.3 larger flex ("open top") · 7.3-8 fade out.
 * Rendered transparent (ProRes 4444) so the editor can place it over black or footage.
 */

export type ChassisFlexProps = {
  background: "transparent" | "black";
  title: string;
  closedLabel: string;
  openLabel: string;
  note: string;
};

export const chassisFlexDefaults: ChassisFlexProps = {
  background: "transparent",
  title: "CHASSIS FLEX",
  closedLabel: "ROOF ON",
  openLabel: "OPEN TOP",
  note: "MOVEMENT EXAGGERATED FOR ILLUSTRATION",
};

export const CHASSIS_FLEX_FPS = 24000 / 1001;
export const CHASSIS_FLEX_SECONDS = 8;

const INK = "#e8ecf2";
const PTS = outline.pts as [number, number][];

// Roof geometry in outline units (measured on the traced scan outline).
const ROOF_X0 = 0.235; // rear of roof / deck
const ROOF_X1 = 0.52; // top of windshield
const BELT = (x: number) => 0.085 + ((x - ROOF_X0) / (0.672 - ROOF_X0)) * 0.01;
const WHEELS = [
  { x: 0.222, y: 0.222 },
  { x: 0.8, y: 0.222 },
];
const WHEEL_R = 0.071;

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const mix = (c1: number[], c2: number[], t: number) =>
  `rgb(${c1.map((v, i) => Math.round(lerp(v, c2[i], t))).join(",")})`;

export const ChassisFlex: React.FC<ChassisFlexProps> = ({ background, title, closedLabel, openLabel, note }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const u = width / 3840; // design unit (designed at UHD)

  const L = 2500 * u; // car length on screen
  const ox = (width - L) / 2;
  const oy = height * 0.5 - outline.aspect * L * 0.42;

  const ease = { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) } as const;
  const draw = interpolate(t, [0.1, 1.1], [0, 1], ease);
  const open = interpolate(t, [3.5, 4.2], [0, 1], ease); // 0 = roof on, 1 = open top
  const fade = interpolate(t, [7.3, 7.95], [1, 0], ease);
  const flexIn = interpolate(t, [1.0, 1.6], [0, 1], ease);
  const flexOut = interpolate(t, [6.9, 7.3], [1, 0], ease);

  // Bend amount: slow oscillation, bigger once the roof is gone.
  const amp = lerp(0.018, 0.07, open) * flexIn * flexOut;
  const osc = Math.sin((t - 1.0) * Math.PI * 2 * 0.62);
  const A = amp * osc;
  const strain = Math.min(1, Math.abs(A) / 0.07);

  // Beam-style bend about the door opening: ends move one way, middle the other.
  const bend = (x: number) => -A * (4 * (x - 0.51) * (x - 0.51) - 0.335);
  const P = (x: number, y: number, deform = true): [number, number] => [
    ox + x * L,
    oy + (y + (deform ? bend(x) : 0)) * L,
  ];

  const inRoof = (x: number, y: number) => x > ROOF_X0 && x < ROOF_X1 && y < BELT(x);
  const toPath = (pts: [number, number][], close: boolean) =>
    pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join(" ") + (close ? " Z" : "");

  // Open-top outline: the roof run is replaced by a thin windshield frame + the beltline.
  const start = PTS.reduce((best, p, i) => (p[1] > PTS[best][1] ? i : best), 0); // underside: never in the roof
  const ring = [...PTS.slice(start), ...PTS.slice(0, start)];
  const first = ring.findIndex(([x, y]) => inRoof(x, y));
  const last = ring.length - 1 - [...ring].reverse().findIndex(([x, y]) => inRoof(x, y));
  const frame2belt: [number, number][] = [[0.5, 0.013]];
  for (let x = 0.63; x >= ROOF_X0; x -= 0.02) frame2belt.push([x, BELT(x)]);
  const frontFirst = ring[first][0] > ring[last][0];
  const openPts = [...ring.slice(0, first), ...(frontFirst ? frame2belt : [...frame2belt].reverse()), ...ring.slice(last + 1)];

  const closedBody = toPath(PTS.map(([x, y]) => P(x, y)), true);
  const openBody = toPath(openPts.map(([x, y]) => P(x, y)), true);
  const ghost = toPath(PTS.map(([x, y]) => P(x, y, false)), true);
  const roofPts = PTS.filter(([x, y]) => x > ROOF_X0 - 0.01 && x < ROOF_X1 + 0.01 && y < BELT(x) + 0.004).sort(
    (a, b) => a[0] - b[0],
  );
  const roof = toPath(roofPts.map(([x, y]) => P(x, y, false)), false);

  const hot = mix([232, 236, 242], [255, 106, 44], strain);
  const sw = 7 * u;
  const groundY = oy + (WHEELS[0].y + WHEEL_R) * L + 6 * u;

  const arrow = (x: number, dir: 1 | -1, key: string) => {
    // dir 1 = pushing up from the ground, -1 = pushing down
    const [px] = P(x, 0);
    const len = (70 + 150 * strain) * u;
    const base = dir === 1 ? groundY + 250 * u : oy - 330 * u;
    const tip = dir === 1 ? base - len : base + len;
    const h = 30 * u;
    return (
      <g key={key} opacity={0.25 + 0.75 * strain} stroke={hot} strokeWidth={8 * u} strokeLinecap="round" fill="none">
        <line x1={px} y1={base} x2={px} y2={tip} />
        <path d={`M${px - h} ${tip + dir * h} L${px} ${tip} L${px + h} ${tip + dir * h}`} strokeLinejoin="round" />
      </g>
    );
  };
  // Loads flip with the bend direction: wheels push up while the middle sags, and vice versa.
  const up = osc >= 0;

  const label = open < 0.5 ? closedLabel : openLabel;
  const labelOpacity = Math.abs(open - 0.5) * 2 * interpolate(t, [1.0, 1.5], [0, 1], ease);
  const titleIn = interpolate(t, [0.2, 0.9], [0, 1], ease);

  return (
    <AbsoluteFill style={{ backgroundColor: background === "black" ? "#000" : "transparent", opacity: fade }}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <defs>
          <linearGradient id="strain" gradientUnits="userSpaceOnUse" x1={ox} y1={0} x2={ox + L} y2={0}>
            <stop offset="0" stopColor={INK} />
            <stop offset="0.3" stopColor={INK} />
            <stop offset="0.51" stopColor={hot} />
            <stop offset="0.64" stopColor={INK} />
            <stop offset="1" stopColor={INK} />
          </linearGradient>
          <filter id="glow" x="-10%" y="-40%" width="120%" height="180%">
            <feGaussianBlur stdDeviation={14 * u} />
          </filter>
        </defs>

        {/* ground */}
        <line
          x1={ox - 120 * u}
          x2={ox - 120 * u + (L + 240 * u) * draw}
          y1={groundY}
          y2={groundY}
          stroke={INK}
          strokeOpacity={0.35}
          strokeWidth={3 * u}
        />

        {/* undeformed reference */}
        <path
          d={ghost}
          fill="none"
          stroke={INK}
          strokeOpacity={0.3 * flexIn}
          strokeWidth={3 * u}
          strokeDasharray={`${14 * u} ${14 * u}`}
        />
        {/* roof that drops out */}
        <path
          d={roof}
          fill="none"
          stroke={INK}
          strokeOpacity={0.3 * flexIn * open}
          strokeWidth={3 * u}
          strokeDasharray={`${14 * u} ${14 * u}`}
        />

        {/* wheels stay planted; the body bends between them */}
        {WHEELS.map((w, i) => {
          const [cx, cy] = P(w.x, w.y, false);
          return (
            <g key={i} opacity={draw} fill="none" stroke={INK}>
              <circle cx={cx} cy={cy} r={WHEEL_R * L} strokeWidth={sw} />
              <circle cx={cx} cy={cy} r={WHEEL_R * L * 0.56} strokeWidth={3 * u} strokeOpacity={0.6} />
            </g>
          );
        })}

        {/* body: closed and open-top outlines crossfade; glow on the strained zone */}
        {[
          { d: closedBody, o: 1 - open },
          { d: openBody, o: open },
        ].map(({ d, o }, i) => (
          <g key={i} opacity={o}>
            <path d={d} fill="none" stroke="url(#strain)" strokeWidth={sw * 3} opacity={0.55 * strain} filter="url(#glow)" />
            <path
              d={d}
              fill="none"
              stroke="url(#strain)"
              strokeWidth={sw}
              strokeLinejoin="round"
              pathLength={1}
              strokeDasharray="1"
              strokeDashoffset={1 - draw}
            />
          </g>
        ))}

        {flexIn > 0 && (
          <>
            {arrow(WHEELS[0].x, up ? 1 : -1, "r")}
            {arrow(WHEELS[1].x, up ? 1 : -1, "f")}
            {arrow(0.42, up ? -1 : 1, "m")}
          </>
        )}
      </svg>

      <div
        style={{
          position: "absolute",
          left: 220 * u,
          top: 200 * u,
          color: INK,
          opacity: titleIn,
          transform: `translateY(${(1 - titleIn) * 24 * u}px)`,
        }}
      >
        <div style={{ fontFamily: "Inter Display, Inter, sans-serif", fontWeight: 700, fontSize: 132 * u, letterSpacing: "0.06em" }}>
          {title}
        </div>
        <div
          style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 50 * u,
            letterSpacing: "0.12em",
            marginTop: 22 * u,
            opacity: labelOpacity,
            color: open < 0.5 ? INK : hot,
          }}
        >
          {label}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          right: 220 * u,
          bottom: 190 * u,
          color: INK,
          opacity: 0.55 * flexIn,
          fontFamily: "JetBrains Mono, monospace",
          fontSize: 34 * u,
          letterSpacing: "0.12em",
        }}
      >
        {note}
      </div>
    </AbsoluteFill>
  );
};
