from dotenv import load_dotenv
import os
from src.recommendation_engine import generate_recommendations_from_description

load_dotenv()
lastfm_api_key = os.getenv("LASTFM_API_KEY")

desc = "I want some energetic and romantic pop music"
year = 2010

result = generate_recommendations_from_description(desc, year, lastfm_api_key)
print("Selected Tags:", result["selected_tags"])
print("Unique Tags:", result["unique_tags"])
print("Tracks Returned:", len(result["filtered_tracks"]))
