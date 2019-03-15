import requests
from bs4 import BeautifulSoup


def fetchData(url):
    links = []
    resp = requests.get(url)
    soup = BeautifulSoup("\n".join(resp.text.splitlines()[2:]), "html.parser")
    for i in soup.find_all("a"):
        links.append(i.get("href"))
    del links[0]
    return links


def main():
    url = "https://landsat-pds.s3.amazonaws.com/c1/L8/139/045/LC08_L1TP_139045_20170304_20170316_01_T1/index.html"  # Test data repo

    data = fetchData(url)

    while url[-1] != "/":
        url = url[:-1]

    saveData(data, url)


def saveData(extensions, url):
    for ext in extensions:
        resp = requests.get(url + ext, allow_redirects=True)
        open(ext, "wb").write(resp.content)


if __name__ == "__main__":
    main()
