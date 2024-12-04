import os
import subprocess
import time

def is_file_empty(file_path):
    """
    Check if the given file is empty or contains only whitespace.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            return len(content) == 0
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return True

def run_script(script_name):
    """
    Run a Python script using subprocess and handle errors.
    """
    try:
        print(f"Running {script_name}...")
        # Ensure spaces in paths are correctly handled by quoting the paths
        subprocess.run(['python3', script_name], check=True)
        print(f"{script_name} finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
    except FileNotFoundError:
        print(f"Script not found: {script_name}")

def main():
    current_dir = os.getcwd()  # Get the current working directory
    urls_file = os.path.join(current_dir, "urls.txt")
    chadly_puker_script = os.path.join(current_dir, "puker.py")
    reload_script = os.path.join(current_dir, "reload.py")

    while not is_file_empty(urls_file):
        run_script(chadly_puker_script)
        time.sleep(1)  # Optional delay between scripts
        run_script(reload_script)
        time.sleep(1)

    print("Processing completed. 'urls.txt' is empty.")

if __name__ == "__main__":
    main()
