#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import json
import argparse
import sys
from shutil import copyfile
import time
import os

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from io import BytesIO

archive_text = "metadata.txt"
archive_final_image = "final_image.png"

def make_or_cleanup(local_dir):
    # make output directory if it is not there
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # and clean it out if it is there
    filelist = [ f for f in os.listdir(local_dir) ]
    for f in filelist:
        os.remove(os.path.join(local_dir, f))

def archive_post(subdir, post_image, post_text, archive_dir="archives"):
    # setup paths
    archive_dir = "{}/{}".format(archive_dir, subdir)
    archive_text_path = "{}/{}".format(archive_dir, archive_text)
    archive_final_image_path = "{}/{}".format(archive_dir, archive_final_image)

    # prepare output directory
    make_or_cleanup(archive_dir)

    # save metadata
    with open(archive_text_path, 'ab') as f:
        # might be unicode. what a PITA
        f.write(u'\t'.join([u"post_text", post_text]).encode('utf-8').strip())

    # save input, a few working files, outputs
    copyfile(post_image, archive_final_image_path)

def run_tweet_code(source_html, timeout):
    params = '--web-security=no'
    driver = webdriver.PhantomJS(service_args=[params])
    driver.set_window_size(440, 220) # optional
    driver.get(source_html)
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#render_ready")))
    except TimeoutException:
        print("Timeout waiting for page load")
        print(driver.get_log("browser"))
        return None
    img = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img))
    cropped = img.crop((0,0,440,220))
    cropped.save('temp/image.png')

    elem = driver.find_element_by_css_selector('#tweet_text')
    return elem.get_attribute('innerHTML')

last_index_file = "temp/last_index.txt"
def run_swaplist(swaplist, sourcedir):
    try:
        with open(last_index_file) as f:
            content = f.readlines()
            last_index = int(content[0])
    except EnvironmentError: # parent of IOError, OSError
        # that's ok
        print("No record of last index ({}), will create".format(last_index_file))
        last_index = -1
    cur_index = last_index + 1
    if cur_index >= len(swaplist):
        cur_index = 0
    record = swaplist[cur_index]

    command = "cd {} && git pull".format(record["subdir"])
    os.system(command)

    command = "cp {}/* {}/.".format(record["subdir"], sourcedir)
    os.system(command)

    os.system("cp example/index.html {}/.".format(sourcedir))
    os.system("cp example/sketch.js {}/.".format(sourcedir))
    os.system("cp example/focusedRandom.js {}/.".format(sourcedir))
    os.system("cp example/.purview_helper.js {}/.".format(sourcedir))

    if os.path.isfile(last_index_file):
        copyfile(last_index_file, "{}.bak".format(last_index_file))
    with open(last_index_file, "w") as f:
        f.write("{}\n".format(cur_index))
    return record["name"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Post beeps to timeline')
    parser.add_argument('-d','--debug', help='Debug: do not post', default=False, action='store_true')
    parser.add_argument('-s', '--sourcedir', dest='sourcedir', default='example',
                        help="Source html to run")
    parser.add_argument('-c','--creds', dest='creds', default='creds.json',
                        help='Twitter json credentials.')
    parser.add_argument('--swaplist', dest='swaplist', default=None,
                        help='Run swap settings json list')
    parser.add_argument("--archive-subdir", dest='archive_subdir', default=None,
                        help="specific subdirectory for archiving results")
    parser.add_argument('-t', "--timeout", dest='timeout', type=int, default=20,
                        help="timeout for running tweet")
    args = parser.parse_args()

    swaplist_name = None
    if args.swaplist is not None:
        with open(args.swaplist) as data_file:
            swaplist = json.load(data_file)
            swaplist_name = run_swaplist(swaplist, args.sourcedir)
            print("Swapped in bot from {}".format(swaplist_name))

    source_url = "{}/index.html".format(args.sourcedir)
    tweet_status = run_tweet_code(source_url, args.timeout)
    if tweet_status is None:
        status = "(timeout)"
    else:
        status = tweet_status
    if swaplist_name is not None:
        status = "{} ({})".format(status, swaplist_name)

    if args.debug:
        print("Status is: {}".format(status))
        sys.exit(0)

    with open(args.creds) as data_file:
        creds = json.load(data_file)

    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])

    api = tweepy.API(auth)

    try:
        if tweet_status is None:
            # Error, no image
            api.update_status(status=status)
        else:
            api.update_with_media(filename='temp/image.png', status=status)
    except tweepy.error.TweepError as e:
        now_string = time.strftime("%Y%m%d_%H%M%S")
        new_status = "{} [{}]".format(e["message"], now_string)
        if swaplist_name is not None:
            new_status = "{} ({}) [now_string]".format(new_status, swaplist_name)
        api.update_status(status=new_status)

    if args.archive_subdir:
        archive_subdir = args.archive_subdir
    else:
        archive_subdir = time.strftime("%Y%m%d_%H%M%S")
    archive_post(archive_subdir, post_image='temp/image.png', post_text=status)

    print(u"Posted: {}".format(status))

