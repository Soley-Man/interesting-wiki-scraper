import requests
from bs4 import BeautifulSoup
import random

starting_url = "https://en.wikipedia.org/wiki/Web_scraping"

source = requests.get(url = starting_url)
soup = BeautifulSoup(source.content, "html.parser")

title = soup.find(id = "firstHeading")
print(title.text)

allLinks = soup.find(id = "bodyContent").find_all("a")
random.shuffle(allLinks)

for link in allLinks:
    # Only follow links that lead to another wiki page:
    if link["href"].startswith("/wiki/"):
        # Exclude namespaces like Special:
        if ":" in link["href"]:
            continue

        # Exclude links in the reference list
        if link.find_parent(class_ = "reflist"):
            continue

        # Exclude links in a <table> element
        if link.find_parent("table"):
            continue

        print(link["href"])