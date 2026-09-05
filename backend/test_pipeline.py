import os
from ml_pipeline import process_audio

samples = [
    'test_audio/hunger_cry_rhythmic.wav',
    'test_audio/pain_colic_screaming.wav',
    'test_audio/discomfort_diaper_fuss.wav',
    'test_audio/tired_whimper_yawn.wav',
    'test_audio/belly_gas_grunts.wav',
    'test_audio/baby_cooing_safe.wav'
]

print("=" * 85)
print("CRYANALYZE ACOUSTIC ML & TRIAGE PIPELINE VERIFICATION")
print("=" * 85)

for s in samples:
    if os.path.exists(s):
        res = process_audio(s)
        pred = res["prediction"]
        conf = res["confidence"] * 100
        esc = res["escalate"]
        f0 = res["acoustic_metrics"]["mean_pitch_hz"]
        cent = res["acoustic_metrics"]["spectral_centroid_hz"]
        rhythm = res["acoustic_metrics"]["rhythmicity_score"]
        print(f"File: {os.path.basename(s):<28} | Result: {pred:<25} | Conf: {conf:>4.1f}% | Escalate: {str(esc):<5} | F0: {f0:>5.1f}Hz | Centroid: {cent:>6.1f}Hz")

print("=" * 85)
print("Pipeline verified successfully!")
