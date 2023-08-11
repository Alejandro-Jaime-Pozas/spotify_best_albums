import requests,  re
from bs4 import BeautifulSoup

# include this later in for loop / while loop
current_year = 1967

# get a website's response content
r = requests.get(f'https://www.acclaimedmusic.net/year/{current_year}a.htm')
# print(r.text)

if r.status_code == 200:

    # # Beautiful soup tutorial
    soup = BeautifulSoup(r.text, "html.parser")#.prettify().encode('utf-8')

    soup_str = ''.join([c for c in soup.prettify() if ord(c)<128])

    pattern = r'<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>\s*<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>'
    matches = re.findall(pattern, soup_str, re.DOTALL)

    cleaned_data = []

    for match in matches:
        artist = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[0]).replace(' amp ', ' ').strip()

        album = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[1]).replace(' amp ', ' ').strip()

        cleaned_data.append((artist, album))

    for artist, album in cleaned_data:
        print("Artist:", artist)
        print("Album:", album)
        print()

else:
    print(r.status_code)