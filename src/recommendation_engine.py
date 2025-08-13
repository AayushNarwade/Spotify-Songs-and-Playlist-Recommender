from src.fetch_spotify import (
    get_spotify_token,
    get_tracks_by_year,
    clean_track_data
)
from src.tag_processing import (
    assign_tags_to_tracks,
    encode_unique_tags,
    extract_relevent_tags
)
from src.tag_mapping import map_tag_to_seed


def generate_recommendations_from_description(description, year, lastfm_api_key):
    token = get_spotify_token()

    # Step 1: Fetch tracks from Spotify
    raw_tracks = get_tracks_by_year(year, token)

    # ✅ Step 2: Clean raw track data
    cleaned_tracks = clean_track_data(raw_tracks)

    # Step 3: Assign tags to tracks using Last.fm
    tagged_tracks = assign_tags_to_tracks(cleaned_tracks, lastfm_api_key)

    # Step 4: Encode unique mapped tags
    unique_tags, _ = encode_unique_tags(tagged_tracks)

    # Step 5: Extract most relevant tags from user description
    selected_tags = extract_relevent_tags(description, unique_tags, top_n=5)

    # Step 6: Map those tags to seed categories
    mapped_seed_tags = list({map_tag_to_seed(tag) for tag in selected_tags})

    # Step 7: Filter tracks using mapped seed tags
    filtered_tracks = [
        track for track in tagged_tracks
        if any(map_tag_to_seed(tag) in mapped_seed_tags for tag in track.get("tags", []))
    ]

    return {
        "filtered_tracks": filtered_tracks,
        "selected_tags": selected_tags,
        "mapped_seed_tags": mapped_seed_tags
    }
