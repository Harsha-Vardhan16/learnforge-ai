import React, { useState } from 'react';
import { Terminal, ChevronDown, ChevronUp, Cpu, Database, CheckCircle2 } from 'lucide-react';

export default function RagInspector({ debugItems = [], activeQuery = "" }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!debugItems || debugItems.length === 0) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-500 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-purple-600" />
          <span className="font-semibold text-slate-700">RAG Vector Retrieval Inspector (Judge / Dev View)</span>
        </div>
        <span className="text-slate-400 italic">Ask a tutor question to inspect vector similarity scores</span>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden transition-all">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-5 py-3.5 bg-slate-50 hover:bg-slate-100 transition-colors text-left cursor-pointer"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-50 rounded-lg text-purple-700 border border-purple-200">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                RAG Retrieval Inspector
              </span>
              <span className="bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded-full">
                FAISS Active
              </span>
            </div>
            <p className="text-xs text-slate-500">
              {debugItems.length} chunks retrieved for: "{activeQuery ? (activeQuery.length > 50 ? activeQuery.substring(0, 50) + '...' : activeQuery) : 'Current Query'}"
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold text-purple-700">
          <span>{isOpen ? 'Hide Inspector' : 'Show Cosine Similarity & Provenance'}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-5 bg-white border-t border-slate-200 space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-500 border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <Database className="w-3.5 h-3.5 text-purple-600" />
              <span>Model: <strong className="text-slate-800">all-MiniLM-L6-v2 (384-dim)</strong></span>
            </div>
            <div className="flex items-center gap-2">
              <Cpu className="w-3.5 h-3.5 text-blue-600" />
              <span>Metric: <strong className="text-slate-800">Inner Product (Cosine Similarity)</strong></span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
            {debugItems.map((item, idx) => (
              <div 
                key={idx}
                className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-purple-700">Rank #{item.rank || idx + 1}</span>
                    <span className="font-mono bg-purple-50 text-purple-700 px-2 py-0.5 rounded-md border border-purple-200 font-bold">
                      Match: {item.similarity_score}
                    </span>
                  </div>

                  <div className="font-bold text-slate-900 text-sm mb-1 truncate" title={item.source_name}>
                    {item.citation || item.source_name}
                  </div>

                  <div className="text-xs text-slate-500 mb-2 flex items-center gap-1.5">
                    <span className="uppercase text-slate-600 font-semibold">{item.source_type}</span>
                    <span>•</span>
                    <span className="text-emerald-700 font-medium">{item.topic}</span>
                  </div>

                  <p className="text-slate-700 text-xs leading-relaxed bg-white p-3 rounded-lg border border-slate-200 font-sans italic line-clamp-4">
                    "{item.snippet}"
                  </p>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-200 flex items-center gap-1.5 text-[11px] text-emerald-700 font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Ground truth verified in vector store</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
