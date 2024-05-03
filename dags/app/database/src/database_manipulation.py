from typing import Tuple

import psycopg2
import json


class DBManipulation:
    def __init__(self, dbname: str, user: str, password: str, host: str, tbname: str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.tbname = tbname

        self.create_database(dbname=self.dbname)
        self.create_table(tbname=self.tbname)

    def create_database(self, dbname: str):
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host)
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
        exist = cur.fetchone()

        if not exist:
            cur.execute("CREATE DATABASE " + dbname)

        conn.commit()

        cur.close()
        conn.close()

    def create_table(self, tbname: str):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        cur = conn.cursor()

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {tbname} (
                id INTEGER PRIMARY KEY,
                data JSONB
            )
        """)
        conn.commit()

        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_id ON {tbname} (id)")
        conn.commit()

        cur.close()
        conn.close()

    def insert(self, id: int, data: json):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        cur = conn.cursor()

        cur.execute("INSERT INTO property (id, data) VALUES (%s, %s)", (id, json.dumps(data),))

        conn.commit()

        cur.close()
        conn.close()

    def update(self, id: int, data: json):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        cur = conn.cursor()

        cur.execute("""
                    UPDATE property
                    SET data = %s
                    WHERE id = %s
                """, (json.dumps(data), id,))

        conn.commit()

        cur.close()
        conn.close()

    def select_property_by_id(self, id: int) -> Tuple[bool, str]:
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        curr = conn.cursor()

        curr.execute("SELECT * FROM property WHERE id = %s", (id,))

        data = curr.fetchall()

        if not data:
            return False, data

        # print(f"Data: {data}")
        return True, json.dumps(data)
