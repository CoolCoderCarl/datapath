import logging
from datetime import date, datetime, timedelta

from newsapi import NewsApiClient

import db
import dynaconfig

API_KEY = dynaconfig.settings["API_KEY"]
QUERY = dynaconfig.settings["QUERY"]

# Use to get news from yesterday to current time
YESTERDAY = date.today() - timedelta(days=1)

newsapi = NewsApiClient(api_key=API_KEY)

now = datetime.now()

CURRENT_TIME = now.strftime("%H:%M")
TIME_TO_SEARCH = "01:00"


# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def fetch_info() -> dict:
    try:
        result = newsapi.get_everything(
            q=QUERY, sort_by="popularity", from_param=YESTERDAY
        )
        logging.info(f"Searching for {QUERY}")
        return result
    except ConnectionError as con_err:
        logging.error(con_err)
        return {}
    except BaseException as base_err:
        logging.error(base_err)
        return {}


def load_to_db(fetch_info: dict):
    if fetch_info:
        for article in fetch_info.get("articles"):
            article_list = []
            for article_key, article_data in article.items():
                if article_key == "source":
                    pass
                elif article_key == "content":
                    pass
                elif article_key == "urlToImage":
                    pass
                else:
                    article_list.append(article_data)
            db.insert_into(
                db.create_connection(db.DB_FILE),
                tuple(article_list),
            )
    else:
        logging.warning("Empty response from API.")
        raise IndexError


if __name__ == "__main__":
    while True:
        # Pull too much info
        if CURRENT_TIME == TIME_TO_SEARCH:
            logging.info("Time to search has come !")
            try:
                load_to_db(fetch_info())
            except BaseException as base_err:
                logging.error(base_err)
