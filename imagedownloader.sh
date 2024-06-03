#!/bin/bash

# Wallhaven API key
API_KEY="SduhMlFOWiBPTgIOPpjKK9uq6w63noqV"

# Directory paths
DOWNLOADS_DIR="$HOME/Pictures/Downloaded"
KEEP_DIR="$DOWNLOADS_DIR/Keep"

# Create directories if they do not exist
mkdir -p "$DOWNLOADS_DIR"
mkdir -p "$KEEP_DIR"

# Move existing files to the "Keep" directory
for file_path in "$DOWNLOADS_DIR"/*; do
    if [ -f "$file_path" ]; then
        destination="$KEEP_DIR/$(basename "$file_path")"
        mv "$file_path" "$destination"
        echo "Moved: $(basename "$file_path")"
    fi
done

# API parameters
CATEGORY="001"
PURITY="010"
SORTING="random"
ATLEAST="1920x1080"
RATIOS="16x9"

# API request
API_URL="https://wallhaven.cc/api/v1/search?apikey=$API_KEY"
API_PARAMS="categories=$CATEGORY&purity=$PURITY&sorting=$SORTING&atleast=$ATLEAST&ratios=$RATIOS"
API_REQUEST="$API_URL&$API_PARAMS"

# Get image URLs from the API response
api_response=$(curl -s "$API_REQUEST")
image_urls=$(echo "$api_response" | jq -r '.data[].path')

# Check if image_urls is null or empty
if [ -z "$image_urls" ]; then
    echo "No image URLs found in API response. Exiting."
    exit 1
fi

# Function to download an image
download_image() {
    local url="$1"
    local filename=$(basename "$url")
    
    # Download the image using curl
    curl -s -o "$DOWNLOADS_DIR/$filename" "$url"
    
    if [ $? -eq 0 ]; then
        echo "Downloaded: $filename"
    else
        echo "Error downloading: $filename"
    fi
}

# Download images sequentially
for url in $image_urls; do
    download_image "$url"
done