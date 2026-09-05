import os
import numpy as np
import librosa
import json

# Add parent to path
import sys
sys.path.insert(0, '.')
from ml_pipeline import extract_acoustic_features

# Compute exact features for each preset sample
presets = {
    "Hunger": "test_audio/hunger_cry_rhythmic.wav",
    "Pain / Colic": "test_audio/pain_colic_screaming.wav",
    "Discomfort (Diaper/Temp)": "test_audio/discomfort_diaper_fuss.wav",
    "Tiredness / Overstimulated": "test_audio/tired_whimper_yawn.wav",
    "Belly Gas / Reflux": "test_audio/belly_gas_grunts.wav",
    "Normal / Cooing": "test_audio/baby_cooing_safe.wav",
}

# Also compute stats across multiple files per category
base_dir = 'temp_dataset/donateacry_corpus_cleaned_and_updated_data'
category_map = {
    "Hunger": "hungry",
    "Pain / Colic": "belly_pain",
    "Discomfort (Diaper/Temp)": "discomfort",
    "Tiredness / Overstimulated": "tired",
    "Belly Gas / Reflux": "burping",
}

print("=" * 90)
print("PRESET SAMPLE EXACT FEATURE VECTORS")
print("=" * 90)

preset_features = {}
for label, path in presets.items():
    if os.path.exists(path):
        y, sr = librosa.load(path, sr=16000, duration=8.0)
        try:
            y_trimmed, _ = librosa.effects.trim(y, top_db=25)
            if len(y_trimmed) > sr * 0.4:
                y = y_trimmed
        except:
            pass
        feat = extract_acoustic_features(y, sr)
        preset_features[label] = feat
        print(f"{label:<28} | F0: {feat['mean_pitch']:>6.1f} | Cent: {feat['spectral_centroid']:>7.1f} | Rhythm: {feat['rhythmicity']:.2f} | HighR: {feat['high_freq_ratio']:.3f} | Flat: {feat['spectral_flatness']:.3f} | RMS: {feat['rms_energy']:.3f}")

print()
print("=" * 90)
print("FULL CATEGORY DISTRIBUTIONS (Up to 30 files each)")
print("=" * 90)

for label, cat_folder in category_map.items():
    cat_dir = os.path.join(base_dir, cat_folder)
    if not os.path.exists(cat_dir):
        continue
    files = [f for f in os.listdir(cat_dir) if f.endswith('.wav')][:30]
    
    all_feats = []
    for f in files:
        try:
            y, sr = librosa.load(os.path.join(cat_dir, f), sr=16000, duration=7.0)
            feat = extract_acoustic_features(y, sr)
            all_feats.append(feat)
        except:
            continue
    
    if all_feats:
        pitches = [f["mean_pitch"] for f in all_feats]
        cents = [f["spectral_centroid"] for f in all_feats]
        rhythms = [f["rhythmicity"] for f in all_feats]
        highs = [f["high_freq_ratio"] for f in all_feats]
        flats = [f["spectral_flatness"] for f in all_feats]
        rmss = [f["rms_energy"] for f in all_feats]
        
        print(f"{label:<28} ({len(all_feats)} files)")
        print(f"  Pitch:   {np.mean(pitches):>6.1f} +/- {np.std(pitches):>5.1f}  (range: {np.min(pitches):.0f} - {np.max(pitches):.0f})")
        print(f"  Cent:    {np.mean(cents):>6.1f} +/- {np.std(cents):>5.1f}  (range: {np.min(cents):.0f} - {np.max(cents):.0f})")
        print(f"  Rhythm:  {np.mean(rhythms):>6.2f} +/- {np.std(rhythms):>5.2f}  (range: {np.min(rhythms):.2f} - {np.max(rhythms):.2f})")
        print(f"  HighR:   {np.mean(highs):>6.3f} +/- {np.std(highs):>5.3f}  (range: {np.min(highs):.3f} - {np.max(highs):.3f})")
        print(f"  Flat:    {np.mean(flats):>6.3f} +/- {np.std(flats):>5.3f}  (range: {np.min(flats):.3f} - {np.max(flats):.3f})")
        print(f"  RMS:     {np.mean(rmss):>6.3f} +/- {np.std(rmss):>5.3f}  (range: {np.min(rmss):.3f} - {np.max(rmss):.3f})")
        print()
