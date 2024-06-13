import os
import shutil
import time
from datetime import datetime

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Change to the desired directory
desired_directory = '/Users/viralpreetijoshi/Desktop/Clutter Cleaner'  # Replace this with your actual directory
os.chdir(desired_directory)

# List files in the new directory
files = os.listdir()
print(files)

# Configuration
directory_to_clean = '/Users/viralpreetijoshi/Desktop/Clutter Cleaner'
days_old_threshold = 30  # Files older than this number of days will be deleted
file_types_to_move = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.avif'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav']
}
log_file = os.path.join(directory_to_clean, 'cleaner_log.txt')  # Ensure log file is created in the target directory

# Helper function to log actions
def log_action(message):
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} - {message}\n")
    print(message)  # Also print the message for real-time feedback

# Helper function to delete old files
def delete_old_files(directory, days_old):
    now = time.time()
    cutoff_time = now - (days_old * 86400)  # Convert days to seconds

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = os.path.getmtime(file_path)
            if file_age < cutoff_time:
                try:
                    os.remove(file_path)
                    log_action(f"Deleted file: {file_path}")
                except Exception as e:
                    log_action(f"Error deleting file {file_path}: {e}")

# Helper function to move files to subfolders
def move_files_to_subfolders(directory, file_type_dict):
    for subfolder, extensions in file_type_dict.items():
        subfolder_path = os.path.join(directory, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in extensions:
                try:
                    shutil.move(file_path, os.path.join(subfolder_path, filename))
                    log_action(f"Moved file {file_path} to {subfolder_path}")
                except Exception as e:
                    log_action(f"Error moving file {file_path} to {subfolder_path}: {e}")

# Main function to run the cleaner
def run_folder_cleaner():
    log_action("Starting folder cleaner")
    delete_old_files(directory_to_clean, days_old_threshold)
    move_files_to_subfolders(directory_to_clean, file_types_to_move)
    log_action("Folder cleaner completed")

if __name__ == '__main__':
    run_folder_cleaner()
