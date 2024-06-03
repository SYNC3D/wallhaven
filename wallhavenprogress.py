import requests
import urllib3
import os
import shutil
import argparse
import logging
from pathlib import Path
from tqdm import tqdm
import concurrent.futures


def download_image(url, path_to_downloads):
    if '/' in url:
        url1 = url.rsplit('/', 1)[1]
        complete_name = path_to_downloads / url1
        try:
            data = requests.get(url)
            data.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Error downloading image: {url1}")
            return

        # Save file data to local copy
        with complete_name.open('wb') as file:
            file.write(data.content)
            logging.info(f"Downloaded: {url1}")


def download_images(category, purity, num_threads=4):
    # Creating directories if they do not exist
    path_to_downloads = Path.home() / 'Pictures' / 'Downloaded'
    path_to_keep = path_to_downloads / 'Keep'
    path_to_downloads.mkdir(parents=True, exist_ok=True)
    path_to_keep.mkdir(exist_ok=True)

    # First moving all files already downloaded
    for file_path in path_to_downloads.glob('*'):
        if file_path.is_file():
            destination = path_to_keep / file_path.name
            shutil.move(str(file_path), str(destination))
            logging.info(f"Moved: {file_path.name}")

    # You can change the parameters below.
    parameters = {
        "categories": category,
        "purity": purity,
        "sorting": "random",
        "atleast": "1920x1080",
        "ratios": "16x9",
    }

    # Your API must be in a file called api.key in the same directory as this script
    api_key_file = Path(__file__).parent / 'api.key'
    with api_key_file.open() as f:
        contents = f.read().strip()
        api_key = f"https://wallhaven.cc/api/v1/search?apikey={contents}"
        try:
            response = requests.get(api_key, params=parameters)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Error retrieving images: {error}")
            return

    # Calling the API and storing the output in a dictionary
    data = response.json()['data']
    urls = [d['path'] for d in data]
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(download_image, url, path_to_downloads) for url in urls]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            pass


if __name__ == '__main__':
    # This section is accepting external commands from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('categories')
    parser.add_argument('purity')
    parser.add_argument('--threads', '-t', type=int, default=2)
    args = parser.parse_args()

    # Setting up logging
    logging.basicConfig(
        filename='image_downloader.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    download_images(args.categories, args.purity, args.threads)
