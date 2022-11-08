# datapath

Simple ETL getting info from https://newsapi.org/ and send to telegram channel

## Prehistory
This simple service help to search information automatically via News API

> Datapath it is like telepath or astropath  
> (c) Author

Enjoy.

## How to use
You can check the last available tags here - 
1) https://hub.docker.com/repository/docker/h0d0user/truth_seeker
2) https://hub.docker.com/repository/docker/h0d0user/datapath
3) https://hub.docker.com/repository/docker/h0d0user/news_db

Need to fill `settings.toml` with next important variables:
1) `DB_NAME`. Where you want to load your data before send to telegram.
2) `API_KEY`. You can find this data here - https://my.telegram.org/apps
3) `QUERY`. Key word to search for in articles.
4) `API_TOKEN`. Ask *BotFather* in telegram.
5) `CHAT_ID`. Use this to find chat ID where you want to send messages - https://api.telegram.org/botAPI_TOKEN/getUpdates
6) `docker-compose up -d`
7) ...
8) PROFIT !!!

*It is not final configuration. You can find template below.*

File `settings.toml` template:
```
[DB]
DB_NAME = "/mnt/test.db"


[NEWS_API]
API_KEY = ""
QUERY = "test"
LANGUAGE = "en"


[TELEGRAM]
API_TOKEN = ""
CHAT_ID = ""


[TIMINIGS]
TIME_TO_PURGE = "00:00"
TIME_TO_SEARCH = "02:00"
TIME_TO_SEND_START = "10:00"
TIME_TO_SEND_END = "20:00"
SENDING_INTERVAL = 300
```



**Still have questions ? Google it.**