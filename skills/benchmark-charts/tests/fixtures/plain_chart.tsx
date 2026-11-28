// Deliberately plain: a static SVG bar chart with no interaction. check_premium.py must fail it.
import { Page, Section, Diagram, useGrokTheme } from "grok/canvas";

function PlainBars() {
  const t = useGrokTheme();
  return (
    <svg width="640" viewBox="0 0 640 200">
      <defs><linearGradient id="g"><stop offset="0" stopColor="#3366ff" /></linearGradient></defs>
      <rect x="10" y="20" width="300" height="30" fill="url(#g)" />
      <rect x="10" y="70" width="120" height="30" fill="#999999" />
      <text x="320" y="40" fill={t.text.primary}>ESTIMATE 300</text>
    </svg>
  );
}

export default function App() {
  return (
    <Page title="Plain">
      <Section heading="Bars"><PlainBars /></Section>
      <Section heading="Graph"><Diagram nodes={[{ id: "a", label: "A" }]} edges={[]} /></Section>
    </Page>
  );
}
