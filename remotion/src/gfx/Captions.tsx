import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, useCurrentFrame } from "remotion";
import { C, FPS, SANS } from "./theme";

/**
 * Burned-in captions for the HUD rail centre zone. Transparent strip 1100x120 (ProRes 4444 alpha),
 * place at x=410, y=940 on the 1920x1080 timeline. Hard in/out on exact frames (no fades) so a caption
 * never precedes its first word. Props: captions.json from the project (start/end in seconds, lines[]).
 */
export type Cap = { n: number; start: number; end: number; lines: string[] };
export type CaptionsProps = { fps: number; durationInFrames: number; captions: Cap[] };
export const captionsDefaults: CaptionsProps = { fps: FPS, durationInFrames: 48, captions: [] };
export const calculateCaptionsMetadata: CalculateMetadataFunction<CaptionsProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames, fps: props.fps, width: 1100, height: 120,
});

export const Captions: React.FC<CaptionsProps> = ({ captions, fps }) => {
  const f = useCurrentFrame();
  const t = (f + 0.5) / fps; // sample mid-frame
  const cap = captions.find((c) => t >= c.start && t < c.end);
  return (
    <AbsoluteFill style={{ background: "transparent", justifyContent: "center", alignItems: "center" }}>
      {cap ? (
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 48, lineHeight: "54px", color: C.ink, textAlign: "center", whiteSpace: "nowrap", textShadow: "0 2px 6px rgba(0,0,0,0.85)" }}>
          {cap.lines.map((l, i) => (<div key={i}>{l}</div>))}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
