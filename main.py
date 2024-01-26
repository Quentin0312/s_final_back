# import io
# from starlette.responses import StreamingResponse
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
from sqlite3 import Cursor

from pydantic import BaseModel

from db import sql_utils

# TODO: Clean file

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO: Mettre en place sécurité contre injection SQL
# TODO: Create a service like function that handle requests to db
# TODO: Clean and refactor
# TODO: Setup tests
# TODO: Gérer les cas d'erreurs


# TODO: Rename
# TODO: Put in an other file
def get_pages(key_words: list[str], category: int, cur: Cursor) -> list[str]:
    sql = sql_utils.get_sql_statement("select_pages_v1.sql")
    keyword = f"%{key_words[0]}%"

    # TODO: Take into account multiple key_words

    # Take into account the category
    if category != -1:
        sql += f" AND id_category = {category};"

    res = cur.execute(sql, (keyword,))
    return res.fetchall()


# TODO: Put in an other file
def get_image_encoded(url: str) -> str:
    image_bytes = b""
    with open(url, "rb") as image_file:
        image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        image_file.close()

    return encoded_image


@app.get("/")
def read_root():
    return {"Hello": "World"}


class SearchInfos(BaseModel):
    key_words: list[str]
    category: int


@app.post("/search")
def read_item(search_infos: SearchInfos):
    # con = sqlite3.connect("./db/db_training_v1.sqlite")
    con = sqlite3.connect("./db/db_v1.sqlite")
    cur = con.cursor()

    response = get_pages(search_infos.key_words, search_infos.category, cur)
    print(response)

    # Linked categories
    categories = list(set([elt[2] for elt in response]))
    if None in categories:
        categories.remove(None)

    # Images
    images_encoded = [get_image_encoded(elt[1]) for elt in response]

    return {"categories": categories, "list_image_base64": images_encoded}
