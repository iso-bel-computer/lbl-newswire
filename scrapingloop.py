import sys
import json
import requests
import dateparser
import datetime
import traceback
import importlib
# booting selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def scrapeWebsites(log):

    with open("./config/sacrpingCONFIG.json") as f:
        scrapers = json.load(f)

    headers = {"User-Agent": "PolicyDashboard/1.0 (izzy@iso-bel.computer)"}
    scrapedArticles = []

    driver = None

    try:
        for scraper in scrapers:

            try:
                spec = importlib.util.spec_from_file_location(scraper['shortname'], scraper['path'])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if scraper['type'] == 'selenium':

                    if driver is None:
                        options = Options()
                        options.add_argument("-headless")
                        options.add_argument("--width=1920")
                        options.add_argument("--height=1080")
                        driver = webdriver.Firefox(options=options)

                    driver.get(scraper['url'])
                    articles = module.scrape(driver.page_source, scraper)

                elif scraper['type'] == 'standard':

                    page = requests.get(scraper['url'], headers=headers, timeout=20)

                    if page.status_code != 200:
                        raise Exception(f'Bad status code for {scraper["name"]}: {page.status_code}')

                    articles = module.scrape(page, scraper)

                else:
                    raise Exception(f'Unknown scraper type for {scraper["name"]}: {scraper["type"]}')

                scrapedArticles.extend(articles)

                if len(articles) < 1:
                    raise Exception(f"No articles found for {scraper['name']}")

            except Exception as e:

                log[scraper['name']] = {
                    "fetched": 0,
                    "new": 0,
                    "error": str(e)
                }

                traceback.print_exc()

    finally:
        if driver is not None:
            driver.quit()

    return scrapedArticles
