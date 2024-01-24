import sys
import time
import cv2
import sqlite3
from db import sql_utils

"""
Labelisation des pages présents dans la database de training.

Boucle
    - image_path récup depuis db
    - image à afficher
    - input à enregistrer
    - label à save dans un fichiers texte
"""

# TODO: Database de training à mettre en place !
con = sqlite3.connect("./db/db_v1.sqlite")
cur = con.cursor()

select_sql_statement = sql_utils.get_sql_statement("select_training.sql")

response = cur.execute(select_sql_statement).fetchall()
"""
Format:
list[(id_page:int, image_path: str)]
"""

# def loop():
#     while cv2.waitKey(30) == ord("a")

for item in response:
    id_page = item[0]
    image_path = item[1]

    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)

    cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(image_path, width=700, height=1000)
    cv2.imshow(image_path, img)
    label = []
    while True:
        key_pressed = cv2.waitKey(30000)
        if key_pressed == ord("\r"):  # `enter` key
            break
        else:
            print("in else")
            label.append(key_pressed)
    # ! Mettre en place une fonction pour transfomer `label` en int de 0 à 15
    # ! Afficher l'image plus petit
    print("label", label)
    cv2.destroyAllWindows()
