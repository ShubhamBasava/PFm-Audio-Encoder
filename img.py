import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

def update_audio_files_image(image_path, audio_files_dir):
    """
    Updates the cover image for all MP3 files in the specified directory.

    :param image_path: Path to the image file to use as the cover art.
    :param audio_files_dir: Path to the directory containing MP3 files.
    """
    # Ensure the image file exists
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return

    # Ensure the audio files directory exists
    if not os.path.isdir(audio_files_dir):
        print(f"Audio files directory not found: {audio_files_dir}")
        return

    # Iterate over all files in the directory
    for file_name in os.listdir(audio_files_dir):
        file_path = os.path.join(audio_files_dir, file_name)

        # Only process MP3 files
        if file_name.lower().endswith(".mp3"):
            try:
                # Load the MP3 file and its ID3 tag
                audio = MP3(file_path, ID3=ID3)

                # If the file does not have an ID3 tag, add one
                if audio.tags is None:
                    audio.add_tags()

                # Remove existing APIC (cover art) tags
                audio.tags.delall("APIC")

                # Add or update the cover image
                with open(image_path, 'rb') as img_file:
                    audio.tags.add(
                        APIC(
                            encoding=3,  # UTF-8
                            mime='image/jpeg',  # MIME type for the image
                            type=3,  # Front cover
                            desc='Cover',
                            data=img_file.read()  # Read the image data
                        )
                    )

                # Save the changes to the MP3 file
                audio.save()
                print(f"Updated cover image for: {file_name}")

            except error as e:
                print(f"Error updating {file_name}: {e}")
        else:
            print(f"Skipping non-MP3 file: {file_name}")

if __name__ == "__main__":
    # Correct image and audio files directory paths
    image_path = r"D:\Telegram\PFM Eps Rename\New_Encoder\image.jpg"
    audio_files_dir = r"D:\Telegram\PFM Eps Rename\New_Encoder\source"

    # Update the cover image for all MP3 files in the directory
    update_audio_files_image(image_path, audio_files_dir)
