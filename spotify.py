import requests, json
from spotify_keys import get_tokens, api_code

# WILL NEED TO GET THE CODE FIRST, THEN USE CODE TO GET ACCESS_TOKEN WHICH EXPIRES IN 1HR, THEN TAKE THE REFRESH_TOKEN IN RESPONSE OF ACCESS_TOKEN AND USE IT IN PLACE OF THE CODE KEY TO MAKE ANOTHER ACCESS_TOKEN REQUEST BUT WITH REFRESH_TOKEN VS GET CODE. REPEAT AS NEEDED. 

# access_tokens = get_tokens() # this returns a dict
# while access_tokens is not None: # will prob have to change this to time 3600 seconds from when get_tokens() gets called, to 
#   access_token = access_tokens['access_token']
#   refresh_token = access_tokens['refresh_token']


# TEMPORARY DELETE LATER
access_token = 'BQBsxotnCtKv0rXUmXsk932NaMNwMjQUna1HBptsXGIxSJuc3_aadM2a7AX6PbweLb7xc75mPz9Kn4SlTO8NM_AkI9UDEpx29EAFZ-1Beurk13XY5sd_yVYS4mSUfMxbeBU6aq0HY0KWj1k6xA1DJF8WxiMqPCOV8TD0AyBSmGG3NsHEQCKlvBVSFbjds5tAKXZPml2lxpfXD6Jv8bsYMT3tqqIYCFwDdf09HAYwUl2hoMRgy9GK3bOx'

refresh_token = 'AQDI3fChzjaRvRwpiE928Z9QHgpt918U0u2gbw418aJHBWnG41pgTG_ZXwqlLmaz--0Jhx-iHLSt5CW4wyNe-JU-hFaFGqg23hBpezZW1tcxFLcxJECHvoFQH2XFSphF0js'

# FOR EACH YEAR
# CREATE A NEW PLAYLIST
def create_new_playlist(year):
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
def add_tracks_to_playlist(playlist_id, album):

  # SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT  
  url = f"https://api.spotify.com/v1/search/?q={album}&type=album&limit=1"
  headers = {'Authorization': f'Bearer {access_token}'}
  search = requests.request("GET", url, headers=headers)
  # print(search.text)
  search_json = search.json() 
  album_id = search_json['albums']['items'][0]['id']
  artist_name = search_json['albums']['items'][0]['artists'][0]['name']
  album_name = search_json['albums']['items'][0]['name']
  # print(album_id)
  print(f'''SPOTIFY SEARCH: {artist_name}, {album_name}''')

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