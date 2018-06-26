"""
* Responsibility:
Provide functions for crawler and parser to pertaining to any data persistance task.

- Why a database instead of a simpler csv file? (CSV is very popular with data science related projects)
Because I wanted to make the scraper handle errors gracefully.
I wanted the stacktrace to be stored somewhere when crawling or parsing fails so that I can review later.
I wanted the crawler to skip successfully crawled pages.
I also wanted to do housekeeping like track insertion datetime.
"""

import sqlite3
from time import gmtime, strftime


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('fraiser.db')
        self.create_tables()

    def create_tables(self):
        sqls = [
            """
                CREATE TABLE IF NOT EXISTS history
                (
                    url TEXT,
                    detail TEXT,
                    status TEXT,
                    timestamp TEXT
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS episode
                (
                    url TEXT,
                    season INTEGER,
                    episode INTEGER,
                    title TEXT,
                    transcript_written_date TEXT,
                    transcript_revised_date TEXT,
                    aired_date TEXT,
                    writers TEXT,
                    directors TEXT,
                    timestamp TEXT
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS script
                (
                    url TEXT,
                    cast TEXT,
                    dialog TEXT,
                    timestamp TEXT
                );
            """
        ]
        for sql in sqls:
            self.conn.execute(sql)
            self.conn.commit()

    def save_history(self, url, detail, status):
        sql = """
                INSERT INTO history VALUES (
                    ?,
                    ?,
                    ?,
                    ?
                )
        """
        self.conn.execute(sql, (
            url,
            detail,
            status,
            strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ))
        self.conn.commit()

    def check_history(self, url, status):
        sql = """
                SELECT * FROM history
                WHERE 
                    url = ?
                    and status = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (
            url,
            status
        ))
        return cur.fetchall()

    def save_episode_info(self, url, info):
        sql = """
                INSERT INTO episode VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
        """
        self.conn.execute(sql, (
            url,
            info['season'],
            info['episode'],
            info['title'],
            info['written_date'],
            info['revised_date'],
            info['aired_date'],
            info['writers'],
            info['director'],
            strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ))
        self.conn.commit()

    def save_script(self, url, cast, dialog):
        sql = """
                INSERT INTO script VALUES (
                    ?,
                    ?,
                    ?,
                    ?
                )
        """
        self.conn.execute(sql, (
            url,
            cast,
            dialog,
            strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ))
        self.conn.commit()
