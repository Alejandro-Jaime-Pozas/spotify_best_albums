import requests
# get manually from copy pasting postman url to browser and getting the code in query params
api_code = """AQBRvFbuHtbga471GYsoQNlnooJZclPlx-bXpl0gDltacrwKJdj3gqvBMqKTQVcPE_0M-PswItsGU5Uk_IHMhEKaR7Im9jEPSdP98mMdwzF8FTC3S6KnVCAAM6MjDD0XPJdT6BivYa34DEoSn8S3nP3symwe772pMBo_bundVAcSIqQzjdqNzywB_GBrKNCyFjFWVi9iIEWtgZleGSTojH9jCqDqr71s6Rr3CZ6FkntElfquAXQvlApr0SrL8g"""

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
        access_tokens = response.json() # use refresh_token key code to replace original api_code once the access_token expires in 1hr, only need to include grant_type=refresh_token&refresh_token={refresh_token} in payload for this
        return access_tokens # to get the actual tokens: access_tokens['access_token'] or ['refresh_token']

    else: 
        print(response.status_code)
        return None 

# print(get_tokens())