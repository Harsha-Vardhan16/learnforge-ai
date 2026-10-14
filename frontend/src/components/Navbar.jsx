import React, { useState } from 'react';
import { 
  Sparkles, 
  RotateCcw, 
  Play, 
  Activity, 
  GraduationCap,
  Shield,
  Check
} from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ 
  overallHealth = 78, 
  onResetDemo, 
  onOpenTour,
  backendOnline = true,
  judgeMode = false,
  onToggleJudgeMode
}) {
  const [resetting, setResetting] = useState(false);

  const handleReset = async () => {
    if (confirm("Reset demo course state to baseline (Recursion 42%, Binary Search 85%, etc.)?")) {
      try {
        setResetting(true);
        await api.resetDemoState();
        if (onResetDemo) onResetDemo();
      } catch (err) {
        alert("Failed to reset demo: " + err.message);
      } finally {
        setResetting(false);
      }
    }
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-40 shadow-xs">
      {/* Brand Identity */}
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-xs">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              LearnForge <span className="text-purple-600">AI</span>
            </h1>
          </div>
          <p className="text-xs text-slate-500 font-medium">Adaptive learning companion</p>
        </div>
      </div>

      {/* Student Progress Badge */}
      <div className="hidden md:flex items-center gap-4">
        <div className="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-full text-xs text-slate-700">
          <GraduationCap className="w-4 h-4 text-purple-600" />
          <span>Student: <strong className="text-slate-900">Alex Chen</strong></span>
        </div>

        <div className="flex items-center gap-2 bg-purple-50 border border-purple-200/80 px-3 py-1.5 rounded-full text-xs">
          <Activity className="w-3.5 h-3.5 text-purple-600" />
          <span className="text-slate-600">Learning Progress:</span>
          <span className="font-bold text-purple-700">{overallHealth}%</span>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2.5">
        {/* Judge Mode Switch */}
        <button
          onClick={onToggleJudgeMode}
          className={`text-xs px-2.5 py-1.5 rounded-lg border font-medium flex items-center gap-1.5 transition-colors cursor-pointer ${
            judgeMode
              ? 'bg-purple-100 text-purple-800 border-purple-300'
              : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
          }`}
          title="Toggle Hackathon Judge / Developer view (reveals RAG Inspector & Sources)"
        >
          <Shield className="w-3.5 h-3.5 text-purple-600" />
          <span className="hidden sm:inline">Judge View</span>
          {judgeMode && <Check className="w-3 h-3 text-purple-700" />}
        </button>

        {/* Demo Tour CTA */}
        <button
          onClick={onOpenTour}
          className="btn-soft-purple text-xs px-3 py-1.5 rounded-lg"
          title="Quick 3-minute guided walkthrough"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span className="hidden sm:inline">Demo Tour</span>
        </button>

        {/* Reset Demo State Button */}
        <button
          onClick={handleReset}
          disabled={resetting}
          className="text-xs px-2.5 py-1.5 text-slate-600 hover:text-slate-900 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 cursor-pointer"
          title="Reset student mastery to initial baseline"
        >
          <RotateCcw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin' : ''}`} />
          <span className="hidden md:inline">{resetting ? 'Resetting...' : 'Reset'}</span>
        </button>

        {/* Status Dot */}
        <div 
          className="flex items-center gap-1.5 pl-2 border-l border-slate-200 text-xs"
          title={backendOnline ? "System connected" : "Connecting..."}
        >
          <span className={`w-2.5 h-2.5 rounded-full ${backendOnline ? 'bg-emerald-500' : 'bg-amber-500 animate-ping'}`} />
        </div>
      </div>
    </header>
  );
}
