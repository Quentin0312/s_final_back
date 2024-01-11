import re
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


def filter_refs(refs: list):
    for ref in refs:
        if ref[-2:-1] != "":
            if ref[-2:-1] != 9:
                pattern = ref[:-2] + r"[" + str(int(ref[-2:-1]) + 1) + r"-9]\/"
                regex = re.compile(pattern)
                matches = [s for s in refs if regex.search(s)]
                if len(matches) >= 1:
                    refs.remove(ref)


def save_all_refs(refs: list[str]):
    with open("./dataset/scraping/refs.txt", "w") as refs_file:
        for ref in refs:
            refs_file.write(ref + "\n")
        refs_file.close()


# Get all refs
refs = get_refs(url="https://lapub.re/prospectus/?C=M;O=D", regex=r"\d{17}-\d\/")

# Remove duplicate refs
filter_refs(refs)


# Save refs
save_all_refs(refs)
