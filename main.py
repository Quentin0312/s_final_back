import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
from sqlite3 import Cursor

from starlette.responses import StreamingResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Clean and refactor
# TODO: Setup tests
# TODO: Gérer les cas d'erreurs


# TODO: Put in an other file
def get_page(key_word: str, cur: Cursor) -> list[str]:
    sql = ""
    with open("./db/sql/select_pages.sql") as sql_select:
        sql = sql_select.read()
        sql_select.close()

    res = cur.execute(sql, (f"%{key_word}%",))  # TODO: Put sql in a sql file
    return res.fetchall()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search/{key_word}")
def read_item(key_word: str):
    con = sqlite3.connect("./db/db_v0.sqlite")
    cur = con.cursor()

    response = get_page(key_word, cur)

    # return {"key_word": key_word, "first_text_content": response[0][0]}
    return StreamingResponse(io.BytesIO(response[0][1]), media_type="image/jpg")
