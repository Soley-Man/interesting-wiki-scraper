import requests
from bs4 import BeautifulSoup
import random

starting_url = "https://en.wikipedia.org/wiki/Web_scraping"

source = requests.get(url = starting_url)
soup = BeautifulSoup(source.content, "html.parser")

title = soup.find(id="firstHeading")
print(title.text)