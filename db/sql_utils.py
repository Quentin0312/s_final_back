import pathlib

path = pathlib.Path(__file__).parent.resolve()


def get_sql_statement(file_name: str) -> str:
    """
    Get sql statement stored in `.sql` files
    """
    sql_statement = ""
    with open(f"{path}/sql/{file_name}") as sql_file:
        sql_statement = sql_file.read()
        sql_file.close()

    return sql_statement
