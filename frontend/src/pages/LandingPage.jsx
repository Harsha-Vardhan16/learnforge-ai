import React from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  BookOpen, 
  Video, 
  Presentation, 
  ShieldCheck, 
  RotateCcw, 
  CheckCircle2, 
  Flame, 
  Zap, 
  Target, 
  BrainCircuit, 
  FileCheck 
} from 'lucide-react';

export default function LandingPage({ onStartDemo, onEnterApp }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between selection:bg-purple-500 selection:text-white">
      {/* Navigation Header */}
      <nav className="h-16 border-b border-slate-200 bg-white/80 backdrop-blur-xs px-6 sm:px-8 flex items-center justify-between max-w-7xl mx-auto w-full sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-xs">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-slate-900">
              LearnForge <span className="text-purple-600">AI</span>
            </h1>
            <p className="text-[11px] text-slate-500 font-medium">Multimodal AI Hackathon 2026</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onEnterApp}
            className="text-xs text-slate-600 hover:text-slate-900 font-semibold transition-colors hidden sm:block cursor-pointer px-3 py-1.5 rounded-lg hover:bg-slate-100"
          >
            Open Dashboard
          </button>
          <button
            onClick={onStartDemo}
            className="btn-primary text-xs px-4 py-2 font-bold shadow-xs cursor-pointer"
          >
            <span>Try Demo Course</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-6 py-14 flex-1 flex flex-col items-center justify-center text-center">
        {/* Hackathon Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-50 border border-purple-200 text-purple-700 text-xs font-semibold mb-6">
          <Zap className="w-3.5 h-3.5 text-purple-600" />
          <span>IIT Mandi Hackathon 2026 • Personalized Tutoring & Adaptive Learning</span>
        </div>

        {/* Master Headline */}
        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-slate-900 max-w-4xl leading-tight mb-5">
          Stop revising. <br />
          <span className="text-purple-600">
            Start learning adaptively.
          </span>
        </h1>

        {/* Master Subheadline */}
        <p className="text-base sm:text-xl text-slate-600 max-w-2xl leading-relaxed mb-8">
          LearnForge AI turns your lectures, textbooks, and slide decks into an intelligent tutor 
          that remembers what you struggle with and changes how it teaches.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center gap-4 mb-14">
          <button
            onClick={onStartDemo}
            className="btn-primary text-base px-8 py-3.5 font-bold shadow-md shadow-purple-600/20 cursor-pointer"
          >
            <span>Try Demo Course</span>
            <ArrowRight className="w-5 h-5" />
          </button>
          <button
            onClick={onEnterApp}
            className="btn-secondary text-base px-8 py-3.5 font-bold cursor-pointer"
          >
            <span>Explore Course</span>
          </button>
        </div>

        {/* Three Core Differentiator Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left max-w-5xl">
          {/* 1. Multimodal */}
          <div className="lf-card lf-card-hover p-6 flex flex-col justify-between">
            <div>
              <div className="p-3 bg-purple-50 rounded-xl text-purple-600 w-fit mb-4 border border-purple-100">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">MULTIMODAL</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Ingests PDF textbooks, PPTX slides, and timestamped lecture transcripts into a unified FAISS vector knowledge base.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-purple-700 font-semibold flex items-center gap-1">
              <span>PDF · PPTX · Video Transcripts</span>
            </div>
          </div>

          {/* 2. Source-Cited */}
          <div className="lf-card lf-card-hover p-6 flex flex-col justify-between">
            <div>
              <div className="p-3 bg-emerald-50 rounded-xl text-emerald-600 w-fit mb-4 border border-emerald-100">
                <FileCheck className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">SOURCE-CITED</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Every answer connects back to verified course materials with exact citations: <em>Textbook · p.58</em> and <em>Lecture · 12:34</em>.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-emerald-700 font-semibold flex items-center gap-1">
              <span>Zero Hallucinations</span>
            </div>
          </div>

          {/* 3. Adaptive */}
          <div className="lf-card lf-card-hover p-6 flex flex-col justify-between">
            <div>
              <div className="p-3 bg-amber-50 rounded-xl text-amber-600 w-fit mb-4 border border-amber-100">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">ADAPTIVE</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                When you struggle, the tutor doesn't just repeat words—it switches to real-world analogies, step traces, and recalibrates your mastery.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-amber-700 font-semibold flex items-center gap-1">
              <span>Dynamic Difficulty Loop</span>
            </div>
          </div>
        </div>

        {/* Section: How it works visual pipeline for judges */}
        <div className="mt-12 w-full max-w-5xl bg-white border border-slate-200 rounded-2xl p-6 text-left shadow-xs">
          <span className="text-xs font-bold uppercase tracking-wider text-purple-700 block mb-1">
            System Architecture Pipeline
          </span>
          <h3 className="text-base font-bold text-slate-900 mb-4">
            How LearnForge AI Works End-to-End
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2 text-center text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-800 block font-bold">1. Sources</span>
              <span className="text-[11px] text-slate-500">PDF/PPTX/Audio</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-800 block font-bold">2. Index</span>
              <span className="text-[11px] text-slate-500">FAISS Chunks</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-800 block font-bold">3. RAG</span>
              <span className="text-[11px] text-slate-500">Cosine Match</span>
            </div>
            <div className="p-3 bg-purple-50 rounded-xl border border-purple-200">
              <span className="text-purple-800 block font-bold">4. Tutor</span>
              <span className="text-[11px] text-purple-600">Llama 3.2</span>
            </div>
            <div className="p-3 bg-amber-50 rounded-xl border border-amber-200">
              <span className="text-amber-800 block font-bold">5. Assess</span>
              <span className="text-[11px] text-amber-600">Diagnostic</span>
            </div>
            <div className="p-3 bg-rose-50 rounded-xl border border-rose-200">
              <span className="text-rose-800 block font-bold">6. Detect Gap</span>
              <span className="text-[11px] text-rose-600">Misconception</span>
            </div>
            <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200">
              <span className="text-emerald-800 block font-bold">7. Adapt</span>
              <span className="text-[11px] text-emerald-600">Teach Differently</span>
            </div>
            <div className="p-3 bg-blue-50 rounded-xl border border-blue-200">
              <span className="text-blue-800 block font-bold">8. Model</span>
              <span className="text-[11px] text-blue-600">Update Mastery</span>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="h-14 border-t border-slate-200 px-8 flex items-center justify-between max-w-7xl mx-auto w-full text-xs text-slate-500 bg-white">
        <div>
          LearnForge AI • Personalizing computer science learning through grounded multimodal adaptation.
        </div>
        <div className="font-mono text-slate-400">
          FastAPI · FAISS · React · Tailwind
        </div>
      </footer>
    </div>
  );
}
