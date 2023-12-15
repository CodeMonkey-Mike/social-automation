import random

scenery = [
  "a Seascape",
  "a Mountain",
  "Mountains",
  "a Forest",
  "a Beach",
  "a Cloudscape",
  "a desert",
  "Astrophotography",
  "Panorama Photography",
  "Time Lapse Photography",
  "Long Exposure Photography",
  "Star Trail Photography",
  "a Sunrise",
  "a Sunset",
  "Night Photography",
  "Representational Photography",
  "Abstract Photography",
  "a Fantasy world",
  "a Futuristic Landscape",
  "a Underwater World",
  "a Winter Wonderland",
  "Enchanted Nature",
  "a Countryside Landscape",
  "a Surreal landscape",
  "an Urban landscape",
  "Starry skies",
  "a Moonlit landscape",
]

styles = [
  "psychedelic",
  "surreal",
  "vaporwave",
  "modern",
  "ancient",
  "futuristic",
  "retro",
  "realistic",
  "dreamlike",
  "ultra realistic",
  "hyper realistic",
  "high details",
  "holographic",
  "cyberpunk",
  "nanopunk",
  "biopunk",
  "cyber noir",
  "steampunk",
  "clockpunk",
  "dieselpunk",
  "decopunk",
  "coalpunk",
  "atompunk",
  "steelpunk",
  "islandpunk",
  "oceanpunk",
  "rococopunk",
  "stonepunk",
  "mythpunk",
  "raypunk",
  "nowpunk",
  "cyberprep",
  "postcyberpunk",
  "solarpunk",
  "lunarpunk",
  "elfpunk",
  "atompunk",
  "neonpunk",
  "translucent",
  "luminescent",
  "magical",
  "glowing particles",
  "creation",
  "living breathing",
  "cinematic",
  "masterpiece",
  "octane render",
  "8k",
  "ray-tracing",
  "blender",
  "highly detailed",
  "oil painting",
  "voluminous lighting",
  "photo-realistic",
  "watercolor",
  "vintage",
  "high color depth",
]
artist_name = [
  "Arthur Adams",
  "Neal Adams",
  "Scott Adams",
  "Charles Addams",
  "Mattias Adolfsson",
  "Alena Aenami",
  "David Aja",
  "Rafael Albuquerque",
  "Mike Allred",
  "Chris Van Allsburg",
  "Yoshitaka Amano",
  "Sarah Andersen",
  "Richard Anderson",
  "Mitsumasa Anno",
  "Martin Ansin",
  "Sabbas Apterus",
  "Sergio Aragones",
  "Hiromu Arakawa",
  "Rolf Armstrong",
  "Artgerm",
  "Thomas Ascott",
  "John James Audubon",
  "Tex Avery",
  "Chris Bachalo",
  "Anne Bachelier",
  "Peter Bagge",
  "Mark Bagley",
  "Ralph Bakshi",
]

def pick_random_text(text_array):
    # Check if the array is empty
    if not text_array:
        return None

    # Use random.choice to pick a random text item
    random_text = random.choice(text_array)
    return random_text

def pick_unique_style(text_array):
    # Check if the array is empty
    if not text_array:
        return None

    # Use random.sample() to pick 3 unique items
    random_text = random.sample(text_array, 3)
    styles = ", ".join(random_text)
    return styles

def get_prompt(article_title, artist):
  prompt = f'{article_title}, expansive view of {pick_random_text(scenery)},  art style of {artist}, {pick_unique_style(styles)}, --no text,words --ar 16:9'
  return prompt

def get_artist_name():
  return pick_random_text(artist_name)