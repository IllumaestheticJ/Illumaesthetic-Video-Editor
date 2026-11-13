import { Composition } from "remotion";
import { calculateScanHudMetadata, ScanHUD, scanHudDefaults } from "./ScanHUD";
import { calculateHudRailMetadata, HudRail, hudRailDefaults } from "./gfx/HudRail";
import { calculateGfxMetadata, GfxCard, gfxDefaults, ScanLabel } from "./gfx/Cards";
import { calculateCaptionsMetadata, Captions, captionsDefaults } from "./gfx/Captions";
import { calculateHudV2Metadata, HudV2, hudV2Defaults } from "./gfx/v2/HudV2";
import { calculateCueV2Metadata, CardV2, CueV2, cueV2Defaults, FxGlitch } from "./gfx/v2/CuesV2";
import { calculateWebZoomMetadata, WebZoom, webZoomDefaults } from "./WebZoom";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ScanHUD"
        component={ScanHUD}
        durationInFrames={scanHudDefaults.durationInFrames}
        fps={scanHudDefaults.fps}
        width={scanHudDefaults.width}
        height={scanHudDefaults.height}
        defaultProps={scanHudDefaults}
        calculateMetadata={calculateScanHudMetadata}
      />
      <Composition
        id="WebZoom"
        component={WebZoom}
        durationInFrames={webZoomDefaults.durationInFrames}
        fps={webZoomDefaults.fps}
        width={webZoomDefaults.width}
        height={webZoomDefaults.height}
        defaultProps={webZoomDefaults}
        calculateMetadata={calculateWebZoomMetadata}
      />
      <Composition id="HudRail" component={HudRail} durationInFrames={hudRailDefaults.durationInFrames} fps={hudRailDefaults.fps} width={1920} height={160} defaultProps={hudRailDefaults} calculateMetadata={calculateHudRailMetadata} />
      <Composition id="GfxCard" component={GfxCard} durationInFrames={gfxDefaults.frames} fps={23.976} width={1920} height={1080} defaultProps={gfxDefaults} calculateMetadata={calculateGfxMetadata} />
      <Composition id="ScanLabel" component={ScanLabel} durationInFrames={gfxDefaults.frames} fps={23.976} width={1920} height={1080} defaultProps={{ ...gfxDefaults, cue: "G10", text: "LEXUS IS350", sub: "FULL CAR SCAN" }} calculateMetadata={calculateGfxMetadata} />
      <Composition id="Captions" component={Captions} durationInFrames={captionsDefaults.durationInFrames} fps={23.976} width={1100} height={120} defaultProps={captionsDefaults} calculateMetadata={calculateCaptionsMetadata} />
      <Composition id="HudV2" component={HudV2} durationInFrames={hudV2Defaults.durationInFrames} fps={hudV2Defaults.fps} width={1920} height={270} defaultProps={hudV2Defaults} calculateMetadata={calculateHudV2Metadata} />
      <Composition id="CueV2" component={CueV2} durationInFrames={cueV2Defaults.frames} fps={23.976} width={1920} height={1080} defaultProps={cueV2Defaults} calculateMetadata={calculateCueV2Metadata} />
      <Composition id="CardV2" component={CardV2} durationInFrames={cueV2Defaults.frames} fps={23.976} width={1920} height={1080} defaultProps={cueV2Defaults} calculateMetadata={calculateCueV2Metadata} />
      <Composition id="FxGlitch" component={FxGlitch} durationInFrames={cueV2Defaults.frames} fps={23.976} width={1920} height={1080} defaultProps={cueV2Defaults} calculateMetadata={calculateCueV2Metadata} />
    </>
  );
};
