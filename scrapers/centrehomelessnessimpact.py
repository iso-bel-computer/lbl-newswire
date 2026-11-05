#!/usr/bin/env python3

import json

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    main = soup.find(class_='news-main')
    items = main.find_all(class_='column')

    for item in items:
        ptags = item.find_all('p')

        itemData = {
            "title": item.find('h4').text,
            "url": "https://www.homelessnessimpact.org" + item.find('a')['href'],
            "date": ptags[0].text,
            "description": ptags[1].text,
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
