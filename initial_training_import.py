import os
import sqlite3
import easyocr
from db import sql_utils

con = sqlite3.connect("./db/db_training.sqlite")
cur = con.cursor()

reader = easyocr.Reader(lang_list=["en"])  # or fr ?

# Inference
# TODO: fns to put in "inference_pipeline_utils"

datas_dict = {}
"""
Format: {[path] : [content, category]}
"""

page_indice = 0
for category in os.listdir("./dataset/train"):
    print("Category => ", category)

    for page in os.listdir(f"./dataset/train/{category}"):
        page_indice += 1
        print(page_indice)

        path = f"./dataset/train/{category}/{page}"

        text_content = ""

        results = reader.readtext(path)
        for result in results:
            text_content += " " + str(result[1])

        datas_dict[path] = [text_content, category]

# Save in DB

sql = sql_utils.get_sql_statement("insert_pages_training.sql")

for key in datas_dict.keys():
    cur.execute(sql, (datas_dict[key][0], key, datas_dict[key][1]))

con.commit()
