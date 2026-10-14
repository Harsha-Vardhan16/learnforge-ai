import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Presentation, 
  Video, 
  Upload, 
  CheckCircle2, 
  Database, 
  FileText, 
  FolderTree,
  AlertCircle
} from 'lucide-react';
import { api } from '../services/api';

export default function CourseMaterialsPage() {
  const [materialsData, setMaterialsData] = useState(null);
  const [topicsData, setTopicsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploading, setUploading] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [mat, top] = await Promise.all([
        api.getCourseMaterials(),
        api.getCourseTopics()
      ]);
      setMaterialsData(mat);
      setTopicsData(top.topics || []);
    } catch (err) {
      console.error("Error loading course materials:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFileUpload = async (event, uploadType) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadStatus({ type: 'info', message: `Processing ${file.name}... Extracting chunks and computing embeddings.` });

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("source_name", file.name.replace(/\.[^/.]+$/, ""));

      let res;
      if (uploadType === 'pdf') {
        res = await api.uploadPDF(formData);
      } else if (uploadType === 'slides') {
        res = await api.uploadSlides(formData);
      } else if (uploadType === 'video') {
        res = await api.uploadVideo(formData);
      }

      setUploadStatus({
        type: 'success',
        message: `✓ Successfully processed "${res.source_name}". Created ${res.chunks_created} indexed chunks!`
      });
      await loadData();
    } catch (err) {
      setUploadStatus({
        type: 'error',
        message: `Failed to upload: ${err.message}`
      });
    } finally {
      setUploading(false);
    }
  };

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
    <div className="w-full space-y-6 animate-in fade-in duration-150">
      {/* Top Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
              Multimodal Knowledge Base Ready
            </span>
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mt-1">
            Course Sources & Uploads
          </h2>
          <p className="text-sm text-slate-600 mt-1">
            Textbooks, slides, and lecture video transcripts indexed into your personal searchable knowledge base.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <div className="text-center px-4 border-r border-slate-200">
            <span className="text-2xl font-black text-slate-900 block">
              {materialsData?.total_sources || 3}
            </span>
            <span className="text-[11px] text-slate-500 uppercase font-bold">Sources</span>
          </div>
          <div className="text-center px-4">
            <span className="text-2xl font-black text-purple-700 block">
              {materialsData?.total_chunks || 11}
            </span>
            <span className="text-[11px] text-slate-500 uppercase font-bold">Chunks</span>
          </div>
        </div>
      </div>

      {/* Upload Action Cards */}
      <div>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
          <Upload className="w-4 h-4 text-purple-600" />
          Add Learning Material
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Upload PDF */}
          <label className="lf-card lf-card-hover cursor-pointer border-dashed border-slate-300 flex flex-col items-center justify-center p-6 text-center group bg-white">
            <input 
              type="file" 
              accept=".pdf" 
              className="hidden" 
              disabled={uploading}
              onChange={(e) => handleFileUpload(e, 'pdf')} 
            />
            <div className="p-3 bg-purple-50 text-purple-700 rounded-xl group-hover:scale-105 transition-transform mb-3">
              <BookOpen className="w-6 h-6" />
            </div>
            <span className="text-base font-bold text-slate-900 mb-1">Upload PDF Textbook</span>
            <p className="text-xs text-slate-500">Extracts page-by-page text with academic page citations</p>
          </label>

          {/* Upload Slides */}
          <label className="lf-card lf-card-hover cursor-pointer border-dashed border-slate-300 flex flex-col items-center justify-center p-6 text-center group bg-white">
            <input 
              type="file" 
              accept=".pptx,.ppt" 
              className="hidden" 
              disabled={uploading}
              onChange={(e) => handleFileUpload(e, 'slides')} 
            />
            <div className="p-3 bg-amber-50 text-amber-600 rounded-xl group-hover:scale-105 transition-transform mb-3">
              <Presentation className="w-6 h-6" />
            </div>
            <span className="text-base font-bold text-slate-900 mb-1">Upload PPTX Slides</span>
            <p className="text-xs text-slate-500">Extracts slide-by-slide text, shapes & presentation notes</p>
          </label>

          {/* Upload Lecture Video / Transcript */}
          <label className="lf-card lf-card-hover cursor-pointer border-dashed border-slate-300 flex flex-col items-center justify-center p-6 text-center group bg-white">
            <input 
              type="file" 
              accept=".vtt,.srt,.txt,.json,.mp4" 
              className="hidden" 
              disabled={uploading}
              onChange={(e) => handleFileUpload(e, 'video')} 
            />
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl group-hover:scale-105 transition-transform mb-3">
              <Video className="w-6 h-6" />
            </div>
            <span className="text-base font-bold text-slate-900 mb-1">Upload Lecture Video / Transcript</span>
            <p className="text-xs text-slate-500">Preserves precise timestamp intervals (e.g. 12:34)</p>
          </label>
        </div>

        {uploadStatus && (
          <div className={`mt-3 p-3.5 rounded-xl border text-sm flex items-center gap-2 ${
            uploadStatus.type === 'success' 
              ? 'bg-emerald-50 border-emerald-200 text-emerald-800' 
              : uploadStatus.type === 'error'
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-purple-50 border-purple-200 text-purple-800'
          }`}>
            {uploadStatus.type === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4" />}
            <span>{uploadStatus.message}</span>
          </div>
        )}
      </div>

      {/* Ingested Sources List */}
      <div>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
          <Database className="w-4 h-4 text-emerald-600" />
          Active Course Material
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(materialsData?.materials || []).map((source, idx) => (
            <div 
              key={idx}
              className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-slate-50 rounded-xl">
                    {getSourceIcon(source.source_type)}
                  </div>
                  <span className="badge-strong">
                    <CheckCircle2 className="w-3 h-3" /> Indexed
                  </span>
                </div>

                <h4 className="text-base font-bold text-slate-900 mb-1">
                  {source.source_name}
                </h4>
                <div className="flex items-center gap-2 text-xs text-slate-500 mb-3">
                  <span className="uppercase text-purple-700 font-bold">{source.source_type}</span>
                  <span>•</span>
                  <span>{source.num_chunks} chunks</span>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 text-xs text-slate-500 flex items-center justify-between">
                <span>FAISS Status:</span>
                <span className="text-emerald-700 font-bold">Searchable</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Syllabus Topic Map */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
        <div className="flex items-center gap-2 mb-4">
          <FolderTree className="w-5 h-5 text-purple-600" />
          <div>
            <h3 className="text-base font-bold text-slate-900">Topic Curriculum</h3>
            <p className="text-xs text-slate-500">Prerequisite map governing recommendations</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {topicsData.map((topic, idx) => (
            <div 
              key={idx}
              className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-mono text-slate-400">#{topic.order_index}</span>
                  {topic.prerequisites?.length > 0 && (
                    <span className="text-[10px] bg-purple-50 text-purple-700 px-1.5 py-0.5 rounded border border-purple-200 font-medium">
                      Req: {topic.prerequisites.join(", ")}
                    </span>
                  )}
                </div>
                <h5 className="text-sm font-bold text-slate-900 mb-1">{topic.name}</h5>
                <p className="text-xs text-slate-500 leading-snug">{topic.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
