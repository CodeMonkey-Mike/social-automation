# -*- encoding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, send_from_directory
from .poll import save_poll_to_db
from .linkedin_poll import post_linkedin_poll
from .twitter_poll import post_twitter_poll
from .generate_video import generate_images_from_prompts
from .carousel import get_tweet_and_save_to_db
from .carousel_slide import create_tweet_in_carousel


app = Flask(__name__)

app.config.from_object('api.config.BaseConfig')
CORS(app)


@app.route('/')
def home():
    html = 'Welcome to Social Generator!'
    return html


@app.route('/static/<path:path>')
def send_files(path):
    return send_from_directory('static', path)


@app.route('/generate-video')
def generate_video():
    generate_images_from_prompts()
    return 'Done!'


@app.route('/generate-linkedin-polls')
def generate_linkedin_polls():
    save_poll_to_db("linkedin")
    return 'Done!'


@app.route('/generate-twitter-polls')
def generate_twitter_polls():
    save_poll_to_db("twitter")
    return 'Done!'


@app.route('/twitter-poll')
def twitter_poll():
    post_twitter_poll()
    return 'Done!'


@app.route('/linkedin-poll')
def linkedin_poll():
    post_linkedin_poll()
    return 'Done!'


@app.route('/generate-carousel')
def generate_carousel():
    get_tweet_and_save_to_db()
    return 'Done!'


@app.route('/tweet-to-twitter')
def tweet_to_twitter():
    create_tweet_in_carousel()
    return 'Done!'
