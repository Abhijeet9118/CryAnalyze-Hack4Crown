import os, librosa
from ml_pipeline import extract_acoustic_features
from test_knn import classify_normalized_knn

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

print("=" * 90)
print("TESTING NORMALIZED KNN CLASSIFIER (ZERO TRAP)")
print("=" * 90)

correct = 0
total = 0
for path, expected in all_samples:
    if os.path.exists(path):
        y, sr = librosa.load(path, sr=16000)
        feat = extract_acoustic_features(y, sr)
        pred, conf, probs = classify_normalized_knn(feat)
        match = "PASS" if pred == expected else "FAIL"
        if pred == expected:
            correct += 1
        total += 1
        print(f"[{match}] {os.path.basename(path):<28} | Expected: {expected:<26} | Got: {pred:<26} | Conf: {int(conf*100):>3}%")
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        for label, prob in sorted_probs[:3]:
            print(f"       -> {label:<26} {int(prob*100):>3}%")
        print()

print("=" * 90)
print(f"Overall Accuracy: {correct}/{total} ({100*correct//total}%)")
