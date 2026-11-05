#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='item-inner')

    for item in items:

        itemData = {

            "title": item.find('h3').text.strip(),
            "url": "https://www.crisis.org.uk" + item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find(class_='info-tab').text.strip(),
            "description": item.find(class_='item-body').text,
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
