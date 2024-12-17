import requests
from bs4 import BeautifulSoup
import random
import webbrowser

starting_url = input("Link to a Wikipedia page of a topic you find interesting: ")
depth_of_search = int(input("Depth of search: "))

def crawlWikiPage(url):
    global depth_of_search

    source = requests.get(url = url)
    soup = BeautifulSoup(source.content, "html.parser")

    title = soup.find(id = "firstHeading")
    print(title.text)

    allLinks = soup.find(id = "bodyContent").find_all("a")
    random.shuffle(allLinks)

    for link in allLinks:
        # Only follow links that lead to another wiki page:
        if link.has_attr("href") and link["href"].startswith("/wiki/"):
            # Exclude namespaces like Special:
            if ":" in link["href"]:
                continue

            # Exclude links in the reference list
            if link.find_parent(class_ = "reflist"):
                continue

            # Exclude links in a <table> element
            if link.find_parent("table"):
                continue

            new_url = link["href"]
            break
    
    depth_of_search -= 1

    if depth_of_search > 0:
        crawlWikiPage("https://en.wikipedia.org" + new_url)
    else:
        # If crawler has reached the end of its crawling, open the final wikipedia page in the user's browser:
        webbrowser.open("https://en.wikipedia.org" + new_url)

crawlWikiPage(starting_url)