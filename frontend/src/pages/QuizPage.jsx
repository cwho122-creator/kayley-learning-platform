import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getQuizByLesson, submitQuiz } from '../api';
import QuizQuestion from '../components/QuizQuestion';
import LoadingSpinner from '../components/LoadingSpinner';

export default function QuizPage() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (lessonId) {
      loadQuiz(lessonId);
    }
  }, [lessonId]);

  const loadQuiz = async (lid) => {
    try {
      const res = await getQuizByLesson(lid);
      const data = res.data;
      if (data?.questions) {
        // Limit to 5
        data.questions = data.questions.slice(0, 5);
      }
      setQuiz(data);
    } catch {
      setQuiz({ questions: [] });
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (opt) => {
    setSelected(opt);
  };

  const handleConfirm = () => {
    if (selected === null) return;
    setAnswered(true);
    setAnswers((prev) => ({ ...prev, [current]: selected }));
  };

  const handleNext = () => {
    if (current < quiz.questions.length - 1) {
      setCurrent((c) => c + 1);
      setSelected(null);
      setAnswered(false);
    } else {
      handleFinish();
    }
  };

  const handleFinish = async () => {
    setSubmitting(true);
    try {
      const payload = { answers };
      const res = await submitQuiz(quiz.id, payload);
      setResults(res.data);
    } catch {
      // Compute local score
      const correct = quiz.questions.reduce((sum, q, i) => sum + (answers[i] === q.correct_answer ? 1 : 0), 0);
      setResults({ score: correct, total: quiz.questions.length, points_earned: correct * 5 });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading quiz..." />;

  const questions = quiz?.questions || [];
  const total = questions.length;

  if (results) {
    const pct = total > 0 ? Math.round((results.score / total) * 100) : 0;
    return (
      <div className="q-finish">
        <div className="q-finish-card">
          <div className="q-finish-emoji">{pct >= 80 ? '🎉' : pct >= 50 ? '👍' : '💪'}</div>
          <h2>Quiz Complete!</h2>
          <p className="q-finish-score">{results.score} / {total} correct</p>
          <p className="q-finish-pct">{pct}%</p>
          <p className="q-finish-pts">⭐ You earned <strong>{results.points_earned || 0} points</strong>!</p>
          <div className="q-finish-bar">
            <div className="q-finish-fill" style={{ width: `${pct}%`, background: pct >= 80 ? 'var(--success)' : pct >= 50 ? 'var(--warning)' : 'var(--error)' }} />
          </div>
          <button className="q-finish-btn" onClick={() => navigate('/dashboard')}>
            Back to Dashboard 🚀
          </button>
        </div>
        <style>{`
          .q-finish { display: flex; justify-content: center; padding: 2rem 0; }
          .q-finish-card {
            background: var(--card);
            border-radius: var(--radius-lg);
            padding: 2.5rem;
            text-align: center;
            max-width: 420px;
            width: 100%;
            box-shadow: var(--shadow-lg);
          }
          .q-finish-emoji { font-size: 3.5rem; margin-bottom: 0.5rem; }
          .q-finish-card h2 { font-size: 1.5rem; font-weight: 800; margin-bottom: 0.5rem; }
          .q-finish-score { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem; }
          .q-finish-pct { font-size: 2.5rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem; }
          .q-finish-pts { color: var(--text-light); margin-bottom: 1rem; }
          .q-finish-bar { height: 12px; background: var(--bg); border-radius: 6px; overflow: hidden; margin-bottom: 1.5rem; }
          .q-finish-fill { height: 100%; border-radius: 6px; transition: width 0.6s ease; }
          .q-finish-btn {
            padding: 0.875rem 2rem;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: var(--radius);
            font-weight: 800;
            font-size: 1rem;
            cursor: pointer;
          }
          .q-finish-btn:hover { background: var(--primary-dark); }
        `}</style>
      </div>
    );
  }

  if (total === 0) {
    return (
      <div className="q-empty">
        <p>No quiz found for this lesson. Check back later! 🎉</p>
        <button onClick={() => navigate('/lessons')}>Back to Lessons</button>
        <style>{`.q-empty { text-align: center; padding: 3rem; } .q-empty button { margin-top: 1rem; padding: 0.75rem 1.5rem; background: var(--primary); color: white; border: none; border-radius: var(--radius); font-weight: 700; cursor: pointer; }`}</style>
      </div>
    );
  }

  const q = questions[current];

  return (
    <div className="qpage">
      <div className="q-header">
        <h1>📝 Quiz Time!</h1>
        <div className="q-progress">
          <span>Question {current + 1} of {total}</span>
          <div className="q-progress-track">
            <div className="q-progress-fill" style={{ width: `${((current + 1) / total) * 100}%` }} />
          </div>
        </div>
      </div>

      <div className="q-card">
        <QuizQuestion
          question={q.question}
          options={q.options || []}
          selected={selected}
          answered={answered}
          correctAnswer={q.correct_answer}
          onSelect={handleSelect}
        />

        <div className="q-actions">
          {!answered ? (
            <button className="q-confirm-btn" onClick={handleConfirm} disabled={selected === null}>
              Confirm Answer ✅
            </button>
          ) : (
            <button className="q-next-btn" onClick={handleNext} disabled={submitting}>
              {current < total - 1 ? 'Next Question ➡️' : 'Finish Quiz 🎉'}
            </button>
          )}
        </div>
      </div>

      <style>{`
        .qpage { max-width: 700px; margin: 0 auto; }
        .q-header { margin-bottom: 1.5rem; }
        .q-header h1 { font-size: 1.5rem; font-weight: 800; margin-bottom: 0.75rem; }
        .q-progress { display: flex; align-items: center; gap: 0.75rem; }
        .q-progress span { font-weight: 600; font-size: 0.9rem; color: var(--text-light); white-space: nowrap; }
        .q-progress-track { flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
        .q-progress-fill { height: 100%; background: var(--primary); border-radius: 4px; transition: width 0.3s ease; }
        .q-card {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 2rem;
          box-shadow: var(--shadow-lg);
        }
        .q-actions { margin-top: 1.5rem; display: flex; justify-content: center; }
        .q-confirm-btn, .q-next-btn {
          padding: 0.875rem 2rem;
          border: none;
          border-radius: var(--radius);
          font-size: 1rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.2s;
        }
        .q-confirm-btn { background: var(--primary); color: white; }
        .q-confirm-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .q-next-btn { background: var(--secondary); color: white; }
        .q-confirm-btn:hover:not(:disabled), .q-next-btn:hover { transform: translateY(-1px); }
      `}</style>
    </div>
  );
}