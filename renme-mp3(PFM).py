import os
import re

def extract_number(filename: str, exclude_words=None):
    """
    Extracts the first number found in a filename.
    Optionally removes specified words before extracting.
    """
    if exclude_words:
        for word in exclude_words:
            filename = re.sub(rf'\b{word}\b', '', filename, flags=re.IGNORECASE)
    
    numbers = re.findall(r'\d+', filename)
    return numbers[0] if numbers else None

def rename_mp3_files(directory: str, exclude_words=None):
    """Renames all .mp3 files in the given directory based on extracted numbers."""
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mp3"):
            number = extract_number(filename, exclude_words)
            if number:
                new_filename = f"{number}.mp3"
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                else:
                    print(f"Skipped: {filename} (already named correctly)")
            else:
                print(f"Skipped: {filename} (no number found)")

# Usage
directory_path = r"D:\\Telegram\\PFM Eps Rename\\New_Encoder\\source"
exclude_words = ["ep", "chapter"] # Add words you want to exclude
rename_mp3_files(directory_path, exclude_words)
