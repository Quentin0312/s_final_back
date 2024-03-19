import cv2
import sqlite3

from db import sql_utils
import data_labelizer_utlis

# TODO: Pour rester cohérent, commentaires et noms de variables à garder en anglais
"""
Labelisation des pages présents dans la database de training.

- Récupération de n 'image_path' image_path depuis la db
- Récupérer la liste d' 'image_path' des images déjà labelisé

Boucle (chaque 'image_path')
    - Affichage de l'image
    - Label input de l'utilisateur enregistré dans un fichiers .txt
"""

# con = sqlite3.connect("./db/db_training_v1.sqlite")
con = sqlite3.connect("./db/db_analytic_multi-class.sqlite")

cur = con.cursor()

select_sql_statement = sql_utils.get_sql_statement("select_training.sql")

response = cur.execute(select_sql_statement).fetchall()
"""
Format:
list[(id_page:int, image_path: str)]
"""


labels_file_name = "labels_multi-class.txt"
unlabeled_images_file_name = "unlabeled_images_multi-class.txt"

already_labelized_images_path = data_labelizer_utlis.get_already_labelized_image_path(
    labels_file_name, unlabeled_images_file_name
)

print("already labelized images =>", len(already_labelized_images_path))


def listen_keys():
    """
    Listen inputed keys and save labels in file
    """

    labels = ""
    for i in range(16):
        # Get key pressed
        key_pressed = cv2.waitKey(0)

        if key_pressed == ord(" "):
            # If image has no label (no product on it)
            if labels == "":
                with open(
                    f"./{unlabeled_images_file_name}", "a"
                ) as unlabeled_images_file:
                    unlabeled_images_file.write(image_path + "\n")
                    unlabeled_images_file.close()
                    cv2.destroyAllWindows()
                return

            # If all label key already pressed
            else:
                break

        # Get label from key pressed
        label = data_labelizer_utlis.get_label_from_key_pressed(key_pressed)
        if i == 0:
            labels += str(label)
        else:
            labels += "," + str(label)

    # Save in file
    with open(f"./{labels_file_name}", "a") as labels_file:
        labels_file.write(image_path + "|" + str(labels) + "\n")
        labels_file.close()


# For each images of training dataset
for item in response:
    id_page = item[0]
    image_path = item[1]

    # If image already labelized
    if image_path in already_labelized_images_path:
        continue

    # Display image
    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
    cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(image_path, width=700, height=1000)
    cv2.imshow(image_path, img)

    # Listen inputed keys and save labels in file
    listen_keys()

    # Destroy image displayed windows
    cv2.destroyAllWindows()
