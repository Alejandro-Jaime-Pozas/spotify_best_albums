import requests, re
from bs4 import BeautifulSoup
from spotify_keys import get_token
from spotify import access_token, create_new_playlist, add_tracks_to_playlist

# fully working, may need to clean up searches that dont match, or leave as is and clean up manually in spotify while storing the albums that dont match from code. missing spotify access_token functionality, will need to check for refresh_token to make that work, will need to wait 1hr for refresh to go into effect to test out

# include this later in for loop / while loop with changing number, initial year 1954
year = 1995
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
        artists_albums = []
        for match in matches:
            artist = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[0]).replace(' amp ', ' ').strip().replace(' ', '%20')
            album = re.sub(r'[^a-zA-Z0-9\s]', ' ', match[1]).replace(' amp ', ' ').strip().replace(' ', '%20')
            artists_albums.append(f"{artist}%20{album}")
        # print(artists_albums)

        # CREATE A PLAYLIST FOR CURRENT YEAR
        playlist_id = create_new_playlist(year)

        # FOR EACH ALBUM IN ARTISTS_ALBUMS SEARCH THE ALBUM AND ADD TRACKS TO NEW PLAYLIST
        for album in artists_albums:
            print(f'''REAL ALBUM: {album.replace('%20', ' ')} - YEAR: {year}''')
            add_tracks_to_playlist(playlist_id, album)
            print()

    else:
        print(f"status code: {albums_by_year.status_code} - for year {year}")