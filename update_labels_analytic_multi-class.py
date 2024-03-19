import sqlite3
from db import sql_utils

db_file_name = "db_analytic_multi-class.sqlite"
labels_file_name = "labels_multi-class.txt"

con = sqlite3.connect(f"./db/{db_file_name}")
cur = con.cursor()

# ̣ Get all labels values from labels_file
labels_dict = {}
"""
Format: {[image_path: str]: labels:str}
"""
with open(f"./{labels_file_name}", "r") as labels_file:
    lines = labels_file.read().split("\n")[:-1]
    for line in lines:
        line_info = line.split("|")
        labels_dict[line_info[0]] = line_info[1]

    labels_file.close()

#  Insert in db

category_data_dict = {
    0: "Décoration / Meubles / Aménagement intérieur",
    1: "Électroménager  / Ustensiles / équipement de maison (caméra)",
    2: "Multimédia (son, TV)",
    3: "Aménagement ext / Jardin / Piscine / Animalerie",
    4: "Papeterie",
    5: "Téléphone",
    6: "Informatique",
    7: "Produits alimentaire et grande consommation",
    8: "Bricolage / Bâtiments / Travaux maison",
    9: "Culture (livres, jeux-vidéos, musique)",
    10: "Mode (bijoux, …) / Vêtements / Chaussure",
    11: "Sport / AP",
    12: "Bébé",
    13: "Beauté / Bien être",
    14: "Véhicule (auto, moto, trottinette,...)",
    16: "Jouets",
}  # Add "unlabeled" label ?

sql_update_statement = sql_utils.get_sql_statement(
    "update_category_analytic_multi-class.sql"
)

for key in list(labels_dict.keys()):
    cur.execute(sql_update_statement, (labels_dict[key], key))

con.commit()
