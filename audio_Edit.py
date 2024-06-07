import os
import json
import shutil
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, APIC, TENC, TCOP
from mutagen.mp3 import MP3

# Read the chapters file
with open("chapters.json", "r", encoding="utf-8") as file:
    chapters = json.load(file)

start = 0
end = min(821, len(chapters))  # Ensure we don't go out of bounds
input_path = "./source"
output_path = "./Output"
cover_photo_path = "./cover.jpg"
title = "Games of Leo The All-Out System"
author = "@PocketFmEnglish2"
contributing_artist = "@PFM_Daily(Telegram)"
encoded_by = "PFM_Daily"
copyright = "POCKETFM PVT LTD"

# Read the cover photo
with open(cover_photo_path, "rb") as file:
    cover_photo = file.read()

missing_titles = [i + 1 for i, chapter in enumerate(chapters) if chapter == "!Missing Title!"]
if missing_titles:
    print(f"Missing titles for chapters: {', '.join(map(str, missing_titles))}")
    raise ValueError(f"Missing titles for chapters: {', '.join(map(str, missing_titles))}")

print("Note:- Check For Any Missing Episodes")

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

def add_id3_tags(file_path, chapter_num, chapter_name):
    audio = MP3(file_path, ID3=ID3)
    if audio.tags is None:
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=f"Ep. {chapter_num} - {chapter_name}"))
    audio.tags.add(TALB(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=author))  # Author
    audio.tags.add(TPE2(encoding=3, text=contributing_artist))  # Contributing artist
    audio.tags.add(TRCK(encoding=3, text=f"{chapter_num}/{len(chapters)}"))
    audio.tags.add(TENC(encoding=3, text=encoded_by))
    audio.tags.add(TCOP(encoding=3, text=copyright))
    audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_photo))

    audio.save()

missing_files = []

for i in range(start, end):
    chapter = chapters[i].replace("?", "")
    original_file_name = f"{i + 1}.mp3"
    original_file_path = os.path.join(input_path, original_file_name)
    
    if not os.path.isfile(original_file_path):
        missing_files.append(original_file_name)
        continue
    
    # Clean up chapter names by removing unwanted substrings
    clean_chapter = chapter.replace("", "").replace("", "").strip()
    new_file_name = f"{title} Ep.{i + 1} - {clean_chapter} Encoded -{contributing_artist}.mp3"
    new_file_path = os.path.join(output_path, new_file_name)

    try:
        shutil.copyfile(original_file_path, new_file_path)
    except Exception as error:
        print(error)
    
    add_id3_tags(new_file_path, i + 1, clean_chapter)

if missing_files:
    print(f"Missing audio files: {', '.join(missing_files)}")

print("All files have been renamed successfully.")
