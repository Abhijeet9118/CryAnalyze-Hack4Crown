import librosa
from ml_pipeline import extract_acoustic_features
import test_rbf

y, sr = librosa.load('test_audio/belly_gas_grunts.wav', sr=16000)
feat = extract_acoustic_features(y, sr)

weights = {
    "pitch": 3.0,
    "spec_cent": 1.2,
    "rhythm": 1.5,
    "high_ratio": 1.2,
    "flatness": 0.8,
    "rms": 1.0
}

pitch = feat["mean_pitch"]
rms = feat["rms_energy"]
spec_cent = feat["spectral_centroid"]
rhythm = feat["rhythmicity"]
high_ratio = feat["high_freq_ratio"]
flat = feat["spectral_flatness"]

print("Pitch:", pitch, "RMS:", rms, "Cent:", spec_cent)
for c_name, p in test_rbf.PROFILES.items():
    z_pitch = (pitch - p["mean_pitch"]) / p["std_pitch"]
    z_cent = (spec_cent - p["spec_cent"]) / p["std_cent"]
    z_rhythm = (rhythm - p["rhythm"]) / p["std_rhythm"]
    z_high = (high_ratio - p["high_ratio"]) / p["std_high"]
    z_flat = (flat - p["flatness"]) / p["std_flatness"]
    z_rms = (rms - p["rms"]) / p["std_rms"]
    
    d2 = (
        weights["pitch"] * (z_pitch ** 2) +
        weights["spec_cent"] * (z_cent ** 2) +
        weights["rhythm"] * (z_rhythm ** 2) +
        weights["high_ratio"] * (z_high ** 2) +
        weights["flatness"] * (z_flat ** 2) +
        weights["rms"] * (z_rms ** 2)
    )
    print(f"Class: {c_name:<28} | Raw d2: {d2:.2f}")
