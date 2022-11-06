import logging
import time
from datetime import datetime

import requests

import dynaconfig
import news_db

# Time range for sending messages
TIME_TO_SEND_START = datetime.now().replace(hour=10, minute=00).strftime("%H:%M")
TIME_TO_SEND_END = datetime.now().replace(hour=20, minute=00).strftime("%H:%M")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


API_TOKEN = dynaconfig.settings["API_TOKEN"]
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
CHAT_ID = dynaconfig.settings["CHAT_ID"]


def send_news_to_telegram(message):
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
    data_from_db = news_db.create_connection(news_db.DB_FILE)
    while True:
        time.sleep(1)
        current_time = datetime.now().strftime("%H:%M")
        if TIME_TO_SEND_START < current_time < TIME_TO_SEND_END:
            logging.info(f"Time: {current_time}. Time to send has come !")
            for news in news_db.send_all_news(data_from_db):
                send_news_to_telegram(news)
                time.sleep(300)
        else:
            logging.info(f"Time: {current_time}. Still waiting to send.")
