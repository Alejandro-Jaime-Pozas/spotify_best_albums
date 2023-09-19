import requests, re, json, difflib


# SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT AND RETURN MULTIPLE ALBUM RESULTS
def album_search_list(artist_album, access_token):
    url = f"https://api.spotify.com/v1/search/?q={artist_album}&type=album&limit=50" # CHANGE LIMIT HERE!!
    headers = {'Authorization': f'Bearer {access_token}'}
    search = requests.request("GET", url, headers=headers)
    # print(search.text)
    search_json = search.json() 
    try:
        spotify_results_list = search_json['albums']['items'] # contains multiple album results for search query
    except KeyError:
        print(f'no album info obtained for this search query: {artist_album}')
        spotify_results_list = None 

    return spotify_results_list if spotify_results_list else None 


# CHECK SIMILARITY BW ACCLAIMED VS SPOTIFY RESULTS
def similarity_score(acclaimed, spotify, acclaimed_year, spotify_album_year):
    # Convert the strings to lowercase to make the comparison case-insensitive
    acclaimed = acclaimed.lower()
    spotify = spotify.lower()
    # Remove everythiinng in parentheses or [] from all spotify album names
    spotify = re.sub(r'\([^)]*\)', '', re.sub(r'\[[^\]]*\]', '', spotify))
    # Calculate the similarity ratio between the two strings
    similarity_ratio = difflib.SequenceMatcher(None, acclaimed, spotify).quick_ratio()
    # Check if spotify year = acclaimed year and increase ratio if true
    if similarity_ratio > 0.90:
        similarity_ratio += 3.7
    if acclaimed_year == spotify_album_year:
        similarity_ratio += 0.3
    # Check if 'Deluxe' reduce similarity
    if 'deluxe' in spotify:
        similarity_ratio -= 0.3

    return similarity_ratio


# RETRIEVE INDIVIDUAL ALBUM TRACKS IN ORDER for the highest match
def get_album_tracks(top_album_id, access_token):
    url = f"https://api.spotify.com/v1/albums/{top_album_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    album_tracks = requests.request("GET", url, headers=headers)
    # print(album_tracks.text.encode("utf-8"))
    album_tracks_json = album_tracks.json() 
    tracks = [track['uri'] for track in album_tracks_json['tracks']['items']]
    # print(tracks)
    return tracks


#  FEED LIST OF TRACKS TO THE ADD TO PLAYLIST ENDPOINT
def add_tracks_to_spotify(playlist_id, tracks, access_token, top_album_score):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" 
    payload = json.dumps({"uris": tracks})
    headers = {'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'}
    add_tracks_to_playlist = requests.request("POST", url, headers=headers, data=payload)
    # print(add_tracks_to_playlist.text)

    print(f'album w/similarity = {top_album_score:.2f} was added\n')
    return add_tracks_to_playlist


# FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
# NEED TO CHANGE THIS TO CREATE HIGHER QUALITY MATCHES FOR ARTIST/ALBUMS
def get_album_match(spotify_results_list, acclaimed_music_album_name, year, list_data):

    top_album_score = 0
    top_album_id = None 
    top_album_spotify_name = None 

    for result in spotify_results_list:
        album_id = result['id']
        artist_name = result['artists'][0]['name'] # may need to change encoding here
        album_name = result['name'] # may need to change encoding here
        album_year = int(result['release_date'][:4])
        # print(album_id)
        spotify_search_album_name = f'''{artist_name} {album_name}'''
        similarity = similarity_score(acclaimed_music_album_name, spotify_search_album_name, year, album_year)
        # PRINT RESULTS FROM BOTH SITES, ALONG W/SIMILARITY
        print(f'''REAL ALBUM: {acclaimed_music_album_name} - YEAR: {year}''')
        try:
            print(f'''SPOTIFY SEARCH: {spotify_search_album_name} - YEAR: {album_year}''')
        except UnicodeEncodeError as e:
            print('Unable to print due to Unicode Error!!!')
        print(f'''SIMILARITY: {similarity:.2f}''')
        print()
        if similarity > top_album_score:
            top_album_id = album_id
            top_album_spotify_name = spotify_search_album_name
            top_album_score = similarity

    # ADD THE ALBUM DATA TO A DICTIONARY
    data = {
        'top_album_id': top_album_id, 
        'top_album_spotify_name': top_album_spotify_name, 
        'acclaimed_music_album_name': acclaimed_music_album_name, 
        'top_album_score': top_album_score, 
        'album_found': True if top_album_score > 0.35 else False, 
        'year': year
        }
    list_data.append(data)

    # IF SIMILARTY SCORE IS BELOW X AMOUNT, DON'T ADD THE ALBUM
    if top_album_score < 0.35 or top_album_id == None:
        print(f'there is no match for this album: {acclaimed_music_album_name}')
        return None 
    
    return data 