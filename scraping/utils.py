import re
import time
import requests
from bs4 import BeautifulSoup


def get_refs(url: str, regex) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    pattern = re.compile(regex)

    specific_links = soup.find_all("a", href=pattern)

    refs = []
    for link in specific_links:
        refs.append(link.text)

    return refs


# def wait_sleep_time_is_passed(reference_time, sleep_time: int):
#     # Be sure to do 1 request each sleep_time sec
#     request_time = datetime.datetime.now()
#     # if :
#     # reference_time = request_time
#     if (
#         reference_time is not None
#         and reference_time.timestamp() + sleep_time > request_time.timestamp()
#     ):
#         time.sleep(reference_time.timestamp() + sleep_time - request_time.timestamp())
#         # reference_time = request_time


#     # return reference_time
#     return request_time


def force_wait_sleep_time(sleep_time: int):
    time.sleep(sleep_time)


# TODO: Create list of dict instead !
def get_full_links_from_file() -> list[list[str]]:
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
