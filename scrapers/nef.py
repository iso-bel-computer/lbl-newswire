#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='morepanel')

    for item in items:

        ptags = item.find_all('p')
        itemData = {

            "title": item.find("h4").text.strip(),
            "url": item.find('a')['href'],
            "category": scraper['category'],
            "date": item.find(class_='list-dateline').text.strip(),
            "description": ptags[1].text,
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
