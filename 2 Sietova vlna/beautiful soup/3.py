import requests
from bs4 import BeautifulSoup
from time import sleep

response = requests.get("https://python.iamroot.eu/tutorial/")   # Getting response from server
page = response.content # content of response is actually our page
soup = BeautifulSoup(page, "html.parser")   # creating BS object for upcoming scraping

p_tags = soup.find_all("p")
#print(p_tags)
num_a = 0

for i in range(4):
    paragraf = str(p_tags[i]).split()
    for j in paragraf:
        if j.startswith("a") or j.startswith("A"):
            num_a += 1

print(num_a)
