import React, { useState } from 'react';
import { Sparkles, CheckCircle2, ChevronRight, X, Play } from 'lucide-react';

const TOUR_STEPS = [
  {
    step: 1,
    time: "0:00 - 0:30",
    title: "1. Unified Multimodal Knowledge Base",
    action: "Go to 'Course Sources' or view Home",
    description:
      "A student preparing for exams uploads their PDF Textbook (Data Structures & Algorithms Analysis), " +
      "PowerPoint Slides (Searching & Sorting), and Lecture Recording transcripts (DSA Lecture 3). " +
      "LearnForge AI ingests all three multimodal formats into a unified FAISS vector knowledge base with page, slide, and timestamp citations.",
    badge: "Multimodal Grounding"
  },
  {
    step: 2,
    time: "0:30 - 1:00",
    title: "2. Grounded AI Tutor with Exact Citations",
    action: "Go to 'AI Tutor' and ask 'Why does recursion need a base case?'",
    description:
      "Ask the tutor about recursion. Notice the verified citations attached to the response: " +
      "[Textbook · p.58] and [Lecture · 12:34]. Click any citation chip to inspect the exact retrieved excerpt. " +
      "Expand the RAG Inspector to see raw cosine similarity scores.",
    badge: "Zero Hallucination"
  },
  {
    step: 3,
    time: "1:00 - 1:45",
    title: "3. Adaptive Diagnostic Assessment",
    action: "Click 'Practice', select Recursion, and take the quiz",
    description:
      "Click 'Submit Answer' with an incorrect choice like 'It automatically stops and returns 0'. " +
      "The engine diagnoses the exact misconception: missing base cases cause StackOverflowError!",
    badge: "Misconception Diagnosis"
  },
  {
    step: 4,
    time: "1:45 - 2:30",
    title: "4. Teach Differently (The 'Wow' Feature)",
    action: "Click 'Teach Me Differently' button",
    description:
      "Most AI bots simply repeat the textbook. LearnForge AI switches strategy! " +
      "It delivers Strategy 2: Russian Nesting Dolls (Matryoshka) Analogy and a step-by-step factorial(4) call stack trace. " +
      "The student completes the micro-check question and achieves conceptual clarity.",
    badge: "Adaptive Pedagogy"
  },
  {
    step: 5,
    time: "2:30 - 3:00",
    title: "5. Student Model Recalibration & Recommendation",
    action: "View 'My Progress' and 'Home'",
    description:
      "Student answers correctly. The explainable mastery formula recalculates: " +
      "Recursion mastery jumps from 42% to 67% (+25%). " +
      "The recommendation engine warns: 'Practice Recursion before Trees because Recursion is an essential prerequisite for tree traversal algorithms.'",
    badge: "Measurable Learning Change"
  }
];

export default function DemoTourModal({ isOpen, onClose, onNavigate }) {
  const [currentIdx, setCurrentIdx] = useState(0);

  if (!isOpen) return null;

  const current = TOUR_STEPS[currentIdx];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
      <div className="bg-white border border-slate-200 rounded-2xl max-w-xl w-full p-6 shadow-2xl relative animate-in fade-in zoom-in duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1.5 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 mb-2">
          <span className="p-1.5 bg-purple-50 text-purple-700 rounded-lg border border-purple-200">
            <Sparkles className="w-4 h-4" />
          </span>
          <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
            Judge Demo Walkthrough (3 Minutes)
          </span>
        </div>

        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
          <h3 className="text-lg font-bold text-slate-900">
            {current.title}
          </h3>
          <span className="text-xs font-mono bg-purple-50 text-purple-700 px-2.5 py-1 rounded-md border border-purple-200 font-bold">
            {current.time}
          </span>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 mb-5 space-y-2.5">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              {current.badge}
            </span>
            <span className="text-xs text-slate-500 font-medium">Recommended Action:</span>
            <span className="text-xs text-purple-700 font-bold">{current.action}</span>
          </div>
          <p className="text-sm text-slate-700 leading-relaxed">
            {current.description}
          </p>
        </div>

        {/* Step indicator pagination */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex gap-1.5">
            {TOUR_STEPS.map((s, idx) => (
              <button
                key={s.step}
                onClick={() => setCurrentIdx(idx)}
                className={`h-2 rounded-full transition-all cursor-pointer ${
                  idx === currentIdx ? 'bg-purple-600 w-8' : 'bg-slate-200 hover:bg-slate-300 w-5'
                }`}
              />
            ))}
          </div>

          <div className="flex items-center gap-2">
            {currentIdx > 0 && (
              <button
                onClick={() => setCurrentIdx(currentIdx - 1)}
                className="btn-secondary text-xs px-3.5 py-2"
              >
                Previous
              </button>
            )}

            {currentIdx < TOUR_STEPS.length - 1 ? (
              <button
                onClick={() => setCurrentIdx(currentIdx + 1)}
                className="btn-primary text-xs px-4 py-2"
              >
                Next Step <ChevronRight className="w-3.5 h-3.5" />
              </button>
            ) : (
              <button
                onClick={onClose}
                className="btn-primary text-xs px-4 py-2 bg-emerald-600 hover:bg-emerald-700"
              >
                Start Exploring! <CheckCircle2 className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
