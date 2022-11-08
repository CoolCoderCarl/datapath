import logging
import time
from datetime import date, datetime, timedelta

from newsapi import NewsApiClient

import dynaconfig
import news_db

# News API params loaded from settings.toml
API_KEY = dynaconfig.settings["NEWS_API"]["API_KEY"]
QUERY = dynaconfig.settings["NEWS_API"]["QUERY"]
LANGUAGE = dynaconfig.settings["NEWS_API"]["LANGUAGE"]
TIME_TO_SEARCH = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEARCH"]

newsapi = NewsApiClient(api_key=API_KEY)


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
    """
    Fetch info from API according to query in settings.toml
    This is the extraction step in ETL pipeline
    :return:
    """
    # Use to get news from yesterday to current time
    yesterday = date.today() - timedelta(days=1)
    try:
        logging.info(
            f"Searching for {QUERY}; most popular; from: {yesterday}; language: {LANGUAGE}"
        )
        result = newsapi.get_everything(
            q=QUERY, sort_by="popularity", from_param=yesterday, language=LANGUAGE
        )
        return result
    except ConnectionError as con_err:
        logging.error(con_err)
        return {}
    except BaseException as base_err:
        logging.error(base_err)
        return {}


def load_to_db(fetch_info: dict):
    """
    Load specific info to db
    These are the transform and load steps in ETL pipeline
    :param fetch_info:
    :return:
    """
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
            news_db.insert_into(
                news_db.create_connection(news_db.DB_FILE),
                # Pull too much info but add set conversion
                tuple(set(article_list)),
            )
    else:
        logging.warning("Empty response from News API.")
        raise IndexError


if __name__ == "__main__":
    while True:
        CURRENT_TIME = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if CURRENT_TIME == TIME_TO_SEARCH:
            logging.info("Time to search has come !")
            try:
                load_to_db(fetch_info())
            except BaseException as base_err:
                logging.error(base_err)
        else:
            logging.info("Still waiting for searching.")
