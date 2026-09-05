import os
import numpy as np
import librosa
from ml_pipeline import extract_acoustic_features

base_dir = 'temp_dataset/donateacry_corpus_cleaned_and_updated_data'

stats = {}

print("=" * 85)
print("COMPUTING EMPIRICAL ACOUSTIC CENTROIDS FROM REAL DONATE-A-CRY RECORDINGS")
print("=" * 85)

for cat in ['hungry', 'belly_pain', 'discomfort', 'tired', 'burping']:
    cat_dir = os.path.join(base_dir, cat)
    if not os.path.exists(cat_dir):
        continue
    
    files = [f for f in os.listdir(cat_dir) if f.endswith('.wav')][:30] # Sample 30 real files per class
    f0s, cents, rhythms, highs, flats, rmss = [], [], [], [], [], []
    
    for f in files:
        f_path = os.path.join(cat_dir, f)
        try:
            y, sr = librosa.load(f_path, sr=16000, duration=7.0)
            feat = extract_acoustic_features(y, sr)
            f0s.append(feat["mean_pitch"])
            cents.append(feat["spectral_centroid"])
            rhythms.append(feat["rhythmicity"])
            highs.append(feat["high_freq_ratio"])
            flats.append(feat["spectral_flatness"])
            rmss.append(feat["rms_energy"])
        except Exception:
            continue
            
    stats[cat] = {
        "mean_pitch": round(float(np.mean(f0s)), 1), "std_pitch": max(30.0, round(float(np.std(f0s)), 1)),
        "spec_cent": round(float(np.mean(cents)), 1), "std_cent": max(150.0, round(float(np.std(cents)), 1)),
        "rhythm": round(float(np.mean(rhythms)), 2), "std_rhythm": max(0.15, round(float(np.std(rhythms)), 2)),
        "high_ratio": round(float(np.mean(highs)), 3), "std_high": max(0.08, round(float(np.std(highs)), 3)),
        "flatness": round(float(np.mean(flats)), 3), "std_flatness": max(0.1, round(float(np.std(flats)), 3)),
        "rms": round(float(np.mean(rmss)), 3), "std_rms": max(0.03, round(float(np.std(rmss)), 3))
    }
    print(f"Class: {cat:<12} | Pitch: {stats[cat]['mean_pitch']}±{stats[cat]['std_pitch']} Hz | Cent: {stats[cat]['spec_cent']}±{stats[cat]['std_cent']} Hz | Rhythm: {stats[cat]['rhythm']} | HighRatio: {stats[cat]['high_ratio']}")

print("=" * 85)
