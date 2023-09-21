import requests, re
from bs4 import BeautifulSoup
from spotify_keys import get_token
from spotify import create_new_playlist, add_tracks_to_playlist
from excel_file import add_album_data_excel

# TODO
#   - analyze outcomes of excel file to see how best to account for the most album matches while removing those that don't match

# initial year 1950
start_year = 1954
end_year = 1963

# create empty list to later add all data
list_data = []

# FOR EACH YEAR
for accl_year in range(start_year, end_year): # CHANGE TO END_YEAR
    print('='*50)
    print(accl_year)

    # get website's response content
    albums_by_year = requests.get(f'https://www.acclaimedmusic.net/year/{accl_year}a.htm')
    # print(albums_by_year.text)

    if albums_by_year.status_code == 200:

        # CREATE Beautiful soup object
        soup = BeautifulSoup(albums_by_year.text, "html.parser")#.prettify().encode('utf-8')
        soup_str = ''.join([c for c in soup.prettify() if ord(c)<128]) # get alphanum chars only
        pattern = r'<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>\s*<td>\s*<a href="[^"]*">\s*(.*?)\s*</a>\s*</td>'
        matches = re.findall(pattern, soup_str, re.DOTALL)

        # CREATE LIST WITH ARTIST AND ALBUM FORMATTED FOR URL PARAMS
        # need to...separate the acclaimed artist and album names..then spotify as well in order to compare...then 
        artists_albums_search = []
        for match in matches:
            # HERE MAYBE CHANGE THE CHARS THAT ARE BEING MAPPED I.E. turn é into e
            accl_artist = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[0]).replace(' amp ', ' ').strip()
            accl_album = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[1]).replace(' amp ', ' ').strip()
            artists_albums_search.append((accl_artist, accl_album))
        # print(artists_albums_search)

        # GET THE ACCESS TOKEN FOR SPOTIFY API
        access_token = get_token()

        # CREATE A PLAYLIST FOR CURRENT YEAR
        playlist_id = create_new_playlist(accl_year, access_token)

        # FOR EACH ALBUM IN ARTISTS_ALBUMS SEARCH THE ALBUM AND ADD TRACKS TO NEW PLAYLIST
        for accl_artist, accl_album in artists_albums_search:
            add_tracks_to_playlist(playlist_id, accl_artist, accl_album, accl_year, list_data, access_token)

        # ADD ALL OF THE LIST_DATA FOR ALBUMS TO AN EXCEL FILE
        add_album_data_excel(list_data)
        

    else:
        print(f"status code: {albums_by_year.status_code} - for year {accl_year} in acclaimed music website")

# # ADD ALL OF THE LIST_DATA FOR ALBUMS TO AN EXCEL FILE
# add_album_data_excel(list_data)