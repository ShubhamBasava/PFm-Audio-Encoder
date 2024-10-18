import os
import zipfile
from tqdm import tqdm

def get_file_size(file_path):
    return os.path.getsize(file_path)

def create_zip_files(directory, base_zip_name, max_size_gb=1.9):
    max_size_bytes = max_size_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    files = [file for file in os.listdir(directory) if file.endswith('.mp3')]
    files.sort()

    total_size = sum(get_file_size(os.path.join(directory, file)) for file in files)
    processed_size = 0

    zip_index = 1
    current_zip_size = 0
    zip_file = None

    # Initialize the progress bar with total size
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Processing files") as pbar:
        for file in files:
            file_path = os.path.join(directory, file)
            file_size = get_file_size(file_path)

            if zip_file is None or current_zip_size + file_size > max_size_bytes:
                if zip_file is not None:
                    zip_file.close()

                zip_file_name = f"{base_zip_name}_{zip_index}.zip"
                zip_file_path = os.path.join(directory, zip_file_name)
                zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
                print(f"Created zip file: {zip_file_path}")
                zip_index += 1
                current_zip_size = 0

            zip_file.write(file_path, os.path.basename(file_path))
            current_zip_size += file_size
            processed_size += file_size
            pbar.update(file_size)  # Update the progress bar with the file size

    if zip_file is not None:
        zip_file.close()
        print(f"Finalized zip file: {zip_file.filename}")

if __name__ == "__main__":
    # Define the source directory and get the base name for zip files from the user
    source_directory = r"D:\Telegram\PFM Eps Rename\New_Encoder\Output"
    base_zip_name = input("Enter the base name for the zip files: ")

    # Create the zip files
    create_zip_files(source_directory, base_zip_name)
