# Import your models
import tweepy
from .config import BaseConfig
from .poll import delete_posted_poll, pick_poll_more_than_7_days, get_chat_message, get_options, filter_options, globalMessages, get_poll_data

client = tweepy.Client(
    consumer_key=BaseConfig.TW_CONSUMER_KEY,
    consumer_secret=BaseConfig.TW_CONSUMER_SECRET,
    access_token=BaseConfig.TW_ACCESS_TOKEN,
    access_token_secret=BaseConfig.TW_ACCESS_SECRET
)


def post_poll_to_twitter(tw_text, tw_topic, options):
    if len(options):
        client.create_tweet(
            text=f"{tw_text} \nsubsKribe to me on YouTube: https://bit.ly/subscribeToCodeMonkey\n#{tw_topic.replace(' ', '')}",
            poll_options=options,
            poll_duration_minutes=10080
        )
    else:
        print('Error when posting new poll.')
        return None


def create_twitter_poll():
    message = get_chat_message()
    print("message:", message)
    tw_text = message.get('poll_name')
    tw_topic = message.get('topic')
    options, hasLongLength = get_options(message, 25)

    if hasLongLength == 1:
        options = filter_options(options)
    elif hasLongLength >= 2:
        globalMessages.append({
            "role": "user",
            "content": "Generate a new one"
        })
        create_twitter_poll()
        print("hasLongLength:", hasLongLength)

    print("new_options:", options)
    post_poll_to_twitter(tw_text, tw_topic, options)


def post_twitter_poll():
    polls = get_poll_data("twitter")
    poll = pick_poll_more_than_7_days(polls)
    print('poll:', poll)
    tw_text = poll.get('title')
    tw_topic = poll.get('topic')
    options, hasLongLength = get_options(poll, 25)
    if hasLongLength == 1:
        options = filter_options(options)
    elif hasLongLength >= 2:
        post_twitter_poll()

    print("new_options:", options)
    post_poll_to_twitter(tw_text, tw_topic, options)
    delete_posted_poll(poll)
