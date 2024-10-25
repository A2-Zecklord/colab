# First Cell - Text to Speech Generator
import subprocess
import os
from datetime import datetime
import json

class TextToSpeech:
    def __init__(self):
        # Load voice configurations
        with open('voice_config.json', 'r') as f:
            self.voice_config = json.load(f)

    def list_available_voices(self):
        """Display available voices"""
        print("Available voices:")
        for i, voice in enumerate(self.voice_config.keys(), 1):
            print(f"{i}. {voice}")

    def generate_speech(self, voice, input_text=None, input_file=None):
        """Generate speech from text input or file"""
        if not voice in self.voice_config:
            raise ValueError(f"Invalid voice selection. Available voices: {', '.join(self.voice_config.keys())}")
        
        if not input_text and not input_file:
            raise ValueError("Either input_text or input_file must be provided")

        voice_data = self.voice_config[voice]
        sample = voice_data['sample']
        output_dir = voice_data['output_dir']
        sample_text = voice_data['sample_text']

        # Create a unique subdirectory using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_subdir = f"{output_dir}/{timestamp}"
        os.makedirs(output_subdir, exist_ok=True)

        command = [
            'python',
            'inference-cli.py',
            '-m', 'F5-TTS',
            '-r', sample,
            '-s', sample_text,
            '-o', output_subdir,
        ]

        if input_file:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
            command.extend(['-f', input_file])
        else:
            command.extend(['-t', input_text])

        output_file = f"{output_subdir}/out.wav"
        
        try:
            print("Generating speech...")
            subprocess.run(command, check=True)
            if os.path.exists(output_file):
                print(f"Speech generated successfully! Output file: {output_file}")
                return output_file
            else:
                raise FileNotFoundError(f"Audio file not found at {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate speech: {str(e)}")
            raise

def main():
    tts = TextToSpeech()
    
    # Display available voices
    tts.list_available_voices()
    
    # Get voice selection from user
    voice = input("\nEnter voice name: ")
    
    # Get input method from user
    print("\nSelect input method:")
    print("1. Text input")
    print("2. File input")
    input_method = input("Enter choice (1 or 2): ")
    
    try:
        if input_method == "1":
            text = input("Enter the text to convert: ")
            output_file = tts.generate_speech(voice, input_text=text)
        elif input_method == "2":
            file_path = input("Enter the path to text file: ")
            output_file = tts.generate_speech(voice, input_file=file_path)
        else:
            print("Invalid input method selection")
            return
        
        print(f"\nGeneration complete! Audio saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()