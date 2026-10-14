import React from 'react';
import { 
  ArrowRight, 
  AlertCircle, 
  CheckCircle2, 
  Sparkles, 
  Target, 
  TrendingUp,
  BookOpen
} from 'lucide-react';

export default function DashboardPage({ 
  progressData, 
  onNavigate, 
  onStartPractice 
}) {
  const health = progressData?.overall_health || 78;
  const topics = progressData?.topics || [];
  const weakTopics = progressData?.weak_topics || ["Recursion", "Trees"];
  const strongTopics = progressData?.strong_topics || ["Binary Search", "Arrays"];
  const rec = progressData?.recommended_next;

  const targetTopic = rec?.topic || "Recursion";

  return (
    <div className="w-full space-y-8 animate-in fade-in duration-150">
      {/* 1. Welcome Header */}
      <div className="space-y-1.5">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Welcome back, Alex 👋
        </h1>
        <p className="text-lg text-slate-600 font-medium">
          Here is your personalized study status for <span className="text-purple-700 font-semibold">Data Structures & Algorithms</span>.
        </p>
      </div>

      {/* Main Grid: Progress & Recommended Lesson */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full">
        {/* 2. One Recommended Lesson & Continue Learning (Hero Card) */}
        <div className="lg:col-span-7 lf-card border-purple-200/80 bg-gradient-to-br from-white via-white to-purple-50/40 p-8 flex flex-col justify-between shadow-xs">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-100 text-purple-700 border border-purple-200">
                <Sparkles className="w-3.5 h-3.5 text-purple-600" />
                Recommended Next Step
              </span>
              <span className="text-xs font-semibold text-slate-500">
                Estimated time: 3 mins
              </span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-3">
              {rec?.target_concept || "Recursion → Base Cases & Stack Unwinding"}
            </h2>

            <p className="text-base text-slate-600 leading-relaxed mb-6">
              {rec?.reason || "You should practice Recursion before advancing to Trees because your recursion mastery is currently 42%. Recursion is an essential prerequisite for tree traversal algorithms."}
            </p>
          </div>

          <div>
            {/* Prominent Continue Learning Button */}
            <button
              onClick={() => onStartPractice ? onStartPractice(targetTopic) : onNavigate('practice')}
              className="btn-primary text-base px-8 py-4 w-full sm:w-auto justify-center font-bold shadow-md shadow-purple-600/20 cursor-pointer"
            >
              <span>Continue Learning</span>
              <ArrowRight className="w-5 h-5 ml-1" />
            </button>
          </div>
        </div>

        {/* 3. Overall Learning Progress Card */}
        <div className="lg:col-span-5 lf-card p-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-bold uppercase tracking-wider text-slate-500">
                Overall Progress
              </span>
              <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                <TrendingUp className="w-3.5 h-3.5" /> On Track
              </span>
            </div>

            <div className="flex items-baseline gap-3 mb-4">
              <span className="text-5xl font-black text-slate-900 tracking-tight">
                {health}%
              </span>
              <span className="text-base text-slate-500 font-medium">
                course mastery
              </span>
            </div>

            {/* Simple progress bar */}
            <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden mb-4">
              <div 
                className="bg-purple-600 h-full rounded-full transition-all duration-700"
                style={{ width: `${health}%` }}
              />
            </div>

            <p className="text-sm text-slate-600 leading-relaxed">
              Based on your quiz attempts and concept checks across 5 course topics.
            </p>
          </div>

          <div className="pt-4 border-t border-slate-100 mt-6 flex items-center justify-between text-sm">
            <span className="text-slate-500 font-medium">Mastered concepts:</span>
            <span className="font-bold text-slate-800">{strongTopics.length} of {topics.length || 5}</span>
          </div>
        </div>
      </div>

      {/* 4. Weak Topics (Needs Practice) Card */}
      <div className="lf-card p-6 w-full">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-rose-50 text-rose-600 rounded-lg">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">Topics Needing Practice</h3>
              <p className="text-sm text-slate-500">These concepts have low accuracy and need reinforcement before your exam.</p>
            </div>
          </div>

          <button
            onClick={() => onStartPractice ? onStartPractice("Recursion") : onNavigate('practice')}
            className="text-sm font-semibold text-purple-700 hover:text-purple-800 flex items-center gap-1 cursor-pointer self-start sm:self-center"
          >
            <span>Practice Weakest Topic</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {weakTopics.map((top, idx) => {
            const topicObj = topics.find(t => t.topic === top);
            const score = topicObj ? Math.round(topicObj.mastery * 100) : (top === "Recursion" ? 42 : 51);
            return (
              <div 
                key={idx}
                className="bg-slate-50 border border-slate-200/80 rounded-xl p-4 flex items-center justify-between hover:border-slate-300 transition-colors"
              >
                <div>
                  <h4 className="font-bold text-slate-900 text-base">{top}</h4>
                  <p className="text-xs text-slate-500 mt-0.5">Needs practice before moving ahead</p>
                </div>
                <div className="text-right">
                  <span className="badge-weak">
                    {score}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
