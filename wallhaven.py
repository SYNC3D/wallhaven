import requests
import urllib3
import os
import shutil
import argparse

#This section is accepting external commands from the command Line
parser = argparse.ArgumentParser()

parser.add_argument('categories')
parser.add_argument('purity')

args = parser.parse_args()

#Determining your home directory and then downloading to the Pictures folder
home_directory = os.path.expanduser( '~' )
path_to_downloads = os.path.join( home_directory, 'Pictures', 'Downloaded/' )
path_to_keep = os.path.join( path_to_downloads, 'Keep/' )

http = urllib3.PoolManager()
paths = []
downloaddir = path_to_downloads

#First moving all files already Download
for file_name in os.listdir(path_to_downloads):
    # construct full file path
    source = path_to_downloads + file_name
    destination = path_to_keep + file_name
    # move only files
    if os.path.isfile(source):
        shutil.move(source, destination)
        print('Moved:', file_name)

# You can change the parameters below.

parameters = {
    "categories": args.categories,
    "purity": args.purity,
    "sorting": "random",
    "atleast": "1920x1080",
    "ratios": "16x9",
}
# This is where you have to insert your apikey. Not sure whether I should hardcode it or load it
# from somewhere else. I suspect it might be better to load it from somewhere else.

response = requests.get(
    "https://wallhaven.cc/api/v1/search?apikey=SduhMlFOWiBPTgIOPpjKK9uq6w63noqV", params=parameters)

# Calling the API and storing the output in a dictionary

data = response.json()['data']
for d in data:
    url = d['path']
    paths.append(url)
##
# Reading the Dictionary one item at a time and downloading it.
for I in paths:
    url = I
    url2 = I
    print(I)
    if url2.find('/'):
        url3 = (url2.rsplit('/', 1)[1])
        completeName = os.path.join(downloaddir, url3)
    data = requests.get(url)
    # Save file data to local copy
    with open(completeName, 'wb')as file:
        file.write(data.content)
