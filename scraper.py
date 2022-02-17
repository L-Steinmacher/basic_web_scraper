#!/usr/bin/env python3

import argparse
import time

from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

parser = argparse.ArgumentParser(description='Insert a URL')
parser.add_argument('url', type=str, nargs=1,
                    help='try URL: https://status.uptimerobot.com/778224451, https://stats.uptimerobot.com/Q5ogPt6JAQ/787944757 or https://stats.uptimerobot.com/Q5ogPt6JAQ/785837216')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-m", "--minimum", action="store_true",
                    help="shows the minimum ping")
parser.add_argument("-a", "--average", action="store_true",
                    help="shows the average ping")
args = parser.parse_args()
url = vars(args)["url"][0]

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# We wait for the page to load
time.sleep(5)
page_source = driver.page_source
soup = BeautifulSoup(page_source, features="xml")

heading = soup.find("span", class_="uk-display-inline-block")

# Grab all the data points
points = soup.find_all(class_="ct-point")

# Touples containing the data of ping and date from the meta
highest = (0, "")
min = (float("inf"), "")

count= 0
total = 0

for point in points:
    value = float(point.get("ct:value"))
    meta = point.get("ct:meta")
    count += 1
    total += value
    if value > highest[0]:
        highest = (value, meta)
    if value < min[0]:
        min = (value, meta)

average = round(total / count, 2)

if args.verbose:
    print(f"{heading.text} recieved Highest ping: {highest[0]}ms on {highest[1]}, Min: {min[0]}ms on {min[1]}, and the Average: {average}ms on {date.today()}.")
elif args.minimum:
    print(f"{heading.text} Lowest Ping {min[0]}ms on {min[1]} ")
elif args.average:
    print(f"The average Ping for {heading.text} is {average}ms as of {date.today()}")
else:
    print(f"{heading.text} Highest Ping {highest[0]}ms on {highest[1]}")

