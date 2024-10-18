from pydub import AudioSegment
import os

def convert_m4b_to_mp3(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(source_folder):
        if filename.endswith(".m4b"):
            m4b_path = os.path.join(source_folder, filename)
            mp3_filename = filename.replace(".m4b", ".mp3")
            mp3_path = os.path.join(output_folder, mp3_filename)
            
            # Load m4b file
            audio = AudioSegment.from_file(m4b_path, format="m4b")
            
            # Export as mp3
            audio.export(mp3_path, format="mp3")
            print(f"Converted {filename} to {mp3_filename}")

# Usage example
source_folder = "D:\Telegram\PFM Eps Rename\New_Encoder\source"
output_folder = "D:\Telegram\PFM Eps Rename\New_Encoder\Output"
convert_m4b_to_mp3(source_folder, output_folder)
