import { Composition } from 'remotion';
import { Up2YouAd } from './Up2YouAd';

export const RemotionRoot = () => {
  return (
    <Composition
      id="Up2YouAd"
      component={Up2YouAd}
      durationInFrames={900}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
