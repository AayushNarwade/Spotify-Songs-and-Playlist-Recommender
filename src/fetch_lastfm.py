import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Updated to accept api_key as argument (for flexibility)
def get_artist_top_tags(artist_name, api_key=None):
    if api_key is None:
        api_key = os.getenv("LASTFM_API_KEY")

    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "toptags" in data and "tag" in data["toptags"]:
            tags = [tag["name"] for tag in data["toptags"]["tag"]]
            return tags
        else:
            return []
    else:
        print(f"Error: {response.status_code}")
        return []

# # Optional test block
# if __name__ == "__main__":
#     artist = "coldplay"
#     tags = get_artist_top_tags(artist)
#     print(f"Top tags for {artist}: {tags}")
