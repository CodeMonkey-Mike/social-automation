import os
import datetime
from pathlib import Path

# Get the project root directory
project_root = os.path.dirname(__file__)
# Specify the folder path where your videos are located
folder_path = os.path.join(Path(project_root).resolve().parents[0], 'static/videos')

# Calculate the current date and time
current_date = datetime.datetime.now()

# Define the maximum age for videos (5 days)
max_age = datetime.timedelta(days=5)

def clenup():
  # Iterate over the files in the folder
  for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)

      # Check if the file is a regular file (not a directory) and it's older than max_age
      if os.path.isfile(file_path) and file_path.endswith(".mp4"):
          file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
          file_age = current_date - file_creation_time

          if file_age > max_age:
              # If the file is older than max_age, delete it
              os.remove(file_path)
              print(f"Deleted {filename} (age: {file_age})")