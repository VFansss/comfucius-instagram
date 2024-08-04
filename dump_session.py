import os
from instagrapi import Client
from dotenv import load_dotenv

# Load .env file, if present

load_dotenv()

INSTAGRAM_USERNAME=os.environ.get('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD=os.environ.get('INSTAGRAM_PASSWORD')

if __name__ == "__main__":

    # Dump a valid user session
    # Straight from official Instagrapi documentation:
    # https://subzeroid.github.io/instagrapi/usage-guide/best-practices.html

    cl = Client()
    cl.login('comfucius_official', '5upzkPPkSAb8vDR')
    cl.dump_settings("session.json")