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
                datos JSONB
            )
        """)

        conn.commit()

        cur.close()
        conn.close()

    def insert(self, id: int, data: json):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        cur = conn.cursor()

        cur.execute(f"INSERT INTO {self.tbname} (id, datos) VALUES ({id}, '{json.dumps(data)}')")

        conn.commit()

        cur.close()
        conn.close()

    def update(self, id: int, data: json):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        cur = conn.cursor()

        cur.execute(f"""
            UPDATE {self.tbname}
            SET datos = '{json.dumps(data)}'
            WHERE id = {id}
        """)

        conn.commit()

        cur.close()
        conn.close()


dbm = DBManipulation(
    dbname="properties_raw_data",
    user="karel",
    password="karel123",
    host="localhost",
    tbname="property"
)

# dbm.insert(1, {"nombre": "Sabrina", "edad": 8, "ciudad": "Gent"})
dbm.update(1, {
    "nombre": "karel",
    "edad": 39,
    "ciudad": "Gent"
})
