import React, { useState } from 'react';

const STEPS = [
  {
    title: 'Read',
    icon: '📖',
    desc: 'Read the lesson carefully, twice if you need!',
    example: '"Multiplication is adding groups of numbers together."',
  },
  {
    title: 'Ask',
    icon: '❓',
    desc: 'Ask yourself: Do I understand this? What is it about?',
    example: '"So 4 × 3 means 4 groups of 3? That is 12!"',
  },
  {
    title: 'Put',
    icon: '✏️',
    desc: 'Put it into your own words. Try a practice problem!',
    example: '"I will solve 5 × 2 by counting by 5s: 5, 10 — that is 10!"',
  },
];

export default function RAPCard({ collapsed: externalCollapsed }) {
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const collapsed = externalCollapsed !== undefined ? externalCollapsed : internalCollapsed;
  const setCollapsed = externalCollapsed !== undefined ? undefined : setInternalCollapsed;

  return (
    <div className="rap-card">
      <button
        className="rap-header"
        onClick={() => setCollapsed && setCollapsed(!collapsed)}
        aria-expanded={!collapsed}
      >
        <span className="rap-title">🧠 RAP Strategy</span>
        <span className="rap-toggle">{collapsed ? '▶' : '▼'}</span>
      </button>
      {!collapsed && (
        <div className="rap-body">
          {STEPS.map((step, i) => (
            <div key={i} className="rap-step">
              <div className="rap-step-header">
                <span className="rap-step-icon">{step.icon}</span>
                <strong>{step.title}</strong>
              </div>
              <p className="rap-step-desc">{step.desc}</p>
              <p className="rap-step-example">✨ {step.example}</p>
            </div>
          ))}
        </div>
      )}
      <style>{`
        .rap-card {
          background: #FEF9C3;
          border: 2px solid #FDE047;
          border-radius: var(--radius-lg);
          overflow: hidden;
        }
        .rap-header {
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.875rem 1rem;
          background: none;
          border: none;
          cursor: pointer;
        }
        .rap-title { font-weight: 700; color: #854D0E; font-size: 0.95rem; }
        .rap-toggle { color: #854D0E; font-size: 0.75rem; }
        .rap-body { padding: 0.5rem 1rem 1rem; display: flex; flex-direction: column; gap: 0.75rem; }
        .rap-step { background: rgba(255,255,255,0.6); border-radius: var(--radius); padding: 0.75rem; }
        .rap-step-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; color: #854D0E; }
        .rap-step-icon { font-size: 1.1rem; }
        .rap-step-desc { font-size: 0.82rem; color: #713F12; margin-bottom: 0.3rem; }
        .rap-step-example { font-size: 0.78rem; color: #92400E; font-style: italic; }
      `}</style>
    </div>
  );
}