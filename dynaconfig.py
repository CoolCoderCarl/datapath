import logging

from dynaconf import Dynaconf

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)

settings = Dynaconf(
    settings_files=[".secrets.toml"],
)

if __name__ == "__main__":
    for data in settings:
        logging.info(f"Loaded variable {data}")
