import re
import os
import datetime

from utils import get_refs, force_wait_sleep_time


def open_refs_file() -> list[str]:
    with open("./scraping/refs.txt", "r") as refs_file:
        refs = refs_file.read().split("\n")
        return refs[:-1]


def get_filtered_refs() -> list[str]:
    """
    Get all_refs from file
    and filter the refs of data already downloaded
    """
    all_refs = open_refs_file()
    refs_already_downloaded = os.listdir("./dataset")
    filtered_refs = []

    for ref in all_refs:
        if ref[:-1] not in refs_already_downloaded:
            filtered_refs.append(ref)

    return filtered_refs


# TODO: Add log system !
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


def save_full_links(prospectus: dict):
    with open("./scraping/full_links.txt", "w") as file:
        for ref in list(prospectus.keys()):
            for file_name in prospectus[ref]:
                file.write(
                    f"https://lapub.re/prospectus/{ref}HTML/files/assets/common/page-html5-substrates/{file_name}|"
                    + ref
                    + "|"
                    + file_name
                    + "\n"
                )
        file.close()


print("\n-----Fetch refs from files-----")
refs = get_filtered_refs()

print("\n-----Fetch file names from web-----")
prospectus = get_all_files_names(
    refs[:10], sleep=60
)  # ! Change to the full refs list to get alls

print("\n-----Remove low quality file names-----")
remove_lower_quality_image_names(prospectus)

print("\n-----Saving-----")
save_full_links(prospectus)

print("Done")
