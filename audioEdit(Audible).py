import os
import json
import sys
import shutil
import tqdm
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK, TCON, COMM, TCOP, TPUB, TENC, APIC

def check_required_files(base_path):
    """Check for required files and warn about missing ones."""
    required_files = ["chapters.json", "image.jpg"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(base_path, f))]
    
    if missing_files:
        print(f"Warning: Missing required files - {', '.join(missing_files)}. Continuing without them.")

def load_chapter_titles(json_path):
    """Load chapter titles from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error: Invalid or missing chapters.json. Using default episode numbering.")
        return []

def process_audio_files(base_path, album_name, start_eps, end_eps):
    """Process and rename audio files with metadata tagging."""
    source_dir = os.path.join(base_path, "source")
    output_dir = os.path.join(base_path, "Output")
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(base_path, "chapters.json")
    image_path = os.path.join(base_path, "image.jpg")
    titles = load_chapter_titles(json_path)

    album_prefix = "".join([word[0].upper() for word in album_name.split()])
    artist = "@AudioVerseNetwork(Telegram)"
    
    total_files = end_eps - start_eps + 1
    processed_files = 0
    image_data = None
    
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            image_data = img.read()
    else:
        print("Warning: Cover image not found. Files will be processed without cover art.")

    for eps in tqdm.tqdm(range(start_eps, end_eps + 1), desc="Processing Files", unit="file"):
        title = titles[eps - 1] if eps - 1 < len(titles) else f"Episode {eps}"
        input_file = os.path.join(source_dir, f"{eps}.mp3")
        output_file = os.path.join(output_dir, f"{album_prefix} EPs {eps} by {artist}.mp3")

        if not os.path.exists(input_file):
            print(f"Skipping {eps}.mp3 - File not found")
            continue

        audio = MP3(input_file, ID3=ID3)

        if audio.tags is None:
            audio.tags = ID3()

        # Add metadata
        audio.tags["TIT2"] = TIT2(encoding=3, text=title)
        audio.tags["TALB"] = TALB(encoding=3, text=album_name)
        audio.tags["TPE1"] = TPE1(encoding=3, text=artist)
        audio.tags["TRCK"] = TRCK(encoding=3, text=str(eps))  
        audio.tags["TCON"] = TCON(encoding=3, text="Audiobook")  
        audio.tags["COMM"] = COMM(encoding=3, lang='eng', desc='Comment', text="Uploaded by @AudioVerseNetwork(Telegram)")  
        audio.tags["TCOP"] = TCOP(encoding=3, text="Aethon Audio")  
        audio.tags["TPUB"] = TPUB(encoding=3, text="Aethon Audio")  
        audio.tags["TENC"] = TENC(encoding=3, text="@AudioVerseNetwork(Telegram)")  

        if image_data:
            audio.tags["APIC"] = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=image_data)

        audio.save()
        shutil.copy(input_file, output_file)
        processed_files += 1
        percentage = (processed_files / total_files) * 100
        print(f"Processed: {output_file} ({percentage:.2f}%)")

if __name__ == "__main__":
    base_path = r"D:\\Telegram\\PFM Eps Rename\\New_Encoder"
    check_required_files(base_path)

    album_name = input("Enter album name: ").strip()
    start_eps = int(input("Enter start episode number: "))
    end_eps = int(input("Enter end episode number: "))

    if start_eps > end_eps:
        print("Error: Start episode number must be less than or equal to end episode number.")
        sys.exit(1)

    process_audio_files(base_path, album_name, start_eps, end_eps)
