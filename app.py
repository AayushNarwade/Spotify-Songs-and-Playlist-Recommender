import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
# Import project modules
from src.fetch_spotify import get_spotify_token, get_top_tracks_filtered_by_tags

# Load environment variables from .env
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="🎶 Artist Mood Recommender", layout="centered")
st.title("🎶 Fav. Artist Song Recommender")

# Description
st.markdown("""
Find songs by your favorite artist based on **mood** and **genre** using semantic tag matching powered by Last.fm + Spotify + spaCy.
""")

# Input form
with st.form(key="input_form"):
    artist_name = st.text_input("🎤 Artist Name", "Sabrina Carpenter")
    genre = st.text_input("🎸 Genre (e.g., rock, pop)", "pop")
    mood = st.text_input("😌 Mood (e.g., relaxing, energetic)", "love")
    submit = st.form_submit_button("🎧 Get Songs")

# On form submission
if submit:
    with st.spinner("⏳ Searching for tracks..."):
        try:
            # Get tokens and API keys
            token = get_spotify_token()
            lastfm_api_key = os.getenv("LASTFM_API_KEY")

            # Fetch songs
            songs = get_top_tracks_filtered_by_tags(artist_name, genre, mood, token, lastfm_api_key)

            if songs:
                # Sort by popularity descending
                songs.sort(key=lambda x: x["popularity"], reverse=True)
                st.success(f"✅ Found {len(songs)} matching songs for *{artist_name}* with genre *{genre}* and mood *{mood}*:")

                for song in songs:
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if song["cover_url"]:
                            st.image(song["cover_url"], width=200, use_container_width=False)

                    with col2:
                        st.markdown(f"### 🎵 **{song['name']}**")
                        st.markdown(f"**🎼 Album:** *{song['album']}*")
                        try:
                            date_obj = datetime.strptime(song['release_date'], "%Y-%m-%d")
                            formatted_date = date_obj.strftime("%B %d, %Y")  # e.g., June 5, 2025
                        except:
                            formatted_date = song['release_date']  # fallback if formatting fails

                        st.markdown(f"**📅 Release Date:** `{formatted_date}`")
                        st.markdown(f"**📈 Popularity:** `{song['popularity']}`")

                        # Limit to first 10 tags and add tooltip for full tag list
                        short_tags = ', '.join(song['tags'][:10])
                        full_tags = ', '.join(song['tags'])
                        st.markdown(f"**🏷 Tags:** `{short_tags}`")

                        st.markdown(f"[▶️ Listen on Spotify]({song['spotify_url']})")

                    st.markdown("---")



            else:
                st.warning("😕 No songs found for that combination. Try changing the mood or genre.")

        except Exception as e:
            st.error(f"🚨 Error: {e}")




#Section 2 Inputs

st.subheader("🎯 Mood Description based Playlist Generator")
st.text("🛠️🔧 Under Construction 🔧🛠️")
# with st.form(key = "description_form"):
#     description = st.text_input("📝 Describe the type of Music you want:")
#     year = st. number_input("📅 Year", min_value = 1850, max_value= 2025, step = 1)
#     submit2 = st.form_submit_button("🎼 Recommend Songs")
