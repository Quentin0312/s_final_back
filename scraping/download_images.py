import requests
import shutil

url = "https://img.freepik.com/photos-gratuite/jetee-au-bord-lac-hallstatt-autriche_181624-44201.jpg"

file_name = "image_test.jpg"

res = requests.get(url, stream=True)

if res.status_code == 200:
    with open(file_name, "wb") as image_file:
        shutil.copyfileobj(res.raw, image_file)
    print("Image sucessfully Downloaded: ", file_name)
else:
    print("Image Couldn't be retrieved")
