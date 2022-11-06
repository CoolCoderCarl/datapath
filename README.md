# truth_seeker

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
1) `API_KEY`. You can find this data here - https://my.telegram.org/apps
2) `API_TOKEN`. Ask *BotFather* in telegram.
3) `CHAT_ID`. Use this to find chat ID where you want to send messages - https://api.telegram.org/bot<API_TOKEN>/getUpdates
4) `DB_NAME`. Where you want to load your data before send to telegram.
5) `QUERY`. Key word to search for in articles.
6) `docker-compose up -d`
7) ...
8) PROFIT !!!

**Still have questions ? Google it.**