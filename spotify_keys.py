import requests
from refresh_token import refresh_token

# post request requirements to get a new access token from the refresh token; uses encoded client_id:client_secret obatined from postman snippet
url = "https://accounts.spotify.com/api/token"
payload = f'grant_type=refresh_token&refresh_token={refresh_token}'
headers = {
  'Authorization': 'Basic MzNjNmQ5M2MxZjZiNGE2N2E3YmI3MzhiN2MxZWEzNzA6OThhNzY5NjY3Nzc1NDljYmIzNTRhMWI5OTYxOTc4ZTI=',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__Host-device_id=AQD50xdWI8NLcNIo85P1qYZ7A0YjanF65t6gaWSck1uDvcvK5XBHLTKwIDnj6E34KBGVF6lKw-xIVK_da9w_R-WUheu6-Vn4eCs; sp_tr=false'
}

# store the token
def get_token():
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        access_token = response.json()
        # print(access_tokens)
        return access_token['access_token'] # to get the actual token: access_token['access_token']
    else: 
        print(response.status_code)
        return response.status_code 

# print(get_token())