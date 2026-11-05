#!/usr/bin/env python3

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='views-row')

    for item in items:

        itemData = {

            "title": item.find('h3').text.strip(),
            "url": "https://www.londoncouncils.gov.uk" + item.find('a', href=True)['href'],
            "category": scraper['category'],
            "date": item.find_all('div', attrs={"class":"field--type-datetime"})[0].text,
            "description": item.find_all('div', attrs={"class":"field--name-body"})[0].text,
            "source": scraper["name"]

        }

        articles.append(itemData)


    return articles
