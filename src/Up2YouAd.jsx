import React from 'react';
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  AbsoluteFill,
} from 'remotion';

// ─── Design tokens ───────────────────────────────────────────────────────────
const GREEN      = '#00C47A';
const GREEN_DARK = '#008A55';
const WHITE      = '#FFFFFF';
const DARK       = '#060E1A';
const GRAY       = '#8B9BB4';
const FONT_BLACK = '"Arial Black", Arial, sans-serif';
const FONT       = 'Arial, sans-serif';

// ─── Utility ─────────────────────────────────────────────────────────────────
const makeEntrance = (s, distance = 50) => ({
  opacity:   interpolate(s, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' }),
  transform: `translateY(${interpolate(s, [0, 1], [distance, 0])}px)`,
});

const makeFadeOut = (frame, start, end) =>
  interpolate(frame, [start, end], [1, 0], {
    extrapolateLeft:  'clamp',
    extrapolateRight: 'clamp',
  });

const makeFadeIn = (frame, start, end) =>
  interpolate(frame, [start, end], [0, 1], {
    extrapolateLeft:  'clamp',
    extrapolateRight: 'clamp',
  });

// ─── Shared: animated gradient background ────────────────────────────────────
const Background = () => {
  const frame = useCurrentFrame();
  const x = 50 + Math.sin(frame * 0.012) * 20;
  const y = 45 + Math.cos(frame * 0.009) * 15;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at ${x}% ${y}%, #0D2A1A 0%, #060E1A 65%, #04090F 100%)`,
      }}
    />
  );
};

// Subtle dot-grid overlay
const DotGrid = () => {
  const frame = useCurrentFrame();
  const dots = [];
  const cols = 22, rows = 13;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const delay = (r * cols + c) * 1.2;
      const op = interpolate(frame, [delay, delay + 25], [0, 0.12], {
        extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
      });
      dots.push(
        <div key={`${r}-${c}`} style={{
          position:        'absolute',
          left:            `${(c / (cols - 1)) * 100}%`,
          top:             `${(r / (rows - 1)) * 100}%`,
          width:           3, height: 3,
          borderRadius:    '50%',
          backgroundColor: GREEN,
          opacity:         op,
          transform:       'translate(-50%, -50%)',
        }} />
      );
    }
  }
  return <AbsoluteFill style={{ overflow: 'hidden' }}>{dots}</AbsoluteFill>;
};

// Green accent bar
const AccentBar = ({ frame, startFrame, width = 120 }) => {
  const w = interpolate(frame, [startFrame, startFrame + 35], [0, width], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  return (
    <div style={{
      width:           w,
      height:          4,
      background:      `linear-gradient(90deg, ${GREEN}, ${GREEN_DARK})`,
      borderRadius:    2,
      marginTop:       24,
      boxShadow:       `0 0 16px ${GREEN}66`,
    }} />
  );
};

// ─── Scene 1: HOOK  (frames 0 → 150) ─────────────────────────────────────────
const SceneHook = () => {
  const frame        = useCurrentFrame();
  const { fps }      = useVideoConfig();
  const s1 = spring({ frame,          fps, config: { damping: 200 } });
  const s2 = spring({ frame: frame - 22, fps, config: { damping: 200 } });
  const fadeOut = makeFadeOut(frame, 115, 150);

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '0 180px', opacity: fadeOut,
    }}>
      <div style={{ ...makeEntrance(s1), fontFamily: FONT_BLACK, fontSize: 76, fontWeight: 900,
        color: WHITE, textAlign: 'center', lineHeight: 1.15, marginBottom: 18 }}>
        La sostenibilità è un obbligo.
      </div>
      <div style={{ ...makeEntrance(s2), fontFamily: FONT_BLACK, fontSize: 76, fontWeight: 900,
        color: GREEN, textAlign: 'center', lineHeight: 1.15 }}>
        Falla diventare un vantaggio.
      </div>
      <AccentBar frame={frame} startFrame={45} width={130} />
    </AbsoluteFill>
  );
};

// ─── Scene 2: PROBLEM  (frames 120 → 270 → local 0-150) ──────────────────────
const SceneProblem = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s0 = spring({ frame,          fps, config: { damping: 200 } });
  const s1 = spring({ frame: frame - 15, fps, config: { damping: 200 } });
  const s2 = spring({ frame: frame - 30, fps, config: { damping: 200 } });
  const s3 = spring({ frame: frame - 45, fps, config: { damping: 200 } });
  const alpha = Math.min(makeFadeIn(frame, 0, 18), makeFadeOut(frame, 110, 150));

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '0 180px', opacity: alpha,
    }}>
      <div style={{ ...makeEntrance(s0, 30), fontFamily: FONT, fontSize: 26,
        color: GRAY, letterSpacing: 5, marginBottom: 48,
        textTransform: 'uppercase', fontWeight: 400 }}>
        Redigere il Bilancio ESG?
      </div>
      <div style={{ display: 'flex', gap: 52, alignItems: 'baseline' }}>
        {[
          { text: 'Complesso.', s: s1, color: WHITE },
          { text: 'Lungo.',     s: s2, color: GRAY },
          { text: 'Dispersivo.', s: s3, color: '#4A5E72' },
        ].map(({ text, s, color }) => (
          <div key={text} style={{ ...makeEntrance(s), fontFamily: FONT_BLACK, fontSize: 58,
            fontWeight: 900, color }}>
            {text}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ─── Scene 3: SOLUTION  (frames 240 → 450 → local 0-210) ─────────────────────
const SceneSolution = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s0 = spring({ frame,          fps, config: { damping: 200 } });
  const s1 = spring({ frame: frame - 18, fps, config: { damping: 200 } });
  const s2 = spring({ frame: frame - 36, fps, config: { damping: 200 } });
  const s3 = spring({ frame: frame - 54, fps, config: { damping: 200 } });
  const alpha = Math.min(makeFadeIn(frame, 0, 18), makeFadeOut(frame, 160, 210));
  const standards = ['VSME', 'GRI', 'ESRS', 'CSRD'];

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '0 140px', opacity: alpha, gap: 22,
    }}>
      {/* Badge */}
      <div style={{ ...makeEntrance(s0, 20), background: `linear-gradient(135deg, ${GREEN}22, ${GREEN}11)`,
        border: `1.5px solid ${GREEN}55`, borderRadius: 50, padding: '10px 30px',
        fontFamily: FONT, fontSize: 17, color: GREEN, letterSpacing: 4,
        fontWeight: 700, textTransform: 'uppercase' }}>
        UP2YOU
      </div>

      {/* Title */}
      <div style={{ ...makeEntrance(s1), fontFamily: FONT_BLACK, fontSize: 70, fontWeight: 900,
        color: WHITE, textAlign: 'center', lineHeight: 1.1 }}>
        Bilancio di Sostenibilità
      </div>

      {/* Subtitle */}
      <div style={{ ...makeEntrance(s2), fontFamily: FONT, fontSize: 26,
        color: GREEN, textAlign: 'center', fontWeight: 500 }}>
        Con intelligenza artificiale integrata
      </div>

      {/* Standard chips */}
      <div style={{ ...makeEntrance(s3, 20), display: 'flex', gap: 16, marginTop: 8 }}>
        {standards.map(std => (
          <div key={std} style={{
            background:   'rgba(255,255,255,0.05)',
            border:       '1px solid rgba(255,255,255,0.18)',
            borderRadius: 8, padding: '9px 22px',
            fontFamily: FONT, fontSize: 16, color: WHITE, fontWeight: 700, letterSpacing: 2,
          }}>
            {std}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ─── Scene 4: BENEFITS  (frames 420 → 690 → local 0-270) ─────────────────────
const BenefitCard = ({ icon, title, desc, frame, startFrame }) => {
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - startFrame, fps, config: { damping: 200 } });
  return (
    <div style={{
      opacity:      interpolate(s, [0, 0.5], [0, 1], { extrapolateRight: 'clamp' }),
      transform:    `translateX(${interpolate(s, [0, 1], [70, 0])}px)`,
      background:   `rgba(0, 196, 122, 0.07)`,
      border:       `1px solid rgba(0, 196, 122, 0.28)`,
      borderRadius: 18, padding: '32px 30px',
      display: 'flex', alignItems: 'flex-start', gap: 22, flex: 1,
    }}>
      <div style={{ fontSize: 44, lineHeight: 1 }}>{icon}</div>
      <div>
        <div style={{ fontFamily: FONT_BLACK, fontSize: 22, fontWeight: 900, color: WHITE, marginBottom: 10 }}>
          {title}
        </div>
        <div style={{ fontFamily: FONT, fontSize: 17, color: GRAY, lineHeight: 1.6 }}>
          {desc}
        </div>
      </div>
    </div>
  );
};

const SceneBenefits = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleS  = spring({ frame, fps, config: { damping: 200 } });
  const alpha   = Math.min(makeFadeIn(frame, 0, 18), makeFadeOut(frame, 220, 270));

  const benefits = [
    { icon: '🤖', title: 'AI Integrata',     desc: '-40% tempo nella raccolta dati con la piattaforma Choral', startFrame: 20 },
    { icon: '✅', title: 'Standard Europei', desc: 'Allineato con VSME, GRI, ESRS e direttiva CSRD',           startFrame: 45 },
    { icon: '👥', title: 'Team Dedicato',    desc: 'Specialisti ESG al tuo fianco in ogni fase del progetto',  startFrame: 70 },
  ];

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '50px 110px', opacity: alpha, gap: 36,
    }}>
      <div style={{
        ...makeEntrance(titleS, 25),
        fontFamily: FONT, fontSize: 22, color: GREEN,
        letterSpacing: 4, textTransform: 'uppercase', fontWeight: 700,
      }}>
        I Vantaggi della Nostra Soluzione
      </div>
      <div style={{ display: 'flex', gap: 28, width: '100%' }}>
        {benefits.map(b => <BenefitCard key={b.title} {...b} frame={frame} />)}
      </div>
    </AbsoluteFill>
  );
};

// ─── Scene 5: SOCIAL PROOF  (frames 660 → 810 → local 0-150) ─────────────────
const AnimatedCounter = ({ frame, fps, target, startFrame, suffix = '' }) => {
  const s   = spring({ frame: frame - startFrame, fps, config: { damping: 200 } });
  const val = Math.round(interpolate(s, [0, 1], [0, target]));
  return <span>{val}{suffix}</span>;
};

const SceneSocialProof = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const alpha   = Math.min(makeFadeIn(frame, 0, 18), makeFadeOut(frame, 110, 150));
  const s0 = spring({ frame,          fps, config: { damping: 200 } });
  const s1 = spring({ frame: frame - 20, fps, config: { damping: 200 } });
  const s2 = spring({ frame: frame - 40, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '0 140px', opacity: alpha, gap: 50,
    }}>
      <div style={{ ...makeEntrance(s0, 25), fontFamily: FONT, fontSize: 26,
        color: GRAY, textAlign: 'center', lineHeight: 1.7, maxWidth: 720,
        fontStyle: 'italic' }}>
        "Up2YOU ci ha permesso di rafforzare il nostro percorso verso la sostenibilità
        per il secondo anno consecutivo."
      </div>
      <div style={{ display: 'flex', gap: 120 }}>
        <div style={{ ...makeEntrance(s1), textAlign: 'center' }}>
          <div style={{ fontFamily: FONT_BLACK, fontSize: 88, fontWeight: 900,
            color: GREEN, lineHeight: 1, textShadow: `0 0 40px ${GREEN}55` }}>
            <AnimatedCounter frame={frame} fps={fps} target={450} startFrame={20} suffix="+" />
          </div>
          <div style={{ fontFamily: FONT, fontSize: 22, color: WHITE, marginTop: 10 }}>
            Aziende clienti
          </div>
        </div>
        <div style={{ ...makeEntrance(s2), textAlign: 'center' }}>
          <div style={{ fontFamily: FONT_BLACK, fontSize: 88, fontWeight: 900,
            color: GREEN, lineHeight: 1, textShadow: `0 0 40px ${GREEN}55` }}>
            <AnimatedCounter frame={frame} fps={fps} target={180} startFrame={40} suffix="+" />
          </div>
          <div style={{ fontFamily: FONT, fontSize: 22, color: WHITE, marginTop: 10 }}>
            Bilanci realizzati
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ─── Scene 6: CTA  (frames 780 → 900 → local 0-120) ──────────────────────────
const SceneCTA = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const alpha   = makeFadeIn(frame, 0, 20);
  const s0 = spring({ frame,          fps, config: { damping: 200 } });
  const s1 = spring({ frame: frame - 18, fps, config: { damping: 200 } });
  const s2 = spring({ frame: frame - 36, fps, config: { damping: 15, stiffness: 200 } });

  // Button pulse
  const pulse = 1 + interpolate(Math.sin(frame * 0.12), [-1, 1], [0, 0.025]);

  return (
    <AbsoluteFill style={{
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
      alignItems: 'center', padding: '0 180px', opacity: alpha, gap: 30,
    }}>
      <div style={{ ...makeEntrance(s0), fontFamily: FONT_BLACK, fontSize: 62, fontWeight: 900,
        color: WHITE, textAlign: 'center', lineHeight: 1.2 }}>
        Semplifica il tuo<br />Bilancio di Sostenibilità ESG
      </div>
      <div style={{ ...makeEntrance(s1), fontFamily: FONT, fontSize: 24, color: GRAY, textAlign: 'center' }}>
        Team dedicato · AI integrata · Standard europei
      </div>
      <div style={{
        ...makeEntrance(s2),
        transform: `${makeEntrance(s2).transform} scale(${pulse})`,
        background:   `linear-gradient(135deg, ${GREEN} 0%, ${GREEN_DARK} 100%)`,
        borderRadius: 60, padding: '22px 64px',
        fontFamily: FONT_BLACK, fontSize: 30, fontWeight: 900, color: '#000',
        letterSpacing: 1, boxShadow: `0 8px 44px ${GREEN}55`,
        marginTop: 10,
      }}>
        u2y.io
      </div>
    </AbsoluteFill>
  );
};

// ─── Root composition ─────────────────────────────────────────────────────────
export const Up2YouAd = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: DARK }}>
      <Background />
      <DotGrid />

      {/* Scene 1 – Hook */}
      <Sequence from={0} durationInFrames={150} premountFor={0}>
        <SceneHook />
      </Sequence>

      {/* Scene 2 – Problem */}
      <Sequence from={120} durationInFrames={150} premountFor={10}>
        <SceneProblem />
      </Sequence>

      {/* Scene 3 – Solution */}
      <Sequence from={240} durationInFrames={210} premountFor={10}>
        <SceneSolution />
      </Sequence>

      {/* Scene 4 – Benefits */}
      <Sequence from={420} durationInFrames={270} premountFor={10}>
        <SceneBenefits />
      </Sequence>

      {/* Scene 5 – Social Proof */}
      <Sequence from={660} durationInFrames={150} premountFor={10}>
        <SceneSocialProof />
      </Sequence>

      {/* Scene 6 – CTA */}
      <Sequence from={780} durationInFrames={120} premountFor={10}>
        <SceneCTA />
      </Sequence>
    </AbsoluteFill>
  );
};
