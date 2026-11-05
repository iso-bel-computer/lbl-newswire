#!/usr/bin/env python3

#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='card-news')

    for item in items:

        itemData = {

            "title": item.find(class_="primary-info").text.strip(),
            "url": "https://committees.parliament.uk" + item['href'],
            "category": scraper['category'],
            "date": item.find(class_='info-inner').text.strip(),
            "description": item.find(class_='text').text,
            "source": scraper["name"]
        }

        articles.append(itemData)


    return articles
