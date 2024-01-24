import os
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

con = sqlite3.connect("./db/db_training_v1.sqlite")
cur = con.cursor()

select_sql_statement = sql_utils.get_sql_statement("select_training.sql")

response = cur.execute(select_sql_statement).fetchall()
"""
Format:
list[(id_page:int, image_path: str)]
"""


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


labels_file_name = "labels.txt"
unlabeled_images_file_name = "unlabeled_images.txt"
# TODO: Put in utils file
already_labelized_images_path = []
if labels_file_name in os.listdir("./"):
    with open(f"./{labels_file_name}", "r") as labels_file:
        lines = labels_file.read().split("\n")
        for info in lines[:-1]:  # * last line is ""
            image_path = info.split("|")[0]
            already_labelized_images_path.append(image_path)

        labels_file.close()

if unlabeled_images_file_name in os.listdir("./"):
    with open(f"./{unlabeled_images_file_name}") as unlabeled_images_file:
        [
            already_labelized_images_path.append(image_path)
            for image_path in unlabeled_images_file.read().split("\n")[
                :-1
            ]  # * last line is ""
        ]
        unlabeled_images_file.close()

print("already_labelized_images", already_labelized_images_path)

for item in response:
    id_page = item[0]
    image_path = item[1]

    # If image already labelizes
    if image_path in already_labelized_images_path:
        continue

    # Display image
    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)

    cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(image_path, width=700, height=1000)
    cv2.imshow(image_path, img)

    # Get label inputed
    key_pressed = cv2.waitKey(0)

    # If image has no label (no product on it)
    if key_pressed == ord(" "):
        with open(f"./{unlabeled_images_file_name}", "a") as unlabeled_images_file:
            unlabeled_images_file.write(image_path + "\n")
            unlabeled_images_file.close()
            cv2.destroyAllWindows()
        continue

    label = get_label_from_key_pressed(key_pressed)

    print("label", label)
    cv2.destroyAllWindows()

    # Save in file
    with open(f"./{labels_file_name}", "a") as labels_file:
        labels_file.write(image_path + "|" + str(label) + "\n")
        labels_file.close()
