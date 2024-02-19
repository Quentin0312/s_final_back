import re
import datetime
import shutil
import time
import requests
from bs4 import BeautifulSoup


def get_dates(href: str) -> tuple[str, str]:
    response = requests.get("https://lapub.re/" + href)
    time.sleep(2)
    soup = BeautifulSoup(response.text, "html.parser")
    start_date = soup.find(id="tzA16").text
    end_date = soup.find(id="tzA17").text

    return (start_date, end_date)


def save_dates(ref: str, start_date: str, end_date: str) -> None:
    with open("./catalog_dates.txt", "a") as catalog_dates_file:
        catalog_dates_file.write(ref + "|" + start_date + "|" + end_date + "|" + "\n")


# TODO: Refactor
def get_refs(url: str, regex) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    pattern = re.compile(regex)

    specific_links = soup.find_all("a", href=pattern)

    refs = []
    for link in specific_links:
        refs.append(link.text)

    return refs


# TODO: Refactor
def remove_lower_quality_image_names(prospectus: dict[str, list[str]]) -> dict:
    for i in range(
        100
    ):  # TODO: Fix to not have to use this anymore (recurcive fn that restart with the array each time)
        for ref in list(prospectus.keys()):
            for file_name in prospectus[ref]:
                pattern = (
                    file_name[:9]
                    + r"["
                    + str(int(file_name[9:10]) + 1)
                    + r"-9]"
                    + ".jpg"
                )
                regex = re.compile(pattern)
                matches = [s for s in prospectus[ref] if regex.search(s)]

                if len(matches) >= 1:
                    prospectus[ref].remove(file_name)


# TODO: Refactor
def get_all_files_names(refs: list[str], sleep: int) -> dict:
    prospectus = {}
    # reference_time = None
    # Get all file names
    for ref in refs:
        # Wait sleep time to be passed
        # reference_time = wait_sleep_time_is_passed(reference_time, sleep_time=30)

        image_file_names = get_refs(
            url=f"https://lapub.re/prospectus/{ref}HTML/files/assets/common/page-html5-substrates/",
            regex=r"page\d{4}_\d\.jpg",
        )
        print(
            datetime.datetime.now(),
            f"=> https://lapub.re/prospectus/{ref}HTML/files/assets/common/page-html5-substrates/",
        )
        force_wait_sleep_time(sleep)  # ! Dirty fix

        prospectus[ref] = image_file_names

    return prospectus


# TODO: Refactor
def force_wait_sleep_time(sleep_time: int):
    time.sleep(sleep_time)


# TODO: Refactor
def download_image(url: str, ref: str, file_name: str) -> None:
    res = requests.get(url, stream=True)
    log_info = (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + " | Ref: "
        + ref
        + " | File: "
        + file_name
    )

    if res.status_code == 200:
        with open(f"../../prod_dataset/{ref}/{file_name}", "wb") as image_file:
            shutil.copyfileobj(res.raw, image_file)
            image_file.close()
    else:
        error_log_info = " ERROR: Status code: " + res.status_code + log_info
        print(error_log_info)


def get_full_links(ref: str) -> list[str]:
    catalog_dict = get_all_files_names([ref], sleep=2)
    remove_lower_quality_image_names(catalog_dict)

    links = []
    for ref in list(catalog_dict.keys()):
        for file_name in catalog_dict[ref]:
            links.append(
                f"https://lapub.re/prospectus/{ref}HTML/files/assets/common/page-html5-substrates/{file_name}"
            )

    return links


def download_all_images(links: list[str], ref: str) -> None:
    for link in links:
        download_image(link, ref, link.split("/")[-1])
        force_wait_sleep_time(1)
