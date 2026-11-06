#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all('section')

    for item in items:

        itemData = {

            "title": item.find("a").text.strip(),
            "url": "https://www.housinglin.org.uk" + item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find('time').text.strip(),
            "description": item.find('p').text,
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
