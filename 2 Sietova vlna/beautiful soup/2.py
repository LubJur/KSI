import requests
from bs4 import BeautifulSoup
from time import sleep

response = requests.get("https://python.iamroot.eu/extending/")   # Getting response from server
page = response.content # content of response is actually our page
soup = BeautifulSoup(page, "html.parser")   # creating BS object for upcoming scraping

a_tags = soup.find_all("a")
print(a_tags)
num_href = 0

for i in a_tags:
    if len(i.get("href")) >= 30:
        num_href += 1

print(num_href)
sleep(2)

response = requests.get("https://python.iamroot.eu/installing/")   # Getting response from server
page = response.content # content of response is actually our page
soup = BeautifulSoup(page, "html.parser")   # creating BS object for upcoming scraping

a_tags = soup.find_all("a")
print(a_tags)

for i in a_tags:
    if len(i.get("href")) >= 30:
        num_href += 1

print(num_href)
