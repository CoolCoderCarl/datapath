import logging
import time
from datetime import datetime

import requests

import dynaconfig

# Time range for sending messages loaded from settings.toml
TIME_TO_SEND_START = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEND_START"]
TIME_TO_SEND_END = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEND_END"]
SENDING_INTERVAL = dynaconfig.settings["TIMINIGS"]["SENDING_INTERVAL"]

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


API_TOKEN = dynaconfig.settings["TELEGRAM"]["API_TOKEN"]
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
CHAT_ID = dynaconfig.settings["TELEGRAM"]["CHAT_ID"]

NEWS_DB_API_URL = dynaconfig.settings["DB"]["DB_API_URL"]


def check_api_available() -> bool:
    try:
        logging.info(f"Try to connect to API, URL: {NEWS_DB_API_URL}/healthcheck")
        time.sleep(1)
        return requests.get(f"{NEWS_DB_API_URL}/healthcheck").ok
    except (ConnectionError, ConnectionRefusedError) as con_err:
        logging.error(con_err)
        return False


def send_news_to_telegram(message):
    """
    Send messages from db to telegram
    :param message:
    :return:
    """
    try:
        response = requests.post(
            API_URL,
            json={
                "chat_id": CHAT_ID,
                "text": f"Author: {message['author']}\n"
                f"\n"
                f"Title: {message['title']}\n"
                f"\n"
                f"{message['description']}\n"
                f"\n"
                f"URL: {message['url']}\n"
                f"\n"
                f"Date published: {message['pub_date']}\n",
            },
        )
        if response.status_code == 200:
            logging.info(
                f"Sent: {response.reason}. Status code: {response.status_code}"
            )
        else:
            logging.error(
                f"Not sent: {response.reason}. Status code: {response.status_code}"
            )
    except Exception as err:
        logging.error(err)


def ask_entities() -> int:
    """
    Ask API request to discover how much entities in db
    Return int instead of str
    :return:
    """
    return int(requests.get(f"{NEWS_DB_API_URL}/entities").text)


if __name__ == "__main__":
    while True:
        if check_api_available():
            current_time = datetime.now().strftime("%H:%M")
            if TIME_TO_SEND_START < current_time < TIME_TO_SEND_END:
                logging.info("Time to send news has come !")
                if ask_entities() == 0:
                    logging.warning("Database is empty ! Take a break for 30 min.")
                    time.sleep(1800)
                else:
                    try:
                        data_from_db = requests.get(f"{NEWS_DB_API_URL}/news").json()
                        for news in data_from_db:
                            send_news_to_telegram(news)
                            time.sleep(SENDING_INTERVAL)
                        else:
                            logging.warning(
                                f"All news was sent ! Going to purge ! Entities in db for now {ask_entities()}."
                            )
                            try:
                                response = requests.get(f"{NEWS_DB_API_URL}/purge")
                            except Exception as exception:
                                logging.error(f"Exception while purging: {exception}.")
                            else:
                                logging.info(
                                    f"Database was purged successfully ! Entities in db for now {ask_entities()}."
                                )
                    except Exception as exception:
                        logging.error(f"Exception while getting news: {exception}")
            else:
                logging.info("Still waiting to send.")
                time.sleep(5)
        else:
            logging.error("API is not available !")
            time.sleep(5)
