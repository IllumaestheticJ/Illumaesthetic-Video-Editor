import { Composition } from "remotion";
import { calculateScanHudMetadata, ScanHUD, scanHudDefaults } from "./ScanHUD";

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
    </>
  );
};
