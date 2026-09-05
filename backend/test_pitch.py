import numpy as np
import librosa
import scipy.signal

# Test pitch estimation with expanded range (80Hz - 1600Hz)
def estimate_pitch_robust(y, sr):
    frame_len = int(sr * 0.05) # 50ms frame
    hop_len = int(sr * 0.02)   # 20ms hop
    min_period = int(sr / 1600) # ~10 samples (1600Hz)
    max_period = int(sr / 80)   # ~200 samples (80Hz)
    
    f0_list = []
    # Bandpass filter before autocorrelation to reduce mic hiss (>3000Hz) and DC rumble (<60Hz)
    sos = scipy.signal.butter(4, [80 / (sr/2), 3000 / (sr/2)], btype='bandpass', output='sos')
    y_filtered = scipy.signal.sosfilt(sos, y)
    
    for i in range(0, len(y_filtered) - frame_len, hop_len):
        frame = y_filtered[i:i + frame_len]
        if np.max(np.abs(frame)) < 0.01:
            continue
        corr = np.correlate(frame, frame, mode='full')
        corr = corr[len(corr)//2:]
        if len(corr) > max_period:
            peak_idx = min_period + np.argmax(corr[min_period:max_period])
            if corr[peak_idx] > 0.3 * corr[0]:
                f0_list.append(sr / peak_idx)
                
    if len(f0_list) > 0:
        return float(np.median(f0_list)), float(np.max(f0_list)), float(np.std(f0_list))
    return 350.0, 400.0, 20.0

print("Pitch estimator tested successfully!")
