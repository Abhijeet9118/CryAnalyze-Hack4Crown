import numpy as np
from scipy.io.wavfile import write
import scipy.signal
import os

def generate_samples(base_dirs=["test_audio", "../frontend/public/samples"]):
    for base_dir in base_dirs:
        os.makedirs(base_dir, exist_ok=True)
    
    sample_rate = 16000
    duration = 5.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    samples = {}
    
    def lowpass(data, cutoff=1200):
        b, a = scipy.signal.butter(4, cutoff / (sample_rate / 2), btype='low')
        return scipy.signal.lfilter(b, a, data)
    
    # 1. Hunger Cry (Rhythmic 480Hz fundamental, 1.2Hz burst envelope)
    env = 0.5 * (1.0 + np.sin(2 * np.pi * 1.2 * t - np.pi/2))
    h_tone = (
        0.55 * np.sin(2 * np.pi * 480 * t) +
        0.25 * np.sin(2 * np.pi * 960 * t)
    ) * (env ** 1.5)
    noise_h = lowpass(np.random.normal(0, 0.02, len(t)), cutoff=800)
    samples["hunger_cry_rhythmic.wav"] = np.clip(h_tone + noise_h, -1.0, 1.0)
    
    # 2. Pain / Colic Cry (High-pitch 880Hz scream with 1760Hz harmonics, intense continuous strain)
    pain_f = 880 + 60 * np.sin(2 * np.pi * 3.5 * t)
    p_tone = (
        0.7 * np.sin(2 * np.pi * pain_f * t) +
        0.5 * np.sin(2 * np.pi * pain_f * 2 * t) +
        0.3 * np.sin(2 * np.pi * pain_f * 3 * t)
    )
    p_env = 0.85 + 0.15 * np.sin(2 * np.pi * 0.8 * t)
    p_noise = np.random.normal(0, 0.08, len(t))
    samples["pain_colic_screaming.wav"] = np.clip((p_tone * p_env) + p_noise, -1.0, 1.0)
    
    # 3. Discomfort / Diaper (340Hz irregular whiny bursts with pauses)
    disc_env = np.where(np.sin(2 * np.pi * 0.5 * t) > 0.1, 0.6, 0.05)
    d_tone = (
        0.6 * np.sin(2 * np.pi * 340 * t) +
        0.2 * np.sin(2 * np.pi * 680 * t)
    ) * disc_env
    d_noise = lowpass(np.random.normal(0, 0.02, len(t)), cutoff=700) * disc_env
    samples["discomfort_diaper_fuss.wav"] = np.clip(d_tone + d_noise, -1.0, 1.0)
    
    # 4. Tiredness / Sleepy Whimper (340Hz descending glide, slow sighing pauses)
    t_mod = t % 1.5
    sweep_freq = 340 - (40 * (t_mod / 1.5))
    tired_env = 0.35 * (1.0 - (t_mod / 1.5)) ** 1.5
    t_tone = 0.5 * np.sin(2 * np.pi * sweep_freq * t) * tired_env
    t_noise = lowpass(np.random.normal(0, 0.005, len(t)), cutoff=500)
    samples["tired_whimper_yawn.wav"] = np.clip(t_tone + t_noise, -1.0, 1.0)
    
    # 5. Belly Gas / Reflux (Low 210Hz guttural grunt pressure, short bursts)
    gas_pulse = np.maximum(0, np.sin(2 * np.pi * 0.5 * t)) ** 5
    g_tone = (
        0.7 * np.sin(2 * np.pi * 210 * t) +
        0.2 * np.sin(2 * np.pi * 420 * t)
    ) * gas_pulse
    g_noise = lowpass(np.random.normal(0, 0.03, len(t)), cutoff=400) * gas_pulse
    samples["belly_gas_grunts.wav"] = np.clip(g_tone + g_noise, -1.0, 1.0)
    
    # 6. Normal Cooing / Safe (Soft 380Hz melodic chirps, very gentle)
    coo_f = 370 + 30 * np.sin(2 * np.pi * 0.4 * t)
    coo_env = np.maximum(0, np.sin(2 * np.pi * 0.5 * t)) ** 4
    c_tone = 0.08 * np.sin(2 * np.pi * coo_f * t) * coo_env
    c_noise = lowpass(np.random.normal(0, 0.001, len(t)), cutoff=400)
    samples["baby_cooing_safe.wav"] = np.clip(c_tone + c_noise, -1.0, 1.0)
    
    # Write files
    for filename, wave_data in samples.items():
        pcm_data = np.int16(wave_data * 32767)
        for base_dir in base_dirs:
            out_path = os.path.join(base_dir, filename)
            write(out_path, sample_rate, pcm_data)

if __name__ == "__main__":
    generate_samples()
    print("Samples refreshed!")
