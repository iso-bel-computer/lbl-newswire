#!/usr/bin/env python3

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    newsSection = soup.find('main')
    items = newsSection.find_all(class_='card-body')

    for item in items:

        itemData = {
            "title": item.find('h3').text,
            "url": item.find('a')['href'],
            "date": item.find('time').text,
            "description": item.find('a').text,
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
