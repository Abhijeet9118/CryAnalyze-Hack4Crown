import os, librosa
from ml_pipeline import extract_acoustic_features
from test_rbf import classify_rbf

samples = [
    'test_audio/hunger_cry_rhythmic.wav',
    'test_audio/pain_colic_screaming.wav',
    'test_audio/discomfort_diaper_fuss.wav',
    'test_audio/tired_whimper_yawn.wav',
    'test_audio/belly_gas_grunts.wav',
    'test_audio/baby_cooing_safe.wav',
    'test_audio/test_adult_voice.wav',
    'test_audio/test_room_hiss.wav'
]

print("=" * 85)
print("EVALUATING CONTINUOUS ACOUSTIC DISTANCE (RBF) CLASSIFIER")
print("=" * 85)

for s in samples:
    if os.path.exists(s):
        y, sr = librosa.load(s, sr=16000)
        feat = extract_acoustic_features(y, sr)
        pred, conf, probs = classify_rbf(feat)
        f0 = feat["mean_pitch"]
        cent = feat["spectral_centroid"]
        rhythm = feat["rhythmicity"]
        print(f"File: {os.path.basename(s):<28} -> {pred:<26} | Conf: {int(conf*100):>3}% | F0: {f0:>5.1f}Hz | Centroid: {cent:>6.1f}Hz | Rhythm: {rhythm}")

print("=" * 85)
