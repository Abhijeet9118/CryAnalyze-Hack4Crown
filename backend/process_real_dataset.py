import os
import shutil
import librosa
import soundfile as sf

base_dir = 'temp_dataset/donateacry_corpus_cleaned_and_updated_data'
target_audio_dir = 'test_audio'
public_samples_dir = '../frontend/public/samples'
real_library_dir = 'test_audio/real_dataset'

os.makedirs(target_audio_dir, exist_ok=True)
os.makedirs(public_samples_dir, exist_ok=True)
os.makedirs(real_library_dir, exist_ok=True)

# Mapping of dataset categories to our prototype targets
mapping = {
    "hungry": "hunger_cry_rhythmic.wav",
    "belly_pain": "pain_colic_screaming.wav",
    "discomfort": "discomfort_diaper_fuss.wav",
    "tired": "tired_whimper_yawn.wav",
    "burping": "belly_gas_grunts.wav"
}

print("=" * 80)
print("EXTRACTING REAL INFANT CRY RECORDINGS INTO PROTOTYPE")
print("=" * 80)

for cat, target_name in mapping.items():
    cat_dir = os.path.join(base_dir, cat)
    if os.path.exists(cat_dir):
        files = [f for f in os.listdir(cat_dir) if f.endswith('.wav')]
        print(f"Found {len(files)} authentic recordings in '{cat}' category.")
        if files:
            # Pick a clear file with good duration (>4 seconds)
            selected_file = None
            for f in files:
                f_path = os.path.join(cat_dir, f)
                try:
                    y, sr = librosa.load(f_path, sr=16000, duration=8.0)
                    if len(y) > 16000 * 3.0: # At least 3 seconds
                        selected_file = f_path
                        break
                except Exception:
                    continue
            
            if not selected_file:
                selected_file = os.path.join(cat_dir, files[0])
            
            # Load and normalize
            y, sr = librosa.load(selected_file, sr=16000)
            
            # Write to test_audio and public/samples
            dest_backend = os.path.join(target_audio_dir, target_name)
            dest_frontend = os.path.join(public_samples_dir, target_name)
            
            sf.write(dest_backend, y, sr)
            sf.write(dest_frontend, y, sr)
            print(f"  -> Extracted '{os.path.basename(selected_file)}' -> {target_name} ({len(y)/sr:.2f}s)")
            
            # Also save 3 extra real clips for user exploration
            cat_lib_dir = os.path.join(real_library_dir, cat)
            os.makedirs(cat_lib_dir, exist_ok=True)
            for idx, extra_f in enumerate(files[:5]):
                src = os.path.join(cat_dir, extra_f)
                dst = os.path.join(cat_lib_dir, f"{cat}_sample_{idx+1}.wav")
                shutil.copy2(src, dst)

print("=" * 80)
print("All authentic infant cry recordings extracted and ready!")
