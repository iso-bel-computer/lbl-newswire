#!/usr/bin/env python3

import json

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    main = soup.find('main')
    items = main.find_all('li')

    for item in items:
        print(item)

        itemData = {
            "title": item.find('h3').text,
            "url": "https://www.theguardian.com" + item.find('a')['href'],
            "date": item.find('footer').text,
            "description": '',
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
