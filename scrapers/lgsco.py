#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    news = soup.find(class_='news')
    items = news.find_all(class_='clearfix')

    for item in items:

        itemData = {

            "title": item.find('a').text.strip(),
            "url": "https://www.lgo.org.uk" + item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find(class_='date').text.strip(),
            "description": '',
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
