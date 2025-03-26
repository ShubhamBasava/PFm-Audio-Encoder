from pydub import AudioSegment
import os

def convertm4btomp3(sourcefolder, outputfolder):
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    
    for filename in os.listdir(sourcefolder):
        if filename.endswith(".m4b"):
            m4bpath = os.path.join(sourcefolder, filename)
            mp3filename = filename.replace(".m4b", ".mp3")
            mp3path = os.path.join(outputfolder, mp3filename)
            
            # Load m4b file
            audio = AudioSegment.fromfile(m4bpath, format="m4b")
            
            # Export as mp3
            audio.export(mp3path, format="mp3")
            print(f"Converted {filename} to {mp3filename}")

# Usage example
sourcefolder = "D:\Telegram\PFM Eps Rename\NewEncoder\source"
outputfolder = "D:\Telegram\PFM Eps Rename\NewEncoder\Output"
convertm4btomp3(sourcefolder, outputfolder)
