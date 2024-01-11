import os
import datetime
import requests
import shutil

from utils import wait_sleep_time_is_passed


def open_full_links_file() -> list:  # TODO: Préciser en com le format de la liste
    """
    Format: [[URL, ref, file_name],...]
    """
    links = []
    with open("./scraping/full_links.txt", "r") as links_file:
        file_content = links_file.read().split("\n")
        links_file.close()

    for link in file_content:
        links.append(link.split("|"))

    return links


def is_file_already_stored(ref: str, file_name: str) -> bool:
    """
    Also create folder if non existent
    """
    ref_folder_name = ref[:-1]
    if ref_folder_name not in os.listdir("./dataset"):
        os.makedirs(f"./dataset/{ref}")
        return False
    else:
        if file_name in os.listdir(f"./dataset/{ref_folder_name}"):
            return True
        else:
            return False


def download_image(url: str, ref: str, file_name: str):
    res = requests.get(url, stream=True)
    log_info = (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + " | Ref: "
        + ref
        + " | File: "
        + file_name
    )

    if res.status_code == 200:
        with open(f"./dataset/{ref}/{file_name}", "wb") as image_file:
            shutil.copyfileobj(res.raw, image_file)
        print(log_info)
    else:
        print("Image Couldn't be retrieved: " + url)
        with open(f"./scraping/logs/{today}.txt", "a") as log_file:
            log_file.write("\n ERROR: " + log_info)
            log_file.close()


today = datetime.date.today().strftime("%Y-%m-%d")

print("\n----------Fetching links from local file----------")
links = open_full_links_file()

print("\n----------Download images----------")
reference_time = None
for link in links:
    url = link[0]
    ref = link[1]
    file_name = link[2]
    if not is_file_already_stored(ref, file_name):
        # Wait for sleep_time to be over
        reference_time = wait_sleep_time_is_passed(reference_time, sleep_time=60)

        # Download image if not already stored
        download_image(url, ref, file_name)
