import requests
from bs4 import BeautifulSoup
import random
import webbrowser


def crawlWikiPage(wiki_url):
    global runs

    if not wiki_url.startswith("https://en.wikipedia.org/wiki/"):
        wiki_url = topic_to_url(wiki_url)

    source = requests.get(url = wiki_url)
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
            
            # Exclude links within a <cite> element
            if link.find_parent("cite"):
                continue

            new_url = link["href"]
            break
    
    runs -= 1

    if runs > 0:
        crawlWikiPage("https://en.wikipedia.org" + new_url)
    else:
        # If crawler has reached the end of its crawling, open the final wikipedia page in the user's browser:
        webbrowser.open("https://en.wikipedia.org" + new_url)

        # and print its title:
        source = requests.get(url = "https://en.wikipedia.org" + new_url)
        soup = BeautifulSoup(source.content, "html.parser")
        title = soup.find(id = "firstHeading")
        print("\n" + title.text + "\n")

def topic_to_url(topic_name: str):
    '''Return the url to the topic's wiki page from the topic name.'''

    separate_words = topic_name.split()
    wiki_topic_name = '_'.join(separate_words)  # Whitespaces in pages' names are substituted with _ in the url
    wiki_url = "https://en.wikipedia.org/wiki/" + wiki_topic_name
    
    return wiki_url

starting_url = input("Wikipedia page you find interesting: ")
depth_of_search = int(input("Depth of search: "))
runs = depth_of_search

crawlWikiPage(starting_url)

while True:
    command = input("Repeat (R) / New (N) / Quit (Q) ").upper()
    if command == "R":
        runs = depth_of_search
        crawlWikiPage(starting_url)
        
    elif command == "N":
        starting_url = input("Wikipedia page you find interesting: ")
        depth_of_search = int(input("Depth of search: "))
        runs = depth_of_search
        crawlWikiPage(starting_url)

    elif command == "Q":
        break