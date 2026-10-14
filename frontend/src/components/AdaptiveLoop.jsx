import React, { useState } from 'react';
import { 
  BookOpen, 
  HelpCircle, 
  AlertTriangle, 
  Sparkles, 
  RotateCcw, 
  CheckCircle, 
  TrendingUp,
  ChevronRight,
  Info
} from 'lucide-react';

const LOOP_STEPS = [
  {
    id: 'learn',
    label: '1. UNDERSTAND',
    icon: BookOpen,
    color: 'from-blue-600 to-indigo-600',
    border: 'border-blue-500',
    title: 'Multimodal Grounded Learning',
    desc: 'Student asks questions. RAG retrieves verified chunks across Textbooks, Slides, and Lecture transcripts.'
  },
  {
    id: 'assess',
    label: '2. TEST',
    icon: HelpCircle,
    color: 'from-indigo-600 to-purple-600',
    border: 'border-indigo-500',
    title: 'Adaptive Assessment',
    desc: 'System dynamically generates diagnostic checks calibrated to the student\'s estimated mastery tier.'
  },
  {
    id: 'gap',
    label: '3. DETECT GAP',
    icon: AlertTriangle,
    color: 'from-amber-600 to-orange-600',
    border: 'border-amber-500',
    title: 'Misconception Diagnosis',
    desc: 'If an error occurs, the engine diagnoses the exact conceptual blind spot (e.g. missing recursion base cases).'
  },
  {
    id: 'adapt',
    label: '4. ADAPT',
    icon: Sparkles,
    color: 'from-emerald-600 to-teal-600',
    border: 'border-emerald-500',
    title: 'Teach Differently',
    desc: 'Instead of repeating definitions, the tutor pivots to real-world analogies, visual state flows, and micro-checks.'
  },
  {
    id: 'practice',
    label: '5. REASSESS',
    icon: RotateCcw,
    color: 'from-cyan-600 to-blue-600',
    border: 'border-cyan-500',
    title: 'Targeted Verification',
    desc: 'The student re-tests on a reinforced micro-problem to confirm mental model correction.'
  },
  {
    id: 'model',
    label: '6. UPDATE MODEL',
    icon: TrendingUp,
    color: 'from-violet-600 to-fuchsia-600',
    border: 'border-violet-500',
    title: 'Explainable Student Model',
    desc: 'Mastery recalculated with accuracy, difficulty factor, and consistency weights. Live progress updates.'
  },
  {
    id: 'recommend',
    label: '7. RECOMMEND',
    icon: CheckCircle,
    color: 'from-emerald-500 to-green-600',
    border: 'border-emerald-400',
    title: 'Explainable Next Step',
    desc: 'Prerequisite graph recommends what to learn next with explicit pedagogical rationale.'
  }
];

export default function AdaptiveLoop({ currentStep = 'gap', onSelectStep }) {
  const [selectedStep, setSelectedStep] = useState(currentStep);

  const active = LOOP_STEPS.find(s => s.id === selectedStep) || LOOP_STEPS[2];

  return (
    <div className="bg-gray-900/90 border border-gray-800 rounded-2xl p-6 shadow-xl mb-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5 border-b border-gray-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
              Core Differentiator
            </span>
          </div>
          <h2 className="text-xl font-bold text-white mt-0.5">
            The Adaptive Tutor Loop
          </h2>
          <p className="text-xs text-gray-400 mt-0.5">
            "Most educational AI systems answer what you ask. LearnForge AI remembers what you struggle with and changes how it teaches."
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs text-gray-400 bg-gray-800/80 px-3 py-1.5 rounded-lg border border-gray-700/60">
          <Info className="w-3.5 h-3.5 text-indigo-400" />
          <span>Click any phase to inspect the engine behavior</span>
        </div>
      </div>

      {/* Pipeline Steps Flow */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 mb-5">
        {LOOP_STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isCurrent = step.id === selectedStep;
          return (
            <button
              key={step.id}
              onClick={() => {
                setSelectedStep(step.id);
                if (onSelectStep) onSelectStep(step.id);
              }}
              className={`flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all cursor-pointer relative group ${
                isCurrent
                  ? `bg-gradient-to-b ${step.color} ${step.border} text-white shadow-lg shadow-indigo-500/20 scale-102`
                  : 'bg-gray-800/50 border-gray-700/60 text-gray-400 hover:border-gray-600 hover:text-gray-200 hover:bg-gray-800'
              }`}
            >
              <div className={`p-2 rounded-lg mb-1.5 ${isCurrent ? 'bg-black/20' : 'bg-gray-700/50 group-hover:bg-gray-700'}`}>
                <Icon className={`w-4 h-4 ${isCurrent ? 'text-white' : 'text-gray-300'}`} />
              </div>
              <span className="text-xs font-bold leading-tight tracking-tight">
                {step.label}
              </span>
              {isCurrent && (
                <span className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-1 bg-white rounded-full" />
              )}
            </button>
          );
        })}
      </div>

      {/* Active Stage Detail Card */}
      <div className="bg-gray-950/80 border border-gray-800 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className={`p-3 rounded-xl bg-gradient-to-br ${active.color} text-white shadow-md`}>
            <active.icon className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
                Phase Breakdown
              </span>
              <span className="text-xs text-gray-500">•</span>
              <span className="text-xs text-gray-400 font-mono">{active.label}</span>
            </div>
            <h4 className="text-base font-bold text-white mt-0.5">{active.title}</h4>
            <p className="text-xs text-gray-300 mt-0.5 max-w-2xl">{active.desc}</p>
          </div>
        </div>

        <div className="text-xs text-gray-400 flex items-center gap-1.5 self-end sm:self-center shrink-0 bg-gray-900 px-3 py-1.5 rounded-lg border border-gray-800">
          <span className="text-emerald-400 font-medium">Stage Active</span>
        </div>
      </div>
    </div>
  );
}
