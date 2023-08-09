import requests, pyperclip
from bs4 import BeautifulSoup

# get a website's response content
r = requests.get('https://www.acclaimedmusic.net/year/1954a.htm')
# print(r.text)

# # Beautiful soup tutorial
soup = BeautifulSoup(r.text, "html.parser")

# print(''.join([c for c in soup.prettify() if ord(c)<128]))
print(soup.title)

with open('main_html.html', 'w', encoding='utf-8') as file:
    file.write(''.join([c for c in soup.prettify() if ord(c)<128]))

# cleaned_prettified = ''.join(c for c in soup.prettify() if ord(c) < 128)
# print(cleaned_prettified.p)

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup2 = BeautifulSoup(html_doc, 'html.parser')

# print(soup2.title)