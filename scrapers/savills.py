#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:

        try:
            itemData = {

                "title": item.find("h3").text.strip(),
                "url": 'https://www.savills.co.uk' +  item.find('a')['href'],
                "category": scraper['category'],
                "date": item.find('time').text.strip(),
                "description": item.find(class_='sv--quote').text.strip(),
                "source": scraper["name"]
            }

            articles.append(itemData)

        except: # a little hacky - 'articles' returns the cookies prompt as well??
            continue


    return articles
