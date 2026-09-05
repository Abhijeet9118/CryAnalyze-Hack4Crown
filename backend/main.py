from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import json
import time
from datetime import datetime, timedelta
from ml_pipeline import process_audio, SOOTHING_PROTOCOLS, CLASSES

app = FastAPI(
    title="CryAnalyze API",
    description="Acoustic AI infant cry classification, Grad-CAM explainability, and pediatric escalation triage engine.",
    version="2.0.0"
)

# Enable CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
TEST_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "test_audio")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEST_AUDIO_DIR, exist_ok=True)

# Preset Demo Samples Metadata for 1-Click Judge Evaluation
DEMO_SAMPLES = [
    {
        "id": "hunger",
        "title": "Hungry Infant (Rhythmic Wailing)",
        "filename": "hunger_cry_rhythmic.wav",
        "description": "Rhythmic 480Hz cry bursts with periodic breathing pauses and rooting cues.",
        "expected_class": "Hunger",
        "tag": "Feeding Routine",
        "badge_color": "emerald"
    },
    {
        "id": "pain",
        "title": "Acute Colic / Pain (Shrill Screams)",
        "filename": "pain_colic_screaming.wav",
        "description": "High-pitch (>1100Hz) screaming with sustained acoustic strain and unyielding intensity.",
        "expected_class": "Pain / Colic",
        "tag": "ESCALATION ALERT",
        "badge_color": "rose"
    },
    {
        "id": "discomfort",
        "title": "Wet Diaper / Chafing Discomfort",
        "filename": "discomfort_diaper_fuss.wav",
        "description": "Mid-pitch 340Hz irregular whimpers accompanied by shuffling and squirming noise.",
        "expected_class": "Discomfort (Diaper/Temp)",
        "tag": "Physical Check",
        "badge_color": "cyan"
    },
    {
        "id": "tired",
        "title": "Sleepy / Overstimulated Whimper",
        "filename": "tired_whimper_yawn.wav",
        "description": "Descending pitch glide (~280Hz) with prolonged sighing pauses and yawning cadence.",
        "expected_class": "Tiredness / Overstimulated",
        "tag": "Sleep Soothing",
        "badge_color": "cyan"
    },
    {
        "id": "gas",
        "title": "Belly Gas / Reflux Pressure",
        "filename": "belly_gas_grunts.wav",
        "description": "Low 210Hz guttural grunts with abdominal straining bursts and sudden pauses.",
        "expected_class": "Belly Gas / Reflux",
        "tag": "Burp & Digestion",
        "badge_color": "amber"
    },
    {
        "id": "cooing",
        "title": "Healthy Vocalization / Cooing",
        "filename": "baby_cooing_safe.wav",
        "description": "Gentle 440Hz melodic infant chirps and content vocal play (safe baseline).",
        "expected_class": "Normal / Cooing",
        "tag": "Content & Safe",
        "badge_color": "emerald"
    }
]

# Initialize Default 7-Day Cry History if not present
def initialize_history():
    if not os.path.exists(HISTORY_FILE):
        now = datetime.now()
        mock_history = [
            {
                "id": "cry-101",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=6, hours=4)).isoformat(),
                "prediction": "Hunger",
                "confidence": 0.96,
                "escalate": False,
                "triage_level": 1,
                "duration_sec": 42,
                "notes": "Fed 120ml formula, settled promptly."
            },
            {
                "id": "cry-102",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=5, hours=2)).isoformat(),
                "prediction": "Discomfort (Diaper/Temp)",
                "confidence": 0.91,
                "escalate": False,
                "triage_level": 1,
                "duration_sec": 30,
                "notes": "Diaper wetness changed, calm immediately."
            },
            {
                "id": "cry-103",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=4, hours=19)).isoformat(),
                "prediction": "Belly Gas / Reflux",
                "confidence": 0.94,
                "escalate": False,
                "triage_level": 2,
                "duration_sec": 65,
                "notes": "Burped after bicycle legs maneuver."
            },
            {
                "id": "cry-104",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=3, hours=20)).isoformat(),
                "prediction": "Pain / Colic",
                "confidence": 0.98,
                "escalate": True,
                "triage_level": 3,
                "duration_sec": 120,
                "notes": "Evening intense crying episode. Football hold helped."
            },
            {
                "id": "cry-105",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=2, hours=20)).isoformat(),
                "prediction": "Pain / Colic",
                "confidence": 0.97,
                "escalate": True,
                "triage_level": 3,
                "duration_sec": 95,
                "notes": "Witching hour peak at 8:30 PM."
            },
            {
                "id": "cry-106",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(days=1, hours=8)).isoformat(),
                "prediction": "Tiredness / Overstimulated",
                "confidence": 0.92,
                "escalate": False,
                "triage_level": 1,
                "duration_sec": 25,
                "notes": "Swaddled and played white noise."
            },
            {
                "id": "cry-107",
                "baby_name": "Baby Liam",
                "timestamp": (now - timedelta(hours=3)).isoformat(),
                "prediction": "Hunger",
                "confidence": 0.99,
                "escalate": False,
                "triage_level": 1,
                "duration_sec": 38,
                "notes": "Morning feed, calm."
            }
        ]
        with open(HISTORY_FILE, "w") as f:
            json.dump(mock_history, f, indent=2)

initialize_history()

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history_data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=2)

# Models
class HistoryEntry(BaseModel):
    baby_name: Optional[str] = "Baby Liam"
    prediction: str
    confidence: float
    escalate: bool
    triage_level: int
    duration_sec: Optional[int] = 30
    notes: Optional[str] = ""

class TriageRequest(BaseModel):
    cry_type: str
    duration_minutes: int
    has_fever: bool
    temperature_c: Optional[float] = 37.0
    inconsolable: bool
    vomiting: bool
    lethargic: bool

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "CryAnalyze API",
        "version": "2.0.0",
        "mode": "100% Offline Edge ML Inference",
        "endpoints": ["/analyze", "/samples", "/sample-audio/{id}", "/history", "/trends", "/pediatric-report"]
    }

@app.get("/samples")
def get_demo_samples():
    """Returns the list of 6 pre-configured audio test clips for 1-click evaluation."""
    return {"samples": DEMO_SAMPLES}

@app.get("/sample-audio/{sample_id}")
def stream_sample_audio(sample_id: str):
    """Streams demo WAV files for client-side playback."""
    matched = next((s for s in DEMO_SAMPLES if s["id"] == sample_id), None)
    if not matched:
        raise HTTPException(status_code=404, detail="Demo sample not found")
    
    file_path = os.path.join(TEST_AUDIO_DIR, matched["filename"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file missing on disk")
    
    return FileResponse(file_path, media_type="audio/wav", filename=matched["filename"])

@app.post("/analyze")
async def analyze_cry(audio: UploadFile = File(...)):
    """
    Receives raw audio clip (wav/webm/mp3), extracts acoustic metrics,
    executes clinical ML inference, generates Mel-spectrogram + Grad-CAM heatmap,
    and determines pediatric triage escalation.
    """
    temp_filename = f"upload_{int(time.time()*1000)}_{audio.filename}"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        
    try:
        result = process_audio(file_path)
    finally:
        # Clean up temporary uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
            
    return result

@app.get("/history")
def get_cry_history():
    """Fetches persistent cry logs for the active baby profile."""
    return {"history": load_history()}

@app.post("/history")
def add_cry_event(entry: HistoryEntry):
    """Logs a new cry analysis event to the trend history."""
    history = load_history()
    new_event = {
        "id": f"cry-{int(time.time())}",
        "baby_name": entry.baby_name,
        "timestamp": datetime.now().isoformat(),
        "prediction": entry.prediction,
        "confidence": entry.confidence,
        "escalate": entry.escalate,
        "triage_level": entry.triage_level,
        "duration_sec": entry.duration_sec,
        "notes": entry.notes
    }
    history.insert(0, new_event)
    save_history(history)
    return {"status": "success", "event": new_event}

@app.get("/trends")
def get_trend_analytics():
    """Computes 7-day pattern insights, witching hour colic detection, and category ratios."""
    history = load_history()
    
    category_counts = {c: 0 for c in CLASSES}
    hourly_distribution = [0] * 24
    daily_trend = {}
    escalation_count = 0
    
    for item in history:
        pred = item.get("prediction", "Hunger")
        if pred in category_counts:
            category_counts[pred] += 1
            
        if item.get("escalate", False):
            escalation_count += 1
            
        ts_str = item.get("timestamp")
        if ts_str:
            try:
                dt = datetime.fromisoformat(ts_str)
                hour = dt.hour
                hourly_distribution[hour] += 1
                day_key = dt.strftime("%a %d")
                daily_trend[day_key] = daily_trend.get(day_key, 0) + 1
            except Exception:
                pass

    # Colic / Witching Hour pattern detection (high crying between 6 PM - 10 PM)
    evening_cries = sum(hourly_distribution[18:23])
    total_cries = len(history)
    colic_risk = "Moderate" if evening_cries >= 2 else "Low"
    if evening_cries >= 4 or escalation_count >= 3:
        colic_risk = "High (Colic / Witching Hour Cluster Detected)"

    insights = [
        f"Total of {total_cries} cry episodes recorded across monitoring timeline.",
        f"Hunger and Discomfort represent {round((category_counts.get('Hunger',0) + category_counts.get('Discomfort (Diaper/Temp)',0))/(max(1, total_cries))*100)}% of daily routine events.",
        f"Evening distress cluster (6 PM - 10 PM): {evening_cries} recorded episodes (Colic Risk Index: {colic_risk})."
    ]
    
    if escalation_count > 0:
        insights.append(f"⚠️ {escalation_count} high-pitch acute distress episodes flagged for pediatric review.")

    return {
        "total_cries": total_cries,
        "escalation_count": escalation_count,
        "category_counts": category_counts,
        "hourly_distribution": hourly_distribution,
        "daily_trend": daily_trend,
        "colic_risk": colic_risk,
        "insights": insights
    }

@app.post("/triage/evaluate")
def evaluate_clinical_triage(req: TriageRequest):
    """
    Multi-symptom pediatric risk calculator combining cry type with vital signs & red flags.
    """
    risk_score = 0
    red_flags = []
    
    if req.cry_type == "Pain / Colic":
        risk_score += 40
    elif req.cry_type == "Belly Gas / Reflux":
        risk_score += 15
        
    if req.duration_minutes >= 60:
        risk_score += 25
        red_flags.append("Prolonged crying episode (>60 minutes)")
        
    if req.has_fever or (req.temperature_c and req.temperature_c >= 38.0):
        risk_score += 35
        red_flags.append(f"Fever detected ({req.temperature_c}°C / {round(req.temperature_c * 9/5 + 32, 1)}°F)")
        
    if req.inconsolable:
        risk_score += 20
        red_flags.append("Inconsolable despite standard soothing maneuvers")
        
    if req.vomiting:
        risk_score += 25
        red_flags.append("Frequent or projectile vomiting reported")
        
    if req.lethargic:
        risk_score += 30
        red_flags.append("Unusual lethargy or floppiness")

    if risk_score >= 60:
        level = 3
        recommendation = "RED ALERT: Immediate Pediatric Consultation Recommended. Do not delay medical evaluation."
        color = "rose"
    elif risk_score >= 30:
        level = 2
        recommendation = "MODERATE RISK: Active soothing, colic carry, and monitor vitals closely over next 1-2 hours."
        color = "amber"
    else:
        level = 1
        recommendation = "ROUTINE CARE: Standard feeding, diaper check, and comfortable sleep environment."
        color = "emerald"

    return {
        "risk_score": min(100, risk_score),
        "triage_level": level,
        "recommendation": recommendation,
        "badge_color": color,
        "red_flags": red_flags
    }

@app.get("/pediatric-report")
def get_pediatric_report(baby_name: str = "Liam", age_weeks: int = 8):
    """
    Generates a structured clinical consultation summary for doctors.
    """
    history = load_history()
    trends = get_trend_analytics()
    
    return {
        "patient": {
            "name": baby_name,
            "age_weeks": age_weeks,
            "gender": "Male",
            "primary_physician": "Dr. S. Sharma, MD (Pediatrics)",
            "report_generated": datetime.now().strftime("%B %d, %Y - %I:%M %p")
        },
        "monitoring_summary": {
            "total_episodes": len(history),
            "escalations_flagged": trends["escalation_count"],
            "colic_risk_index": trends["colic_risk"],
            "primary_cry_reasons": sorted(trends["category_counts"].items(), key=lambda x: x[1], reverse=True)
        },
        "recent_episodes": history[:5],
        "clinical_notes": "Acoustic screening conducted via CryAnalyze AI edge engine. F0 fundamental pitch, spectral brightness, and rhythmicity tracked in real time. For diagnostic confirmation by licensed pediatrician."
    }
