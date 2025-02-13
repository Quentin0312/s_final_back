import pathlib
import sqlite3
import sql_utils

path = pathlib.Path(__file__).parent.resolve()

# Connect / Create database
con = sqlite3.connect(f"{path}/db_training.sqlite")
cur = con.cursor()

# Create tables
sql_statement = sql_utils.get_sql_statement("create_training_tables.sql")
cur.execute(sql_statement)
