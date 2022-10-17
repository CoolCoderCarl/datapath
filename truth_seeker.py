from newsapi import NewsApiClient

import dynaconfig

# https://newsapi.org/

API_KEY = dynaconfig.config["API_KEY"]

newsapi = NewsApiClient(api_key=API_KEY)

try:
    all_articles = newsapi.get_everything(q="test", sort_by="popularity")

    for k_a, v_a in all_articles.items():
        print(k_a, v_a)
        if k_a == "articles":
            for list_i in v_a:
                print("=======================")
                print("NEW NEWS")
                print("=======================")
                for k, v in list_i.items():
                    print(k, v)

except ConnectionError as con_err:
    print(con_err)
except BaseException as base_err:
    print(base_err)

# print(all_articles)


