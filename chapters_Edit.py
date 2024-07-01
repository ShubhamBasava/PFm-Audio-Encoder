import json
import re

# Function to clean chapter titles
def clean_chapter_title(title):
    # Regular expression to match and remove any "Ep-", "EP-", "Ch-", "CH-", "Cp-", "CP-" parts
    cleaned_title = re.sub(r'\b(?:Ep|EP|Ch|CH|Cp|CP)-*\s*\d*\s*-*\s*', '', title).strip()
    return cleaned_title

# Function to double-check and clean chapter titles
def double_check_clean_titles(titles):
    cleaned_titles = [clean_chapter_title(clean_chapter_title(title)) for title in titles]
    return cleaned_titles

# Load the JSON data from the file
with open('chapters.json', 'r', encoding='utf-8') as file:
    chapters = json.load(file)

# Clean each chapter title and double-check
cleaned_chapters = double_check_clean_titles(chapters)

# Save the cleaned data back to the JSON file
with open('chapters.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_chapters, file, indent=2, ensure_ascii=False)

print("Chapter titles have been successfully cleaned and the file has been updated.")
