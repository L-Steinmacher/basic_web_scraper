#!/usr/bin/env python3

import argparse
import time

from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scraper(url):
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

    print(f"{heading.text} recieved Highest ping of {highest[0]} on {highest[1]}, Min was {min[0]} on {min[1]} and the Average is: {average} on {date.today()}.")

parser = argparse.ArgumentParser(description='Insert a URL')
parser.add_argument('url', type=str, nargs=1,
                    help='try URL: https://status.uptimerobot.com/778224451')
arg = parser.parse_args()
url = vars(arg)["url"][0]
scraper(url)