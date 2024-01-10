# import io
# from starlette.responses import StreamingResponse
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
from sqlite3 import Cursor


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO: Create a service like function that handle requests to db
# TODO: Clean and refactor
# TODO: Setup tests
# TODO: Gérer les cas d'erreurs


# TODO: Rename
# TODO: Put in an other file
def get_page(key_word: str, cur: Cursor) -> list[str]:
    sql = ""
    with open("./db/sql/select_pages.sql") as sql_select:
        sql = sql_select.read()
        sql_select.close()

    res = cur.execute(sql, (f"%{key_word}%",))  # TODO: Put sql in a sql file
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


@app.get("/search/{key_word}")
def read_item(key_word: str):
    con = sqlite3.connect("./db/db_v0.sqlite")
    cur = con.cursor()

    response = get_page(key_word, cur)

    encoded_image = get_image_encoded(response[0][1])

    return {
        "key_word": key_word,
        "first_text_content": response[0][0],
        "image_base64": encoded_image,
    }
    # return StreamingResponse(io.BytesIO(response[0][1]), media_type="image/jpg")
