from datasets import load_dataset
import soundfile as sf
import pandas as pd
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hours', type=float, default=None,
                       help='Number of hours to process (optional)')
    return parser.parse_args()

# Load the dataset
dataset = load_dataset("Cossale/gujarati-interspeech", split="train")

args = parse_arguments()

# Create directory structure
base_dir = "train"
wav_dir = os.path.join(base_dir, "wavs")  # Changed to wavs
os.makedirs(wav_dir, exist_ok=True)

metadata = []
total_duration = 0
target_duration = args.hours * 3600 if args.hours else float('inf')  # Convert hours to seconds

# First pass to calculate cumulative durations
cumulative_durations = []
for example in dataset:
    audio_data = example["audio"]["array"]
    sampling_rate = example["audio"]["sampling_rate"]
    duration = len(audio_data) / sampling_rate
    total_duration += duration
    cumulative_durations.append(total_duration)

# Find the index where we reach the target duration
if args.hours:
    # Find the largest index where cumulative duration is less than or equal to target
    for idx, cum_duration in enumerate(cumulative_durations):
        if cum_duration > target_duration:
            process_until_idx = idx
            break
    else:
        process_until_idx = len(dataset)
else:
    process_until_idx = len(dataset)

# Reset total duration for actual processing
total_duration = 0

# Process the dataset
for i, example in enumerate(dataset):
    if i >= process_until_idx:
        break
        
    # Get audio data
    audio_data = example["audio"]["array"]
    sampling_rate = example["audio"]["sampling_rate"]
    
    # Calculate duration from array length and sampling rate
    duration = len(audio_data) / sampling_rate  # Duration in seconds
    
    # Add to total duration
    total_duration += duration

    # Create filename in the required format: aud-XXXXX-YYYY.wav
    file_id = f"aud-{i:05d}-0001.wav"
    filepath = os.path.join(wav_dir, file_id)

    # Save audio as WAV file
    sf.write(filepath, audio_data, sampling_rate)

    # Create metadata row with pipe delimiter
    # file_id without .wav extension | text
    row = {
        'file_id': file_id[:-4],  # Remove .wav extension
        'text': example["text"]
    }
    metadata.append(row)

# Create metadata.csv with pipe delimiter
df = pd.DataFrame(metadata)
metadata_path = os.path.join(base_dir, "metadata.csv")

# Save with pipe delimiter, no index, and proper encoding for Gujarati text
df.to_csv(metadata_path, 
          sep='|', 
          index=False, 
          encoding='utf-8',
          header=False)

# Calculate hours, minutes, and seconds
hours = total_duration // 3600
minutes = (total_duration % 3600) // 60
seconds = total_duration % 60

print(f"\nDataset Statistics:")
print(f"Total number of audio files: {len(metadata)}")
print(f"Total duration: {hours:.2f} hours ({total_duration:.2f} seconds)")
print(f"Total duration: {int(hours)}:{int(minutes):02d}:{int(seconds):02d} (HH:MM:SS)")

print(f"\nCreated directory structure:")
print(f"train/")
print(f"├── metadata.csv")
print(f"└── wavs/")  # Changed to wavs
print(f"    └── {len(metadata)} wav files")