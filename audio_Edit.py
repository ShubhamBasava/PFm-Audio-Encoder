import os
import json
import shutil
import re
import sys
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, APIC, TENC, TCOP
from mutagen.mp3 import MP3, HeaderNotFoundError

# Function to clean chapter titles
def clean_chapter_title(title):
    cleaned_title = re.sub(r'\b(?:Ep|Ch|CP|Cp|EP|Ep|CH|Ch)-?\d*-*\s*', '', title).strip()
    return cleaned_title

# Get user input for title, start, and end episodes
title = sys.argv[1]
start = int(sys.argv[2]) - 1
end = int(sys.argv[3])

# Initialize chapters variable
chapters = []

# Check if chapters.json exists
if os.path.exists("chapters.json"):
    with open("chapters.json", "r", encoding="utf-8") as file:
        chapters = json.load(file)
    end = min(end, len(chapters))  # Ensure we don't go out of bounds
else:
    print("chapters.json file not found. Skipping chapter processing.")
    chapters = None  # No chapters to process

input_path = "./source"
output_path = "./Output"
cover_photo_path = "./cover.png"
author = "@AudioVerseNetwork(Telegram)"
contributing_artist = "@AudioVerseNetwork(Telegram)"
encoded_by = "PFM_Daily(Telegram)"
copyright = "Pocket FM Private Limited"

# Check if cover photo exists
if os.path.exists(cover_photo_path):
    with open(cover_photo_path, "rb") as file:
        cover_photo = file.read()
else:
    print("Cover photo not found. Skipping adding cover to MP3 files.")
    cover_photo = None

# Check for missing titles if chapters exist
if chapters:
    missing_titles = [i + 1 for i, chapter in enumerate(chapters) if chapter == "!Missing Title!"]
    if missing_titles:
        print(f"Missing titles for chapters: {', '.join(map(str, missing_titles))}")
        raise ValueError(f"Missing titles for chapters: {', '.join(map(str, missing_titles))}")

    print("Note: Check For Any Missing Episodes")

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

def add_id3_tags(file_path, chapter_num, chapter_name):
    try:
        audio = MP3(file_path, ID3=ID3)
    except HeaderNotFoundError:
        print(f"Error: {file_path} is not a valid MP3 file.")
        return False
    except Exception as e:
        print(f"Error loading MP3 file {file_path}: {e}")
        return False

    if audio.tags is None:
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=f"EP {chapter_num} - {chapter_name}"))
    audio.tags.add(TALB(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=author))  # Author without URL
    audio.tags.add(TPE2(encoding=3, text=contributing_artist))  # Contributing artist
    audio.tags.add(TRCK(encoding=3, text=f"{chapter_num}/{len(chapters) if chapters else 'Unknown'}"))
    audio.tags.add(TENC(encoding=3, text=encoded_by))
    audio.tags.add(TCOP(encoding=3, text=copyright))

    if cover_photo:
        audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_photo))

    audio.save()
    return True

def abbreviate(text):
    return ''.join(word[0] for word in text.split() if word).upper()

missing_files = []
corrupt_files = []
total_files = end - start

for count, i in enumerate(range(start, end), start=1):
    if chapters:
        chapter = chapters[i].replace("?", "")
        cleaned_chapter = clean_chapter_title(chapter)
    else:
        cleaned_chapter = "Unknown Chapter"

    original_file_name = f"{i + 1}.mp3"
    original_file_path = os.path.join(input_path, original_file_name)
    
    print(f"Processing file: {original_file_name}")
    
    if not os.path.isfile(original_file_path):
        missing_files.append(original_file_name)
        print(f"File not found: {original_file_name}")
        continue
    
    abbreviated_title = abbreviate(title)
    new_file_name = f"{abbreviated_title}_EP{i + 1}_ENCODED_{encoded_by}.mp3"
    new_file_path = os.path.join(output_path, new_file_name)

    print(f"Copying file to: {new_file_path}")

    try:
        shutil.copyfile(original_file_path, new_file_path)
    except Exception as error:
        print(f"Error copying file {original_file_name} to {new_file_name}: {error}")
        continue
    
    print(f"Adding ID3 tags to: {new_file_name}")
    if not add_id3_tags(new_file_path, i + 1, cleaned_chapter):
        corrupt_files.append(original_file_name)
    
    # Display progress
    progress = (count / total_files) * 100
    print(f"Progress: {progress:.2f}%")

if missing_files:
    print(f"Missing audio files: {', '.join(missing_files)}")

if corrupt_files:
    print(f"Corrupt audio files: {', '.join(corrupt_files)}")

print("All files have been processed successfully.")
