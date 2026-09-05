# 👑 CryAnalyze — AI-Powered Infant Cry Triage
**Team Name:** Foxfin  
**Track:** Healthcare  
**Hackathon:** Code Build 1.0  
**Team Members:** Abhijeet (Team Lead), Jatin Gupta, Siddhant Yadav  

---

## 📌 Project Overview
CryAnalyze is an instant, hardware-free acoustic screening system that categorizes infant cry audio into **Hunger**, **Pain**, **Discomfort**, or **Tiredness** within seconds. It incorporates **Grad-CAM Explainable AI** and a **Responsible Clinical Escalation Engine** to advise parents between home soothing vs consulting a pediatrician.

---

## 🚀 Key Features
* 🎙️ **Zero Hardware Cost**: Captures audio via any basic smartphone or web microphone.
* 🧠 **Live Explainable AI**: Spectrogram & saliency heatmaps render visually on screen.
* 🛡️ **Clinically Honest Triage**: Non-diagnostic screening aid with automatic pediatrician escalation alerts.
* ⚡ **100% Offline Edge Execution**: Runs on local CPU without cloud API or internet dependencies.

---

## 🛠️ Tech Stack
* **Frontend**: React (Vite), TailwindCSS, MediaRecorder API
* **Backend**: FastAPI (Python 3.12), Librosa, NumPy
* **Machine Learning**: TensorFlow / PyTorch CNN, Mel-Spectrogram & MFCC Feature Extraction

---

## 💻 Quickstart (Run Locally)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

* Open App: [http://localhost:5173](http://localhost:5173)  
* API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
