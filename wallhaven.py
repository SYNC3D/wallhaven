import requests
import json
import urllib3
import wget

http = urllib3.PoolManager()
paths = []

parameters = {
    "categories": "101",
    "purity": "010",
    "sorting": "random",
    "resolutions": "1920x1080",
    "ratio": "16x9"
}

response = requests.get(
    "https://wallhaven.cc/api/v1/search?apikey=SduhMlFOWiBPTgIOPpjKK9uq6w63noqV", params=parameters)


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


data = response.json()['data']
for d in data:
    url = d['path']
    paths.append(url)

print(paths)
for I in paths:
    url = I
    url2 = I
    if url2.find('/'):
        url3 = (url2.rsplit('/', 1)[1])
    data = requests.get(url)
    # Save file data to local copy
    with open(url3, 'wb')as file:
        file.write(data.content)
