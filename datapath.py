import requests

import dynaconfig

API_TOKEN = dynaconfig.settings["API_TOKEN"]
CHAT_ID = dynaconfig.settings["CHAT_ID"]
apiURL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"


def send_news_to_telegram(message):
    try:
        response = requests.post(apiURL, json={"chat_id": CHAT_ID, "text": message})
        print(response.text)
    except Exception as e:
        print(e)
