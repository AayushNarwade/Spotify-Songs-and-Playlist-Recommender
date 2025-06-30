from sentence_transformers import SentenceTransformer, util
from src.fetch_lastfm import get_artist_top_tags
import os
from dotenv import load_dotenv


load_dotenv()
lastfm_api_key = os.getenv("LASTFM_API_KEY")


model = SentenceTransformer("all-MiniLM-L6-v2")



def extract_relevent_tags(description, all_tags, top_n=5):
    description_embedding = model.encode(description, convert_to_tensor=True)
    tag_embeddings = model.encode(all_tags, convert_to_tensor=True)

    similarities = util.cos_sim(description_embedding, tag_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_n]

    return [all_tags[i] for i in top_indices]



def assign_tags_to_tracks(tracks, lastfm_api_key):
    for track in tracks:
        artist = track.get("artist_name", "")
        if artist:
            tags = get_artist_top_tags(artist, lastfm_api_key)
            track["tags"] = tags
        else:
            track["tags"] = []
    return tracks



def encode_unique_tags(tracks):
    tag_set = set()
    for track in tracks:
        tag_set.update(track.get("tags", []))

    unique_tags = list(tag_set)
    tag_embeddings = model.encode(unique_tags, convert_to_tensor=True)
    return unique_tags, tag_embeddings



# Testing
# if __name__ == "__main__":
#
#     description = "I want calm and emotional indie music"
#
#     tracks = [
#         {"track_name": "Fix You", "artist_name": "Coldplay"},
#         {"track_name": "Someone Like You", "artist_name": "Adele"},
#         {"track_name": "Lose Yourself", "artist_name": "Eminem"}
#     ]
#     tracks_with_tags = assign_tags_to_tracks(tracks, lastfm_api_key)
#
#     unique_tags, tag_embeddings = encode_unique_tags(tracks_with_tags)
#
#     top_tags = extract_relevent_tags(description, unique_tags, top_n=5)
#
#     print("Top tags based on description:")
#     print(top_tags)
#
#     print("\nTracks with assigned tags:")
#     for track in tracks_with_tags:
#         print(f"{track['track_name']} by {track['artist_name']} → Tags: {track['tags']}")
