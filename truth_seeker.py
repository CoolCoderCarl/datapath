import logging
import time
from datetime import date, datetime, timedelta

import pandas as pd
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
        logging.info(f"Found about {fetch_info['totalResults']} entities.")
        # articles_df = pd.unique(pd.DataFrame(fetch_info["articles"]))
        articles_df = pd.DataFrame(fetch_info["articles"])
        del articles_df["source"]
        del articles_df["content"]
        del articles_df["urlToImage"]
        for article in articles_df.values:
            news_db.insert_into(
                news_db.create_connection(news_db.DB_FILE),
                # Pull too much info
                tuple(article),
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
            except ValueError as val_err:
                logging.error(f"ValueError: {val_err}")
            except IndexError as ind_err:
                logging.error(f"IndexError: {ind_err}")
            except BaseException as base_err:
                logging.error(f"BaseException: {base_err}")
        else:
            logging.info("Still waiting for searching.")
