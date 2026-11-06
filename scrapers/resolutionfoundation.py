#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:


        title = item.find(class_='entry-title').text.strip()
        subtitle = item.find(class_='sub-title')

        if subtitle:
            title = title + ' - ' + subtitle.text.strip()

        summary = item.find(class_='entry-summary')
        if summary:
            summary = summary.text.strip()
        else:
            summary = ''


        itemData = {

            "title": title,
            "url": item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find('time').text.strip(),
            "description": summary,
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
