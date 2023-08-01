import requests

r = requests.get('https://www.rollingstone.com/music/music-lists/50-best-albums-of-2016-119690/')
# returns response object
print(r) 

# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.get('https://httpbin.org/get', params=payload)
print(r.content)