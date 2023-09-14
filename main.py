import requests, re, difflib
from bs4 import BeautifulSoup
from spotify_keys import get_token
from spotify import create_new_playlist, add_tracks_to_playlist

# fully working, may need to clean up searches that dont match, or leave as is and clean up manually in spotify while storing the albums that dont match from code. 

# TODO
#         - for main code:
#                 - only add matching albums on spotify, if not found don't add (but store in text file missing album)
#                 - ideally, only add original songs from albums, no deluxe/ultimate/bonus/live tracks
#                         - maybe to avoid deluxe albums, return 2-3 album results, and grab best matching album
#         - fix timeout error occurring related to requests package not communicating w/spotify api correctly resuling in timeout error
#         - create a word/excel file or csv to store all artists and album and year info, and whether there was a successful result when searching for album

# include this later in for loop / while loop with changing number, initial year 1954
year = 1997
end_year = 2020

# FOR EACH YEAR
for year in range(year, end_year): # CHANGE TO END_YEAR
    print('='*50)
    print(year)

    # get website's response content
    albums_by_year = requests.get(f'https://www.acclaimedmusic.net/year/{year}a.htm')
    # print(r.text)

    if albums_by_year.status_code == 200:

        # CREATE Beautiful soup object
        soup = BeautifulSoup(albums_by_year.text, "html.parser")#.prettify().encode('utf-8')
        soup_str = ''.join([c for c in soup.prettify() if ord(c)<128]) # get alphanum chars only
        pattern = r'<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>\s*<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>'
        matches = re.findall(pattern, soup_str, re.DOTALL)

        # CREATE LIST WITH ARTIST AND ALBUM FORMATTED FOR URL PARAMS
        artists_albums_search = []
        for match in matches:
            artist = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[0]).replace(' amp ', ' ').strip().replace(' ', '%20')
            album = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[1]).replace(' amp ', ' ').strip().replace(' ', '%20')
            artists_albums_search.append(f"{artist}%20{album}")
        # print(artists_albums_search)

        # GET THE ACCESS TOKEN FOR SPOTIFY API
        access_token = get_token()

        # CREATE A PLAYLIST FOR CURRENT YEAR
        playlist_id = create_new_playlist(year, access_token)

        # FOR EACH ALBUM IN ARTISTS_ALBUMS SEARCH THE ALBUM AND ADD TRACKS TO NEW PLAYLIST
        for artist_album in artists_albums_search:
            add_tracks_to_playlist(playlist_id, artist_album, year, access_token)

    else:
        print(f"status code: {albums_by_year.status_code} - for year {year} in acclaimed music website")