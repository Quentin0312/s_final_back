import os
import datetime
import requests
import shutil

import utils


def is_file_already_stored(ref: str, file_name: str, today: str) -> bool:
    """
    Also create folder if non existent
    """
    ref_folder_name = ref[:-1]
    if ref_folder_name not in os.listdir("./dataset"):
        os.makedirs(f"./dataset/{ref}")
        return False
    else:
        if file_name in os.listdir(f"./dataset/{ref_folder_name}"):
            log_info = (
                "Already stored"
                + " | Ref: "
                + ref_folder_name
                + " | File: "
                + file_name
            )

            write_log(today, to_write=log_info)

            return True
        else:
            return False


def write_log(today: str, to_write: str, error=False):
    if error:
        location = f"./scraping/logs/error/{today}_ERROR.txt"
    else:
        location = f"./scraping/logs/{today}.txt"

    with open(location, "a") as log_file:
        print(to_write)
        log_file.write("\n" + to_write)
        log_file.close()


def download_image(url: str, ref: str, file_name: str, today: str):
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
            image_file.close()

        write_log(today, to_write=log_info)
    else:
        error_log_info = " ERROR: Status code: " + res.status_code + log_info
        write_log(today, to_write=error_log_info, error=True)


# TODO: Use beginning start instead (with seconds)
today = datetime.date.today().strftime("%Y-%m-%d")

print("\n----------Fetching links from local file----------")
links = utils.get_full_links_from_file()

print("\n----------Download images----------")
# reference_time = None
for link in links:
    url = link[0]
    ref = link[
        1
    ]  # TODO: Fix: at the end of the file this index out of range beacuse "" is the raw data
    file_name = link[2]
    if not is_file_already_stored(ref, file_name, today):
        # Wait for sleep_time to be over
        # reference_time = wait_sleep_time_is_passed(reference_time, sleep_time=60)

        # Download image if not already stored
        download_image(url, ref, file_name, today)

        utils.force_wait_sleep_time(15)  # ! Dirty fix
