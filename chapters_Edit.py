import json
import re

# Function to clean chapter titles
def clean_chapter_title(title):
    # Regular expression to match and remove any "Ep X", "Ch Y", "Ep X -", "Ch Y -" parts
    cleaned_title = re.sub(r'(Ep \d+\s*-*\s*)|(Ch \d+\s*-*\s*)', '', title).strip()
    return cleaned_title

# Function to double-check and clean chapter titles
def double_check_clean_titles(titles):
    cleaned_titles = []
    for title in titles:
        cleaned_title = clean_chapter_title(title)
        cleaned_title = clean_chapter_title(cleaned_title)  # Clean again if needed
        cleaned_titles.append(cleaned_title)
    return cleaned_titles

# Load the JSON data from the file
with open('chapters.json', 'r') as file:
    chapters = json.load(file)

# Clean each chapter title and double-check
cleaned_chapters = double_check_clean_titles(chapters)

# Save the cleaned data back to the JSON file
with open('chapters.json', 'w') as file:
    json.dump(cleaned_chapters, file, indent=2)

print("Chapter titles have been successfully cleaned and the file has been updated.")
