import { Composition } from "remotion";
import { calculateScanHudMetadata, ScanHUD, scanHudDefaults } from "./ScanHUD";
import { CHASSIS_FLEX_FPS, CHASSIS_FLEX_SECONDS, ChassisFlex, chassisFlexDefaults } from "./ChassisFlex";
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
      <Composition
        id="ChassisFlex"
        component={ChassisFlex}
        durationInFrames={Math.round(CHASSIS_FLEX_FPS * CHASSIS_FLEX_SECONDS)}
        fps={CHASSIS_FLEX_FPS}
        width={3840}
        height={2160}
        defaultProps={chassisFlexDefaults}
      />
    </>
  );
};
