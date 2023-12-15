import asyncio
import os
import time
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
from .utils import fetch_and_parse_articles, create_image, create_summary_from_chatgpt, text_to_speech_api_request, remove_breakline
from .movie_maker import generate_video
from .midjourney import MidjourneyAPI
from .prompt import get_prompt, get_artist_name
from snakecase import convert
from .cleanup import clenup

# Get the project root directory
project_root = os.path.dirname(__file__)

# RSS feed URL
rss_url = "https://finance.yahoo.com/rss/"

# Define a directory to save the images in the project root
image_directory = os.path.join(
    Path(project_root).resolve().parents[0], 'static/images')
audio_directory = os.path.join(
    Path(project_root).resolve().parents[0], 'static/audios')
video_directory = os.path.join(
    Path(project_root).resolve().parents[0], 'static/videos')

# Create the image directory if it doesn't exist
os.makedirs(image_directory, exist_ok=True)
midjourney_api = MidjourneyAPI()


def create_event_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())


def generate_images_from_prompts(prompts, artist_name):
    img_uris = []

    # Create an event loop for each thread
    create_event_loop()

    async def process_prompts():
        nonlocal img_uris

        for original_prompt in prompts:
            article_title = original_prompt.get("art")
            prompt = get_prompt(article_title, artist_name)
            if len(article_title) > 0:
                img_uri = await midjourney_api.generate_image(prompt)
                img_uris.append(img_uri)
            else:
                None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_prompts())
    loop.close()

    return img_uris


def generate_video_by_mj():
  # Fetch and parse two random articles
    articles = fetch_and_parse_articles(rss_url, num_articles=2)
    image_paths = []
    title_audio_paths = []

    # Build an image from title
    for article in articles:
        title = article['title']
        img = create_image(title)
        title_audio_path = text_to_speech_api_request(
            f"title_{convert(title).replace(' ', '')}", title, audio_directory)
        title_audio_paths.append(title_audio_path)
        # Save the image to the project root
        img_path = os.path.join(
            image_directory, f'{convert(title).replace(" ", "")}.png')
        img.save(img_path)
        image_paths.append(img_path)

    summaries = []
    prompts = []
    titles = []
    # Build a plain text response
    for article in articles:
        title = article['title']
        titles.append(title)
        link = article['link']
        paragraphs, article_summary = create_summary_from_chatgpt(link)
        if len(paragraphs) > 0:
            prompts.append(paragraphs)

        summaries.append({"title": title, "summary": article_summary})
        time.sleep(20)

    art_images1 = []
    if len(prompts) > 0 and len(prompts[0]) > 0:
        artist_name_1 = get_artist_name()
        generated_images1 = generate_images_from_prompts(
            prompts[0], artist_name_1)
        art_images1 = generated_images1

    audio_paths1 = []
    if len(prompts) > 0 and len(prompts[0]) > 0:
        for index, prompt in enumerate(prompts[0], start=1):
            article_title = prompt.get("text")
            if article_title and len(article_title) > 0:
                audio_path = text_to_speech_api_request(
                    f"{index}_{convert(titles[0]).replace(' ', '')}", article_title, audio_directory)
                audio_paths1.append(audio_path)

    # Generate video 1
    if image_paths[0] and title_audio_paths[0]:
        generate_video(image_paths[0], title_audio_paths[0], convert(
            titles[0]).replace(' ', '_'), art_images1, audio_paths1, video_directory)
    else:
        print("Generate video 1 is failed")

    # art_images2 = []
    # if len(prompts) > 0 and len(prompts[1]) > 0:
    #     artist_name_2 = get_artist_name()
    #     generated_images2 = generate_images_from_prompts(prompts[1], artist_name_2)
    #     art_images2 = generated_images2

    # audio_paths2 = []
    # if len(prompts) > 0 and len(prompts[1]) > 0:
    #     for index, prompt in enumerate(prompts[1], start=1):
    #         article_title = prompt.get("text")
    #         if article_title and len(article_title) > 0:
    #             audio_path = text_to_speech_api_request(f"{index}_{convert(titles[1]).replace(' ', '')}", article_title, audio_directory)
    #             audio_paths2.append(audio_path)

    # # Generate video 2
    # if image_paths[1] and title_audio_paths[1]:
    #     generate_video(image_paths[1], title_audio_paths[1], convert(titles[1]).replace(' ', '_'), art_images2, audio_paths2, video_directory)
    # else:
    #     print("Generate video 2 is failed")

    # Do cleanup after 5 days
    clenup()

    # Display the images on the webpage
    # image_tags = [f'<img src="{img_path}" alt="{article["title"]}">' for img_path, article in zip(image_paths, articles)]
    # html = ''.join(image_tags)
