#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:

        try:
            itemData = {

                "title": item.find("h4").text.strip(),
                "url": item.find('a')['href'],
                "category": scraper['category'],
                "date": item.find(class_='elementor-post-date').text.strip(),
                "description": item.find(class_='elementor-post__excerpt').text.strip(),
                "source": scraper["name"]
            }

            articles.append(itemData)

        except: # a little hacky - 'articles' returns the cookies prompt as well??
            continue


    return articles
