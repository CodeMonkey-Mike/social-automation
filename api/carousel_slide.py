import asyncio
import time
from .carousel import delete_posted_carousel, reply_to_tweet_by_id, post_to_twitter_in_thread, get_carousel, pick_carousel_more_than_7_days, get_carousel_slides


def create_event_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())


def create_tweet_in_carousel():

    carousel_list = get_carousel()
    carousel = pick_carousel_more_than_7_days(carousel_list)
    carousel_id = carousel.get('id')
    if carousel_id:
        carousel_slides = get_carousel_slides(carousel_id)
        first_tweet = carousel_slides[0]
        original_tweet = post_to_twitter_in_thread(
            first_tweet.get('description'))
        print('original_tweet:', original_tweet['id'])
        reply_carousel_slides = carousel_slides[1:]

        async def process_carousel_slides():
            for carousel_slide in reply_carousel_slides:
                time.sleep(20)
                reply_to_tweet_by_id(carousel_slide.get(
                    'description'), original_tweet['id'])
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_carousel_slides())
        loop.close()
        delete_posted_carousel(carousel_id)
