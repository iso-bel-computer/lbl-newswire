from flask import Flask, render_template, jsonify, request, abort, redirect
import json
from datetime import datetime, timedelta, date
from urllib.parse import quote
import sqlite3
from pathlib import Path


app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "articles.db"

@app.template_global()
def format_date(y, m, d):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = months[m - 1]

        if   d == 1 or d == 21 or d == 31:
                day = f"{d}st"
        elif d == 2 or d == 22:
                day = f"{d}nd"
        elif d == 3 or d == 23:
                day = f"{d}rd"
        else:
                day = f"{d}th"

        year = str(y)[-2:]

        try:
                articledate = date(int(y), int(m), int(d))
        except (TypeError, ValueError):
                return False
        if (date.today() - articledate).days < 1:
                return 'Today'
        if (date.today() - articledate).days < 2:
                return 'Yesterday'
        if (date.today().year != y):
                return f"{day} {month} {year}"
        return f"{day} {month}"


@app.template_global()
def uriEncode(string):
        return quote(string)

@app.template_global()
def dateIsRecent(y, m, d):
    try:
        articledate = date(int(y), int(m), int(d))
    except (TypeError, ValueError):
        return False
    return (date.today() - articledate).days < 2



@app.template_global()
def returnIcon(name):
        icons = {
                "National Housing Federation": "/static/icons/nhf.png",
                "MHCLG - Comms": "/static/icons/govuk.webp",
                "MHCLG - Policy": "/static/icons/govuk.webp",
                "MHCLG - Regulation": "/static/icons/govuk.webp",
                "HCLIC Stats": "/static/icons/govuk.webp",
                "Crisis": "/static/icons/crisis.png",
                "Homeless Link": "/static/icons/homelesslink.png",
                "Shelter": "/static/icons/shelter.png",
                "LGA": "/static/icons/lga.png",
                "RSH - Research": "/static/icons/rsh.png",
                "RSH - Regulation": "/static/icons/rsh.png",
                "RSH - Policy": "/static/icons/rsh.png",
                "RSH - Comms": "/static/icons/rsh.png",
                "GLA - Mayor": "/static/icons/gla.png",
                "GLA - Assembly": "/static/icons/gla.png",
                "CIH": "/static/icons/cih.jpeg",
                "The MJ": "/static/icons/mj.png",
                "London Councils": "/static/icons/londoncouncils.png",
                "Salamander": "/static/icons/salamander.png",
                "HO": "/static/icons/ombudsman.png",
                "Inside Housing (Regulation)": "/static/icons/insidehousing.png",
                "Google News - LBL Housing": "/static/icons/googlenews.png",
                "Peter Apps": "/static/icons/substack.png",
                "Centre for Cities": "/static/icons/centerforcities.png",
                "Trust for London": "/static/icons/trustforlondon.jpeg",
                "Local Gov & Social Care Ombudsman": "/static/icons/lgsco.png",
                "G15": "/static/icons/g15.png",
                "Centre for London": "/static/icons/centreforlondon.png",
                "UK Collaborative Centre for Housing Evidence": "/static/icons/ukcche.png",
                "Guardian - Social Housing": "/static/icons/guardian.png",
                "Centre for Homelessness Impact": "/static/icons/centreforhomelessnessimpact.png",
                "Resolution Foundation": "/static/icons/ResolutionFoundation.jpg",

        }
        if icons.get(name):
                return icons[name]
        return None




@app.route('/')
def dashboard():



        category = request.args.get("category")
        if not category:
                category = 'all'

        sqliteConnection = sqlite3.connect(DB_PATH)
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()

        sources = None

        cursor.execute("""
        SELECT DISTINCT category FROM articles
        """)

        categories = cursor.fetchall()

        if category != 'all':
                cursor.execute("""
                SELECT DISTINCT source FROM articles
                WHERE CATEGORY = ?
                """, (category,))

                sources = cursor.fetchall()


                cursor.execute("""
                SELECT * FROM ARTICLES
                WHERE year > 2025
                AND category = ?
                ORDER BY year DESC, month DESC, day DESC;
                """, (category,))

                articles = cursor.fetchall()


        else:
                cursor.execute("""
                SELECT DISTINCT source FROM articles
                WHERE year > 2025
                """,)

                sources = cursor.fetchall()

                cursor.execute("""
                SELECT * FROM ARTICLES
                WHERE year > 2025
                ORDER BY year DESC, month DESC, day DESC;

                """)

                articles = cursor.fetchall()



        sqliteConnection.close()
        return render_template('dashboard.html',
                               articles=articles,
                               categories = categories,
                               selected = category,
                               sources=sources)


if __name__ == '__main__':
        app.run(debug=True, port=2133, host='0.0.0.0')
