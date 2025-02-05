import os
import sqlite3
import torch
import spacy

from db import sql_utils
from labos.nlp import model_utils, preprocessing

# TODO: Put chanhging variables on top: db_file_name, model_weight_path,...

# Get raw texts from db
con = sqlite3.connect("./db/db_v1.sqlite")
cur = con.cursor()

select_sql_statement = sql_utils.get_sql_statement("select_pages_inference_v1.sql")

"""
Format: list[(id: int, text: str)]
"""
response = cur.execute(select_sql_statement).fetchall()

# predict label with NLP model
vocabulary = preprocessing.get_vocabulary("./labos/nlp/vocab_v1.txt")

# labels = [int(label) for label in os.listdir("./dataset/train")]
labels = [i for i in range(16)]

# ! Only because category don't added to db yet ---------------------------------------------
insert_category_sql_statement = sql_utils.get_sql_statement("insert_category_v1.sql")
for label in labels:
    cur.execute(insert_category_sql_statement, (label,))
# ! -----------------------------------------------------------------------------------------

model = model_utils.PageClassifier(len(vocabulary), len(labels))
model.load_state_dict(torch.load("./labos/nlp/model_weight_v1.pth"))

nlp = spacy.load("fr_core_news_lg")

i = 0
for page_element in response:
    id_page = page_element[0]
    raw_text = page_element[1]

    i += 1
    if i % 10 == 0:
        print(i)
    input = preprocessing.pipeline_from_raw_text_to_vectors(raw_text, nlp, vocabulary)
    label = model_utils.predict(model, input)
    # print("label", label)
    update_page_sql_statement = sql_utils.get_sql_statement(
        "update_with_category_v1.sql"
    )
    cur.execute(
        update_page_sql_statement,
        (
            label,
            id_page,
        ),
    )

con.commit()
