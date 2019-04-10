import requests


# Input: url to STAC catalog
# Output: the list of urls to STAC items in the catalog
def get_STAC_items_from_catalog(catalog):
    resp = requests.get(catalog).json()["links"]
    url = catalog.split("catalog.json")[0]

    items = []
    for elem in resp:
        if elem["rel"] != "item":
            continue
        items.append(url + elem["href"])
    return items


def divide_list(items, partitions):
    i = 0
    result = [ [] for _ in range(partitions)]
    while i < len(items):
        result[i%partitions].append(items[i])
        i += 1
    return result