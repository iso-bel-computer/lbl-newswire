#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='news-article')

    for item in items:

        itemData = {

            "title": item.find("h3").text.strip(),
            "url": 'https://www.nrla.org.uk' + item['href'],
            "category": scraper['category'],
            "date": item.find(class_='news-article-meta-date').text.strip(),
            "description": '',
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
