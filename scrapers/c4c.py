
#!/usr/bin/env python3

from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all('article')

    for item in items:

        itemData = {
            "title": item.find('a')['title'],
            "description": item.find(class_="c-card__excerpt ts-small").text.strip(),
            "date": item.find(class_='c-card-meta__date').text,
            "source": scraper['name'],
            "category": scraper['category'],
            "url":  item.find('a', href=True)['href']
        }

        articles.append(itemData)

    return articles
