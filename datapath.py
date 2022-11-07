import logging
import time
from datetime import datetime

import requests

import dynaconfig
import news_db

# Time range for sending messages loaded from settings.toml
TIME_TO_SEND_START = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEND_START"]
TIME_TO_SEND_END = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEND_END"]

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


def send_news_to_telegram(message):
    """
    Send messages from db to telegram
    :param message:
    :return:
    """
    try:
        response = requests.post(API_URL, json={"chat_id": CHAT_ID, "text": message})
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


if __name__ == "__main__":
    db_connection = news_db.create_connection(news_db.DB_FILE)
    while True:
        if db_connection:
            time.sleep(1)
            current_time = datetime.now().strftime("%H:%M")
            if TIME_TO_SEND_START < current_time < TIME_TO_SEND_END:
                logging.info("Time to send has come !")
                data_from_db = news_db.send_all_news(db_connection)
                if len(data_from_db) == 0:
                    logging.warning("Database is empty !")
                else:
                    for news in data_from_db:
                        send_news_to_telegram(news)
                        time.sleep(300)
            else:
                logging.info("Still waiting to send.")
        else:
            logging.error("Connection to db is not exist !")
