import os
import sys
import requests
import shutil
import time

def get_image_purity(image_id, api_key):
    api_url = f"https://wallhaven.cc/api/v1/w/{image_id}?apikey={api_key}"
    response = requests.get(api_url)
    data = response.json()
    return data["data"]["purity"]

def main():
    folder_path = sys.argv[1]
    api_key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api.key")
    with open(api_key_file, "r") as f:
        api_key = f.read().strip()
    
    for file in os.listdir(folder_path):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join(folder_path, file)
            image_id = file.split("-")[-1].split(".")[0]
            print(f"Checking image {image_id}...")
            try:
                purity = get_image_purity(image_id, api_key)
                dest_folder = os.path.join(folder_path, purity)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(image_path, os.path.join(dest_folder, file))
                print(f"Moved image {file} to folder {purity}.")
            except:
                print(f"Could not determine purity for image {file}.")
                continue
            time.sleep(2)  # add a 2 second delay between API calls

if __name__ == "__main__":
    main()
