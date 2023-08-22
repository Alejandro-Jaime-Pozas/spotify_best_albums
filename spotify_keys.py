import requests
# get manually from copy pasting postman url to browser and getting the code in query params
api_code = """AQCUanL815D1OcqRaaOx7fxI_2UxZp0Kj0BZzyFpbNrwH83EpPv2lYEjqGqYY5Jn_bRXP9YMDrz0hLZBO9SrfyiXMq4ksMFtVrs14_y9mE4tBgohkv8b2gwRiTgE4p-a32M0yJYqyVVrO8f8mvUgHWZBAwo70IljitBQ2kPWu6blCPuXUzzsgMG1LWWXiJdFP4MpiNONdzUAeTD-qIhFEx9uCMXGM7ixYFp_4DR-h4HIMmwQHO4yoiNARRp9Rg"""

# use code to get the access token and refresh token
url = "https://accounts.spotify.com/api/token"
payload = f'grant_type=authorization_code&code={api_code}&redirect_uri=https%3A%2F%2Flocalhost%3A3000&client_id=33c6d93c1f6b4a67a7bb738b7c1ea370&client_secret=98a76966777549cbb354a1b9961978e2'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__Host-device_id=AQD50xdWI8NLcNIo85P1qYZ7A0YjanF65t6gaWSck1uDvcvK5XBHLTKwIDnj6E34KBGVF6lKw-xIVK_da9w_R-WUheu6-Vn4eCs; __Host-sp_csrf_sid=757f7d8edc6c9c65c520fe41f1b25a8b15e262fecc31d5050460e968bb2a2074; __Secure-TPASESSION=AQDt5zvCvwn0kbZtfdRhACwrjnktTSdZe3EoNIhAD0IH+V9RVu4zMNeTuyxGypeqaSRId8MYTufbEe/iiDpQoef3Oe1eQ5mx6z4=; inapptestgroup=; sp_sso_csrf_token=013acda71961e3486356a921b66b30fd2a9898dd1c31363932363733363234373630; sp_tr=false'
}

# store the tokens
def get_tokens():
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        access_tokens = response.json() 
        access_token = access_tokens['access_token']
        refresh_token = access_tokens['refresh_token'] # use this code to replace original api_code once the access_token expires in 1hr, only need to include grant_type=refresh_token&refresh_token={refresh_token} in payload for this

        print(access_token)
        print()
        print(api_code)
        return access_tokens

    else: 
        print(response.status_code)
        return None 

print(get_tokens())