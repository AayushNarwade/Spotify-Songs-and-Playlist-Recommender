import os
import requests
import en_core_web_md
from dotenv import load_dotenv
from src.fetch_lastfm import get_artist_top_tags

# Load environment variables from .env
load_dotenv()

# Load the correct spaCy model with proper vectors
nlp = en_core_web_md.load()

# Semantic similarity function
def is_semantically_similar(tag, target, threshold=0.6):
    try:
        return nlp(tag.replace("-", " ")).similarity(nlp(target)) > threshold
    except:
        return False

# Get Spotify access token (Client Credentials Flow)
def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_url = "https://accounts.spotify.com/api/token"

    response = requests.post(
        auth_url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret)
    )

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to get Spotify token")

# Get Spotify artist ID
def get_artist_id(artist_name, token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}

    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    if "artists" in data and data["artists"]["items"]:
        return data["artists"]["items"][0]["id"]
    return None


def get_top_tracks_filtered_by_tags(artist_name, genre, mood, token, lastfm_api_key):
    artist_id = get_artist_id(artist_name, token)
    if not artist_id:
        return []

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"market": "US"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return []

    tracks = response.json().get("tracks", [])
    matching_songs = []

    for track in tracks:
        track_tags = get_artist_top_tags(artist_name, lastfm_api_key)

        if any(is_semantically_similar(tag, genre) for tag in track_tags) and \
           any(is_semantically_similar(tag, mood) for tag in track_tags):
            song_info = {
                "name": track["name"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "popularity": track["popularity"],
                "spotify_url": track["external_urls"]["spotify"],
                "cover_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "tags": track_tags
            }
            matching_songs.append(song_info)

    return matching_songs


def get_tracks_by_year(year, token, limit=50):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}

    all_tracks = []
    batch_size = 50
    for offset in range(0, limit, batch_size):
        params = {
            "q": f"year:{year}",
            "type": "track",
            "market": "US",
            "limit": batch_size,
            "offset": offset
        }

        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code} – {response.text}")
            break

        batch = response.json().get("tracks", {}).get("items", [])
        if not batch:
            break

        all_tracks.extend(batch)

    return all_tracks


def clean_track_data(raw_tracks):
    cleaned_tracks = []

    for track in raw_tracks:
        try:
            cleaned = {
                "name": track.get("name", ""),
                "artists": track.get("artists", []),  # required by Last.fm tagging
                "album": track.get("album", {}).get("name", ""),
                "release_date": track.get("album", {}).get("release_date", ""),
                "cover_url": track.get("album", {}).get("images", [{}])[0].get("url"),
                "popularity": track.get("popularity", 0),
                "spotify_url": track.get("external_urls", {}).get("spotify", "")
            }
            cleaned_tracks.append(cleaned)
        except Exception as e:
            print(f"Error cleaning track: {e}")
            continue

    return cleaned_tracks



# Testing
# token = get_spotify_token()
# tracks = get_tracks_by_year(2015, token)
# print(f"Fetched {len(tracks)} tracks")



#
# # Optional: test run
# if __name__ == "__main__":
#     artist = "Coldplay"
#     genre = "indie"
#     mood = "relaxing"
#     token = get_spotify_token()
#     lastfm_api_key = os.getenv("LASTFM_API_KEY")
#
#     songs = get_top_tracks_filtered_by_tags(artist, genre, mood, token, lastfm_api_key)
#
#     for song in songs:
#         print(f"{song['name']} — {song['tags']}")
