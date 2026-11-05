#!/usr/bin/env python3
import json

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='grid-item-cont')

    for item in items:

        itemData = {
            "title": item.find('h2').text,
            "url": item.find('a')['href'],
            "date": item.find(class_='published').text,
            "description": '',
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
