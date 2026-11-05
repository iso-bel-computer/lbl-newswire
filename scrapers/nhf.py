#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='news-item')

    for item in items:

        date = "Unknown"
        datepieces = None
        dateDiv = None
        ptags = item.find_all('p')

        if ptags:
            if len(ptags) > 1:
                dateDiv = ptags[1]

        if dateDiv:
            datepieces = dateDiv.text.split(',')

        if datepieces:
            if len(datepieces) > 1:
                date = datepieces[1]
            else:
                date = datepieces[0]

        itemData = {

            "title": item.find('h3').text.strip(),
            "url": "https://www.housing.org.uk" + item['href'],
            "category": scraper['category'],
            "date": date,
            "description": item.find_all('p')[0].text,
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
