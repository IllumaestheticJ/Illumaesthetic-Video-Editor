import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, useCurrentFrame } from "remotion";
import { C, FPS, SANS } from "./theme";

/**
 * v2: burned-in captions as an overlay on full-frame footage. Transparent band 1200x160 (ProRes 4444 alpha),
 * place at x=360, y=880 on the 1920x1080 timeline (reserved caption band y880-1040). Plate matches HUD_v2
 * (50% black, 12 px radius), bottom-anchored, width follows the text. Hard in/out on exact frames (no fades) so a caption
 * never precedes its first word. Props: captions.json from the project (start/end in seconds, lines[]).
 */
export type Cap = { n: number; start: number; end: number; lines: string[] };
export type CaptionsProps = { fps: number; durationInFrames: number; captions: Cap[] };
export const captionsDefaults: CaptionsProps = { fps: FPS, durationInFrames: 48, captions: [] };
export const calculateCaptionsMetadata: CalculateMetadataFunction<CaptionsProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: 1200, height: 160,
});

export const Captions: React.FC<CaptionsProps> = ({ captions, fps }) => {
  const f = useCurrentFrame();
  const t = (f + 0.5) / fps; // sample mid-frame
  const cap = captions.find((c) => t >= c.start && t < c.end);
  return (
    <AbsoluteFill style={{ background: "transparent", justifyContent: "flex-end", alignItems: "center", paddingBottom: 20 }}>
      {cap ? (
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 46, lineHeight: "52px", color: C.ink, textAlign: "center", whiteSpace: "nowrap", background: "rgba(0,0,0,0.5)", borderRadius: 12, padding: "10px 28px", textShadow: "0 2px 5px rgba(0,0,0,0.9)" }}>
          {cap.lines.map((l, i) => (<div key={i}>{l}</div>))}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
