import requests
import sqlite3
import pprint
import os
import random
from instagrapi import Client
from datetime import datetime
from image_generator.generate_image import generate_image
from dotenv import load_dotenv

# Load .env file, if present

load_dotenv()

DRY_RUN_ENABLED=True

PATH_FOLDER_BASE_IMAGES = os.path.abspath("folder_base_images")
PATH_FOLDER_GENERATED_IMAGES = os.path.abspath("folder_generated_images")

COMFUCIUS_GET_PHRASE_PUBLIC_API_URL = 'https://comfucius.xyz/quotes/api/get-fake-quote'

INSTAGRAM_USERNAME=os.environ.get('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD=os.environ.get('INSTAGRAM_PASSWORD')

INSTAGRAM_POST_GOOD_WORD_LIMIT=20
INSTAGRAM_POST_BAD_WORD_LIMIT=2

def get_instagram_post_caption(good_word_limit, bad_word_limit):
    '''
    Get instagram caption concatenating a series of "good word" hashtags (e.g. philosophy, love)
    and a series of "bad" ones (e.g. atomicbomb, backache)
    '''

    sqlite_db = sqlite3.connect("database.sqlite")

    hashtags_good = []
    hashtags_bad = []

    output_obj = sqlite_db.execute("SELECT word FROM hashtag WHERE type == 'good' ORDER BY RANDOM() LIMIT "+str(good_word_limit))

    for single_row in output_obj.fetchall():
        hashtags_good.append('#'+single_row[0])

    output_obj = sqlite_db.execute("SELECT word FROM hashtag WHERE type == 'bad' ORDER BY RANDOM() LIMIT "+str(bad_word_limit))

    for single_row in output_obj.fetchall():
        hashtags_good.append('#'+single_row[0])

    return (f'{" ".join(hashtags_good)}{" ".join(hashtags_bad)}')

def post_photo_on_instagram(image_path, post_caption, accessibility_caption):
    '''
    Post a .jpg image on instagram as a photo post. Use data generated early
    Instaclient doc URL: https://adw0rd.github.io/instagrapi/usage-guide/media.html

    If "dry run", don't post anything on insta, just print info locally
    '''

    if DRY_RUN_ENABLED is True:

        # Avoid actual posting on Instagram
        pprint.pprint(locals())

    else:

        instaclient = Client()
        instaclient.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

        media = instaclient.photo_upload(
            image_path,
            post_caption,
            extra_data={
                "custom_accessibility_caption": accessibility_caption,
            }
        )

        pprint.pprint(media.dict())

if __name__ == "__main__":

    # Get phrase from Comfucius

    comfucius_phrase_data = requests.get(COMFUCIUS_GET_PHRASE_PUBLIC_API_URL).json()
    comfucius_complete_quote = f'{comfucius_phrase_data["Phrase"]} ~ {comfucius_phrase_data["Thinker"]}'
    
    # Generate a .jpg photo, using a random base image
    
    background_image_filename=random.choice(os.listdir(PATH_FOLDER_BASE_IMAGES))
    background_image_filepath=PATH_FOLDER_BASE_IMAGES + os.sep + background_image_filename

    generated_image_filename_no_extension = f'generated_image___{datetime.utcnow().strftime("%Y-%m-%d_%I-%M-%S_%p")}'

    generated_image_path = generate_image(
        background_image_filepath, 
        PATH_FOLDER_GENERATED_IMAGES, 
        generated_image_filename_no_extension,
        comfucius_complete_quote
    )

    # Generate a cool caption

    generated_post_caption = get_instagram_post_caption(
        good_word_limit=INSTAGRAM_POST_GOOD_WORD_LIMIT, 
        bad_word_limit=INSTAGRAM_POST_BAD_WORD_LIMIT
    )

    # Post on Instagram, if "DRY_RUN_ENABLED" is True

    post_result_info = post_photo_on_instagram(
        image_path=generated_image_path,
        post_caption=generated_post_caption,
        accessibility_caption=comfucius_complete_quote
    )

    print(f"Post done! Date: {datetime.now()}")

    # Delete the used .jpg photo, if "DRY_RUN_ENABLED" is False

    if DRY_RUN_ENABLED is False:

        os.remove(generated_image_path)