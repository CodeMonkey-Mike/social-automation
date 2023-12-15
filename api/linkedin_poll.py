import json
import os
import sys
from dotenv import load_dotenv, find_dotenv
from linkedin_api.clients.restli.client import RestliClient
from .poll import delete_posted_poll, get_chat_message, get_options, filter_options, globalMessages, get_poll_data, pick_poll_more_than_7_days


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

load_dotenv(find_dotenv())

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if ACCESS_TOKEN is None:
    raise Exception(
        'A valid access token must be defined in the /examples/.env file under the variable name "ACCESS_TOKEN"'
    )

ME_RESOURCE = "/me"
UGC_POSTS_RESOURCE = "/ugcPosts"
POSTS_RESOURCE = "/posts"
API_VERSION = "202302"

restli_client = RestliClient()
restli_client.session.hooks["response"].append(lambda r: r.raise_for_status())


def getPollOptions(options):
    conduct_options = []
    for option in options:
        conduct_options.append({
            "text": option
        })
    return conduct_options


def create_linkedin_poll():
    message = get_chat_message()
    print("message:", message)
    linkedin_topic = message.get('topic')
    linkedin_title = message.get('poll_name')
    options, hasLongLength = get_options(message, 30)

    if hasLongLength == 1:
        options = filter_options(options)
    elif hasLongLength >= 2:
        globalMessages.append({
            "role": "user",
            "content": "Generate a new one"
        })
        create_linkedin_poll()
        print("hasLongLength:", hasLongLength)

    print("new_options:", options)
    linkedin_options = getPollOptions(options)
    print("linkedin_options:", linkedin_options)
    """
    Calling the /me endpoint to get the authenticated user's person URN
    """
    me_response = restli_client.get(
        resource_path=ME_RESOURCE, access_token=ACCESS_TOKEN)
    print(f"Successfully fetched profile: {json.dumps(me_response.entity)}")

    """
    Calling the legacy /ugcPosts API to create a text post on behalf of the authenticated member
    """
    # ugc_posts_create_response = restli_client.create(
    #     resource_path=UGC_POSTS_RESOURCE,
    #     entity={
    #         "author": f"urn:li:person:{me_response.entity['id']}",
    #         "lifecycleState": "PUBLISHED",
    #         "specificContent": {
    #             "com.linkedin.ugc.ShareContent": {
    #                 "shareCommentary": {
    #                     "text": "Sample text post created with /ugcPosts API"
    #                 },
    #                 "shareMediaCategory": "NONE",
    #             }
    #         },
    #         "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    #     },
    #     access_token=ACCESS_TOKEN,
    # )
    # print(
    #     f"Successfully created post using /ugcPosts: {ugc_posts_create_response.entity_id}"
    # )

    """
    Calling the newer, more streamlined (and versioned) /posts API to create a text post on behalf
    of the authenticated member
    """
    posts_create_response = restli_client.create(
        resource_path=POSTS_RESOURCE,
        entity={
            "author": f"urn:li:person:{me_response.entity['id']}",
            "commentary": f"{linkedin_title} \nsubsKribe to me on YouTube: https://lnkd.in/gxw3deeN \n#{linkedin_topic.replace(' ', '')}",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
            "content": {
                "poll": {
                    "question": " ",
                    "options": linkedin_options,
                    "settings": {"duration": "SEVEN_DAYS"}
                }
            }
        },
        version_string=API_VERSION,
        access_token=ACCESS_TOKEN,
    )
    print(
        f"Successfully created post using /posts: {posts_create_response.entity_id}")


def post_linkedin_poll():
    polls = get_poll_data("linkedin")
    print("polls:", polls)
    poll = pick_poll_more_than_7_days(polls)
    print("poll:", poll)
    linkedin_topic = poll.get('topic')
    linkedin_title = poll.get('title')
    options, hasLongLength = get_options(poll, 30)

    if hasLongLength == 1:
        options = filter_options(options)
    elif hasLongLength >= 2:
        post_linkedin_poll()

    print("new_options:", options)
    linkedin_options = getPollOptions(options)
    print("linkedin_options:", linkedin_options)
    """
    Calling the /me endpoint to get the authenticated user's person URN
    """
    me_response = restli_client.get(
        resource_path=ME_RESOURCE, access_token=ACCESS_TOKEN)
    print(f"Successfully fetched profile: {json.dumps(me_response.entity)}")
    """
    Calling the newer, more streamlined (and versioned) /posts API to create a text post on behalf
    of the authenticated member
    """
    posts_create_response = restli_client.create(
        resource_path=POSTS_RESOURCE,
        entity={
            "author": f"urn:li:person:{me_response.entity['id']}",
            "commentary": f"{linkedin_title} \nsubsKribe to me on YouTube: https://lnkd.in/gxw3deeN \n#{linkedin_topic.replace(' ', '')}",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
            "content": {
                "poll": {
                    "question": " ",
                    "options": linkedin_options,
                    "settings": {"duration": "SEVEN_DAYS"}
                }
            }
        },
        version_string=API_VERSION,
        access_token=ACCESS_TOKEN,
    )
    print(
        f"Successfully created post using /posts: {posts_create_response.entity_id}")
    delete_posted_poll(poll)
