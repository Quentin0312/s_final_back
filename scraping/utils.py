import re
import time
import datetime
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


def wait_sleep_time_is_passed(reference_time, sleep_time: int):
    # Be sure to do 1 request each sleep_time sec
    request_time = datetime.datetime.now()
    if reference_time is None:
        reference_time = request_time
    elif request_time.timestamp() < reference_time.timestamp() + sleep_time:
        time.sleep(reference_time.timestamp() + sleep_time - request_time.timestamp())

    return reference_time
