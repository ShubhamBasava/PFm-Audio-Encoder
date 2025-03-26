import os
import zipfile
import math
from tqdm import tqdm

CHUNK_SIZE = 1024 * 1024 * 1024  # 1 GB chunks for large files

def get_file_size(file_path):
    """Returns the file size in bytes."""
    return os.path.getsize(file_path)

def split_large_file(file_path, output_dir, max_size=3.5 * 1024 * 1024 * 1024):
    """Splits a large file into smaller chunks."""
    file_size = get_file_size(file_path)
    
    if file_size <= max_size:
        return [file_path]  # No need to split

    print(f"Splitting large file: {os.path.basename(file_path)} ({file_size / (1024**3):.2f} GB)")
    
    base_name = os.path.basename(file_path)
    file_parts = []
    part_num = 1

    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            part_name = os.path.join(output_dir, f"{base_name}_Part{part_num}.mp3")
            with open(part_name, "wb") as part_file:
                part_file.write(chunk)
            file_parts.append(part_name)
            part_num += 1

    return file_parts

def create_zip(output_dir, zip_name, max_size=3.5 * 1024 * 1024 * 1024):
    """Splits and zips MP3 files, ensuring no ZIP exceeds max_size."""
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.mp3')]
    
    if not files:
        print("No MP3 files found in the directory. Exiting.")
        return

    # Handle large files by splitting them first
    all_files = []
    for file in files:
        all_files.extend(split_large_file(file, output_dir, max_size))

    total_size = sum(get_file_size(f) for f in all_files)
    num_parts = math.ceil(total_size / max_size)
    
    print(f"Total MP3 files (after splitting): {len(all_files)}, Total Size: {total_size / (1024**3):.2f} GB")
    print(f"Splitting into {num_parts} ZIP files (Max {max_size / (1024**3):.2f} GB each)")
    
    part = 1
    current_size = 0
    zip_part_name = os.path.join(output_dir, f"{zip_name}_Part{part}.zip")
    zip_file = zipfile.ZipFile(zip_part_name, 'w', zipfile.ZIP_STORED)
    
    for file in tqdm(all_files, desc="Zipping Files", unit="file"):
        file_size = get_file_size(file)
        
        # Start a new ZIP file if size exceeds limit
        if current_size + file_size > max_size:
            zip_file.close()
            part += 1
            zip_part_name = os.path.join(output_dir, f"{zip_name}_Part{part}.zip")
            zip_file = zipfile.ZipFile(zip_part_name, 'w', zipfile.ZIP_STORED)
            current_size = 0  # Reset counter
        
        zip_file.write(file, os.path.basename(file))
        current_size += file_size
    
    zip_file.close()
    print(f"Zipping completed. Created {part} ZIP file(s).")

if __name__ == "__main__":
    output_dir = r"D:\Telegram\PFM Eps Rename\New_Encoder\Output"
    zip_name = input("Enter ZIP file name: ").strip()
    create_zip(output_dir, zip_name)
