import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DemoTourModal from './components/DemoTourModal';
import RagInspector from './components/RagInspector';

// Pages
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import TutorChatPage from './pages/TutorChatPage';
import CourseMaterialsPage from './pages/CourseMaterialsPage';
import PracticePage from './pages/PracticePage';
import ProgressPage from './pages/ProgressPage';

import { api } from './services/api';

export default function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'dashboard' | 'chat' | 'materials' | 'practice' | 'progress' | 'inspector'
  const [judgeMode, setJudgeMode] = useState(false);
  const [progressData, setProgressData] = useState(null);
  const [practiceTopic, setPracticeTopic] = useState('Recursion');
  const [isTourOpen, setIsTourOpen] = useState(false);
  const [backendOnline, setBackendOnline] = useState(true);

  const fetchProgress = async () => {
    try {
      const data = await api.getProgress('demo-student-01');
      setProgressData(data);
      setBackendOnline(true);
    } catch (err) {
      console.warn("Backend connectivity check failed:", err);
      setBackendOnline(false);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, []);

  const handleStartPractice = (topic) => {
    setPracticeTopic(topic || 'Recursion');
    setCurrentView('practice');
  };

  const handleResetDemo = async () => {
    await fetchProgress();
    setPracticeTopic('Recursion');
    setCurrentView('dashboard');
  };

  if (currentView === 'landing') {
    return (
      <LandingPage
        onStartDemo={() => {
          fetchProgress();
          setCurrentView('dashboard');
        }}
        onEnterApp={() => setCurrentView('dashboard')}
      />
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <Navbar
        overallHealth={progressData?.overall_health || 78}
        onResetDemo={handleResetDemo}
        onOpenTour={() => setIsTourOpen(true)}
        backendOnline={backendOnline}
        judgeMode={judgeMode}
        onToggleJudgeMode={() => setJudgeMode(!judgeMode)}
      />

      {/* Main Layout Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar
          activeTab={currentView}
          onTabChange={(tab) => setCurrentView(tab)}
          weakTopics={progressData?.weak_topics || ["Recursion", "Trees"]}
          judgeMode={judgeMode}
        />

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-slate-50">
          <div className="w-full max-w-[1600px] mx-auto">
            {currentView === 'dashboard' && (
              <DashboardPage
                progressData={progressData}
                onNavigate={(tab) => setCurrentView(tab)}
                onStartPractice={handleStartPractice}
              />
            )}

            {currentView === 'chat' && (
              <TutorChatPage
                onNavigateToPractice={(topic) => handleStartPractice(topic)}
                judgeMode={judgeMode}
              />
            )}

            {currentView === 'materials' && (
              <CourseMaterialsPage />
            )}

            {currentView === 'practice' && (
              <PracticePage
                initialTopic={practiceTopic}
                onMasteryUpdated={fetchProgress}
              />
            )}

            {currentView === 'progress' && (
              <ProgressPage
                progressData={progressData}
                onNavigateToPractice={(topic) => handleStartPractice(topic)}
              />
            )}

            {currentView === 'inspector' && (
              <div className="space-y-4">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
                  <h2 className="text-xl font-bold text-slate-900 mb-2">
                    Developer & Judge RAG Retrieval Inspector
                  </h2>
                  <p className="text-sm text-slate-500 mb-6">
                    This panel verifies live vector search, cosine distance metrics, and ground-truth metadata provenance.
                  </p>
                  <RagInspector
                    activeQuery="Why does recursion require a base case?"
                    debugItems={[
                      {
                        rank: 1,
                        citation: "Textbook · p.58",
                        source_type: "textbook",
                        source_name: "Data Structures & Algorithm Analysis",
                        similarity_score: 0.8842,
                        topic: "Recursion",
                        page: 58,
                        snippet: "Recursion is a programming technique in which a method invokes itself. A well-formed recursive algorithm must satisfy two requirements: First, it must include one or more base cases. Without a valid base case, recursive calls consume stack frames until StackOverflowError."
                      },
                      {
                        rank: 2,
                        citation: "Lecture · 12:34",
                        source_type: "lecture",
                        source_name: "DSA Lecture 3: Recursion and Trees",
                        similarity_score: 0.8621,
                        topic: "Recursion",
                        start_time: 754.0,
                        timestamp_display: "12:34",
                        snippet: "When a function calls itself, Python or Java pushes a new activation frame onto the call stack. If your base case is missing, those frames keep piling up until memory runs out. That is stack overflow."
                      },
                      {
                        rank: 3,
                        citation: "Slides · Slide 8",
                        source_type: "slides",
                        source_name: "Recursion & Trees Masterclass",
                        similarity_score: 0.7955,
                        topic: "Recursion",
                        slide: 8,
                        snippet: "Slide 8: Anatomy of a Recursive Function. Every recursive function consists of: 1. Base Case: The condition that terminates the recursion. 2. Recursive Step: Transforming input toward the base case."
                      }
                    ]}
                  />
                </div>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Guided Judge Demo Tour Modal */}
      <DemoTourModal
        isOpen={isTourOpen}
        onClose={() => setIsTourOpen(false)}
        onNavigate={(tab) => {
          setCurrentView(tab);
          setIsTourOpen(false);
        }}
      />
    </div>
  );
}
