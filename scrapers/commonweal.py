#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='gallery-item-container')

    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    for item in items:

        if not has_numbers(item.find(class_='time-ago').text):
            continue # some items written as '8 hrs ago' (eg) - so we ignore them
                    # so that it doesnt break the parser

        itemData = {

            "title": item.find('h2').text.strip(),
            "url": item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find(class_='post-metadata__date').text.strip(),
            "description": item.find(class_='blog-post-description-style-font').text,
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
