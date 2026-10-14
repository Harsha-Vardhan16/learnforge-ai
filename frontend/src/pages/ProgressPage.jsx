import React from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  CheckCircle2, 
  AlertCircle, 
  Flame, 
  Sparkles, 
  ArrowRight,
  BookOpen
} from 'lucide-react';

export default function ProgressPage({ progressData, onNavigateToPractice }) {
  const health = progressData?.overall_health || 78;
  const topics = progressData?.topics || [
    { topic: "Arrays", mastery: 0.90, attempts: 10, correct: 9, incorrect: 1, difficulty_reached: "HARD" },
    { topic: "Binary Search", mastery: 0.85, attempts: 8, correct: 7, incorrect: 1, difficulty_reached: "MEDIUM" },
    { topic: "Sorting", mastery: 0.72, attempts: 6, correct: 4, incorrect: 2, difficulty_reached: "MEDIUM" },
    { topic: "Trees", mastery: 0.51, attempts: 5, correct: 2, incorrect: 3, difficulty_reached: "EASY" },
    { topic: "Recursion", mastery: 0.42, attempts: 7, correct: 3, incorrect: 4, difficulty_reached: "EASY" }
  ];

  const weakTopics = progressData?.weak_topics || ["Recursion", "Trees"];
  const strongTopics = progressData?.strong_topics || ["Arrays", "Binary Search"];
  const rec = progressData?.recommended_next;

  const getBarColor = (val) => {
    if (val >= 0.75) return "bg-emerald-500";
    if (val >= 0.60) return "bg-amber-500";
    return "bg-rose-500";
  };

  const getStatusBadge = (val) => {
    if (val >= 0.75) {
      return (
        <span className="badge-strong">
          <CheckCircle2 className="w-3.5 h-3.5" /> Mastered
        </span>
      );
    }
    if (val >= 0.60) {
      return (
        <span className="badge-competent">
          Good
        </span>
      );
    }
    return (
      <span className="badge-weak">
        <AlertCircle className="w-3.5 h-3.5" /> Needs Practice
      </span>
    );
  };

  return (
    <div className="w-full space-y-6 animate-in fade-in duration-150">
      {/* Top Header Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-900 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-purple-600" />
            My Learning Progress
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Track your mastery across syllabus topics and follow your personalized learning path.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-purple-50 px-4 py-2 rounded-xl border border-purple-200">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            <div>
              <span className="text-xs text-slate-500 block">Overall Mastery</span>
              <strong className="text-xl font-black text-purple-700">{health}%</strong>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-amber-50 px-4 py-2 rounded-xl border border-amber-200">
            <Flame className="w-5 h-5 text-amber-500" />
            <div>
              <span className="text-xs text-slate-500 block">Study Streak</span>
              <strong className="text-xl font-black text-amber-700">3 Days</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Topic Mastery using simple progress bars */}
      <div className="lf-card p-8 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Topic Mastery</h3>
            <p className="text-sm text-slate-500">Progress bars update automatically as you complete practice questions.</p>
          </div>

          <div className="flex items-center gap-4 text-xs font-semibold text-slate-500 hidden sm:flex">
            <span className="flex items-center gap-1.5 text-emerald-700">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Mastered (&ge;75%)
            </span>
            <span className="flex items-center gap-1.5 text-rose-700">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> Needs Practice (&lt;60%)
            </span>
          </div>
        </div>

        {/* List of Simple Progress Bars */}
        <div className="space-y-5">
          {topics.map((t, idx) => {
            const pct = Math.round(t.mastery * 100);
            return (
              <div key={idx} className="bg-slate-50 border border-slate-200/80 rounded-xl p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-base font-bold text-slate-900">{t.topic}</span>
                    {getStatusBadge(t.mastery)}
                  </div>

                  <div className="flex items-center gap-4">
                    <span className="text-xs text-slate-500 font-mono">
                      {t.correct || 0} of {t.attempts || 0} questions correct
                    </span>
                    <span className="text-base font-black text-slate-900 font-mono w-12 text-right">
                      {pct}%
                    </span>
                  </div>
                </div>

                {/* Clean Simple Progress Bar */}
                <div className="w-full bg-slate-200/70 rounded-full h-3 overflow-hidden">
                  <div 
                    className={`h-full rounded-full transition-all duration-500 ${getBarColor(t.mastery)}`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommended Next Steps Card */}
      <div className="lf-card border-purple-200/80 bg-gradient-to-br from-white via-white to-purple-50/30 p-8 space-y-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-bold text-slate-900">Recommended Next Steps</h3>
        </div>

        <div className="bg-white p-5 rounded-xl border border-purple-100 shadow-2xs space-y-3">
          <div className="flex items-start gap-3">
            <span className="w-7 h-7 rounded-full bg-purple-100 text-purple-700 font-bold flex items-center justify-center text-xs shrink-0 mt-0.5">
              1
            </span>
            <div>
              <h4 className="text-base font-bold text-slate-900">
                {rec?.target_concept || "Recursion → Base Cases & Stack Unwinding"}
              </h4>
              <p className="text-sm text-slate-600 mt-1 leading-relaxed">
                {rec?.reason || "Practice Recursion before Trees because Recursion is an essential prerequisite for tree traversal algorithms."}
              </p>
            </div>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={() => onNavigateToPractice ? onNavigateToPractice(rec?.topic || "Recursion") : null}
            className="btn-primary text-sm px-6 py-2.5 font-bold cursor-pointer"
          >
            <span>Start Recommended Practice</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
}
