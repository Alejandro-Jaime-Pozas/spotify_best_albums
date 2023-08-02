import requests, pyperclip
from bs4 import BeautifulSoup

# get a website's response content
r = requests.get('https://www.rollingstone.com/music/music-lists/50-best-albums-of-2016-119690/')
# print(r.content)


# # Beautiful soup tutorial
# doc = BeautifulSoup(r.text, "html.parser")
# text = doc.find_all("p")
# print(text)

