# 👑 CryAnalyze: The Complete Project Blueprint
**Team Foxfin (Abhijeet, Jatin Gupta, Siddhant Yadav) | Hack-4-Crown | Track 02: Tech4Health**

---

## 1. Project Overview & Architecture
CryAnalyze is an AI-powered infant cry triage system. It records audio, processes it via a Machine Learning pipeline, and returns a plain-language diagnosis with medical escalation alerts.

**Tech Stack:**
*   **Machine Learning:** `librosa`, `TensorFlow` / `PyTorch`
*   **Backend:** `FastAPI` (Python)
*   **Frontend:** `React` via `Vite`, `TailwindCSS`

---

## 2. Phase 1: Building the Backend (From Scratch)

The backend handles the heavy lifting: receiving audio, extracting audio features, and returning the prediction.

### Step 1: Environment Setup
1. Create a project folder and navigate into it.
2. Create a Python Virtual Environment: `python -m venv venv`
3. Activate it: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install fastapi uvicorn python-multipart librosa numpy pydantic tensorflow`

### Step 2: The ML Pipeline (`ml_pipeline.py`)
This script uses `librosa` to convert the raw audio `.wav` file into a Mel-spectrogram, which is the standard way to process audio for deep learning.
*   **Action:** Write a function `process_audio(file_path)` that loads the audio and extracts features.
*   **Integration:** Load your trained `.h5` CNN model and pass the extracted features into `model.predict()`.

### Step 3: The API Server (`main.py`)
*   **Action:** Initialize a FastAPI app and enable CORS (so the React app can communicate with it).
*   **Action:** Create a `POST /analyze` endpoint that accepts an `UploadFile`, saves the audio locally, passes it to `process_audio()`, and returns the JSON result.

### Step 4: Run the Backend
Run the server using: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.

---

## 3. Phase 2: Building the Frontend (From Scratch)

The frontend is the "live, explainable AI" dashboard that parents (and judges) will interact with.

### Step 1: React Setup
1. Scaffold the app: `npx create-vite@latest frontend --template react`
2. Install UI libraries: `npm install axios lucide-react`
3. Install styling framework: `npm install -D @tailwindcss/postcss tailwindcss`

### Step 2: Building the UI (`App.jsx`)
*   **Capture Mode:** Use the browser's `MediaRecorder` API to capture microphone input, or a standard `<input type="file">` for pre-recorded audio.
*   **API Integration:** Use `axios` to POST the audio blob to `http://localhost:8000/analyze`.
*   **Result Display:** Build a conditional UI that displays:
    1. The predicted classification (e.g., Hunger, Pain).
    2. A confidence score bar.
    3. An Escalation Alert box (Red for "See a Doctor", Green for "Soothe it").

### Step 3: Run the Frontend
Start the React server using: `npm run dev` (Runs on port 5173).

---

## 4. Phase 3: Training the AI Model

To move past a prototype, you must train a real model on the **Donate-a-Cry** corpus.

1.  **Data Prep:** Organize `.wav` files into folders by class (`hungry/`, `pain/`, etc.).
2.  **Feature Extraction:** Write a script looping through all audio files, using `librosa.feature.melspectrogram()` to convert them into 2D numpy arrays (images).
3.  **CNN Architecture:** Build a Convolutional Neural Network (CNN) in TensorFlow/Keras.
    *   *Input Layer* -> *Conv2D* -> *MaxPooling2D* -> *Dropout* -> *Dense (Softmax)*
4.  **Training:** Run `model.fit()` on your dataset. Because the dataset is small, use high Dropout (0.5) to prevent overfitting.
5.  **Export:** Save the weights via `model.save('cry_model.h5')`.

---

## 5. Phase 4: Pitching & Presentation Guide

To win the Tech4Health track, structure your 3-minute pitch as follows:

*   **0:00 - 0:30 (The Hook):** Introduce the problem. Talk about exhausted parents at 3 AM and the lack of pediatric access in rural areas. Do not start with technical jargon.
*   **0:30 - 1:30 (The Live Demo):** Open the React app. Play a crying audio clip into the microphone. Let the judges watch the UI process the audio and display the triage result in real-time.
*   **1:30 - 2:30 (The Tech):** Explain the architecture. Mention how `librosa` extracts the acoustic signature and the CNN classifies it. Mention that the app can run fully offline, proving accessibility.
*   **2:30 - 3:00 (The USP & Closing):** Highlight your Unique Selling Points:
    *   **Zero extra hardware** (accessible to low-income families).
    *   **Screening, not diagnosis** (clinically safe and responsible).

**Q&A Defense Strategy:**
If judges ask about medical liability, confidently reply: *"We designed this as a triage aid, not a diagnostic tool. Our UI specifically uses safe escalation language ('Consult a pediatrician') to prevent panic and prioritize infant safety."*
