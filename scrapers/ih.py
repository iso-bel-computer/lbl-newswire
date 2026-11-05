#!/usr/bin/env python3
#
from bs4 import BeautifulSoup
import re

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.select('div[class^="aos-SHC"]')

    for item in items:

        itemData = {
            "title": item.find('h2'),
            "description": '',
            "url": item.find('a', href=True)['href'],
            "category": scraper['category'],
            "source": scraper["name"],
            "date": item.select_one('span[class*="aos-ArticleDate"]')


        }

        if itemData['date']:
            itemData["date"] = itemData["date"].text
            if itemData['title']:
                itemData["title"] = itemData['title'].text
                articles.append(itemData)


    return articles
