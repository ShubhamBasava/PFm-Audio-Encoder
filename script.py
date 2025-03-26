import json
import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1, TALB, COMM, TRCK, APIC, ID3NoHeaderError
from mutagen.mp3 import MP3

# Function to sanitize file names
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).strip()

# Read the chapters JSON file
with open("chapters.json", "r", encoding="utf8") as f:
    chapters = json.load(f)

# Validate chapters JSON
if not isinstance(chapters, list) or not all(isinstance(chapter, str) for chapter in chapters):
    raise ValueError("chapters.json must be a list of strings")

start = 0
end = min(850, len(chapters))  # Prevent index errors
input_path = "./source"
output_path = "./Output"
cover_photo_path = "image.jpg"
title = "Ruthless Rick"
short_title = "".join(word[0] for word in title.split())  # Extract first letter of each word (GA)
encoded_by = "@AudioVerseNetwork(Telegram)"
copyright = "POCKETFM PVT LTD"

# Load cover photo
try:
    with open(cover_photo_path, "rb") as f:
        cover_photo = f.read()
except FileNotFoundError:
    print("Cover image not found. Proceeding without it.")
    cover_photo = None

# Validate missing titles
missing_titles = [i + 1 for i, chapter in enumerate(chapters) if chapter == "!Missing Title!"]
if missing_titles:
    raise Exception(f"Missing titles for chapters: {', '.join(map(str, missing_titles))}")

for i in range(start, end):
    episode_title = chapters[i].strip()  # Use exact title from chapters.json
    original_file_name = f"{i + 1}.mp3"
    original_file_path = os.path.join(input_path, original_file_name)
    
    if not os.path.isfile(original_file_path):
        print(f"Skipping: File not found -> {original_file_name}")
        continue

    # Ensure episode title does not already contain "EP" or "EPS"
    if re.search(r"\bEP\b|\bEPS\b", episode_title, re.IGNORECASE):
        formatted_title = f"{short_title} {episode_title} by {encoded_by}"
    else:
        formatted_title = f"{short_title} EP {i+1} by {encoded_by}"

    # Sanitize filename to prevent illegal characters
    new_file_name = sanitize_filename(formatted_title) + ".mp3"
    new_file_path = os.path.join(output_path, new_file_name)

    try:
        shutil.copyfile(original_file_path, new_file_path)
    except Exception as error:
        print(f"Error copying {original_file_name}: {error}")
        continue

    # Metadata Tags
    tags = {
        "TIT2": TIT2(encoding=3, text=episode_title),  # Use title directly from chapters.json
        "TPE1": TPE1(encoding=3, text=encoded_by),
        "TALB": TALB(encoding=3, text=title),
        "COMM": COMM(encoding=3, lang="eng", desc="Comment", text=copyright),
        "TRCK": TRCK(encoding=3, text=str(i + 1)),
    }

    if cover_photo:
        tags["APIC"] = APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover_photo)

    # Apply ID3 tags
    try:
        audio = MP3(new_file_path, ID3=ID3)
    except ID3NoHeaderError:
        audio = MP3(new_file_path)
        audio.add_tags()
    
    for key, value in tags.items():
        try:
            audio.tags.add(value)
        except Exception as tag_error:
            print(f"Error adding {key} tag for {new_file_name}: {tag_error}")

    audio.save()
    print(f"Processed: {new_file_name}")
