import os
import json
import asyncio
import feedparser
import random
import requests

from pathlib import Path
from .chat_gpt import ChatGPTAPI
from PIL import Image, ImageDraw, ImageFont
from snakecase import convert
from newsplease import NewsPlease
from .config import BaseConfig


# Get the project root directory
project_root = os.path.dirname(__file__)

# Define a directory to save the images in the project root
font_path = os.path.join(Path(project_root).resolve().parents[0], 'static/fonts/Raleway-Bold.ttf')
logo_path = os.path.join(Path(project_root).resolve().parents[0], 'static/Yahoo-Finance-logo.jpg')

chat_gpt = ChatGPTAPI()

def create_event_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())


def fetch_and_parse_articles(rss_url, num_articles=2):
    # Fetch the RSS feed
    feed = feedparser.parse(rss_url)
    # print('feed:', feed)
    # Check if the feed was successfully fetched
    if feed.bozo == 0 or feed.bozo == False:
        # Get a list of all the entries in the feed
        entries = feed.entries

        # Filter articles with source = "Yahoo Finance"
        yahoo_finance_articles = [article for article in entries if "finance.yahoo.com" in article.link]

        new_articles = yahoo_finance_articles
        if len(yahoo_finance_articles) < 2:
            new_articles = entries
        
        # Ensure there are enough articles to choose from
        if len(new_articles) >= num_articles:
            # Randomly select two articles
            selected_articles = random.sample(entries, num_articles)

            # Return the selected articles as a list of dictionaries
            return [{"title": article.title, "link": article.link} for article in selected_articles]

    # Return an empty list if fetching or parsing fails
    return []

def create_image(title):
    yahoo_finance_logo = Image.open(logo_path)
    # Create an image with the title text
    font_size = 74
    image = Image.new('RGB', (1456, 816), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    font.getbbox
    # Apply line wrap if the text is longer than the image width
    max_width = int(image.width * 0.9)
    wrapped_text = wrap_text(title, max_width, font)
    line_spacing = 1.3  # Adjust this value based on your needs
    x = (image.width - max_width) // 2
    y = (image.height - int(font_size * len(wrapped_text) * line_spacing)) // 2
    image.paste(yahoo_finance_logo, (x, y - 100)) 
    for line in wrapped_text:
        draw.text((x, y), line, fill='black', font=font)
        y += int(font_size * line_spacing)

    return image

def wrap_text(text, max_width, font):
    lines = []
    words = text.split(' ')
     
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        _, _,line_width, _ = font.getbbox(test_line)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line[:-1])
            current_line = word + ' '
 
    lines.append(current_line[:-1])
    return lines

def remove_breakline(text):
    # Replace single and double newline characters with spaces
    print('text:', text)
    cleaned_text = text.replace('\n', '').replace('\n\n', '').replace('* ', '').replace('**', '')
    print('cleaned_text:', cleaned_text)
    return cleaned_text

def extract_content_until_paragraph(text, stop_phrase):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')
    paragraphs.pop(0)
    # print('paragraphs=>>>>>', paragraphs)

    # Initialize the extracted content
    extracted_content = ""
    extracted_paragraphs = []

    for paragraph in paragraphs:
        # Append each paragraph to the extracted content
        extracted_content += paragraph + '\n\n'

        # Check if the stop phrase is found in the paragraph
        if stop_phrase in paragraph:
            break
        if "Here are some additional things" in paragraph:
            break
        if "I hope this summary is helpful" in paragraph:
            break
        if "Summary in less than 100 words:" in paragraph:
            break
        if "Summary in less than 200 words:" in paragraph:
            break

    # Strip leading and trailing whitespace
    extracted_content = extracted_content.strip()
    extracted_paragraphs = extracted_content
    # Split the extracted content into paragraphs again
    extracted_paragraphs = extracted_content.split('\n\n')

    # Remove the last paragraph (if it exists)
    if extracted_paragraphs and extracted_paragraphs[-1].strip():
        extracted_paragraphs.pop()

    # Join the remaining paragraphs back together
    extracted_content = '\n\n'.join(extracted_paragraphs)

    return extracted_content, extracted_paragraphs

def create_summary_from_chatgpt(article_url):
    article = NewsPlease.from_url(article_url)
    if article and article.maintext and len(article.maintext) > 0:
        paragraphs, article_summary = get_summary_from_prompt(article.maintext)
        return paragraphs, article_summary 
    else:
        return [], ""

def get_summary_from_prompt(prompt):
    paragraphs = []
    article_summary = ""


    # Create an event loop for each thread
    create_event_loop()

    async def process_prompts():
        nonlocal paragraphs
        nonlocal article_summary
        p, a = await chat_gpt.get_summary(prompt)
        paragraphs = p
        article_summary = a

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_prompts())
    loop.close()

    return paragraphs, article_summary


# def create_summary(article_url):
#     article = NewsPlease.from_url(article_url)
#     if article and len(article.maintext) > 0:
#         summary = bard.get_answer(f"Write a summary less than 200 words from this content: \n {article.maintext}")['content']
#         stop_phrase = "Here are some additional details"
#         res = extract_content_until_paragraph(summary, stop_phrase)
#         return res
#     else:
#         return "", []

def text_to_speech_api_request(title, text, audito_directory):
    url = 'https://api.elevenlabs.io/v1/text-to-speech/1zgL8r0RQHbUVHDHch2D'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': f'{BaseConfig.ELEVENLAB_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "text": json.dumps(text),
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:

        # Specify the name of the audio file
        audio_filename = f'{convert(title).replace(" ", "")}.mp3'
        os.makedirs(audito_directory, exist_ok=True)
        audio_path = os.path.join(audito_directory, audio_filename)

        # Save the audio data to the specified path
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        
        return audio_path
    else:
        return None
    