import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {script_name}:\n{result.stderr}")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")

print("Starting chapters_Edit...")
run_script('chapters_Edit.py')
print("Starting audio edit Process please wait..")
run_script('audio_Edit.py')
print("audio_Edit.py completed.")
