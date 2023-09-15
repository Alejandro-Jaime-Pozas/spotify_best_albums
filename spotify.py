import requests, json, difflib
from spotify_keys import get_token


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
  url = f"https://api.spotify.com/v1/search/?q={artist_album}&type=album&limit=6" # CHANGE LIMIT HERE!!
  headers = {'Authorization': f'Bearer {access_token}'}
  search = requests.request("GET", url, headers=headers)
  # print(search.text)
  search_json = search.json() 
  results_list = search_json['albums']['items'] # contains multiple album results for search query

  acclaimed_music_album_name = artist_album.replace('%20', ' ')


  # FUNCTION TO CHECK SIMILARITY BW ACCLAIMED VS SPOTIFY
  def similarity_score(str1, str2):
    # Convert the strings to lowercase to make the comparison case-insensitive
    str1 = str1.lower()
    str2 = str2.lower()
    # Calculate the similarity ratio between the two strings
    similarity_ratio = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
    return similarity_ratio
  
  top_album_score = 0
  # FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
  for result in results_list:
    album_id = result['id']
    artist_name = result['artists'][0]['name'] # may need to change encoding here
    album_name = result['name'] # may need to change encoding here
    # print(album_id)
    spotify_search_album_name = f'''{artist_name} {album_name}'''
    similarity = similarity_score(acclaimed_music_album_name, spotify_search_album_name)
    # PRINT RESULTS FROM BOTH SITES, ALONG W/SIMILARITY
    print(f'''REAL ALBUM: {acclaimed_music_album_name} - YEAR: {year}''')
    try:
      print(f'''SPOTIFY SEARCH: {spotify_search_album_name}''')
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
  if top_album_score < 0.35:
    print(f'there is no match for this album: {acclaimed_music_album_name}')
    return None 
  

  # RETRIEVE INDIVIDUAL ALBUM TRACKS IN ORDER for the highest match
  url = f"https://api.spotify.com/v1/albums/{top_album_id}"
  headers = {'Authorization': f'Bearer {access_token}'}
  album_tracks = requests.request("GET", url, headers=headers)
  # print(album_tracks.text.encode("utf-8"))
  album_tracks_json = album_tracks.json() 
  tracks = [track['uri'] for track in album_tracks_json['tracks']['items']]
  # print(tracks)

  #  FEED LIST OF TRACKS TO THE ADD TO PLAYLIST ENDPOINT
  url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" # REPLACE WITH PLAYLIST_ID
  payload = json.dumps({"uris": tracks})
  headers = {'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'}
  add_tracks_to_playlist = requests.request("POST", url, headers=headers, data=payload)
  # print(add_tracks_to_playlist.text)

  print(f'album w/similarity = {top_album_score:.2f} was added\n')
  return add_tracks_to_playlist