from newsapi import NewsApiClient
# https://newsapi.org/

API_KEY = ""

newsapi = NewsApiClient(api_key=API_KEY)

# TRY
all_articles = newsapi.get_everything(q="test",
                                      sort_by="popularity")

# print(all_articles)

for k_a, v_a in all_articles.items():
    print(k_a, v_a)
    if k_a == "articles":
        for list_i in v_a:
            print("=======================")
            print("NEW NEWS")
            print("=======================")
            for k, v in list_i.items():
                print(k, v)
