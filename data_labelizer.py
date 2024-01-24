import cv2
import sqlite3
from db import sql_utils

"""
Labelisation des pages présents dans la database de training.

- Récupération de 'image_path' de n image_path depuis la db

Boucle (chaque 'image_path')
    - Affichage de l'image
    - Label input de l'utilisateur enregistré dans un fichiers .txt
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

# ! Filter response of image that already have labels (check labels.txt) !


# TODO: Put in utils file
def get_label_from_key_pressed(key: int) -> int:
    key_label_mapping = {
        ord("d"): 0,
        ord("e"): 1,
        ord("s"): 2,
        ord("a"): 3,
        ord("p"): 4,
        ord("t"): 5,
        ord("i"): 6,
        ord("h"): 7,
        ord("b"): 8,
        ord("c"): 9,
        ord("m"): 10,
        ord("s"): 11,
        ord("."): 12,
        ord("q"): 13,
        ord("v"): 14,
        ord("j"): 15,
    }

    return key_label_mapping[key]


for item in response:
    id_page = item[0]
    image_path = item[1]

    # Display image
    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)

    cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(image_path, width=700, height=1000)
    cv2.imshow(image_path, img)

    # Get label inputed
    key_pressed = cv2.waitKey(0)

    label = get_label_from_key_pressed(key_pressed)

    print("label", label)
    cv2.destroyAllWindows()

    # Save in file
    with open("./labels.txt", "a") as labels_file:
        labels_file.write(image_path + "|" + str(label) + "\n")
        labels_file.close()
