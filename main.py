import requests, re
from bs4 import BeautifulSoup
from spotify_keys import get_token
from spotify import create_new_playlist, add_tracks_to_playlist
from excel_file import add_album_data_excel

# TODO
#   - clean spotify year playlists based on albums that are NOT a match

# initial year 1950 end year 2020
start_year =  1950
end_year = 2010
genres = []
# create empty list to later add all data
list_data = []

# FOR EACH YEAR
for accl_year in range(start_year, end_year): # CHANGE CODE BACK!!!
# for accl_year in genres:
# for accl_year in range(1):
    print('='*50)
    print(accl_year)

    # get website's response content
    albums_by_year = requests.get(f'https://www.acclaimedmusic.net/year/{accl_year}a.htm') # CHANGE CODE BACK!!!
    # albums_by_year = requests.get(f'https://www.acclaimedmusic.net/year/2010-19a.htm')
    # albums_by_year = requests.get(f'https://www.acclaimedmusic.net/genre/genre{accl_year}.htm')
    # print(albums_by_year.text)

    if albums_by_year.status_code == 200:

        # CREATE Beautiful soup object
        soup = BeautifulSoup(albums_by_year.text, "html.parser")#.prettify().encode('utf-8')
        soup_str = ''.join([c for c in soup.prettify() if ord(c)<128]) # get alphanum chars only
        pattern = r'<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>\s*<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>'
        matches = re.findall(pattern, soup_str, re.DOTALL)
        genre_pattern = r'<div class="auto-style1">\s*<strong>\s*(.*?)\s*</strong>\s*</div>'
        genre_match = re.search(genre_pattern, soup_str, re.DOTALL)
        # print(genre_match)
        if genre_match:
            genre_text = genre_match.group(1)
            print(genre_text)

        # CREATE LIST WITH ARTIST AND ALBUM FORMATTED FOR URL PARAMS
        # need to...separate the acclaimed artist and album names..then spotify as well in order to compare...then 
        artists_albums_search = []
        for match in matches:
            # HERE MAYBE CHANGE THE CHARS THAT ARE BEING MAPPED I.E. turn é into e
            accl_artist =  match[0].replace(' &amp; ', '').strip()
            accl_album =  match[1].replace(' &amp; ', '').strip()
            # accl_artist = re.sub(r'[^a-zA-Z0-9.\/\'\s]', ' ', match[0]).replace(' amp ', ' ').strip()
            # accl_album = re.sub(r'[^a-zA-Z0-9.\/\'\s]', ' ', match[1]).replace(' amp ', ' ').strip()
            artists_albums_search.append((accl_artist, accl_album))
        # print(artists_albums_search)

        # GET THE ACCESS TOKEN FOR SPOTIFY API
        access_token = get_token()

        # CREATE A PLAYLIST FOR CURRENT YEAR
        playlist_id = create_new_playlist(accl_year, access_token) # CHANGE BACK!@!!
        # playlist_id = create_new_playlist(genre_text, access_token) # CHANGE BACK!!!!   

        # FOR EACH ALBUM IN ARTISTS_ALBUMS SEARCH THE ALBUM AND ADD TRACKS TO NEW PLAYLIST
        for accl_artist, accl_album in artists_albums_search:
            add_tracks_to_playlist(playlist_id, accl_artist, accl_album, accl_year, list_data, access_token)

        # ADD ALL OF THE LIST_DATA FOR ALBUMS TO AN EXCEL FILE
        add_album_data_excel(list_data)
        

    else:
        print(f"status code: {albums_by_year.status_code} - for year {accl_year} in acclaimed music website")