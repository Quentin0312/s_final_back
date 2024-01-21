import os
import sqlite3
import easyocr
from db import sql_utils

con = sqlite3.connect("./db/db_v0.sqlite")
cur = con.cursor()

reader = easyocr.Reader(lang_list=["en"])  # or fr ?
# TODO: fns to put in "inference_pipeline_utils"
# Inference

datas_dict = {}

p_indice = 0
page_indice = 0
for prospectus in os.listdir("./datas"):  # TODO: Absolute path instead !
    p_indice += 1
    print("Prospectus n°", p_indice)

    for page in os.listdir(f"./datas/{prospectus}"):
        page_indice += 1
        print(page_indice)

        full_path = f"./datas/{prospectus}/{page}"
        text_content = ""

        results = reader.readtext(full_path)
        for result in results:
            text_content += " " + str(result[1])  # TODO: Remove useless first space

        datas_dict[full_path] = text_content


# Save in DB

sql = sql_utils.get_sql_statement("insert_pages.sql")

for key in datas_dict.keys():
    cur.execute(sql, (datas_dict[key], key))

con.commit()
