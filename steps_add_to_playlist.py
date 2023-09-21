import requests, re, json, difflib


# SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT AND RETURN MULTIPLE ALBUM RESULTS
def album_search_list(accl_artist, accl_album, access_token):
    artist_album = f'''{accl_artist.replace(' ', '%20')}%20{accl_album.replace(' ', '%20')}'''
    url = f"https://api.spotify.com/v1/search/?q={artist_album}&type=album&limit=50" # CHANGE LIMIT HERE!!
    headers = {'Authorization': f'Bearer {access_token}'}
    search = requests.request("GET", url, headers=headers)
    # print(search.text)
    search_json = search.json() 
    try:
        spotify_results_list = search_json['albums']['items'] # contains multiple album results for single search query
    except KeyError:
        print(f'no album info obtained for this spotify search query: {artist_album}')
        spotify_results_list = None 

    return spotify_results_list if spotify_results_list else None 


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
def add_tracks_to_spotify(playlist_id, tracks, access_token, top_album_overall_score):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" 
    payload = json.dumps({"uris": tracks})
    headers = {'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'}
    add_tracks_to_playlist = requests.request("POST", url, headers=headers, data=payload)
    # print(add_tracks_to_playlist.text)

    print(f'album w/similarity = {top_album_overall_score:.2f} was added\n')
    return add_tracks_to_playlist


# CHECK SIMILARITY BW ACCLAIMED VS SPOTIFY RESULTS
def similarity_score(accl_artist, 
                     accl_album, 
                     spot_artist_name, 
                     spot_album_name,
                     accl_year, 
                     spot_album_year):
    # Convert the strings to lowercase to make the comparison case-insensitive
    accl_artist, accl_album = accl_artist.lower(), accl_album.lower()
    spot_artist_name, spot_album_name = spot_artist_name.lower(), spot_album_name.lower()
    # Remove everythiinng in parentheses or [] from all spotify album names
    spot_album_name_clean = re.sub(r'\([^)]*\)', '', re.sub(r'\[[^\]]*\]', '', spot_album_name))
    # Calculate the similarity ratio between the two strings
    artist_similarity_ratio = difflib.SequenceMatcher(None, accl_artist, spot_artist_name).quick_ratio()
    album_similarity_ratio = difflib.SequenceMatcher(None, accl_album, spot_album_name_clean).quick_ratio()
    accl_artist_album = f'''{accl_artist} {accl_album}'''
    spot_artist_album = f'''{spot_artist_name} {spot_album_name_clean}'''
    overall_similarity_ratio = difflib.SequenceMatcher(None, accl_artist_album, spot_artist_album).quick_ratio()

    # CREATE A SCORE SYSTEM SO THAT THE HIGHEST MATCHING ALBUM GOES THROUGH
    # First filter: if overall score > 0.90, then album is a match (manually checked this)
    # 2nd filter: if overall score <= 0.90, then check that both accl artist and album are included or highly ratioed in spot artist and album...
    # Check if spotify year = acclaimed year and increase ratio if true
    if overall_similarity_ratio > 0.90:
        overall_similarity_ratio += 3.7
    if accl_year == spot_album_year:
        overall_similarity_ratio += 0.3
    # # Check if 'Deluxe' reduce similarity????
    # if 'deluxe' in spot_album_name:
    #     overall_similarity_ratio -= 0.3

    return overall_similarity_ratio, artist_similarity_ratio, album_similarity_ratio


# FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
# NEED TO CHANGE THIS TO CREATE HIGHER QUALITY MATCHES FOR ARTIST/ALBUMS
def get_album_match(spotify_results_list, accl_artist, accl_album, accl_year, list_data):

    top_album_overall_score = 0
    top_album_artist_score = 0
    top_album_score = 0
    top_album_id = None 
    top_album_artist_name = None 
    top_album_name = None 

    for result in spotify_results_list:
        spot_album_id = result['id']
        spot_artist_name = result['artists'][0]['name'] # may need to change encoding here
        spot_album_name = result['name'] # may need to change encoding here
        spot_album_year = int(result['release_date'][:4])
        # print(spot_album_id)

        similarity = similarity_score(accl_artist, 
                                      accl_album, 
                                      spot_artist_name, 
                                      spot_album_name,
                                      accl_year, 
                                      spot_album_year)
        
        # # PRINT RESULTS FROM BOTH SITES, ALONG W/SIMILARITY
        # print(f'''REAL ARTIST: {accl_artist}
        #       === REAL ALBUM: {accl_album} - YEAR: {accl_year}''')
        # try:
        #     print(f'''SPOTIFY ARTIST: {spot_artist_name}
        #           === SPOTIFY ALBUM: {spot_album_name} - YEAR: {spot_album_year}''')
        # except UnicodeEncodeError as e:
        #     print('Unable to print due to Unicode Error!!!')
        # print(f'''SIMILARITY: {similarity[0]:.2f}''')
        # print()
        if similarity[0] > top_album_overall_score:
            top_album_id = spot_album_id
            top_album_artist_name = spot_artist_name
            top_album_name = spot_album_name
            top_album_overall_score = similarity[0]
            top_album_artist_score = similarity[1]
            top_album_score = similarity[2]


    # add an upper limit to reject albums below that limit
    limit = 0.35

    # ADD THE ALBUM DATA TO A DICTIONARY
    data = {
        'spot_top_album_id': top_album_id, 
        'spot_top_album_artist_name': top_album_artist_name, 
        'accl_album_artist_name': accl_artist, 
        'top_album_artist_score': top_album_artist_score, 
        'spot_top_album_name': top_album_name, 
        'accl_album_name': accl_album, 
        'top_album_score': top_album_score, 
        'top_album_overall_score': top_album_overall_score, 
        'year': accl_year,
        'album_found': True if top_album_overall_score > limit else False, 
        }
    list_data.append(data)

    # TODO - IF SIMILARTY SCORE IS BELOW X AMOUNT, DON'T ADD THE ALBUM
    if top_album_overall_score < limit or top_album_id == None:
        print(f'''there is no match for this album: {accl_artist} {accl_album}''')
        return None 
    
    print(f'''ADDED TO SPOTIFY: {top_album_artist_name} - {top_album_name}''')
    return data 