import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";

/**
 * Mobile-version CTA end card: the product listing as it looks on a phone (Playwright, iPhone 14 Pro UA, viewport 393 x
 * 699 CSS px @3x = exactly 9:16), entered by a 1:1 cut from the scan render to the listing's own photo.
 *
 * Frame 0 = the 1:1 frame: the gallery photo `photos[start]` fills the frame at `startScale` (photo px -> video px) with
 * its centre at (540, 960); the scan render's last frame was rendered from the camera solved against that photo with the
 * same mapping, so the car does not move across the cut. Then the page zooms out until the photo sits in its gallery slot,
 * the carousel swipes through `swipes` on the beat (photos drawn in the slot at the page's measured pitch), and the CTA
 * lands at the bottom. `pages` = screenshots of the page with each carousel dot active (gallery images hidden there are
 * irrelevant: the strip is drawn on top), swapped at the middle of each swipe so the dots follow.
 */
export type MobileCTAProps = {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  pageW: number; // screenshot px
  pages: { src: string; from: number }[];
  slot: { x: number; y: number; w: number; h: number; pitch: number }; // screenshot px
  photos: { src: string; w: number; h: number }[];
  start: number; // photo index shown at frame 0
  startScale: number; // photo px -> video px at frame 0
  hold: number; // frames held on the 1:1 frame
  zoomEnd: number; // frame the page is fully zoomed out
  swipes: { at: number; to: number; dur: number }[];
  ctaAt: number;
  urlAt: number;
  highlights?: { x: number; y: number; w: number; h: number }[]; // screenshot px: flash these when the page changes
  ctaBand?: number; // video px from the bottom the CTA may use (below the dropdown so option + price stay readable)
  drift?: number; // slow push-in after the zoom-out (1.0 -> 1 + drift by the last frame) so the page never sits dead
  title: string;
  sub: string;
  url: string;
};

export const mobileCtaDefaults: MobileCTAProps = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 184,
  pageW: 1179,
  pages: [{ src: "f296_mpage_d1.png", from: 0 }],
  slot: { x: 147.4, y: 177, w: 884.25, h: 585.6, pitch: 896.25 },
  photos: [{ src: "f296_p00.jpg", w: 3465, h: 2292 }],
  start: 0,
  startScale: 0.45,
  hold: 6,
  zoomEnd: 48,
  swipes: [],
  ctaAt: 110,
  urlAt: 124,
  title: "SCAN DATA",
  sub: "AVAILABLE NOW",
  url: "ILLUMAESTHETIC.COM",
};

export const calculateMobileCtaMetadata: CalculateMetadataFunction<MobileCTAProps> = ({ props }) => ({
  width: props.width,
  height: props.height,
  fps: props.fps,
  durationInFrames: props.durationInFrames,
});

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const MobileCTA: React.FC<MobileCTAProps> = (p) => {
  const f = useCurrentFrame();
  const page0 = p.width / p.pageW; // screenshot px -> video px when the page fills the frame
  // photo display scale in the slot at rest (object-fit: cover by width)
  const ph0 = p.photos[p.start];
  const slotScale = p.slot.w / ph0.w;
  // zoom factor Z: 1 = page fills the frame. At frame 0 the slot photo shows at startScale.
  const Z0 = p.startScale / (slotScale * page0);
  const u = interpolate(f, [p.hold, p.zoomEnd], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const Z = Math.exp(Math.log(Z0) * (1 - u)); // log-space zoom: constant perceived speed
  // anchor: the slot centre moves from the frame centre (540, 960) to where the page puts it
  const scx = (p.slot.x + p.slot.w / 2) * page0;
  const scy = (p.slot.y + p.slot.h / 2) * page0;
  const ax = p.width / 2 + (scx - p.width / 2) * u;
  const ay = p.height / 2 + (scy - p.height / 2) * u;
  const s = page0 * Z; // screenshot px -> video px now
  const ox = ax - (p.slot.x + p.slot.w / 2) * s;
  const oy = ay - (p.slot.y + p.slot.h / 2) * s;

  // carousel position (in slides)
  let pos = p.start;
  for (const sw of p.swipes) {
    const prev = pos;
    const k = interpolate(f, [sw.at, sw.at + sw.dur], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
    pos = prev + (sw.to - prev) * k;
  }
  // page screenshot whose dots match the slide we are nearest to
  let page = p.pages[0].src;
  for (const pg of p.pages) if (f >= pg.from) page = pg.src;

  // dropdown/price flash whenever the page (selected option) changes
  let flash = 0;
  for (const pg of p.pages.slice(1)) flash = Math.max(flash, interpolate(f, [pg.from, pg.from + 3, pg.from + 16], [0, 1, 0], clamp));
  const push = 1 + (p.drift ?? 0) * interpolate(f, [p.zoomEnd, p.durationInFrames - 1], [0, 1], clamp);
  const ctaIn = interpolate(f, [p.ctaAt, p.ctaAt + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const urlIn = interpolate(f, [p.urlAt, p.urlAt + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  const lo = Math.max(0, Math.floor(pos) - 1);
  const hi = Math.min(p.photos.length - 1, Math.ceil(pos) + 1);
  const strip = [];
  for (let i = lo; i <= hi; i++) {
    const ph = p.photos[i];
    const x = p.slot.x + (i - pos) * p.slot.pitch;
    strip.push(
      <Img
        key={i}
        src={staticFile(ph.src)}
        style={{ position: "absolute", left: x * s + ox, top: p.slot.y * s + oy, width: p.slot.w * s, height: p.slot.h * s, objectFit: "cover" }}
      />,
    );
  }
  return (
    <AbsoluteFill style={{ backgroundColor: "#0b0b0b", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: "50% 40%" }}>
      <Img src={staticFile(page)} style={{ position: "absolute", left: ox, top: oy, width: p.pageW * s }} />
      {/* gallery strip, clipped to the full-width band of the slot like the page's overflow */}
      <div style={{ position: "absolute", left: 0, top: p.slot.y * s + oy, width: p.width, height: p.slot.h * s, overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, top: -(p.slot.y * s + oy), width: p.width, height: p.height }}>{strip}</div>
      </div>
      {(p.highlights ?? []).map((r, i) => (
        <div key={`hl${i}`} style={{ position: "absolute", left: r.x * s + ox - 8, top: r.y * s + oy - 8, width: r.w * s + 16, height: r.h * s + 16,
          borderRadius: 10, border: "4px solid #6fcf8a", boxShadow: "0 0 26px rgba(111,207,138,0.75)", opacity: flash }} />
      ))}
      </AbsoluteFill>
      {/* CTA: compact band under the dropdown so the selected option and its price stay readable */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: p.ctaBand ?? 600,
          opacity: ctaIn,
          transform: `translateY(${(1 - ctaIn) * 40}px)`,
          background: "linear-gradient(to bottom, rgba(11,11,11,0) 0%, #0b0b0b 14%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-end",
          paddingBottom: 26,
          boxSizing: "border-box",
          color: "#e8ecf2",
          fontFamily: "'Inter Display', 'Inter', sans-serif",
        }}
      >
        <div style={{ fontWeight: 700, fontSize: 34, letterSpacing: 8, lineHeight: 1 }}>{p.title} {p.sub}</div>
        <div
          style={{
            marginTop: 16,
            padding: "16px 44px",
            borderRadius: 10,
            background: "#5c9e6e",
            color: "#0b0b0b",
            fontWeight: 800,
            fontSize: 46,
            letterSpacing: 6,
            opacity: urlIn,
            transform: `scale(${0.8 + 0.2 * urlIn})`,
          }}
        >
          {p.url}
        </div>
      </div>
    </AbsoluteFill>
  );
};
