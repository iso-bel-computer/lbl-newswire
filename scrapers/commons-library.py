#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:
        print(item)

        title = item.find('h2')
        if not title:
            title = item.find('h4')

        date = item.find(class_='card__date')

        itemData = {

            "title": title.text.strip(),
            "url": item.find('a')['href'],
            "category": scraper['category'],
            "date": date.text.strip(),
            "description": date.findNext('p').text.strip(),
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
