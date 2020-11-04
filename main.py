# selenium imports
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

# dotenv
from dotenv import load_dotenv

# time and datetime
import time
from datetime import datetime

# other imports
import os
import sys
import getopt
import requests
from urllib.parse import urlparse

def print_help(message = ""):
    if message != "":
        print("Error: {}".format(message))
    print("python3 main.py -dt [day of month]-[month]-[year]#[hour]:[minute]:[second] -u [valid zoom meeting url]")
    exit(0)

load_dotenv()

if not os.getenv("USER_DATA_DIR"):
    print("Please set the USER_DATA_DIR in the .env first before using the application")
    exit(0)

now = time.time()

opts, _ = getopt.getopt(sys.argv[1:], "dt:hu:", ["datetime=", "help=","url="])

target = -1
url = ""

for k, v in opts:
    if k == "-h" or k == "--help":
        print_help()
    if k == "-dt" or k == "--datetime":
        try:
            target = datetime.strptime(v, "%d-%m-%Y#%H:%M:%S").timestamp()
        except ValueError as e:
            print_help("Format doesn't right")
    if k == "-u" or k == "--url":
        try:
            requests.get(v)
        except requests.ConnectionError as identifier:
            print_help("Please input a valid url")
        domain = urlparse(v).netloc
        if domain[-8:] != ".zoom.us":
            print_help("Please provide a valid zoom meeting url")
        url = v
    
            

if target == -1:
    print_help("-dt or --datetime argument is required")

if url == "":
    print_help("-u or --url argument is required")

diff = target-now
if diff < 0:
    print_help("Target cannot be less than current date and time")

print("Please wait until inputted date and time...")
time.sleep(diff)
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=./{}".format(os.getenv("USER_DATA_DIR")))
options.add_argument("profile-directory={}".format(os.getenv("PROFILE_DIRECTORY")))


try:
    browser = Chrome(options=options)
except InvalidArgumentException as e:
    print("Please check if the profile directory already created")
    exit(0)
browser.get(url)
browser.close()
print("Browser closed successfully")