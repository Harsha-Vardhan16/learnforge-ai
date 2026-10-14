import React, { useState, useEffect } from 'react';
import { 
  Target, 
  CheckCircle2, 
  XCircle, 
  Sparkles, 
  Lightbulb, 
  ArrowRight, 
  RotateCcw, 
  AlertTriangle,
  Award
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { api } from '../services/api';

const TOPICS = [
  "Recursion",
  "Binary Search",
  "Sorting",
  "Trees",
  "Arrays"
];

export default function PracticePage({ initialTopic = "Recursion", onMasteryUpdated }) {
  const [selectedTopic, setSelectedTopic] = useState(initialTopic);
  const [question, setQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [adaptiveBreakdown, setAdaptiveBreakdown] = useState(null);
  const [microAnswer, setMicroAnswer] = useState(null);
  const [microEvaluated, setMicroEvaluated] = useState(false);
  const [improvedMastery, setImprovedMastery] = useState(null);

  const fetchQuestion = async (topicToUse = selectedTopic) => {
    try {
      setLoading(true);
      setEvaluation(null);
      setSelectedOption(null);
      setAdaptiveBreakdown(null);
      setMicroAnswer(null);
      setMicroEvaluated(false);
      setImprovedMastery(null);

      const q = await api.generateAssessment({
        topic: topicToUse,
        studentId: 'demo-student-01'
      });
      setQuestion(q);
    } catch (err) {
      console.error("Failed to fetch assessment question:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestion(selectedTopic);
  }, [selectedTopic]);

  const handleSubmit = async () => {
    if (!selectedOption || submitting) return;

    try {
      setSubmitting(true);
      const res = await api.submitAssessment({
        questionId: question.question_id,
        selectedAnswer: selectedOption,
        studentId: 'demo-student-01'
      });
      setEvaluation(res);
      if (res.is_correct) {
        confetti({ particleCount: 70, spread: 60 });
        if (onMasteryUpdated) onMasteryUpdated();
      }
    } catch (err) {
      alert("Submission error: " + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleTriggerTeachDifferently = async () => {
    try {
      setLoading(true);
      const breakdown = await api.getAdaptiveTeachingBreakdown({
        topic: selectedTopic,
        attemptCount: 1,
        studentId: 'demo-student-01'
      });
      setAdaptiveBreakdown(breakdown);
    } catch (err) {
      alert("Failed to load adaptive breakdown: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleMicroSubmit = () => {
    if (!microAnswer) return;
    setMicroEvaluated(true);
    if (microAnswer === adaptiveBreakdown.mini_question.correct_option) {
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      setImprovedMastery({
        before: 42,
        after: 67,
        delta: 25
      });
      if (onMasteryUpdated) onMasteryUpdated();
    }
  };

  return (
    <div className="w-full space-y-6 animate-in fade-in duration-150">
      {/* Topic Selection Tabs */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Target className="w-5 h-5 text-purple-600" />
            Practice Questions
          </h2>
          <p className="text-sm text-slate-500">One question at a time. Difficulty adapts to your answers.</p>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {TOPICS.map((top) => (
            <button
              key={top}
              onClick={() => setSelectedTopic(top)}
              className={`text-sm px-3.5 py-1.5 rounded-lg font-semibold transition-all cursor-pointer whitespace-nowrap ${
                selectedTopic === top
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'
              }`}
            >
              {top} {top === "Recursion" && <span className="opacity-80 text-xs ml-1">(42%)</span>}
            </button>
          ))}
        </div>
      </div>

      {/* Main Single Question Card */}
      {loading ? (
        <div className="lf-card p-12 text-center text-slate-500">
          <div className="w-8 h-8 rounded-full border-3 border-purple-600 border-t-transparent animate-spin mx-auto mb-3" />
          <p className="text-base font-medium">Loading question...</p>
        </div>
      ) : question ? (
        <div className="lf-card p-8 space-y-6">
          {/* Question Header Meta */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold uppercase tracking-wider text-purple-700 bg-purple-50 px-2.5 py-1 rounded-md border border-purple-200">
                {question.topic}
              </span>
              <span className="text-xs font-semibold text-slate-500">
                Level: <strong className="text-slate-800">{question.difficulty}</strong>
              </span>
            </div>

            <button
              onClick={() => fetchQuestion()}
              className="text-xs font-semibold text-slate-500 hover:text-slate-900 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Try Another Question</span>
            </button>
          </div>

          {/* Prompt */}
          <div className="text-xl font-bold text-slate-900 leading-relaxed">
            {question.prompt}
          </div>

          {/* Clear Answer Choices */}
          <div className="space-y-3">
            {(question.options || []).map((opt, idx) => {
              const isSelected = selectedOption === opt;
              let choiceStyle = "bg-white border-slate-200 text-slate-800 hover:border-purple-300 hover:bg-purple-50/20";

              if (evaluation) {
                if (opt === evaluation.expected_answer) {
                  choiceStyle = "bg-emerald-50 border-emerald-500 text-emerald-900 font-bold shadow-xs";
                } else if (isSelected && !evaluation.is_correct) {
                  choiceStyle = "bg-rose-50 border-rose-400 text-rose-900 font-semibold";
                } else {
                  choiceStyle = "bg-slate-50 border-slate-200 text-slate-400 opacity-60";
                }
              } else if (isSelected) {
                choiceStyle = "bg-purple-50/70 border-purple-600 text-purple-950 font-semibold shadow-xs ring-2 ring-purple-600/20";
              }

              return (
                <button
                  key={idx}
                  onClick={() => !evaluation && setSelectedOption(opt)}
                  disabled={!!evaluation}
                  className={`w-full text-left p-4 sm:p-5 rounded-xl border text-base transition-all flex items-center justify-between cursor-pointer ${choiceStyle}`}
                >
                  <div className="flex items-center gap-3.5">
                    <span className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold font-mono shrink-0 ${
                      isSelected ? 'bg-purple-600 text-white' : 'bg-slate-100 text-slate-600'
                    }`}>
                      {String.fromCharCode(65 + idx)}
                    </span>
                    <span className="leading-snug">{opt}</span>
                  </div>

                  {evaluation && opt === evaluation.expected_answer && (
                    <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0 ml-2" />
                  )}
                  {evaluation && isSelected && !evaluation.is_correct && (
                    <XCircle className="w-6 h-6 text-rose-600 shrink-0 ml-2" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Submit Action */}
          {!evaluation && (
            <div className="flex justify-end pt-2">
              <button
                onClick={handleSubmit}
                disabled={!selectedOption || submitting}
                className="btn-primary text-base px-8 py-3.5 font-bold disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                <span>{submitting ? "Checking..." : "Submit Answer"}</span>
                <ArrowRight className="w-5 h-5 ml-1" />
              </button>
            </div>
          )}

          {/* Feedback Section */}
          {evaluation && (
            <div className={`p-6 rounded-2xl border space-y-4 animate-in fade-in duration-200 ${
              evaluation.is_correct
                ? 'bg-emerald-50/60 border-emerald-200 text-emerald-900'
                : 'bg-rose-50/60 border-rose-200 text-rose-900'
            }`}>
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-2.5">
                  {evaluation.is_correct ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                  ) : (
                    <AlertTriangle className="w-6 h-6 text-rose-600" />
                  )}
                  <h4 className="text-lg font-bold">
                    {evaluation.is_correct ? "Correct! Well done." : "Not quite right"}
                  </h4>
                </div>

                <div className="text-xs font-bold px-3 py-1 rounded-full bg-white border border-slate-200 text-slate-700">
                  Mastery: {Math.round(evaluation.previous_mastery * 100)}% &rarr; {Math.round(evaluation.new_mastery * 100)}%
                </div>
              </div>

              {/* Diagnosed Misconception if wrong */}
              {!evaluation.is_correct && evaluation.misconception_detected && (
                <div className="bg-white p-3.5 rounded-xl border border-rose-200 text-sm text-rose-900">
                  <strong>What happened:</strong> {evaluation.misconception_detected}
                </div>
              )}

              {/* Detailed Explanation */}
              <p className="text-sm text-slate-700 leading-relaxed">
                {evaluation.explanation}
              </p>

              {/* "Teach Me Differently" Button if incorrect */}
              {!evaluation.is_correct && !adaptiveBreakdown && (
                <div className="pt-3 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-rose-200/80">
                  <span className="text-sm text-slate-600">
                    Struggling with this concept? Let's try a different explanation style.
                  </span>
                  <button
                    onClick={handleTriggerTeachDifferently}
                    className="btn-amber text-sm px-5 py-2.5 font-bold shrink-0 w-full sm:w-auto justify-center cursor-pointer"
                  >
                    <Lightbulb className="w-4 h-4" />
                    <span>Teach Me Differently</span>
                  </button>
                </div>
              )}

              {/* Next Question Button if correct */}
              {evaluation.is_correct && (
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => fetchQuestion()}
                    className="btn-primary text-sm px-6 py-2.5 font-bold cursor-pointer"
                  >
                    <span>Next Question</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      ) : null}

      {/* "Teach Differently" Remediation Card */}
      {adaptiveBreakdown && (
        <div className="lf-card border-2 border-purple-300 bg-white p-8 space-y-6 animate-in slide-in-from-bottom duration-200 shadow-md">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-amber-100 text-amber-800 rounded-xl">
                <Lightbulb className="w-6 h-6 text-amber-600" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
                  {adaptiveBreakdown.strategy_label}
                </span>
                <h3 className="text-2xl font-extrabold text-slate-900">
                  {adaptiveBreakdown.title}
                </h3>
              </div>
            </div>

            <span className="text-xs bg-purple-50 text-purple-700 border border-purple-200 px-3 py-1 rounded-full font-bold">
              Adaptive Teaching
            </span>
          </div>

          {/* Analogy & Walkthrough Content */}
          <div className="text-base text-slate-800 leading-relaxed whitespace-pre-line bg-slate-50 p-6 rounded-2xl border border-slate-200 font-sans">
            {adaptiveBreakdown.content}
          </div>

          {/* Micro-Check Question */}
          {adaptiveBreakdown.mini_question && (
            <div className="bg-purple-50/50 border border-purple-200 rounded-2xl p-6 space-y-4">
              <div className="flex items-center gap-2 text-xs font-bold text-purple-800 uppercase tracking-wider">
                <Sparkles className="w-4 h-4 text-purple-600" />
                <span>Quick Check: Confirm Your Understanding</span>
              </div>

              <p className="text-base font-bold text-slate-900">
                {adaptiveBreakdown.mini_question.question}
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {adaptiveBreakdown.mini_question.options.map((opt, oIdx) => {
                  const isSelected = microAnswer === opt;
                  let optStyle = "bg-white border-slate-200 text-slate-800 hover:border-purple-300";

                  if (microEvaluated) {
                    if (opt === adaptiveBreakdown.mini_question.correct_option) {
                      optStyle = "bg-emerald-50 border-emerald-500 text-emerald-900 font-bold";
                    } else if (isSelected) {
                      optStyle = "bg-rose-50 border-rose-300 text-rose-900";
                    }
                  } else if (isSelected) {
                    optStyle = "bg-purple-100 border-purple-600 text-purple-950 font-bold";
                  }

                  return (
                    <button
                      key={oIdx}
                      onClick={() => !microEvaluated && setMicroAnswer(opt)}
                      disabled={microEvaluated}
                      className={`p-4 rounded-xl border text-sm text-left transition-all cursor-pointer ${optStyle}`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>

              {!microEvaluated && (
                <div className="flex justify-end pt-2">
                  <button
                    onClick={handleMicroSubmit}
                    disabled={!microAnswer}
                    className="btn-primary text-sm px-6 py-2.5 font-bold cursor-pointer"
                  >
                    <span>Check Understanding</span>
                  </button>
                </div>
              )}

              {/* Improved Mastery Celebration Banner */}
              {improvedMastery && (
                <div className="p-5 bg-emerald-50 border border-emerald-300 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 animate-in zoom-in duration-200">
                  <div className="flex items-center gap-3">
                    <Award className="w-8 h-8 text-emerald-600 shrink-0" />
                    <div>
                      <h5 className="text-base font-bold text-emerald-950">
                        Concept Mastered! Learning Gap Resolved.
                      </h5>
                      <p className="text-sm text-emerald-800">
                        Recursion mastery improved: <strong>{improvedMastery.before}% &rarr; {improvedMastery.after}% (+{improvedMastery.delta}%)</strong>
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => fetchQuestion("Trees")}
                    className="btn-primary text-sm px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 shrink-0 cursor-pointer"
                  >
                    <span>Advance to Trees</span>
                    <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
