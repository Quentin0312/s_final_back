# import cv2
import os

import cv2

image_paths = []

catalogs = os.listdir("./dataset")
catalogs.sort()

for catalog in catalogs[:200]:
    image_list = os.listdir(f"./dataset/{catalog}")
    image_list.sort()
    image_paths.append(f"./dataset/{catalog}/{image_list[0]}")


def are_images_similar(image1_path, image2_path, threshold=0.8):
    # Load images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute structural similarity index
    result = cv2.matchTemplate(gray_image1, gray_image2, cv2.TM_CCOEFF_NORMED)

    # Get the maximum similarity score
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the maximum similarity score exceeds the threshold
    if max_val >= threshold:
        return True
    else:
        return False


for i in range(len(image_paths)):
    print("i", i)
    for j in range(len(image_paths[i:]))[:-1]:
        print("j", j)
        try:
            result = are_images_similar(image_paths[i], image_paths[i + j + 1])
            if result:
                print("---")
                print(image_paths[i], image_paths[i + j + 1])
                with open("./similar_images.txt", "w") as file:
                    file.write(image_paths[i], image_paths[i + j + 1])
                    file.close()

        except Exception as error:
            print("error", error)
            print(image_paths[i], image_paths[i + j + 1])
