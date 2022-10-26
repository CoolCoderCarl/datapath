import logging
import sqlite3
from pathlib import Path
from sqlite3 import Error

DB_FILE = Path("test.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news (
news_id INTEGER PRIMARY KEY,
author TEXT,
title TEXT,
description TEXT,
url TEXT,
pub_date TEXT,
used_bool TEXT
);
"""

INSERT_INTO_SQL = """
INSERT INTO news
(author,title,description,url,pub_date,used_bool)
VALUES(?,?,?,?,?,?)
"""


# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def create_connection(db_file: Path):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Database created successfully !")
        return conn
    except Error as create_conn_err:
        logging.error(create_conn_err)
    return conn


def create_table(conn, create_table_query):
    try:
        c = conn.cursor()
        c.execute(create_table_query)
        logging.info("Table created successfully !")
    except Error as create_table_err:
        logging.error(create_table_err)


def insert_into(conn, data: tuple):
    try:
        cur = conn.cursor()
        cur.execute(INSERT_INTO_SQL, data)
        conn.commit()

        logging.info("Data inserted successfully !")
        return cur.lastrowid
    except Error as insert_err:
        logging.error(insert_err)


if __name__ == "__main__":
    conn = create_connection(DB_FILE)
    if conn is not None:
        create_table(conn, CREATE_TABLE_SQL)
    else:
        logging.error("Error! Cannot create the database connection.")
