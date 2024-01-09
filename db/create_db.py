import pathlib
import sqlite3

path = pathlib.Path(__file__).parent.resolve()

con = sqlite3.connect(f"{path}/db_v0.sqlite")
cur = con.cursor()

with open(f"{path}/sql/create_tables.sql") as create_tables:
    cur.execute(create_tables.read())
