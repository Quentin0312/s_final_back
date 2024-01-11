import re

from utils import get_refs


def filter_refs(refs: list) -> list:
    new_refs = []
    for ref in refs:
        if ref[-2:-1] != "":
            if ref[-2:-1] != 9:
                pattern = ref[:-2] + r"[" + str(int(ref[-2:-1]) + 1) + r"-9]\/"
                regex = re.compile(pattern)
                matches = [s for s in refs if regex.search(s)]
                if len(matches) == 0:
                    new_refs.append(ref)

    return new_refs


def save_all_refs(refs: list[str]):
    with open("./dataset/scraping/refs.txt", "w") as refs_file:
        for ref in refs:
            refs_file.write(ref + "\n")
        refs_file.close()


# Get all refs
print("\n-----Getting all refs-----")
refs = get_refs(url="https://lapub.re/prospectus/?C=M;O=D", regex=r"\d{17}-\d\/")

# Remove duplicate refs
print("\n----Droping duplicates----")
filtered_refs = filter_refs(refs)


# Save refs
print("\n----------Saving----------")
save_all_refs(filtered_refs)
