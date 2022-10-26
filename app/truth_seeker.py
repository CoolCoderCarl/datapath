import logging
from datetime import date, timedelta

from newsapi import NewsApiClient

import databaseconnection
import dynaconfig

API_KEY = dynaconfig.settings["API_KEY"]
QUERY = dynaconfig.settings["QUERY"]

# Use to get news from yesterday to current time
YESTERDAY = date.today() - timedelta(days=1)

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


def list_info(fetch_info: dict):
    if fetch_info:
        for article in fetch_info.get("articles"):
            for article_key, article_data in article.items():
                if article_key == "urlToImage":
                    continue
                elif article_key == "source":
                    print(article_key.capitalize(), article_data.get("name"))
                else:
                    print(article_key.capitalize(), article_data)
    else:
        logging.warning("Empty response from API")
        raise IndexError


def load_to_db():
    for article in fetch_info().get("articles"):
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
        article_list.append("True")
        databaseconnection.insert_into(
            databaseconnection.create_connection(databaseconnection.DB_FILE),
            tuple(article_list),
        )


if __name__ == "__main__":
    if dynaconfig.settings["LOAD_TO_DB"]:
        try:
            load_to_db()
        except BaseException as base_err:
            logging.error(base_err)
    else:
        list_info(fetch_info())
