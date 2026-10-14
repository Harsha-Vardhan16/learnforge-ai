import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Sparkles, 
  Lightbulb, 
  Target, 
  HelpCircle, 
  BookOpen, 
  RotateCcw, 
  ChevronRight,
  Code2,
  Terminal
} from 'lucide-react';
import { api } from '../services/api';
import CitationBadge from '../components/CitationBadge';
import CitationModal from '../components/CitationModal';
import RagInspector from '../components/RagInspector';

const STARTER_PROMPTS = [
  "Explain binary search",
  "Why does recursion need a base case?",
  "How does the call stack work?",
  "Give me an example of recursion in Python"
];

export default function TutorChatPage({ onNavigateToPractice, judgeMode = false }) {
  const [messages, setMessages] = useState([
    {
      role: 'tutor',
      content: 
        "Hello Alex! I am your AI learning companion for Data Structures & Algorithms.\n\n" +
        "Ask me any question about your course materials, or click one of the quick actions below to get started.",
      citations: [
        {
          source_type: 'textbook',
          source_name: 'Data Structures & Algorithm Analysis',
          page: 58,
          timestamp_display: 'Textbook · p.58',
          topic: 'Recursion',
          text_snippet: 'Recursion is a programming technique in which a method invokes itself. A well-formed recursive algorithm must include one or more base cases.',
          relevance_score: 0.884
        },
        {
          source_type: 'lecture',
          source_name: 'DSA Lecture 3: Recursion and Trees',
          start_time: 754.0,
          timestamp_display: 'Lecture · 12:34',
          topic: 'Recursion',
          text_snippet: 'When a function calls itself, Python pushes an activation frame onto the call stack. Without a base case, frames accumulate until a stack overflow occurs.',
          relevance_score: 0.862
        }
      ],
      topic: 'Recursion',
      suggestedFollowups: [
        "Why does recursion need a base case?",
        "Can you trace factorial(3) for me?"
      ]
    }
  ]);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [lastDebugInfo, setLastDebugInfo] = useState([]);
  const [lastQuery, setLastQuery] = useState('');

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend = null, mode = "Explain") => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: query,
      mode: mode
    };

    setMessages(prev => [...prev, userMessage]);
    if (!textToSend) setInput('');
    setLoading(true);
    setLastQuery(query);

    try {
      const response = await api.chatWithTutor({
        message: query,
        mode: mode,
        studentId: 'demo-student-01'
      });

      const tutorMessage = {
        role: 'tutor',
        content: response.response,
        citations: response.citations || [],
        topic: response.topic,
        mode: response.mode,
        adaptive_strategy: response.adaptive_strategy,
        suggestedFollowups: response.suggested_followups || []
      };

      setMessages(prev => [...prev, tutorMessage]);
      if (response.retrieval_debug) {
        setLastDebugInfo(response.retrieval_debug);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'tutor',
          content: "Sorry, I had trouble retrieving your course materials: " + err.message,
          citations: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleExplainSimply = () => {
    handleSendMessage("Can you explain this simply in plain English?", "Simplify");
  };

  const handleGiveExample = () => {
    handleSendMessage("Can you give me a clear code example and walk through it?", "Give Example");
  };

  const handleTestMe = () => {
    if (onNavigateToPractice) {
      onNavigateToPractice("Recursion");
    } else {
      handleSendMessage("Give me a practice quiz question on this topic.", "Quiz Me");
    }
  };

  const handleTeachDifferently = (topic = "Recursion") => {
    handleSendMessage(`I still don't understand ${topic}. Can you explain it differently using an analogy and visual steps?`, "Teach Differently");
  };

  return (
    <div className="w-full flex flex-col h-[calc(100vh-6.5rem)] space-y-4">
      {/* Top Controls: 3 Main Actions */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-purple-50 text-purple-700 rounded-lg">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">AI Tutor</h2>
            <p className="text-xs text-slate-500">Ask questions with real citations from your course material.</p>
          </div>
        </div>

        {/* The 3 Main Actions required by spec */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={handleExplainSimply}
            className="btn-secondary text-xs px-3.5 py-2 hover:border-purple-300 hover:text-purple-700"
            title="Get a beginner-friendly explanation"
          >
            <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
            <span>Explain Simply</span>
          </button>

          <button
            onClick={handleGiveExample}
            className="btn-secondary text-xs px-3.5 py-2 hover:border-purple-300 hover:text-purple-700"
            title="See concrete code and execution walk-through"
          >
            <Code2 className="w-3.5 h-3.5 text-blue-500" />
            <span>Give Example</span>
          </button>

          <button
            onClick={handleTestMe}
            className="btn-primary text-xs px-3.5 py-2 shadow-xs"
            title="Take a quick quiz question"
          >
            <Target className="w-3.5 h-3.5" />
            <span>Test Me</span>
          </button>
        </div>
      </div>

      {/* Chat Messages Conversation Area */}
      <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-6 overflow-y-auto space-y-6 shadow-xs">
        {messages.map((msg, idx) => (
          <div 
            key={idx}
            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className={`max-w-3xl rounded-2xl p-5 shadow-xs leading-relaxed ${
              msg.role === 'user'
                ? 'bg-purple-600 text-white rounded-tr-xs'
                : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-xs'
            }`}>
              {/* Header */}
              <div className="flex items-center justify-between gap-4 mb-2 text-xs opacity-75 border-b border-black/5 pb-1.5 font-medium">
                <span>{msg.role === 'user' ? 'You' : 'LearnForge Tutor'}</span>
                {msg.topic && (
                  <span className="uppercase tracking-wider font-semibold text-[11px]">
                    {msg.topic}
                  </span>
                )}
              </div>

              {/* Message Content */}
              <div className="text-base whitespace-pre-line leading-relaxed">
                {msg.content}
              </div>

              {/* Compact Clickable Citations */}
              {msg.role === 'tutor' && msg.citations && msg.citations.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-200/80">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-2">
                    Sources:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {msg.citations.map((c, cIdx) => (
                      <CitationBadge 
                        key={cIdx} 
                        citation={c} 
                        onClick={(cit) => setSelectedCitation(cit)} 
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Teach Me Differently button (kept available when needed) */}
              {msg.role === 'tutor' && (
                <div className="mt-4 pt-2.5 flex flex-wrap gap-2 text-xs border-t border-slate-200/60">
                  <button
                    onClick={() => handleTeachDifferently(msg.topic || "Recursion")}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 hover:bg-amber-100 transition-colors font-semibold cursor-pointer"
                  >
                    <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
                    <span>Teach Me Differently</span>
                  </button>

                  <button
                    onClick={handleTestMe}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-50 border border-purple-200 text-purple-700 hover:bg-purple-100 transition-colors font-semibold cursor-pointer"
                  >
                    <Target className="w-3.5 h-3.5 text-purple-600" />
                    <span>Test Me on This</span>
                  </button>
                </div>
              )}
            </div>

            {/* Quick Follow-up chips */}
            {msg.role === 'tutor' && msg.suggestedFollowups && msg.suggestedFollowups.length > 0 && idx === messages.length - 1 && (
              <div className="mt-2.5 flex flex-wrap gap-2 max-w-3xl">
                {msg.suggestedFollowups.map((sug, sIdx) => (
                  <button
                    key={sIdx}
                    onClick={() => handleSendMessage(sug)}
                    className="text-xs px-3 py-1.5 rounded-full bg-white hover:bg-purple-50 text-slate-700 hover:text-purple-700 border border-slate-200 transition-colors flex items-center gap-1 cursor-pointer shadow-2xs font-medium"
                  >
                    <span>{sug}</span>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 p-4 bg-slate-50 border border-slate-200 rounded-2xl max-w-sm text-slate-600">
            <div className="w-4 h-4 rounded-full border-2 border-purple-600 border-t-transparent animate-spin" />
            <span className="text-sm font-medium">Checking course materials & answering...</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Starter Prompts Bar (when conversation is short) */}
      {messages.length <= 2 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs text-slate-500 shrink-0">
          <span className="font-semibold text-slate-400 shrink-0">Try asking:</span>
          {STARTER_PROMPTS.map((prompt, pIdx) => (
            <button
              key={pIdx}
              onClick={() => handleSendMessage(prompt)}
              className="px-3 py-1.5 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 whitespace-nowrap cursor-pointer transition-colors font-medium shadow-2xs"
            >
              "{prompt}"
            </button>
          ))}
        </div>
      )}

      {/* Input Composer */}
      <div className="bg-white border border-slate-200 rounded-2xl p-2.5 flex items-center gap-3 shrink-0 shadow-xs">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
          placeholder="Ask a question about your course materials..."
          className="flex-1 bg-transparent px-4 py-2.5 text-base text-slate-900 placeholder-slate-400 focus:outline-none"
        />

        <button
          onClick={() => handleSendMessage()}
          disabled={!input.trim() || loading}
          className="btn-primary text-sm px-5 py-2.5 shrink-0 disabled:opacity-40 disabled:cursor-not-allowed font-bold"
        >
          <Send className="w-4 h-4" />
          <span>Send</span>
        </button>
      </div>

      {/* RAG Inspector (Only shown in Judge View) */}
      {judgeMode && (
        <RagInspector debugItems={lastDebugInfo} activeQuery={lastQuery} />
      )}

      {/* Citation Inspector Modal */}
      {selectedCitation && (
        <CitationModal
          citation={selectedCitation}
          onClose={() => setSelectedCitation(null)}
        />
      )}
    </div>
  );
}
