from bs4 import BeautifulSoup

def scrape(page, scraper):

    soup = BeautifulSoup(page.text, 'html.parser')
    articles = []

    items = soup.select('div[class^="padded-box"]')

    for item in items:

        itemData = {
            "title": item.find('h2').text,

            "category": scraper['category'],

            "description": item.find('p').text,
            "url": 'https://england.shelter.org.uk' + item.find('a', href=True)['href'],
            "source": scraper["name"]
        }

        date_el = item.select_one('p[class*="PostedDate"]')

        if date_el:
            # Use .get_text() before you .replace()
            itemData["date"] = date_el.get_text().replace('Published:', '').replace('Last updated:','').strip()
        else:
            itemData["date"] = "No date found"

        articles.append(itemData)



    return articles
