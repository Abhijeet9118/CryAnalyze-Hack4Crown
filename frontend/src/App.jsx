import { useState, useRef } from 'react';
import axios from 'axios';
import { Mic, Upload, Activity, AlertTriangle, CheckCircle, ShieldCheck, Server, RefreshCw } from 'lucide-react';

// Smart API URL Detection:
// Localhost uses http://localhost:8000
// Deployed GitHub Pages uses Render backend or local fallback
const DEFAULT_API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : 'https://cryanalyze-hack4crown.onrender.com';

function App() {
  const [apiUrl, setApiUrl] = useState(DEFAULT_API_URL);
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
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
      setStatusMessage('Recording audio...');
    } catch (err) {
      console.error("Microphone access denied", err);
      alert('Microphone access required to record audio.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
      setStatusMessage('Audio clip captured.');
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioBlob(file);
      setResult(null);
      setStatusMessage(`File selected: ${file.name}`);
    }
  };

  const analyzeAudio = async () => {
    if (!audioBlob) return;
    setIsAnalyzing(true);
    setResult(null);
    setStatusMessage('Analyzing audio spectrum...');

    const formData = new FormData();
    formData.append('audio', audioBlob, 'cry_audio.wav');

    // Attempt 1: Send to primary API URL
    try {
      const targetUrl = `${apiUrl.replace(/\/$/, '')}/analyze`;
      const response = await axios.post(targetUrl, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 45000 // Render free instance wake-up timeout
      });
      setResult(response.data);
      setStatusMessage('Analysis complete.');
    } catch (error) {
      console.warn('Primary backend failed, attempting local fallback...', error);
      
      // Attempt 2: Fallback to localhost if running locally
      if (apiUrl !== 'http://localhost:8000') {
        try {
          setStatusMessage('Primary cloud waking up... Trying local server...');
          const fallbackResponse = await axios.post('http://localhost:8000/analyze', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
            timeout: 5000
          });
          setResult(fallbackResponse.data);
          setApiUrl('http://localhost:8000');
          setStatusMessage('Connected via local server.');
          setIsAnalyzing(false);
          return;
        } catch (localErr) {
          console.error('Local fallback also failed', localErr);
        }
      }
      
      alert(`Could not connect to backend server at: ${apiUrl}\n\nTip: If using Render free tier, wait 30 seconds for server to wake up, or make sure your Render web service status is Live!`);
      setStatusMessage('Backend connection error.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-8 text-slate-100 flex flex-col items-center">
      {/* Header */}
      <header className="w-full max-w-3xl mb-8 flex flex-col md:flex-row items-center justify-between border-b border-slate-700 pb-6 gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-wider text-cyan-400">CryAnalyze</h1>
          <p className="text-slate-400 mt-1 text-xs md:text-sm tracking-widest uppercase">AI-Powered Infant Cry Triage</p>
        </div>
        <div className="flex items-center space-x-2 text-cyan-400 bg-slate-800/80 px-4 py-2 rounded-lg border border-slate-700">
          <ShieldCheck size={24} />
          <span className="font-semibold tracking-widest text-xs uppercase">Code Build 1.0</span>
        </div>
      </header>

      {/* Backend Settings Bar */}
      <div className="w-full max-w-3xl mb-6 bg-slate-800/60 p-3 rounded-lg border border-slate-700/80 flex flex-col sm:flex-row items-center justify-between text-xs gap-2">
        <div className="flex items-center text-slate-400">
          <Server size={14} className="mr-2 text-cyan-400" />
          <span>Backend Server:</span>
        </div>
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <input 
            type="text" 
            value={apiUrl} 
            onChange={(e) => setApiUrl(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs w-full sm:w-64 focus:outline-none focus:border-cyan-400"
            placeholder="http://localhost:8000"
          />
          <button 
            onClick={() => setApiUrl('http://localhost:8000')} 
            className="bg-slate-700 hover:bg-slate-600 px-2 py-1 rounded text-slate-300 transition-all whitespace-nowrap"
            title="Use Localhost"
          >
            Local
          </button>
        </div>
      </div>

      {/* Main Container */}
      <main className="w-full max-w-3xl grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Left Column - Input */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-xl flex flex-col justify-center items-center min-h-72">
          <h2 className="text-lg font-semibold mb-6 text-slate-200">Capture Audio Clip</h2>
          
          <div className="flex space-x-4 mb-6">
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`p-4 rounded-full transition-all shadow-lg ${
                isRecording ? 'bg-red-500 hover:bg-red-600 animate-pulse' : 'bg-cyan-600 hover:bg-cyan-500'
              }`}

            >
              <Mic size={28} />
            </button>
            <label className="p-4 rounded-full bg-slate-700 hover:bg-slate-600 cursor-pointer transition-all flex items-center justify-center shadow-lg">
              <Upload size={28} />
              <input type="file" accept="audio/*" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>

          <div className="text-center min-h-16 flex flex-col items-center justify-center">
            {isRecording && <p className="text-red-400 font-medium animate-pulse">Listening to cry audio...</p>}
            {audioBlob && !isRecording && (
              <div>
                <p className="text-emerald-400 mb-3 font-medium flex items-center justify-center text-sm">
                  <CheckCircle size={16} className="mr-2"/> Audio Ready for Analysis
                </p>
                <button 
                  onClick={analyzeAudio}
                  disabled={isAnalyzing}
                  className="bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold py-2.5 px-6 rounded-lg transition-all disabled:opacity-50 flex items-center shadow-lg text-sm"
                >
                  {isAnalyzing ? (
                    <><Activity className="animate-spin mr-2" size={18}/> Processing Spectrum...</>
                  ) : (
                    "Analyze Cry"
                  )}
                </button>
              </div>
            )}
            {!audioBlob && !isRecording && (
              <p className="text-xs text-slate-500">Record mic audio or upload a .wav sample clip</p>
            )}
          </div>
        </div>

        {/* Right Column - Output */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-xl min-h-72 flex flex-col relative overflow-hidden">
          <h2 className="text-lg font-semibold mb-4 text-slate-200 border-b border-slate-700 pb-2">Analysis & Triage Result</h2>
          
          {!result && !isAnalyzing && (
            <div className="flex-1 flex items-center justify-center text-slate-500 text-sm">
              <p>Upload or record a cry to view triage results.</p>
            </div>
          )}

          {isAnalyzing && (
            <div className="flex-1 flex flex-col items-center justify-center text-cyan-400 py-6">
              <Activity className="animate-pulse mb-3 text-cyan-400" size={40} />
              <p className="text-sm font-medium">Extracting Mel-Spectrogram & MFCCs...</p>
              <p className="text-xs text-slate-400 mt-2">{statusMessage}</p>
            </div>
          )}

          {result && !isAnalyzing && (
            <div className="flex-1 flex flex-col">
              <div className="mb-4">
                <span className="text-xs text-slate-400 uppercase tracking-wider">Classification</span>
                <h3 className="text-2xl font-bold text-white mt-1">{result.prediction}</h3>
              </div>
              
              <div className="mb-6">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Model Confidence</span>
                  <span className="text-cyan-400 font-semibold">{Math.round(result.confidence * 100)}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div className="bg-cyan-400 h-2 rounded-full transition-all duration-500" style={{ width: `${result.confidence * 100}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-lg mt-auto flex items-start ${result.escalate ? 'bg-red-500/20 border border-red-500/50 text-red-200' : 'bg-emerald-500/20 border border-emerald-500/50 text-emerald-200'}`}>
                <div className="mr-3 mt-0.5 shrink-0">
                  {result.escalate ? <AlertTriangle size={20} className="text-red-400"/> : <CheckCircle size={20} className="text-emerald-400"/>}
                </div>
                <div>
                  <h4 className={`font-semibold text-sm ${result.escalate ? 'text-red-400' : 'text-emerald-400'}`}>
                    {result.escalate ? 'Pediatrician Escalation Alert' : 'Soothe & Monitor at Home'}
                  </h4>
                  <p className="text-xs mt-1 leading-relaxed">{result.message}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      
      {/* Footer / Status */}
      <footer className="w-full max-w-3xl mt-8 bg-slate-800/30 p-3 rounded-lg border border-slate-700/50 text-center">
        <p className="text-xs text-slate-500">
          <strong>100% Offline Edge ML Inference Architecture</strong> | Team Foxfin
        </p>
      </footer>
    </div>
  );
}

export default App;
