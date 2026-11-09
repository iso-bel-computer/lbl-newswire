#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    json_response = json.loads(page.text)
    articles = []

    for item in json_response['items']:
        soup = BeautifulSoup(item['markup'], 'html.parser')

        itemData = {

            "title": soup.find("h3").text.strip(),
            "url": 'https://www.jrf.org.uk' + soup.find('a')['href'],
            "category": scraper['category'],
            "date": soup.find('time').text.strip(),
            "description": soup.find('p').text.strip(),
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
