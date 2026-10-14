import React from 'react';
import { BookOpen, Presentation, Video, FileText, X } from 'lucide-react';

export default function CitationModal({ citation, onClose }) {
  if (!citation) return null;

  const getSourceIcon = (type) => {
    switch (type?.toLowerCase()) {
      case 'textbook':
        return <BookOpen className="w-5 h-5 text-purple-600" />;
      case 'slides':
        return <Presentation className="w-5 h-5 text-amber-600" />;
      case 'lecture':
        return <Video className="w-5 h-5 text-emerald-600" />;
      default:
        return <FileText className="w-5 h-5 text-blue-600" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
      <div className="bg-white border border-slate-200 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative animate-in fade-in zoom-in duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 transition-colors p-1.5 rounded-lg hover:bg-slate-100 cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-slate-100 rounded-xl">
            {getSourceIcon(citation.source_type)}
          </div>
          <div>
            <span className="text-xs font-bold tracking-wider uppercase text-purple-700">
              Verified Course Source
            </span>
            <h3 className="text-lg font-bold text-slate-900">
              {citation.source_name || "Course Material"}
            </h3>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 mb-4 text-sm bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
          <div>
            <span className="text-slate-500 block text-xs">Reference:</span>
            <span className="font-bold text-slate-900">{citation.timestamp_display || "Reference"}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-xs">Topic:</span>
            <span className="font-bold text-purple-700">{citation.topic || "General"}</span>
          </div>
          {citation.page && (
            <div>
              <span className="text-slate-500 block text-xs">Textbook Page:</span>
              <span className="text-slate-800 font-medium">Page {citation.page}</span>
            </div>
          )}
          {citation.slide && (
            <div>
              <span className="text-slate-500 block text-xs">Slide Number:</span>
              <span className="text-slate-800 font-medium">Slide {citation.slide}</span>
            </div>
          )}
          {citation.start_time !== undefined && citation.start_time !== null && (
            <div>
              <span className="text-slate-500 block text-xs">Lecture Timestamp:</span>
              <span className="text-slate-800 font-medium">{citation.timestamp_display}</span>
            </div>
          )}
          {citation.relevance_score && (
            <div>
              <span className="text-slate-500 block text-xs">Vector Match:</span>
              <span className="text-purple-700 font-mono font-bold">
                {(citation.relevance_score * 100).toFixed(1)}% relevance
              </span>
            </div>
          )}
        </div>

        <div className="mb-6">
          <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1.5">
            Verified Excerpt from Material
          </label>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-slate-700 text-sm leading-relaxed max-h-48 overflow-y-auto font-sans italic">
            "{citation.text_snippet || "Excerpt retrieved directly from verified course material."}"
          </div>
        </div>

        <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
          <button
            onClick={onClose}
            className="btn-primary text-sm px-5 py-2 cursor-pointer"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
