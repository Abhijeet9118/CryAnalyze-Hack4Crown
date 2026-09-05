import numpy as np
from scipy.io.wavfile import write
import os

# Create a folder for the test audio files
output_dir = "test_audio"
os.makedirs(output_dir, exist_ok=True)

sample_rate = 16000  # 16kHz is standard for audio ML
duration = 4         # 4 seconds long

time = np.linspace(0, duration, int(sample_rate * duration))

# 1. Mock "Hungry Cry" (Lower pitch, rhythmic wailing)
# Base tone 440Hz, modulated by a 1.5Hz envelope to sound like rhythmic crying
hungry_wave = np.sin(2 * np.pi * 440 * time) * (0.5 * (1 + np.sin(2 * np.pi * 1.5 * time)))
hungry_wave = np.int16(hungry_wave * 32767) # Convert to 16-bit PCM format
write(os.path.join(output_dir, "mock_hungry_cry.wav"), sample_rate, hungry_wave)

# 2. Mock "Pain Cry" (High pitch, sharp, continuous)
# Base tone 900Hz, louder and more constant
pain_wave = np.sin(2 * np.pi * 900 * time) * 0.9
pain_wave = np.int16(pain_wave * 32767)
write(os.path.join(output_dir, "mock_pain_cry.wav"), sample_rate, pain_wave)

# 3. Mock "Discomfort/Fussing" (White noise mixed with low pitch)
# Simulates shuffling and grunting
noise = np.random.normal(0, 0.3, len(time))
fuss_wave = (np.sin(2 * np.pi * 200 * time) * 0.4) + noise
fuss_wave = np.clip(fuss_wave, -1.0, 1.0) # Prevent clipping
fuss_wave = np.int16(fuss_wave * 32767)
write(os.path.join(output_dir, "mock_discomfort_fuss.wav"), sample_rate, fuss_wave)

print("Test audio files generated successfully in the 'test_audio' folder!")
