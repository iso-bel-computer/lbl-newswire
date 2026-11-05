#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='card--index')

    for item in items:

        itemData = {

            "title": item.find(class_='card__title').text.strip(),
            "url": "https://homeless.org.uk" + item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find(class_='news-item__date').text.strip(),
            "description": item.find(class_='card__blurb').text.strip(),
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
