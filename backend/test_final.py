import os
from ml_pipeline import process_audio

all_samples = [
    ('test_audio/hunger_cry_rhythmic.wav', 'Hunger'),
    ('test_audio/pain_colic_screaming.wav', 'Pain / Colic'),
    ('test_audio/discomfort_diaper_fuss.wav', 'Discomfort (Diaper/Temp)'),
    ('test_audio/tired_whimper_yawn.wav', 'Tiredness / Overstimulated'),
    ('test_audio/belly_gas_grunts.wav', 'Belly Gas / Reflux'),
    ('test_audio/baby_cooing_safe.wav', 'Normal / Cooing'),
    ('test_audio/test_adult_voice.wav', 'Normal / Cooing'),
    ('test_audio/test_room_hiss.wav', 'Normal / Cooing'),
]

print("=" * 100)
print("FULL CLASSIFICATION TEST ON REAL BABY CRY AUDIO + AMBIENT AUDIO")
print("=" * 100)

correct = 0
total = 0
for path, expected in all_samples:
    if os.path.exists(path):
        res = process_audio(path)
        pred = res["prediction"]
        conf = int(res["confidence"] * 100)
        match = "PASS" if pred == expected else "FAIL"
        if pred == expected:
            correct += 1
        total += 1
        f0 = res["acoustic_metrics"]["mean_pitch_hz"]
        rms = res["acoustic_metrics"]["energy_rms"]
        cent = res["acoustic_metrics"]["spectral_centroid_hz"]
        print(f"[{match}] {os.path.basename(path):<28} | Expected: {expected:<26} | Got: {pred:<26} | Conf: {conf:>3}% | F0: {f0:>5.1f}Hz | Cent: {cent:>6.1f}Hz | RMS: {rms:.3f}")
        
        # Show top-3 ranked probabilities
        ranked = res.get("ranked_probabilities", [])
        for r in ranked[:3]:
            marker = " >>>" if r["is_primary"] else "    "
            print(f"   {marker} #{r['rank']} {r['label']:<26} {r['percentage']:>5.1f}%")
        print()

print("=" * 100)
print(f"Accuracy: {correct}/{total} ({100*correct//total}%)")
