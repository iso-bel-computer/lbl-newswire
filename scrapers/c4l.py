#!/usr/bin/env python3
import json

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:

        br = item.find('br')
        if br:
            date = br.previous_sibling.text
        else:
            date = None

        itemData = {
            "title": item.find(class_='content-tile__title').text,
            "url": item.find('a')['href'],
            "date": date,
            "description": item.find('a').text,
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
