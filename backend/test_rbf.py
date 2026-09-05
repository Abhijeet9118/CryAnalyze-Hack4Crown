import numpy as np

# Calibrated Acoustic Reference Profiles (Universal ML Classifier)
PROFILES = {
    "Hunger": {
        "mean_pitch": 470.0, "std_pitch": 55.0,
        "spec_cent": 800.0, "std_cent": 350.0,
        "rhythm": 0.65, "std_rhythm": 0.25,
        "high_ratio": 0.20, "std_high": 0.15,
        "flatness": 0.10, "std_flatness": 0.25,
        "rms": 0.15, "std_rms": 0.10
    },
    "Pain / Colic": {
        "mean_pitch": 950.0, "std_pitch": 150.0,
        "spec_cent": 2800.0, "std_cent": 600.0,
        "rhythm": 0.35, "std_rhythm": 0.25,
        "high_ratio": 0.45, "std_high": 0.18,
        "flatness": 0.15, "std_flatness": 0.25,
        "rms": 0.30, "std_rms": 0.15
    },
    "Discomfort (Diaper/Temp)": {
        "mean_pitch": 340.0, "std_pitch": 35.0,
        "spec_cent": 600.0, "std_cent": 250.0,
        "rhythm": 0.15, "std_rhythm": 0.20,
        "high_ratio": 0.15, "std_high": 0.15,
        "flatness": 0.12, "std_flatness": 0.25,
        "rms": 0.12, "std_rms": 0.08
    },
    "Tiredness / Overstimulated": {
        "mean_pitch": 265.0, "std_pitch": 30.0,
        "spec_cent": 380.0, "std_cent": 180.0,
        "rhythm": 0.40, "std_rhythm": 0.25,
        "high_ratio": 0.06, "std_high": 0.10,
        "flatness": 0.08, "std_flatness": 0.25,
        "rms": 0.05, "std_rms": 0.05
    },
    "Belly Gas / Reflux": {
        "mean_pitch": 205.0, "std_pitch": 30.0,
        "spec_cent": 320.0, "std_cent": 160.0,
        "rhythm": 0.08, "std_rhythm": 0.15,
        "high_ratio": 0.04, "std_high": 0.10,
        "flatness": 0.08, "std_flatness": 0.25,
        "rms": 0.10, "std_rms": 0.08
    },
    "Normal / Cooing": {
        "mean_pitch": 420.0, "std_pitch": 100.0,
        "spec_cent": 650.0, "std_cent": 300.0,
        "rhythm": 0.06, "std_rhythm": 0.12,
        "high_ratio": 0.05, "std_high": 0.10,
        "flatness": 0.05, "std_flatness": 0.25,
        "rms": 0.015, "std_rms": 0.02
    }
}

def classify_rbf(feat):
    pitch = feat["mean_pitch"]
    rms = feat["rms_energy"]
    spec_cent = feat["spectral_centroid"]
    rhythm = feat["rhythmicity"]
    high_ratio = feat["high_freq_ratio"]
    flat = feat["spectral_flatness"]
    
    # 1. Silence / Quiet ambient baseline (<0.018 RMS)
    if rms < 0.018:
        probs = {k: 0.01 for k in PROFILES}
        probs["Normal / Cooing"] = 0.95
        return "Normal / Cooing", 0.95, probs

    # 2. Adult speaking voice (<160Hz without screaming strain)
    if pitch < 160 and spec_cent < 1500:
        probs = {k: 0.01 for k in PROFILES}
        probs["Normal / Cooing"] = 0.92
        probs["Belly Gas / Reflux"] = 0.05
        return "Normal / Cooing", 0.92, probs

    weights = {
        "pitch": 3.0,
        "spec_cent": 1.0,
        "rhythm": 1.2,
        "high_ratio": 1.0,
        "flatness": 0.5,
        "rms": 0.8
    }

    logits = {}
    for c_name, p in PROFILES.items():
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

        # Domain boundary penalties
        if c_name == "Pain / Colic":
            if pitch < 650 or spec_cent < 1600 or rms < 0.04:
                d2 += 50.0
        elif c_name == "Hunger":
            if pitch < 380 or pitch > 650:
                d2 += 30.0
        elif c_name == "Discomfort (Diaper/Temp)":
            if pitch < 275 or pitch > 420:
                d2 += 50.0
        elif c_name == "Tiredness / Overstimulated":
            if pitch < 220 or pitch > 320:
                d2 += 30.0
        elif c_name == "Belly Gas / Reflux":
            if pitch > 260:
                d2 += 40.0
        elif c_name == "Normal / Cooing":
            if rms > 0.08 or pitch > 600:
                d2 += 30.0
        
        logits[c_name] = -0.5 * (d2 / 2.0)

    # Softmax
    max_l = max(logits.values())
    exp_l = {k: np.exp(v - max_l) for k, v in logits.items()}
    sum_exp = sum(exp_l.values())
    probs = {k: round(float(v / sum_exp), 3) for k, v in exp_l.items()}
    
    top_label = max(probs, key=probs.get)
    return top_label, probs[top_label], probs
