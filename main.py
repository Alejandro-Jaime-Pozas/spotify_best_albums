import requests, re
from bs4 import BeautifulSoup
from spotify_keys import get_tokens, api_code
from spotify import create_new_playlist, add_tracks_to_playlist

# include this later in for loop / while loop with changing number, initial year 1954
year = 1954
end_year = 2020

# get website's response content
r = requests.get(f'https://www.acclaimedmusic.net/year/{year}a.htm')
# print(r.text)

if r.status_code == 200:

    # Beautiful soup
    soup = BeautifulSoup(r.text, "html.parser")#.prettify().encode('utf-8')

    soup_str = ''.join([c for c in soup.prettify() if ord(c)<128]) # alphanum chars only

    pattern = r'<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>\s*<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>'
    matches = re.findall(pattern, soup_str, re.DOTALL)

    artists_albums = []

    for match in matches:
        artist = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[0]).replace(' amp ', ' ').strip().replace(' ', '%20')
        album = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[1]).replace(' amp ', ' ').strip().replace(' ', '%20')
        artists_albums.append(f"{artist}%20{album}")
    print(artists_albums)

    # # CREATE A PLAYLIST FOR CURRENT YEAR
    # playlist_id = create_new_playlist(year)

    # # FOR EACH ALBUM IN ARTISTS_ALBUMS SEARCH THE ALBUM AND ADD TRACKS TO NEW PLAYLIST
    # for album in artists_albums:
    #     add_tracks_to_playlist(playlist_id, album)

else:
    print(r.status_code)

# need to connect to spotify api and handle all of the requests from here:
    # GET oauth 2.0 code
    # POST oath 2.0 code for token


	# Steps:
	# 	1. get required access token for all api calls
    #   2. for each year 1954-2019, 
    #       create a new playlist on spotify. ie "1954 Best Albums"
	# 	3. for each of the albums for each year:
    #       search for the artist/album pair in search endpoint, retrieve all tracks in order
    #       compile a list of the tracks to add by relevant track id
    #       feed list of tracks to the add to playlist endpoint