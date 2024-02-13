import os

import sqlite3
from sqlite3 import Cursor, Connection
from easyocr import Reader

from db import sql_utils


# TODO: Use the function from original file or put into utils files
def open_refs_file() -> list[str]:
    with open("./scraping/refs.txt", "r") as refs_file:
        refs = refs_file.read().split("\n")
        return refs[:-1]


def delete_db_if_already_exists(db_file_name: str) -> None:
    if db_file_name in os.listdir("./db"):
        os.remove(f"./db/{db_file_name}")


def create_db_with_tables(db_file_name: str, sql_file_name: str):
    delete_db_if_already_exists(db_file_name)

    # Create database and connect
    con = sqlite3.connect(f"./db/{db_file_name}")
    cur = con.cursor()

    # Create tables
    sql_statement = sql_utils.get_sql_statement(sql_file_name)

    cur.executescript(sql_statement)


# TODO: Clean
# TODO: Make a specific one for production db initial import
def get_data_dict(reader: Reader, nb_catalog: int) -> dict:
    datas_dict = {}
    """
    Format: {[path] : [content, catalog_ref]}
    """

    catalog_i = 0
    page_i = 0

    refs_list = open_refs_file()[
        :nb_catalog
    ]  # ! Change for production initial import !
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

    return datas_dict


def initial_import(
    cur: Cursor,
    con: Connection,
    datas_dict: dict,
    sql_insert_catalog: str,
    sql_insert_page: str,
) -> None:
    # Insert new catalogs ref
    catalog_list = list(set([datas_dict[key][1] for key in list(datas_dict.keys())]))
    for catalog in catalog_list:
        cur.execute(sql_insert_catalog, (catalog,))

    #  Insert new pages
    for key in list(datas_dict.keys()):
        cur.execute(sql_insert_page, (key, datas_dict[key][0], datas_dict[key][1]))

    # Commit
    con.commit()


def initial_import_analytic(
    cur: Cursor,
    con: Connection,
    datas_dict: dict,
    sql_insert_page: str,
) -> None:
    #  Insert new pages
    for key in list(datas_dict.keys()):
        cur.execute(
            sql_insert_page,
            (
                key,
                datas_dict[key][0],
            ),
        )

    # Commit
    con.commit()
