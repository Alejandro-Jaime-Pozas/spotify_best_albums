import requests, json
from spotify_keys import get_token

# # TEMPORARY DELETE LATER when replacing with get_token. IF I LEAVE THIS, CODE SHOULD STILL WORK
# access_token = 'BQCKFCDwTSLEVhv-DYz3sE5zTV3cn7AuBym01_ainyXoWdNiDeSy8T6n8FdnWLeEugLQBdxq5gWWLJfwplne4SGN-a0SWgZ7NrLk34lfs_eplkoOdZW6N4sXlPnsKiIhPpzgg8iBDJegjVxhGbyQs7nHGcyaP_Zp0FBR7sdkHpOciBcGvd61mBk-dwFMBNPlBV_TrQLEw7XTqnt1565RVPIPBQojMbCvA3NW_-g3o0zvdWLBJKpkXohg'


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
def add_tracks_to_playlist(playlist_id, album, access_token):

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