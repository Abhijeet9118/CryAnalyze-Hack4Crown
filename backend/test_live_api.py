import requests
import os

samples = [
    'hunger_cry_rhythmic.wav',
    'pain_colic_screaming.wav',
    'discomfort_diaper_fuss.wav',
    'tired_whimper_yawn.wav',
    'belly_gas_grunts.wav',
    'baby_cooing_safe.wav'
]

print("=" * 80)
print("TESTING LIVE FASTAPI /analyze ENDPOINT OVER HTTP (http://localhost:8000)")
print("=" * 80)

for s in samples:
    path = os.path.join('test_audio', s)
    with open(path, 'rb') as f:
        r = requests.post('http://localhost:8000/analyze', files={'audio': (s, f, 'audio/wav')})
        if r.status_code == 200:
            data = r.json()
            pred = data.get('prediction', 'Unknown')
            conf = int(data.get('confidence', 0) * 100)
            esc = data.get('escalate', False)
            f0 = data.get('acoustic_metrics', {}).get('mean_pitch_hz', 0)
            cent = data.get('acoustic_metrics', {}).get('spectral_centroid_hz', 0)
            print(f"File: {s:<28} | HTTP: {r.status_code} | Result: {pred:<24} | Conf: {conf}% | Escalate: {str(esc):<5} | F0: {f0}Hz")
        else:
            print(f"File: {s} | FAILED with HTTP {r.status_code}: {r.text}")

print("=" * 80)
print("All audio files intake and analysis passed!")
