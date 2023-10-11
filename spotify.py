import requests, json
from steps_add_to_playlist import album_search_list, similarity_score, get_album_tracks, add_tracks_to_spotify, get_album_match

# FOR EACH YEAR
# CREATE A NEW PLAYLIST
def create_new_playlist(genre_name, access_token):
  url = "https://api.spotify.com/v1/users/alexjaime/playlists"
  payload = json.dumps({
    # "name": f"{year} Best Albums" # CHANGE BACK!!!
    "name": f"{' '.join((genre_name.split()[1:-1]))} Best Albums"
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
  # pass 


# FOR EACH ALBUM, SEATCH AND ADD ALBUM TRACKS TO YEAR PLAYLIST
def add_tracks_to_playlist(playlist_id, accl_artist, accl_album, accl_year, list_data, access_token):

  # SEARCH FOR THE ARTIST/ALBUM PAIR IN SEARCH ENDPOINT AND RETURN MULTIPLE ALBUM RESULTS
  spotify_results_list = album_search_list(accl_artist, accl_album, access_token)
  

  # FOR EACH ALBUM RESULT, COLLECT ITS SIMILARITY TO ACCLAIMED MUSIC ALBUM, RETURN THE HIGHEST RESULT MATCH
  data = get_album_match(spotify_results_list, accl_artist, accl_album, accl_year, list_data)

  # RETRIEVE INDIVIDUAL ALBUM TRACKS IN ORDER for the highest match
  if data:
    tracks = get_album_tracks(data['spot_top_album_id'], access_token)

    #  FEED LIST OF TRACKS TO THE ADD TO PLAYLIST ENDPOINT
    tracks_added_to_playlist = add_tracks_to_spotify(playlist_id, tracks, access_token, data['top_album_overall_score'])

    return tracks_added_to_playlist