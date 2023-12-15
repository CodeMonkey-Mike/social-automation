import os
import requests
import re
from PIL import Image
from io import BytesIO
import numpy as np
from pathlib import Path
from moviepy.editor import VideoFileClip, VideoClip, AudioFileClip, ImageClip, concatenate_videoclips

Image.ANTIALIAS=Image.Resampling.LANCZOS

project_root = os.path.dirname(__file__)
playlist_file = os.path.join(Path(project_root).resolve().parents[0], 'stream/playlist.txt')

def title_cleanup(text):
    # Define a regular expression pattern to match special characters
    pattern = r'[^A-Za-z0-9_ ]+'
    
    # Use re.sub to replace matched special characters with an empty string
    clean_string = re.sub(pattern, '', text)
    
    return clean_string

def resize_video(video, input_video_path):
    # Resize the video to a specific width and height
    new_width = 1280  # Replace with your desired width
    new_height = 720  # Replace with your desired height
    video_resized = video.resize((new_width, new_height), Image.LANCZOS)

    # Write the resized video to the final path
    video_resized.write_videofile(input_video_path, codec='libx264', fps=24, audio_codec='aac', audio_fps=44100)

def save_video_to_playlist(video_path):
    with open(playlist_file, 'a') as playlist:
        playlist.write(f"file '{video_path}'\n")

def filter_videos():
    # Read the playlist and filter existing files
    existing_files = []
    with open(playlist_file, 'r') as playlist:
        for line in playlist:
            file_path = line.strip().replace("file '", "").replace("'", "")
            if os.path.exists(file_path):
                existing_files.append(line)
    
    print("existing_files:", existing_files)
    # Overwrite the original playlist with the filtered version
    with open(playlist_file, 'w') as output:
        output.writelines(existing_files)

def generate_video(title_img_path, title_audio_path, video_title, image_paths, audio_paths, project_folder):

    if len(image_paths) != len(audio_paths):
        raise ValueError("The number of image paths must match the number of audio paths.")

    # Create a list to store video clips for each pair of image and audio
    video_clips = []

    # Create intro
    title_audio_clip = AudioFileClip(title_audio_path)
    title_image_clip = ImageClip(title_img_path, duration=title_audio_clip.duration)
    title_video_with_audio = title_image_clip.set_audio(title_audio_clip)
    video_clips.append(title_video_with_audio)
    for image_path, audio_path in zip(image_paths, audio_paths):
        # Load the audio as an audio clip
        audio_clip = AudioFileClip(audio_path)
        
        # Set a custom User-Agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Make an HTTP request with the custom User-Agent
        response_image_path = requests.get(image_path, headers=headers)
        # Load the image as a video clip with the same duration as the audio
        # Check if the request was successful
        if response_image_path.status_code == 200:
            # Convert the response content (bytes) to a PIL Image
            image = Image.open(BytesIO(response_image_path.content))
            
            # Convert the PIL Image to a NumPy array
            image_array = np.array(image)

            # Create an ImageClip from the NumPy array
            image_clip = ImageClip(image_array, duration=audio_clip.duration)
            
            # You can perform further operations on the image clip or use it in your video composition
        else:
            print("Failed to fetch the image.")
        # image_clip = ImageClip(response_image_path.content, duration=audio_clip.duration)
        print('image_clip:', image_clip)
        # Set the audio of the image clip to the loaded audio clip
        video_with_audio = image_clip.set_audio(audio_clip)
        
        video_clips.append(video_with_audio)

    # Concatenate the video clips to create the final video
    # final_video = VideoFileClip.empty()
    # for video_clip in video_clips:
    #     final_video = final_video.set_duration(final_video.duration + video_clip.duration)
    #     final_video = final_video.set_audio(final_video.audio.set_duration(final_video.duration))
    #     final_video = final_video.set_video(final_video.video.set_duration(final_video.duration))
    #     final_video = final_video.set_make_frame(lambda t: final_video.get_frame(t))

    # Concatenate the video clips to create the final video
    final_video = concatenate_videoclips(video_clips, method="compose")


    # Specify the output video file path within the project folder
    output_video_path = title_cleanup(video_title)
    final_video_path = os.path.join(project_folder, f"{output_video_path}.mp4")

    # Write the composite video to the output file
    
    final_video.write_videofile(final_video_path, codec='libx264', fps=24, audio_codec='aac', audio_fps=44100)
    resize_video(final_video, final_video_path)
    filter_videos()
    save_video_to_playlist(final_video_path)
# def generate_video(video_title, image_path, audio_path, project_folder):
    
#     # Load the audio as an audio clip
#     audio_clip = AudioFileClip(audio_path)
    
#     # Load the image as a video clip
#     print('audio_clip.duration:', audio_clip.duration)
#     image_duration = audio_clip.duration
#     # image_clip = VideoClip(make_frame=lambda t: image_path, duration=image_duration)
#     image_clip = ImageClip(image_path, duration=image_duration)
#     # image_clip = VideoClip(make_frame=lambda t: image_path, duration=audio_clip.duration)
#     # Set the audio of the image clip to the loaded audio clip

#     video_with_audio = image_clip.set_audio(audio_clip)
#     # Specify the output video file path within the project folder
#     output_video_path = os.path.join(project_folder, f'{video_title}.mp4')

#     # Write the composite video to the output file
#     video_with_audio.write_videofile(output_video_path, codec='libx264', fps=24, audio_codec='aac', audio_fps=44100)