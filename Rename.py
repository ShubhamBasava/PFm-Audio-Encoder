import os
import re

def rename_files_in_directory(directory):
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied to access '{directory}'.")
        return

    # Filter out non-mp3 files
    mp3_files = [file for file in files if file.endswith('.mp3')]

    # Check if there are any mp3 files to rename
    if not mp3_files:
        print("No .mp3 files found in the directory.")
        return

    # Sort the files to ensure consistent renaming
    mp3_files.sort()

    # Regular expression to match only numbers in the filenames
    number_pattern = re.compile(r'\d+')

    for filename in mp3_files:
        # Extract the first number found in the filename
        match = number_pattern.search(filename)
        if match:
            new_name = f"{match.group()}.mp3"  # Keep only the number as the new name
        else:
            print(f"Warning: No number found in '{filename}', skipping.")
            continue
        
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_name)

        try:
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_name}'")
        except OSError as e:
            print(f"Error renaming '{filename}': {e}")

# Example usage
source_directory = r"D:\Telegram\PFM Eps Rename\New_Encoder\source"
rename_files_in_directory(source_directory)
