const API_BASE = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Accept": "application/json",
        ...(options.headers || {})
      }
    });

    if (!res.ok) {
      let errDetail = `HTTP ${res.status}`;
      try {
        const errorJson = await res.json();
        errDetail = errorJson.detail || errDetail;
      } catch (_) {
        errDetail = await res.text() || errDetail;
      }
      throw new Error(errDetail);
    }

    return await res.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // System Health
  getHealth: () => request("/health"),

  // Student Progress & Analytics
  getProgress: (studentId = "demo-student-01") =>
    request(`/progress?student_id=${encodeURIComponent(studentId)}`),

  getTopicMastery: (studentId = "demo-student-01") =>
    request(`/progress/topics?student_id=${encodeURIComponent(studentId)}`),

  getRecommendations: (studentId = "demo-student-01") =>
    request(`/recommendations?student_id=${encodeURIComponent(studentId)}`),

  // Course & Knowledge Base
  getCourseMaterials: () => request("/course/materials"),
  getCourseTopics: () => request("/course/topics"),

  // Chat & Tutor
  chatWithTutor: ({ message, mode = "Explain", topic = null, studentId = "demo-student-01" }) =>
    request("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, mode, topic, student_id: studentId })
    }),

  explainDifferently: ({ topic, message = "I don't understand, please explain differently", studentId = "demo-student-01" }) =>
    request("/tutor/explain-differently", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, mode: "Teach Differently", topic, student_id: studentId })
    }),

  getHint: ({ topic, message, studentId = "demo-student-01" }) =>
    request("/tutor/hint", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, mode: "Hint", topic, student_id: studentId })
    }),

  // Assessment & Adaptivity
  generateAssessment: ({ topic, difficulty = null, studentId = "demo-student-01" }) =>
    request("/assessment/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, difficulty, student_id: studentId })
    }),

  submitAssessment: ({ questionId, selectedAnswer, studentId = "demo-student-01" }) =>
    request("/assessment/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question_id: questionId, selected_answer: selectedAnswer, student_id: studentId })
    }),

  getAdaptiveTeachingBreakdown: ({ topic, attemptCount = 1, studentId = "demo-student-01" }) =>
    request("/assessment/teach-differently", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, attempt_count: attemptCount, student_id: studentId })
    }),

  // Multimodal File Ingestion
  uploadPDF: (formData) =>
    request("/upload/pdf", {
      method: "POST",
      body: formData
    }),

  uploadSlides: (formData) =>
    request("/upload/slides", {
      method: "POST",
      body: formData
    }),

  uploadVideo: (formData) =>
    request("/upload/video", {
      method: "POST",
      body: formData
    }),

  // Demo Controls
  resetDemoState: () =>
    request("/demo/reset", {
      method: "POST"
    }),

  getDemoStatus: () => request("/demo/status")
};
