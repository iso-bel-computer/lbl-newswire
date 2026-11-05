from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.find_all(class_='listpageitem', href=True)

    for item in items:
        link = item['href']
        header = item.find('h3').text
        description = item.find('p').text
        date = item.find(class_='date').text

        # filter out results abt northern ireland
        if 'ireland' not in header.lower():

            itemData = {
                "title": header,
                "description": description,
                "url": link,
                "source": scraper["name"],
                "category": scraper['category'],
                "date": date
            }

            articles.append(itemData)


    return articles
