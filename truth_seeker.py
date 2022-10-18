import logging

from newsapi import NewsApiClient

import dynaconfig

# https://newsapi.org/

API_KEY = dynaconfig.config["API_KEY"]

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


def fetch_info(query: str) -> dict:
    try:
        result = newsapi.get_everything(q=query, sort_by="popularity")
        logging.info(f"Searching for {query}")
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
            for article_point, article_data in article.items():
                if article_point == "urlToImage":
                    continue
                elif article_point == "source":
                    print(article_point.capitalize(), article_data.get("name"))
                else:
                    print(article_point.capitalize(), article_data)
    else:
        logging.warning("Empty response from API")
        raise IndexError


if __name__ == "__main__":
    list_info(fetch_info("test"))
