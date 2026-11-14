import { Composition } from "remotion";
import { calculateScanHudMetadata, ScanHUD, scanHudDefaults } from "./ScanHUD";
import { calculateWebZoomMetadata, WebZoom, webZoomDefaults } from "./WebZoom";
import { calculateWebZoomSplitMetadata, WebZoomSplit, webZoomSplitDefaults } from "./WebZoomSplit";
import { calculatePromoCaptionMetadata, PromoCaption, promoCaptionDefaults } from "./PromoCaption";
import { calculateMobileCtaMetadata, MobileCTA, mobileCtaDefaults } from "./MobileCTA";

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
        id="WebZoomSplit"
        component={WebZoomSplit}
        durationInFrames={webZoomSplitDefaults.durationInFrames}
        fps={webZoomSplitDefaults.fps}
        width={webZoomSplitDefaults.width}
        height={webZoomSplitDefaults.height}
        defaultProps={webZoomSplitDefaults}
        calculateMetadata={calculateWebZoomSplitMetadata}
      />
      <Composition
        id="MobileCTA"
        component={MobileCTA}
        durationInFrames={mobileCtaDefaults.durationInFrames}
        fps={mobileCtaDefaults.fps}
        width={mobileCtaDefaults.width}
        height={mobileCtaDefaults.height}
        defaultProps={mobileCtaDefaults}
        calculateMetadata={calculateMobileCtaMetadata}
      />
      <Composition
        id="PromoCaption"
        component={PromoCaption}
        durationInFrames={promoCaptionDefaults.durationInFrames}
        fps={promoCaptionDefaults.fps}
        width={promoCaptionDefaults.width}
        height={promoCaptionDefaults.height}
        defaultProps={promoCaptionDefaults}
        calculateMetadata={calculatePromoCaptionMetadata}
      />
    </>
  );
};
