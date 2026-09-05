import requests
import os
import shutil

categories = {
    "hungry": "hunger_cry_rhythmic.wav",
    "belly_pain": "pain_colic_screaming.wav",
    "discomfort": "discomfort_diaper_fuss.wav",
    "tired": "tired_whimper_yawn.wav",
    "burping": "belly_gas_grunts.wav"
}

headers = {'User-Agent': 'Mozilla/5.0'}

test_audio_dir = "test_audio"
public_samples_dir = "../frontend/public/samples"
os.makedirs(test_audio_dir, exist_ok=True)
os.makedirs(public_samples_dir, exist_ok=True)

print("=" * 80)
print("DOWNLOADING AUTHENTIC INFANT CRY AUDIO RECORDINGS (DONATE-A-CRY CORPUS)")
print("=" * 80)

for cat_folder, target_filename in categories.items():
    api_url = f"https://api.github.com/repos/gveres/donateacry-corpus/contents/donateacry_corpus_cleaned_and_updated_data/{cat_folder}"
    r = requests.get(api_url, headers=headers)
    if r.status_code == 200:
        files = r.json()
        # Find the first valid .wav file
        wav_files = [f for f in files if f['name'].endswith('.wav')]
        if wav_files:
            sample_file = wav_files[0]
            download_url = sample_file['download_url']
            print(f"Downloading real {cat_folder} cry from: {sample_file['name']}...")
            audio_resp = requests.get(download_url, headers=headers)
            
            dest_backend = os.path.join(test_audio_dir, target_filename)
            dest_frontend = os.path.join(public_samples_dir, target_filename)
            
            with open(dest_backend, 'wb') as f:
                f.write(audio_resp.content)
            with open(dest_frontend, 'wb') as f:
                f.write(audio_resp.content)
                
            print(f" Saved -> {dest_backend} ({len(audio_resp.content)} bytes)")
        else:
            print(f"No WAV found for {cat_folder}")
    else:
        print(f"Failed to fetch {cat_folder}: {r.status_code}")

print("=" * 80)
print("Finished downloading real baby crying audio files!")
