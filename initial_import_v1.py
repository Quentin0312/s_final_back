import os
import sqlite3
import easyocr
from db import sql_utils

con = sqlite3.connect("./db/db_v1.sqlite")
cur = con.cursor()

reader = easyocr.Reader(lang_list=["en"])  # or fr ?

# TODO: Clean

# Inference
# TODO: fns to put in "inference_pipeline_utils"

datas_dict = {}
"""
Format: {[path] : [content, catalog_ref]}
"""

catalog_i = 0
page_i = 0


# TODO: Use the function from original file or put into utils files
def open_refs_file() -> list[str]:
    with open("./scraping/refs.txt", "r") as refs_file:
        refs = refs_file.read().split("\n")
        return refs[:-1]


refs_list = open_refs_file()[:100]

# for catalog_ref in os.listdir("./dataset")[:100]:
for catalog_ref in refs_list:
    catalog_ref = catalog_ref[:-1]
    catalog_i += 1
    print("Catalogue n°", catalog_i)
    # TODO: Remove when possible
    if catalog_ref == "train":
        pass

    for page_file_name in os.listdir(f"./dataset/{catalog_ref}"):
        page_i += 1
        print(page_i)

        path = f"./dataset/{catalog_ref}/{page_file_name}"

        text_content = ""

        results = reader.readtext(path)
        for result in results:
            text_content += " " + str(result[1])

        datas_dict[path] = [text_content, catalog_ref]

# Save in DB

# Insert new catalogs ref
sql_insert_catalog = sql_utils.get_sql_statement("initial_import_v1_catalog.sql")

catalog_list = list(set([datas_dict[key][1] for key in list(datas_dict.keys())]))

for catalog in catalog_list:
    cur.execute(sql_insert_catalog, (catalog,))

#  Insert new pages
sql_insert_page = sql_utils.get_sql_statement("initial_import_v1_page.sql")

for key in list(datas_dict.keys()):
    cur.execute(sql_insert_page, (key, datas_dict[key][0], datas_dict[key][1]))

con.commit()
