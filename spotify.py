import requests, json
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
def add_tracks_to_playlist(playlist_id, artist_album, year, access_token):

  # SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT  
  url = f"https://api.spotify.com/v1/search/?q={artist_album}&type=album&limit=1"
  headers = {'Authorization': f'Bearer {access_token}'}
  search = requests.request("GET", url, headers=headers)
  # print(search.text)
  search_json = search.json() 
  album_id = search_json['albums']['items'][0]['id']
  artist_name = search_json['albums']['items'][0]['artists'][0]['name'] # may need to change encoding here
  album_name = search_json['albums']['items'][0]['name'] # may need to change encoding here
  # print(album_id)
  acclaimed_music_album_name = artist_album.replace('%20', ' ')
  spotify_search_album_name = f'{artist_name} {album_name}'

  # CHECK SIMILARITY BW THE TWO ALBUMS
  def similarity_score(str1, str2):
    # Convert the strings to lowercase to make the comparison case-insensitive
    str1 = str1.lower()
    str2 = str2.lower()
    # Calculate the similarity ratio between the two strings
    similarity_ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio
  print(f'''REAL ALBUM: {acclaimed_music_album_name} - YEAR: {year}''')
  print(f'''SPOTIFY SEARCH: {spotify_search_album_name} - SIMILARITY: {""}''')
  print()

  # RETRIEVE INDIVIDUAL ALBUM TRACKS IN ORDER 
  url = f"https://api.spotify.com/v1/albums/{album_id}"
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
  return add_tracks_to_playlist