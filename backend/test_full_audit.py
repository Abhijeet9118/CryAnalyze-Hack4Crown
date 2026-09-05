import os
from ml_pipeline import process_audio

all_samples = [
    'test_audio/hunger_cry_rhythmic.wav',
    'test_audio/pain_colic_screaming.wav',
    'test_audio/discomfort_diaper_fuss.wav',
    'test_audio/tired_whimper_yawn.wav',
    'test_audio/belly_gas_grunts.wav',
    'test_audio/baby_cooing_safe.wav',
    'test_audio/test_adult_voice.wav',
    'test_audio/test_room_hiss.wav'
]

print("=" * 95)
print("COMPREHENSIVE CLASSIFICATION AUDIT (BABY CRIES + ADULT SPEECH + AMBIENT ROOM NOISE)")
print("=" * 95)

for s in all_samples:
    if os.path.exists(s):
        res = process_audio(s)
        pred = res["prediction"]
        conf = int(res["confidence"] * 100)
        esc = res["escalate"]
        f0 = res["acoustic_metrics"]["mean_pitch_hz"]
        rms = res["acoustic_metrics"]["energy_rms"]
        print(f"File: {os.path.basename(s):<30} | Result: {pred:<26} | Conf: {conf:>3}% | Escalate: {str(esc):<5} | F0: {f0:>5.1f}Hz | RMS: {rms:.3f}")

print("=" * 95)
print("Audit Complete!")
