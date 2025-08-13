import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

from src.fetch_spotify import get_spotify_token, get_top_tracks_filtered_by_tags
from src.recommendation_engine import generate_recommendations_from_description


load_dotenv()
lastfm_api_key = os.getenv("LASTFM_API_KEY")

# Set page
st.set_page_config(page_title="🎶 Music Mood Recommender", layout="centered")
st.title("🎶 Semantic Music Recommendation App")

# Tabs
tab1, tab2 = st.tabs(["🎧 Artist-Based Search", "🧠 Description-Based Search"])

# --------------- TAB 1 -----------------
with tab1:
    st.subheader("🎯 Artist Mood & Genre Based Recommender")
    st.markdown("Find songs by your favorite artist based on **mood** and **genre**.")

    with st.form(key="input_form"):
        artist_name = st.text_input("🎤 Artist Name", "Sabrina Carpenter")
        genre = st.text_input("🎸 Genre (e.g., rock, pop)", "pop")
        mood = st.text_input("😌 Mood (e.g., relaxing, energetic)", "love")
        submit = st.form_submit_button("🎧 Get Songs")

    if submit:
        with st.spinner("⏳ Searching for tracks..."):
            try:
                token = get_spotify_token()
                songs = get_top_tracks_filtered_by_tags(artist_name, genre, mood, token, lastfm_api_key)

                if songs:
                    songs.sort(key=lambda x: x["popularity"], reverse=True)
                    st.success(f"✅ Found {len(songs)} matching songs")

                    for song in songs:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            if song["cover_url"]:
                                st.image(song["cover_url"], width=200)

                        with col2:
                            st.markdown(f"### 🎵 **{song['name']}**")
                            st.markdown(f"**🎼 Album:** *{song['album']}*")
                            formatted_date = song['release_date']
                            try:
                                date_obj = datetime.strptime(song['release_date'], "%Y-%m-%d")
                                formatted_date = date_obj.strftime("%B %d, %Y")
                            except:
                                pass
                            st.markdown(f"**📅 Release Date:** `{formatted_date}`")
                            st.markdown(f"**📈 Popularity:** `{song['popularity']}`")
                            st.markdown(f"**🏷 Tags:** `{', '.join(song['tags'][:10])}`")
                            st.markdown(f"[▶️ Listen on Spotify]({song['spotify_url']})")

                        st.markdown("---")
                else:
                    st.warning("😕 No songs found. Try adjusting genre or mood.")

            except Exception as e:
                st.error(f"🚨 Error: {e}")

# --------------- TAB 2 -----------------
with tab2:
    st.subheader("🧠 Mood Description Based Playlist Generator")
    st.markdown("Describe your music mood and get song recommendations!")

    with st.form(key="desc_form"):
        description = st.text_input("📝 Describe the mood/genre you want (e.g. sad indie rock for night walks)")
        year = st.number_input("📅 Year of Release", min_value=1950, max_value=2025, value=2015)
        submit2 = st.form_submit_button("🎼 Recommend Songs")

    if submit2:
        with st.spinner("🔍 Analyzing and fetching music..."):
            try:
                result = generate_recommendations_from_description(description, year, lastfm_api_key)
                filtered_tracks = result["filtered_tracks"]

                if filtered_tracks:
                    filtered_tracks.sort(key=lambda x: x["popularity"], reverse=True)
                    st.success(f"✅ Found {len(filtered_tracks)} matching songs for your mood description!")

                    for song in filtered_tracks:
                        col1, col2 = st.columns([1, 2])

                        # -- Cover Image
                        with col1:
                            image_url = song.get("cover_url") or song.get("album", {}).get("images", [{}])[0].get("url", None)
                            if image_url:
                                st.image(image_url, width=200)

                        # -- Song Details
                        with col2:
                            st.markdown(f"### 🎵 **{song.get('name', 'Unknown')}**")

                            album_name = song.get("album", {}).get("name", "Unknown") \
                                if isinstance(song.get("album"), dict) else song.get("album", "Unknown")
                            st.markdown(f"**🎼 Album:** *{album_name}*")

                            # Format release date
                            release_date = song.get("release_date", "Unknown")
                            try:
                                date_obj = datetime.strptime(release_date, "%Y-%m-%d")
                                release_date = date_obj.strftime("%B %d, %Y")
                            except:
                                pass
                            st.markdown(f"**📅 Release Date:** `{release_date}`")

                            st.markdown(f"**📈 Popularity:** `{song.get('popularity', 'N/A')}`")

                            tags = ", ".join(song.get("tags", [])[:10])
                            st.markdown(f"**🏷 Tags:** `{tags}`")

                            spotify_url = song.get("spotify_url", "#")
                            st.markdown(
                                f'<a href="{spotify_url}" target="_blank">▶️ Listen on Spotify</a>',
                                unsafe_allow_html=True
                            )

                        st.markdown("---")
                else:
                    st.warning("😕 No matching songs found. Try changing your description or year.")

            except Exception as e:
                st.error(f"🚨 Error: {e}")
