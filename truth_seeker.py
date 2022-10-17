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


def fetch_info(query: str):
    try:
        result = newsapi.get_everything(q=query, sort_by="popularity")
        logging.info(f"Searching for {query}")
        return result
    except ConnectionError as con_err:
        logging.error(con_err)
    except BaseException as base_err:
        logging.error(base_err)


def list_info():
    for k_a, v_a in fetch_info("test").items():
        print(k_a, v_a)
        if k_a == "articles":
            for list_i in v_a:
                print("=======================")
                print("NEW NEWS")
                print("=======================")
                for k, v in list_i.items():
                    print(k, v)


if __name__ == "__main__":
    list_info()
