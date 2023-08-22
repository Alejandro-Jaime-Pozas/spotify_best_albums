import requests, json
from spotify_keys import access_token, api_code

# WILL NEED TO GET THE CODE FIRST, THEN USE CODE TO GET ACCESS_TOKEN WHICH EXPIRES IN 1HR, THEN TAKE THE REFRESH_TOKEN IN RESPONSE OF ACCESS_TOKEN AND USE IT IN PLACE OF THE CODE KEY TO MAKE ANOTHER ACCESS_TOKEN REQUEST BUT WITH REFRESH_TOKEN VS GET CODE. REPEAT AS NEEDED. 


# create a new playlist...
url = "https://api.spotify.com/v1/users/alexjaime/playlists"
payload = json.dumps({
  "name": f"1954 Best Albums"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {access_token}'
}
response = requests.request("POST", url, headers=headers, data=payload)
# print(response.json())


# search for the artist/album pair in search endpoint, retrieve all tracks in order
url = "https://api.spotify.com/v1/search/?q=wilco yankee hotel foxtrot&type=album&limit=1"
# payload = {}
headers = {
  'Authorization': f'Bearer {access_token}'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)


# compile a list of the tracks to add by relevant track id


# feed list of tracks to the add to playlist endpoint