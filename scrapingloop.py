import importlib.util
import sys
import json
import requests
import dateparser
import datetime
import traceback

def scrapeWebsites(log):

    with open("./config/sacrpingCONFIG.json") as f:
        scrapers = json.load(f)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    headers = {"User-Agent": "PolicyDashboard/1.0 (izzy@iso-bel.computer)"}
    scrapedArticles = []

    for scraper in scrapers:

        try:
            spec = importlib.util.spec_from_file_location(scraper['shortname'], scraper['path'])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print(f"fetching {scraper['url']}")
            page = requests.get(scraper['url'], headers=headers, timeout=20)

            if page.status_code != 200:
                raise Exception(f'Bad status code for {scraper["name"]}: {page.status_code}')

            articles = module.scrape(page, scraper)

            for article in articles:
                scrapedArticles.append(article)

            print(f"Scraper - Fetched {len(articles)} from {scraper['name']}")

        except Exception as e:
            log[scraper['name']] = {
                "fetched": 0,
                "new": 0,
                "error": str(e)
            }

            traceback.print_exc()

    return scrapedArticles
