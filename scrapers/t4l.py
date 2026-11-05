#!/usr/bin/env python3

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.select('li[class^="news-index-page__item"]')

    for item in items:


        itemData = {
            "title": item.find('h3').text,
            "description": '',
            "date": item.find('p').text,
            "source": scraper['name'],
            "category": scraper['category'],
            "url": 'https://trustforlondon.org.uk' + item.find('a', href=True)['href']
        }

        articles.append(itemData)

    return articles
