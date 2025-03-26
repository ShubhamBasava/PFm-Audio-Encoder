import os
import json

def get_chapters_from_files(directory, use_titles):
    """
    Generates chapters based on the file names or titles in the specified directory.

    Args:
        directory (str): Path to the directory containing MP3 files.
        use_titles (bool): If True, use file titles; if False, use file names.

    Returns:
        list: List of chapter names.
    """
    chapters = []

    for file in sorted(os.listdir(directory)):
        if file.lower().endswith(".mp3"):
            if use_titles:
                # Extract the title by removing the extension
                title = os.path.splitext(file)[0]
                chapters.append(title)
            else:
                # Use file name directly without the extension
                chapters.append(os.path.splitext(file)[0])

    return chapters

def main():
    source_dir = r"D:\Telegram\PFM Eps Rename\New_Encoder\source"
    output_dir = r"D:\Telegram\PFM Eps Rename\New_Encoder"
    output_file = os.path.join(output_dir, "chapters.json")

    print("Choose an option to generate chapters:")
    print("1: Use file names")
    print("2: Use titles")

    try:
        option = int(input("Enter your choice (1 or 2): "))
        if option not in [1, 2]:
            print("Invalid option. Please choose 1 or 2.")
            return

        use_titles = option == 2

        # Generate chapters
        chapters = get_chapters_from_files(source_dir, use_titles)

        # Save chapters to output file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chapters, f, indent=2, ensure_ascii=False)

        print(f"Chapters have been successfully saved to: {output_file}")
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
