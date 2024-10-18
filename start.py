import subprocess
def run_script(script_name, *args):
    try:
        result = subprocess.run(['python', script_name, *args], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {script_name}:\n{result.stderr}")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")

# Get user input for title, start, and end episodes
title = input("Enter the title: ")
start = input("Enter the starting episode number: ")
end = input("Enter the ending episode number: ")

print("Starting chapters_Edit...")
run_script('chapters_Edit.py')
print("Starting audio edit process, ")
run_script('audio_edit.py', title, start, end)
print("Audio edit process completed.")

# Ask user if they want to create zip files
create_zip = input("Do you want to create zip files? (Yes/No): ").strip().lower()

if create_zip in ['yes', 'y']:
    base_zip_name = title  # Use the title as the base name for zip files
    print("Starting zip process,")
    run_script('zipAudio.py', base_zip_name)
    print("Zip process completed.")
else:
    print("Skipping zip process.")
