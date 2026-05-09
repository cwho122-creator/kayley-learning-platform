import React from 'react';

export default function QuizQuestion({ question, options, selected, answered, correctAnswer, onSelect }) {
  return (
    <div className="qq-wrap">
      <p className="qq-question">{question}</p>
      <div className="qq-options">
        {options.map((opt, i) => {
          let state = '';
          if (answered) {
            if (opt === correctAnswer) state = 'correct';
            else if (opt === selected && opt !== correctAnswer) state = 'wrong';
          } else if (selected === opt) {
            state = 'selected';
          }
          return (
            <button
              key={i}
              className={`qq-opt ${state}`}
              onClick={() => !answered && onSelect(opt)}
              disabled={answered}
            >
              <span className="qq-opt-letter">{String.fromCharCode(65 + i)}</span>
              <span className="qq-opt-text">{opt}</span>
            </button>
          );
        })}
      </div>
      {answered && (
        <p className={`qq-feedback ${selected === correctAnswer ? 'fb-good' : 'fb-bad'}`}>
          {selected === correctAnswer ? '🎉 Correct! Great job!' : `❌ Not quite — the answer was: ${correctAnswer}`}
        </p>
      )}
      <style>{`
        .qq-wrap { width: 100%; }
        .qq-question { font-size: 1.15rem; font-weight: 700; margin-bottom: 1.25rem; color: var(--text); }
        .qq-options { display: flex; flex-direction: column; gap: 0.75rem; }
        .qq-opt {
          display: flex; align-items: center; gap: 0.75rem;
          padding: 0.875rem 1rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          background: var(--card);
          text-align: left;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .qq-opt:hover:not(:disabled) { border-color: var(--primary); background: #EEF2FF; }
        .qq-opt.selected { border-color: var(--primary); background: #EEF2FF; }
        .qq-opt.correct { border-color: var(--success); background: #D1FAE5; }
        .qq-opt.wrong { border-color: var(--error); background: #FEE2E2; }
        .qq-opt:disabled { cursor: default; }
        .qq-opt-letter {
          width: 28px; height: 28px;
          border-radius: 50%;
          background: var(--bg);
          display: flex; align-items: center; justify-content: center;
          font-weight: 700; font-size: 0.8rem; flex-shrink: 0;
        }
        .qq-opt.correct .qq-opt-letter { background: var(--success); color: white; }
        .qq-opt.wrong .qq-opt-letter { background: var(--error); color: white; }
        .qq-opt.selected .qq-opt-letter { background: var(--primary); color: white; }
        .qq-feedback { margin-top: 1rem; padding: 0.75rem 1rem; border-radius: var(--radius); font-weight: 600; font-size: 0.95rem; }
        .fb-good { background: #D1FAE5; color: #065F46; }
        .fb-bad { background: #FEE2E2; color: #991B1B; }
      `}</style>
    </div>
  );
}