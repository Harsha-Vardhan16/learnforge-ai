import React from 'react';
import { 
  Home, 
  MessageSquare, 
  Target, 
  BarChart3, 
  BookOpen, 
  Terminal,
  Flame,
  AlertCircle,
  FolderOpen
} from 'lucide-react';

const MAIN_NAV_ITEMS = [
  { id: 'dashboard', label: 'Home', icon: Home },
  { id: 'chat', label: 'AI Tutor', icon: MessageSquare },
  { id: 'practice', label: 'Practice', icon: Target },
  { id: 'progress', label: 'My Progress', icon: BarChart3 }
];

export default function Sidebar({ 
  activeTab, 
  onTabChange, 
  weakTopics = [], 
  judgeMode = false 
}) {
  return (
    <aside className="w-60 bg-white border-r border-slate-200 flex flex-col justify-between p-4 shrink-0 h-[calc(100vh-4rem)] sticky top-16 shadow-2xs">
      {/* Primary Navigation */}
      <div className="space-y-6">
        <div className="space-y-1">
          <div className="px-3 py-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Learn
          </div>

          {MAIN_NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-3 rounded-xl text-base font-semibold transition-all cursor-pointer ${
                  isActive
                    ? 'bg-purple-600 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* Secondary / Judge Sections */}
        <div className="space-y-1 pt-2 border-t border-slate-100">
          <div className="px-3 py-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            {judgeMode ? 'Judge & Developer' : 'Course Files'}
          </div>

          <button
            onClick={() => onTabChange('materials')}
            className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all cursor-pointer ${
              activeTab === 'materials'
                ? 'bg-purple-50 text-purple-700 font-semibold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <BookOpen className="w-4 h-4 text-slate-500" />
              <span>Course Sources</span>
            </div>
            <span className="text-[10px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded font-mono">
              Uploads
            </span>
          </button>

          {judgeMode && (
            <button
              onClick={() => onTabChange('inspector')}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all cursor-pointer ${
                activeTab === 'inspector'
                  ? 'bg-purple-50 text-purple-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Terminal className="w-4 h-4 text-purple-600" />
                <span>RAG Inspector</span>
              </div>
              <span className="text-[10px] bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded font-bold">
                Judge
              </span>
            </button>
          )}
        </div>
      </div>

      {/* Student Study Tip Card */}
      <div className="space-y-3">
        {weakTopics.length > 0 && (
          <div className="bg-rose-50 border border-rose-200/80 rounded-xl p-3 text-xs">
            <div className="flex items-center gap-1.5 font-bold text-rose-800 mb-1">
              <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
              <span>Needs Practice</span>
            </div>
            <p className="text-slate-600 leading-snug">
              Focus on <strong>{weakTopics.join(", ")}</strong> to boost your score.
            </p>
          </div>
        )}

        <div className="flex items-center justify-between px-3 py-2 bg-slate-50 rounded-xl text-xs text-slate-600 border border-slate-100">
          <span className="flex items-center gap-1.5">
            <Flame className="w-4 h-4 text-amber-500" />
            <span>Streak:</span>
          </span>
          <strong className="text-slate-900">3 Days 🔥</strong>
        </div>
      </div>
    </aside>
  );
}
