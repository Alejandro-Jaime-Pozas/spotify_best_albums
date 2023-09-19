import requests, re, openpyxl
from bs4 import BeautifulSoup
from spotify_keys import get_token
from spotify import create_new_playlist, add_tracks_to_playlist
from excel_file import add_album_data_excel

# TODO
#   - need to find a way to reduce the correct albums in black text below 460% similarity by increasing their similarity, and accounting for edge cases with red text above 460% so that they don't create a match

# initial year 1950
year = 1950
end_year = 1960

# create empty list to later add all data
list_data = []

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
            add_tracks_to_playlist(playlist_id, artist_album, year, list_data, access_token)

        # ADD ALL OF THE LIST_DATA FOR ALBUMS TO AN EXCEL FILE
        add_album_data_excel(list_data)
        

    else:
        print(f"status code: {albums_by_year.status_code} - for year {year} in acclaimed music website")

# # ADD ALL OF THE LIST_DATA FOR ALBUMS TO AN EXCEL FILE
# add_album_data_excel(list_data)