from bs4 import BeautifulSoup
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
import requests
import feedparser
import json
import dateparser
import time
from scrapingloop import scrapeWebsites
from pathlib import Path
import sqlite3
from datetime import datetime

sqliteConnection = sqlite3.connect("./data/articles.db")
cursor = sqliteConnection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
sqliteConnection.commit()

BASE_DIR = Path(__file__).resolve().parent

articleTableSchema = "CREATE TABLE IF NOT EXISTS articles (\n    article_id INTEGER PRIMARY KEY,\n title TEXT,\n url TEXT UNIQUE,\n summary TEXT,\n year TEXT,\n month TEXT,\n day TEXT,\n source TEXT\n, category TEXT\n, relevant TEXT\n)"
cursor.execute(articleTableSchema)

# Create a 'zero' time structure (Jan 1, 1970) to use as a fallback
epoch_time = time.gmtime(0)

fetchedArticles = 0

def addArticle(title, url, summary, year, month, day, source, category):
    global fetchedArticles
    fetchedArticles = fetchedArticles + 1

    cursor.execute("""
        SELECT * from articles
        WHERE title = ?
        AND day = ?
    """, (title, day))

    alreadyIn = cursor.fetchall()

    if len(alreadyIn) < 1:
        relevance = getRelevanceScore(f"From {source} - {title} - {summary}")
        cursor.execute("""
        INSERT OR IGNORE INTO articles (title, url, summary, year, month, day, date, source, category, relevance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, url, summary, year, month, day, f"{year}-{month}-{day}" , source, category, relevance))
        sqliteConnection.commit()

        return True

    return False


with open("./newsSrc/livenews.json") as f:
    liveNews = json.load(f)

def getRelevanceScore(assessingText):

    client = TypeSafeClient(api_key='local', base_url = 'http://127.0.0.1:8765')
    response = client.system_one(
        state=assessingText,
        questions={
            "relevance": Score(
            instructions=(
                "Rate how relevant this article is to the housing policy team at "
                "Lewisham Council (a London borough). The team cares about social and "
                "affordable housing, temporary accommodation and homelessness, "
                "renters' rights and private rented sector regulation, planning and "
                "development, building safety, and housing funding or legislation."
            ),
            criteria=[
                "Irrelevant - not about housing, or only mentions housing in passing, or is specifically about a different local authority.",
                "Somewhat relevant - housing policy or news elsewhere in the UK, or general local government news touching on housing.",
                "Very relevant - new national housing legislation, policy, or funding, announcement of a consultation or anything that directly names Lewisham or London boroughs' housing duties.",
            ],
        )}
    )


    return response.answers['relevance'].score



log = {}
SCRAPEDARTICLES = scrapeWebsites(log)


def normaliseDate(datestr):
    if not datestr:
        return None
    dateObj = dateparser.parse(datestr.strip(), settings={'DATE_ORDER': 'DMY'})
    if not dateObj:
        return None
    cleanDate = {
        "year": dateObj.strftime('%Y'),
        "month": dateObj.strftime('%m'),
        "day": dateObj.strftime('%d'),
        }
    return cleanDate


def logarticle(source, new):

    if not log.get(source):
        log[source] = {
            "fetched": 0,
            "new": 0,
            "error": None
        }


    log[source]['fetched'] += 1
    if new:
        log[source]['new'] += 1



for entry in SCRAPEDARTICLES:

    date = normaliseDate(entry['date'])
    if not date:
        date = {'year': 00, 'month': 00, 'day': 00}

    articleIsNew = addArticle(
        entry['title'],
        entry['url'],
        entry['description'],
        date['year'],
        date['month'],
        date['day'],
        entry['source'],
        entry['category']
    )

    logarticle(entry['source'], articleIsNew)


for source in liveNews:

    # Get the feed
    feed = feedparser.parse(source['url'])

    for entry in feed.entries:
        entryIsNew = addArticle(
            entry.title,
            entry.link,
            entry.summary,
            entry.updated_parsed.tm_year,
            entry.updated_parsed.tm_mon,
            entry.updated_parsed.tm_mday,
            source['name'],
            source['category']
        )

        logarticle(source['name'], entryIsNew)




now = datetime.now().strftime("%y-%m-%d - %H:%M")
shortnow = datetime.now().strftime("%b-%d")

try:
    with open('/home/izzy/logs/izzylog', 'a') as izzylog:
        izzylog.write(f"{shortnow} - Ran Policy Scraper.\n")
except:
    print("Unable to open izzylog")

for key, item in log.items():
    LOGS_PATH = BASE_DIR / "logs" / key
    ERRORLOG_PATH = BASE_DIR / "logs" / 'ERRORS'
    with open(LOGS_PATH, 'a') as f:
        f.write(f"{now} - {key} | {item['fetched']} Fetched - {item['new']} New{ ' - ' + item['error'] if item.get('error') else ''} \n")

    if item.get('error'):
        try:
            with open('/home/izzy/logs/izzylog', 'a') as izzylog:
                izzylog.write(f"{shortnow} - Error fetching {key} - {item['error']}\n")
        except:
            print(f"Error fetching {key} - {item['error']} (and unable to open izzylog)")

        with open(ERRORLOG_PATH, 'a') as errorlog:
            errorlog.write(f"{now} - Error fetching {key} - {item['error']}\n")

sqliteConnection.commit()
sqliteConnection.close()
