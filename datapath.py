import logging

import requests

import dynaconfig

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
