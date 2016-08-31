#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import json
import argparse
import sys

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO

def run_tweet_code():
    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(440, 220) # optional
    driver.get('example/index.html')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#render_ready")))
    img = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img))
    cropped = img.crop((0,0,440,220))
    cropped.save('temp/image.png')

    elem = driver.find_element_by_css_selector('#tweet_text')
    return elem.get_attribute('innerHTML')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Post beeps to timeline')
    parser.add_argument('-d','--debug', help='Debug: do not post', default=False, action='store_true')
    # parser.add_argument('-m','--mode', help='mode: [text|image|images]', default="text")
    args = parser.parse_args()

    status = run_tweet_code()

    if args.debug:
        print("Status is: {}".format(status))
    else:    
        with open('creds.json') as data_file:    
            creds = json.load(data_file)

        auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
        auth.set_access_token(creds["access_token"], creds["access_token_secret"])

        api = tweepy.API(auth)

        api.update_with_media(filename='temp/image.png', status=status)
