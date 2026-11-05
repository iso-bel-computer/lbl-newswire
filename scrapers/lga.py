from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.select('div[class="news__body"]')

    for item in items:


        itemData = {
            "title":        item.find('h2').text.strip(),
            "url":         'https://www.local.gov.uk' + item.find('a', href=True)['href'],
            "description":  item.find('p').text,
            "category": scraper['category'],
            "date":         item.find('time').text,
            "source":       scraper["name"]
        }

        articles.append(itemData)



    return articles
