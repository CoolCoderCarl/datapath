import logging
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

import dynaconfig

TIME_TO_PURGE = "00:00"

DB_FILE = Path(f"/mnt/{dynaconfig.settings['DB_NAME']}")

# SQL queries
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news (
author TEXT,
title TEXT,
description TEXT,
url TEXT,
pub_date TEXT
);
"""

INSERT_INTO_SQL = """
INSERT INTO news
(author,title,description,url,pub_date)
VALUES(?,?,?,?,?)
"""


SELECT_FROM_SQL = """
SELECT * FROM news
"""

DELETE_FROM_SQL = """
DELETE FROM news
"""


# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def create_connection(db_file: Path):
    """
    Create db file
    :param db_file: path to db file to create
    :return:
    """
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Connection created successfully !")
        return conn
    except Error as create_conn_err:
        logging.error(create_conn_err)
    return None


def create_table(conn, create_table_query):
    """
    :param conn: Connection to the SQLite database
    :param create_table_query:
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_query)
        logging.info("Table created successfully !")
    except Error as create_table_err:
        logging.error(create_table_err)


def insert_into(conn, data: tuple):
    """
    Insert data to base
    This is the load step in ETL pipeline
    :param conn: Connection to the SQLite database
    :param data:
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(INSERT_INTO_SQL, data)
        conn.commit()
        logging.info("Data inserted successfully !")
        return cur.lastrowid
    except Error as insert_err:
        logging.error(insert_err)


def send_all_news(conn):
    """
    Query all rows in the news table
    :param conn: Connection to the SQLite database
    :return:
    """
    cur = conn.cursor()
    cur.execute(SELECT_FROM_SQL)

    rows = cur.fetchall()

    return rows


def delete_all_news(conn):
    """
    Delete all rows in the news table
    :param conn: Connection to the SQLite database
    :return:
    """
    cur = conn.cursor()
    cur.execute(DELETE_FROM_SQL)
    conn.commit()
    logging.info("Database was purged !")


if __name__ == "__main__":
    conn = create_connection(DB_FILE)
    if DB_FILE.exists():
        create_table(conn, CREATE_TABLE_SQL)

    while True:
        CURRENT_TIME = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if conn is not None:
            send_all_news(conn)
            if CURRENT_TIME == TIME_TO_PURGE:
                logging.info(f"Time: {CURRENT_TIME}. Time to purge has come !")
                delete_all_news(conn)
            else:
                logging.info(f"Time: {CURRENT_TIME}. Still waiting for purging.")
        else:
            logging.error("Error! Cannot create the database connection.")
