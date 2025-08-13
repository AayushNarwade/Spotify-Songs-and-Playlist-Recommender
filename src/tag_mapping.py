seed_tag_dict = {
    # Mood-based
    "calm": ["calm", "soothing", "mellow", "relaxing", "chill", "tranquil", "ambient"],
    "happy": ["happy", "cheerful", "uplifting", "positive", "joyful", "bright"],
    "sad": ["sad", "melancholy", "emotional", "blue", "heartbroken", "downbeat"],
    "energetic": ["energetic", "upbeat", "fast", "lively", "motivational", "intense"],
    "romantic": ["romantic", "love", "passionate", "sensual", "intimate"],
    "dark": ["dark", "moody", "gloomy", "introspective", "haunting"],
    "epic": ["epic", "powerful", "cinematic", "grand", "anthemic", "dramatic"],

    # Genre-based
    "rock": ["rock", "alt rock", "indie rock", "hard rock", "punk", "garage rock"],
    "pop": ["pop", "synthpop", "electropop", "teen pop", "pop rock"],
    "hip hop": ["hip hop", "rap", "trap", "boom bap", "conscious rap"],
    "electronic": ["electronic", "edm", "house", "techno", "trance", "dubstep"],
    "jazz": ["jazz", "smooth jazz", "bebop", "fusion", "swing"],
    "classical": ["classical", "orchestral", "symphony", "baroque", "piano"],
    "indie": ["indie", "indie pop", "indie folk", "indietronica"],
    "lo-fi": ["lo-fi", "lofi", "study beats", "chillhop", "downtempo"],
    "metal": ["metal", "heavy metal", "death metal", "thrash", "black metal"],
    "folk": ["folk", "acoustic", "americana", "bluegrass", "singer-songwriter"],
    "funk": ["funk", "groove", "soul", "disco", "neo soul"],

    # Region-based
    "bollywood": ["bollywood", "hindi", "desi", "indian pop"],
    "k-pop": ["k-pop", "korean pop", "korean", "kpop"],
    "j-pop": ["j-pop", "japanese pop", "anime", "japanese"],
    "latin": ["latin", "reggaeton", "latin pop", "salsa", "bachata"],
    "uk": ["uk drill", "grime", "british rap", "uk pop", "british"],
    "punjabi": ["punjabi", "bhangra", "panjabi", "punjabi pop"],
    "french": ["french", "chanson", "french pop", "francophone"],
    "afrobeat": ["afrobeat", "afropop", "nigerian pop", "afrofusion"],
}

def map_tag_to_seed(tag):
    for seed, variations in seed_tag_dict.items():
        if tag.lower() in variations:
            return seed
    return tag.lower

