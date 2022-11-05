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
        # response = requests.post(API_URL, json={"chat_id": CHAT_ID, "text": message})
        requests.post(API_URL, json={"chat_id": CHAT_ID, "text": message})
        # print(response.text)
    except Exception as err:
        logging.error(err)
