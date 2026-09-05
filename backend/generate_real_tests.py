import numpy as np
from scipy.io.wavfile import write
import os

# Create mock test cases
sr = 16000
duration = 4.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Adult male talking (120Hz fundamental with voice harmonics)
adult_voice = (0.6 * np.sin(2 * np.pi * 120 * t) + 0.3 * np.sin(2 * np.pi * 240 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 1.5 * t))
write("test_audio/test_adult_voice.wav", sr, np.int16(adult_voice * 32767))

# Room ambient fan hiss (low volume white noise)
room_hiss = np.random.normal(0, 0.008, len(t))
write("test_audio/test_room_hiss.wav", sr, np.int16(room_hiss * 32767))

print("Created test adult voice and room hiss wav files.")
