import os

def rename_files_in_directory(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    # Filter out non-mp3 files
    mp3_files = [file for file in files if file.endswith('.mp3')]
    
    # Sort the files to ensure consistent renaming
    mp3_files.sort()
    
    # Rename files to a sequential format
    for i, filename in enumerate(mp3_files):
        new_name = f"{i + 1}.mp3"
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_name)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{old_file_path}' to '{new_file_path}'")

# Define the source directory
source_directory = r"D:\Telegram\PFM Eps Rename\New_Encoder\source"

# Rename the files in the specified directory
rename_files_in_directory(source_directory)
