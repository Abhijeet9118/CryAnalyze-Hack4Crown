import { useState, useRef } from 'react';
import axios from 'axios';
import { Mic, Upload, Activity, AlertTriangle, CheckCircle, ShieldCheck } from 'lucide-react';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const mediaRecorder = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      const chunks = [];
      mediaRecorder.current.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.current.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        setAudioBlob(blob);
      };
      mediaRecorder.current.start();
      setIsRecording(true);
      setResult(null);
    } catch (err) {
      console.error("Microphone access denied", err);
      alert('Microphone access required.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioBlob(file);
      setResult(null);
    }
  };

  const analyzeAudio = async () => {
    if (!audioBlob) return;
    setIsAnalyzing(true);
    setResult(null);

    const formData = new FormData();
    formData.append('audio', audioBlob, 'cry_audio.wav');

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing audio:', error);
      alert('Could not connect to FastAPI backend at http://localhost:8000. Please ensure the backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen p-8 text-slate-100 flex flex-col items-center">
      {/* Header */}
      <header className="w-full max-w-3xl mb-12 flex items-center justify-between border-b border-slate-700 pb-6">
        <div>
          <h1 className="text-4xl font-bold tracking-wider text-cyan-400">CryAnalyze</h1>
          <p className="text-slate-400 mt-2 text-sm tracking-widest uppercase">AI-Powered Infant Cry Triage</p>
        </div>
        <div className="flex items-center space-x-2 text-cyan-500">
          <ShieldCheck size={32} />
          <span className="font-semibold tracking-widest text-sm">Code Build 1.0</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="w-full max-w-3xl grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Left Column - Input */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-xl flex flex-col justify-center items-center h-80">
          <h2 className="text-xl font-semibold mb-6 text-slate-200">Capture Audio</h2>
          
          <div className="flex space-x-4 mb-8">
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`p-4 rounded-full transition-all ${
                isRecording ? 'bg-red-500 hover:bg-red-600 animate-pulse' : 'bg-cyan-600 hover:bg-cyan-500'
              }`}
            >
              <Mic size={32} />
            </button>
            <label className="p-4 rounded-full bg-slate-700 hover:bg-slate-600 cursor-pointer transition-all flex items-center justify-center">
              <Upload size={32} />
              <input type="file" accept="audio/*" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>

          <div className="text-center h-16">
            {isRecording && <p className="text-red-400 font-medium">Listening...</p>}
            {audioBlob && !isRecording && (
              <div>
                <p className="text-emerald-400 mb-2 font-medium flex items-center justify-center">
                  <CheckCircle size={16} className="mr-2"/> Audio Ready
                </p>
                <button 
                  onClick={analyzeAudio}
                  disabled={isAnalyzing}
                  className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold py-2 px-6 rounded-lg transition-all disabled:opacity-50 flex items-center"
                >
                  {isAnalyzing ? (
                    <><Activity className="animate-spin mr-2" size={18}/> Analyzing...</>
                  ) : (
                    "Analyze Cry"
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Right Column - Output */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-xl min-h-80 flex flex-col relative overflow-hidden">
          <h2 className="text-xl font-semibold mb-4 text-slate-200 border-b border-slate-700 pb-2">Analysis Result</h2>
          
          {!result && !isAnalyzing && (
            <div className="flex-1 flex items-center justify-center text-slate-500">
              <p>Upload or record a cry to see results.</p>
            </div>
          )}

          {isAnalyzing && (
            <div className="flex-1 flex flex-col items-center justify-center text-cyan-400">
              <Activity className="animate-pulse mb-4" size={48} />
              <p>Extracting Mel-spectrogram...</p>
              <p className="text-sm text-slate-500 mt-2">Running CNN Classifier</p>
            </div>
          )}

          {result && !isAnalyzing && (
            <div className="flex-1 flex flex-col animation-fadeIn">
              <div className="mb-4">
                <span className="text-sm text-slate-400 uppercase tracking-wider">Classification</span>
                <h3 className="text-3xl font-bold text-white mt-1">{result.prediction}</h3>
              </div>
              
              <div className="mb-6">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Confidence</span>
                  <span className="text-cyan-400 font-medium">{Math.round(result.confidence * 100)}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-cyan-400 h-2 rounded-full" style={{ width: `${result.confidence * 100}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-lg mt-auto flex items-start ${result.escalate ? 'bg-red-500/20 border border-red-500/50 text-red-200' : 'bg-emerald-500/20 border border-emerald-500/50 text-emerald-200'}`}>
                <div className="mr-3 mt-1">
                  {result.escalate ? <AlertTriangle size={20} className="text-red-400"/> : <CheckCircle size={20} className="text-emerald-400"/>}
                </div>
                <div>
                  <h4 className={`font-semibold ${result.escalate ? 'text-red-400' : 'text-emerald-400'}`}>
                    {result.escalate ? 'Escalation Alert' : 'Soothe & Monitor'}
                  </h4>
                  <p className="text-sm mt-1">{result.message}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      
      {/* Footer / Trend Mockup */}
      <footer className="w-full max-w-3xl mt-12 bg-slate-800/30 p-4 rounded-lg border border-slate-700/50 text-center">
        <p className="text-xs text-slate-500">
          <strong>Trend-based Prevention Layer</strong> active. Cry history logged per profile.
        </p>
      </footer>
    </div>
  );
}

export default App;
