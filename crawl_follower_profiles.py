#!/usr/bin/env python3

"""Crawls all followers of a user and extracts profile informations of them.
"""
import json
import sys
from instapy import InstaPy
from instapy import smart_run
from util.settings import Settings

# instagram-profilecrawl imports
from util.chromedriver import SetupBrowserEnvironment
from util.datasaver import Datasaver
from util.extractor import extract_information

# login credentials
with open('credentials.json', 'r') as f:
    credentials = json.load(f)
insta_username = credentials['username']
insta_password = credentials['password']

# get followers of this user
username = sys.argv[1]

# crawl user profiles
def crawl_profile(usernames):
    with SetupBrowserEnvironment() as browser:
        for username in usernames:
            print('Extracting information from ' + username)
            information, user_commented_list = extract_information(browser, username, Settings.limit_amount)
            Datasaver.save_profile_json(username, information.to_dict())
            print ("Number of users who commented on their profile is ", len(user_commented_list),"\n")

# get an InstaPy session
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True, geckodriver_path="assets/geckodriver.exe")

with smart_run(session):
    followers = session.grab_followers(username=username, amount="full", live_match=True, store_locally=True)
    print("Found a total of {} followers:".format(len(followers)))
    print(followers)

crawl_profile(followers)
