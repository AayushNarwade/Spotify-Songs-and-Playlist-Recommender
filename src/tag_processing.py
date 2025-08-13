from sentence_transformers import SentenceTransformer, util
from src.fetch_lastfm import get_artist_top_tags
import os
from dotenv import load_dotenv
from src.tag_mapping import map_tag_to_seed

# Load API Key
load_dotenv()
lastfm_api_key = os.getenv("LASTFM_API_KEY")

# Load Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_relevent_tags(description, all_tags, top_n=5):
    if not all_tags:
        raise ValueError("⚠️ No tags provided to match with the description.")

    description_embedding = model.encode(description, convert_to_tensor=True)
    tag_embeddings = model.encode(all_tags, convert_to_tensor=True)

    similarities = util.cos_sim(description_embedding, tag_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_n]

    return [all_tags[i] for i in top_indices]


def assign_tags_to_tracks(tracks, lastfm_api_key):
    for track in tracks:
        artists = track.get("artists", [])
        artist_name = artists[0]["name"] if artists else ""

        if artist_name:
            tags = get_artist_top_tags(artist_name, lastfm_api_key)
            if not tags:
                print(f"⚠️ No tags found for artist: {artist_name}")
            track["tags"] = tags
            track["artist_name"] = artist_name
        else:
            print("⚠️ No artist name found for track:", track.get("name", "Unknown Track"))
            track["tags"] = []
    return tracks


def encode_unique_tags(tracks):
    tag_set = set()

    for track in tracks:
        mapped_tags = [map_tag_to_seed(tag) for tag in track.get("tags", [])]
        mapped_tags = [tag for tag in mapped_tags if isinstance(tag, str) and tag.strip() != ""]
        track["tags"] = mapped_tags
        tag_set.update(mapped_tags)

    unique_tags = list(tag_set)

    if not unique_tags:
        raise ValueError("❌ unique_tags must be a list of strings and cannot be empty")

    tag_embeddings = model.encode(unique_tags, convert_to_tensor=True)
    return unique_tags, tag_embeddings




if __name__ == "__main__":
    from src.fetch_spotify import get_spotify_token, get_tracks_by_year, clean_track_data

    print("🧪 Running test on tag processing functions...")

    load_dotenv()
    lastfm_api_key = os.getenv("LASTFM_API_KEY")
    token = get_spotify_token()

    # Sample inputs
    year = 2010
    description = "I want some energetic and romantic pop music"

    # Step 1: Fetch tracks
    raw_tracks = get_tracks_by_year(year, token)
    tracks = clean_track_data(raw_tracks)

    # Step 2: Assign tags
    tracks = assign_tags_to_tracks(tracks[:5], lastfm_api_key)
    for i, t in enumerate(tracks):
        print(f"🎶 Track {i+1}: {t.get('name', 'Unknown')} | Artist: {t.get('artist_name')} | Tags: {t.get('tags')}")

    # Step 3: Map & encode tags
    unique_tags, tag_embeddings = encode_unique_tags(tracks)
    print(f"🧩 Unique mapped tags ({len(unique_tags)}): {unique_tags}")

    # Step 4: Extract tags from description
    selected_tags = extract_relevent_tags(description, unique_tags, top_n=5)
    print(f"🧠 Tags relevant to description:\n→ {selected_tags}")

    print("✅ Tag processing test completed.")

