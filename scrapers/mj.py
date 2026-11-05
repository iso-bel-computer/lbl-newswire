#!/usr/bin/env python3

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.select('div[class^="secondary-content"]')

    for item in items:


        title = item.find(class_='headline')
        url = "https://www.themj.co.uk" + title.find('a', href=True)['href']
        itemData = {
            "title": title.text,
            "url": url,
            "date": item.find('h6').text.split('|')[1].strip(),
            "description": item.find('p').text,
            "category": scraper['category'],
            "source": scraper["name"],
        }

        articles.append(itemData)


    return articles
