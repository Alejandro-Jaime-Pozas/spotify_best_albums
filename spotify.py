import requests, re, json, difflib
from steps_add_to_playlist import album_search_list, similarity_score, get_album_tracks, add_tracks_to_spotify

# FOR EACH YEAR
# CREATE A NEW PLAYLIST
def create_new_playlist(year, access_token):
  url = "https://api.spotify.com/v1/users/alexjaime/playlists"
  payload = json.dumps({
    "name": f"{year} Best Albums"
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}' # CHANGE THIS LATER TO AUTOMATE ACCESS_TOKEN
  }
  new_playlist = requests.request("POST", url, headers=headers, data=payload)
  # print(response.json())
  playlist = new_playlist.json()
  playlist_id = playlist['id']
  # print(playlist_id)
  return playlist_id


# FOR EACH ALBUM
def add_tracks_to_playlist(playlist_id, artist_album, year, list_data, access_token):

  # SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT AND RETURN MULTIPLE ALBUM RESULTS
  spotify_results_list = album_search_list(artist_album, access_token)
  acclaimed_music_album_name = artist_album.replace('%20', ' ')
  
  
  top_album_score = 0
  top_album_id = None 
  top_album_spotify_name = None 
  # FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
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

  # ADD THE ALBUM DATA TO A LIST AS TUPLE, THEN 
  data = top_album_id, top_album_spotify_name, acclaimed_music_album_name, top_album_score, True if top_album_score > 0.35 else False, year
  list_data.append(data)

  # IF SIMILARTY SCORE IS BELOW X AMOUNT, DON'T ADD THE ALBUM
  if top_album_score < 0.35 or top_album_id == None:
    print(f'there is no match for this album: {acclaimed_music_album_name}')
    return None 

  # RETRIEVE INDIVIDUAL ALBUM TRACKS IN ORDER for the highest match
  tracks = get_album_tracks(top_album_id, access_token)

  #  FEED LIST OF TRACKS TO THE ADD TO PLAYLIST ENDPOINT
  tracks_added_to_playlist = add_tracks_to_spotify(playlist_id, tracks, access_token, top_album_score)

  return tracks_added_to_playlist