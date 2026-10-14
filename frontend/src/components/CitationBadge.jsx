import React from 'react';
import { BookOpen, Presentation, Video, FileText } from 'lucide-react';

export default function CitationBadge({ citation, onClick }) {
  const getIcon = () => {
    switch (citation.source_type?.toLowerCase()) {
      case 'textbook':
        return <BookOpen className="w-3.5 h-3.5 text-purple-600" />;
      case 'slides':
        return <Presentation className="w-3.5 h-3.5 text-amber-600" />;
      case 'lecture':
        return <Video className="w-3.5 h-3.5 text-emerald-600" />;
      default:
        return <FileText className="w-3.5 h-3.5 text-blue-600" />;
    }
  };

  return (
    <button
      onClick={() => onClick && onClick(citation)}
      className="badge-citation inline-flex items-center gap-1.5 px-3 py-1 text-xs rounded-lg bg-purple-50 hover:bg-purple-100 border border-purple-200 text-purple-700 transition-all cursor-pointer font-semibold shadow-2xs"
      title={`Click to view verified excerpt from ${citation.source_name}`}
    >
      {getIcon()}
      <span className="tracking-tight">
        {citation.timestamp_display || `${citation.source_name}`}
      </span>
    </button>
  );
}
