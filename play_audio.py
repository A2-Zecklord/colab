# Second Cell - Audio Player
import glob
import os
from datetime import datetime
from IPython.display import Audio, display

def play_latest_audio():
    # Find all .wav files in the output directory and its subdirectories
    wav_files = []
    for voice_data in TextToSpeech().voice_config.values():
        output_dir = voice_data['output_dir']
        wav_files.extend(glob.glob(f"{output_dir}/**/*.wav", recursive=True))
    
    if not wav_files:
        print("No audio files found")
        return
    
    # Get the most recent file based on directory timestamp
    latest_file = max(wav_files, key=lambda x: os.path.getctime(x))
    
    print(f"Playing most recent audio file: {latest_file}")
    print(f"Created at: {datetime.fromtimestamp(os.path.getctime(latest_file))}")
    
    # Display audio player
    display(Audio(latest_file))

# Call the function to play the latest audio
play_latest_audio()