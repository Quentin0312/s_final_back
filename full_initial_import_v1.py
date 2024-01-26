import sqlite3
import easyocr

from db import sql_utils
import initial_import_utils


db_file_name = "db_v1.sqlite"
sql_file_name = "create_tables_v1.sql"

# Create db with tables
initial_import_utils.create_db(db_file_name, sql_file_name)

# Connect to db
con = sqlite3.connect(f"./db/{db_file_name}")
cur = con.cursor()

# Extract datas from images
"""
(OCR) image => text
folder_name = catalog_ref
image_path => file location
"""
reader = easyocr.Reader(lang_list=["en"])  # or fr ?
datas_dict = initial_import_utils.get_data_dict(reader, nb_catalog=100)

# Insert in db
sql_insert_catalog = sql_utils.get_sql_statement("initial_import_v1_catalog.sql")
sql_insert_page = sql_utils.get_sql_statement("initial_import_v1_page.sql")
initial_import_utils.initial_import(
    cur, con, datas_dict, sql_insert_catalog, sql_insert_page
)
