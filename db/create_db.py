import pathlib
import sqlite3
import sql_utils

path = pathlib.Path(__file__).parent.resolve()

# Connect / Create database
con = sqlite3.connect(f"{path}/db_prod.sqlite")

cur = con.cursor()

# Create tables
sql_statement = sql_utils.get_sql_statement("create_tables_prod.sql")
cur.executescript(sql_statement)


# Insert categories
labels = [
    (0, "Aménagement intérieur"),
    (1, "Électroménager"),
    (2, "Multimédia (son, TV)"),
    (3, "Aménagement extérieur"),
    (4, "Papeterie"),
    (5, "Téléphone"),
    (6, "Informatique"),
    (7, "Grandes distribution"),
    (8, "Bricolage / Bâtiments / Travaux"),
    (9, "Culture (livres, jeux-vidéos, musique)"),
    (10, "Mode / Vêtements / Chaussures"),
    (11, "Sport"),
    (12, "Bébé"),
    (13, "Beauté / Bien être"),
    (14, "Mobilité"),
    (16, "Jouets"),
]

sql_insert_categories = sql_utils.get_sql_statement("insert_category_db_prod.sql")
for label in labels:
    cur.execute(
        sql_insert_categories,
        (
            label[0],
            label[1],
        ),
    )
con.commit()
