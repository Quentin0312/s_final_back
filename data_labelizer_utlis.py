import os


def get_already_labelized_image_path(
    labels_file_name: str, unlabeled_images_file_name: str
) -> list[str]:
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

    return already_labelized_images_path


# ! FIX: "s" UTILISÉ POUR 2 CATÉGORIES (SPORT ET MULTIMÉDIA)
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
