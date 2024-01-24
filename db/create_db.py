import pathlib
import sqlite3
import sql_utils

path = pathlib.Path(__file__).parent.resolve()

# Connect / Create database
# con = sqlite3.connect(f"{path}/db_v0.sqlite")
con = sqlite3.connect(f"{path}/db_v1.sqlite")

cur = con.cursor()

# Create tables
# sql_statement = sql_utils.get_sql_statement("create_tables.sql")
sql_statement = sql_utils.get_sql_statement("create_tables_v1.sql")

# cur.execute(sql_statement)
cur.executescript(sql_statement)
